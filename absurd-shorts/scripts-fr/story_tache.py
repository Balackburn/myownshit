#!/usr/bin/env python3
"""La tache (story 93, cycle 51; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man made a stain on his shirt. The stain refused to leave. The judge signed its eviction. The riot police charged the shirt. The stain dug in
under the pocket. A tank fired stain remover. It bleached the whole neighbourhood. The houses, the cars, the mayor. The stain stayed red. Stretched,
it had the exact shape of the country. A presidential decree forbids washing it. The shirt replaced the flag. Two guards salute it day and night.
The embassies officially recognised the stain. The shirt stays his. So does the upkeep. He irons around the stain.
Running gag: whatever the State fires, sprays or hoists, the stain stays red while everything round it changes (a white neighbourhood, a white
mayor); the State's own blast gives it the country's shape, and the State ends up saluting what it shot at.
Staging: in his kitchen, the hero in a white shirt (collar, buttons, breast pocket always readable) lifts a forkful of spaghetti; a glob drops and
a small irregular orange-red splat with a pasta strand and one drip lands on his chest; he looks down, then at us (push-in). At the bathroom basin
he scrubs it with a sponge, harder, and the sponge falls apart in his hand; the stain has not moved. In court, over the shirt's shoulder (it hangs
on a rack in the dock, facing the judge), the judge strikes the gavel; reverse on the shirt: an eviction order pops up beside it and is stamped
EXPULSÉE. In the street of his pastel neighbourhood the shirt hangs alone on a clothes rack, low in the foreground, and a line of riot police with
round shields and visors charges at it from the end of the street. Macro on the shirt's chest: the splat slides up and under the pocket flap, a
drip left peeking out; behind, the riot police stand with their shields up. From a side street, a tank with a giant stain-remover spray bottle
strapped to its barrel fires a thick white jet (recoil, dust). From high above, the jet sweeps down the street and the houses, the trees, the
cars and the road turn white one after another in bursts of foam (DÉCOLORÉ). Three beats: white houses, white cars, the mayor on the town hall
steps, white down to his sash, blinking, unhurt. Low push-in on the shirt against the sky in the white street: only the stain is red, stretched
into a long splash with drips and the pasta strand, trailing the jet's way. Forensic officers in pale suits tape it off; a transparent map of an
invented country comes down over it and matches drip for drip (the coast flashes); they step back. In the press room the president signs a
decree at the lectern and holds up a crossed-out washing machine on a stick; flashes. On the palace roof, low: a soldier carries away a folded
bundle of old cloth while another hoists the shirt on its hanger up the pole (HISSÉE). Two ceremonial guards salute at the foot of the pole; the
sky snaps to night with a moon and stars and they do not move. Ambassadors in plain dark suits and plain sashes sign a register under the pole, a
band plays. Two soldiers hand the hero (now in a pale blue shirt) a folded ironing board with a form on it and an iron; he holds them flatly. At
dawn on the roof he irons the shirt laid on the board, steering the iron round the country-shaped stain, the two guards saluting behind him.
Natural look; cycle 51: props_tache.js (tacheShirtFront, tacheHangShirt, tacheRack, tacheSponge, tachePastaPlate, tacheFork, tachePastaGlob,
tacheEvictOrder, tacheRoundShield, tacheTank, tacheJet, tacheBleach, tacheGround, tacheTape, tacheNoWashSign, tacheDecree, tachePalaceRoof,
tachePole, tacheBundle, tacheIron, tacheBoard); cottage, car, tree, table, gavel, soundBlock, moon, stars (props.js), visorHelmet (props_chat),
guardHelmet, epaulettes, sabre, bandInstr (props_centime), brass, register, kepi (props_conseiller), camFlash (props_bocal), wallTitle (props_rayon)
reused.
Lessons applied from the start: `lens` is the vertical field; characters are about 2.3 m tall with the box head; faces and key props above the
caption band (0.77-0.83) and heads below the card band (0.07-0.18) when a card stamps; every character and key prop checked with project(); the
stain is never a round disc (an irregular splat, then a long splash, always orange-red, never red-on-white disc: it would read as a real flag); no
flags, insignia, or real country outline (the map is made up); no raised straight arm (the sign is held at the shoulder, elbow bent; the guards'
salute is the hand at the brow); the payoff (S16) gets its own camera; white things against the sky or a dark doorway (white on white vanishes);
no English, no brands; nobody hurt (the mayor blinks)."""
from story_kit import *
import math

st = Story('tache', look='natural')
st.plan([(f'S{i:02d}', f'L{i:02d}', 0) for i in range(1, 17)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def sub(a, b): return [r(a[i] - b[i]) for i in range(3)]
def mul(a, s): return [a[i] * s for i in range(3)]
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

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
DEAD = {'lid': 0.4, 'mouth': 'line'}
def blink(t, face=None): return [k(t, toon={'face': {**(face or DEAD), 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(t + 0.1), toon={'face': face or DEAD}, toonDur=0.06, keepPose=True)]
def R5(p, w=1, s=0.04): return [*p, w, s]
def FRONT(pid, who, **o): return P(pid, 'tacheShirtFront', on={'actor': who, 'joint': 'torso', 'offset': [0.0, 0.03, 0.135]}, opts=o)
def VISOR(pid, who): return P(pid, 'visorHelmet', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.0, 0.0]})
def KEPI(pid, who): return P(pid, 'kepi', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'w': 0.222, 'd': 0.17, 'color': '#4E5A3A', 'band': '#2E3424'})
def GUARD(pid, who): return P(pid, 'guardHelmet', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}, scale=1.1, opts={'gold': True})
def EPAU(pid, who): return P(pid, 'epaulettes', on={'actor': who, 'joint': 'torso', 'offset': [0.0, 0.635, 0.0]}, opts={'w': 0.58})
def SABRE(pid, who): return P(pid, 'sabre', on={'actor': who, 'joint': 'torso', 'offset': [0.26, 0.02, 0.15]})
def SALUTE(p, ry): return R5(off(p, ry, 0.08, 0.2, 2.02), 1, 0.03)
SAL_F = {'lid': 0.35, 'mouth': 'line', 'brow': -0.3}
def saluting(p, ry, t0=0.0, life=()):
    return [k(0.0, look='camera'), k(0.0, toon={'reach': {'R': SALUTE(p, ry)}, 'hands': {'R': 'open'}, 'face': SAL_F}, toonDur=0.0), *life]

for g_ in [('S01', 1.2, 'mec', 'splat'), ('S02', 1.45, 'mec', 'sponge'), ('S08', 2.0, 'maire', 'white mayor'), ('S15', 1.9, 'mecB', 'upkeep'), ('S16', 2.4, 'mecB', 'ironing')]:
    st.gag(*g_)

# ============================== his kitchen (kitchenDay: the back wall at z -3.4)
KIT = {'fridge': False}
ME1 = [0.0, 0, -1.2]; RY1 = 14
STAIN1 = off(ME1, RY1, 0.16, 0.085, 1.31)                      # the splat's centre on his chest (u 0.34, v 0.5 of the shirt front)
# 1: the hook. Close and frontal at his counter: he lifts a forkful of spaghetti, a glob drops and a small irregular splat with a pasta strand
#    lands on his white shirt on « tache »; he looks down at it, then at us; a slow push in to the stain, his face kept in the frame
D1 = st.dur('S01'); DROP1 = 0.72; LAND1 = r(st.at('S01', 'L01', 5) - 0.02)
C1 = cam(0.0, off(ME1, RY1, 2.95, -0.35, 1.74), off(ME1, RY1, 2.45, -0.27, 1.68), off(ME1, RY1, 0.0, 0.0, 1.6), off(ME1, RY1, 0.0, 0.02, 1.53), lens=40, ease='inOut')
chkc('S01', C1, {'headTop': off(ME1, RY1, 0, 0, 2.3), 'eyes': off(ME1, RY1, 0.17, 0, 2.05), 'stain': STAIN1, 'pocket': off(ME1, RY1, 0.16, -0.06, 1.47), 'plate': off(ME1, RY1, 0.55, 0.05, 1.03)})
chkc('S01', C1, {'headTop': off(ME1, RY1, 0, 0, 2.3), 'eyes': off(ME1, RY1, 0.17, 0, 2.05), 'stain': STAIN1, 'hem': off(ME1, RY1, 0.16, 0, 1.05)}, end=True)
FORKUP = R5(off(ME1, RY1, 0.36, 0.13, 1.62), 1, 0.05); FORKDN = R5(off(ME1, RY1, 0.5, 0.12, 1.12), 1, 0.05)
EAT = {'lid': 0.2, 'mouth': 'O', 'jaw': 0.35, 'brow': 0.3}
HERO1 = [k(0.0, look=add(FORKUP[:3], [0, 0.1, 0])), k(0.0, toon={'reach': {'R': FORKDN}, 'hands': {'R': 'grip', 'L': 'open'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.0),
         k(0.12, toon={'reach': {'R': FORKUP}, 'hands': {'R': 'grip'}, 'face': EAT, 'sq': [0.97, 1.03, 0.97]}, toonDur=0.32, toonEase='inOut'),
         k(0.5, toon={'reach': {'R': R5(add(FORKUP[:3], [0, 0.03, -0.02]), 1, 0.05)}, 'hands': {'R': 'grip'}, 'face': {**EAT, 'jaw': 0.5}, 'sq': [1, 1, 1]}, toonDur=0.12),
         k(r(DROP1 + 0.02), look=STAIN1, lookDur=0.1),
         k(LAND1, toon={'reach': {'R': FORKUP}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'o', 'jaw': 0.25, 'brow': 0.9}, 'sq': [1.04, 0.95, 1.04], 'bend': {'neck': [0.35, 0, 0, 1, None]}}, toonDur=0.05, toonEase='out', blend=0.02),
         k(r(LAND1 + 0.1), toon={'reach': {'R': FORKUP}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.1, 'mouth': 'o', 'jaw': 0.15, 'brow': 0.7}, 'sq': [1, 1, 1], 'bend': {'neck': [0.32, 0, 0, 1, None]}}, toonDur=0.1),
         k(1.42, look='camera', lookDur=0.12), k(1.42, toon={'reach': {'R': FORKUP}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.1}, 'bend': {'neck': [0.0, 0, 0, 1, None]}}, toonDur=0.14),
         *blink(1.72, {'lid': 0.45, 'mouth': 'line', 'brow': -0.1})]
GLOB0 = off(ME1, RY1, 0.36, 0.11, 1.78)
st.shot('S01', 'kitchenDay', setOpts=KIT, actors=[act('mec', ME1, RY1, 'stand', 'neutral', keys=HERO1)],
        props=[FRONT('chemise1', 'mec', stainAt=LAND1),
               P('comptoir1', 'table', pos=off(ME1, RY1, 0.62, 0, 0), ry=RY1, opts={'w': 1.5, 'd': 0.6, 'h': 1.0, 'color': '#E8A97E'}),
               P('assiette1', 'tachePastaPlate', pos=off(ME1, RY1, 0.55, 0.05, 1.0), ry=RY1, opts={'s': 1.2}),
               P('fourchette1', 'tacheFork', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.02, 0.04], 'face': 'camera'}, opts={'s': 1.5, 'emptyAt': DROP1}),
               P('miette1', 'tachePastaGlob', pos=GLOB0, opts={'s': 1.3}, keys=[k(0.0, visible=False), k(DROP1, visible=True), k(DROP1, to=add(STAIN1, [0, 0.0, 0.03]), dur=r(LAND1 - DROP1), ease='in'), k(LAND1, visible=False)])],
        cams=[C1])
st.cue('sfx:splat', 'S01', LAND1, 0.55); st.cue('sfx:gasp', 'S01', r(LAND1 + 0.08), 0.25)

# ============================== the bathroom (salleDeBain: the basin at x -1.7 on the back wall z -2.2)
ME2 = [-0.7, 0, -1.15]; RY2 = 22
STAIN2 = off(ME2, RY2, 0.16, 0.085, 1.31)
# 2: the stain refused to leave. At the basin, three-quarter front: he scrubs his chest with a yellow sponge, then harder and faster (a squash),
#    and the sponge falls apart in his hand; the splat has not moved; he stares at his empty fingers, then at us
D2 = st.dur('S02'); HARD2 = 0.62; BREAK2 = r(st.at('S02', 'L02', 5) + 0.05)
C2 = cam(0.0, off(ME2, RY2, 2.75, 0.05, 1.72), off(ME2, RY2, 2.5, 0.02, 1.7), off(ME2, RY2, 0.0, 0.32, 1.62), off(ME2, RY2, 0.0, 0.3, 1.6), lens=42)
chkc('S02', C2, {'headTop': off(ME2, RY2, 0, 0, 2.3), 'stain': STAIN2, 'basin': [-1.7, 0.95, -1.9], 'hem': off(ME2, RY2, 0.16, 0, 1.05)})
SCRUB = lambda dx, dy=0.0: R5(off(ME2, RY2, 0.24, 0.085 + dx, 1.31 + dy), 1, 0.04)
EFF = {'lid': 0.55, 'mouth': 'clench', 'brow': -0.7}
HERO2 = [k(0.0, look=STAIN2), k(0.0, toon={'reach': {'R': SCRUB(0.0)}, 'touch': {'L': ['torso', 0.22, 0.05, 0.12, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'open'}, 'bend': {'neck': [0.3, 0, 0, 1, None]}, 'face': EFF}, toonDur=0.0)]
for i in range(int(HARD2 / 0.1)):
    HERO2.append(k(r(0.05 + 0.1 * i), toon={'reach': {'R': SCRUB(0.05 if i % 2 else -0.05, 0.02 * (i % 2))}}, toonDur=0.08, keepPose=True))
for i in range(int((BREAK2 - HARD2) / 0.06)):
    HERO2.append(k(r(HARD2 + 0.06 * i), toon={'reach': {'R': SCRUB(0.08 if i % 2 else -0.08, 0.03 * (i % 2))}, 'sq': [1.05, 0.95, 1.05] if i % 2 else [0.98, 1.02, 0.98], 'face': {**EFF, 'lid': 0.75, 'brow': -1.0}}, toonDur=0.05, keepPose=True))
HERO2 += [k(BREAK2, toon={'reach': {'R': R5(off(ME2, RY2, 0.34, 0.12, 1.36), 1, 0.05)}, 'hands': {'R': 'spread'}, 'sq': [1, 1, 1], 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'o', 'brow': 0.8}}, toonDur=0.06, toonEase='out', keepPose=True),
          k(r(BREAK2 + 0.04), look=off(ME2, RY2, 0.34, 0.12, 1.36), lookDur=0.08),
          k(r(BREAK2 + 0.42), look='camera', lookDur=0.12), k(r(BREAK2 + 0.42), toon={'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.12, keepPose=True)]
st.shot('S02', 'salleDeBain', setOpts={'half': 3.4}, actors=[act('mec', ME2, RY2, 'stand', 'neutral', keys=HERO2)],
        props=[FRONT('chemise2', 'mec'), P('eponge2', 'tacheSponge', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.05, 0.05]}, opts={'s': 1.3, 'breakAt': BREAK2})],
        cams=[C2])
for t_ in [0.05, 0.25, 0.45, HARD2, r(HARD2 + 0.12), r(HARD2 + 0.24)]: st.cue('sfx:scratch', 'S02', t_, 0.18)
st.cue('sfx:crunch', 'S02', BREAK2, 0.4)

# ============================== the court (replicaCourt: the judge's bench at z -14)
JG = [-0.35, -0.3, -14.0]; RYJ = 0
RACK3 = [0.45, 0, -11.6]; RYR3 = 172
# 3: the judge signed its eviction. Over the shirt's shoulder (it hangs on a rack in the dock, facing the bench): the judge strikes the gavel on
#    « signé »; reverse on the shirt's front: the eviction order pops up beside it and is stamped EXPULSÉE on « expulsion »
D3 = st.dur('S03'); HIT3 = r(st.at('S03', 'L03', 3) + 0.04); CUT3 = 0.92; STAMP3 = r(st.at('S03', 'L03', 5) + 0.02)
F3A = [-0.3, 1.6, -9.5]
L3A, LENS3A, W3A = fit(F3A, {'judge': add(JG, [0, 2.3, 0]), 'judgeL': add(JG, [-0.45, 1.6, 0]), 'shirtTop': add(RACK3, [0.3, 1.9, 0]), 'shirtHem': add(RACK3, [0.3, 1.05, 0])}, margin=0.05, top=0.12, bottom=0.86, lenses=range(30, 72))
C3A = cam(0.0, F3A, add(F3A, [0.03, 0.0, -0.2]), L3A, add(L3A, [0, -0.02, 0]), lens=LENS3A)
CHECKS.append(f'S03a fit lens {LENS3A} {W3A}')
ORDER3 = [-0.12, 1.0, -12.15]
F3B = [0.12, 1.5, -14.6]
L3B, LENS3B, W3B = fit(F3B, {'collarL': add(RACK3, [0.33, 1.88, 0]), 'collarR': add(RACK3, [-0.33, 1.88, 0]), 'hem': add(RACK3, [0, 1.05, 0]), 'orderTop': add(ORDER3, [-0.32, 0.84, 0]), 'orderBot': add(ORDER3, [-0.32, 0.0, 0])}, margin=0.04, top=0.18, bottom=0.8, lenses=range(30, 72))
C3B = cam(CUT3, F3B, add(F3B, [0.0, 0.0, 0.15]), L3B, L3B, lens=LENS3B)
CHECKS.append(f'S03b fit lens {LENS3B} {W3B}')
chkc('S03a', C3A, {'judgeHead': add(JG, [0, 2.0, 0]), 'shirtTop': add(RACK3, [0, 1.9, 0]), 'shirtHem': add(RACK3, [0, 1.05, 0]), 'gavel': [-0.37, 1.41, -13.3]})
chkc('S03b', C3B, {'stain': off(RACK3, RYR3, 0.05, -0.1, 1.5), 'collar': add(RACK3, [0, 1.85, 0]), 'hem': add(RACK3, [0, 1.07, 0]), 'orderTop': add(ORDER3, [0, 0.82, 0]), 'orderL': add(ORDER3, [-0.31, 0.4, 0]), 'orderR': add(ORDER3, [0.31, 0.4, 0])})
st.shot('S03', 'replicaCourt', setOpts={'handle': 'TRIBUNAL', 'windowX': -1.5, 'chairW': 1.2, 'chairH': 2.75, 'chairX': 0.15, 'benchGlow': '#5A564A'},
        actors=[act('juge', JG, RYJ, 'gavelStrikeL', params={'hit': HIT3}, keys=[k(0.0, look=add(RACK3, [0, 1.5, 0])), k(r(HIT3 + 0.4), look=add(RACK3, [0, 1.6, 0]), lookDur=0.1)])],
        props=[P('specs3', 'glasses', on={'actor': 'juge', 'joint': 'head', 'offset': [0.02, 0.17, 0.15]}, opts={'r': 0.042, 'dx': 0.07}),
               P('gavelUp3', 'gavel', on={'actor': 'juge', 'hand': 'L'}, keys=[k(0.0, visible=True), k(r(HIT3 - 0.02), visible=False)]),
               P('gavel3', 'gavel', pos=[-0.37, 1.41, -13.3], rot=[0, 0, -1.5708], keys=[k(0.0, visible=False), k(r(HIT3 - 0.02), visible=True)]),
               P('block3', 'soundBlock', pos=[0.1, 1.18, -13.3]),
               P('portant3', 'tacheRack', pos=RACK3, ry=RYR3, opts={'w': 0.9, 'shirt': {'stain': 'splat', 'sway': 0.02}}),
               P('barre3', 'table', pos=add(RACK3, [0.0, 0, -0.75]), ry=RYR3, opts={'w': 1.4, 'd': 0.12, 'h': 1.0, 'color': '#8A5A3A'}),
               P('ordre3', 'tacheEvictOrder', pos=ORDER3, ry=yaw(ORDER3, C3B['from']), scale=0.01, opts={'stampAt': STAMP3}, keys=[k(r(CUT3 + 0.06), scale=1.0, dur=0.14, ease='out')])],
        fx=[{'type': 'shake', 'at': HIT3, 'dur': 0.18, 'amount': 0.018}],
        cams=[C3A, C3B])
st.card('S03', 'EXPULSÉE', at=r(STAMP3 + 0.04))
st.cue('sfx:gavel', 'S03', HIT3, 0.55); st.cue('whoosh', 'S03', r(CUT3 + 0.04), 0.2, 0.2, 500, 2200); st.cue('thud', 'S03', STAMP3, 0.5)

# ============================== his neighbourhood: a pastel street along z, the shirt's rack in the middle of the road at the origin
COLS = [('#F2B8C6', '#B5402F'), ('#BFE3C0', '#4A6A8A'), ('#F6E3A1', '#8A5A3A'), ('#B9D7F0', '#B5402F'), ('#F4C7A1', '#4A6A8A'), ('#D9C6EE', '#8A5A3A')]
ZROW = [20.5, 12.0, 3.5, -5.0, -13.5, -22.0, -30.5, -39.0, -47.5]
HOUSES = [(10.4, z, -90, i) for i, z in enumerate(ZROW)] + [(-10.4, z, 90, i + 3) for i, z in enumerate(ZROW) if z not in (3.5, -5.0)]
TREES = [(6.6, z + 4.25) for z in ZROW[1:-1]] + [(-6.6, z + 4.25) for z in ZROW[1:-1] if abs(z + 4.25) > 4]
CARS = [(4.3, 7.5, 90, '#3E7AB8'), (4.3, 1.0, 90, '#E0A020'), (4.3, -6.5, 90, '#C23A2E'), (-4.3, 10.0, -90, '#2F8A4A'), (-4.3, -11.0, -90, '#7A2E4E'), (4.3, -18.0, 90, '#F4F1EA'), (-4.3, -26.0, -90, '#3E7AB8')]
RACK = [0.0, 0, 0.0]
WZ0, WV, WT0 = 22.0, 50.0, 0.12                                 # the white wave of S07: t = WT0 + (WZ0 - z) / WV
def wipe(z): return r(WT0 + (WZ0 - z) / WV)
GROUND = [[0, -15, 7, 80, '#6E7178', -1.5], [4.5, -15, 2, 80, '#D8D2C4', -1.5], [-4.5, -15, 2, 80, '#D8D2C4', -1.5], [10.25, -15, 9.5, 80, '#8CC46A', -1.5], [-10.25, -15, 9.5, 80, '#8CC46A', -1.5],
          [-18.0, 0, 26, 7, '#6E7178', -1.4]] + [[0, z, 0.15, 2.2, '#F4F1E8', -1.2] for z in range(22, -55, -5)]
def TOWN(sid, mode, zmin=-60.0, zmax=30.0, cars=True):
    """mode 'colour' (before), 'sweep' (S07: everything goes white as the wave passes), 'white' (after)"""
    at_ = (lambda z: 99) if mode == 'colour' else ((lambda z: -1) if mode == 'white' else wipe)
    gopt = {'rects': GROUND, 'at': 99} if mode == 'colour' else ({'rects': GROUND, 'at': -1} if mode == 'white' else {'rects': GROUND, 't0': WT0, 'z0': WZ0, 'v': WV, 'strip': 4})
    out = [P(f'sol{sid}', 'tacheGround', pos=[0, 0, 0], opts=gopt)]
    for j, (x, z, ry, i) in enumerate(HOUSES):
        if zmin <= z <= zmax: out.append(P(f'maison{sid}_{j}', 'tacheBleach', pos=[x, 0, z], ry=ry, opts={'prop': 'cottage', 'popts': {'color': COLS[i % 6][0], 'roof': COLS[i % 6][1]}, 'at': at_(z), 'puffAt': [0, 2.6, 2.0], 'puffR': 4.0, 'puffS': 1.4, 'seed': j}))
    for j, (x, z) in enumerate(TREES):
        if zmin <= z <= zmax: out.append(P(f'arbre{sid}_{j}', 'tacheBleach', pos=[x, 0, z], opts={'prop': 'tree', 'popts': {'seed': j + 3}, 'at': at_(z), 'puff': False}, scale=1.5))
    if cars:
        for j, (x, z, ry, c) in enumerate(CARS):
            if zmin <= z <= zmax: out.append(P(f'auto{sid}_{j}', 'tacheBleach', pos=[x, 0, z], ry=ry, scale=1.25, opts={'prop': 'car', 'popts': {'color': c}, 'at': at_(z), 'puffAt': [0, 1.0, 0], 'puffR': 2.2, 'puffS': 0.8, 'seed': 40 + j}))
    return out
TOWNSET = {'clouds': 0}
WHITESET = {'clouds': 0, 'grass': '#DCE5D3'}
def SHIRT_RACK(pid, **o): return P(pid, 'tacheRack', pos=RACK, ry=0, opts={'w': 1.0, 'h': 1.95, 'shirt': {'s': 1.0, **o}})
SH_TOP = 1.95 + 0.06 - 0.13                                    # the shirt's shoulders (the torso from 1.88 down to 1.08)
def SHP(u, v): return [r(-0.31 + 0.62 * u), r(SH_TOP - 0.62 * v), 0.03]   # a point on the shirt's front (u across, v in widths from the top)

CRS = [('crs1', -1.5, -24.0), ('crs2', -0.5, -23.0), ('crs3', 0.55, -23.4), ('crs4', 1.6, -24.4), ('crs5', -2.4, -25.2)]
STOP4 = 2.05
def crs_end(x, z0): return [r(0.12 + x * 0.42), 0, r(-4.2 - 0.35 * abs(x))]
def CRS_KEYS(j, x, z0, start=0.0, stop=STOP4):
    a, b = [x, 0, z0], crs_end(x, z0); hold = lambda p_, sq_, t_, dur_: k(t_, toon={'reach': {'L': R5(off(p_, 0, 0.36, -0.14, 1.22 * sq_[1]), 1, 0.03), 'R': R5(off(p_, 0, 0.36, 0.14, 1.18 * sq_[1]), 1, 0.03)},
        'hands': {'L': 'grip', 'R': 'grip'}, 'sq': list(sq_), 'face': {'lid': 0.0, 'mouth': 'clench', 'brow': -0.6}}, toonDur=dur_)
    return [k(start, to=b, dur=r(stop - start + 0.03 * j), clip='run', ease='linear'), hold(a, (1, 1, 1), 0.0, 0.0), hold(b, (1.15, 0.86, 1.1), r(stop + 0.03 * j), 0.05), hold(b, (1, 1, 1), r(stop + 0.03 * j + 0.15), 0.1)]
def SHIELD(pid, j, x, z0, start=0.0, stop=STOP4):
    a, b = [x, 0, z0], crs_end(x, z0)
    return P(pid, 'tacheRoundShield', pos=off(a, 0, 0.5, 0.0, 1.25), keys=[k(start, to=off(b, 0, 0.5, 0.0, 1.25), dur=r(stop - start + 0.03 * j), ease='linear')])
# 4: the riot police charged the shirt. Low in the road: the shirt hangs alone on its rack in the right foreground (its stain to us) and a line of
#    riot police with round shields and dark visors charges at it from the end of the street; the camera trucks slowly to the left
D4 = st.dur('S04')
C4 = cam(0.0, [-0.85, 0.62, 3.5], [-1.15, 0.6, 3.2], [0.55, 1.75, -12.0], [0.45, 1.72, -12.0], lens=50)
chkc('S04', C4, {'stain': SHP(0.34, 0.47), 'collar': SHP(0.5, 0.0), 'hem': SHP(0.5, 1.29), **{n: [x, 2.0, z0] for n, x, z0 in CRS}})
chkc('S04', C4, {'stain': SHP(0.34, 0.47), **{n: add(crs_end(x, z0), [0, 2.0, 0]) for n, x, z0 in CRS}}, end=True)
st.shot('S04', 'grassland', setOpts=TOWNSET, actors=[act(n, [x, 0, z0], 0, 'stand', 'determined', keys=CRS_KEYS(j, x, z0)) for j, (n, x, z0) in enumerate(CRS)],
        props=[*TOWN('S04', 'colour', zmin=-60, zmax=10), SHIRT_RACK('portant4', stain='splat', sway=0.03),
               *[SHIELD(f'bouclier4_{j}', j, x, z0) for j, (n, x, z0) in enumerate(CRS)], *[VISOR(f'casque4_{j}', n) for j, (n, x, z0) in enumerate(CRS)]],
        cams=[C4])
st.cue('sfx:stepRun', 'S04', 0.05, 0.4); st.cue('sfx:stepRun', 'S04', 0.8, 0.4); st.cue('sfx:siren', 'S04', 0.0, 0.1); st.cue('thud', 'S04', STOP4, 0.3)

# 5: the stain dug in under the pocket. Macro on the shirt's chest: the splat slides up and under the pocket flap on « retranchée », one drip left
#    peeking out; behind the collar the riot police stand with their shields raised
D5 = st.dur('S05'); SLIDE5 = r(st.at('S05', 'L05', 3) - 0.02)
C5 = cam(0.0, [0.12, 1.36, 1.45], [0.1, 1.38, 1.3], [0.05, 1.56, 0.0], [0.05, 1.58, 0.0], lens=40)
CRS5 = [('crs1', -0.5, -2.75), ('crs2', 0.12, -2.55), ('crs3', 0.72, -2.85)]
chkc('S05', C5, {'stain': SHP(0.34, 0.47), 'pocket': SHP(0.71, 0.31), 'collar': SHP(0.5, 0.0), 'stainLow': SHP(0.34, 0.6), **{n: [x, 2.05, z] for n, x, z in CRS5}, **{n + 'sh': [x, 2.35, z + 0.45] for n, x, z in CRS5}})
def CRS5K(j, p):
    UP = {'reach': {'L': R5(off(p, 0, 0.42, -0.14, 1.95), 1, 0.03), 'R': R5(off(p, 0, 0.42, 0.14, 1.9), 1, 0.03)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': {'lid': 0.1, 'mouth': 'clench', 'brow': -0.7}}
    return [k(0.0, look=[0, 1.6, 0]), k(0.0, toon={**UP, 'sq': [1.08, 0.93, 1.08]}, toonDur=0.0), k(0.12, toon={**UP, 'sq': [1, 1, 1]}, toonDur=0.15),
            k(r(SLIDE5 + 0.3 + 0.07 * j), toon={**UP, 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.0, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.08), k(r(SLIDE5 + 0.5 + 0.07 * j), toon={**UP, 'sq': [1, 1, 1]}, toonDur=0.12)]
st.shot('S05', 'grassland', setOpts=TOWNSET, actors=[act(n, [x, 0, z], 0, 'stand', 'determined', keys=CRS5K(j, [x, 0, z])) for j, (n, x, z) in enumerate(CRS5)],
        props=[*TOWN('S05', 'colour', zmin=-30, zmax=0, cars=False), SHIRT_RACK('portant5', stain='splat', slideAt=SLIDE5, slideDur=0.55, peek=1.0, sway=0.012),
               *[P(f'bouclier5_{j}', 'tacheRoundShield', pos=[x, 2.3, r(z + 0.45)]) for j, (n, x, z) in enumerate(CRS5)], *[VISOR(f'casque5_{j}', n) for j, (n, x, z) in enumerate(CRS5)]],
        cams=[C5])
st.cue('sfx:slideUp', 'S05', SLIDE5, 0.35); st.cue('sfx:squeak', 'S05', r(SLIDE5 + 0.5), 0.25)

# ============================== the tank, in the side street (x -24), facing +x, firing at the rack
TANK = [-24.0, 0, 0.0]; MUZ = [r(-24.0 + 4.97), 2.38, 0.0]
SHIRT_PT = [0.0, 1.5, 0.0]
# 6: a tank fired stain remover. Three-quarter front of the tank in the side street: the giant spray bottle strapped to its barrel; on « tiré » it
#    fires a thick white jet off to the right toward the rack; the hull rocks back, dust at the tracks, foam at the nozzle
D6 = st.dur('S06'); FIRE6 = r(st.at('S06', 'L06', 3) - 0.02)
C6 = cam(0.0, [-11.6, 1.3, 5.2], [-11.9, 1.32, 4.95], [-22.0, 2.0, 0.2], [-22.0, 2.05, 0.2], lens=44)
chkc('S06', C6, {'tankBack': [-27.0, 2.2, 0], 'tankFront': [-21.0, 1.0, 1.5], 'muzzle': MUZ, 'turretTop': [-24.4, 2.4, 0], 'trackL': [-24.0, 0.1, 1.8], 'jetOut': [-10.0, 1.8, 0.0]})
st.shot('S06', 'grassland', setOpts=TOWNSET, actors=[],
        props=[*TOWN('S06', 'colour', zmin=-14, zmax=22), P('char6', 'tacheTank', pos=TANK, ry=90, opts={'fireAt': FIRE6}),
               P('jet6', 'tacheJet', pos=MUZ, opts={'fireAt': r(FIRE6 + 0.02), 'v': 40, 'r': 0.3, 'hits': [[0, sub(SHIRT_PT, MUZ)]], 'mist': 2.0})],
        cams=[C6])
st.cue('thunder', 'S06', FIRE6, 0.5); st.cue('sfx:splash', 'S06', r(FIRE6 + 0.03), 0.5); st.cue('whoosh', 'S06', r(FIRE6 + 0.05), 0.35, 0.5, 300, 2400)

# 7: it bleached the whole neighbourhood. From high above the street: the jet sweeps down it from the near end to the far end and the houses, trees,
#    cars and road turn white one after another in bursts of foam (DÉCOLORÉ)
D7 = st.dur('S07'); CARD7 = r(st.at('S07', 'L07', 2) + 0.05)
C7 = cam(0.0, [9.0, 15.0, 30.0], [8.4, 14.2, 28.5], [-1.0, 0.0, -10.0], [-1.0, 0.0, -11.0], lens=46)
JETEND = lambda z: sub([7.2, 2.2, z], MUZ)
chkc('S07', C7, {'nearR': [10.4, 3, 20.5], 'nearL': [-10.4, 3, 12.0], 'farR': [10.4, 3, -47.5], 'rack': [0, 2, 0], 'muzzle': MUZ, 'cardBand': [0, 6, -30]})
st.shot('S07', 'grassland', setOpts=TOWNSET, look={'shafts': 0}, actors=[],
        props=[*TOWN('S07', 'sweep'), SHIRT_RACK('portant7', stain='splat', slid=True, stretchAt=wipe(0.0), hitAt=[wipe(0.0)]),
               P('jet7', 'tacheJet', pos=MUZ, opts={'fireAt': -1, 'v': 400, 'r': 0.55, 'sag': 0.04, 'mist': 6.0, 'splash': 2.5, 'hits': [[0.0, JETEND(WZ0 + 2)], [r(WT0 + 70 / WV), JETEND(WZ0 - 70)]]})],
        cams=[C7])
st.card('S07', 'DÉCOLORÉ', at=CARD7)
st.cue('sfx:splash', 'S07', 0.05, 0.4); st.cue('gust', 'S07', 0.1, 0.35, 1.5)
for z_ in [20.5, 3.5, -13.5, -30.5]: st.cue('sfx:poof', 'S07', wipe(z_), 0.3)

# ============================== the white neighbourhood
HALL = [30.0, 0, 40.0]
MAIRE = [30.0, 0.4, 43.25]
# 8: the houses, the cars, the mayor. Three beats: a low look at white cottages and a white tree against the blue sky; the white cars along the
#    kerb; the mayor on the town hall's steps, white from his hair to his sash, in his dark doorway: he blinks, twice, unhurt
D8 = st.dur('S08'); CUT8B = r(st.at('S08', 'L08', 2) - 0.03); CUT8C = r(st.at('S08', 'L08', 4) - 0.03)
C8A = cam(0.0, [1.8, 0.95, 16.0], [2.1, 1.0, 15.4], [10.4, 3.6, 10.0], [10.4, 3.7, 9.6], lens=46)
C8B = cam(CUT8B, [2.6, 0.85, 12.5], [2.75, 0.85, 12.0], [4.6, 1.0, -2.0], [4.6, 1.0, -2.5], lens=44)
C8C = cam(CUT8C, [30.35, 1.6, 46.4], [30.3, 1.62, 46.0], [30.0, 2.15, 43.2], [30.0, 2.15, 43.2], lens=44)
chkc('S08a', C8A, {'roof': [10.4, 6.0, 12.0], 'door': [7.2, 1.0, 12.0], 'base': [7.2, 0.0, 10.5]})
chkc('S08b', C8B, {'car0': [4.3, 1.4, 7.5], 'car1': [4.3, 1.4, 1.0], 'car2': [4.3, 1.4, -6.5]})
chkc('S08c', C8C, {'head': add(MAIRE, [0, 2.0, 0]), 'headTop': add(MAIRE, [0, 2.32, 0]), 'sash': add(MAIRE, [0, 1.3, 0.13]), 'door': [30.0, 2.6, 42.9], 'feet': MAIRE})
WF = {'lid': 0.35, 'mouth': 'line', 'brow': 0.1}
MAIREK = [k(0.0, look='camera'), k(0.0, toon={'face': WF, 'touch': {'L': ['torso', 0.28, 0.05, 0.06, 1, 0.03], 'R': ['torso', -0.28, 0.05, 0.06, 1, 0.03]}}, toonDur=0.0),
          *blink(r(CUT8C + 0.22), WF), *blink(r(CUT8C + 0.5), WF),
          k(r(CUT8C + 0.68), toon={'face': {'lid': 0.2, 'mouth': 'o', 'brow': 0.5}, 'sq': [0.98, 1.03, 0.98]}, toonDur=0.08, keepPose=True), k(r(CUT8C + 0.75), look=[31.5, 2.0, 46.0], lookDur=0.1), k(r(D8 - 0.05), look='camera', lookDur=0.08)]
st.shot('S08', 'grassland', setOpts=WHITESET, actors=[act('maire', MAIRE, 0, 'stand', 'neutral', keys=MAIREK)],
        props=[*TOWN('S08', 'white', zmin=-10, zmax=24), P('mairie8', 'tacheBleach', pos=HALL, ry=0, opts={'prop': 'townHall', 'popts': {'w': 6}, 'at': -1, 'puff': False}),
               P('porte8', 'table', pos=[30.0, 0.4, 42.55], opts={'w': 1.5, 'd': 0.06, 'h': 2.9, 'color': '#343A44'})],
        cams=[C8A, C8B, C8C])
st.cue('sfx:ding', 'S08', 0.15, 0.2); st.cue('sfx:ding', 'S08', CUT8B, 0.2); st.cue('sfx:boing', 'S08', r(CUT8C + 0.25), 0.15)

# 9: the stain, it, stayed red. A slow low push-in on the shirt against the sky in the white street: only the stain is red, stretched into a long
#    splash with drips and the pasta strand, trailing the jet's way; the drips creep a little longer
D9 = st.dur('S09')
C9 = cam(0.0, [0.35, 0.95, 3.4], [0.15, 1.18, 1.55], [0.0, 1.5, 0.0], [0.0, 1.45, 0.0], lens=40, ease='inOut')
chkc('S09', C9, {'collar': SHP(0.5, 0.0), 'stainL': SHP(0.15, 0.64), 'stainR': SHP(0.88, 0.64), 'drip': SHP(0.42, 0.85), 'hem': SHP(0.5, 1.29)})
chkc('S09', C9, {'collar': SHP(0.5, 0.0), 'stainL': SHP(0.15, 0.64), 'stainR': SHP(0.88, 0.64), 'drip': SHP(0.42, 0.85)}, end=True)
st.shot('S09', 'grassland', setOpts=WHITESET, actors=[], props=[*TOWN('S09', 'white', zmin=-40, zmax=8), SHIRT_RACK('portant9', stain='country', dripAt=0.6, sway=0.015)], cams=[C9])
st.cue('sfx:tense', 'S09', 0.0, 0.2)

# 10: stretched, it had the exact shape of the country. Forensic officers in pale suits by the rack; the tape runs out round it; a transparent map of
#     an invented country comes down over the shirt and matches drip for drip (the coast flashes on « exacte »); the officers step back
D10 = st.dur('S10'); MAP10 = 0.85; PULSE10 = r(st.at('S10', 'L10', 5) + 0.05); BACK10 = r(PULSE10 + 0.35)
C10 = cam(0.0, [0.3, 1.6, 4.9], [0.25, 1.57, 4.45], [0.0, 1.38, 0.0], [0.0, 1.4, 0.0], lens=44)
LEG = [('legiste1', [-0.68, 0, 0.75], 35), ('legiste2', [0.68, 0, 0.75], -35)]
chkc('S10', C10, {'collar': SHP(0.5, 0.0), 'stain': SHP(0.5, 0.64), 'hem': SHP(0.5, 1.29), **{n: add(p, [0, 2.05, 0]) for n, p, ry in LEG}, 'post': [1.2, 1.0, 0.8], 'post2': [-1.2, 1.0, 0.8]})
def LEGK(n, p, ry, sd):
    face = {'lid': 0.35, 'mouth': 'line', 'brow': 0.2}
    hold = R5(add(SHP(0.5 - 0.6 * sd, 0.4), [0, 0.0, 0.15]), 1, 0.04)
    back = add(p, [r(-0.45 * sd), 0, 0.35])
    return [k(0.0, look=SHP(0.5, 0.6)), k(0.0, toon={'face': face}, toonDur=0.0),
            k(r(MAP10 - 0.15), toon={'reach': {'L' if sd > 0 else 'R': hold}, 'hands': {'L': 'open', 'R': 'open'}, 'face': face}, toonDur=0.2),
            k(r(PULSE10 - 0.02), toon={'reach': {'L' if sd > 0 else 'R': hold}, 'face': {'lid': 0.0, 'mouth': 'O', 'brow': 0.9}, 'sq': [0.96, 1.05, 0.96]}, toonDur=0.06, keepPose=True),
            k(BACK10, to=back, dur=0.32, clip='walk', ease='inOut'), k(BACK10, toon={'face': {'lid': 0.1, 'mouth': 'o', 'brow': 0.7}, 'sq': [1, 1, 1]}, toonDur=0.15),
            k(r(BACK10 + 0.3), look='camera', lookDur=0.12)]
st.shot('S10', 'grassland', setOpts=WHITESET, actors=[act(n, p, ry, 'stand', 'neutral', keys=LEGK(n, p, ry, -1 if p[0] < 0 else 1)) for n, p, ry in LEG],
        props=[*TOWN('S10', 'white', zmin=-40, zmax=8), SHIRT_RACK('portant10', stain='country', mapAt=MAP10, mapDur=0.5, mapPulse=PULSE10, sway=0.01),
               P('ruban10', 'tacheTape', pos=[0, 0, 0.05], opts={'w': 2.4, 'd': 1.5, 'runAt': [0.0, 0.7], 'open': True})],
        cams=[C10])
st.cue('sfx:zip', 'S10', 0.05, 0.3); st.cue('sfx:paper', 'S10', MAP10, 0.35); st.cue('sfx:ding', 'S10', PULSE10, 0.4)

# ============================== the press room
PRES = [0.0, 0, -2.45]
SIGN0 = [0.42, 0.55, -2.25]; SIGN1 = off(PRES, 0, 0.38, -0.5, 1.48)
# 11: a presidential decree forbids washing it. The president in his plain sash signs the decree on the lectern, then holds up on « interdit » a
#     crossed-out washing machine on a stick, at his shoulder, elbow bent (never a straight raised arm); flashes
D11 = st.dur('S11'); UP11 = r(st.at('S11', 'L11', 3) - 0.12)
C11 = cam(0.0, [-0.55, 1.95, 1.75], [-0.5, 1.93, 1.5], [0.35, 1.9, -2.5], [0.32, 1.92, -2.5], lens=42)
chkc('S11', C11, {'head': add(PRES, [0, 2.0, 0]), 'headTop': add(PRES, [0, 2.32, 0]), 'signTop': add(SIGN1, [0, 0.3 + 0.74, 0]), 'signC': add(SIGN1, [0, 0.3 + 0.37, 0]), 'decree': [0.0, 1.16, -2.05], 'title': [0.0, 3.1, -2.96]})
SPF = {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}
PEN = lambda dx: R5([r(0.02 + dx), 1.2, -2.02], 1, 0.03)
PRESK = [k(0.0, look=[0.0, 1.15, -2.05]), k(0.0, toon={'reach': {'R': PEN(0.0), 'L': R5([0.3, 1.13, -2.08], 1, 0.04)}, 'hands': {'R': 'pinch', 'L': 'open'}, 'bend': {'neck': [0.3, 0, 0, 1, None]}, 'face': SPF}, toonDur=0.0)]
for i in range(6): PRESK.append(k(r(0.12 + 0.11 * i), toon={'reach': {'R': PEN(0.04 * (i % 3) - 0.03)}}, toonDur=0.08, keepPose=True))
PRESK += [k(0.82, look='camera', lookDur=0.12), k(0.82, toon={'reach': {'R': R5([-0.28, 1.13, -2.08], 1, 0.04), 'L': R5([0.3, 1.13, -2.08], 1, 0.04)}, 'hands': {'R': 'open', 'L': 'open'}, 'bend': {'neck': [0.0, 0, 0, 1, None]}, 'face': SPF}, toonDur=0.15),
          *blink(1.0, SPF),
          k(UP11, toon={'reach': {'R': R5([-0.28, 1.13, -2.08], 1, 0.04), 'L': R5(add(SIGN1, [0, 0.12, 0]), 1, 0.05)}, 'hands': {'L': 'grip', 'R': 'open'}, 'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.1, 'mouth': 'bigsmile', 'brow': 0.7}}, toonDur=0.18, toonEase='out'),
          k(r(UP11 + 0.25), toon={'reach': {'R': R5([-0.28, 1.13, -2.08], 1, 0.04), 'L': R5(add(SIGN1, [0, 0.1, 0]), 1, 0.05)}, 'hands': {'L': 'grip', 'R': 'open'}, 'sq': [1, 1, 1], 'face': {'lid': 0.25, 'mouth': 'smile', 'brow': 0.5}}, toonDur=0.15),
          *blink(r(UP11 + 0.75), {'lid': 0.25, 'mouth': 'smile', 'brow': 0.5})]
st.shot('S11', 'pressRoom', setOpts={'backdrop': ' ', 'fg': 'rgba(0,0,0,0)', 'chairs': False, 'flags': False}, actors=[act('president', PRES, 0, 'podium', 'neutral', keys=PRESK)],
        props=[P('decret11', 'tacheDecree', pos=[0.02, 1.16, -2.06], opts={'signAt': 0.12, 'signDur': 0.66}),
               P('stylo11', 'marker', on={'actor': 'president', 'hand': 'R', 'offset': [0.0, -0.03, 0.03]}, keys=[k(0.82, visible=False)]),
               P('panneau11', 'tacheNoWashSign', pos=SIGN0, ry=-8, keys=[k(0.0, visible=False), k(r(UP11 - 0.02), visible=True), k(UP11, to=SIGN1, dur=0.18, ease='out'), k(r(UP11 + 0.25), to=add(SIGN1, [0, -0.02, 0]), dur=0.15)]),
               P('titre11', 'wallTitle', pos=[0.0, 3.1, -2.96], opts={'w': 1.9, 'h': 0.36, 'text': 'DÉCRET PRÉSIDENTIEL', 'bg': '#7A2E3A', 'fg': '#F4F1E8', 'rule': False, 'tick': True, 'emit': 0.3}),
               P('flash11a', 'camFlash', pos=[-0.9, 1.9, 0.3], opts={'w': 0.5, 'at': [r(UP11 + 0.1), r(UP11 + 0.55)]}),
               P('flash11b', 'camFlash', pos=[1.1, 1.8, 0.2], opts={'w': 0.5, 'at': [r(UP11 + 0.3)]}),
               P('flash11c', 'camFlash', pos=[0.9, 1.6, 0.5], opts={'w': 0.45, 'at': [0.4]})],
        cams=[C11])
st.cue('sfx:scratch', 'S11', 0.15, 0.2); st.cue('sfx:shutter', 'S11', r(UP11 + 0.1), 0.35); st.cue('sfx:shutter', 'S11', r(UP11 + 0.3), 0.3); st.cue('sfx:shutter', 'S11', r(UP11 + 0.55), 0.3)

# ============================== the palace roof (the terrace at y 8, the town's roofs below), the pole at the back
RY0 = 8.0
ROOF = [0.0, RY0, 0.0]
POLE = [0.0, RY0, -3.0]; PH = 6.0
def RP(x, z): return [x, RY0, z]
def ROOFP(pid, **o): return P(pid, 'tachePalaceRoof', pos=ROOF, opts={'w': 14, 'd': 10, 'lift': RY0, **o})
def POLEP(pid, **o): return P(pid, 'tachePole', pos=POLE, opts={'h': PH, 'y0': 1.6, 'y1': 5.0, **o})
SHY = lambda yh: RY0 + yh                                       # a hook height on the pole in the world
# 12: the shirt replaced the flag. Low on the palace roof: a soldier carries away a folded bundle of old cloth (never unfolded) while another hauls
#     on the halyard and the shirt on its hanger rises up the pole in front of it, the country-shaped stain on its chest (HISSÉE)
D12 = st.dur('S12'); CARD12 = r(st.at('S12', 'L12', 3) + 0.05)
C12 = cam(0.0, [1.3, RY0 + 1.0, 3.6], [1.2, RY0 + 1.0, 3.3], [0.0, RY0 + 3.6, -3.0], [0.0, RY0 + 3.8, -3.0], lens=52)
S1_12 = RP(-0.95, -2.4); S2_12 = RP(0.75, -2.55)
chkc('S12', C12, {'shirtStart': [0, SHY(1.6) - 0.6, -2.87], 'shirtEnd': [0, SHY(5.0) - 0.6, -2.87], 'hookEnd': [0, SHY(5.0), -2.87], 'hemEnd': [0, SHY(5.0) - 1.2, -2.87], 'ball': [0, RY0 + PH + 0.45, -3], 'sold1': add(S1_12, [0, 2.0, 0]), 'sold2': add(S2_12, [0, 2.0, 0])})
ROPE = lambda y: R5([0.07, RY0 + y, -2.9], 1, 0.03)
def HAUL():
    out = [k(0.0, look=[0, RY0 + 4.5, -2.9]), k(0.0, toon={'reach': {'R': ROPE(2.2), 'L': ROPE(1.7)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'clench', 'brow': -0.4}}, toonDur=0.0)]
    for i in range(6):
        t_ = r(0.15 + 0.24 * i); hi, lo = (2.3, 1.5) if i % 2 == 0 else (1.5, 2.3)
        out.append(k(t_, toon={'reach': {'R': ROPE(hi), 'L': ROPE(lo)}, 'sq': [1.03, 0.97, 1.03] if i % 2 else [0.98, 1.02, 0.98]}, toonDur=0.2, keepPose=True))
    return out + [k(1.75, look='camera', lookDur=0.15)]
BUND = off(S1_12, 115, 0.38, 0.0, 1.2)
st.shot('S12', 'grassland', setOpts={'clouds': 12}, actors=[
        act('soldat1', S1_12, 115, 'stand', 'neutral', keys=[k(0.0, look=add(BUND, [0, -0.1, 0])), k(0.0, toon={'reach': {'L': R5(off(S1_12, 115, 0.36, -0.22, 1.25), 1, 0.04), 'R': R5(off(S1_12, 115, 0.36, 0.22, 1.25), 1, 0.04)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': {'lid': 0.45, 'mouth': 'line'}}, toonDur=0.0),
                                                         k(0.5, to=RP(-3.2, -1.2), dur=1.5, clip='walk', ease='linear')]),
        act('soldat2', S2_12, -95, 'stand', 'neutral', keys=HAUL())],
        props=[ROOFP('toit12'), POLEP('mat12', hoistAt=0.1, hoistDur=1.5, shirt={'stain': 'country', 'sway': 0.04}), KEPI('kepi12a', 'soldat1'), KEPI('kepi12b', 'soldat2'),
               P('ballot12', 'tacheBundle', pos=add(BUND, [0, -0.12, 0]), ry=115, keys=[k(0.5, to=add(off(RP(-3.2, -1.2), 115, 0.38, 0.0, 1.2), [0, -0.12, 0]), dur=1.5, ease='linear')])],
        cams=[C12])
st.card('S12', 'HISSÉE', at=CARD12)
st.cue('sfx:squeak', 'S12', 0.2, 0.2); st.cue('sfx:squeak', 'S12', 0.7, 0.2); st.cue('sfx:fanfare', 'S12', r(CARD12 - 0.05), 0.3)

# 13: two guards salute it day and night. Low at the foot of the pole: two ceremonial guards (plumed helmets, epaulettes, sabres) salute, hand at
#     the brow, the shirt high above them; on « nuit » the sky snaps to night (a moon, stars) and they do not move; one blinks
D13 = st.dur('S13'); NIGHT13 = r(st.at('S13', 'L13', 4) - 0.05)
G13 = [('garde1', RP(-0.85, -2.1), 0), ('garde2', RP(0.85, -2.1), 0)]
C13 = cam(0.0, [0.3, RY0 + 1.2, 3.9], [0.28, RY0 + 1.15, 3.6], [0.0, RY0 + 3.3, -2.5], [0.0, RY0 + 3.35, -2.5], lens=52)
chkc('S13', C13, {**{n: add(p, [0, 2.0, 0]) for n, p, ry in G13}, **{n + 'Top': add(p, [0, 2.75, 0]) for n, p, ry in G13}, 'feet': RP(0.85, -2.1), 'shirtTop': [0, SHY(5.0), -2.87], 'shirtHem': [0, SHY(5.0) - 1.2, -2.87], 'moon': [4.0, RY0 + 9.0, -14.0]})
st.shot('S13', 'grassland', setOpts={'clouds': 12}, daynight={'from': NIGHT13, 'period': 0.24, 'once': True},
        actors=[act(n, p, ry, 'stand', 'determined', keys=saluting(p, ry, life=[*blink(r(0.55 + 0.3 * j), SAL_F), *blink(r(NIGHT13 + 0.4 + 0.12 * j), SAL_F)])) for j, (n, p, ry) in enumerate(G13)],
        props=[ROOFP('toit13'), POLEP('mat13', shirt={'stain': 'country', 'sway': 0.03}), *[x for j, (n, p, ry) in enumerate(G13) for x in (GUARD(f'casque13_{j}', n), EPAU(f'epau13_{j}', n), SABRE(f'sabre13_{j}', n))],
               P('lune13', 'moon', pos=[4.0, RY0 + 8.0, -14.0], opts={'radius': 1.0}, keys=[k(0.0, visible=False), k(r(NIGHT13 + 0.1), visible=True)]),
               P('etoiles13', 'stars', pos=[0, RY0, -3], opts={'count': 160, 'radius': 50}, keys=[k(0.0, visible=False), k(r(NIGHT13 + 0.1), visible=True)])],
        cams=[C13])
st.cue('sfx:crickets', 'S13', r(NIGHT13 + 0.05), 0.3)

# 14: the embassies officially recognised the stain. Wide and low under the pole: ambassadors in plain dark suits and plain sashes step up one after
#     another and sign the register on a table at its foot; two bandsmen play by the balustrade
D14 = st.dur('S14')
TAB14 = RP(0.75, -1.9)
AMB = [('ambassadeur1', RP(0.05, -1.25), RP(-1.1, -0.2), 0.12), ('ambassadeur2', RP(-0.8, -0.35), RP(0.05, -1.25), 0.85), ('ambassadeur3', RP(-1.6, 0.4), RP(-0.8, -0.35), 1.55)]
C14 = cam(0.0, [3.4, RY0 + 1.35, 5.6], [3.25, RY0 + 1.35, 5.3], [0.0, RY0 + 2.9, -2.4], [0.0, RY0 + 2.95, -2.4], lens=56)
chkc('S14', C14, {**{n: add(p, [0, 2.0, 0]) for n, p, q, t0 in AMB}, 'register': add(TAB14, [0, 1.05, 0]), 'shirtTop': [0, SHY(5.0), -2.87], 'shirtHem': [0, SHY(5.0) - 1.2, -2.87], 'band1': RP(1.45, -3.9), 'band2': RP(2.15, -3.6)})
def AMBK(p, q, t0, j):
    face = {'lid': 0.35, 'mouth': 'line', 'brow': 0.1}; sign = R5(add(TAB14, [-0.05, 1.08, 0.1]), 1, 0.04)
    ks = [k(0.0, look=add(TAB14, [0, 1.0, 0]) if j == 0 else [0, SHY(4.5), -2.9]), k(0.0, toon={'face': face}, toonDur=0.0)]
    if j == 0:
        ks += [k(0.1, toon={'reach': {'R': sign}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': face}, toonDur=0.15),
               *[k(r(0.28 + 0.09 * i), toon={'reach': {'R': R5(add(sign[:3], [0.04 * (i % 2), 0, 0]), 1, 0.04)}}, toonDur=0.07, keepPose=True) for i in range(4)],
               k(0.72, to=q, dur=0.5, clip='walk', ease='inOut'), k(0.72, toon={'face': face, 'bend': {'spine': [0, 0, 0, 1, None]}}, toonDur=0.15), k(1.1, look='camera', lookDur=0.15)]
    else:
        ks += [k(r(t0 - 0.62), to=add(TAB14, [-0.65, 0, 0.55]), dur=0.55, clip='walk', ease='inOut'), k(r(t0 - 0.05), look=add(TAB14, [0, 1.0, 0]), lookDur=0.12),
               k(t0, toon={'reach': {'R': sign}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': face}, toonDur=0.15),
               *[k(r(t0 + 0.18 + 0.09 * i), toon={'reach': {'R': R5(add(sign[:3], [0.04 * (i % 2), 0, 0]), 1, 0.04)}}, toonDur=0.07, keepPose=True) for i in range(4)]]
    return ks
BEAT14 = [r(0.1 + 0.42 * i) for i in range(6)]
st.shot('S14', 'grassland', setOpts={'clouds': 12}, actors=[
        *[act(n, p, yaw(p, TAB14), 'stand', 'neutral', keys=AMBK(p, q, t0, j)) for j, (n, p, q, t0) in enumerate(AMB)],
        act('musicien1', RP(1.45, -3.9), -30, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': R5(off(RP(1.45, -3.9), -30, 0.3, 0.12, 1.75), 1, 0.04), 'L': R5(off(RP(1.45, -3.9), -30, 0.3, -0.08, 1.75), 1, 0.04)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'puff'}}, toonDur=0.0), *[k(b_, toon={'sq': [1.03, 0.97, 1.03] if i_ % 2 else [0.98, 1.02, 0.98]}, toonDur=0.1, keepPose=True) for i_, b_ in enumerate(BEAT14)]]),
        act('musicien2', RP(2.15, -3.6), -45, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'puff'}}, toonDur=0.0), *[k(b_, toon={'sq': [1.04, 0.96, 1.04] if i_ % 2 else [0.97, 1.03, 0.97]}, toonDur=0.1, keepPose=True) for i_, b_ in enumerate(BEAT14)]])],
        props=[ROOFP('toit14'), POLEP('mat14', shirt={'stain': 'country', 'sway': 0.03}),
               P('table14', 'table', pos=TAB14, ry=-20, opts={'w': 1.0, 'd': 0.6, 'h': 1.0, 'color': '#7A2E3A'}), P('registre14', 'register', pos=add(TAB14, [0, 1.0, 0]), ry=-20, opts={'w': 0.6, 'h': 0.42}),
               P('trompette14', 'brass', on={'actor': 'musicien1', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}, opts={'kind': 'trumpet'}),
               P('tuba14', 'bandInstr', on={'actor': 'musicien2', 'joint': 'torso', 'offset': [0.0, 0.45, 0.1]}, opts={'kind': 'sousa', 'beat': BEAT14}),
               KEPI('kepi14a', 'musicien1'), KEPI('kepi14b', 'musicien2')],
        cams=[C14])
st.cue('sfx:fanfare', 'S14', 0.05, 0.35); st.cue('sfx:scratch', 'S14', 0.3, 0.15); st.cue('sfx:scratch', 'S14', r(AMB[1][3] + 0.2), 0.15); st.cue('sfx:scratch', 'S14', r(AMB[2][3] + 0.2), 0.15)

# 15: the shirt stays his. So does the upkeep. On the roof, medium close: two soldiers hand him (now in a pale blue shirt) a folded ironing board with
#     a form clipped on it and an iron; he holds them flatly; on « L'entretien » he glances at the iron, then at us, and blinks
D15 = st.dur('S15'); GIVE15 = r(st.at('S15', 'L15', 4) - 0.1); LOOK15 = r(st.at('S15', 'L15', 6) + 0.05)
ME15 = RP(0.0, 0.0)
SB = RP(0.7, -0.4); SI = RP(-0.72, -0.4)
BOARD0 = RP(0.62, 0.42); BOARD1 = RP(0.42, 0.3)
C15 = cam(0.0, [0.3, RY0 + 1.75, 3.25], [0.28, RY0 + 1.73, 3.0], [0.0, RY0 + 1.55, 0.0], [0.0, RY0 + 1.56, 0.0], lens=46)
chkc('S15', C15, {'head': add(ME15, [0, 2.0, 0]), 'headTop': add(ME15, [0, 2.32, 0]), 'boardTop': add(BOARD1, [0, 1.42, 0]), 'boardLow': add(BOARD1, [0, 0.6, 0]), 'iron': off(ME15, 0, 0.35, 0.3, 1.0), 'soldB': add(SB, [0, 2.0, 0]), 'soldI': add(SI, [0, 2.0, 0])})
MF = {'lid': 0.45, 'mouth': 'line', 'brow': -0.1}
IRONH = R5(off(ME15, 0, 0.32, 0.26, 1.05), 1, 0.04)
HERO15 = [k(0.0, look=add(SB, [0, 1.9, 0])), k(0.0, toon={'face': MF}, toonDur=0.0), k(0.5, look=add(SI, [0, 1.9, 0]), lookDur=0.15), k(r(GIVE15 - 0.1), look='camera', lookDur=0.12),
          k(GIVE15, toon={'reach': {'L': R5(add(BOARD1, [-0.05, 1.3, 0.05]), 1, 0.04), 'R': IRONH}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': MF, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.15),
          k(r(GIVE15 + 0.2), toon={'reach': {'L': R5(add(BOARD1, [-0.05, 1.3, 0.05]), 1, 0.04), 'R': IRONH}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': MF, 'sq': [1, 1, 1]}, toonDur=0.12),
          k(LOOK15, look=add(IRONH[:3], [0, -0.1, 0.1]), lookDur=0.12), k(r(LOOK15 + 0.35), look='camera', lookDur=0.12), *blink(r(LOOK15 + 0.6), MF)]
def SOLDK(p, ry, item, sd):
    hold = R5(off(p, ry, 0.42, 0.0, 1.15), 1, 0.04)
    return [k(0.0, look=add(ME15, [0, 2.0, 0])), k(0.0, toon={'reach': {'R' if sd < 0 else 'L': hold}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.0),
            k(r(GIVE15 + 0.25), to=add(p, [r(0.4 * sd), 0, 0.15]), dur=0.4, clip='walk', ease='inOut'), k(r(GIVE15 + 0.25), toon={'face': {'lid': 0.4, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.15)]
st.shot('S15', 'grassland', setOpts={'clouds': 12}, actors=[
        act('mecB', ME15, 0, 'stand', 'unimpressed', keys=HERO15),
        act('soldat1', SB, -60, 'stand', 'neutral', keys=SOLDK(SB, -60, 'board', 1)), act('soldat2', SI, 60, 'stand', 'neutral', keys=SOLDK(SI, 60, 'iron', -1))],
        props=[ROOFP('toit15'), FRONT('chemise15', 'mecB', stain='none', bg='#BFD7EA'), KEPI('kepi15a', 'soldat1'), KEPI('kepi15b', 'soldat2'),
               P('planche15', 'tacheBoard', pos=BOARD0, rot=[0, PI / 2, PI / 2], opts={'folded': True, 'form': True, 'formX': 0.32}, keys=[k(r(GIVE15 - 0.12), to=BOARD1, dur=0.2, ease='inOut')]),
               P('fer15s', 'tacheIron', on={'actor': 'soldat2', 'hand': 'R', 'offset': [0.0, -0.06, 0.05]}, scale=1.6, keys=[k(GIVE15, visible=False)]),
               P('fer15', 'tacheIron', on={'actor': 'mecB', 'hand': 'R', 'offset': [0.0, -0.06, 0.05]}, scale=1.6, opts={'steamAt': [r(LOOK15 + 0.05)]}, keys=[k(0.0, visible=False), k(GIVE15, visible=True)])],
        cams=[C15])
st.cue('clack', 'S15', GIVE15, 0.3); st.cue('sfx:sniff', 'S15', r(LOOK15 + 0.1), 0.2)

# 16: he irons around the stain. The payoff's own camera, static and close at dawn on the roof: he irons the shirt laid on the board, steering the
#     iron carefully round the country-shaped stain (the iron loops past it, never on it); the two guards salute behind him; a look to us at the end
D16 = st.dur('S16')
ME16 = RP(0.15, -0.62); BRD = RP(0.0, 0.0); BH = 0.95
SHS = 1.0; SHO = [-0.35, RY0 + BH + 0.045, 0.0]                   # the shirt laid on the board: collar at SHO, the torso along +x
def ONSH(u, v): return [r(SHO[0] + (0.13 + 0.62 * v) * SHS), r(SHO[1] + 0.03), r((u - 0.5) * 0.62 * SHS)]   # a point on the laid shirt (u across, v in widths from the shoulders)
SC16 = ONSH(0.5, 0.64)
LOOP = [ONSH(0.08, 0.2), ONSH(0.15, 0.95), ONSH(0.5, 1.12), ONSH(0.88, 0.95), ONSH(0.92, 0.25), ONSH(0.5, 0.12), ONSH(0.1, 0.25), ONSH(0.15, 0.9)]
G16 = [('garde1', RP(-1.3, -2.7), 0), ('garde2', RP(0.5, -3.0), 0)]
C16 = cam(0.0, [1.15, RY0 + 2.35, 3.15], [1.12, RY0 + 2.33, 3.05], [0.05, RY0 + 1.25, -0.4], [0.05, RY0 + 1.25, -0.4], lens=48)
chkc('S16', C16, {'head': add(ME16, [0, 2.0, 0]), 'headTop': add(ME16, [0, 2.32, 0]), 'stain': SC16, 'collar': ONSH(0.5, 0.0), 'hem': ONSH(0.5, 1.29), **{n: add(p, [0, 2.0, 0]) for n, p, ry in G16}, **{n + 'Top': add(p, [0, 2.75, 0]) for n, p, ry in G16}, 'boardEnd': [0.7, RY0 + BH, 0]})
T16 = [0.15, 0.55, 0.9, 1.25, 1.6, 1.95, 2.25, 2.55]
IRON_Y = 0.0
def iron_at(p): return [p[0], r(p[1] + IRON_Y), p[2]]
HANDI = lambda p: R5([p[0], r(p[1] + 0.2), r(p[2] - 0.02)], 1, 0.04)
DF = {'lid': 0.5, 'mouth': 'line', 'brow': 0.1}
HERO16 = [k(0.0, look=SC16), k(0.0, toon={'reach': {'R': HANDI(LOOP[0])}, 'touch': {'L': ['torso', 0.25, 0.1, 0.12, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'open'}, 'bend': {'spine': [0.25, 0, 0, 1, None], 'neck': [0.25, 0, 0, 1, None]}, 'face': DF}, toonDur=0.0)]
for i, t_ in enumerate(T16[1:], 1):
    HERO16.append(k(t_, toon={'reach': {'R': HANDI(LOOP[i])}}, toonDur=r(T16[i] - T16[i - 1]), keepPose=True))
HERO16 += [k(r(D16 - 0.55), look='camera', lookDur=0.15), *blink(r(D16 - 0.35), DF)]
IRONK = [k(T16[i], to=iron_at(LOOP[i]), dur=r(T16[i] - T16[i - 1]), ease='inOut') for i in range(1, len(T16))]
st.shot('S16', 'grassland', setOpts={'clouds': 12, 'sky': ['#E9A48E', '#FBD7B0']}, look={'sunDir': [0.75, 0.2, 0.62], 'sunColor': '#FFB27A', 'fill': 1.15},
        actors=[act('mecB', ME16, 0, 'stand', 'unimpressed', keys=HERO16),
                *[act(n, p, ry, 'stand', 'determined', keys=saluting(p, ry, life=[*blink(r(1.1 + 0.5 * j), SAL_F), *blink(r(2.3 + 0.2 * j), SAL_F)])) for j, (n, p, ry) in enumerate(G16)]],
        props=[ROOFP('toit16'), P('mat16', 'tachePole', pos=POLE, opts={'h': PH, 'y0': -9.0, 'y1': -9.0, 'shirt': {'stain': 'none'}}), FRONT('chemise16', 'mecB', stain='none', bg='#BFD7EA'),
               *[x for j, (n, p, ry) in enumerate(G16) for x in (GUARD(f'casque16_{j}', n), EPAU(f'epau16_{j}', n), SABRE(f'sabre16_{j}', n))],
               P('planche16', 'tacheBoard', pos=BRD, opts={'h': BH}),
               P('chemise16b', 'tacheHangShirt', pos=SHO, rot=[-PI / 2, PI / 2, 0], rotOrder='YXZ', opts={'s': SHS, 'stain': 'country', 'flat': True}),
               P('fer16', 'tacheIron', pos=iron_at(LOOP[0]), ry=90, scale=1.5, opts={'steamAt': [0.6, 1.4, 2.2]}, keys=IRONK)],
        cams=[C16])
for t_ in [0.55, 1.25, 1.95]: st.cue('sfx:stretch', 'S16', t_, 0.12)
st.cue('sfx:tick', 'S16', r(D16 - 0.35), 0.2)

print('\n'.join(CHECKS))

TOON = {'breathe': 1.7, 'holdLife': 1.6}
MEC = {'preset': 'lemec', 'atlasBody': False, 'outfit': 'suit', 'suit': '#F4F2EC', 'pants': '#2B3550', 'shirt': '#F4F2EC', 'lapel': '#F4F2EC', 'tie': '#F4F2EC', 'cuff': '#F4F2EC',
       'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': TOON}
CRSC = {'preset': 'boss', 'outfit': 'suit', 'facial': 'none', 'suit': '#4C5058', 'pants': '#3E4148', 'shirt': '#4C5058', 'lapel': '#3E4148', 'tie': '#2E3036', 'cuff': '#4C5058', 'hat': 'none', 'glasses': False, 'gloves': '#1A1B1E', 'build': {'width': 1.12, 'headWidth': 1.2}, 'toon': EX}
SOLD = {'preset': 'boss', 'outfit': 'suit', 'facial': 'none', 'suit': '#556140', 'pants': '#4A5538', 'shirt': '#C9C2A8', 'lapel': '#4A5538', 'tie': '#3A4230', 'cuff': '#556140', 'hat': 'none', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
GARD = {'preset': 'cop', 'outfit': 'suit', 'suit': '#1E2A44', 'pants': '#F2F0EA', 'shirt': '#F2F0EA', 'lapel': '#1E2A44', 'tie': '#1E2A44', 'cuff': '#1E2A44', 'hat': 'none', 'hair': 'crew', 'facial': 'none', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
st.write("La tache", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'mecB': {**MEC, 'suit': '#BFD7EA', 'shirt': '#BFD7EA', 'lapel': '#BFD7EA', 'tie': '#BFD7EA', 'cuff': '#BFD7EA'},
    'juge': {'preset': 'judge', 'facial': 'stubble', 'seed': 931, 'build': {'width': 0.86, 'headWidth': 1.3, 'headScale': 1.05}},
    **{f'crs{i + 1}': {**CRSC, 'seed': 940 + i, 'facial': 'mustache' if i % 2 else 'none'} for i in range(5)},
    'maire': {'preset': 'politique', 'seed': 950, 'suit': '#F2F2EE', 'pants': '#F2F2EE', 'shirt': '#FFFFFF', 'lapel': '#F2F2EE', 'tie': '#F2F2EE', 'cuff': '#F2F2EE', 'skin': '#F1EFEA', 'hair': 'receding', 'hairColor': '#F4F4F2',
              'facial': 'mustache', 'beardColor': '#E8E8E4', 'glasses': False, 'sash': ['#FFFFFF'], 'sashW': 0.11, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.12}, 'toon': EX},
    'legiste1': {'preset': 'doctor', 'seed': 951, 'suit': '#E6EEF4', 'pants': '#E6EEF4', 'shirt': '#E6EEF4', 'lapel': '#D4DEE6', 'tie': '#5C8FB8', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'legiste2': {'preset': 'doctor', 'seed': 952, 'suit': '#E6EEF4', 'pants': '#E6EEF4', 'shirt': '#E6EEF4', 'lapel': '#D4DEE6', 'tie': '#5C8FB8', 'glasses': False, 'hair': 'bun', 'lipstick': True, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'president': {'preset': 'politique', 'seed': 953, 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#7A2333', 'hairColor': '#BDBDBD', 'sash': ['#C9A23A'], 'sashW': 0.11, 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.06}, 'toon': EX},
    'soldat1': {**SOLD, 'seed': 960}, 'soldat2': {**SOLD, 'seed': 961, 'facial': 'mustache'},
    'garde1': {**GARD, 'seed': 962}, 'garde2': {**GARD, 'seed': 963, 'facial': 'mustache'},
    'ambassadeur1': {'preset': 'politique', 'seed': 964, 'suit': '#23262C', 'lapel': '#23262C', 'tie': '#3A3D44', 'sash': ['#6A2E5A'], 'sashW': 0.1, 'hairColor': '#2A2420', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'ambassadeur2': {'preset': 'madame', 'seed': 965, 'suit': '#2A2D36', 'sash': ['#2E6B4A'], 'sashW': 0.1, 'glasses': False, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'ambassadeur3': {'preset': 'politique', 'seed': 966, 'suit': '#1F2430', 'lapel': '#1F2430', 'tie': '#3A3D44', 'sash': ['#2C4F86'], 'sashW': 0.1, 'skin': '#8A5A3A', 'faceRim': True, 'hairColor': '#1B1B1E', 'glasses': True, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'musicien1': {**SOLD, 'seed': 967, 'suit': '#7A2E3A', 'pants': '#1E2A44', 'lapel': '#1E2A44', 'cuff': '#E2B53C'}, 'musicien2': {**SOLD, 'seed': 968, 'suit': '#7A2E3A', 'pants': '#1E2A44', 'lapel': '#1E2A44', 'cuff': '#E2B53C', 'facial': 'mustache'},
})
