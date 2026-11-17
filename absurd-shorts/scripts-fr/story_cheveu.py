#!/usr/bin/env python3
"""Le cheveu (story 88, cycle 49; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man found a hair in his soup. A police helicopter lit the soup. The hair was arrested with tweezers. Photographed from the front, then in
profile. Questioned twelve hours under the lamp. It curled; that was held against it. The dogs followed its trail to the cook. They broke down
his door. And every door in the street. The cook was bald. He was shaved anyway. Then the customers and the passers-by, for comparison. The police
dog too. This man, twice. Under the microscope: no match. The minister apologised to the hair. It was the last hair in the neighbourhood. The
helicopter put it back. In this man's soup.
Staging: at a bistro table at night (checked cloth, a big white bowl of pale golden soup, a SOUPE DU JOUR chalkboard, a window on the night behind
him) a thick black hair floats waving on the soup; he points at it, eyes down, then looks at us. Low from the table: through the window above his
head a navy police helicopter hovers and its searchlight cone drops onto the bowl, the soup flaring in a pool of light, he squints up. A gloved
policeman lifts the hair out with giant steel tweezers (it hangs, blinking) while his colleague holds an open evidence bag. Mugshot: the hair
stands on a little ledge against a pale height chart, a tiny number board hung on it; flash; it turns a quarter; flash; it looks exactly the same
(FICHÉ). In the interrogation room it stands alone on a pale metal chair under a big lamp bent down at it, an inspector leaning on the table, the
wall clock spinning. The lamp glows hot: the hair coils into a tight curl with a boing, sweating (FRISÉ); the inspector slams a stamp on its file:
RETENU. Two sniffer dogs drag their leaning handlers up the pavement toward us, then stop at the cook's feet on his doorstep, key in hand. From
inside his hallway at floor level his front door falls flat toward us, dust, masked officers with a ram in the doorway. Down the street every
front door falls inward one after the other as the ram team sprints along the pavement. The cook lifts his toque: bald, shining under an officer's
torch (CHAUVE). Tight on his head: clippers buzz across the bare scalp, nothing falls, a glint. On the pavement outside the restaurant a row of
customers and passers-by sit bald on chairs while officers buzz over their heads, piles of hair in their old colours growing at their feet, each
with a numbered evidence tag. The police dog sits shaved pink and smooth beside its handler, at attention, tongue out, its own tagged pile beside
it. He, bald, sits in the barber chair: the clippers pass, pause, pass again. In a pale lab a scientist peers into a microscope before shelves of
numbered hair bags; on the screen the two samples, a scan line, then a big red cross. In the press room the minister bows deeply to the hair
standing on a little red-cushioned stand beside the podium, flashes popping. Crane down over a square of shining bald heads (and the pink dog)
round the hair alone on its stand, which looks up at us. Night: the helicopter lowers the hair on its winch cable through the window toward the
bowl, searchlight on, he looks up, bald. The framing of the first shot: he, bald, before the same bowl; the hair drops onto the soup, a ripple,
it floats and opens two little eyes at him; he looks at us.
Natural look; cycle 49: props_cheveu.js (chvHair, chvBowl, chvTable, chvRoom, chvTweezers, chvMugWall, chvLamp, chvFile, chvRam, chvDoorWall,
chvHall, chvClippers, chvHairPile, chvShine, chvMicroscope, chvBagShelf, chvScreen, chvStand, chvPool, chvBeam; round 1: chvHeli, chvTorch, chvToque,
chvChefFront, chvBag, chvPanel, chvDog), chair, table, wallClock (props.js), tableStamp, tacLight (props_table), balaclava (props_rambarde), shopFront (props_news),
flashBursts (props_moustache), bigKey (props_moustache) reused; tethers for the leashes and the winch cable.
Lessons applied from the start: `lens` is the vertical field; characters are about 2.3 m tall with the box head; faces and key props above the
caption band (0.77-0.86) and heads below the card band (0.07-0.18) when a card stamps; every camera checked with project() before stills; the
hair (black) always against a pale ground (cream soup, pale chart, pale chair back, light press backdrop, white stand panel); thin cords as
tethers with minPx; nobody hurt (shaving only, the ram hits doors, the dog fine and pleased); no English on screen, no brands, no real insignia
or organisation, no flags; flashes at most three a second.
Round 1 corrections: beams (searchlight, lamp, torch) drawn in the opaque pass behind every actor (props_cheveu onTopActors), never over a
face; a readable outlined navy helicopter whole in a bigger window; the hair outlined white wherever it meets a dark ground; a real chef
(double-breasted jacket, tall toque); doors that fall in a wave with dust; rig takes (double take, bug-eyed take, bow overshoot, clipper
stretch and recoil); alive() puts blinks and breaths in every hold."""
from story_kit import *
import math

st = Story('cheveu', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 20)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def lerp(a, b, u): return [r(a[i] + (b[i] - a[i]) * u) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]   # his right hand side (at -X when he faces +Z)
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
CHECKS = []
def chk(sid, frm, look, lens, pts):
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {project(frm, look, lens, p)}" for n, p in pts.items()))

def FC(sid, t, frm, pts, top=0.08, bottom=0.74, lenses=range(30, 61), drift=(0.0, 0.0, -0.12), margin=0.06):
    """a camera at frm aimed and sized by fit() on the named points (between top and bottom of the height), drifting a little (drift)"""
    look, lens, _ = fit(frm, pts, margin=margin, top=top, bottom=bottom, lenses=lenses)
    if lens is None: print(f'  FC {sid}: WARNING no lens fits'); lens = max(lenses)
    to = [r(frm[i] + drift[i]) for i in range(3)]; chk(sid, frm, look, lens, pts)
    return cam(t, frm, to, look, look, lens)

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
    """(round 1) life in every hold (review 1: frozen holds, blinks in two shots only): blinks every ~gap s and breaths (a keyed squash with
    keepPose, the face carried) in the quiet windows, never inside a keyed move or another key's tween; returns the keys to add"""
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
    """adds alive() keys to an act() dict (a static actor) and returns it"""
    a['keys'] = a['keys'] + alive(a['keys'], D, **kw); return a
def aim_rot(src, dst):
    """rot for a prop whose -Y must point from src to dst (the beam): (rx, ry deg, rz)"""
    Y = unit3([src[i] - dst[i] for i in range(3)]); X = unit3(cross3(Y, [0, 0, 1])) if abs(Y[2]) < 0.95 else unit3(cross3(Y, [1, 0, 0])); Z = cross3(X, Y)
    return axes_euler(X, Y, Z)
def BALD(pid, who, s=1.0, tw=(), tw0=0.35): return P(pid, 'chvShine', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.03]}, opts={'s': s, 'twinkle': list(tw), 'tw0': tw0})

# ============================== the bistro at night: a dark void outside, the room (back wall z -1.5, the window above his head), the table
NIGHT = {'color': '#1A2442'}
WIN = [0.6, 2.18, 1.75, 1.35]                          # (round 1) a bigger, lower window: the helicopter whole in it, the beam through it
TBL = [0.0, 0, 0.0]; TH = 0.76
BOWL = [0.0, TH, -0.2]; SOUP_Y = r(TH + 0.2 * 0.55 * 0.82 + 0.005)
HAIR1 = [0.0, SOUP_Y, -0.19]
HERO = [0.0, 0.03, -0.8]                               # seated (clip sit) behind the table, facing +Z
HEAD_S = [0.0, 1.72, -0.78]                            # his eyes, seated
ROOM = lambda lit=None: [P('salle', 'chvRoom', pos=[0, 0, 0], opts={'win': WIN, 'boardX': -1.55, 'picX': 2.6, 'sconces': [-0.55, 2.0]}),
                P('table', 'chvTable', pos=TBL, opts={'r': 0.5, 'h': TH, 'drop': 0.15}), P('chaise', 'chair', pos=[0.0, 0, -0.95], opts={'color': '#7A4A2A'}),
                P('bol', 'chvBowl', pos=BOWL, opts={'steam': True, **({'lit': lit, 'glareS': 1.1} if lit else {})})]
HAIRF = {'L': 0.3, 'r': 0.0095, 'wig': 0.07}           # the floating hair
SIT = lambda face, reach=None, hands=None: {'face': face, **({'reach': reach} if reach else {}), **({'hands': hands} if hands else {})}

# 1: the hook. Low over the bowl, three-quarter from his right: the thick black hair floating and waving on the pale soup in the foreground, he
#    behind it, seated; (round 1) his finger draws a clear arc: up beside his head (an "aha"), then down onto the hair with an overshoot and
#    two little jabs; his eyes are on the hair; then the pupils come up to us first and the head follows, one brow up, deadpan
D1 = st.dur('S01')
PT1 = R5([-0.17, 0.97, -0.33], 1, 0.2); PT1hi = R5([-0.44, 1.86, -0.6], 1, 0.12); PT1over = R5([-0.13, 0.92, -0.29], 1, 0.2)
C1 = FC('S01', 0.0, [-0.45, 1.12, 1.12], {'headTop': [0, 1.98, -0.8], 'hairL': add(HAIR1, [-0.16, 0, 0.05]), 'hairR': add(HAIR1, [0.16, 0, 0.05]), 'bowlFront': [0, TH + 0.05, 0.0], 'handHi': PT1hi[:3], 'elbowR': [-0.5, 1.3, -0.7]}, top=0.06, bottom=0.76, lenses=range(18, 67), drift=(0.02, 0, -0.08))
F1a = {'lid': 0.2, 'mouth': 'o', 'gy': 1.0, 'brow': 0.5}
F1b = {'lid': 0.05, 'mouth': 'O', 'gy': 1.0, 'gx': 0.3, 'brow': 0.9, 'eye': 0.2}
F1c = {'lid': 0.45, 'mouth': 'line', 'browL': 0.55, 'browR': -0.15, 'gy': 0.0}
KEYS1 = [k(0.0, look=add(HAIR1, [0, 0.05, 0])),
         k(0.0, toon=SIT({'lid': 0.3, 'mouth': 'line', 'gy': 0.6}), toonDur=0.0),
         k(0.18, toon=SIT(F1a, {'R': PT1hi}, {'R': 'point'}), toonDur=0.2, toonEase='out'),
         k(0.46, toon=SIT(F1b, {'R': PT1over}, {'R': 'point'}), toonDur=0.1, toonEase='in'),
         k(0.58, toon=SIT(F1b, {'R': PT1}, {'R': 'point'}), toonDur=0.12, toonEase='out'),
         *[k(r(0.78 + 0.14 * i), toon=SIT(F1b, {'R': R5(add(PT1[:3], [0.02 * ((i + 1) % 2), -0.03 * ((i + 1) % 2), 0.02 * ((i + 1) % 2)]), 1, 0.12)}, {'R': 'point'}), toonDur=0.07) for i in range(3)],
         k(1.2, toon=SIT({**F1b, 'gy': -0.35, 'brow': 0.4, 'mouth': 'line'}, {'R': PT1}, {'R': 'point'}), toonDur=0.08),
         k(1.36, look='camera', lookDur=0.14), k(1.36, toon=SIT(F1c, {'R': PT1}, {'R': 'point'}), toonDur=0.14)]
st.shot('S01', 'whiteVoid', setOpts=NIGHT, actors=[LIFE(act('mec', HERO, 0, 'sit', 'neutral', keys=KEYS1), D1, t0=1.7, gap=0.9)],
        props=[*ROOM(), P('cheveu1', 'chvHair', pos=HAIR1, ry=12, opts=HAIRF)],
        cams=[C1])
st.cue('sfx:clink', 'S01', 0.1, 0.2); st.cue('sfx:tense', 'S01', 0.45, 0.15)

# ============================== the helicopter outside the window (round 1: a navy chvHeli with a pale halo, whole in the window, nose to the
# left; its searchlight runs from the lamp under its nose through the window opening onto the bowl, drawn behind the man)
def ray_at(c, p, z): u = (z - c[2]) / (p[2] - c[2]); return [r(c[i] + (p[i] - c[i]) * u) for i in range(3)]
def rot_y(v, ry): a = math.radians(ry); return [v[0] * math.cos(a) + v[2] * math.sin(a), v[1], -v[0] * math.sin(a) + v[2] * math.cos(a)]
HS, HRY = 0.5, 90
HOT = add(BOWL, [0, 0.11, 0])
def HELI_AT(cam_from, win_pt, zh, dy=0.0):
    """the helicopter centred on the camera's ray through win_pt (a point of the window opening) at depth zh: (pos, lamp world point)"""
    h = add(ray_at(cam_from, win_pt, zh), [0, dy, 0]); return h, add(h, [r(v * HS) for v in rot_y([0, -0.5, 0.62], HRY)])
def BEAM_THROUGH(lamp, sid):
    """where the beam crosses the window plane (it must be inside the opening)"""
    d = [HOT[i] - lamp[i] for i in range(3)]; u = (-1.5 - lamp[2]) / d[2]; x, y = lamp[0] + d[0] * u, lamp[1] + d[1] * u
    CHECKS.append(f"{sid} beam crosses the window at x {x:.2f} y {y:.2f} (opening x {WIN[0] - WIN[2] / 2:.2f}..{WIN[0] + WIN[2] / 2:.2f}, y {WIN[1] - WIN[3] / 2:.2f}..{WIN[1] + WIN[3] / 2:.2f})")
def HELIP(pid, heli, lamp, on=None, r1=0.3):
    BR = aim_rot(lamp, HOT); BL = r(math.dist(lamp, HOT) + 0.05)
    return [P(pid, 'chvHeli', pos=heli, ry=HRY, scale=HS, opts={'rim': '#A9C2E6', 'rimW': 0.05, 'spin': 1.15}),
            P(pid + 'b', 'chvBeam', pos=lamp, ry=BR[1], rot=[BR[0], 0, BR[2]], opts={'len': BL, 'r': r1, 'r0': 0.08, 'op': 0.12, 'fade': 0.75, 'lampR': 0.06, 'flare': 0.7, 'on': on or [[0, 1]]})]

# 2: a police helicopter lit the soup. Low from the table, looking up: his face, and above his head through the window the navy helicopter
#    hovering whole in the window, its searchlight dropping through the window onto the bowl, which flares white-hot; (round 1) the light
#    passes behind him; he gets a squash-and-stretch double take up at it, then shades his eyes with his hand and squints, still moving
D2 = st.dur('S02'); LOCK2 = 0.25
C2F = [-0.05, 0.8, 1.75]
HELI2, LAMP2 = HELI_AT(C2F, [0.38, 2.28, -1.5], -3.4); BEAM_THROUGH(LAMP2, 'S02')
C2 = FC('S02', 0.0, C2F, {'bowl': add(BOWL, [-0.1, 0.1, 0.1]), 'headTop': [0, 2.02, -0.8], 'heliTop': add(HELI2, [0, 0.75, 0]), 'heliNose': add(HELI2, [0.8, 0, 0]), 'heliTail': add(HELI2, [-1.25, 0.3, 0]), 'eyesL': [-0.2, 1.72, -0.8]}, top=0.05, bottom=0.75, lenses=range(18, 70), margin=0.03, drift=(0, 0, -0.1))
UP2 = [0.4, 2.25, 1.2]
F2 = {'lid': 0.4, 'mouth': 'line'}
SQ2 = {'lid': 0.5, 'low': 0.45, 'mouth': 'grimace', 'brow': -0.6, 'gy': -0.9}
def SHADE(i): return {'face': {**SQ2, 'low': 0.45 if i % 2 == 0 else 0.3, 'mouth': 'grimace' if i % 2 == 0 else 'clench', 'browL': -0.7 if i % 2 else -0.4},
                      'touch': {'L': ['face', 0.08 if i % 2 == 0 else -0.02, 0.84 if i % 2 == 0 else 0.88, 0.1, 1, 0.06]}, 'hands': {'L': 'open'}}
KEYS2 = [k(0.0, look='camera'), k(0.0, toon=SIT(F2), toonDur=0.0),
         k(LOCK2, toon={**SIT({**F2, 'lid': 0.15, 'brow': 0.3}), 'sq': [1.04, 0.95, 1.04]}, toonDur=0.04),
         k(0.36, look=UP2, lookDur=0.1), k(0.36, toon=SIT({'lid': 0.2, 'mouth': 'line', 'gy': -0.6, 'brow': 0.3}), toonDur=0.08),
         k(0.52, look='camera', lookDur=0.1), k(0.52, toon=SIT({'lid': 0.3, 'mouth': 'line', 'brow': 0.1}), toonDur=0.08),
         k(0.69, toon={**SIT({'lid': 0.6, 'mouth': 'line', 'brow': -0.3}), 'sq': [1.14, 0.82, 1.14]}, toonDur=0.05),
         k(0.76, look=UP2, lookDur=0.06), k(0.76, toon={**SIT({'pop': 0.5, 'popLen': 0.22, 'brow': 1, 'jaw': 0.35, 'mouth': 'O', 'gy': -0.8}), 'sq': [0.86, 1.2, 0.86], 'hairUp': 0.0}, toonDur=0.05, toonEase='outBack'),
         k(0.9, toon={**SIT({'pop': 0.5, 'popLen': 0.22, 'brow': 1, 'jaw': 0.3, 'mouth': 'O', 'gy': -0.8}), 'sq': [0.9, 1.15, 0.9]}, toonDur=0.06),
         k(1.04, toon={**SIT({'brow': 0.4, 'mouth': 'o', 'gy': -0.8}), 'sq': [1.05, 0.95, 1.05]}, toonDur=0.08, toonEase='in'),
         *[k(r(1.16 + 0.22 * i), toon=SHADE(i), toonDur=0.12 if i else 0.14, toonEase='inOut') for i in range(6)],
         *[k(r(1.2 + 0.3 * i), look=[UP2[0] + (0.5 if i % 2 else -0.3), UP2[1], UP2[2]], lookDur=0.25) for i in range(4)]]
st.shot('S02', 'whiteVoid', setOpts=NIGHT, look={'sun': 0.35, 'fill': 0.6, 'exposure': 1.05}, actors=[act('mec', HERO, 0, 'sit', 'neutral', keys=KEYS2)],
        props=[*ROOM([[0, 0.15], [LOCK2, 1]]), P('cheveu2', 'chvHair', pos=HAIR1, ry=12, opts={**HAIRF, 'waveF': 3.2}), *HELIP('heli2', HELI2, LAMP2, [[0, 0.35], [LOCK2, 1]]),
               P('pool2', 'chvPool', pos=add(BOWL, [0, 0.01, 0]), opts={'r': 0.42, 'h': 0.35, 'power': 0.8, 'range': 0.6, 'on': [[0, 0.2], [LOCK2, 1]]})],
        cams=[C2])
st.cue('engine', 'S02', 0.0, 0.3, D2); st.cue('sfx:rotor', 'S02', 0.0, 0.35); st.cue('clack', 'S02', LOCK2, 0.3)

# 3: the hair was arrested with tweezers. Across the table: a gloved policeman lifts the hair out of the soup with big light steel tweezers and
#    holds it out at arm's length toward us, against the cream wall: (round 1) the hair outlined white, its eyes right under the tips, blinking;
#    his colleague at the right holds open a clear evidence bag with a red label; he, seated behind, follows it with his eyes, worried
D3 = st.dur('S03'); PICK3 = 0.5
COP3 = [-1.0, 0, -0.15]; RYC3 = 50; COP3b = [0.78, 0, -0.5]; RYB3 = -38
TWL = 0.6
TW0 = [r(HAIR1[0]), r(SOUP_Y + TWL * 1.3 - 0.01), HAIR1[2]]            # the tweezers' hinge with the tips at the hair
TW1 = [-0.35, 2.3, -0.05]; TW2 = [-0.32, 2.22, 0.55]
BAG3 = [0.42, 1.42, 0.02]
C3 = FC('S03', 0.0, [0.1, 1.32, 3.6], {'copTop': [COP3[0], 2.45, COP3[2]], 'copL': [COP3[0] - 0.24, 2.1, COP3[2]], 'cop2Top': [COP3b[0], 2.45, COP3b[2]], 'cop2R': [COP3b[0] + 0.24, 2.1, COP3b[2]],
        'tw2top': add(TW2, [0, 0.06, 0]), 'hairBot': add(TW2, [0, -TWL * 1.3 - 0.45, 0]), 'bowl': add(BOWL, [0, 0.0, 0.35])}, top=0.06, bottom=0.76, lenses=range(24, 66), margin=0.04, drift=(0, 0, -0.12))
GRIP = lambda p: R5(add(p, [0.0, -0.26, 0.0]), 1, 0.06)
FC3 = {'lid': 0.35, 'lowR': 0.4, 'mouth': 'grimace', 'brow': -0.3, 'browTiltL': 12}
KEYS3a = [k(0.0, look=add(TW0, [0, -0.5, 0])),
          k(0.0, toon={'reach': {'R': GRIP(TW0)}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.0),
          k(PICK3, toon={'reach': {'R': GRIP(TW1)}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.0, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'line', 'brow': 0.5}}, toonDur=0.4, toonEase='inOut'),
          k(r(PICK3 + 0.15), look=add(TW1, [0, -0.7, 0]), lookDur=0.2),
          k(1.0, toon={'reach': {'R': GRIP(TW2)}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [-0.12, 0, 0, 1, None]}, 'face': FC3}, toonDur=0.35, toonEase='inOut'), k(1.1, look=add(TW2, [0, -0.75, 0]), lookDur=0.2),
          k(1.75, look='camera', lookDur=0.15)]
KEYS3b = [k(0.0, look=add(TW1, [0, -0.7, 0])),
          k(0.0, toon={'reach': {'R': R5(add(BAG3, [-0.13, 0.2, 0.02])), 'L': R5(add(BAG3, [0.13, 0.2, 0.02]))}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': 0.1}}, toonDur=0.0),
          k(1.2, look=add(TW2, [0, -0.7, 0]), lookDur=0.25),
          k(1.2, toon={'reach': {'R': R5(add(BAG3, [-0.15, 0.24, 0.05])), 'L': R5(add(BAG3, [0.15, 0.24, 0.05]))}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'bend': {'spine': [0.12, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'o', 'brow': 0.5}}, toonDur=0.3)]
FW = {'lid': 0.25, 'mouth': 'wavy', 'browTilt': 15, 'brow': 0.3}
KEYS3c = [k(0.0, look=add(HAIR1, [0, 0.1, 0])), k(0.0, toon=SIT({'lid': 0.4, 'mouth': 'line'}), toonDur=0.0), k(r(PICK3 + 0.15), look=add(TW1, [0, -0.7, 0]), lookDur=0.3),
          k(r(PICK3 + 0.2), toon=SIT({**FW, 'gy': -0.4}), toonDur=0.2), k(1.15, look=add(TW2, [0, -0.7, 0]), lookDur=0.3), k(1.3, toon=SIT({**FW, 'gx': -0.6, 'mouth': 'zigzag'}), toonDur=0.2)]
st.shot('S03', 'whiteVoid', setOpts=NIGHT, actors=[LIFE(act('flic1', COP3, RYC3, 'stand', 'neutral', keys=KEYS3a), D3, breath=False, t0=1.5), LIFE(act('flic2', COP3b, RYB3, 'stand', 'neutral', keys=KEYS3b), D3, t0=0.6),
        LIFE(act('mec', HERO, 0, 'sit', 'neutral', keys=KEYS3c), D3, t0=1.7)],
        props=[*ROOM(), P('cheveu3', 'chvHair', pos=HAIR1, ry=12, opts=HAIRF, keys=[k(PICK3 - 0.02, visible=False)]),
               P('pince3', 'chvTweezers', pos=TW0, ry=10, scale=1.3, opts={'len': TWL, 'bw': 0.07, 'hairAt': PICK3 - 0.02, 'hairL': 0.34, 'r': 0.011, 'rim': '#FFFFFF', 'rimW': 2.0, 'eyes': True, 'eyeS': 1.6, 'blinks': [1.25, 1.9],
                                                             'gaze': [[0, 0, 0], [1.4, -0.6, -0.3], [1.8, 0, 0]], 'open': [[0, 0.22], [r(PICK3 - 0.1), 0.02]], 'swing': 0.5},
                 keys=[k(PICK3, to=TW1, dur=0.4, ease='inOut'), k(1.0, to=TW2, dur=0.35, ease='inOut')]),
               P('sachet3', 'chvBag', pos=BAG3, ry=-14, opts={'w': 0.3, 'h': 0.4})],
        cams=[C3])
st.cue('sfx:squeak', 'S03', PICK3, 0.3); st.cue('sfx:slideUp', 'S03', r(PICK3 + 0.05), 0.2)

# 4: photographed from the front, then in profile. Locked frontal camera: the hair stands on the pale chart's ledge holding its tiny number
#    board; flash; a quarter turn; flash; it looks exactly the same (FICHÉ)
D4 = st.dur('S04'); FL4a, TURN4, FL4b = 0.42, 1.12, 1.55
HAIR4 = [0.0, 0.03, 0.0]
C4 = cam(0.0, [0.0, 0.2, 1.0], [0.0, 0.2, 0.97], [0.0, 0.165, 0.0], [0.0, 0.165, 0.0], lens=36)
chk('S04', C4['from'], C4['lookAt'], 36, {'hairTop': [0, 0.36, 0], 'eyes': [0, 0.33, 0.01], 'board': [0, 0.13, 0.02], 'hairFoot': HAIR4, 'wallTop': [0, 0.62, -0.01], 'wallL': [-0.4, 0.3, 0]})
st.shot('S04', 'whiteVoid', setOpts={'color': '#B9C2CC'}, actors=[],
        props=[P('toise4', 'chvMugWall', pos=[0, 0, -0.03]),
               P('cheveu4', 'chvHair', pos=HAIR4, opts={'L': 0.3, 'r': 0.0105, 'wig': 0.04, 'waveF': 1.4, 'stand': [[0, 1]], 'stand0': 1, 'eyes': True, 'brows': True, 'board': ['N° 0088', '17.11'], 'boardU': 0.62,
                                                     'yaw': [[TURN4, 90]], 'boardYaw': [[TURN4, -70]], 'blinks': [r(FL4a + 0.12), r(FL4b + 0.12)], 'gaze': [[0, 0, 0], [0.9, 0.6, 0], [1.05, 0, 0]], 'brow': [[0, 0.0], [r(FL4a + 0.1), -0.5]]})],
        cams=[C4], fx=[{'type': 'flash', 'at': FL4a, 'dur': 0.12}, {'type': 'flash', 'at': FL4b, 'dur': 0.12}])
st.card('S04', 'FICHÉ', at=r(FL4a + 0.25))
st.cue('sfx:shutter', 'S04', FL4a, 0.5); st.cue('sfx:squeak', 'S04', TURN4, 0.15); st.cue('sfx:shutter', 'S04', FL4b, 0.5)

# ============================== the interrogation room (grey walls): the hair on a pale metal chair beside the table, the lamp clamped at the
# table's corner bent down over it, the inspector leaning on the table, the clock on the back wall
CH5 = [1.4, 0, 0.2]; SEAT = 0.48
HAIR5 = [CH5[0], SEAT + 0.005, CH5[2] + 0.02]
LAMP5 = [0.66, 0.785, -0.42]
INSP = [-0.6, 0, -1.45]; RYI = 30
CLOCK = [0.55, 2.3, -3.1]   # (round 1) in the frame, spinning
MIRROR = [-0.55, 0.4, -3.14]   # (round 1) a dark one-way mirror behind the chair: the outlined hair reads against it
HAIR5O = {'L': 0.5, 'r': 0.019, 'eyeS': 1.7, 'wig': 0.04, 'waveF': 1.6, 'stand': [[0, 1]], 'stand0': 1, 'eyes': True, 'brows': True, 'rim': '#FFFFFF', 'rimW': 1.9}   # (round 1) bigger, outlined
INTERRO = lambda heat=None: [P('chaise5', 'chair', pos=CH5, ry=-25, opts={'color': '#30353C'}), P('lampe5', 'chvLamp', pos=LAMP5, ry=yaw(LAMP5, CH5), opts={'h': 0.55, 'reach': 0.86, 'tilt': 0.35, 'beamLen': 0.75, 'power': 3.5, 'heat': heat or []}),
                             P('horloge5', 'wallClock', pos=CLOCK, scale=1.25, opts={'rate': 2.2}), P('miroir5', 'chvPanel', pos=MIRROR, opts={'w': 2.4, 'h': 1.5})]

# 5: questioned twelve hours under the lamp. Low, strong push-in: (round 1) the hair, bigger and outlined white, alone on the dark chair in
#    front of the dark one-way mirror under the bent lamp; the inspector leaning on the table at the left (his head clear of the top band),
#    the wall clock spinning behind; the lamp's light passes behind him
D5 = st.dur('S05')
C5F = [2.35, 0.62, 1.75]
C5 = FC('S05', 0.0, C5F, {'hairTop': add(HAIR5, [0, 0.55, 0]), 'hairFoot': add(HAIR5, [0, -0.05, 0]), 'inspTop': [INSP[0], 2.4, INSP[2]], 'inspHead': add(off(INSP, RYI, 0.55, 0.3, 1.95), [0, 0, 0]), 'inspL': [INSP[0] - 0.3, 2.0, INSP[2]], 'clock': add(CLOCK, [0, 0.4, 0])},
        top=0.2, bottom=0.74, lenses=range(24, 70), margin=0.1, drift=(-0.3, 0.04, -0.55))
CHECKS.append(f"S05 behind the hair: {ray_at(C5F, add(HAIR5, [0, 0.3, 0]), -3.14)} (mirror x {MIRROR[0] - 1.2:.2f}..{MIRROR[0] + 1.2:.2f}, y {MIRROR[1]:.2f}..{MIRROR[1] + 1.5:.2f})")
PALMS = lambda dz=0.0: {'R': R5([INSP[0] + 0.25, 0.8, -0.95 + dz]), 'L': R5([INSP[0] - 0.2, 0.8, -1.0 + dz])}
FI = {'lid': 0.55, 'mouth': 'line', 'brow': -0.6}
KEYS5 = [k(0.0, look=add(HAIR5, [0, 0.3, 0])),
         k(0.0, toon={'reach': PALMS(), 'hands': {'R': 'open', 'L': 'open'}, 'bend': {'spine': [0.45, 0, 0, 1, None]}, 'face': FI}, toonDur=0.0),
         k(0.55, toon={'reach': PALMS(0.08), 'hands': {'R': 'open', 'L': 'open'}, 'bend': {'spine': [0.62, 0, 0, 1, None], 'neck': [0.15, 0, 0, 1, None]}, 'face': {'lid': 0.7, 'lowL': 0.35, 'mouth': 'clench', 'brow': -0.9}}, toonDur=0.35, toonEase='inOut'),
         k(1.15, toon={'reach': PALMS(0.08), 'hands': {'R': 'fist', 'L': 'open'}, 'bend': {'spine': [0.58, 0, 0, 1, None]}, 'face': {'lid': 0.45, 'mouth': 'teeth', 'brow': -1.0, 'vein': 1}}, toonDur=0.2)]
st.shot('S05', 'interrogation', actors=[LIFE(act('inspecteur', INSP, RYI, 'stand', 'suspicious', keys=KEYS5), D5, t0=0.3)],
        props=[*INTERRO([[0, 0.15]]), P('cheveu5', 'chvHair', pos=HAIR5, ry=-25, opts={**HAIR5O, 'blinks': [0.45, 1.05, 1.6], 'gaze': [[0, -0.6, 0], [0.7, 0.0, -0.7], [1.2, -0.7, 0.2]], 'brow': [[0, -0.6], [1.2, -1]], 'sweat': [1.0]})],
        cams=[C5])
st.cue('sfx:ticks', 'S05', 0.0, 0.25); st.cue('sfx:static', 'S05', 0.2, 0.08)

# 6: it curled; that was held against it. Close on the hair under the lamp gone hot orange: it coils into a tight curl with a boing, sweating
#    (FRISÉ); cut on the table: the inspector slams the stamp on its open file, RETENU
D6 = st.dur('S06'); CURL6 = 0.18; CUT6 = 1.05; STAMP6 = 1.48
FILE6 = [-0.15, 0.79, -0.7]
STAMPUP = add(FILE6, [0.04, 0.62, 0.02]); STAMPDN = add(FILE6, [0.04, 0.4, 0.02])
C6b = cam(CUT6, [-0.15, 1.75, 0.15], [-0.15, 1.72, 0.1], [-0.15, 0.8, -0.72], [-0.15, 0.8, -0.72], lens=50)
C6a = FC('S06a', 0.0, [1.15, 0.85, 1.35], {'hairTop': add(HAIR5, [0, 0.56, 0]), 'hairFoot': add(HAIR5, [0, -0.04, 0]), 'side': add(HAIR5, [0.2, 0.2, 0]), 'side2': add(HAIR5, [-0.2, 0.2, 0])}, top=0.19, bottom=0.74, lenses=range(24, 62), drift=(0.02, 0, -0.08))
chk('S06b', C6b['from'], C6b['lookAt'], 50, {'file': FILE6, 'stampUp': STAMPUP, 'inspFace': [INSP[0], 2.05, INSP[2]], 'fileL': add(FILE6, [-0.3, 0, 0])})
KNOB = lambda p: R5(add(p, [0.0, 0.0, 0.0]), 1, 0.06)
st.shot('S06', 'interrogation', actors=[
        act('inspecteur', INSP, RYI, 'stand', 'suspicious', keys=[k(0.0, look=add(HAIR5, [0, 0.3, 0])),
            k(0.0, toon={'reach': {'R': KNOB(STAMPUP), 'L': R5([INSP[0] - 0.2, 0.8, -1.0])}, 'hands': {'R': 'grip', 'L': 'open'}, 'bend': {'spine': [0.4, 0, 0, 1, None]}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.6}}, toonDur=0.0),
            k(r(CUT6 - 0.1), look=FILE6, lookDur=0.15),
            k(r(STAMP6 - 0.2), toon={'reach': {'R': KNOB(add(STAMPUP, [0, 0.1, 0])), 'L': R5([INSP[0] - 0.2, 0.8, -1.0])}, 'hands': {'R': 'grip', 'L': 'open'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.4, 'mouth': 'clench', 'brow': -0.8}}, toonDur=0.14),
            k(STAMP6, toon={'reach': {'R': KNOB(STAMPDN), 'L': R5([INSP[0] - 0.2, 0.8, -1.0])}, 'hands': {'R': 'grip', 'L': 'open'}, 'bend': {'spine': [0.55, 0, 0, 1, None]}, 'sq': [1.04, 0.95, 1.04], 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.8}}, toonDur=0.05, toonEase='in'),
            k(r(STAMP6 + 0.3), look='camera', lookDur=0.15)])],
        props=[*INTERRO([[0, 0.3], [0.05, 1.0]]), P('dossier6', 'chvFile', pos=FILE6, ry=0, opts={'stampAt': r(STAMP6 + 0.02), 'stamp': 'RETENU'}),
               P('tampon6', 'tableStamp', pos=STAMPUP, opts={'squash': [[STAMP6, 1], [r(STAMP6 + 0.1), 0]]}, keys=[k(r(STAMP6 - 0.2), to=add(STAMPUP, [0, 0.1, 0]), dur=0.14), k(STAMP6, to=STAMPDN, dur=0.05, ease='in'), k(r(STAMP6 + 0.25), to=STAMPUP, dur=0.2)]),
               P('cheveu6', 'chvHair', pos=HAIR5, ry=-25, opts={**HAIR5O, 'curl': [[CURL6, 1]], 'curlDur': 0.3, 'hop': [[CURL6, 1], [r(CURL6 + 0.18), 0]], 'sweat': [0.45, 0.85], 'blinks': [0.75], 'gaze': [[0, 0, -0.8], [0.6, -0.7, 0]], 'brow': [[0, -0.9]]})],
        cams=[C6a, C6b])
st.card('S06', 'FRISÉ', at=0.52)
st.cue('sfx:boing', 'S06', CURL6, 0.45); st.cue('sfx:spring', 'S06', r(CURL6 + 0.05), 0.25); st.cue('thud', 'S06', STAMP6, 0.6)

# ============================== the street (parisStreet): the road along Z (x -5..5), the right pavement x 5..10; the cook's house front at x 8.6
STREET = {'clouds': 0, 'clear': [-30.0, 12.0], 'clearL': [-30.0, 12.0]}
DOGF = {'color': '#3A3530', 'muzzle': '#1E1A18', 'walk': True, 'tongue': True}
# 7: the dogs followed its trail to the cook. Low ahead of them, dollying back: two sniffer dogs pull their leaning handlers up the pavement
#    toward us; cut: they stop at the feet of the cook on his doorstep (white jacket, toque, his key in hand), sniffing up at him
D7 = st.dur('S07'); CUT7 = 1.25
DA0, DA1 = [6.6, 0, -4.6], [6.6, 0, -1.0]; DB0, DB1 = [7.4, 0, -4.1], [7.4, 0, -0.5]
H7a0, H7a1 = [6.45, 0, -5.9], [6.45, 0, -2.3]; H7b0, H7b1 = [7.55, 0, -5.4], [7.55, 0, -1.8]
C7a = cam(0.0, [7.0, 0.8, 1.6], [7.0, 0.85, 2.6], [7.0, 1.05, -3.5], [7.0, 1.05, -2.0], lens=48)
COOK = [7.95, 0, -12.0]; RYK = -90                     # on his doorstep, facing the street (-X)
DOGc1, DOGc2 = [7.25, 0, -11.55], [7.3, 0, -12.5]
chk('S07a', C7a['from'], C7a['lookAt'], 48, {'dogA1': add(DA1, [0, 0.6, 0]), 'dogB0': add(DB0, [0, 0.6, 0]), 'handA1': [H7a1[0], 2.0, H7a1[2]], 'handB0': [H7b0[0], 2.0, H7b0[2]]})
C7b = FC('S07b', CUT7, [4.2, 1.25, -10.5], {'cookTop': [COOK[0], 2.98, COOK[2]], 'dog1': add(DOGc1, [-0.3, 0.75, 0.2]), 'dog2': add(DOGc2, [-0.3, 0.75, -0.2]), 'dogFeet': add(DOGc2, [0, 0.05, 0])}, top=0.06, bottom=0.78, lenses=range(30, 66), drift=(0.08, 0, -0.05))
LEAN = lambda p, i=0: {'reach': {'R': R5(off(p, 0, 0.95, 0.12, 0.95 + 0.04 * (i % 2))), 'L': R5(off(p, 0, 0.88, -0.1, 0.92 + 0.04 * ((i + 1) % 2)))}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.5 + 0.05 * (i % 2), 0, 0, 1.05, None], 'neck': [-0.35, 0, 0, 1, None]}, 'hose': 0.15}   # (round 1) dragged: pitched forward, arms out to the leash
def LEASH(hid, dog, frm=None, until=None):
    d = {'a': {'actor': hid, 'hand': 'R'}, 'b': {'prop': dog, 'offset': [0, 0.53, 0.3]}, 'color': '#C0392B', 'sag': 0.04, 'radius': 0.014, 'minPx': 4}
    if frm is not None: d['from'] = frm
    if until is not None: d['until'] = until
    return d
KEYOPT = {'len': 0.2}
CHEF = lambda pid, who: P(pid, 'chvChefFront', on={'actor': who, 'joint': 'torso', 'offset': [0, 0, 0]}, opts={'w': 0.38, 'z': 0.172})   # (round 1) a double-breasted chef's jacket
TOQUE_ON = lambda pid, who, keys=None: P(pid, 'chvToque', on={'actor': who, 'joint': 'head', 'offset': [0, 0.47, 0]}, keys=keys or [])
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[
        act('maitre1', H7a0, 0, 'walk', 'scared', keys=[k(0.0, to=H7a1, dur=CUT7, clip='walk', ease='linear', cruise=True), k(0.0, look='camera'), k(0.0, toon={**LEAN(H7a0), 'face': {'lid': 0.0, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.0),
            *[k(r(0.2 * i), toon={**LEAN(lerp(H7a0, H7a1, 0.2 * i / CUT7), i), 'face': {'lid': 0.0, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.2, toonEase='linear') for i in range(1, 7)], k(CUT7, visible=False)]),
        act('maitre2', H7b0, 0, 'walk', 'surprised', keys=[k(0.0, to=H7b1, dur=CUT7, clip='walk', ease='linear', cruise=True), k(0.0, look='camera'), k(0.0, toon={**LEAN(H7b0), 'face': {'lid': 0.0, 'mouth': 'wavy', 'brow': 0.8}}, toonDur=0.0),
            *[k(r(0.2 * i), toon={**LEAN(lerp(H7b0, H7b1, 0.2 * i / CUT7), i + 1), 'face': {'lid': 0.0, 'mouth': 'wavy', 'brow': 0.8}}, toonDur=0.2, toonEase='linear') for i in range(1, 7)], k(CUT7, visible=False)]),
        LIFE(act('cuisinier', COOK, RYK, 'stand', 'neutral', keys=[k(0.0, look=add(DOGc1, [0, 0.5, 0])), k(0.0, toon={'reach': {'R': R5(off(COOK, RYK, 0.38, 0.15, 1.25))}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.0),
            k(r(CUT7 + 0.55), look='camera', lookDur=0.2), *blink(r(CUT7 + 0.85), {'lid': 0.35, 'mouth': 'line', 'brow': 0.2}), k(r(CUT7 + 0.3), toon={'reach': {'R': R5(off(COOK, RYK, 0.38, 0.15, 1.25))}, 'hands': {'R': 'pinch'}, 'face': {'lid': 0.1, 'mouth': 'o', 'brow': 0.6}}, toonDur=0.15)]), D7, t0=1.6, gap=0.7),
        LIFE(act('maitre3', [6.3, 0, -10.9], -120, 'stand', 'neutral', keys=[k(0.0, look=add(DOGc1, [0, 0.5, 0])), k(0.0, toon={'reach': {'R': R5([6.75, 1.0, -11.2])}, 'hands': {'R': 'grip'}, 'bend': {'spine': [-0.2, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'O', 'brow': 0.5}}, toonDur=0.0)]), D7, t0=1.5)],
        props=[P('chien7a', 'chvDog', pos=DA0, opts={**DOGF, 'sniff': [[0.1, 0.4], [0.62, 0.92]], 'wag': 3}, keys=[k(0.0, to=DA1, dur=CUT7, ease='linear'), k(CUT7, visible=False)]),
               P('chien7b', 'chvDog', pos=DB0, opts={**DOGF, 'sniff': [[0.3, 0.6], [0.85, 1.2]], 'wag': 3.4}, keys=[k(0.0, to=DB1, dur=CUT7, ease='linear'), k(CUT7, visible=False)]),
               P('chien7c', 'chvDog', pos=DOGc1, ry=60, opts={**DOGF, 'walk': False, 'proud': [[0, 0.6]], 'sniff': [[1.6, 1.85], [2.15, 2.4]], 'wag': 3}, keys=[k(0.0, visible=False), k(CUT7, visible=True), k(r(CUT7 + 0.2), rotTo=[0.25, 1.05, 0], dur=0.1), k(r(CUT7 + 0.45), rotTo=[-0.05, 1.05, 0], dur=0.1), k(r(CUT7 + 0.7), rotTo=[0.25, 1.05, 0], dur=0.1)]),
               P('chien7d', 'chvDog', pos=DOGc2, ry=80, opts={**DOGF, 'walk': False, 'proud': [[0, 0.8]], 'sniff': [[1.4, 1.7], [1.95, 2.25]], 'wag': 2.6}, keys=[k(0.0, visible=False), k(CUT7, visible=True), k(r(CUT7 + 0.3), rotTo=[0.3, 1.4, 0], dur=0.1), k(r(CUT7 + 0.6), rotTo=[0.0, 1.4, 0], dur=0.1)]),
               P('maison7', 'chvDoorWall', pos=[8.6, 0, -12.0], ry=-90, opts={'facade': True, 'w': 3.4, 'num': 12, 'color': '#E7D2B0', 'door': '#2F5D8A'}),
               P('cle7', 'bigKey', on={'actor': 'cuisinier', 'hand': 'R', 'face': 'camera'}, opts=KEYOPT), CHEF('veste7', 'cuisinier'), TOQUE_ON('toque7', 'cuisinier')],
        cams=[C7a, C7b],
        tethers=[LEASH('maitre1', 'chien7a', until=CUT7), LEASH('maitre2', 'chien7b', until=CUT7), {**LEASH('maitre3', 'chien7c', frm=CUT7), 'a': {'point': [6.75, 1.0, -11.2]}}])
st.cue('sfx:stepRun', 'S07', 0.1, 0.25); st.cue('sfx:sniff', 'S07', 0.4, 0.3); st.cue('sfx:sniff', 'S07', 0.8, 0.3); st.cue('sfx:sniff', 'S07', r(CUT7 + 0.2), 0.35); st.cue('sfx:sniff', 'S07', r(CUT7 + 0.5), 0.3)

# 8: they broke down his door. Inside his hallway, at floor level: the front door falls flat toward us in a puff of dust; in the bright doorway
#    two masked officers hold the ram, a third behind
D8 = st.dur('S08'); HIT8 = 0.32
RAM8a, RAM8b = [0.0, 1.05, -1.05], [0.0, 1.05, -0.62]
SW1, SW2 = [-0.32, 0, -0.95], [0.32, 0, -1.35]
C8 = cam(0.0, [0.28, 0.28, 3.7], [0.26, 0.28, 3.55], [0.0, 1.15, -0.6], [0.0, 1.15, -0.6], lens=46)
chk('S08', C8['from'], C8['lookAt'], 46, {'doorTop': [0, 2.15, 0.05], 'doorFlat': [0, 0.06, 2.1], 'sw1Face': [SW1[0], 2.05, SW1[2]], 'sw2Face': [SW2[0], 2.05, SW2[2]], 'ram': RAM8b, 'ceil': [0, 2.9, 2.0]})
def RAMHANDS(ram, side):
    g = [[0, 0.21, -0.28], [0, 0.21, 0.22]]
    return {'R': R5(add(ram, [side * 0.06, g[0][1], g[0][2]])), 'L': R5(add(ram, [side * 0.06, g[1][1], g[1][2]]))}
MASKED = lambda who: [P(f'cagoule_{who}', 'balaclava', on={'actor': who, 'joint': 'head', 'offset': [0, 0, 0]}), P(f'casque_{who}', 'tacHelmet', on={'actor': who, 'joint': 'head', 'offset': [0, 0.47, 0]})]
st.shot('S08', 'whiteVoid', setOpts={'color': '#E4ECF2'}, actors=[
        act('swat1', SW1, 0, 'stand', 'angry', keys=[k(0.0, look=[0, 1.2, 1.5]), k(0.0, toon={'reach': RAMHANDS(RAM8a, 1), 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.2, 0, 0, 1, None]}}, toonDur=0.0),
            k(r(HIT8 - 0.12), toon={'reach': RAMHANDS(RAM8b, 1), 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.35, 0, 0, 1, None]}}, toonDur=0.12, toonEase='in'), k(r(HIT8 + 0.6), look='camera', lookDur=0.2)]),
        act('swat2', SW2, 0, 'stand', 'angry', keys=[k(0.0, look=[0, 1.2, 1.5]), k(0.0, toon={'reach': RAMHANDS(RAM8a, -1), 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.2, 0, 0, 1, None]}}, toonDur=0.0),
            k(r(HIT8 - 0.12), toon={'reach': RAMHANDS(RAM8b, -1), 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.35, 0, 0, 1, None]}}, toonDur=0.12, toonEase='in'), *blink(1.1, {'lid': 0.3, 'mouth': 'line'})]),
        LIFE(act('swat3', [0.75, 0, -2.4], -20, 'stand', 'neutral', keys=[k(0.0, look=[0, 1.2, 1.5]), k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.0), k(r(HIT8 + 0.05), toon={'sq': [1.06, 0.94, 1.06], 'face': {'lid': 0.0, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.04), k(r(HIT8 + 0.25), toon={'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.15)]), D8, t0=0.9)],
        props=[P('couloir8', 'chvHall', pos=[0, 0, 0]), P('porte8', 'chvDoorWall', pos=[0, 0, 0], opts={'w': 1.9, 'h': 2.95, 'dir': 1, 'fallAt': HIT8, 'num': 12, 'color': '#D6C3A0', 'trim': '#F2EEE4', 'bounce': 0.38, 'bounceF': 13, 'bounceDecay': 4.5, 'slamSq': True}),
               P('belier8', 'chvRam', pos=RAM8a, keys=[k(r(HIT8 - 0.12), to=RAM8b, dur=0.12, ease='in')]), *MASKED('swat1'), *MASKED('swat2'), *MASKED('swat3')],
        cams=[C8], fx=[{'type': 'shake', 'at': HIT8, 'dur': 0.2, 'amount': 0.02}])
st.cue('thud', 'S08', HIT8, 0.7); st.cue('sfx:crunch', 'S08', HIT8, 0.35); st.cue('thud', 'S08', r(HIT8 + 0.24), 0.6); st.cue('sfx:poof', 'S08', r(HIT8 + 0.26), 0.3)

# 9: and every door in the street. From the road, down the row of house fronts: the ram team sprints toward us along the pavement and each front
#    door falls inward as they pass, one after the other, a black doorway opening each time
D9 = st.dur('S09')
HZ = [-3.3, -5.5, -7.7, -9.9, -12.1, -14.3, -16.5]
RUN0, RUN1 = -14.0, -5.6; SPD9 = (RUN1 - RUN0) / D9
FALL9 = lambda z: r((z - 2.0 - RUN0) / SPD9)   # (round 1) each door drops 2 m ahead of the team: a wave of doors falling toward us
C9 = FC('S09', 0.0, [5.3, 0.62, -2.3], {'door0top': [8.5, 2.45, HZ[2]], 'door4': [8.5, 2.3, HZ[4]], 'run1top': [6.5, 2.5, RUN1 + 0.2], 'run1feet': [6.5, 0.0, RUN1 + 0.2], 'run1L': [5.9, 1.5, RUN1], 'farFeet': [7.6, 0.0, HZ[4]]},
        top=0.08, bottom=0.8, lenses=range(24, 66), margin=0.03, drift=(0.05, 0.0, 0.25))
RUNNERS = [('swat1', 6.15, 0.0), ('swat2', 6.85, -0.9), ('swat3', 6.5, -2.0)]
def RAMAT(t): return [6.5, 1.05, r(RUN0 + SPD9 * t + 0.45)]
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[
        *[act(w, [x, 0, r(RUN0 + dz)], 0, 'run', 'angry', keys=[k(0.0, to=[x, 0, r(RUN1 + dz)], dur=D9, clip='run', ease='linear', cruise=True), k(0.0, look=[x, 1.8, 10]),
            *([k(r(0.15 * i), toon={'reach': {'R' if w == 'swat1' else 'L': R5(add(RAMAT(0.15 * i), [(-0.18 if w == 'swat1' else 0.18), 0.12, -0.05 if w == 'swat1' else 0.35]))}, 'hands': {'R': 'grip', 'L': 'grip'}, 'autoSq': 0.3}, toonDur=0.15, toonEase='linear') for i in range(int(D9 / 0.15) + 1)] if w != 'swat3' else [])]) for w, x, dz in RUNNERS]],
        props=[*[P(f'maison9{i}', 'chvDoorWall', pos=[8.6, 0, z], ry=-90, opts={'facade': True, 'w': 2.2, 'dir': -1, 'dark': True, 'fallAt': FALL9(z), 'fallDur': 0.2, 'bounce': 0.3, 'bounceF': 15, 'bounceDecay': 5, 'puffOut': True, 'puffS': 1.6, 'puffUp': 0.9, 'num': 2 + 2 * i, 'color': ['#E7D2B0', '#D9B8A0', '#CFD8C6', '#E4C9A8', '#C9D2DE', '#E8D9B8', '#DCC7A4'][i], 'door': ['#2F5D8A', '#8A2E2E', '#2E6B4A', '#5A3E8A', '#B06A2A', '#2F5D8A', '#8A2E2E'][i]}) for i, z in enumerate(HZ)],
               P('belier9', 'chvRam', pos=RAMAT(0), keys=[k(0.0, to=RAMAT(D9), dur=D9, ease='linear')]), *MASKED('swat1'), *MASKED('swat2'), *MASKED('swat3')],
        cams=[C9])
for z in HZ:
    if 0 <= FALL9(z) < D9: st.cue('thud', 'S09', r(FALL9(z) + 0.22), 0.4)
st.cue('sfx:stepRun', 'S09', 0.0, 0.3)

# ============================== the cook's doorstep (the fallen door behind him)
COOK10 = [7.85, 0, -12.0]
DOORSTEP = lambda: [P('maison10', 'chvDoorWall', pos=[8.6, 0, -12.0], ry=-90, opts={'facade': True, 'w': 3.4, 'dir': -1, 'dark': True, 'fallAt': -2.0, 'num': 12, 'color': '#E7D2B0', 'door': '#2F5D8A'})]
TOQUE_H = lambda p, ry: off(p, ry, 0.42, 0.28, 1.35)
# 10: the cook was bald. Medium, three-quarter front: on his doorstep, in his double-breasted white jacket, (round 1) he lifts his tall
#     pleated toque straight up off his head: perfectly bald, a flare of shine on the scalp; an officer at the left holds a short fat cream
#     torch whose beam lands on the scalp (CHAUVE)
D10 = st.dur('S10'); LIFT10 = 0.3
OFF10 = [6.75, 0, -11.25]; RYO10 = yaw(OFF10, COOK10)
TORCH10 = off(OFF10, RYO10, 0.45, -0.2, 1.55)
HEADTOP = [COOK10[0] - 0.04, 2.33, COOK10[2]]
C10 = FC('S10', 0.0, [4.7, 1.75, -13.6], {'cookTop': [COOK10[0], 2.95, COOK10[2]], 'cookHips': [COOK10[0], 0.9, COOK10[2]], 'cookL': [COOK10[0], 1.6, COOK10[2] - 0.45], 'torch': TORCH10, 'offFace': [OFF10[0], 2.1, OFF10[2]]}, top=0.2, bottom=0.8, lenses=range(28, 66), drift=(0.06, 0, 0.04))
TR10 = aim_rot(TORCH10, HEADTOP)
TOQ = lambda pid, who, keys=None: P(pid, 'chvToque', on={'actor': who, 'hand': 'L', 'offset': [0.0, 0.02, 0.0]}, keys=keys or [])
FK = {'lid': 0.4, 'mouth': 'line', 'brow': 0.1}
HL = lambda p, f=FK, extra=None: {'reach': {'L': R5(p, 1, 0.06)}, 'hands': {'L': 'grip'}, 'face': f, **(extra or {})}
KEYS10 = [k(0.0, look='camera'),
          k(0.0, toon=HL(off(COOK10, RYK, 0.06, 0.0, 2.36)), toonDur=0.0),
          k(r(LIFT10 - 0.08), toon=HL(off(COOK10, RYK, 0.06, 0.0, 2.33), FK, {'sq': [1.04, 0.96, 1.04]}), toonDur=0.08),
          k(LIFT10, toon=HL(off(COOK10, RYK, 0.14, -0.3, 2.68), {'lid': 0.2, 'mouth': 'line', 'brow': 0.5}, {'sq': [0.97, 1.04, 0.97]}), toonDur=0.14, toonEase='out'),
          k(r(LIFT10 + 0.45), toon=HL(off(COOK10, RYK, 0.4, -0.3, 1.4), {'lid': 0.45, 'mouth': 'smirk', 'brow': -0.1}), toonDur=0.3)]
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[
        LIFE(act('cuisinier', COOK10, RYK, 'stand', 'neutral', keys=KEYS10), D10, t0=1.12),
        LIFE(act('flic1', OFF10, RYO10, 'stand', 'neutral', keys=[k(0.0, look=HEADTOP), k(0.0, toon={'reach': {'R': R5(TORCH10, 1, 0.0)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.0),
            k(r(LIFT10 + 0.15), toon={'reach': {'R': R5(TORCH10, 1, 0.0)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.1, 'mouth': 'O', 'brow': 0.7}}, toonDur=0.1)]), D10, t0=0.9)],
        props=[*DOORSTEP(), CHEF('veste10', 'cuisinier'), TOQUE_ON('toque10', 'cuisinier', keys=[k(LIFT10, attach='cuisinier', hand='L', offset=[0.0, 0.02, 0.0])]),
               BALD('brille10', 'cuisinier', 1.0, [r(LIFT10 + 0.18), 1.0], 0.5) | {'opts': {'s': 1.0, 'twinkle': [r(LIFT10 + 0.18), 1.0], 'tw0': 0.5, 'flare': [[r(LIFT10 + 0.15), 3.0]]}},
               P('lampe10', 'chvTorch', pos=TORCH10, ry=r(TR10[1]), rot=[r(TR10[0]), 0, r(TR10[2])], opts={'len': r(math.dist(TORCH10, HEADTOP) - 0.2), 'r': 0.15, 'op': 0.45})],
        cams=[C10])
st.card('S10', 'CHAUVE', at=0.82)
st.cue('sfx:ding', 'S10', r(LIFT10 + 0.22), 0.35)

# 11: he was shaved anyway. Tight on his head from a little above and in front, the scalp in the middle of the frame: the officer's hand runs
#     the buzzing clippers across the bare scalp; (round 1) the clippers stretch into the pass, the scalp squashes under them, they recoil off
#     it with a hop; nothing falls; a glint; he blinks, eyes rolled up
D11 = st.dur('S11'); PASS11 = (0.25, 0.85)
OFF11 = [7.2, 0, -12.75]; RYO11 = yaw(OFF11, COOK10)
CLIP0 = [COOK10[0] - 0.05, 2.35, COOK10[2] + 0.14]; CLIP1 = [COOK10[0] - 0.05, 2.35, COOK10[2] - 0.14]; CLIPUP = add(CLIP1, [0.02, 0.14, -0.04])
C11 = FC('S11', 0.0, [6.65, 2.3, -11.9], {'chin': [COOK10[0] - 0.1, 1.76, COOK10[2]], 'scalp': [COOK10[0], 2.4, COOK10[2]], 'earL': [COOK10[0], 2.0, COOK10[2] + 0.24], 'earR': [COOK10[0], 2.0, COOK10[2] - 0.24]},
         top=0.14, bottom=0.74, lenses=range(18, 62), margin=0.12, drift=(0.05, -0.02, 0))
CLIPROT = [0.0, 0, PI / 2 + 0.2]
FS = {'lid': 0.4, 'mouth': 'line', 'gy': -0.9}
TQ = R5(off(COOK10, RYK, 0.4, -0.3, 1.4), 1, 0.06)
K11 = lambda f, sc=None: {'reach': {'L': TQ}, 'hands': {'L': 'grip'}, 'face': f, **({'scl': {'head': sc}} if sc else {})}
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[
        LIFE(act('cuisinier', COOK10, RYK, 'stand', 'neutral', keys=[k(0.0, look='camera'),
            k(0.0, toon=K11({**FS, 'gy': -0.6}), toonDur=0.0),
            k(PASS11[0], toon=K11({**FS, 'gx': 0.5, 'low': 0.2}, [1.05, 0.93, 1.05]), toonDur=0.06),
            k(0.55, toon=K11({**FS, 'gx': 0.0, 'low': 0.25}, [1.05, 0.93, 1.05]), toonDur=0.2),
            k(PASS11[1], toon=K11({**FS, 'gx': -0.5, 'lid': 0.5}, [0.96, 1.06, 0.96]), toonDur=0.05),
            k(1.0, toon=K11({'lid': 0.45, 'mouth': 'wavy', 'gy': -0.3}), toonDur=0.12), *blink(1.2, {'lid': 0.45, 'mouth': 'wavy', 'gy': -0.3})]), D11, blinks=False, t0=0.3),
        act('flic1', OFF11, RYO11, 'stand', 'neutral', keys=[k(0.0, look=HEADTOP), k(0.0, toon={'reach': {'R': R5(add(CLIP0, [0, -0.02, 0.0]), 1, 0.06)}, 'hands': {'R': 'grip'}}, toonDur=0.0),
            k(PASS11[0], toon={'reach': {'R': R5(add(CLIP1, [0, -0.02, 0.0]), 1, 0.06)}, 'hands': {'R': 'grip'}}, toonDur=PASS11[1] - PASS11[0], toonEase='inOut'),
            k(PASS11[1], toon={'reach': {'R': R5(add(CLIPUP, [0, -0.02, 0.0]), 1, 0.06)}, 'hands': {'R': 'grip'}}, toonDur=0.08, toonEase='out'),
            k(1.05, toon={'reach': {'R': R5(add(CLIP1, [0.15, 0.1, -0.1]), 1, 0.06)}, 'hands': {'R': 'grip'}}, toonDur=0.25)])],
        props=[*DOORSTEP(), CHEF('veste11', 'cuisinier'), TOQ('toque11', 'cuisinier'), BALD('brille11', 'cuisinier', 1.0, [r(PASS11[1] + 0.05)], 0.4),
               P('tondeuse11', 'chvClippers', pos=CLIP0, rot=CLIPROT, opts={'buzz': [[0.0, 1.05]], 's': 1.3, 'sq': [[0.0, [1, 1, 1]], [PASS11[0], [0.82, 1.3, 0.9]], [0.75, [0.9, 1.15, 0.95]], [PASS11[1], [1.3, 0.72, 1.2]], [0.93, [0.85, 1.25, 0.9]], [1.02, [1, 1, 1]]]},
                 keys=[k(PASS11[0], to=CLIP1, dur=PASS11[1] - PASS11[0], ease='inOut'), k(PASS11[1], to=CLIPUP, dur=0.08, ease='out'), k(1.05, to=add(CLIP1, [0.15, 0.1, -0.1]), dur=0.25)])],
        cams=[C11])
st.cue('engine', 'S11', 0.0, 0.18, 1.05); st.cue('sfx:ding', 'S11', r(PASS11[1] + 0.05), 0.3)

# ============================== the pavement outside the restaurant: the customers and passers-by on chairs facing the street (-X), officers behind
REST = lambda: [P('resto', 'shopFront', pos=[9.6, 0, -3.0], ry=-90, opts={'text': 'RESTAURANT', 'w': 6.0, 'h': 2.8, 'color': '#E9D9B8', 'signBg': '#7A3328'})]
SEATS = [('client1', -1.0, '#5A3A22'), ('client2', -2.3, '#D8B25A'), ('client3', -3.6, '#9A9A96'), ('client4', -4.9, '#1E1C1E')]
CX = 7.6
# 12: then the customers and the passers-by, for comparison. High and wide: a row of them sitting bald on chairs, officers buzzing clippers over
#     their heads, piles of hair in their old colours growing at their feet, each with a numbered tag; cut lower on the second customer
D12 = st.dur('S12'); CUT12 = 1.2
C12a = FC('S12a', 0.0, [3.0, 5.4, 1.4], {'c1head': [CX, 2.0, -1.0], 'c4head': [CX, 2.0, -4.9], 'pile1': [CX - 0.75, 0.1, -0.9], 'pile4': [CX - 0.75, 0.1, -4.9], 'barb1': [CX + 0.65, 2.2, -1.0], 'barb4': [CX + 0.65, 2.2, -4.9]}, top=0.06, bottom=0.76, lenses=range(26, 72), margin=0.04, drift=(0.1, -0.08, -0.1))
C12b = FC('S12b', CUT12, [4.9, 1.6, -1.0], {'barb2top': [CX + 0.62, 2.3, -2.3], 'c2face': [CX, 1.6, -2.3], 'pile2tag': [CX - 0.62, 0.5, -2.15], 'pile2': [CX - 0.75, 0.05, -2.3]}, top=0.06, bottom=0.76, lenses=range(30, 66), drift=(0.08, 0, -0.04))
def BARBER(i, who, z, t1):
    """the officer behind seat i: his hand and the clippers sweep over the head (front to back), in step"""
    p0, p1 = [CX + 0.03, 1.98, z - 0.12], [CX + 0.03, 1.98, z + 0.12]
    ts = [r(0.12 + 0.3 * j + 0.07 * i) for j in range(int(t1 / 0.3))]
    hand = [k(0.0, toon={'reach': {'R': R5(add(p0, [0.0, -0.03, 0]), 1, 0.06)}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}}, toonDur=0.0)]
    hand += [k(t, toon={'reach': {'R': R5(add(p1 if j % 2 == 0 else p0, [0.0, -0.03, 0]), 1, 0.06)}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.18 + 0.14 * (j % 2), 0.06 * (1 if j % 2 else -1), 0, 1, None]}, 'face': {'lid': 0.3 + 0.2 * (j % 2), 'mouth': 'line' if j % 2 else 'smirk', 'brow': -0.2}}, toonDur=0.28, toonEase='inOut') for j, t in enumerate(ts)]   # (round 1) the barber rocks with each pass
    cl = [k(t, to=(p1 if j % 2 == 0 else p0), dur=0.28, ease='inOut') for j, t in enumerate(ts)]
    return act(who, [CX + 0.62, 0, z], -90, 'stand', 'neutral', keys=[k(0.0, look=[CX, 1.95, z]), *hand]), P(f'tond_{who}', 'chvClippers', pos=p0, rot=[0, 0, PI / 2], opts={'buzz': [[0, 3]], 's': 1.2, 'bits': [[0.0, t1, SEATS[i][2]]]}, keys=cl)
BARBERS = ['flic3', 'flic4', 'flic5', 'flic6']
def CUSTOMERS(D, grow0=0.15):
    acts, props = [], []
    for i, (who, z, col) in enumerate(SEATS):
        ts = [r(0.12 + 0.3 * j + 0.07 * i) for j in range(int(D / 0.3))]
        F0 = {'lid': 0.45 + 0.05 * i, 'mouth': 'line'}; FX = {'lid': 0.75, 'low': 0.3, 'mouth': ['clench', 'wavy', 'grimace', 'zigzag'][i], 'brow': 0.4}
        flinch = [kk for j, t in enumerate(ts) for kk in (k(t, toon={'sq': [1.04, 0.95, 1.04], 'face': FX}, toonDur=0.05), k(r(t + 0.13), toon={'sq': [0.99, 1.02, 0.99], 'face': {**F0, 'gx': 0.4 * (1 if j % 2 else -1)}}, toonDur=0.1))]   # (round 1) each pass: a flinch
        acts.append(act(who, [CX, 0.03, z], -90, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': F0}, toonDur=0.0), *flinch]))
        props += [P(f'chaise12{i}', 'chair', pos=[CX + 0.15, 0, z], ry=-90, opts={'color': '#7A4A2A'}), BALD(f'brille_{who}', who, 1.0, [r(0.3 + 0.4 * i)], 0.4),
                  P(f'tas12{i}', 'chvHairPile', pos=[CX - 0.72, 0.0, r(z + 0.05)], ry=-60, opts={'color': col, 'num': i + 1, 'tagS': 1.6, 'r': 0.22, 'tuftS': 0.1, 'tufts': [r(t + 0.18) for t in ts], 'grow': [[0, grow0 + 0.1 * i], [0.3, grow0 + 0.15 + 0.1 * i], [D, 1.0]]})]
        a, p = BARBER(i, BARBERS[i], z, D); acts.append(a); props.append(p)
    return acts, props
A12, P12 = CUSTOMERS(D12)
st.shot('S12', 'parisStreet', setOpts=STREET, actors=A12, props=[*REST(), *P12], cams=[C12a, C12b])
st.cue('engine', 'S12', 0.0, 0.2, D12); st.cue('sfx:poof', 'S12', 0.6, 0.15)

# 13: the police dog too. Low at its height on the pavement: the dog shaved pink and smooth, standing at attention beside its handler, tongue out,
#     pleased, a glint on its back; its own small tagged pile of dark fur beside it
D13 = st.dur('S13')
DOG13 = [6.6, 0, -6.4]; HAND13 = [7.15, 0, -6.95]
C13 = FC('S13', 0.0, [3.8, 0.9, -4.3], {'dogHead': [DOG13[0] - 0.3, 0.85, DOG13[2] + 0.1], 'dogFeet': [DOG13[0], 0.0, DOG13[2]], 'handTop': [HAND13[0], 2.65, HAND13[2]], 'pile': [DOG13[0] - 0.35, 0.45, DOG13[2] - 0.75]}, top=0.12, bottom=0.8, lenses=range(30, 66), drift=(0.06, 0, -0.05))
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[
        LIFE(act('maitre1', HAND13, -110, 'stand', 'neutral', keys=[k(0.0, look=[DOG13[0], 0.7, DOG13[2]]), k(0.0, toon={'reach': {'R': R5(off(HAND13, -110, 0.2, 0.25, 2.05), 1, 0.03)}, 'hands': {'R': 'open'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.0),
            k(0.3, toon={'reach': {'R': R5(off(HAND13, -110, 0.2, 0.25, 2.05), 1, 0.03)}, 'hands': {'R': 'open'}, 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.2, 'mouth': 'smirk', 'brow': 0.5}}, toonDur=0.15),
            k(0.6, look='camera', lookDur=0.2)]), D13, t0=0.85)],
        props=[P('chien13', 'chvDog', pos=DOG13, ry=-70, opts={'color': '#F2A9B9', 'muzzle': '#E07F96', 'ear': '#E58AA0', 'tongue': 'long', 'eyes': 1.15, 'proud': [[0, 0.2], [0.3, 1.0]], 'wag': 4}, keys=[k(0.3, squash=[1.08, 0.9, 1.08], dur=0.25), k(0.75, rotTo=[0, -1.12, 0], dur=0.12), k(1.05, rotTo=[0, -1.0, 0], dur=0.1)]),   # (round 1) longer muzzle, pointed ears, chest out, tail wagging
               P('brille13', 'chvShine', pos=[DOG13[0] + 0.05, 0.6, DOG13[2] + 0.1], face='camera', opts={'s': 1.4, 'twinkle': [0.3, 1.0], 'tw0': 0.3, 'opacity': 0.0}),
               P('tas13', 'chvHairPile', pos=[DOG13[0] - 0.35, 0.0, DOG13[2] - 0.75], ry=-60, opts={'color': '#3A3530', 'num': 5, 'tagS': 1.4, 'r': 0.2})],
        cams=[C13])
st.cue('sfx:ding', 'S13', 0.3, 0.3); st.cue('sfx:sniff', 'S13', 0.8, 0.2)

# 14: this man, twice. Frontal close-up: he, bald, sits in the chair; the officer's hand runs the clippers over his head, pauses, and passes
#     again; his eyes roll up to them between the passes, then back to us
D14 = st.dur('S14'); P14 = [(0.12, 0.5), (0.85, 1.22)]
HERO14 = [CX, 0.03, -6.8]
B14 = [CX + 0.05, 0, -7.6]
CL14a = [CX + 0.03, 1.98, -6.68]; CL14b = [CX + 0.03, 1.98, -6.92]
C14 = cam(0.0, [6.2, 1.82, -6.8], [6.27, 1.82, -6.8], [7.6, 1.64, -6.8], [7.6, 1.64, -6.8], lens=40)
chk('S14', C14['from'], C14['lookAt'], 40, {'eyes': [CX - 0.09, 1.7, -6.8], 'chin': [CX - 0.09, 1.38, -6.8], 'top': [CX, 1.98, -6.8], 'clipA': CL14a, 'clipB': CL14b, 'barbFace': [B14[0], 2.0, B14[2]]})
FACE14 = {'lid': 0.45, 'mouth': 'line'}
CL14up = add(CL14b, [0.02, 0.14, -0.05])
# (round 1) his face changes between the passes: eyes rolled up to the clippers, the scalp squashing under each pass, cheeks puffed and a
# twitching eye on the second, a heavy deadpan blink at the end; the clippers stretch into each pass and recoil off the scalp with a hop
K14 = lambda f, sc=None: {'face': f, **({'scl': {'head': sc}} if sc else {})}
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[
        act('mecChauve', HERO14, -90, 'sit', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon=K14({**FACE14, 'gy': -0.7}), toonDur=0.0),
            k(P14[0][0], toon=K14({'lid': 0.35, 'mouth': 'line', 'gy': -1.0, 'gx': 0.4, 'low': 0.2}, [1.05, 0.93, 1.05]), toonDur=0.06),
            k(0.32, toon=K14({'lid': 0.35, 'mouth': 'line', 'gy': -1.0, 'gx': -0.4, 'low': 0.2}, [1.05, 0.93, 1.05]), toonDur=0.18),
            k(P14[0][1], toon=K14({'lid': 0.3, 'mouth': 'line', 'brow': 0.4, 'gy': -0.9}, [0.96, 1.06, 0.96]), toonDur=0.05),
            k(0.66, toon=K14({'lid': 0.2, 'mouth': 'line', 'brow': 0.5, 'gy': -1.0}), toonDur=0.1),
            k(P14[1][0], toon=K14({'lid': 0.4, 'lidL': 0.75, 'mouth': 'line', 'puff': 1, 'cheeks': 1, 'gy': -1.0, 'brow': -0.3}, [1.06, 0.92, 1.06]), toonDur=0.06),
            k(1.05, toon=K14({'lid': 0.4, 'lidL': 0.55, 'mouth': 'line', 'puff': 1, 'cheeks': 1, 'gy': -1.0, 'brow': -0.3}, [1.06, 0.92, 1.06]), toonDur=0.1),
            k(P14[1][1], toon=K14({**FACE14, 'mouth': 'wavy'}, [0.97, 1.05, 0.97]), toonDur=0.06), k(1.32, toon=K14({**FACE14, 'mouth': 'wavy'}), toonDur=0.1),
            *blink(1.42, {**FACE14, 'mouth': 'wavy'})]),
        act('flic3', B14, -10, 'stand', 'neutral', keys=[k(0.0, look=[CX, 1.95, -6.8]), k(0.0, toon={'reach': {'R': R5(add(CL14a, [0, -0.03, 0]), 1, 0.06)}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}}, toonDur=0.0),
            k(P14[0][0], toon={'reach': {'R': R5(add(CL14b, [0, -0.03, 0]), 1, 0.06)}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}}, toonDur=0.38, toonEase='inOut'),
            k(P14[0][1], toon={'reach': {'R': R5(add(CL14up, [0, -0.03, 0]), 1, 0.06)}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.2, 0, 0, 1, None]}}, toonDur=0.08, toonEase='out'),
            k(0.66, toon={'reach': {'R': R5(add(CL14a, [0.05, 0.12, 0]), 1, 0.06)}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}}, toonDur=0.18),
            k(P14[1][0], toon={'reach': {'R': R5(add(CL14b, [0, -0.03, 0]), 1, 0.06)}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}}, toonDur=0.37, toonEase='inOut'),
            k(P14[1][1], toon={'reach': {'R': R5(add(CL14up, [0, -0.03, 0]), 1, 0.06)}, 'hands': {'R': 'grip'}, 'bend': {'spine': [0.2, 0, 0, 1, None]}}, toonDur=0.08, toonEase='out')])],
        props=[P('chaise14', 'chair', pos=[CX + 0.15, 0, -6.8], ry=-90, opts={'color': '#7A4A2A'}), BALD('brille14', 'mecChauve', 1.0, [0.55, r(P14[1][1] + 0.05)], 0.35),
               P('tondeuse14', 'chvClippers', pos=CL14a, rot=[0, 0, PI / 2], opts={'buzz': [[0.0, 0.52], [0.82, 1.3]], 'sq': [[0.0, [1, 1, 1]], [P14[0][0], [0.82, 1.3, 0.9]], [0.42, [0.9, 1.15, 0.95]], [P14[0][1], [1.3, 0.72, 1.2]], [0.58, [0.88, 1.2, 0.92]], [0.7, [1, 1, 1]],
                                                                                                      [P14[1][0], [0.82, 1.3, 0.9]], [1.15, [0.9, 1.15, 0.95]], [P14[1][1], [1.3, 0.72, 1.2]], [1.3, [0.88, 1.2, 0.92]], [1.4, [1, 1, 1]]]},
                 keys=[k(P14[0][0], to=CL14b, dur=0.38, ease='inOut'), k(P14[0][1], to=CL14up, dur=0.08, ease='out'), k(0.66, to=add(CL14a, [0.05, 0.12, 0]), dur=0.18), k(P14[1][0], to=CL14b, dur=0.37, ease='inOut'), k(P14[1][1], to=CL14up, dur=0.08, ease='out')])],
        cams=[C14])
st.cue('engine', 'S14', P14[0][0], 0.18, 0.4); st.cue('engine', 'S14', P14[1][0], 0.18, 0.4); st.cue('sfx:ding', 'S14', r(P14[1][1] + 0.05), 0.25)

# ============================== the lab (a pale void): the bench, the microscope, the comparison screen, the shelves of hair bags behind
LAB = {'color': '#DCE6EA'}
BENCH = [0.0, 0, 0.0]; BH = 0.9
MIC = [-0.3, BH, 0.05]; SCR = [0.5, BH, -0.1]
SAV = [-0.3, 0, -0.62]
# 15: under the microscope: no match. The scientist peers into the microscope, one eye shut, the shelves of numbered hair bags behind; cut: push
#     in on the screen: the two samples, a scan line sweeping, then a big red cross
D15 = st.dur('S15'); CUT15 = 1.15; CROSS15 = 1.62
C15a = FC('S15a', 0.0, [0.75, 1.75, 2.9], {'savTop': [SAV[0], 2.35, SAV[2]], 'savL': [SAV[0] - 0.42, 1.6, SAV[2]], 'savR': [SAV[0] + 0.4, 1.9, SAV[2]], 'micBase': add(MIC, [0, 0.0, 0.1]), 'scrR': add(SCR, [0.42, 0.5, 0])},
          top=0.06, bottom=0.76, lenses=range(24, 66), margin=0.05, drift=(0, 0, -0.12))
C15b = FC('S15b', CUT15, [0.65, 1.42, 1.9], {'scrL': add(SCR, [-0.42, 0.47, 0]), 'scrR': add(SCR, [0.42, 0.47, 0]), 'scrTop': add(SCR, [0, 0.82, 0]), 'scrBot': add(SCR, [0, 0.3, 0])}, top=0.15, bottom=0.72, drift=(-0.02, -0.01, -0.35))
# (round 1) he keeps working: the focus knob turned in little twists, a lean in, a jerk back from the eyepiece on each beep, a look at the screen
def SAVPOSE(t, knob, lean, face, neck=-0.25):
    return k(t, toon={'reach': {'R': R5(add(MIC, [0.13, 0.2 + knob, -0.04])), 'L': R5(add(MIC, [-0.12, 0.2, -0.05]))}, 'hands': {'R': 'pinch', 'L': 'pinch'}, 'bend': {'spine': [lean, 0, 0, 1, None], 'neck': [neck, 0, 0, 1, None]}, 'face': face}, toonDur=0.1)
EYE = {'lid': 0.2, 'lidR': 1.0, 'mouth': 'line', 'brow': 0.4}
SAVKEYS = [SAVPOSE(0.0, 0.0, 0.42, EYE) | {'toonDur': 0.0}, SAVPOSE(0.2, -0.03, 0.46, {**EYE, 'mouth': 'pout'}), SAVPOSE(0.4, 0.0, 0.48, EYE), SAVPOSE(0.55, -0.03, 0.5, {**EYE, 'mouth': 'pout'}),
           SAVPOSE(0.65, 0.0, 0.3, {'lid': 0.0, 'mouth': 'O', 'brow': 0.8}, -0.05) | {'toonDur': 0.05}, SAVPOSE(0.82, 0.0, 0.46, EYE), SAVPOSE(1.0, 0.0, 0.25, {'lid': 0.0, 'mouth': 'O', 'brow': 1.0, 'eye': 0.2}, 0.0) | {'toonDur': 0.05},
           k(1.0, look=add(SCR, [0, 0.55, 0]), lookDur=0.1)]
st.shot('S15', 'whiteVoid', setOpts=LAB, actors=[
        LIFE(act('savant', SAV, 0, 'stand', 'neutral', keys=[k(0.0, look=add(MIC, [0, 0.5, -0.1])), *SAVKEYS]), D15, t0=1.3)],
        props=[P('paillasse15', 'table', pos=BENCH, opts={'w': 1.9, 'd': 0.8, 'h': BH, 'color': '#F2F2EE', 'legs': '#9AA2AC'}), P('micro15', 'chvMicroscope', pos=MIC, opts={'s': 1.25}),
               P('ecran15', 'chvScreen', pos=SCR, ry=-12, opts={'w': 0.78, 'scan': 0.6, 'crossAt': CROSS15}), P('etageres15', 'chvBagShelf', pos=[0.0, 0, -1.65])],
        cams=[C15a, C15b])
st.cue('sfx:beep', 'S15', 0.65, 0.2); st.cue('sfx:beep', 'S15', 1.0, 0.2); st.cue('sfx:sting', 'S15', CROSS15, 0.35)

# 16: the minister apologised to the hair. From the press seats: the minister at the podium turns and bows deeply to the hair standing on its
#     little red-cushioned stand beside the podium; flashes pop in the foreground
D16 = st.dur('S16'); BOW16 = 0.45
MIN = [-0.1, 0, -2.35]; RYM = 62
STAND = [0.62, 0, -2.0]; SH16 = 1.12
C16 = FC('S16', 0.0, [1.75, 1.6, 1.55], {'minTop': [MIN[0], 2.55, MIN[2]], 'minL': [MIN[0] - 0.25, 1.5, MIN[2]], 'hairTop': [STAND[0], SH16 + 0.6, STAND[2]], 'standFoot': [STAND[0], 0.7, STAND[2]]}, top=0.06, bottom=0.74, drift=(-0.05, 0, -0.12))
BOWED = {'reach': {'R': R5(off(MIN, RYM, 0.18, 0.12, 1.0)), 'L': R5(off(MIN, RYM, 0.15, -0.14, 1.05))}, 'hands': {'R': 'open', 'L': 'open'}}
st.shot('S16', 'pressRoom', setOpts={'backdrop': 'EXCUSES', 'bg': '#E4E8EE', 'fg': 'rgba(46,69,99,0.35)', 'fontScale': 0.55, 'flags': False, 'chairs': False, 'wall': '#C9D2DE', 'band': '#AAB6C4'}, actors=[
        LIFE(act('ministre', MIN, RYM, 'stand', 'neutral', keys=[k(0.0, look=[STAND[0], 1.5, STAND[2]]),
            k(0.0, toon={**BOWED, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.0),
            k(0.28, toon={**BOWED, 'bend': {'spine': [-0.18, 0, 0, 1.03, None]}, 'face': {'lid': 0.2, 'mouth': 'line', 'brow': 0.6}}, toonDur=0.15, toonEase='out'),
            k(BOW16, toon={**BOWED, 'bend': {'spine': [1.3, 0, 0, 1.18, None], 'neck': [0.45, 0, 0, 1, None]}, 'face': {'lid': 0.9, 'mouth': 'line', 'brow': 0.5}}, toonDur=0.12, toonEase='in'),
            k(r(BOW16 + 0.12), toon={**BOWED, 'bend': {'spine': [0.85, 0, 0, 0.96, None], 'neck': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.85, 'mouth': 'line', 'brow': 0.5}}, toonDur=0.1, toonEase='out'),
            k(r(BOW16 + 0.24), toon={**BOWED, 'bend': {'spine': [0.98, 0, 0, 1.02, None], 'neck': [0.3, 0, 0, 1, None]}, 'face': {'lid': 0.8, 'mouth': 'line', 'brow': 0.5}}, toonDur=0.1),
            k(r(BOW16 + 0.6), toon={**BOWED, 'bend': {'spine': [0.95, 0, 0, 1, None], 'neck': [0.25, 0, 0, 1, None]}, 'face': {'lid': 0.8, 'mouth': 'line', 'brow': 0.5}}, toonDur=0.3),
            k(r(BOW16 + 1.1), toon={**BOWED, 'bend': {'spine': [-0.22, 0, 0, 1.04, None]}, 'face': {'lid': 0.3, 'mouth': 'smile', 'brow': 0.4}}, toonDur=0.16, toonEase='out'),
            k(r(BOW16 + 1.3), toon={**BOWED, 'bend': {'spine': [0.06, 0, 0, 1, None]}, 'face': {'lid': 0.35, 'mouth': 'smile', 'brow': 0.3}}, toonDur=0.12), k(r(BOW16 + 1.25), look='camera', lookDur=0.2)]), D16, breath=False, t0=1.9)],
        props=[P('socle16', 'chvStand', pos=STAND, opts={'h': SH16, 'panel': True}),
               P('cheveu16', 'chvHair', pos=[STAND[0], SH16 + 0.065, STAND[2] + 0.02], ry=-15, opts={'L': 0.42, 'r': 0.013, 'wig': 0.04, 'waveF': 1.5, 'stand': [[0, 1]], 'stand0': 1, 'eyes': True, 'eyeS': 1.3, 'brows': True, 'blinks': [0.3, 1.5], 'gaze': [[0, -0.8, 0], [r(BOW16 + 0.3), -0.8, 0.6], [r(BOW16 + 1.3), 0, 0]], 'brow': [[0, 0.2], [r(BOW16 + 0.4), -0.4]]}),
               P('flash16', 'flashBursts', pos=[1.2, 0.95, 0.2], face='camera', opts={'n': 5, 'w': 1.0, 'h': 0.35, 'at': [0.25, 0.65, 1.05, 1.45, 1.85], 'life': 0.15})],
        cams=[C16])
for t in [0.25, 0.65, 1.05, 1.45, 1.85]: st.cue('sfx:shutter', 'S16', t, 0.3)

# 17: it was the last hair in the neighbourhood. Crane down over a square of shining bald heads (the pink dog among them) packed round the hair
#     alone on its stand in the middle, which looks up at us
D17 = st.dur('S17')
SQ = [0.0, -0.14, -6.0]
CROWD = [('foule0', 'madame'), ('foule1', 'worker'), ('foule2', 'mamie'), ('foule3', 'sportif'), ('foule4', 'boss'), ('foule5', 'serveur'), ('foule6', 'tourist'), ('foule7', 'prefet'),
         ('foule8', 'cop'), ('foule9', 'pyjama'), ('foule10', 'doctor'), ('foule11', 'fermier'), ('foule12', 'cuisinier'), ('foule13', 'client2')]
def ring_pos(i):
    n0 = 6; rr, a0 = (1.25, 0.0) if i < n0 else (2.1, 0.3); n = n0 if i < n0 else len(CROWD) - n0; j = i if i < n0 else i - n0
    a = a0 + j / n * 2 * PI; return [r(SQ[0] + rr * math.sin(a)), SQ[1], r(SQ[2] + rr * math.cos(a))]
C17 = [cam(0.0, [0.6, 10.5, -1.2], [0.5, 4.6, -2.6], [0.0, 0.0, -6.0], [0.0, 0.6, -6.0], lens=48, ease='out')]
chk('S17s', C17[0]['from'], C17[0]['lookAt'], 48, {'stand': add(SQ, [0, 1.2, 0]), 'ringN': add(ring_pos(0), [0, 2.2, 0]), 'ringFar': add(ring_pos(9), [0, 2.2, 0])})
chk('S17e', C17[0]['to'], C17[0]['lookAt2'], 48, {'hairTop': add(SQ, [0, 1.95, 0]), 'stand': add(SQ, [0, 1.2, 0]), 'ringNear': add(ring_pos(0), [0, 2.2, 0]), 'ringBack': add(ring_pos(3), [0, 2.2, 0]), 'outer6': add(ring_pos(6), [0, 2.2, 0])})
st.shot('S17', 'parisStreet', setOpts=STREET, actors=[
        *[LIFE(act(w, ring_pos(i), yaw(ring_pos(i), SQ), 'stand', 'neutral', keys=[k(0.0, look=add(SQ, [0.15 * math.sin(i), 1.5, 0.15 * math.cos(i)])), k(0.0, toon={'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0),
            k(r(0.5 + 0.07 * i), look=add(SQ, [0.25 * math.cos(i * 1.7), 1.75, 0.25 * math.sin(i * 1.7)]), lookDur=0.35),
            k(r(1.1 + 0.05 * i), look='camera' if i % 3 == 0 else add(SQ, [0, 1.3, 0]), lookDur=0.3)]), D17, t0=r(0.3 + 0.09 * i), gap=0.7, amp=1.4) for i, (w, _) in enumerate(CROWD)]],   # (round 1) the crowd breathes, glances, blinks
        props=[P('socle17', 'chvStand', pos=SQ, opts={'h': 1.12, 'panel': False}),
               P('cheveu17', 'chvHair', pos=add(SQ, [0, 1.185, 0]), ry=20, opts={'L': 0.62, 'r': 0.02, 'wig': 0.04, 'waveF': 1.3, 'stand': [[0, 1]], 'stand0': 1, 'eyes': True, 'eyeS': 2.0, 'brows': True, 'rim': '#F4F1E8', 'blinks': [1.5], 'gaze': [[0, 0, 0], [0.9, 0, -1.0]]}),
               *[BALD(f'brille17_{w}', w, 1.1, [r(0.2 + 0.09 * i)], 0.5) for i, (w, _) in enumerate(CROWD)],
               P('chien17', 'chvDog', pos=add(SQ, [1.55, 0.0, 1.2]), ry=-130, opts={'color': '#F2A9B9', 'muzzle': '#E07F96', 'ear': '#E58AA0', 'tongue': 'long', 'proud': [[0, 1]], 'wag': 3.5})],
        cams=C17)
st.cue('sfx:wind', 'S17', 0.0, 0.2); st.cue('sfx:choir', 'S17', 0.2, 0.15)

# 18: the helicopter put it back. Night, low from his left-front (not the frame of shot 2): the helicopter whole in the window; (round 1) the
#    winch descent is the move: the hair, outlined white, comes down on its pale cable against the dark sky, through the window, to just over
#    the bowl; he, bald, follows it all the way down, mouth open, his eyes crossing as it arrives under his nose; the searchlight on the bowl
D18 = st.dur('S18')
C18F = [-0.7, 0.85, 1.9]
HELI18, LAMP18 = HELI_AT(C18F, [0.45, 2.5, -1.5], -3.4); BEAM_THROUGH(LAMP18, 'S18')
WINCH = add(HELI18, [0.05, -0.4, 0.0])
HW0 = add(WINCH, [0.0, -0.2, 0.0]); HW1 = [0.12, 2.12, -1.0]
u18 = (-1.5 - HW0[2]) / (HW1[2] - HW0[2]); CHECKS.append(f"S18 hair crosses the window at y {HW0[1] + (HW1[1] - HW0[1]) * u18:.2f} x {HW0[0] + (HW1[0] - HW0[0]) * u18:.2f}")
C18 = FC('S18', 0.0, C18F, {'bowl': add(BOWL, [0.1, 0.05, 0.15]), 'heliTop': add(HELI18, [0, 0.5, 0]), 'heliNose': add(HELI18, [0.8, 0, 0]), 'heliTail': add(HELI18, [-1.25, 0.2, 0]), 'headTop': [0, 2.0, -0.8], 'chin': [0, 1.45, -0.7], 'hairEnd': add(HW1, [0, -0.36, 0])}, top=0.04, bottom=0.76, lenses=range(18, 70), margin=0.03, drift=(-0.04, 0, -0.12))
def hair18(t): u = min(1.0, t / (D18 - 0.1)); u = u * u * (3 - 2 * u); return lerp(HW0, HW1, u)
FU = {'lid': 0.1, 'mouth': 'o', 'brow': 0.6, 'gy': -0.7}
KEYS18 = [k(0.0, look=[0.4, 2.05, 0.6]), k(0.0, toon=SIT(FU), toonDur=0.0),
          *[k(r(0.25 * i), look=[hair18(0.25 * i + 0.15)[0] * 0.6, min(2.05, hair18(0.25 * i + 0.15)[1]) , 0.6], lookDur=0.25) for i in range(1, 6)],   # (round 1) the head tips a little, the eyes do the rest
          k(0.55, toon=SIT({**FU, 'mouth': 'O', 'brow': 0.9, 'eye': 0.15}), toonDur=0.2),
          k(1.1, toon=SIT({'lid': 0.2, 'mouth': 'O', 'brow': 1.0, 'gy': 0.3, 'cross': 0.55, 'eye': 0.2}), toonDur=0.2)]
st.shot('S18', 'whiteVoid', setOpts=NIGHT, look={'sun': 0.35, 'fill': 0.6, 'exposure': 1.05}, actors=[LIFE(act('mecChauve', HERO, 0, 'sit', 'neutral', keys=KEYS18), D18, t0=0.3, gap=0.75, blinks=False)],
        props=[*ROOM([[0, 1]]), *HELIP('heli18', HELI18, LAMP18), P('pool18', 'chvPool', pos=add(BOWL, [0, 0.01, 0]), opts={'r': 0.42, 'h': 0.35, 'power': 0.8, 'range': 0.6}), BALD('brille18', 'mecChauve', 1.0, [0.2, 1.0], 0.6),
               P('cheveu18', 'chvHair', pos=HW0, rot=[PI, 0, 0], opts={'L': 0.34, 'r': 0.012, 'wig': 0.05, 'stand': [[0, 1]], 'stand0': 1, 'rim': '#FFFFFF', 'rimW': 2.1, 'onTop': True, 'eyes': True, 'eyeS': 1.3, 'blinks': [0.7]},
                 keys=[k(0.0, to=HW1, dur=D18 - 0.1, ease='inOut')])],
        cams=[C18],
        tethers=[{'a': {'point': WINCH}, 'b': {'prop': 'cheveu18', 'offset': [0, 0, 0]}, 'color': '#EEF2F6', 'sag': 0.0, 'radius': 0.011, 'minPx': 4}])
st.cue('engine', 'S18', 0.0, 0.3, D18); st.cue('sfx:rotor', 'S18', 0.0, 0.3); st.cue('sfx:slideDownSlow', 'S18', 0.1, 0.25)

# 19: in this man's soup. The framing of shot 1: he, bald, before the same bowl; the hair drops in from above onto the soup, a ripple, it floats
#     and opens two little eyes at him; he looks at it, then at us
D19 = st.dur('S19'); LAND19 = 0.3
# (round 1) a bug-eyed take at the hair (not the shot-1 pose): a squash as it lands, the eyes out on stalks down at it, both hands flying up open
# beside his face, held; then the hands come down to the table edge and he turns to us, lids heavy, mouth wavy; a slow blink
HUP = {'R': R5([-0.42, 1.62, -0.55], 1, 0.05), 'L': R5([0.42, 1.62, -0.55], 1, 0.05)}; HDN = {'R': R5([-0.3, 0.82, -0.42], 1, 0.05), 'L': R5([0.3, 0.82, -0.42], 1, 0.05)}
TK19 = {'pop': 0.7, 'popLen': 0.28, 'brow': 1, 'jaw': 0.45, 'mouth': 'O', 'eyePitch': 0.5}
KEYS19 = [k(0.0, look=add(HAIR1, [0, 0.35, 0])), k(0.0, toon=SIT({'lid': 0.45, 'mouth': 'line', 'gy': 0.2}), toonDur=0.0),
          k(0.15, look=add(HAIR1, [0, 0.05, 0]), lookDur=0.15),
          k(r(LAND19 + 0.02), toon={**SIT({'lid': 0.7, 'mouth': 'line', 'brow': -0.3, 'gy': 0.8}), 'sq': [1.12, 0.86, 1.12]}, toonDur=0.05),
          k(r(LAND19 + 0.12), toon={**SIT(TK19, HUP, {'R': 'spread', 'L': 'spread'}), 'sq': [0.9, 1.14, 0.9]}, toonDur=0.06, toonEase='outBack'),
          *[k(r(LAND19 + 0.22 + 0.08 * i), toon={**SIT({**TK19, 'eyePitch': 0.5 + 0.06 * (i % 2)}, HUP, {'R': 'spread', 'L': 'spread'}), 'sq': [0.92 + 0.02 * (i % 2), 1.11 - 0.03 * (i % 2), 0.92 + 0.02 * (i % 2)]}, toonDur=0.07) for i in range(6)],
          k(1.05, toon={**SIT({'brow': 0.5, 'mouth': 'o', 'gy': 0.8}, HDN, {'R': 'grip', 'L': 'grip'}), 'sq': [1.04, 0.96, 1.04]}, toonDur=0.2, toonEase='in'),
          k(1.45, look='camera', lookDur=0.15), k(1.45, toon=SIT({'lid': 0.62, 'mouth': 'wavy', 'brow': -0.25, 'browR': 0.3}, HDN, {'R': 'grip', 'L': 'grip'}), toonDur=0.15),
          k(1.95, toon=SIT({'lid': 1.0, 'mouth': 'wavy', 'brow': -0.25}, HDN, {'R': 'grip', 'L': 'grip'}), toonDur=0.15), k(2.25, toon=SIT({'lid': 0.62, 'mouth': 'wavy', 'brow': -0.25, 'browR': 0.3}, HDN, {'R': 'grip', 'L': 'grip'}), toonDur=0.15)]
st.shot('S19', 'whiteVoid', setOpts=NIGHT, actors=[LIFE(act('mecChauve', HERO, 0, 'sit', 'neutral', keys=KEYS19), D19, blinks=False, t0=1.6)],
        props=[*[p for p in ROOM() if p['id'] != 'bol'], P('bol', 'chvBowl', pos=BOWL, opts={'steam': True, 'ripple': [LAND19]}), BALD('brille19', 'mecChauve', 1.0, [1.6], 0.35),
               P('cheveu19', 'chvHair', pos=add(HAIR1, [0, 0.45, 0]), ry=12, opts={**HAIRF, 'eyes': True, 'eyesFloat': True, 'eyesOn': [[0, 0], [0.85, 1]], 'blinks': [1.3], 'gaze': [[0, 0, -0.8], [1.5, 0, 0]], 'eyeS': 0.9},
                 keys=[k(0.0, to=HAIR1, dur=LAND19, ease='in')])],
        cams=[C1])
st.cue('sfx:splash', 'S19', LAND19, 0.3); st.cue('sfx:pop', 'S19', 0.85, 0.2)

print('\n'.join(CHECKS))

MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
BALDC = lambda preset, seed, **kw: {'preset': preset, 'hair': 'bald', 'hat': 'none', 'seed': seed, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX, **kw}
st.write("Le cheveu", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'mecChauve': {**MEC, 'hairColor': '#E2B48E'},
    'flic1': {'preset': 'cop', 'seed': 880, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'flic2': {'preset': 'cop2', 'seed': 881, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.08}, 'toon': EX},
    **{f'flic{i}': {'preset': 'cop' if i % 2 else 'cop2', 'seed': 880 + i, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for i in range(3, 7)},
    'inspecteur': {'preset': 'commissaire', 'seed': 887, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.08}, 'toon': EX},
    'maitre1': {'preset': 'cop', 'seed': 888, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}, 'maitre2': {'preset': 'cop2', 'seed': 889, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'maitre3': {'preset': 'cop', 'seed': 890, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'cuisinier': {'preset': 'chef', 'hat': 'none', 'hair': 'bald', 'glasses': False, 'tie': '#F6F6F2', 'facial': 'mustache', 'seed': 891, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
    **{f'swat{i}': {'preset': 'swat', 'hat': 'none', 'hair': 'bald', 'seed': 892 + i, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX} for i in (1, 2, 3)},
    'client1': BALDC('madame', 900), 'client2': BALDC('worker', 901), 'client3': BALDC('mamie', 902), 'client4': BALDC('sportif', 903),
    'savant': {'preset': 'doctor', 'seed': 905, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ministre': {'preset': 'politique', 'seed': 906, 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#7A2333', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{w: BALDC(p if p not in ('cuisinier', 'client2') else ('chef' if p == 'cuisinier' else 'worker'), 910 + i) for i, (w, p) in enumerate(CROWD)},
})
