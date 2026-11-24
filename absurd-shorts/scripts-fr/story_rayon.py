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
shots get a per-shot grade and the canopy dome for a sky; no transparent key props; no English, no brands, no real organisation or flag."""
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

for g_ in [('S01', 0.4, 'mec', 'squint'), ('S04', 0.5, 'mec', 'rockets'), ('S17', 0.75, 'mec', 'squint2'), ('S19', 1.2, 'mec', 'parasol')]:
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
SQUINT = {'lid': 0.85, 'brow': -0.7, 'mouth': 'grimace'}
VISOR = R5(off(HEAD, RY, 0.24, 0.05, 0.1), 1, 0.05)           # the right hand flat over his brow
GARDEN = {}
def CHAIR(pid): return P(pid, 'deckChair', pos=CH, ry=RY)

# 1: the hook. Close from the sun's side: in his deckchair he squints into the light, a hand for a visor, a warm glare at the top of the frame; on
#    « soleil » the reverse over his shoulder: the blazing cartoon sun over the street
D1 = st.dur('S01'); T1 = 0.85
C1A = cam(0.0, off(CH, RY, 3.0, 0.45, 1.35), off(CH, RY, 2.75, 0.4, 1.36), off(CH, RY, -0.15, 0.0, 1.12), off(CH, RY, -0.15, 0.0, 1.14), lens=36)   # (stills 1) further: his whole squint and the hand
F1B = off(CH, RY, -3.2, -0.5, 1.0)
L1B, LENS1B, W1B = fit(F1B, {'head': HEAD, 'headTop': add(HEAD, [0, 0.3, 0]), 'sun': SUNP, 'sunTop': add(SUNP, [0, 3.2, 0]), 'chair': off(CH, RY, 0.2, 0, 0.6)}, margin=0.1, top=0.12, bottom=0.78)
C1B = cam(T1, F1B, add(F1B, mul(fwd(RY), 0.12)), L1B, L1B, lens=LENS1B)
CHECKS.append(f"S01b fit lens {LENS1B} {W1B}")
GLARE1 = unproject(C1A['from'], C1A['lookAt'], 36, 0.86, 0.06, 1.6)
chk('S01', C1A['from'], C1A['lookAt'], 36, {'head': HEAD, 'visor': VISOR[:3], 'glare': GLARE1, 'chairFoot': add(CH, [0, 0.1, 0])})
chk('S01b', C1B['from'], C1B['lookAt'], 50, {'head': HEAD, 'sun': SUNP, 'shoulder': off(CH, RY, -0.1, -0.2, 1.2)})
HERO1 = [k(0.0, look=SUNP), k(0.0, toon={**LOUNGE, 'reach': {'R': VISOR}, 'face': SQUINT}, toonDur=0.0),
         k(0.3, toon={**LOUNGE, 'reach': {'R': VISOR}, 'face': {**SQUINT, 'lid': 0.95}, 'sq': [1.02, 0.97, 1.02]}, toonDur=0.12),
         k(0.5, toon={**LOUNGE, 'reach': {'R': R5(add(VISOR[:3], [0, 0.03, 0]), 1, 0.05)}, 'face': SQUINT, 'sq': [1, 1, 1]}, toonDur=0.14),
         k(1.25, toon={**LOUNGE, 'reach': {'R': R5(add(VISOR[:3], [0.02, -0.02, 0]), 1, 0.05)}, 'face': {**SQUINT, 'lid': 0.92}}, toonDur=0.2)]
st.shot('S01', 'pavillon', setOpts=GARDEN, actors=[act('mec', SEAT, RY, 'sit', 'unimpressed', keys=HERO1)],
        props=[CHAIR('chaise1'), P('soleil1', 'sun', pos=SUNP, opts={'r': 2.6}, keys=[k(0.0, scale=1.0, dur=0.0), k(T1, scale=1.1, dur=0.3, ease='inOut')]),
               P('eclat1', 'lensGlare', pos=GLARE1, opts={'s': 2.4, 'op': 0.75})],
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
st.shot('S02', 'office', setOpts=CTRL, actors=[
        act(sid, pos, 180, 'sitWrite' if i % 3 == 1 else 'sit', 'neutral', keys=[k(0.0, look=[pos[0], 1.3, r(pos[2] - 0.9)]),
            *([k(0.9, look='camera', lookDur=0.15), *blink(1.4)] if sid == 'savant3' else [])]) for i, (sid, pos) in enumerate(SAV)],
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
C3B = cam(TAP3, [0.12, 1.62, 0.95], [0.1, 1.6, 0.75], [0.02, 1.55, -1.2], [0.02, 1.55, -1.2], lens=40, shake=0.02)
chk('S03', C3A['from'], C3A['lookAt'], 50, {'boardL': [-1.2, 1.55, -1.17], 'boardR': [1.2, 1.55, -1.17], 'dirHead': [DIR3[0], 2.0, DIR3[2]], 'boardTop': [0, 2.25, -1.17]})
chk('S03b', C3B['from'], C3B['lookAt'], 40, {'para': PARA, 'paraTop': [0, 1.85, -1.16], 'paraBot': [0, 1.25, -1.16]})
TAPP = lambda dz: R5([0.06, 1.6, r(-1.15 + dz)], 1, 0.05)
st.shot('S03', 'office', setOpts=CTRL, actors=[
        act('directeur', DIR3, RYD, 'stand', 'neutral', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'R': TAPP(0.25)}, 'hands': {'R': 'point'}, 'face': {'lid': 0.3, 'mouth': 'smirk', 'brow': 0.3}}, toonDur=0.0),
            k(0.5, look=PARA, lookDur=0.15), k(r(TAP3 - 0.12), toon={'reach': {'R': TAPP(0.12)}, 'hands': {'R': 'point'}}, toonDur=0.1, keepPose=True),
            k(TAP3, toon={'reach': {'R': TAPP(0.0)}, 'hands': {'R': 'point'}}, toonDur=0.05, keepPose=True),
            k(r(TAP3 + 0.14), toon={'reach': {'R': TAPP(0.1)}, 'hands': {'R': 'point'}}, toonDur=0.08, keepPose=True),
            k(r(TAP3 + 0.28), toon={'reach': {'R': TAPP(0.0)}, 'hands': {'R': 'point'}}, toonDur=0.05, keepPose=True),
            k(r(TAP3 + 0.6), look='camera', lookDur=0.12), k(r(TAP3 + 0.6), toon={'face': {'lid': 0.3, 'mouth': 'bigsmile', 'brow': 0.4}}, toonDur=0.12, keepPose=True)])],
        props=[P('tableau3', 'diagramBoard', pos=BOARD, opts={'w': 2.4, 'ringAt': r(TAP3 + 0.05)})],
        cams=[C3A, C3B])
st.cue('sfx:click', 'S03', TAP3, 0.4); st.cue('sfx:click', 'S03', r(TAP3 + 0.28), 0.3); st.cue('sfx:squeak', 'S03', r(TAP3 + 0.06), 0.3)

# 4: twelve rockets from his lawn. Wide from the pavement: the rockets lift off one after another in smoke; he gapes in the doorway, deckchair in hand
D4 = st.dur('S04')
SPOTS = [[x, z] for x in (-3.4, -2.1) for z in (-2.6, -1.1, 0.4)] + [[x, z] for x in (2.5, 3.8) for z in (-2.6, -1.1, 0.4)]
DOOR = [0.97, 0, -3.75]
C4 = cam(0.0, [0.9, 1.4, 9.2], [0.9, 1.5, 8.7], [0.6, 2.6, -2.0], [0.6, 2.8, -2.0], lens=58, shake=0.06)
chk('S04', C4['from'], C4['lookAt'], 58, {'head': [DOOR[0], 2.05, DOOR[2]], 'feet': DOOR, 'rocketTop': [-3.4, 2.3, -2.6], 'rocketNear': [3.8, 0.0, 0.4], 'roof': [0, 4.6, -6.6]})
st.shot('S04', 'pavillon', setOpts=GARDEN, actors=[
        act('mec', DOOR, 0, 'stand', 'neutral', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'L': R5([DOOR[0] - 0.28, 0.88, -3.4], 1, 0.04), 'R': R5([DOOR[0] + 0.28, 0.88, -3.4], 1, 0.04)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0),
            k(0.4, look=[-1, 6, -1], lookDur=0.2), k(0.45, toon={'face': {'lid': 0.0, 'mouth': 'O', 'brow': 0.7, 'pop': 0.3}, 'sq': [0.97, 1.05, 0.97]}, toonDur=0.1, keepPose=True),
            k(0.9, look=[2, 8, -1], lookDur=0.3), k(1.6, look=[0, 12, -2], lookDur=0.3), k(1.7, toon={'face': {'lid': 0.15, 'mouth': 'O', 'brow': 0.6}, 'sq': [1, 1, 1]}, toonDur=0.15, keepPose=True)])],
        props=[P('fusees4', 'rocketLawn', pos=[0, 0, 0], opts={'spots': SPOTS, 's': 0.6, 't0': 0.28, 'gap': 0.07, 'acc': 16}),
               P('chaise4', 'deckChair', pos=[DOOR[0], 0, -3.05], ry=0)],
        cams=[C4])
st.cue('sfx:jet', 'S04', 0.28, 0.5); st.cue('engine', 'S04', 0.3, 0.35, 1.8); st.cue('thud', 'S04', 0.3, 0.3)

# ============================== space (spaceDark)
# 5: his tomatoes in orbit. Over the Earth's limb: his tomato stakes, loose tomatoes and the watering can tumble past a satellite
D5 = st.dur('S05')
# (stills 1) a round planet low in the frame: the near limb of a big one read as giant green triangles
C5 = cam(0.0, [0.0, 0.8, 4.6], [0.15, 0.85, 4.2], [0.0, -0.1, -4.0], [0.1, -0.05, -4.0], lens=48)
chk('S05', C5['from'], C5['lookAt'], 48, {'limb': [1.2, -0.4, -16.0], 'tomatoes': [0.3, 0.6, -1.5], 'sat0': [3.6, 1.7, -6.0], 'sat1': [-1.8, 1.5, -6.0]})
st.shot('S05', 'spaceDark', actors=[],
        props=[P('terre5', 'earthGlobe', pos=[1.2, -4.6, -16.0], opts={'radius': 4.2, 'seed': 5}),
               P('tomates5', 'orbitTomatoes', pos=[0.3, 0.6, -1.5], opts={'spin': 0.16}),
               P('sat5', 'satellite', pos=[3.6, 1.7, -6.0], rot=[0.3, 0.6, 0.1], keys=[k(0.0, to=[-1.8, 1.5, -6.0], dur=D5, ease='linear'), k(0.0, rotTo=[0.3, 1.1, 0.25], dur=D5, ease='linear')]),
               ],
        cams=[C5])
st.cue('sfx:tense', 'S05', 0.0, 0.15)

# 6: the size of the country. The parasol snaps open in front of the sun and swallows it; cut to the globe: its round shadow swells over the country
D6 = st.dur('S06'); OPEN6 = 0.2; CUT6 = 0.92
C6A = cam(0.0, [0.4, 1.4, 34.0], [0.3, 1.5, 31.0], [0.0, 3.4, -28.0], [0.0, 3.5, -28.0], lens=30)   # (stills 1) further: the open parasol filled the width
C6B = cam(CUT6, [60.0, 0.9, 14.5], [60.0, 0.85, 13.8], [60.0, 0.2, 0.0], [60.0, 0.2, 0.0], lens=44)
chk('S06', C6A['from'], C6A['lookAt'], 30, {'sun': [0, 4, -70], 'paraTop': [0, 9.2, -28], 'paraBot': [0, -2.8, -28]})
chk('S06b', C6B['from'], C6B['lookAt'], 44, {'globeTop': [60, 3, 0], 'globeBot': [60, -3, 0], 'country': [60, 0, 3]})
st.shot('S06', 'spaceDark', actors=[],
        props=[P('soleil6', 'sun', pos=[0, 4, -70], opts={'r': 4.5}),
               P('parasol6', 'orbitParasol', pos=[0, 3.2, -28], rot=[-PI / 2, 0, 0], opts={'r': 6.5, 'openAt': OPEN6, 'openDur': 0.5, 'spin': 0.15}),
               P('globe6', 'countryGlobe', pos=[60, -3, 0], opts={'radius': 3, 'shadowAt': r(CUT6 + 0.12), 'shadowDur': 0.5, 'shadowAng': 0.55})],
        cams=[C6A, C6B])
st.cue('whoosh', 'S06', OPEN6, 0.3, 0.4, 300, 1800); st.cue('sfx:poof', 'S06', r(OPEN6 + 0.35), 0.45)

# 7: it mowed down three satellites. From the side, the rim of the opening parasol bats them away one after another
D7 = st.dur('S07'); OPEN7, DUR7 = 0.55, 1.1
PZ7 = -10.0; RIM7 = r(PZ7 + 6.5 * 0.32)
def op_(u): c = 1.70158; uu = min(1.0, max(0.0, u)); return min(1.04, (1 + (c + 1) * (uu - 1) ** 3 + c * (uu - 1) ** 2) * 0.96 + 0.04 * uu)
def hit_t(frac):
    u = 0.0
    while u < 1.0 and 0.05 + 0.95 * op_(u) < frac: u += 0.005
    return r(OPEN7 + DUR7 * u, 2)
SATS7 = [('sat7a', [0.5, 3.1, RIM7], 3.1 / 6.5, [6, 10, 6]), ('sat7b', [1.0, -4.4, RIM7], 4.5 / 6.5, [7, -12, 5]), ('sat7c', [-0.3, 5.9, RIM7], 5.9 / 6.5, [3, 14, 7])]
C7 = cam(0.0, [13.5, 0.4, -3.2], [13.0, 0.3, -3.6], [0.0, 0.3, -8.6], [0.0, 0.3, -8.6], lens=56)
chk('S07', C7['from'], C7['lookAt'], 56, {'rimTop': [0, 6.5, RIM7], 'rimBot': [0, -6.5, RIM7], **{n: p for n, p, f, d in SATS7}})
HITS7 = {n: hit_t(f) for n, p, f, d in SATS7}
CHECKS.append(f"S07 hits {HITS7}")
st.shot('S07', 'spaceDark', actors=[],
        props=[P('parasol7', 'orbitParasol', pos=[0, 0, PZ7], rot=[-PI / 2, 0, 0], opts={'r': 6.5, 'openAt': OPEN7, 'openDur': DUR7}),
               P('terre7', 'earthGlobe', pos=[-14, -16, 30], opts={'radius': 10, 'seed': 5}),
               *[P(n, 'satellite', pos=p, rot=[0.2, 1.4, 0.1], scale=0.32, keys=[k(HITS7[n], to=add(p, d), dur=0.9, ease='out'), k(HITS7[n], rotTo=[2.4, 4.0, 1.2], dur=0.9, ease='out')]) for n, p, f, d in SATS7]],
        cams=[C7])
for n in HITS7: st.cue('clang', 'S07', HITS7[n], 0.4)

# 8: the whole country went grey. From the air, the shadow's edge slides over the suburbs (ÉTEINT)
D8 = st.dur('S08')
# (stills 1) the disc's y goes in pos: the prop's own y was overwritten and the disc lay under the lawn
# (staging 2) the slide happens inside the prop (dx0, moveAt): a key move left the disc out of the whole-film render
C8 = cam(0.0, [0.0, 140.0, 240.0], [0.0, 134.0, 226.0], [0.0, 0.0, -120.0], [0.0, 0.0, -120.0], lens=46)
st.shot('S08', 'aerialSuburb', actors=[],
        props=[P('ombre8', 'shadowFront', pos=[-330, 16, -140], opts={'r': 600, 'op': 0.7, 'dx0': -470, 'moveAt': 0.0, 'moveDur': 1.15})],
        cams=[C8])
st.card('S08', 'ÉTEINT', at=1.15)
st.cue('gust', 'S08', 0.1, 0.3, 1.2); st.cue('thud', 'S08', 1.15, 0.4)

# ============================== under the parasol: the canopy for a sky, the grade grey
CAN = {'r': 90, 'haze': 0.75}                                  # (staging 2) haze: the dome's foot reads as an overcast horizon
# 9: the sunflowers hung their heads. Low in the field: the heads swing down in a wave from the front row back
D9 = st.dur('S09')
C9 = cam(0.0, [0.3, 2.0, 3.4], [0.2, 1.95, 3.0], [0.0, 1.5, -2.4], [0.0, 1.45, -2.4], lens=46)   # (staging 2) at head height: from below, the hung heads showed their flat undersides
chk('S09', C9['from'], C9['lookAt'], 46, {'front': [0, 1.75, -1.0], 'back': [0, 1.9, -4.6], 'side': [2.8, 1.8, -1.0]})
st.shot('S09', 'grassland', setOpts={'clouds': 0}, grade=GREY, actors=[],
        props=[P('dome9', 'canopySky', pos=[0, 0, 0], opts=CAN), P('tournesols9', 'sunflowers', pos=[0, 0, -1.0], opts={'cols': 7, 'rows': 5, 'gap': 0.9, 'droopAt': 0.62, 'wave': 0.1, 'hs': 1.45, 'up': -0.2, 'down': 1.25})],
        cams=[C9])
st.cue('sfx:slideDownSlow', 'S09', 0.7, 0.35)

# 10: the solar panels were laid off. From the road: panels on little legs queue sideways along the unemployment office with cardboard signs
D10 = st.dur('S10')
SIGNS = ['CHERCHE\nLUMIÈRE', "DIX ANS\nD'EXPÉRIENCE", 'SANS\nSOLEIL', "J'AI DES\nENFANTS"]
WALK = [[8.9, 0, z] for z in (-4.5, -3.3, -2.1, -0.9)]
C10 = cam(0.0, [5.0, 1.45, 1.9], [4.9, 1.45, 1.5], [9.0, 1.0, -2.6], [9.0, 1.0, -2.8], lens=52)   # (stills 1) closer: the signs read
chk('S10', C10['from'], C10['lookAt'], 52, {'sign0': [8.66, 0.8, -4.5], 'sign3': [8.66, 0.8, -0.9], 'office': [10.0, 2.85, -4.0], 'door': [10.0, 1.2, -5.8]})
st.shot('S10', 'parisStreet', setOpts={'clouds': 0}, grade=GREY, actors=[],
        props=[P('dome10', 'canopySky', pos=[6, 0, -3], opts=CAN), P('bureau10', 'jobOffice', pos=[10.0, 0, -4.0], ry=-90, opts={'w': 6.5, 'doorX': -1.8}),
               *[P(f'panneau10_{i}', 'solarWalker', pos=p, ry=-90, opts={'walk': True, 'phase': i * 0.37, 'sign': SIGNS[i]},
                   keys=[k(r(0.45 + 0.08 * i), to=add(p, [0, 0, -0.45]), dur=0.5, ease='inOut')]) for i, p in enumerate(WALK)],
               *[P(f'petit10_{i}', 'solarWalker', pos=[8.7, 0, r(-0.3 + 0.45 * i)], ry=-90, scale=0.5, opts={'walk': True, 'phase': 0.2 + i * 0.5, 'sign': ' '},
                   keys=[k(0.85, to=[8.7, 0, r(-0.75 + 0.45 * i)], dur=0.5, ease='inOut')]) for i in range(2)]],
        cams=[C10])
st.cue('sfx:stepSoft', 'S10', 0.45, 0.25); st.cue('sfx:stepSoft', 'S10', 0.7, 0.2)

# 11: the agency declared the mission a success. The director beams at the podium under MISSION RÉUSSIE over the grey map; applause, flashes
D11 = st.dur('S11'); OK11 = 1.38
SPK = [0.0, 0, -2.45]
C11 = cam(0.0, [0.3, 1.8, 3.2], [0.3, 1.78, 2.8], [0.55, 1.6, -2.4], [0.55, 1.6, -2.4], lens=44)   # (stills 1) from the front of the room: the director and the screen (the reporters, off screen, are heard and flash)
chk('S11', C11['from'], C11['lookAt'], 44, {'head': [0, 2.0, -2.45], 'screen': [1.45, 1.95, -2.7], 'screenTop': [1.45, 2.55, -2.7], 'journoL': [-0.9, 1.9, 0.4], 'journoR': [1.5, 1.9, 0.3]})
JOUR = [('journaliste1', [-0.9, 0, 0.4], 165), ('journaliste2', [1.5, 0, 0.3], -160)]
def CLAP(pos, ry, t0, n=5):
    c = off(pos, ry, 0.35, 0.0, 1.35); out = []
    for i in range(n):
        tt = r(t0 + i * 0.16); w = 0.09 if i % 2 == 0 else 0.0
        out.append(k(tt, toon={'reach': {'L': R5(off(c, ry, 0, -0.06 - w, 0.0), 1, 0.04), 'R': R5(off(c, ry, 0, 0.06 + w, 0.0), 1, 0.04)}, 'hands': {'L': 'open', 'R': 'open'}}, toonDur=0.07, keepPose=True))
    return out
st.shot('S11', 'pressRoom', setOpts={'backdrop': 'AGENCE|ESPACE|MISSION', 'chairs': False, 'flagOpts': {'colors': ['#6A3FA0', '#F2C94C']}}, grade=GREYIN, actors=[
        act('directeur', SPK, 0, 'podium', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.25, 'mouth': 'smile', 'brow': 0.3}}, toonDur=0.0),
            k(OK11, toon={'face': {'lid': 0.2, 'mouth': 'bigsmile', 'brow': 0.5}, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.1, keepPose=True), *blink(1.8, {'lid': 0.2, 'mouth': 'bigsmile', 'brow': 0.5})])],
        props=[P('ecran11', 'pressScreen', pos=[1.45, 0, -2.7], ry=-10, opts={'w': 1.6, 'y': 1.95}),
               P('flash11a', 'camFlash', pos=[-0.7, 1.95, 0.0], opts={'w': 0.5, 'at': [r(OK11 + 0.05), r(OK11 + 0.45)]}),
               P('flash11b', 'camFlash', pos=[1.2, 1.85, -0.2], opts={'w': 0.5, 'at': [r(OK11 + 0.25)]})],
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
st.shot('S12', 'parisStreet', setOpts={'clouds': 0}, grade=GREY, actors=[
        act(n, p, ry, 'stand', 'neutral', keys=[k(0.0, look=add(TORCH(p, ry), [0, 3, 0])),
            k(0.0, toon={'reach': {'R': R5(TORCH(p, ry), 1, 0.04), **({'L': R5(off(p, ry, 0.3, 0.3, 1.25), 1, 0.04)} if n in SIGN12 else {})}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'open' if i % 2 else 'line', 'brow': -0.3}}, toonDur=0.0),
            *PUMP(p, ry, r(0.75 + 0.05 * i)), *PUMP(p, ry, r(1.3 + 0.04 * i))]) for i, (n, p, ry) in enumerate(MARCH)],
        props=[P('dome12', 'canopySky', pos=[0, 0, -2], opts=CAN),
               *[P(f'torche12_{n}', 'handTorch', pos=add(TORCH(p, ry), [0, -0.12, 0]), opts={'beam': 7, 'beamR': 0.7, 'beamOp': 0.6, 'face': math.radians(yaw(TORCH(p, ry), [0.4, 0, 6.4]))}) for n, p, ry in MARCH],
               *[P(f'pancarte12_{n}', 'protestSign', pos=off(p, ry, 0.3, 0.3, 0.75), ry=ry, opts={'text': SIGN12[n], 'stick': 0.95}) for n, p, ry in MARCH if n in SIGN12]],
        cams=[C12])
st.cue('sfx:street', 'S12', 0.0, 0.3)

# 13: the gendarmes handcuffed the torches. At a table in the square a gendarme clicks the last cuff shut on a row of torches; marchers, hands up
D13 = st.dur('S13'); CLICK13 = 1.3
TAB = [0.0, 0, -0.5]; TH = 0.75
GD1 = [0.45, 0, -1.3]; GD2 = [-0.95, 0, -1.4]
LAST = [0.4, r(TH + 0.06), -0.5]
C13 = cam(0.0, [0.7, 1.95, 3.1], [0.6, 1.85, 2.7], [0.1, 1.15, -0.9], [0.1, 1.15, -0.9], lens=46)
chk('S13', C13['from'], C13['lookAt'], 46, {'gd1': [GD1[0], 2.0, GD1[2]], 'gd2': [GD2[0], 2.0, GD2[2]], 'torches': [0, TH + 0.06, -0.5], 'last': LAST, 'back': [1.5, 2.0, -3.6]})
st.shot('S13', 'parisStreet', setOpts={'clouds': 0}, grade=GREY, actors=[
        act('gendarme1', GD1, 0, 'stand', 'neutral', keys=[k(0.0, look=LAST),
            k(0.0, toon={'bend': {'spine': [0.35, 0, 0, 1, None]}, 'reach': {'L': R5(add(LAST, [-0.06, 0.06, -0.05]), 1, 0.04), 'R': R5(add(LAST, [0.07, 0.08, 0.02]), 1, 0.04)}, 'hands': {'L': 'pinch', 'R': 'pinch'}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.0),
            k(r(CLICK13 - 0.1), toon={'reach': {'R': R5(add(LAST, [0.02, 0.04, 0.0]), 1, 0.04)}}, toonDur=0.1, keepPose=True),
            k(r(CLICK13 + 0.35), look='camera', lookDur=0.15), *blink(1.95, {'lid': 0.45, 'mouth': 'line', 'brow': -0.2})]),
        act('gendarme2', GD2, 25, 'armsCrossed', 'neutral', keys=[k(0.0, look=[0, 1.0, -0.5]), k(0.0, toon={'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.0)]),
        *[act(n, [x, 0, z], 0, 'surrender', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.3, 'mouth': 'wavy', 'brow': 0.4}}, toonDur=0.0)]) for n, x, z in [('manif1', -0.6, -3.6), ('manif3', 1.6, -3.9), ('manif2', -2.4, -4.2)]]],
        props=[P('dome13', 'canopySky', pos=[0, 0, -2], opts=CAN), KEPI('kepi13a', 'gendarme1'), KEPI('kepi13b', 'gendarme2'),
               P('table13', 'table', pos=TAB, opts={'w': 1.6, 'd': 0.7, 'h': TH, 'color': '#8C949A', 'legs': '#5A6066'}),
               P('torches13', 'cuffedTorches', pos=[0, TH, -0.5], opts={'n': 5, 'gap': 0.2, 'beam': 1.4, 'clickAt': CLICK13})],
        cams=[C13])
st.cue('sfx:cuff', 'S13', CLICK13, 0.5)

# 14: a tank shot a hole in the parasol. The tank raises its gun and fires; the camera tilts up after the shell; a hole bursts open in the canopy (PERCÉ)
D14 = st.dur('S14'); FIRE14 = 0.62; PITCH = 1.05; V14 = 170.0
TANK = [0.0, 0, -4.0]
HOLE14 = add(TANK, mul([0.0, math.sin(PITCH), math.cos(PITCH)], 90 * 0.97))
HOLEAT = r(FIRE14 + 88 / V14, 2)
C14A = cam(0.0, [-6.2, 1.1, 6.2], [-6.0, 1.05, 5.8], [0.0, 1.8, -4.0], [0.0, 1.9, -4.0], lens=44)
C14B = cam(0.72, [-6.0, 1.0, 5.8], [-6.2, 0.95, 6.2], [0.0, 4.0, -2.0], HOLE14, lens=58, ease='out')
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
        props=[GDOME('dome15'), PATCH('disque15'), CHAIR('chaise15'),
               P('rayon15', 'lightShaft', pos=HOLEW, rot=[RXS, 0, RZS], ry=RYS, opts={'r': 5.0, 'len': SHAFT_L, 'op': 0.2, 'onAt': 0.02})],
        cams=[C15])
st.cue('sfx:choir', 'S15', 0.02, 0.35)

# 16: above his garden. From high above: the lit disc of his lawn, his deckchair in it, the country round it dark
D16 = st.dur('S16')
C16 = cam(0.0, [G[0] + 0.4, 31.0, G[2] + 5.5], [G[0] + 0.3, 28.5, G[2] + 5.0], G, G, lens=50)
chk('S16', C16['from'], C16['lookAt'], 50, {'chair': CH, 'patchE': add(G, [6.5, 0, 0]), 'patchW': add(G, [-6.5, 0, 0]), 'patchN': add(G, [0, 0, -6.5]), 'patchS': add(G, [0, 0, 6.5])})
st.shot('S16', 'pavillon', setOpts=GARDEN, actors=[act('mec', SEAT, RY, 'sit', 'unimpressed', keys=[k(0.0, look=HOLEW), k(0.0, toon={**LOUNGE, 'reach': {'R': VISOR}, 'face': SQUINT}, toonDur=0.0)])],
        props=[PATCH('disque16', dark=0), P('ombre16', 'sunPatch', pos=[G[0], 6.2, G[2]], opts={'r': 6.5, 'lawn': False, 'dark': 0.78, 'y': 0.0, 'rimOp': 0.0}), CHAIR('chaise16')],
        cams=[C16])

# 17: right in his eyes. The reverse first (the hole and its sun beyond the street, over his shoulder), then his squint: the framing of shot one
D17 = st.dur('S17'); T17 = 0.6
C17A = cam(0.0, C1B['from'], C1B['to'], L1B, L1B, lens=LENS1B)
C17B = cam(T17, C1A['from'], C1A['to'], C1A['lookAt'], C1A['lookAt2'], lens=36)
chk('S17', C17A['from'], C17A['lookAt'], LENS1B, {'hole': add(HEAD, mul(SUNDIR, 87)), 'head': HEAD})
st.shot('S17', 'pavillon', setOpts=GARDEN, actors=[act('mec', SEAT, RY, 'sit', 'unimpressed', keys=[*HERO1[:2],
            k(r(T17 + 0.05), toon={**LOUNGE, 'reach': {'R': R5(add(VISOR[:3], [0, 0.02, 0]), 1, 0.05)}, 'face': {**SQUINT, 'lid': 0.97}, 'sq': [1.03, 0.96, 1.03]}, toonDur=0.08),
            k(r(T17 + 0.3), toon={**LOUNGE, 'reach': {'R': VISOR}, 'face': SQUINT, 'sq': [1, 1, 1]}, toonDur=0.15)])],
        props=[GDOME('dome17'), PATCH('disque17'), CHAIR('chaise17'), P('eclat17', 'lensGlare', pos=GLARE1, opts={'s': 2.6, 'op': 0.85})],
        cams=[C17A, C17B])
st.cue('sfx:static', 'S17', T17, 0.15)

# 18: the whole country picnics at his place. Craning up over the packed disc: the marchers, the gendarmes, the scientists on blankets, the director
#     sunbathing on the car roof, two neighbours squeezed against his deckchair
D18 = st.dur('S18')
# (staging 2) the crowd packed inside the frame: the first layout spread it wider than a 9:16 frame (five of nine off screen); twelve picnickers
#     in rows from the house to the fence, two neighbours squeezed against his deckchair, the car with its towel at the back right
PICROWS = [(3.3, [-0.2, 0.9]), (2.2, [-0.7, 0.4, 1.4]), (1.1, [-0.9, 0.3, 1.3]), (-1.3, [-1.0, 1.0]), (-2.4, [-0.6, 0.4])]
PICWHO = [('manif1', 15, 'sitFloorEat'), ('savant2', -25, 'sitFloorSip'), ('manif6', 30, 'sitFloorWave'), ('gendarme1', -10, 'sitFloorEat'),
          ('journaliste1', -40, 'sitFloor'), ('manif4', 20, 'sitFloorSip'), ('savant1', 160, 'sitFloor'), ('manif5', -60, 'sitFloorEat'),
          ('gendarme2', 35, 'sitFloorSip'), ('savant3', -30, 'sitFloorWave'), ('manif2', 10, 'sitFloorEat'), ('journaliste2', -15, 'sitFloor')]
PICPOS = [[r(CH[0] + dx), 0, r(CH[2] + dz)] for dz, xs in PICROWS for dx in xs]
PIC = [(n, PICPOS[i], ry, clip) for i, (n, ry, clip) in enumerate(PICWHO)] + [('manif3', off(CH, RY, 0.15, -0.62, 0.0), RY, 'sitFloor'), ('voisine', off(CH, RY, 0.15, 0.62, 0.0), RY, 'sitFloorSip')]
BCOL = ['#C23A2E', '#2E6FB5', '#2F8A4A', '#E0A020', '#7A2E4E', '#C23A2E', '#2E6FB5']
BLANK = [[r(CH[0] + sum(xs) / len(xs)), r(CH[2] + dz + 0.1), 0.0, r(1.15 * len(xs) + 0.4), 1.1, BCOL[i]] for i, (dz, xs) in enumerate(PICROWS)]
CAR = [1.6, 0, -2.9]
C18 = cam(0.0, [-0.5, 3.2, 6.6], [-0.3, 9.2, 9.4], [-0.9, 0.7, -0.9], [-0.8, 0.2, -1.3], lens=56, ease='inOut')
chk('S18', C18['from'], C18['lookAt'], 56, {'mec': HEAD, **{n: [p[0], 1.2, p[2]] for n, p, ry, c in PIC}})
chk('S18b', C18['to'], C18['lookAt2'], 56, {'mec': HEAD, 'car': [CAR[0], 2.1, CAR[2]], 'edgeE': add(G, [6.5, 0, 0]), 'edgeW': add(G, [-6.5, 0, 0])})
st.shot('S18', 'pavillon', setOpts={**GARDEN, 'mailbox': False}, actors=[
        act('mec', SEAT, RY, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**LOUNGE, 'reach': {'R': VISOR}, 'face': {**SQUINT, 'mouth': 'line'}, 'sq': [0.9, 1.04, 1.0]}, toonDur=0.0), *blink(1.1, {**SQUINT, 'mouth': 'line'})]),
        *[act(n, p, ry, clip, 'neutral', keys=[k(0.0, look='camera' if i % 3 == 0 else HOLEW), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'smile' if i % 2 else 'line'}}, toonDur=0.0)]) for i, (n, p, ry, clip) in enumerate(PIC)],
        act('directeur', [CAR[0] - 0.2, 2.06, CAR[2]], 90, 'lieRelax', 'neutral', keys=[k(0.0, look=HOLEW), k(0.0, toon={'face': {'lid': 0.8, 'mouth': 'smile'}}, toonDur=0.0)])],
        props=[GDOME('dome18'), PATCH('disque18'), CHAIR('chaise18'), KEPI('kepi18', 'gendarme1'), KEPI('kepi18b', 'gendarme2'),
               P('pique18', 'picnicSpread', pos=[0, 0, 0], opts={'blankets': BLANK}),
               P('voiture18', 'car', pos=CAR, ry=0, opts={'color': '#3E7AB8'}), P('serviette18', 'beachTowel', pos=[CAR[0] - 0.25, 2.06, CAR[2]], ry=90, opts={'w': 0.9, 'd': 1.7, 'hang': 0.3})],
        cams=[C18])
st.cue('sfx:street', 'S18', 0.0, 0.3)

# 19: he had a parasol in the garage. Beside his deckchair, the garage open behind him, he holds a small dusty parasol; it opens with a puff of dust; a
#     look to us
D19 = st.dur('S19'); OPEN19 = 1.08
CH19 = [0.2, 0, -0.5]
PIC19 = [('manif1', [-2.0, 0, 0.9], 25, 'sitFloorEat'), ('savant2', [-2.6, 0, -1.2], 40, 'sitFloorSip'), ('manif4', [-0.3, 0, -3.0], -15, 'sitFloor'), ('gendarme1', [-1.9, 0, -2.6], 20, 'sitFloorEat')]   # (staging 2) the picnic goes on round him, never in front of him and his parasol                                          # (staging 1) the deckchair moved up beside him for this shot: the parasol shades it
PAR19 = [0.0, 0, -1.0]
ME19 = [-0.65, 0, -0.75]; RY19 = 10
SHED = [-2.9, 0, 0.5]
F19 = [r(ME19[0] + 0.2), 1.6, r(ME19[2] + 7.5)]
L19, LENS19, W19 = fit(F19, {'head': [ME19[0], 2.35, ME19[2]], 'feet': [ME19[0], 0, ME19[2]], 'parTop': add(PAR19, [0, 2.3, 0]), 'shed': add(SHED, [0.6, 2.0, 0.6]), 'chair': CH19}, margin=0.1, top=0.12, bottom=0.76)
C19 = cam(0.0, F19, add(F19, [0, 0, -0.2]), L19, L19, lens=LENS19)
CHECKS.append(f"S19 fit lens {LENS19} {W19}")
chk('S19', C19['from'], C19['lookAt'], LENS19, {'head': [ME19[0], 2.05, ME19[2]], 'parTop': add(PAR19, [0, 2.25, 0]), 'shed': add(SHED, [0, 1.2, -1.0]), 'chair': CH19})
st.shot('S19', 'pavillon', setOpts=GARDEN, actors=[
        act('mec', ME19, RY19, 'stand', 'unimpressed', keys=[k(0.0, look='camera'),
            k(0.0, toon={'reach': {'L': R5(add(PAR19, [0.03, 1.12, 0.03]), 1, 0.04)}, 'hands': {'L': 'grip'}, 'face': {'lid': 0.75, 'mouth': 'line', 'brow': -0.4}}, toonDur=0.0),
            k(r(OPEN19 - 0.15), toon={'reach': {'L': R5(add(PAR19, [0.03, 1.02, 0.03]), 1, 0.04)}, 'sq': [1.02, 0.97, 1.02]}, toonDur=0.1, keepPose=True),
            k(OPEN19, toon={'reach': {'L': R5(add(PAR19, [0.03, 1.16, 0.03]), 1, 0.04)}, 'sq': [1, 1, 1]}, toonDur=0.08, keepPose=True),
            k(r(OPEN19 + 0.1), look=add(PAR19, [0, 2.3, 0]), lookDur=0.12), k(r(OPEN19 + 0.25), toon={'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.15, keepPose=True),
            k(r(OPEN19 + 0.75), look='camera', lookDur=0.12), *blink(r(OPEN19 + 1.1), {'lid': 0.4, 'mouth': 'line', 'brow': -0.1})]),
        *[act(n, p, ry, clip, 'neutral', keys=[k(0.0, look=HOLEW if i % 2 else [ME19[0], 1.9, ME19[2]]), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'smile' if i % 2 else 'line'}}, toonDur=0.0)]) for i, (n, p, ry, clip) in enumerate(PIC19)]],
        props=[GDOME('dome19'), PATCH('disque19'), P('chaise19', 'deckChair', pos=CH19, ry=RY), KEPI('kepi19', 'gendarme1'),
               P('pique19', 'picnicSpread', pos=[0, 0, 0], opts={'seed': 37, 'blankets': [[p[0], r(p[2] + 0.1), 0.2, 1.3, 1.1, BCOL[i]] for i, (n, p, ry, c) in enumerate(PIC19)]}),
               P('garage19', 'garageShed', pos=SHED, ry=70), P('etagere19', 'garageShelf', pos=off(SHED, 70, -2.9, 0, 0), ry=70, opts={'w': 1.8}),
               P('parasol19', 'parasol', pos=PAR19, opts={'radius': 1.0, 'height': 2.1, 'openAt': OPEN19, 'colors': ['#2F8A6A', '#F4EEDF']}),
               P('poussiere19', 'dustBurst', pos=add(PAR19, [0, 2.0, 0]), opts={'at': OPEN19, 'dur': 0.9, 'r': 1.1})],
        cams=[C19])
st.cue('whoosh', 'S19', r(OPEN19 - 0.05), 0.2, 0.3, 500, 2000); st.cue('sfx:poof', 'S19', r(OPEN19 + 0.02), 0.4)

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
