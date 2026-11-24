#!/usr/bin/env python3
"""Le rayon (story 90, cycle 50; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man had the sun in his eyes. The space agency gathered three hundred scientists. Chosen solution: a parasol in space. Twelve rockets took off
from his garden. His tomatoes orbit the Earth. The parasol is the size of the country. Opening, it mowed down three satellites. The whole country
went grey. The sunflowers hung their heads. The solar panels were laid off. The agency declared the mission a success. The country marched with
torches. The gendarmes handcuffed the torches. A tank shot a hole in the parasol. Just one. Above his garden. Right in his eyes. The whole country
picnics at his place. He had a parasol in the garage.
Running gag: everything the State does lands on his garden (the rockets leave from it, the tomatoes are lost from it, the one hole is over it).
Staging: in his deckchair on the lawn of his house he squints into a blazing cartoon sun, a hand for a visor (close, from the sun's side, a warm
glare at the top of the frame); the reverse over his shoulder shows the sun over the street. In the agency's darkened control room rows of
scientists at desks all have his squinting photo on their screens, the same photo filling the wall under a red banner, the camera panning along the
rows. The director taps a whiteboard (the sun, a red and white parasol, the Earth with a house and a tiny man, LUI); a snap zoom on the parasol, a red
ring drawn round it. Twelve rockets lift off from his lawn one after another in clouds of smoke, he in his doorway with his deckchair. In space his
tomato stakes, tomatoes and watering can tumble past a satellite over the Earth's limb. The parasol snaps open in front of the sun and swallows it; a
cut to the globe, its round shadow swelling over a made-up ochre country. From the side, the rim of the opening parasol bats three satellites away.
From the air the shadow's edge slides over the suburbs (ÉTEINT). Under the grey sky, which is now the parasol's red and cream underside, a field of
sunflowers hangs its heads in a wave; laid-off solar panels on little legs queue at the unemployment office with cardboard signs; the director, at
the podium, beams under MISSION RÉUSSIE over the grey map, applause and flashes; a grey square of marchers holds torches up to the canopy; a gendarme
cuffs the torches lined up on a table. A tank raises its gun and fires; the camera tilts up after the shell; a hole bursts open in the canopy, the
sun blazing through (PERCÉ). Just one: from beside the single beam, a tilt from the hole down to his garden. From above, the lit disc of his lawn in a
dark country. Right in his eyes: the reverse first (the hole and its sun over the street), then his squint, the framing of shot one. The whole
country (the marchers, the gendarmes, the scientists, the director on the car roof) picnics in the disc, the camera craning up. He stands by his
deckchair with a small dusty parasol from the garage and opens it; dust; a look to us.
Natural look; cycle 50: props_rayon.js (squintScreen, squintWall, diagramBoard, rocketLawn, orbitTomatoes, orbitParasol, countryGlobe, shadowFront,
sunflowers, solarWalker, jobOffice, canopySky, lightShaft, sunPatch, skyTank, protestSign, lensGlare, handTorch, cuffedTorches, pressScreen,
picnicSpread, beachTowel, garageShelf, dustBurst); sun, deckChair, satellite, earthGlobe, parasol, garageShed, camFlash, table, chair, car (reused).
Lessons applied from the start: `lens` is the vertical field; characters are about 2.3 m tall with the box head; faces and key props above the
caption band (0.77-0.86) and heads below the card band (0.07-0.18) when a card stamps; every camera checked with project() before stills; the grey
shots get a per-shot grade and the canopy dome for a sky; no transparent key props; no English, no brands, no real organisation or flag.
Round 1 corrections (review 5.5 / 6.8): his face reads (the visor is his far hand on his brow, slit eyes under it; S17 an extreme crumple and squash;
S04 a close insert of a real take); S19 re-staged as a medium close (a child's faded parasol pulled out of the garage behind him, beige dust, a
double take, a blink, the hold); life in every hold (typing and nodding, the panels' queue, the director's beam, the cuffs, the crowd); S07 three
satellites batted away 0.4 s apart; S05 the patch drifts past at prop scale; S08 / S16 the shade drains the colour; S03 an upright parasol drawn,
the ring drawn on the snap; S14 the recoil; S06 the shadow settles on the country; S09 an overcast sky; no set clouds in the garden (noClouds).
New props: noClouds, kidParasol, hitSpark, cuffedTorchesUp; options added to rocketLawn (clear), orbitParasol (steady, jolts), orbitTomatoes (flow),
countryGlobe (shadowOver), sunPatch (darkColor), solarWalker (steps, droopAt), skyTank (squash, soft smoke), canopySky (overcast, lines), cuffedTorches."""
from story_kit import *
import math

st = Story('rayon', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 20)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def sub(a, b): return [a[i] - b[i] for i in range(3)]
def mul(a, s): return [a[i] * s for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]   # his right hand side (at -X when he faces +Z)
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
CHECKS = []
def chk(sid, frm, look, lens, pts):
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {project(frm, look, lens, p)}" for n, p in pts.items()))

def unproject(frm, look, lens, fx, fy, d, aspect=9 / 16):
    f = unit3(sub(look, frm)); rt = unit3([-f[2], 0.0, f[0]]); up = cross3(rt, f); th = math.tan(math.radians(lens) / 2)
    return [r(frm[i] + f[i] * d + rt[i] * (fx - 0.5) * 2 * d * th * aspect + up[i] * (0.5 - fy) * 2 * d * th) for i in range(3)]

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
DEAD = {'lid': 0.4, 'mouth': 'line'}
def blink(t, face=None): return [k(t, toon={'face': {**(face or DEAD), 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(t + 0.1), toon={'face': face or DEAD}, toonDur=0.06, keepPose=True)]
def R5(p, w=1, s=0.04): return [*p, w, s]
GEND = {'preset': 'cop', 'outfit': 'suit', 'suit': '#1E2A44', 'pants': '#1A2438', 'shirt': '#D9DEE8', 'lapel': '#141C30', 'tie': '#141C30', 'cuff': '#1E2A44', 'hat': 'none', 'hair': 'crew', 'facial': 'none',
        'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
def KEPI(pid, who): return P(pid, 'kepi', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'w': 0.222, 'd': 0.17, 'color': '#1A2438', 'band': '#C9CDD3'})
GREY = 'saturate(0.38) brightness(0.9) contrast(1.04)'          # the country under the parasol ((stills 1) brightness 0.82 was muddy)
GREYIN = 'saturate(0.55) brightness(0.9)'                         # indoors under the parasol (the press room)

for g_ in [('S01', 0.4, 'mec', 'squint'), ('S04', 1.1, 'mec', 'rockets'), ('S17', 0.75, 'mec', 'squint2'), ('S19', 2.4, 'mec', 'parasol')]:
    st.gag(*g_)

# ============================== his garden (pavillon: the house front at z -4.1, the lawn to the fence at z 2.2); the set's sun comes from +X+Z
CH = [-1.4, 0, -0.9]; RY = 40                                  # the deckchair, turned to the sun
SEAT = [CH[0], -0.15, CH[2]]                                   # a deckchair's seat is lower than a chair's
SUNDIR = [0.578, 0.438, 0.689]                                 # azimuth 140, elevation 26 (canopySky's convention): the cartoon sun and, later, the hole
HEAD = off(CH, RY, -0.18, 0.0, 1.3)                            # (stills 1) his head lounging: lower than guessed, the hand went over it
SUNP = add(HEAD, mul(SUNDIR, 34))
G = [r(CH[0] + 0.3), 0, r(CH[2] + 0.3)]                        # the middle of the lit disc
DOME = {'r': 90, 'hole1': True, 'az': 140, 'el': 26, 'holeR': 4, 'haze': 0.6}
LOUNGE = {'bend': {'spine': [-0.42, 0, 0, 1, None], 'neck': [0.12, 0, 0, 1, None]}, 'hands': {'L': 'open', 'R': 'open'},
          'touch': {'L': ['torso', 0.3, 0.1, 0.1, 1, 0.03]}}
SQUINT = {'lid': 0.38, 'low': 0.26, 'brow': -0.7, 'mouth': 'grimace'}   # (round 1) slits that still read: the eyes show under the hand
VISOR = R5(off(HEAD, RY, 0.24, 0.05, 0.1), 1, 0.05)           # (kept for the wide shots S16, S18) the right hand over his brow
VIS_T = ['face', -0.08, 0.84, 0.1, 1, 0.12, [1.0, 0.9, 0.3]]   # (round 1) his LEFT hand (the far side from the lens): fingertips at the brow, elbow out and up
REST_R = ['torso', -0.3, 0.1, 0.1, 1, 0.03]
def LOUNGEV(dy=0.0, dx=0.0, w=1): return {**LOUNGE, 'touch': {'R': REST_R, 'L': ['face', r(VIS_T[1] + dx), r(VIS_T[2] + dy), VIS_T[3], w, VIS_T[5], VIS_T[6]]}, 'hands': {'L': 'open', 'R': 'open'}}
GARDEN = {'clouds': 0}                                         # (round 1) no clouds: they read as floating beige slabs
def CHAIR(pid): return P(pid, 'deckChair', pos=CH, ry=RY)

# 1: the hook. Close from the sun's side: in his deckchair he squints into the light, a hand for a visor, a warm glare at the top of the frame; on
#    « soleil » the reverse over his shoulder: the blazing cartoon sun over the street
D1 = st.dur('S01'); T1 = 0.85
C1A = cam(0.0, off(CH, RY, 2.6, 0.4, 1.45), off(CH, RY, 2.4, 0.36, 1.46), off(CH, RY, -0.15, 0.0, 1.2), off(CH, RY, -0.15, 0.0, 1.21), lens=36)   # (round 1) a little closer and higher: his face under the hand
F1B = off(CH, RY, -3.2, -0.5, 1.0)
L1B, LENS1B, W1B = fit(F1B, {'head': HEAD, 'headTop': add(HEAD, [0, 0.3, 0]), 'sun': SUNP, 'sunTop': add(SUNP, [0, 3.2, 0]), 'chair': off(CH, RY, 0.2, 0, 0.6)}, margin=0.1, top=0.12, bottom=0.78)
C1B = cam(T1, F1B, add(F1B, mul(fwd(RY), 0.12)), L1B, L1B, lens=LENS1B)
CHECKS.append(f"S01b fit lens {LENS1B} {W1B}")
GLARE1 = unproject(C1A['from'], C1A['lookAt'], 36, 0.88, 0.05, 1.6)
LOOK1 = unproject(C1A['from'], C1A['lookAt'], 36, 0.62, 0.12, 1.2)   # (round 1) he squints toward the glare, almost at us: the painted face reads
chk('S01', C1A['from'], C1A['lookAt'], 36, {'head': HEAD, 'headTop': add(HEAD, [0, 0.45, 0]), 'glare': GLARE1, 'chairFoot': add(CH, [0, 0.1, 0])})
chk('S01b', C1B['from'], C1B['lookAt'], 50, {'head': HEAD, 'sun': SUNP, 'shoulder': off(CH, RY, -0.1, -0.2, 1.2)})
# (round 1) the squint lives: the lids flicker, the brow twitches, the hand adjusts its visor, a breath; after the cut he faces the sun (reverse)
# (round 2) no frozen hold: in the close the squint tightens in two steps (0.2 s, 0.5 s), the visor hand shifts and re-shades each time, the head
#     tilts away from the glare; in the reverse the shoulders hunch, the hand readjusts on his brow, and he breathes (a slow rise and fall)
def LV1(dy=0.0, dx=0.0, tilt=0.0, fwd=0.12, twist=0.0, spine=-0.42):
    return {**LOUNGEV(dy, dx), 'bend': {'spine': [spine, 0, 0, 1, None], 'neck': [fwd, tilt, twist, 1, None]}}
SQ1 = {**SQUINT, 'lid': 0.62, 'low': 0.36, 'brow': -0.85}
SQ2 = {**SQUINT, 'lid': 0.86, 'low': 0.46, 'brow': -1.0, 'mouth': 'clench', 'cheeks': 0.5}
HERO1 = [k(0.0, look=LOOK1), k(0.0, toon={**LV1(), 'face': SQUINT}, toonDur=0.0),
         k(0.16, toon={**LV1(0.05, -0.04, 0.12, 0.14, -0.08), 'face': SQ1, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.08, toonEase='out'),
         k(0.3, toon={**LV1(0.03, -0.02, 0.14, 0.14, -0.1), 'face': {**SQ1, 'lid': 0.56}, 'sq': [1, 1, 1]}, toonDur=0.12),
         k(0.48, toon={**LV1(-0.02, 0.04, 0.26, 0.18, -0.18), 'face': SQ2, 'sq': [1.05, 0.95, 1.05]}, toonDur=0.07, toonEase='out'),
         k(0.6, toon={**LV1(-0.01, 0.03, 0.28, 0.18, -0.2), 'face': {**SQ2, 'tremble': 0.5}, 'sq': [1.02, 0.98, 1.02]}, toonDur=0.1),
         k(0.74, toon={**LV1(0.0, 0.035, 0.27, 0.17, -0.19), 'face': {**SQ2, 'lid': 0.8}, 'sq': [1, 1, 1]}, toonDur=0.1),
         k(1.0, look=SUNP, lookDur=0.2),
         k(1.02, toon={**LV1(0.02, 0.0, 0.1, 0.36, 0.0, -0.3), 'face': SQ2, 'sq': [1.07, 0.92, 1.07]}, toonDur=0.16, toonEase='inOut'),
         k(1.3, toon={**LV1(0.08, -0.07, 0.1, 0.34, 0.0, -0.3), 'face': SQ2, 'sq': [1.06, 0.93, 1.06]}, toonDur=0.1, toonEase='out'),
         k(1.45, toon={**LV1(0.03, 0.03, 0.08, 0.34, 0.0, -0.3), 'face': SQ2, 'sq': [1.05, 0.94, 1.05]}, toonDur=0.1),
         k(1.68, toon={**LV1(0.03, 0.03, 0.06, 0.3, 0.0, -0.36), 'face': SQ2, 'sq': [1.03, 0.98, 1.03]}, toonDur=0.22, toonEase='inOut'),
         k(1.92, toon={**LV1(0.04, 0.02, 0.08, 0.34, 0.0, -0.28), 'face': SQ2, 'sq': [1.07, 0.93, 1.07]}, toonDur=0.18, toonEase='inOut')]
st.shot('S01', 'pavillon', setOpts=GARDEN, actors=[act('mec', SEAT, RY, 'sit', 'unimpressed', keys=HERO1)],
        props=[P('nuages01', 'noClouds'), CHAIR('chaise1'), P('soleil1', 'sun', pos=SUNP, opts={'r': 2.6}, keys=[k(0.0, scale=1.0, dur=0.0), k(T1, scale=1.1, dur=0.3, ease='inOut')]),
               P('eclat1', 'lensGlare', pos=GLARE1, opts={'s': 1.5, 'op': 0.45}, keys=[k(T1, visible=False)])],
        cams=[C1A, C1B])
st.cue('sfx:static', 'S01', 0.0, 0.12); st.cue('whoosh', 'S01', T1 - 0.05, 0.15, 0.25, 600, 2400)

# ============================== the agency (the office set, walls darkened: a control room)
CTRL = {'door': False, 'printer': False, 'picture': False, 'carpet': False, 'wall': '#3C4A5C', 'band': '#2C3846', 'trim': '#1E2834', 'floor': '#4A5058'}
ROWS = [-1.7, 0.1, 1.9]; COLS = [-1.6, 0.0, 1.6]
# 2: three hundred scientists. Panning along the rows from behind them: every screen shows his squinting photo, the wall screen too
D2 = st.dur('S02')
SAV = [(f'savant{i + 1}', [x, 0, r(z + 0.85)]) for i, (x, z) in enumerate([(x, z) for z in ROWS[1:] for x in COLS] + [(0.0, ROWS[0])])]
C2 = cam(0.0, [3.0, 2.55, 4.7], [1.3, 2.5, 4.9], [0.7, 1.45, -1.3], [-0.7, 1.45, -1.3], lens=50)
chk('S02', C2['from'], C2['lookAt'], 50, {'wallTop': [0, 3.4, -3.45], 'wallBot': [0, 0.85, -3.45], 'scr': [1.6, 1.35, 0.1], 'savHead': [1.6, 1.75, 2.75]})
# (round 1) the room works: each scientist types (hands on the keyboard, tapping in turn) and nods at his screen in a cascade along the rows; one
#     turns round to us and blinks
KB = lambda pos, sd, up: R5([r(pos[0] + 0.12 * sd), r(0.8 + 0.035 * up), r(pos[2] - 0.55)], 1, 0.04)
def TYPE2(pos, i):
    out = []
    for j in range(int(D2 / 0.11)):
        tt = r(0.05 + 0.11 * j + 0.03 * (i % 3)); a_ = (j + i) % 2
        out.append(k(tt, toon={'reach': {'L': KB(pos, 1, a_), 'R': KB(pos, -1, 1 - a_)}, 'hands': {'L': 'open', 'R': 'open'}, 'face': DEAD}, toonDur=0.06))
    return out
def NOD2(pos, i):
    t0 = r(0.25 + 0.22 * i); scr = [pos[0], 1.35, r(pos[2] - 0.9)]
    return [k(t0, look=add(scr, [0, -0.35, 0]), lookDur=0.1), k(r(t0 + 0.18), look=scr, lookDur=0.12), k(r(t0 + 0.36), look=add(scr, [0, -0.3, 0]), lookDur=0.1), k(r(t0 + 0.52), look=scr, lookDur=0.12)]
st.shot('S02', 'office', setOpts=CTRL, actors=[
        act(sid, pos, 180, 'sit', 'neutral', keys=[k(0.0, look=[pos[0], 1.3, r(pos[2] - 0.9)]), *TYPE2(pos, i),
            *(NOD2(pos, i) if sid != 'savant3' else [k(0.9, look='camera', lookDur=0.15), *blink(1.4), k(1.9, look=[pos[0], 1.3, r(pos[2] - 0.9)], lookDur=0.15)])]) for i, (sid, pos) in enumerate(SAV)],
        props=[P('mur2', 'squintWall', pos=[0, 2.15, -3.45], opts={'w': 4.4}),
               *[P(f'ecran2_{i}', 'squintScreen', pos=[x, 0, z], opts={'desk': True}) for i, (x, z) in enumerate([(x, z) for z in ROWS for x in COLS])],
               *[P(f'chaise2_{i}', 'chair', pos=pos, ry=180, opts={'color': '#2A3240'}) for i, (sid, pos) in enumerate(SAV)]],
        cams=[C2])
st.cue('sfx:ticks', 'S02', 0.1, 0.2)

# 3: the chosen solution. The director taps the whiteboard: the sun, a parasol, the Earth with LUI; on « parasol » a snap zoom, a red ring round it
D3 = st.dur('S03'); TAP3 = 1.26
BOARD = [0.0, 0, -1.2]; PARA = [0.0, 1.55, -1.16]
DIR3 = [1.0, 0, -0.65]; RYD = -40
C3A = cam(0.0, [0.55, 1.75, 3.9], [0.5, 1.72, 3.6], [0.25, 1.5, -1.1], [0.22, 1.5, -1.1], lens=50)
C3B = cam(TAP3, [0.02, 1.54, 1.3], [0.02, 1.54, 1.15], [0.0, 1.54, -1.2], [0.0, 1.54, -1.2], lens=40, shake=0.02)   # (round 1) the whole drawing, header to label, above the caption band
chk('S03', C3A['from'], C3A['lookAt'], 50, {'boardL': [-1.2, 1.55, -1.17], 'boardR': [1.2, 1.55, -1.17], 'dirHead': [DIR3[0], 2.0, DIR3[2]], 'boardTop': [0, 2.25, -1.17]})
chk('S03b', C3B['from'], C3B['lookAt'], 40, {'header': [0, 2.08, -1.17], 'headerL': [-0.42, 2.08, -1.17], 'paraTop': [0, 1.9, -1.16], 'label': [0, 1.146, -1.16], 'sunEdge': [-0.61, 1.55, -1.17], 'earthEdge': [0.54, 1.44, -1.17]})
# (round 1) the tap gets a wind-up (the hand drawn back and up, a squash), two sharp taps with a rebound each, then the hand drops away before the
#     snap zoom; the ring is drawn on the snap
TAPP = lambda dz, dy=0.0, dx=0.0: R5([r(0.08 + dx), r(1.62 + dy), r(-1.15 + dz)], 1, 0.05)
T1_3, T2_3 = r(TAP3 - 0.3), r(TAP3 - 0.14)
SM3 = {'lid': 0.3, 'mouth': 'smirk', 'brow': 0.3}
st.shot('S03', 'office', setOpts=CTRL, actors=[
        act('directeur', DIR3, RYD, 'stand', 'neutral', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': R5([0.62, 1.2, -0.5], 0.0, 0.05)}, 'hands': {'R': 'point'}, 'face': SM3}, toonDur=0.0),
            k(0.45, look=PARA, lookDur=0.15), *blink(0.25, SM3),
            k(0.55, toon={'reach': {'R': TAPP(0.3, 0.05)}, 'hands': {'R': 'point'}, 'face': SM3}, toonDur=0.2),
            k(r(T1_3 - 0.22), toon={'reach': {'R': TAPP(0.42, 0.25, 0.25)}, 'hands': {'R': 'point'}, 'face': {**SM3, 'brow': 0.6}, 'sq': [1.05, 0.95, 1.05]}, toonDur=0.12, toonEase='inOut'),
            k(T1_3, toon={'reach': {'R': TAPP(0.0)}, 'hands': {'R': 'point'}, 'face': {**SM3, 'mouth': 'bigsmile'}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.05, toonEase='in', blend=0.02),
            k(r(T1_3 + 0.06), toon={'reach': {'R': TAPP(0.12, 0.04)}, 'hands': {'R': 'point'}, 'sq': [1, 1, 1]}, toonDur=0.05, keepPose=True),
            k(T2_3, toon={'reach': {'R': TAPP(0.0, -0.02)}, 'hands': {'R': 'point'}}, toonDur=0.04, toonEase='in', keepPose=True),
            k(r(T2_3 + 0.06), toon={'reach': {'R': TAPP(0.2, 0.06, 0.15)}, 'hands': {'R': 'point'}}, toonDur=0.05, keepPose=True),
            k(r(TAP3 - 0.04), toon={'reach': {'R': R5([0.62, 1.2, -0.5], 0.0, 0.05)}, 'hands': {'R': 'point'}, 'face': {'lid': 0.3, 'mouth': 'bigsmile', 'brow': 0.4}}, toonDur=0.08),
            k(r(TAP3 + 0.6), look='camera', lookDur=0.12)])],
        props=[P('tableau3', 'diagramBoard', pos=BOARD, opts={'w': 2.4, 'ringAt': r(TAP3 + 0.04), 'ringDur': 0.3, 'ringWobble': True})],
        cams=[C3A, C3B])
st.cue('sfx:click', 'S03', T1_3, 0.4); st.cue('sfx:click', 'S03', T2_3, 0.35); st.cue('sfx:squeak', 'S03', r(TAP3 + 0.06), 0.3)

# 4: twelve rockets from his lawn. Wide from the pavement: the rockets lift off one after another in smoke; he gapes in the doorway, deckchair in hand
D4 = st.dur('S04')
# (round 2) the twelve are seen: a low camera on the pavement, the rockets bigger (3.6 m) in three rows inside the 9:16 frame, either side of the path
#     (he stands in the doorway between them); the first lifts off on frame 1 and all twelve go inside the wide (0 to 0.61 s), climbing on white
#     exhaust columns, the first leaving the top of the frame at the cut
RS4 = 0.85
# (round 3) a wider gap down the middle (the path to his door): the rockets and their smoke kept clear of it, so the doorway and he read in the wide
SPOTS = [[-1.65, -3.0], [-0.65, -3.0], [2.3, -3.0], [3.3, -3.0], [-1.35, -1.8], [-0.35, -1.8], [2.15, -1.8], [3.1, -1.8], [-1.1, -0.7], [-0.1, -0.7], [2.0, -0.7], [2.85, -0.7]]
# a front rocket first (frame 1 shows a clear ignition), then the back rows rise above the front ones, the front row last
ORDER4 = [1, 4, 7, 2, 8, 3, 6, 10, 0, 11, 5, 9]
DOOR = [0.97, 0, -3.75]
C4 = cam(0.0, [0.95, 1.0, 7.4], [0.95, 0.95, 7.0], [0.8, 3.0, -3.0], [0.8, 3.3, -3.0], lens=60, shake=0.06)
chk('S04', C4['from'], C4['lookAt'], 60, {'head': [DOOR[0], 2.05, DOOR[2]], 'feet': DOOR, **{f'r{i}': [x, 0.0, z] for i, (x, z) in enumerate(SPOTS)}, 'nose0': [-1.65, 4.25 * RS4, -3.0], 'nose3': [3.3, 4.25 * RS4, -3.0], 'roof': [0, 4.6, -6.6]})
# (round 1) the take gets a close insert: the wide shows the lift-off (he is a speck in it), then a cut to him in the doorway, a dip (anticipation),
#     the take (body stretched up, head long and thin, the eyes out on red stalks looking up at the rockets, the jaw down to the chest, hands flung
#     open: the deckchair drops), held trembling, an overshoot squash and the settle into a long gape with a blink
CUT4 = 0.8; TK4 = 1.02; TAKE2_4 = 1.78
# (round 2) the insert is lower and further back: the eave, the roof's ridge and a band of sky over it (19 %) are behind him, and a second battery,
#     in the back garden, streaks up past the ridge behind his head, one rocket after another on its column of smoke, each launch flickering warm
#     on the wall behind him; the take comes on the third rocket
F4B = [0.95, 1.0, 0.2]
L4B, LENS4B, W4B = fit(F4B, {'headTop': [DOOR[0], 4.4, DOOR[2]], 'hip': [DOOR[0], 0.8, DOOR[2]], 'sky': [DOOR[0], 9.0, -11.0], 'side': [DOOR[0] - 0.55, 2.0, DOOR[2]], 'side2': [DOOR[0] + 0.55, 2.0, DOOR[2]]}, margin=0.06, top=0.04, bottom=0.74, lenses=range(30, 70))
C4B = cam(CUT4, F4B, add(F4B, [-0.03, 0.0, -0.1]), L4B, add(L4B, [0, 0.05, 0]), lens=LENS4B, shake=0.025)
CHECKS.append(f"S04b fit lens {LENS4B} {W4B}")
BACK4 = [[-0.9, -10.3], [2.9, -10.6], [0.15, -10.9], [2.05, -10.2], [-0.45, -10.6], [2.5, -11.0], [3.3, -10.4], [1.3, -10.8]]
APPEAR4 = [0.86, 0.93, 1.0, 1.09, 1.2, 1.34, 1.52, 1.76]          # when each nose clears the eave line (the third on the take, TK4; (round 3) the eighth, right behind his head, on the second take)
LIFT4 = [r(a - 0.22) for a in APPEAR4]                         # (v0 14, acc 8, s 0.85: the nose clears the eave line about 0.22 s after lift-off, measured on stills)
chk('S04b', F4B, L4B, LENS4B, {'headTop': [DOOR[0], 3.4, DOOR[2]], 'ridge': [DOOR[0], 4.6, -6.6], 'eave': [DOOR[0], 2.9, -4.1], **{f'b{i}': [x, 6.7, z] for i, (x, z) in enumerate(BACK4)}, 'chair': [DOOR[0], 0.9, -3.05]})
UP4 = add(F4B, [0.0, 0.3, 0.0])                                # he looks at us (eyes on stalks follow the head's axis), the pupils go up
HOLD4 = {'reach': {'L': R5([DOOR[0] + 0.28, 0.88, -3.4], 1, 0.04), 'R': R5([DOOR[0] - 0.28, 0.88, -3.4], 1, 0.04)}, 'hands': {'L': 'grip', 'R': 'grip'}}
TAKE4 = {'sq': [0.86, 1.2, 0.86], 'scl': {'head': [0.84, 1.3, 1.0]}, 'hairUp': 1.0, 'hands': {'L': 'open', 'R': 'open'},
         'face': {'lid': 0.0, 'pop': 1.0, 'popLen': 0.34, 'eyeScale': 1.3, 'stalkRed': 1, 'eyePitch': -0.8, 'jaw': 0.85, 'jawLen': 0.7, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}}
GAPE4 = {'lid': 0.0, 'eye': 0.4, 'jaw': 0.45, 'mouth': 'O', 'brow': 0.8, 'gy': -0.6}
def TK(sq, head, **f): return {**TAKE4, 'sq': sq, 'scl': {'head': head}, 'face': {**TAKE4['face'], **f}}
HERO4 = [k(0.0, look='camera'), k(0.0, toon={**HOLD4, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0),
         k(0.3, look=[-1, 6, -1], lookDur=0.2), k(0.35, toon={**HOLD4, 'face': {'lid': 0.1, 'mouth': 'o', 'brow': 0.5}}, toonDur=0.1),
         k(r(CUT4 - 0.02), look=UP4, lookDur=0.06),
         k(r(TK4 - 0.14), toon={**HOLD4, 'sq': [1.1, 0.88, 1.1], 'scl': {'head': [1.12, 0.88, 1.0]}, 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.1, toonEase='inOut'),
         k(r(TK4 - 0.035), toon={**TAKE4, 'sq': [0.74, 1.42, 0.74], 'scl': {'head': [0.7, 1.55, 1.0]}, 'face': {**TAKE4['face'], 'popLen': 0.5, 'jaw': 1.0}}, toonDur=0.035, toonEase='out', blend=0.02),
         k(TK4, toon=TAKE4, toonDur=0.035, toonEase='inOut'),
         *[k(r(TK4 + 0.07 * (i + 1)), toon=TK([0.86 + 0.015 * (i % 2), 1.2 - 0.025 * (i % 2), 0.86 + 0.015 * (i % 2)], [0.84, 1.3 - 0.03 * (i % 2), 1.0], popLen=0.34 - 0.03 * (i % 2)), toonDur=0.04) for i in range(4)],
         # (round 3) no neutral hold: the take settles a little, still stretched and trembling, and the last rocket streaking up right behind his
         #     head brings a second, smaller take, held trembling to the cut
         *[k(r(TK4 + 0.36 + 0.06 * i), toon=TK([0.9 + 0.015 * (i % 2), 1.14 - 0.02 * (i % 2), 0.9 + 0.015 * (i % 2)], [0.88, 1.2 - 0.03 * (i % 2), 1.0], popLen=0.26 - 0.03 * (i % 2), jaw=0.75), toonDur=0.05) for i in range(6)],
         k(r(TAKE2_4 - 0.07), toon=TK([1.05, 0.94, 1.05], [1.0, 1.05, 1.0], popLen=0.18, jaw=0.6), toonDur=0.05, toonEase='inOut'),
         k(TAKE2_4, toon=TK([0.8, 1.3, 0.8], [0.76, 1.42, 1.0], popLen=0.42, jaw=0.95), toonDur=0.035, toonEase='out'),
         k(r(TAKE2_4 - 0.02), look=add(UP4, [0.0, 0.6, 0]), lookDur=0.05),
         *[k(r(TAKE2_4 + 0.07 + 0.06 * i), toon=TK([0.82 + 0.02 * (i % 2), 1.27 - 0.03 * (i % 2), 0.82 + 0.02 * (i % 2)], [0.78, 1.38 - 0.04 * (i % 2), 1.0], popLen=0.4 - 0.04 * (i % 2), jaw=0.95), toonDur=0.04) for i in range(int((D4 - TAKE2_4 - 0.07) / 0.06))]]
st.shot('S04', 'pavillon', setOpts=GARDEN, actors=[act('mec', DOOR, 0, 'stand', 'neutral', keys=HERO4)],
        props=[P('fusees4', 'rocketLawn', pos=[0, 0, 0], opts={'spots': SPOTS, 's': RS4, 't0': -0.25, 'gap': 0.055, 'order': ORDER4, 'acc': 22, 'v0': 1.0, 'trail': True, 'clear': [-0.4, 2.35], 'hideAfter': CUT4}), P('nuages4', 'noClouds'),
               P('fusees4b', 'rocketLawn', pos=[0, 0, 0], opts={'spots': BACK4, 's': RS4, 'times': LIFT4, 'acc': 8, 'v0': 14, 'trail': True, 'puffs': False}),
               P('lueur4', 'wallFlicker', pos=[DOOR[0], 1.75, -4.06], opts={'w': 3.4, 'h': 3.2, 'op': 0.95, 'color': '#FFB050', 'at': APPEAR4}),
               # (round 2) hang time: the flung hands knock the deckchair up, it hangs for five frames, then crashes forward
               P('chaise4', 'deckChair', pos=[DOOR[0], 0, -3.05], ry=0, keys=[k(r(TK4 + 0.02), to=[DOOR[0], 0.28, -3.0], dur=0.08, ease='out'), k(r(TK4 + 0.02), rotTo=[0.25, 0.1, 0.05], dur=0.08, ease='out'),
                   k(r(TK4 + 0.2), rotTo=[1.45, 0.25, 0.1], dur=0.15, ease='in'), k(r(TK4 + 0.2), to=[DOOR[0] + 0.1, 0, -2.75], dur=0.15, ease='in')])],
        cams=[C4, C4B])
st.cue('sfx:jet', 'S04', 0.02, 0.5); st.cue('sfx:boing', 'S04', TK4, 0.4); st.cue('thud', 'S04', r(TK4 + 0.35), 0.3); st.cue('engine', 'S04', 0.02, 0.35, 1.8); st.cue('thud', 'S04', 0.05, 0.3)

# ============================== space (spaceDark)
# 5: his tomatoes in orbit. Over the Earth's limb: his tomato stakes, loose tomatoes and the watering can tumble past a satellite
D5 = st.dur('S05')
# (stills 1) a round planet low in the frame: the near limb of a big one read as giant green triangles
C5 = cam(0.0, [0.0, 0.8, 4.6], [0.15, 0.85, 4.2], [0.0, -0.1, -4.0], [0.1, -0.05, -4.0], lens=48)
# (round 2) the Earth is huge and close behind (radius 30): its curved limb crosses the lower part of the frame under the drifting patch, which is
#     at prop scale against it; the watering can (bigger, a clear silhouette: handle, spout, rose) crosses the middle side on
GLOBE5 = [1.5, -17.6, -11.0]; RG5 = 16.0; TH5 = 1.35              # (the globe turned on its side: the north cap read as a white slab)
# (round 1) the patch drifts past at prop scale, close to the lens (2 to 4 m), each piece on its own arc and tumbling: stakes with their plants,
#     loose tomatoes, the green watering can; the satellite crosses behind them over the Earth's limb
chk('S05', C5['from'], C5['lookAt'], 48, {'limbTop': add(GLOBE5, [0, RG5, 0]), 'limbL': add(GLOBE5, [-6, r(math.sqrt(RG5 ** 2 - 36)), 0]), 'tomatoes': [0.2, 0.8, 1.1], 'can0': [1.3, 0.65, 1.75], 'sat0': [3.4, 1.9, -8.0], 'sat1': [-2.4, 1.6, -8.0]})
st.shot('S05', 'spaceDark', actors=[],
        props=[P('terre5', 'earthGlobe', pos=[r(GLOBE5[0] - RG5 * math.sin(TH5)), r(GLOBE5[1] - RG5 * math.cos(TH5)), GLOBE5[2]], rot=[0, 0, -TH5], opts={'radius': RG5, 'seed': 5}),
               P('tomates5', 'orbitTomatoes', pos=[0.2, 0.8, 1.1], scale=1.1, opts={'flow': [-1.15, 0.1, 0.15], 'box': [2.6, 1.0, 1.6], 'tumble': 2.2, 'loose': 6, 'canScale': 1.2, 'canAt': [1.0, -0.2, -0.2], 'canSpin': [0.06, 0.18, 0.05]}),
               P('sat5', 'satellite', pos=[3.4, 1.9, -8.0], rot=[0.3, 0.6, 0.1], scale=0.55, keys=[k(0.0, to=[-2.4, 1.6, -8.0], dur=D5, ease='linear'), k(0.0, rotTo=[0.3, 1.1, 0.25], dur=D5, ease='linear')]),
               ],
        cams=[C5])
st.cue('sfx:tense', 'S05', 0.0, 0.15)

# (round 1) S06: the shadow swells past the country's outline and settles back onto it (outBack), its cap no wider than the country
# 6: the size of the country. The parasol snaps open in front of the sun and swallows it; cut to the globe: its round shadow swells over the country
D6 = st.dur('S06'); OPEN6 = 0.2; CUT6 = 0.92
# (round 2) tilted 20 degrees toward the lens, the pole and its crook handle hang below the canopy (face on it read as a peppermint); closer, and the
#     canopy in the upper half, the handle in the lower
C6A = cam(0.0, [0.4, 1.4, 22.0], [0.3, 1.45, 20.5], [0.0, 0.6, -28.0], [0.0, 0.65, -28.0], lens=30)
TILT6 = [-PI / 2 + 0.5, 0.14, 0.0]
C6B = cam(CUT6, [60.0, 0.9, 14.5], [59.0, 1.05, 13.5], [60.0, 0.2, 0.0], [60.0, 0.2, 0.0], lens=44)   # (round 3) a slow drift round the globe in the hold
chk('S06', C6A['from'], C6A['lookAt'], 30, {'sun': [0, 4, -70], 'paraTop': [0, 9.3, -30], 'paraL': [-6.5, 3.2, -28], 'paraR': [6.5, 3.2, -28], 'handle': [2.0, -3.6, -15.6]})
chk('S06b', C6B['from'], C6B['lookAt'], 44, {'globeTop': [60, 3, 0], 'globeBot': [60, -3, 0], 'country': [60, 0, 3]})
st.shot('S06', 'spaceDark', actors=[],
        props=[P('soleil6', 'sun', pos=[0, 4, -70], opts={'r': 4.5}),
               P('parasol6', 'orbitParasol', pos=[0, 3.2, -28], rot=TILT6, opts={'r': 6.5, 'openAt': OPEN6, 'openDur': 0.5, 'spin': 0.15, 'pole': 2.2, 'poleR': 0.022, 'handle': True}),
               P('globe6', 'countryGlobe', pos=[60, -3, 0], opts={'radius': 3, 'shadowAt': r(CUT6 + 0.1), 'shadowDur': 0.55, 'shadowAng': 0.44, 'shadowOver': True})],
        cams=[C6A, C6B])
st.cue('whoosh', 'S06', OPEN6, 0.3, 0.4, 300, 1800); st.cue('sfx:poof', 'S06', r(OPEN6 + 0.35), 0.45)

# 7: it mowed down three satellites. From the side, the rim of the opening parasol bats them away one after another
D7 = st.dur('S07')
# (round 1) from the side, nearly along the canopy's plane: the furled spike opens at a steady rate (the rim's radius grows 4.5 m/s), and three big
#     satellites parked in the rim's plane are batted away one after the other, 0.4 s apart: a contact frame, a spark, the canopy shudders, the
#     satellite spins off out of the frame; then the open parasol holds, turning slowly, with a last panel tumbling away
OPEN7, DUR7 = 0.15, 1.7
R7 = 6.5; PZ7 = -10.0; H7 = R7 * 0.32
def op7(u): return u / 0.85 * 1.03
def rim7(op): return r(R7 * (0.05 + 0.95 * op)), r(PZ7 + H7 * (1 + (1 - op) * 3.2))   # the rim's radius and its z (the furled cone is longer)
def at7(op): return r(OPEN7 + op * 0.85 / 1.03 * DUR7, 2)
SATS7 = []
for n, op, sg, x in [('sat7a', 0.35, 1.0, 0.0), ('sat7b', 0.62, -1.0, 0.3), ('sat7c', 0.9, 1.0, -0.3)]:
    rr, zz = rim7(op); SATS7.append((n, [x, r(sg * (rr + 0.5)), r(zz - 0.25)], [0.0, sg, 0.45], sg, at7(op)))
F7 = [17.0, 0.6, -2.4]
C7 = cam(0.0, F7, add(F7, [-1.2, 0.1, -0.5]), [0.0, 0.7, -6.6], [0.0, 0.8, -7.0], lens=54)
chk('S07', C7['from'], C7['lookAt'], 54, {'rimTop': [0, R7, PZ7 + H7], 'rimBot': [0, -R7, PZ7 + H7], 'apex': [0, 0, PZ7], 'furled': [0, 0, rim7(0)[1]], **{n: p for n, p, d, sg, h in SATS7}})
HITS7 = {n: h for n, p, d, sg, h in SATS7}
CHECKS.append(f"S07 hits {HITS7}")
# (round 3) each satellite stretches as it spins off (a squash key that springs back); the second one first pancakes flat on the rim for 0.1 s and
#     pops back into shape as it flies (flatten and re-inflate)
def SATK(n, p, d, sg, h):
    out = add(p, mul(d, 13.0)); pk = 0.1 if n == 'sat7b' else 0.0
    ks = [k(0.0, to=add(p, [0.0, -0.25 * sg, 0.3]), dur=h, ease='linear'), k(0.0, rotTo=[0.15, 1.35, 0.1 * sg], dur=h, ease='linear'),
          k(h, to=add(p, mul(d, 0.15 if pk else 0.6)), dur=0.04 if pk else 0.06, ease='out'), k(r(h + 0.06 + pk), to=out, dur=0.5, ease='linear'), k(r(h + pk), rotTo=[4.5 * sg, 6.0, 2.5], dur=0.56, ease='out'),
          k(h, scale=0.68, dur=0.0), k(r(h + 0.03), scale=0.58, dur=0.05)]
    if pk: ks.append(k(h, squash=[1.55, 0.3, 1.55], dur=2.0))   # a long spring: about 0.1 s still flat before the pop
    ks.append(k(r(h + 0.06 + pk), squash=[0.62, 1.7, 0.62], dur=0.4))
    return ks
st.shot('S07', 'spaceDark', actors=[],
        props=[P('parasol7', 'orbitParasol', pos=[0, 0, PZ7], rot=[-PI / 2, 0, 0], opts={'r': R7, 'openAt': OPEN7, 'openDur': DUR7, 'steady': True, 'spin': 0.35, 'jolts': list(HITS7.values())}),
               P('terre7', 'earthGlobe', pos=[-40, -30, -14], opts={'radius': 14, 'seed': 5}),
               *[P(n, 'satellite', pos=p, rot=[0.15, 1.35, 0.1 * sg], scale=0.62, keys=SATK(n, p, d, sg, h)) for n, p, d, sg, h in SATS7],
               *[P(f'etincelle7{n[-1]}', 'hitSpark', pos=add(p, [0.6, -0.4 * sg, 0.2]), opts={'at': h, 's': 1.3, 'face': F7}) for n, p, d, sg, h in SATS7]],
        cams=[C7])
for n in HITS7: st.cue('clang', 'S07', HITS7[n], 0.4)

# 8: the whole country went grey. From the air, the shadow's edge slides over the suburbs (ÉTEINT)
D8 = st.dur('S08')
# (stills 1) the disc's y goes in pos: the prop's own y was overwritten and the disc lay under the lawn
# (staging 2) the slide happens inside the prop (dx0, moveAt): a key move left the disc out of the whole-film render
# (round 1) « gris »: the shadow is a mid cool grey laid over the land at 80 %, so what it covers loses its colour, not only its light (the near-black
#     disc kept the red and blue roofs saturated)
C8 = cam(0.0, [0.0, 140.0, 240.0], [0.0, 134.0, 226.0], [0.0, 0.0, -120.0], [0.0, 0.0, -120.0], lens=46)
# (round 3) the edge is timed on the screen: it comes in from the far land (the top of the frame) and slides toward us with an ease-in over 1.5 s,
#     so the card band is already dark when ÉTEINT drops (1.15 s), the edge is still crossing the middle of the frame with a lit strip under it, and
#     it leaves the frame at the bottom before the cut; the shade is darker and cooler (switched off, not fog); little cars on the streets stop dead
#     as it reaches them
CARD8 = 1.15; E0_8, E1_8, V0_8, V1_8, EX8 = 0.18, 1.72, 0.05, 1.08, 1.5
R8, CX8 = 3000.0, -1000.0
def cam8(t):
    u = min(1.0, max(0.0, t / D8)); return [0.0, r(140 - 6 * u), r(240 - 14 * u)]
def v8(t): return V0_8 + (V1_8 - V0_8) * min(1.0, max(0.0, (t - E0_8) / (E1_8 - E0_8))) ** EX8
def edge_z(t, x=0.0):
    want, fr = v8(t), cam8(t); lo, hi = -6000.0, fr[2] - 1.0
    for _ in range(60):
        m = (lo + hi) / 2; q = project(fr, [0.0, 0.0, -120.0], 46, [x, 16.0, m])
        if q is None or q[1] < want: lo = m
        else: hi = m
    return (lo + hi) / 2
def cz8(t): return edge_z(t) - math.sqrt(R8 ** 2 - CX8 ** 2)
PATH8 = [[r(t_, 2), 0.0, r(cz8(t_), 1)] for t_ in [i * 0.05 for i in range(int(D8 / 0.05) + 2)]]
CHECKS.append(f"S08 edge z at card {r(edge_z(CARD8), 1)} v {r(v8(CARD8))} | v at 0.6 {r(v8(0.6))}")
def tstop8(x, z, ry, v):
    for i in range(0, 400):
        t_ = i * 0.005; a_ = math.radians(ry); px, pz = x + math.sin(a_) * v * t_, z + math.cos(a_) * v * t_
        if cz8(t_) + math.sqrt(max(0.0, R8 ** 2 - (px - CX8) ** 2)) >= pz + 3: return r(t_, 3)
    return 9.0
CARS8 = [(-30.0, 62.5 - 4, 90, 15.0, '#E04A3A'), (20.0, 62.5 + 4, -90, 13.0, '#F2C21E'), (-45.0, 12.5 - 4, 90, 14.0, '#2E8FE0'), (35.0, 12.5 + 4, -90, 16.0, '#F07A2A'),
         (-20.0, -37.5 - 4, 90, 15.0, '#F4F1EA'), (50.0 + 2, -60.0, 0, 15.0, '#E04A3A'), (-62.0 - 2, -20.0, 0, 13.0, '#F2C21E'), (5.0, -87.5 + 4, -90, 14.0, '#2E8FE0')]
CARK8 = [[x, z, ry, v, tstop8(x, z, ry, v), c] for x, z, ry, v, c in CARS8]
CHECKS.append("S08 car stops " + ' '.join(str(c[4]) for c in CARK8))
# (round 2) the scattered white specks over the grey suburb: far flat-shaded instanced triangles (smoothFar); no light shafts in the aerial view
st.shot('S08', 'aerialSuburb', look={'shafts': 0}, actors=[],
        props=[P('lisse8', 'smoothFar'), P('autos8', 'stopCars', pos=[0, 0, 0], opts={'cars': CARK8, 's': 2.6}),
               P('ombre8', 'shadowFront', pos=[CX8, 16, 0], opts={'r': R8, 'op': 0.84, 'color': '#38424F', 'path': PATH8, 'edge': 16})],
        cams=[C8])
st.card('S08', 'ÉTEINT', at=CARD8)
st.cue('gust', 'S08', 0.1, 0.3, 1.2); st.cue('thud', 'S08', 1.15, 0.4)

# ============================== under the parasol: the canopy for a sky, the grade grey
CAN = {'r': 90, 'haze': 0.75, 'overcast': 0.9, 'lines': False}  # (staging 2) haze: the dome's foot reads as an overcast horizon; (round 1) cloud banks, no gore lines
CAN0 = {'r': 90, 'haze': 0.75}                                 # S12 keeps the bare striped canopy (the torch beams on the gores)
OVER = {'sun': 0.4, 'fill': 1.4, 'sunDisc': False}             # (round 1) under the canopy: soft light, no hard cast shadows
# 9: the sunflowers hung their heads. Low in the field: the heads swing down in a wave from the front row back
D9 = st.dur('S09')
# (round 1) low and tilted up (the canopy overhead, the heads hanging toward us); (staging 2) at head height: from below, the hung heads showed their flat undersides
# (round 2) lower and closer: the big heads fill the upper half, stems below, the field dense enough to hide the ground's end; the heads hang in a
#     wave from the front row back over about a second, each one sagging past its rest and bobbing back; one in the second row (behind the middle
#     of the front row, shown when the front row drops) hangs on, looks left and right, and drops late
# (round 3) three-quarter front and a little under the heads (1.05 m), so the hung heads show their faces and bent necks; the stems bend in an arc;
#     one big hero flower at the front left droops first, with a sad little face; the canopy is lighter, with a warm light band at its foot that
#     parts it from the field; the straggler ends with a slow sigh (a breath in, then a long sag)
F9 = [0.8, 1.05, 1.9]; L9 = [-0.2, 1.45, -2.2]
C9 = cam(0.0, F9, add(F9, [-0.08, 0.0, -0.18]), L9, add(L9, [0.0, -0.03, 0.0]), lens=56)
HERO9 = [0.1, 0, -0.35]
chk('S09', C9['from'], C9['lookAt'], 56, {'front': [0, 1.75, -1.0], 'row1': [0, 1.75, -1.7], 'back': [0, 1.9, -5.9], 'ground': [0, 0, -1.0], 'hero': add(HERO9, [0, 1.85, 0]), 'heroLow': add(HERO9, [0, 1.3, 0.4])})
st.shot('S09', 'grassland', setOpts={'clouds': 0}, grade=GREY, look=OVER, actors=[],
        props=[P('dome9', 'canopySky', pos=[0, 0, 0], opts={**CAN, 'c1': '#A8786A', 'c2': '#CBC5B9', 'overcast': 0.4, 'haze': 0.1, 'ribs': 40, 'rim': 0.75}),
               P('tournesols9', 'sunflowers', pos=[0, 0, -1.0], opts={'cols': 13, 'rows': 12, 'gap': 0.7, 'droopAt': 0.32, 'wave': 0.11, 'hs': 1.45, 'up': -0.2, 'down': 1.0, 'fall': 0.34, 'sag': 0.2, 'arc': 0.7,
                                                                   'straggler': [6, 1], 'lookAt': 0.6, 'dropAt': 1.08, 'sigh': True, 'sighDur': 0.55}),
               P('heros9', 'sunflowers', pos=HERO9, opts={'cols': 1, 'rows': 1, 'seed': 5, 'h': 1.1, 'droopAt': 0.18, 'hs': 1.6, 'up': -0.2, 'down': 1.0, 'fall': 0.42, 'sag': 0.16, 'arc': 0.75, 'face': True})],
        cams=[C9])
st.cue('sfx:slideDownSlow', 'S09', 0.7, 0.35)

# 10: the solar panels were laid off. From the road: panels on little legs queue sideways along the unemployment office with cardboard signs
D10 = st.dur('S10')
# (round 1) the queue shuffles: the panels step up one at a time, front first (0.35 s apart), and each one's sign droops with a sigh once it stops
STEP10 = [0.22, 0.57, 0.92, 1.27]
SIGNS = ['CHERCHE\nLUMIÈRE', "DIX ANS\nD'EXPÉRIENCE", 'SANS\nSOLEIL', "J'AI DES\nENFANTS"]
WALK = [[8.9, 0, z] for z in (-4.5, -3.3, -2.1, -0.9)]
C10 = cam(0.0, [5.0, 1.45, 1.9], [4.9, 1.45, 1.5], [9.0, 1.0, -2.6], [9.0, 1.0, -2.8], lens=52)   # (stills 1) closer: the signs read
chk('S10', C10['from'], C10['lookAt'], 52, {'sign0': [8.66, 0.8, -4.5], 'sign3': [8.66, 0.8, -0.9], 'office': [10.0, 2.85, -4.0], 'door': [10.0, 1.2, -5.8]})
st.shot('S10', 'parisStreet', setOpts={'clouds': 0}, grade=GREY, look=OVER, actors=[],
        props=[P('dome10', 'canopySky', pos=[6, 0, -3], opts=CAN), P('bureau10', 'jobOffice', pos=[10.0, 0, -4.0], ry=-90, opts={'w': 6.5, 'doorX': -1.8}),
               *[P(f'panneau10_{i}', 'solarWalker', pos=p, ry=-90, opts={'walk': True, 'phase': i * 0.37, 'sign': SIGNS[i], 'steps': [[STEP10[i], r(STEP10[i] + 0.34)]], 'droopAt': r(STEP10[i] + 0.42), 'slump': 1.0, 'side': -1 if i % 2 else 1},
                   keys=[k(STEP10[i], to=add(p, [0, 0, -0.6]), dur=0.34, ease='inOut')]) for i, p in enumerate(WALK)],
               *[P(f'petit10_{i}', 'solarWalker', pos=[8.7, 0, r(-0.3 + 0.45 * i)], ry=-90, scale=0.5, opts={'walk': True, 'phase': 0.2 + i * 0.5, 'sign': ' ', 'steps': [[r(1.55 + 0.12 * i), r(1.9 + 0.12 * i)]]},
                   keys=[k(r(1.55 + 0.12 * i), to=[8.7, 0, r(-0.85 + 0.45 * i)], dur=0.35, ease='inOut')]) for i in range(2)]],
        cams=[C10])
for t_ in STEP10: st.cue('sfx:stepSoft', 'S10', t_, 0.22)

# 11: the agency declared the mission a success. The director beams at the podium under MISSION RÉUSSIE over the grey map; applause, flashes
D11 = st.dur('S11'); OK11 = 1.38
SPK = [0.0, 0, -2.45]
C11 = cam(0.0, [-0.6, 1.9, 1.6], [-0.55, 1.88, 1.35], [0.53, 1.8, -2.5], [0.5, 1.82, -2.5], lens=42)   # (round 1) closer: the director bigger, the screen behind his shoulder   # (stills 1) from the front of the room: the director and the screen (the reporters, off screen, are heard and flash)
chk('S11', C11['from'], C11['lookAt'], 42, {'head': [0, 2.0, -2.45], 'headTop': [0, 2.75, -2.45], 'scrL': [0.38, 1.95, -2.6], 'scrR': [1.49, 1.95, -2.8], 'scrTop': [1.49, 2.33, -2.8], 'titleL': [0.14, 3.3, -2.96], 'titleR': [1.46, 2.96, -2.96], 'flashC': [1.2, 1.7, 0.5]})
JOUR = [('journaliste1', [-0.9, 0, 0.4], 165), ('journaliste2', [1.5, 0, 0.3], -160)]
def CLAP(pos, ry, t0, n=5):
    c = off(pos, ry, 0.35, 0.0, 1.35); out = []
    for i in range(n):
        tt = r(t0 + i * 0.16); w = 0.09 if i % 2 == 0 else 0.0
        out.append(k(tt, toon={'reach': {'L': R5(off(c, ry, 0, -0.06 - w, 0.0), 1, 0.04), 'R': R5(off(c, ry, 0, 0.06 + w, 0.0), 1, 0.04)}, 'hands': {'L': 'open', 'R': 'open'}}, toonDur=0.07, keepPose=True))
    return out
# (round 1) he lives before the word (glances at the reporters left and right, a proud puff of the chest, a blink) and beams on « réussie »: a
#     squash, a stretch up with the head swollen and the grin wide, held trembling with the flashes, an overshoot, the settle
SM11 = {'lid': 0.25, 'mouth': 'smile', 'brow': 0.3}
HANDS11 = {'reach': {'L': R5([0.28, 1.13, -2.08], 1, 0.04), 'R': R5([-0.28, 1.13, -2.08], 1, 0.04)}, 'hands': {'L': 'open', 'R': 'open'}}   # both hands on the lectern: the clip's raised hand covered his face
BEAM11 = {**HANDS11, 'sq': [0.88, 1.18, 0.88], 'scl': {'head': [1.14, 1.12, 1.0]}, 'face': {'lid': 0.0, 'mouth': 'bigsmile', 'mouthW': 0.6, 'eye': 0.35, 'brow': 1.0, 'cheeks': 1.0}}
# (round 2) the backdrop's repeated words (cut by the board and the frame edges) are gone; MISSION RÉUSSIE is a big green banner on the wall over
#     the director's head (twice the size of the screen's old header), the screen keeps the grey map under one clean AGENCE SPATIALE line, whole in
#     the frame
st.shot('S11', 'pressRoom', setOpts={'backdrop': ' ', 'fg': 'rgba(0,0,0,0)', 'chairs': False, 'flagOpts': {'colors': ['#6A3FA0', '#F2C94C']}}, grade=GREYIN, actors=[
        act('directeur', SPK, 0, 'podium', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={**HANDS11, 'face': SM11}, toonDur=0.0),
            k(0.2, look=[-1.5, 1.8, 1.0], lookDur=0.15), k(0.55, look=[1.8, 1.8, 1.0], lookDur=0.18), k(0.9, look='camera', lookDur=0.15),
            k(0.95, toon={**HANDS11, 'face': SM11, 'sq': [1.06, 0.96, 1.06]}, toonDur=0.15), k(1.15, toon={**HANDS11, 'face': SM11, 'sq': [1, 1, 1]}, toonDur=0.12),
            *[{**x, 'toon': {**HANDS11, **x['toon']}} for x in blink(0.75, SM11)],
            *[{**x, 'toon': {**HANDS11, **x['toon']}} for x in beat(OK11, BEAM11, hold=0.33, settle={'face': {'lid': 0.15, 'mouth': 'bigsmile', 'brow': 0.6}}, settle_f=6)],
            *[{**x, 'toon': {**HANDS11, **x['toon']}} for x in blink(r(OK11 + 0.65), {'lid': 0.15, 'mouth': 'bigsmile', 'brow': 0.6})]])],
        props=[P('ecran11', 'pressScreen', pos=[0.93, 0, -2.7], ry=-10, opts={'w': 1.12, 'y': 1.95, 'bannerH': 0.24, 'textW': 0.6, 'textX': 0.6, 'tick': False, 'text': 'AGENCE SPATIALE', 'bannerColor': '#2C4A6E'}),
               P('titre11', 'wallTitle', pos=[0.8, 3.13, -2.96], opts={'w': 1.32, 'h': 0.34, 'text': 'MISSION RÉUSSIE', 'bg': '#2E8A4A', 'fg': '#F4F1E8', 'rule': False, 'tick': True, 'emit': 0.35}),
               P('flash11a', 'camFlash', pos=[-0.7, 1.95, 0.4], opts={'w': 0.5, 'at': [r(OK11 + 0.05), r(OK11 + 0.45)]}),
               P('flash11b', 'camFlash', pos=[1.0, 1.85, 0.2], opts={'w': 0.5, 'at': [r(OK11 + 0.25)]}),
               P('flash11c', 'camFlash', pos=[1.2, 1.7, 0.5], opts={'w': 0.45, 'at': [0.35]}),
               # (round 3) the empty lower frame filled: reporters' hands clapping up from the bottom edge and flash pops low in the room on « réussie »
               *[P(f'mains11_{i}', 'clapHands', pos=unproject(C11['to'], C11['lookAt2'], 42, fx, fy, d), ry=r(yaw(C11['to'], C11['lookAt2']) + 180 + dr), rot=[0.0, 0.0, 0.0],
                   opts={'at': r(OK11 - 0.1 + 0.07 * i), 'rate': 3.3 + 0.3 * i, 'ph': 0.3 * i, 'sleeve': ['#2B3346', '#7A2E4E', '#3A3D44'][i]})
                 for i, (fx, fy, d, dr) in enumerate([(0.16, 0.85, 2.0, 12), (0.5, 0.88, 2.3, 0), (0.84, 0.84, 2.1, -12)])],
               P('flash11d', 'camFlash', pos=unproject(C11['to'], C11['lookAt2'], 42, 0.1, 0.64, 3.4), opts={'w': 0.4, 'at': [r(OK11 + 0.12), r(OK11 + 0.55)]}),
               P('flash11e', 'camFlash', pos=unproject(C11['to'], C11['lookAt2'], 42, 0.9, 0.6, 3.6), opts={'w': 0.4, 'at': [r(OK11 + 0.33), r(OK11 + 0.7)]})],
        cams=[C11])
st.cue('sfx:fanfare', 'S11', OK11, 0.3); st.cue('sfx:shutter', 'S11', r(OK11 + 0.05), 0.35); st.cue('sfx:shutter', 'S11', r(OK11 + 0.25), 0.3)

# 12: the country marched with torches. Low in the grey square: marchers hold torches up to the canopy, signs in the other hand
D12 = st.dur('S12')
MARCH = [('manif1', [-1.6, 0, -0.4], 15), ('manif2', [-0.3, 0, -1.3], 5), ('manif3', [1.1, 0, -0.5], -12), ('manif4', [2.3, 0, -1.6], -20), ('manif5', [-2.6, 0, -2.0], 20), ('manif6', [0.6, 0, -2.8], 0)]
C12 = cam(0.0, [0.4, 0.95, 6.4], [0.35, 0.85, 5.9], [0.0, 2.5, -1.2], [0.0, 2.6, -1.2], lens=52)
TORCH = lambda p, ry: off(p, ry, 0.12, -0.2, 2.62)
chk('S12', C12['from'], C12['lookAt'], 52, {**{n: [p[0], 2.0, p[2]] for n, p, ry in MARCH[:4]}, 'torchTop': add(TORCH(MARCH[0][1], 15), [0, 4, 0])})
SIGN12 = {'manif1': 'RENDEZ-NOUS\nLE SOLEIL', 'manif3': 'ON VEUT\nVOIR CLAIR', 'manif5': 'NON AU\nGRIS'}
def PUMP(p, ry, t0):
    tp = TORCH(p, ry); return [k(t0, toon={'reach': {'R': R5(add(tp, [0, -0.12, 0]), 1, 0.04)}}, toonDur=0.12, keepPose=True), k(r(t0 + 0.2), toon={'reach': {'R': R5(tp, 1, 0.04)}}, toonDur=0.12, keepPose=True)]
# (round 2) a gag beat in the hold: manif3's torch sputters (0.45-1.05 s), he frowns at it and shakes it, it comes back, and he holds it higher, up
#     on tiptoe (a stretch), proud, to the end
SPUT = (0.45, 1.05); M1P, M1RY = MARCH[2][1], MARCH[2][2]; TP1 = TORCH(M1P, M1RY)
SHAKE12 = [(0.62, 0.09), (0.7, -0.09), (0.78, 0.09), (0.86, -0.09), (0.94, 0.0)]
UP12 = add(TP1, [0.0, 0.42, 0.04])
def M1K():
    out = [k(0.0, look=add(TP1, [0, 3, 0])), k(0.0, toon={'reach': {'R': R5(TP1, 1, 0.04), 'L': R5(off(M1P, M1RY, 0.3, 0.3, 1.25), 1, 0.04)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.0),
           k(0.5, look=add(TP1, [0, 0.1, 0.3]), lookDur=0.1), k(0.52, toon={'face': {'lid': 0.45, 'mouth': 'grimace', 'brow': -0.8}}, toonDur=0.08, keepPose=True)]
    for t_, dx in SHAKE12: out.append(k(t_, toon={'reach': {'R': R5(off(TP1, M1RY, 0.0, dx, 0.0), 1, 0.04)}}, toonDur=0.06, keepPose=True))
    out += [k(1.1, look=add(UP12, [0, 3, 0]), lookDur=0.15),
            k(1.12, toon={'reach': {'R': R5(add(TP1, [0, -0.08, 0]), 1, 0.04), 'L': R5(off(M1P, M1RY, 0.3, 0.3, 1.25), 1, 0.04)}, 'sq': [1.06, 0.93, 1.06], 'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.4}}, toonDur=0.08),
            k(1.24, toon={'reach': {'R': R5(UP12, 1, 0.04), 'L': R5(off(M1P, M1RY, 0.3, 0.3, 1.25), 1, 0.04)}, 'sq': [0.9, 1.13, 0.9], 'face': {'lid': 0.1, 'mouth': 'bigsmile', 'brow': 0.8}}, toonDur=0.1, toonEase='out'),
            k(1.42, toon={'reach': {'R': R5(add(UP12, [0, -0.04, 0]), 1, 0.04), 'L': R5(off(M1P, M1RY, 0.3, 0.3, 1.25), 1, 0.04)}, 'sq': [0.93, 1.1, 0.93], 'face': {'lid': 0.15, 'mouth': 'smile', 'brow': 0.6}}, toonDur=0.12),
            k(1.8, toon={'reach': {'R': R5(UP12, 1, 0.04), 'L': R5(off(M1P, M1RY, 0.3, 0.3, 1.25), 1, 0.04)}, 'sq': [0.91, 1.12, 0.91]}, toonDur=0.2, keepPose=True)]
    return out
TK12 = [k(t_, to=add(off(TP1, M1RY, 0.0, dx, 0.0), [0, -0.12, 0]), dur=0.06, ease='inOut') for t_, dx in SHAKE12] + [k(1.12, to=add(TP1, [0, -0.2, 0]), dur=0.08), k(1.24, to=add(UP12, [0, -0.12, 0]), dur=0.1, ease='out'), k(1.42, to=add(UP12, [0, -0.16, 0]), dur=0.12), k(1.8, to=add(UP12, [0, -0.12, 0]), dur=0.2)]
st.shot('S12', 'parisStreet', setOpts={'clouds': 0}, grade=GREY, actors=[
        act('manif3', M1P, M1RY, 'stand', 'neutral', keys=M1K()),
        *[act(n, p, ry, 'stand', 'neutral', keys=[k(0.0, look=add(TORCH(p, ry), [0, 3, 0])),
            k(0.0, toon={'reach': {'R': R5(TORCH(p, ry), 1, 0.04), **({'L': R5(off(p, ry, 0.3, 0.3, 1.25), 1, 0.04)} if n in SIGN12 else {})}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'open' if i % 2 else 'line', 'brow': -0.3}}, toonDur=0.0),
            *PUMP(p, ry, r(0.75 + 0.05 * i)), *PUMP(p, ry, r(1.3 + 0.04 * i))]) for i, (n, p, ry) in enumerate(MARCH) if n != 'manif3']],
        props=[P('dome12', 'canopySky', pos=[0, 0, -2], opts=CAN0),
               *[P(f'torche12_{n}', 'handTorch', pos=add(TORCH(p, ry), [0, -0.12, 0]), opts={'beam': 7, 'beamR': 0.7, 'beamOp': 0.6, 'face': math.radians(yaw(TORCH(p, ry), [0.4, 0, 6.4])), **({'sputter': list(SPUT)} if n == 'manif3' else {})},
                   keys=(TK12 if n == 'manif3' else [])) for n, p, ry in MARCH],
               *[P(f'pancarte12_{n}', 'protestSign', pos=off(p, ry, 0.3, 0.3, 0.75), ry=ry, opts={'text': SIGN12[n], 'stick': 0.95}) for n, p, ry in MARCH if n in SIGN12]],
        cams=[C12])
st.cue('sfx:street', 'S12', 0.0, 0.3)

# 13: the gendarmes handcuffed the torches. At a table in the square a gendarme clicks the last cuff shut on a row of torches; marchers, hands up
D13 = st.dur('S13'); CLICK13 = 1.3
TAB = [0.0, 0, -0.5]; TH = 0.75
GD1 = [0.45, 0, -1.3]; GD2 = [-0.95, 0, -1.4]
LAST = [0.48, r(TH + 0.13), -0.5]
C13 = cam(0.0, [0.7, 1.95, 3.1], [0.6, 1.85, 2.0], [0.1, 1.15, -0.9], [0.2, 1.1, -0.8], lens=46, ease='inOut')   # (round 1) a push in on the table: the cuffs read
chk('S13', C13['from'], C13['lookAt'], 46, {'gd1': [GD1[0], 2.0, GD1[2]], 'gd2': [GD2[0], 2.0, GD2[2]], 'torches': [0, TH + 0.06, -0.5], 'last': LAST, 'back': [1.5, 2.0, -3.6]})
st.shot('S13', 'parisStreet', setOpts={'clouds': 0}, grade=GREY, actors=[
        act('gendarme1', GD1, 0, 'stand', 'neutral', keys=[k(0.0, look=LAST),
            k(0.0, toon={'bend': {'spine': [0.35, 0, 0, 1, None]}, 'reach': {'L': R5(add(LAST, [-0.06, 0.06, -0.05]), 1, 0.04), 'R': R5(add(LAST, [0.07, 0.08, 0.02]), 1, 0.04)}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.0),
            k(r(CLICK13 - 0.1), toon={'reach': {'R': R5(add(LAST, [0.02, 0.04, 0.0]), 1, 0.04)}}, toonDur=0.1, keepPose=True),
            k(r(CLICK13 + 0.35), look='camera', lookDur=0.15), *blink(1.95, {'lid': 0.45, 'mouth': 'line', 'brow': -0.2})]),
        act('gendarme2', GD2, 25, 'armsCrossed', 'neutral', keys=[k(0.0, look=[0, 1.0, -0.5]), k(0.0, toon={'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.0),
            k(0.5, look=[0, 0.85, -0.5], lookDur=0.12), k(0.7, look=[0, 1.0, -0.5], lookDur=0.12), *blink(1.0, {'lid': 0.4, 'mouth': 'line', 'brow': -0.3}), k(r(CLICK13 + 0.1), look=LAST, lookDur=0.1),
            k(r(CLICK13 + 0.12), toon={'face': {'lid': 0.3, 'mouth': 'smirk', 'brow': 0.1}, 'sq': [1.04, 0.96, 1.04]}, toonDur=0.08), k(r(CLICK13 + 0.3), toon={'face': {'lid': 0.35, 'mouth': 'smirk', 'brow': 0.0}, 'sq': [1, 1, 1]}, toonDur=0.12)]),
        *[act(n, [x, 0, z], 0, 'surrender', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'wavy', 'brow': 0.4}}, toonDur=0.0),
            k(r(0.3 + 0.25 * j), look=[0, 0.9, -0.5], lookDur=0.15), *blink(r(0.7 + 0.3 * j), {'lid': 0.3, 'mouth': 'wavy', 'brow': 0.4}), k(r(CLICK13 + 0.05 * j), toon={'face': {'lid': 0.0, 'mouth': 'O', 'brow': 0.8}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.06),
            k(r(CLICK13 + 0.25), toon={'face': {'lid': 0.3, 'mouth': 'wavy', 'brow': 0.5}, 'sq': [1, 1, 1]}, toonDur=0.12)]) for j, (n, x, z) in enumerate([('manif1', -0.6, -3.6), ('manif3', 1.6, -3.9), ('manif2', -2.4, -4.2)])]],
        props=[P('dome13', 'canopySky', pos=[0, 0, -2], opts=CAN), KEPI('kepi13a', 'gendarme1'), KEPI('kepi13b', 'gendarme2'),
               P('table13', 'table', pos=TAB, opts={'w': 1.6, 'd': 0.7, 'h': TH, 'color': '#8C949A', 'legs': '#5A6066'}),
               P('torches13', 'cuffedTorches', pos=[0, TH, -0.5], opts={'n': 5, 'gap': 0.24, 'beam': 0.5, 'clickAt': CLICK13, 'upright': True, 'cuffR': 0.065, 'cuffT': 0.018})],
        cams=[C13])
st.cue('sfx:cuff', 'S13', CLICK13, 0.5)

# (round 1) S14: the recoil reads before the whip tilt (the cut moved from 0.72 to 0.86 s): the hull squashes, rocks back on its tracks and settles;
#     soft smoke at the muzzle and a ring of dust at the tracks
# 14: a tank shot a hole in the parasol. The tank raises its gun and fires; the camera tilts up after the shell; a hole bursts open in the canopy (PERCÉ)
D14 = st.dur('S14'); FIRE14 = 0.62; PITCH = 1.05; V14 = 170.0
TANK = [0.0, 0, -4.0]
HOLE14 = add(TANK, mul([0.0, math.sin(PITCH), math.cos(PITCH)], 90 * 0.97))
HOLEAT = r(FIRE14 + 88 / V14, 2)
C14A = cam(0.0, [-6.2, 1.1, 6.2], [-6.0, 1.05, 5.8], [0.0, 1.8, -4.0], [0.0, 1.9, -4.0], lens=44)
C14B = cam(0.86, [-6.0, 1.0, 5.8], [-6.2, 0.95, 6.2], [0.0, 4.0, -2.0], HOLE14, lens=58, ease='out')
chk('S14', C14A['from'], C14A['lookAt'], 44, {'tank': [0, 1.5, -4.0], 'gun': [0, 3.5, -2.8]})
chk('S14b', C14B['to'], C14B['lookAt2'], 58, {'hole': HOLE14, 'holeEdge': add(HOLE14, [6, 0, 0])})
st.shot('S14', 'parisStreet', setOpts={'clouds': 0}, grade=GREY, actors=[],
        props=[P('dome14', 'canopySky', pos=TANK, opts={'r': 90, 'holeAt': HOLEAT, 'az': 180, 'el': r(math.degrees(PITCH), 1), 'holeR': 4}),
               P('char14', 'skyTank', pos=TANK, ry=0, opts={'raiseAt': 0.08, 'pitch': PITCH, 'fireAt': FIRE14, 'shellV': V14, 'shellMax': 86})],
        cams=[C14A, C14B])
st.card('S14', 'PERCÉ', at=r(HOLEAT + 0.06))
st.cue('sfx:slideUp', 'S14', 0.08, 0.3); st.cue('thunder', 'S14', FIRE14, 0.6); st.cue('whoosh', 'S14', r(FIRE14 + 0.05), 0.3, 0.45, 800, 4000); st.cue('sfx:zip', 'S14', HOLEAT, 0.45); st.cue('pop', 'S14', HOLEAT, 0.4)

# ============================== his garden again, under the canopy with its one hole; the lit disc and the dark country round it
HOLEW = add([CH[0], 0, CH[2]], mul(SUNDIR, 90 * 0.97))
def shaft_rot(top, bot):
    Y = unit3(sub(top, bot)); X = unit3(cross3(Y, [0.0, 0.0, 1.0])); Z = cross3(X, Y); return axes_euler(X, Y, Z)
RXS, RYS, RZS = shaft_rot(HOLEW, G)
SHAFT_L = r(math.dist(HOLEW, G), 2)
PATCH = lambda pid, **o: P(pid, 'sunPatch', pos=G, opts={'r': 6.5, 'dark': 0.55, **o})
GDOME = lambda pid: P(pid, 'canopySky', pos=[CH[0], 0, CH[2]], opts=DOME)
# 15: just one. From beside the single beam: from the hole, a tilt down the beam to his garden
D15 = st.dur('S15')
# (staging 2) from behind the house, high, looking along the beam: the slanted shaft stands upright in the frame, from the hole at the top down to his
#     lawn at the bottom (seen from its side, the shaft spread across the whole 9:16 frame and washed it out)
SH15 = unit3([SUNDIR[0], 0.0, SUNDIR[2]])
F15 = [r(G[0] - SH15[0] * 24), 13.0, r(G[2] - SH15[2] * 24)]
L15, LENS15, W15 = fit(F15, {'hole': HOLEW, 'holeTop': add(HOLEW, [0, 7, 0]), 'garden': G, 'mec': HEAD}, margin=0.08, top=0.1, bottom=0.74)
C15 = cam(0.0, F15, add(F15, mul(SH15, 1.2)), L15, L15, lens=LENS15)
CHECKS.append(f"S15 fit lens {LENS15} {W15}")
chk('S15', F15, L15, LENS15, {'hole': HOLEW, 'garden': G, 'mec': HEAD, 'house': [0, 3, -6.6]})
st.shot('S15', 'pavillon', setOpts=GARDEN, actors=[act('mec', SEAT, RY, 'sit', 'unimpressed', keys=[k(0.0, look=HOLEW), k(0.0, toon={**LOUNGE, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0)])],
        props=[P('nuages15', 'noClouds'), GDOME('dome15'), PATCH('disque15'), CHAIR('chaise15'),
               P('rayon15', 'lightShaft', pos=HOLEW, rot=[RXS, 0, RZS], ry=RYS, opts={'r': 5.0, 'len': SHAFT_L, 'op': 0.2, 'onAt': 0.02})],
        cams=[C15])
st.cue('sfx:choir', 'S15', 0.02, 0.35)

# 16: above his garden. From high above: the lit disc of his lawn, his deckchair in it, the country round it dark
D16 = st.dur('S16')
# (round 2) a push in from 31 m to 14 m (he grows to about 5 % of the frame), and the squirm is a big full-body wriggle seen from above: the body
#     bends side to side and tips, the free arm flaps out wide
C16 = cam(0.0, [G[0] + 0.4, 31.0, G[2] + 5.5], [G[0] + 0.25, 14.0, G[2] + 2.4], G, add(G, [-0.3, 0, -0.4]), lens=50, ease='inOut')
chk('S16', C16['from'], C16['lookAt'], 50, {'chair': CH, 'patchE': add(G, [6.5, 0, 0]), 'patchW': add(G, [-6.5, 0, 0]), 'patchN': add(G, [0, 0, -6.5]), 'patchS': add(G, [0, 0, 6.5])})
# (round 1) the tiny man lives: he squirms in the deckchair (a squash, a shift to one side and back) and fans his face with his free hand
FAN = lambda i: R5(add(VISOR[:3], [0.12 * (1 if i % 2 else -1), -0.12, 0.05]), 1, 0.05)
def WR16(i):
    sg = 1 if i % 2 else -1
    return {'bend': {'spine': [-0.3, 0.5 * sg, 0.25 * sg, 1, None], 'neck': [0.1, -0.35 * sg, 0, 1, None]}, 'lay': [0.0, 0.16 * sg], 'sq': [1.08, 0.92, 1.08] if i % 2 else [0.94, 1.07, 0.94],
            'reach': {'R': VISOR, 'L': R5(off(HEAD, RY, 0.3, -0.85 if i % 2 else -0.2, -0.15 if i % 2 else 0.15), 1, 0.05)}, 'hands': {'L': 'open', 'R': 'open'}, 'face': {**SQUINT, 'mouth': 'grimace' if i % 2 else 'clench'}}
HERO16 = [k(0.0, look=HOLEW), k(0.0, toon={**LOUNGE, 'reach': {'R': VISOR}, 'face': SQUINT}, toonDur=0.0),
          k(0.15, toon={**LOUNGE, 'reach': {'R': VISOR}, 'face': SQUINT, 'sq': [1.1, 0.9, 1.1]}, toonDur=0.08),
          *[k(r(0.25 + 0.12 * i), toon=WR16(i), toonDur=0.09, toonEase='inOut') for i in range(8)],
          k(1.25, toon={**LOUNGE, 'reach': {'R': VISOR}, 'face': SQUINT, 'sq': [1.05, 0.95, 1.05]}, toonDur=0.1), k(1.25, look=add(HOLEW, [6, 0, 0]), lookDur=0.2)]
st.shot('S16', 'pavillon', setOpts=GARDEN, actors=[act('mec', SEAT, RY, 'sit', 'unimpressed', keys=HERO16)],
        props=[P('nuages16', 'noClouds'), PATCH('disque16', dark=0), P('ombre16', 'sunPatch', pos=[G[0], 6.2, G[2]], opts={'r': 6.5, 'lawn': False, 'dark': 0.84, 'darkColor': '#4C545E', 'y': 0.0, 'rimOp': 0.0}), CHAIR('chaise16')],
        cams=[C16])

# 17: right in his eyes. The reverse first (the hole and its sun beyond the street, over his shoulder), then his squint: the framing of shot one
D17 = st.dur('S17'); T17 = 0.6
C17A = cam(0.0, C1B['from'], C1B['to'], L1B, L1B, lens=LENS1B)
C17B = cam(T17, C1A['from'], C1A['to'], C1A['lookAt'], C1A['lookAt2'], lens=36)
chk('S17', C17A['from'], C17A['lookAt'], LENS1B, {'hole': add(HEAD, mul(SUNDIR, 87)), 'head': HEAD})
# (round 1) the escalation of shot one: the visor hand slams up from his lap with a smear, the whole head squashes down and the face crumples
#     (lids shut tight, the brow on the eyes, the mouth clenched), held trembling, then a small overshoot and the squint settles; the glare pulled back
CRUMPLE = {'lid': 0.9, 'low': 0.5, 'brow': -1.0, 'mouth': 'clench', 'mouthW': 0.3, 'tremble': 1, 'cheeks': 0.6}
LAP = ['face', -0.1, -1.2, 0.35, 1, 0.12, [1.0, -0.3, 0.2]]
def LV(pt, w=1): return {**LOUNGE, 'touch': {'R': REST_R, 'L': pt[:4] + [w, pt[5], pt[6]]}, 'hands': {'L': 'open', 'R': 'open'}}
HERO17 = [k(0.0, look=SUNP), k(0.0, toon={**LV(LAP), 'face': {**SQUINT, 'lid': 0.45}}, toonDur=0.0),
          k(r(T17 - 0.02), look=LOOK1, lookDur=0.04),
          k(r(T17 + 0.02), toon={**LV(LAP), 'face': {**SQUINT, 'lid': 0.3, 'brow': 0.2}, 'sq': [0.97, 1.04, 0.97], 'scl': {'head': [0.95, 1.08, 1]}}, toonDur=0.05),
          k(r(T17 + 0.1), toon={**LOUNGEV(0.06), 'face': CRUMPLE, 'sq': [1.08, 0.9, 1.08], 'scl': {'head': [1.2, 0.76, 1.08]}}, toonDur=0.06, toonEase='out'),
          k(r(T17 + 0.24), toon={**LOUNGEV(0.05), 'face': CRUMPLE, 'sq': [1.06, 0.92, 1.06], 'scl': {'head': [1.16, 0.8, 1.06]}}, toonDur=0.07),
          k(r(T17 + 0.36), toon={**LOUNGEV(0.06), 'face': CRUMPLE, 'sq': [1.08, 0.9, 1.08], 'scl': {'head': [1.2, 0.77, 1.08]}}, toonDur=0.07),
          k(r(T17 + 0.48), toon={**LOUNGEV(-0.02), 'face': {**CRUMPLE, 'tremble': 0.4}, 'sq': [0.97, 1.04, 0.97], 'scl': {'head': [0.94, 1.07, 1]}}, toonDur=0.08, toonEase='in'),
          k(r(T17 + 0.6), toon={**LOUNGEV(), 'face': {**SQUINT, 'lid': 0.8, 'low': 0.5}, 'sq': [1, 1, 1], 'scl': {'head': [1.05, 0.95, 1.02]}}, toonDur=0.1)]
st.shot('S17', 'pavillon', setOpts=GARDEN, actors=[act('mec', SEAT, RY, 'sit', 'unimpressed', keys=HERO17)],
        props=[P('nuages17', 'noClouds'), GDOME('dome17'), PATCH('disque17'), CHAIR('chaise17'), P('eclat17', 'lensGlare', pos=GLARE1, opts={'s': 1.3, 'op': 0.4}, keys=[k(0.0, visible=False), k(T17, visible=True)])],
        cams=[C17A, C17B])
st.cue('sfx:static', 'S17', T17, 0.15)

# 18: the whole country picnics at his place. Craning up over the packed disc: the marchers, the gendarmes, the scientists on blankets, the director
#     sunbathing on the car roof, two neighbours squeezed against his deckchair
D18 = st.dur('S18')
# (round 2) he is the centre: the camera comes down out of the wide (the packed lawn, the director on the car roof) onto him, front and centre in his
#     striped deckchair just above the caption band, a clear strip of lawn in front of him and the crowd packed behind and beside him; two
#     neighbours on folding chairs lean in and squeeze his head from both sides (a side squash, one eye pushed shut), twice
RY18 = 22
HEAD18 = off(CH, RY18, -0.18, 0.0, 1.3)
# (round 3) a gap in the rows straight behind him (the line from the end camera through his head), so his head ends against the house wall
PICROWS = [(0.15, [-1.45, -2.35, 1.45]), (-0.9, [-2.3, -1.45, 0.75, 1.6]), (-1.8, [-2.0, 0.45, 1.35]), (-2.6, [-2.3, 0.2])]
PICWHO = [('journaliste1', 20, 'sitFloor'), ('manif6', -15, 'sitFloorWave'), ('gendarme2', -20, 'sitFloorSip'),
          ('manif1', 15, 'sitFloorEat'), ('savant2', -10, 'sitFloorSip'), ('manif4', 5, 'sitFloorSip'), ('gendarme1', -25, 'sitFloorEat'),
          ('savant1', 10, 'sitFloor'), ('manif5', -5, 'sitFloorEat'), ('savant3', 25, 'sitFloorWave'), ('manif2', 10, 'sitFloorEat'), ('manif3', -15, 'sitFloor')]
PICPOS = [[r(CH[0] + dx), 0, r(CH[2] + dz)] for dz, xs in PICROWS for dx in xs]
NB18 = [('journaliste2', off(CH, RY18, -0.3, -0.6, -0.12), 1), ('voisine', off(CH, RY18, -0.3, 0.55, -0.12), -1)]   # (round 3) closer: the cheeks touch his head
PIC = [(n, PICPOS[i], ry, clip) for i, (n, ry, clip) in enumerate(PICWHO)]
BCOL = ['#C23A2E', '#2E6FB5', '#2F8A4A', '#E0A020', '#7A2E4E', '#C23A2E', '#2E6FB5']
BLANK = [[r(CH[0] + (max(xs) + min(xs)) / 2), r(CH[2] + dz + 0.1), 0.0, r(max(xs) - min(xs) + 1.0), 0.95, BCOL[i]] for i, (dz, xs) in enumerate(PICROWS[1:])]
CAR = [1.6, 0, -2.9]
# the second row passes a baguette (manif1 to savant2), the heads turn in a ripple
PA18, PB18 = PICPOS[3], PICPOS[4]
BA = [r(PA18[0] + 0.32), 0.72, r(PA18[2] + 0.2)]; BB = [r(PB18[0] - 0.3), 0.72, r(PB18[2] + 0.2)]; BM = [r((BA[0] + BB[0]) / 2), 0.82, r(BA[2] + 0.05)]
PASS18 = {'manif1': [k(0.15, toon={'reach': {'L': R5(BA, 1, 0.08)}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.15),
                     k(0.6, toon={'reach': {'L': R5(BM, 1, 0.08)}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.25), k(1.0, toon={'reach': {'L': R5(BM, 0.0, 0.08)}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.3), k(0.55, look=BB, lookDur=0.12)],
          'savant2': [k(0.6, toon={'reach': {'R': R5(BM, 1, 0.08)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.2, 'mouth': 'O'}}, toonDur=0.25), k(0.6, look=BM, lookDur=0.12),
                      k(1.05, toon={'reach': {'R': R5(add(BB, [0.05, 0.15, 0]), 1, 0.08)}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.3)]}
F18A = [0.8, 9.5, 10.5]
L18A, LENS18A, W18A = fit(F18A, {'mec': HEAD18, 'car': [3.6, 2.4, -2.9], 'carL': [-0.4, 0.0, -2.0], 'row0': [CH[0] - 2.35, 1.0, CH[2] + 0.15], 'front': off(CH, RY18, 1.0, 0, 0)}, margin=0.04, top=0.12, bottom=0.76, lenses=range(30, 71))
# (round 3) the wide (the packed lawn, the director on the car roof) is only the first beat: from 0.3 s the camera cranes down onto him and ends
#     tight, low and square to him (a little under his head), his head about a sixth of the frame height against the house wall, the two
#     neighbours' heads pressed to his from both sides; then the squash comes in two beats (from screen left, then from screen right) and holds
F18B = off(CH, RY18, 3.0, 0.0, 1.05)
LENS18B = 44
L18B = add(HEAD18, [0.0, -0.22, 0.0])
CR18 = 0.3; GL18 = 0.62
CHECKS.append(f"S18 fit A {LENS18A} {W18A} | B {LENS18B}")
C18 = cam(0.0, F18A, add(F18A, [-0.3, -0.8, -0.6]), L18A, L18A, lens=LENS18A)
C18B = glide([cam(CR18, F18B, add(F18B, [0.0, 0.0, 0.0]), L18B, L18B, lens=LENS18B)], GL18)
chk('S18', F18A, L18A, LENS18A, {'mec': HEAD18, **{n: [p[0], 1.2, p[2]] for n, p, ry, c in PIC}, 'dir': [CAR[0] - 0.2, 2.5, CAR[2]]})
chk('S18b', F18B, L18B, LENS18B, {'mec': HEAD18, 'headTop': add(HEAD18, [0, 0.3, 0]), 'knee': off(CH, RY18, 0.45, 0, 0.3), 'chairFront': off(CH, RY18, 0.75, 0, 0.0), **{n: add(p, [0, 1.3, 0]) for n, p, sg in NB18}})
# beat 1 (B1): pushed from screen left (his right): the head squeezed narrow and tipped to screen right, the near eye shut; beat 2 (B2): pushed
#     from screen right as well: the head squeezed tall and thin between the two cheeks, upright, the eye still shut, held trembling to the end
B1_18, B2_18 = 0.98, 1.3
def SQ18(sx, sy, tilt, sq=(1, 1, 1), mouth='wavy'):
    return {**LOUNGE, 'bend': {'spine': [-0.42, 0, 0, 1, None], 'neck': [0.12, 0, tilt, 1, None]}, 'face': {**SQUINT, 'lidR': 1.0, 'lid': 0.55, 'mouth': mouth, 'mouthTilt': 8},
            'scl': {'head': [sx, sy, 1.0]}, 'sq': list(sq)}
HERO18 = [k(0.0, look='camera'), k(0.0, toon={**LOUNGE, 'face': {**SQUINT, 'mouth': 'line'}}, toonDur=0.0),
          k(r(B1_18 - 0.07), toon={**LOUNGE, 'face': {**SQUINT, 'lid': 0.3, 'mouth': 'line'}}, toonDur=0.06),
          k(B1_18, toon=SQ18(0.72, 1.12, -0.28, (0.96, 1.03, 1.0)), toonDur=0.06, toonEase='out'),
          k(r(B1_18 + 0.12), toon=SQ18(0.78, 1.09, -0.23), toonDur=0.1),
          k(B2_18, toon=SQ18(0.58, 1.24, 0.0, (0.95, 1.05, 1.0)), toonDur=0.06, toonEase='out'),
          k(r(B2_18 + 0.1), toon=SQ18(0.63, 1.2, 0.02, mouth='grimace'), toonDur=0.08),
          *[k(r(B2_18 + 0.2 + 0.1 * j), toon=SQ18(0.61 + 0.03 * (j % 2), 1.21 - 0.02 * (j % 2), 0.01, mouth='grimace'), toonDur=0.05) for j in range(5)]]
def NBK(sg, t1):
    lean = lambda a, face=None: {'bend': {'spine': [0.1, a * sg, 0, 1, None], 'neck': [0.0, 0.5 * a * sg, 0, 1, None]}, 'face': face or {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}}
    PRESS = {'lid': 0.75, 'mouth': 'bigsmile', 'brow': 0.6, 'cheeks': 1.0}
    return [k(0.0, look='camera'), k(0.0, toon=lean(0.06), toonDur=0.0), k(r(t1 - 0.22), look=[HEAD18[0], 1.4, HEAD18[2]], lookDur=0.12),
            k(r(t1 - 0.08), toon=lean(0.02), toonDur=0.08), k(t1, toon=lean(0.3, PRESS), toonDur=0.06, toonEase='out'), k(r(t1 + 0.1), toon=lean(0.27, PRESS), toonDur=0.08),
            *[k(r(t1 + 0.2 + 0.1 * j), toon=lean(0.27 + 0.025 * (j % 2), PRESS), toonDur=0.05) for j in range(int((D18 - t1 - 0.2) / 0.1))]]
st.shot('S18', 'pavillon', setOpts={**GARDEN, 'mailbox': False}, actors=[
        act('mec', SEAT, RY18, 'sit', 'unimpressed', keys=HERO18),
        *[act(n, add(p, [0, 0.0, 0]), r(RY18 - 38 * sg), 'sit', 'neutral', keys=NBK(sg, B1_18 if sg < 0 else B2_18)) for n, p, sg in NB18],
        *[act(n, p, ry, 'sitFloor' if n in ('manif1', 'savant2') else clip, 'neutral', keys=[k(0.0, look='camera' if i % 3 == 0 else HOLEW), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'smile' if i % 2 else 'line'}}, toonDur=0.0),
            k(r(0.25 + 0.11 * i), look=(HOLEW if i % 3 == 0 else [CH[0], 1.0, CH[2]]), lookDur=0.15), k(r(1.0 + 0.07 * i), look=('camera' if i % 2 else [CAR[0], 2.2, CAR[2]]), lookDur=0.15),
            *blink(r(0.5 + 0.13 * (i % 7)), {'lid': 0.5, 'mouth': 'smile' if i % 2 else 'line'}), *PASS18.get(n, [])]) for i, (n, p, ry, clip) in enumerate(PIC)],
        act('directeur', [CAR[0] - 0.2, 2.06, CAR[2]], 90, 'lieRelax', 'neutral', keys=[k(0.0, look=HOLEW), k(0.0, toon={'face': {'lid': 0.8, 'mouth': 'smile'}}, toonDur=0.0)])],
        props=[P('nuages18', 'noClouds'), GDOME('dome18'), PATCH('disque18'), P('chaise18', 'deckChair', pos=CH, ry=RY18), KEPI('kepi18', 'gendarme1'), KEPI('kepi18b', 'gendarme2'),
               *[P(f'glaciere18_{n}', 'cooler', pos=[p[0], 0, p[2]], ry=RY18, opts={'color': '#2E7FC0' if sg > 0 else '#C23A2E'}) for n, p, sg in NB18],
               P('pique18', 'picnicSpread', pos=[0, 0, 0], opts={'blankets': BLANK}),
               P('baguette18', 'baguette', pos=BA, ry=20, keys=[k(0.6, to=BM, dur=0.25, ease='inOut'), k(1.05, to=add(BB, [0.05, 0.15, 0]), dur=0.3, ease='inOut')]),
               P('voiture18', 'car', pos=CAR, ry=0, opts={'color': '#3E7AB8'}), P('serviette18', 'beachTowel', pos=[CAR[0] - 0.25, 2.06, CAR[2]], ry=90, opts={'w': 0.9, 'd': 1.7, 'hang': 0.3})],
        cams=[C18, C18B])
st.cue('sfx:street', 'S18', 0.0, 0.3)

# 19: he had a parasol in the garage. Beside his deckchair, the garage open behind him, he holds a small dusty parasol; it opens with a puff of dust; a
#     look to us
# (round 1) re-staged as a medium close: the open garage right behind him (its shelf of pots and boxes lit at the back), his deckchair beside him.
#     Without looking, his right arm stretches back into the garage and rummages; a tug (anticipation), a yank: out comes a small faded child's
#     parasol, which he raises over his shoulder; it pops open in a soft cloud of beige dust that hangs; he looks up at it, back at us, snaps back to
#     it (double take, eyes out a little), then turns to us, one blink, and holds. Two picnickers eat in the background, nobody in front of him
D19 = st.dur('S19'); YANK19 = 0.62; OPEN19 = 1.05
ME19 = [-1.05, 0, -1.15]; RY19 = 6
# (round 3) a little wider and turned: the garage moved right behind him (his arm still reaches into it), so the garden shows on the left under the
#     parasol with two small picnickers on coolers and the edge of his striped deckchair; the grip raised 0.12 m (the crook and the hand sat on the
#     top line of the caption band)
SHED = [-0.35, 0, -2.15]
CH19 = [-2.0, 0, -0.75]
IN19 = [-1.15, 0.95, -3.0]                                      # the grip, deep in the garage
UPG = [-1.47, 1.72, -0.8]                                      # the grip once raised: in front of his right shoulder, the canopy over it
F19 = [-1.55, 1.7, 2.3]
L19, LENS19, W19 = [-1.25, 1.62, -2.0], 46, {}
C19 = cam(0.0, F19, add(F19, [0.05, 0.0, -0.25]), L19, add(L19, [0.0, 0.03, 0.0]), lens=LENS19)
CHECKS.append(f"S19 fit lens {LENS19} {W19}")
chk('S19', C19['from'], C19['lookAt'], LENS19, {'head': [ME19[0], 2.05, ME19[2]], 'grip': UPG, 'crook': add(UPG, [0, -0.2, 0]), 'parTop': add(UPG, [0.28, 1.1, 0]), 'parL': add(UPG, [-0.18, 0.88, 0]), 'inside': IN19, 'shelf': add(SHED, [0, 1.2, -1.6]), 'chairTop': add(CH19, [0.2, 0.95, 0.1]), 'pic1': [-2.25, 1.0, -3.55], 'pic2': [-1.8, 1.0, -3.95]})
PIC19 = [('manif4', [-2.25, 0, -3.55], 30, 'sitFloorEat'), ('gendarme1', [-1.8, 0, -3.95], 15, 'sitFloorSip')]
DEAD19 = {'lid': 0.4, 'mouth': 'line', 'brow': -0.1}
def G19(p, w=1): return R5(add(p, [0.0, 0.0, 0.0]), w, 0.05)
PATH19 = [(0.0, IN19), (0.18, add(IN19, [0.08, 0.05, 0.05])), (0.32, add(IN19, [-0.06, -0.03, 0.0])), (0.46, add(IN19, [0.04, 0.04, 0.06])),
          (r(YANK19 - 0.08), add(IN19, [0.0, 0.0, -0.12])), (r(YANK19 + 0.16), add(UPG, [0.05, 0.12, 0.1])), (r(YANK19 + 0.3), UPG)]
HERO19 = [k(0.0, look='camera'), k(0.0, toon={'reach': {'R': G19(IN19)}, 'hands': {'R': 'grip'}, 'hose': 0.12, 'face': {**DEAD19, 'gx': -0.6}}, toonDur=0.0)]
for i in range(1, len(PATH19)):
    t_, p_ = PATH19[i]; d_ = r(PATH19[i][0] - PATH19[i - 1][0])
    extra = {}
    if t_ == r(YANK19 - 0.08): extra = {'sq': [1.06, 0.93, 1.06], 'face': {'lid': 0.55, 'mouth': 'clench', 'brow': -0.4, 'gx': -0.6}}
    elif t_ == r(YANK19 + 0.16): extra = {'sq': [0.95, 1.07, 0.95], 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.1}}
    elif t_ == r(YANK19 + 0.3): extra = {'sq': [1, 1, 1], 'face': DEAD19}
    else: extra = {'face': {**DEAD19, 'gx': -0.6, 'mouth': 'wavy' if i % 2 else 'line'}}
    HERO19.append(k(t_, toon={'reach': {'R': G19(p_)}, 'hands': {'R': 'grip'}, 'hose': 0.12, **extra}, toonDur=d_ if t_ != r(YANK19 + 0.16) else 0.16, toonEase='out' if t_ == r(YANK19 + 0.16) else 'inOut'))
HOLD19 = {'reach': {'R': G19(UPG)}, 'hands': {'R': 'grip'}}
PTOP = add(UPG, [0.1, 1.15, 1.6])                              # up and toward us: the head tips back a little, the face stays to the lens
DT19 = r(OPEN19 + 0.12)
HERO19 += [k(r(OPEN19 - 0.06), toon={**HOLD19, 'face': {**DEAD19, 'lid': 0.3}}, toonDur=0.06, keepPose=True),
           k(OPEN19, toon={**HOLD19, 'sq': [1.04, 0.95, 1.04], 'face': {'lid': 0.7, 'mouth': 'grimace', 'brow': -0.3}}, toonDur=0.04),
           k(r(OPEN19 + 0.12), toon={**HOLD19, 'sq': [1, 1, 1], 'face': {'lid': 0.35, 'mouth': 'line', 'brow': 0.0}}, toonDur=0.1),
           *doubleTake(DT19, PTOP, keep=HOLD19, back='camera', pop=0.5, blank=0.22, hold=0.3),
           k(r(DT19 + 0.95), look='camera', lookDur=0.18), k(r(DT19 + 0.95), toon={**HOLD19, 'face': DEAD19}, toonDur=0.15),
           *[{**x, 'toon': {**HOLD19, **x['toon']}} for x in blink(r(DT19 + 1.2), DEAD19)]]
PAR_KEYS = [k(t_, to=p_, dur=r(PATH19[i][0] - PATH19[i - 1][0]) if i else 0.0, ease='out' if t_ == r(YANK19 + 0.16) else 'inOut') for i, (t_, p_) in enumerate(PATH19) if i]
st.shot('S19', 'pavillon', setOpts={**GARDEN, 'mailbox': False}, actors=[
        act('mec', ME19, RY19, 'stand', 'unimpressed', keys=HERO19),
        *[act(n, p, ry, clip, 'neutral', keys=[k(0.0, look=[ME19[0], 1.9, ME19[2]] if i else HOLEW), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'smile' if i % 2 else 'line'}}, toonDur=0.0),
            k(r(OPEN19 + 0.25 + 0.15 * i), look=PTOP, lookDur=0.2), *blink(r(0.5 + 0.7 * i), {'lid': 0.5, 'mouth': 'smile' if i % 2 else 'line'})]) for i, (n, p, ry, clip) in enumerate(PIC19)]],
        props=[P('nuages19', 'noClouds'), GDOME('dome19'), PATCH('disque19'), P('chaise19', 'deckChair', pos=CH19, ry=25), KEPI('kepi19', 'gendarme1'),
               P('pique19', 'picnicSpread', pos=[0, 0, 0], opts={'seed': 37, 'blankets': [[p[0], r(p[2] + 0.1), 0.2, 1.3, 1.1, BCOL[i]] for i, (n, p, ry, c) in enumerate(PIC19)]}),
               P('garage19', 'garageOpen', pos=SHED, ry=0, opts={'w': 2.3, 'd': 1.9, 'h': 2.4, 'color': '#E3D8C2'}), P('etagere19', 'garageShelf', pos=add(SHED, [0, 0, -1.7]), ry=0, opts={'w': 1.8}),
               P('parasol19', 'kidParasol', pos=IN19, rot=[-0.5, 0, 0.3], opts={'r': 0.42, 'len': 1.0, 'openAt': OPEN19}, keys=[*PAR_KEYS, k(r(YANK19 - 0.08), rotTo=[-0.06, 0.0, -0.26], dur=0.3, ease='out')])],
        cams=[C19])
st.cue('whoosh', 'S19', r(YANK19 - 0.02), 0.2, 0.3, 500, 2000); st.cue('sfx:poof', 'S19', r(OPEN19 + 0.02), 0.4); st.cue('sfx:boing', 'S19', r(DT19 + 0.16 + 0.22), 0.25)

print('\n'.join(CHECKS))

MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
st.write("Le rayon", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    **{f'savant{i + 1}': {'preset': 'savant', 'seed': 990 + i, 'hairColor': ['#DADADA', '#3A2A20', '#8A5A2A', '#1B1B1E', '#C9A050', '#6A6A6A', '#DADADA'][i],
                          'hair': ['afro', 'crew', 'slick', 'receding', 'afro', 'crew', 'receding'][i], 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX} for i in range(7)},
    'directeur': {'preset': 'savant', 'seed': 999, 'hair': 'receding', 'hairColor': '#BDBDBD', 'facial': 'mustache', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.12}, 'toon': EX},
    'journaliste1': {'preset': 'madame', 'seed': 1001, 'suit': '#7A2E4E', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'journaliste2': {'preset': 'worker', 'seed': 1002, 'hat': 'none', 'suit': '#3A3D44', 'pants': '#22324A', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'manif1': {'preset': 'worker', 'seed': 1003, 'hat': 'none', 'suit': '#1F4E8C', 'pants': '#22324A', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'manif2': {'preset': 'madame', 'seed': 1004, 'suit': '#2E7D4F', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'manif3': {'preset': 'fermier', 'seed': 1005, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'manif4': {'preset': 'mamie', 'seed': 1006, 'suit': '#7A2E4E', 'lapel': '#5A1E38', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'manif5': {'preset': 'sportif', 'seed': 1007, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'manif6': {'preset': 'lyceen', 'seed': 1008, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'voisine': {'preset': 'madame', 'seed': 1009, 'suit': '#E0A020', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'gendarme1': {**GEND, 'seed': 1010}, 'gendarme2': {**GEND, 'seed': 1011, 'facial': 'mustache'},
})
