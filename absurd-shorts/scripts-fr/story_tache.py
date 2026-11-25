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
# (round 2) a moving hold: slow breathing (the chest rises and settles), the face carried on every key (a keepPose key drops the face), blinks
#     (two frames shut) and an optional chin lift; breath keys stay clear of the blinks so a breath never reopens the eyes
def life(t0, t1, face, ph=0.0, blinks=(), chin=None, period=0.9, amp=0.013):
    out, bl, t_, i = [], sorted(blinks), t0 + ph, 0
    while t_ < t1 - 0.1:
        if not any(-0.04 < t_ - b < 0.2 for b in bl):
            q = [r(1 - amp * 0.4, 4), r(1 + amp, 4), r(1 - amp * 0.4, 4)] if i % 2 == 0 else [r(1 + amp * 0.3, 4), r(1 - amp * 0.6, 4), r(1 + amp * 0.3, 4)]
            tn = {'sq': q, 'face': face}
            if chin and chin[0] <= t_ < chin[1]: tn['bend'] = {'neck': [-0.09, 0, 0, 1, None]}
            elif chin: tn['bend'] = {'neck': [0.0, 0, 0, 1, None]}
            out.append(k(r(t_), toon=tn, toonDur=r(period * 0.8), toonEase='inOut', keepPose=True))
        t_ += period / 2; i += 1
    for b in bl: out += blink(r(b), face)
    return out
def R5(p, w=1, s=0.04): return [*p, w, s]
def FRONT(pid, who, **o): return P(pid, 'tacheShirtFront', on={'actor': who, 'joint': 'torso', 'offset': [0.0, -0.1, 0.135]}, opts={'h': 0.73, 'w': 0.37, 'at': [0.34, 0.42], 'countryAt': [0.5, 0.52], **o})
def VISOR(pid, who): return P(pid, 'visorHelmet', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.0, 0.0]})
def KEPI(pid, who): return P(pid, 'kepi', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'w': 0.222, 'd': 0.17, 'color': '#4E5A3A', 'band': '#2E3424'})
# (round 2) the gold helmet with a living plume (props_tache.js tacheGuardHelmet: it quivers all the time)
def GUARD(pid, who, ph=0.0): return P(pid, 'tacheGuardHelmet', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}, scale=1.1, opts={'phase': ph, 'quiver': 0.08})
def EPAU(pid, who): return P(pid, 'epaulettes', on={'actor': who, 'joint': 'torso', 'offset': [0.0, 0.635, 0.0]}, opts={'w': 0.58})
def SABRE(pid, who): return P(pid, 'sabre', on={'actor': who, 'joint': 'torso', 'offset': [0.26, 0.02, 0.15]})
# (round 1) the salute rides on the face: fingertips at the brim on his right temple, a hand's breadth in front of the face and outside its edge,
#     the elbow out to his right; it follows the head through every idle shift, so the hand never sinks into the head mesh (S13, S16)
SAL_T = ['face', -0.5, 0.9, 0.09, 1, 0.1, [-1.0, 0.45, 0.3]]
SAL_F = {'lid': 0.35, 'mouth': 'line', 'brow': -0.3}
def saluting(p, ry, t0=0.0, life=()):
    return [k(0.0, look='camera'), k(0.0, toon={'touch': {'R': SAL_T}, 'hands': {'R': 'open'}, 'face': SAL_F}, toonDur=0.0), *life]

for g_ in [('S01', 1.2, 'mec', 'splat'), ('S02', 1.45, 'mec', 'sponge'), ('S08', 2.12, 'maire', 'white mayor'), ('S15', 1.95, 'mecB', 'upkeep'), ('S16', 2.2, 'mecB', 'ironing')]:
    st.gag(*g_)

# ============================== his kitchen (kitchenDay: the back wall at z -3.4)
KIT = {'fridge': False}
# (round 2) moved 0.95 m to the right: the kitchen's hanging lamp (0, 2.7, -1.0) hid the top of his stretched head
ME1 = [0.95, 0, -1.2]; RY1 = 14
STAIN1 = off(ME1, RY1, 0.16, 0.085, 1.31)                      # the splat's centre on his chest (u 0.34, v 0.5 of the shirt front)
# 1: the hook. Close and frontal at his counter: he lifts a forkful of spaghetti, a glob drops and a small irregular splat with a pasta strand
#    lands on his white shirt on « tache »; he looks down at it, then at us; a slow push in to the stain, his face kept in the frame
# (round 3) the glob falls for 0.24 s (7 frames at 30 fps) on a gravity curve, stretched long as it speeds up, and splats flat on the chest (the
#     stain pops in with an overshoot); his eyes stay on the fork for two frames after it lets go, then lead the head down
D1 = st.dur('S01'); LAND1 = r(st.at('S01', 'L01', 5) - 0.02); DROP1 = r(LAND1 - 0.24)
CHECKS.append(f"S01 drop {DROP1} land {LAND1} (« {st.L['L01']['words'][5]['w']} »)")
C1 = cam(0.0, off(ME1, RY1, 2.95, -0.35, 1.74), off(ME1, RY1, 2.45, -0.27, 1.68), off(ME1, RY1, 0.0, 0.0, 1.6), off(ME1, RY1, 0.0, 0.02, 1.53), lens=40, ease='inOut')
# (round 2) the take gets its own framing: the camera eases back and tilts up for the full stretch (the head top left the frame), then glides
#     back into the push-in on the stain once he looks at us
TKF1 = r(LAND1 + 0.05 - 0.04)
C1T = glide([cam(TKF1, off(ME1, RY1, 3.15, -0.3, 1.86), off(ME1, RY1, 3.12, -0.3, 1.86), off(ME1, RY1, 0.0, 0.0, 1.9), off(ME1, RY1, 0.0, 0.0, 1.9), lens=40)], 0.12)
C1E = glide([cam(1.42, off(ME1, RY1, 2.62, -0.29, 1.7), off(ME1, RY1, 2.45, -0.27, 1.68), off(ME1, RY1, 0.0, 0.01, 1.56), off(ME1, RY1, 0.0, 0.02, 1.53), lens=40, ease='out')], 0.3)
chk('S01@takecam', C1T['from'], C1T['lookAt'], 40, {'takeTop': off(ME1, RY1, 0, 0, 2.75), 'jawLow': off(ME1, RY1, 0.17, 0, 1.6), 'stain': STAIN1, 'hem': off(ME1, RY1, 0.16, 0, 1.05)})
chkc('S01', C1, {'headTop': off(ME1, RY1, 0, 0, 2.3), 'eyes': off(ME1, RY1, 0.17, 0, 2.05), 'stain': STAIN1, 'pocket': off(ME1, RY1, 0.16, -0.06, 1.47), 'plate': off(ME1, RY1, 0.55, 0.05, 1.03)})
chkc('S01', C1, {'headTop': off(ME1, RY1, 0, 0, 2.3), 'eyes': off(ME1, RY1, 0.17, 0, 2.05), 'stain': STAIN1, 'hem': off(ME1, RY1, 0.16, 0, 1.05)}, end=True)
chk('S01@take', C1['from'], C1['lookAt'], 40, {'takeTop': off(ME1, RY1, 0, 0, 2.62), 'jaw': off(ME1, RY1, 0.17, 0, 1.78)})
FORKUP = R5(off(ME1, RY1, 0.36, 0.13, 1.62), 1, 0.05); FORKAWAY = R5(off(ME1, RY1, 0.36, 0.46, 1.62), 1, 0.05); FORKOUT = R5(off(ME1, RY1, 0.42, 0.36, 1.22), 1, 0.05); FORKDN = R5(off(ME1, RY1, 0.5, 0.12, 1.12), 1, 0.05)
EAT = {'lid': 0.2, 'mouth': 'O', 'jaw': 0.35, 'brow': 0.3}
# (round 1) the take on the splat: two frames of brace, then the body stretched up, the neck drawn out long, the head long and thin and the jaw
#     dropped to the collar, held trembling 0.3 s (the hang time), an overshoot and the settle; the jaw take is this film's own (the eyes on stalks
#     are kept for the mayor's double take in S08)
TK1 = r(LAND1 + 0.05)
HOLD1 = {'reach': {'R': FORKOUT}, 'hands': {'R': 'grip'}}
JAW1 = {**HOLD1, 'sq': [0.92, 1.09, 0.92], 'scl': {'head': [0.88, 1.16, 1.0]}, 'bend': {'neck': [0.1, 0, 0, 1.55, None]},
        'face': {'lid': 0.0, 'eye': 0.45, 'gy': 0.8, 'jaw': 1.0, 'jawLen': 1.7, 'jawBlock': 1, 'jawFwd': 0.4, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}}
HERO1 = [k(0.0, look=add(FORKUP[:3], [0, 0.1, 0])), k(0.0, toon={'reach': {'R': FORKDN}, 'hands': {'R': 'grip', 'L': 'open'}, 'face': {'lid': 0.3, 'mouth': 'smile'}}, toonDur=0.0),
         k(0.12, toon={'reach': {'R': FORKUP}, 'hands': {'R': 'grip'}, 'face': EAT, 'sq': [0.97, 1.03, 0.97]}, toonDur=0.32, toonEase='inOut'),
         k(0.5, toon={'reach': {'R': R5(add(FORKUP[:3], [0, 0.03, -0.02]), 1, 0.05)}, 'hands': {'R': 'grip'}, 'face': {**EAT, 'jaw': 0.5}, 'sq': [1, 1, 1]}, toonDur=0.12),
         # the fork hand jerks up and out as the glob lets go, so the forearm clears the fall in front of his chest
         k(DROP1, toon={'reach': {'R': FORKAWAY}, 'hands': {'R': 'grip'}, 'face': {**EAT, 'jaw': 0.5}}, toonDur=0.1, toonEase='out', keepPose=True),
         k(r(DROP1 + 0.067), toon={'face': {**EAT, 'jaw': 0.5, 'gy': 0.75, 'brow': 0.5}}, toonDur=0.04, keepPose=True),
         k(r(DROP1 + 0.1), look=STAIN1, lookDur=0.12), k(r(TK1 - 0.04), look=off(ME1, RY1, 1.3, 0.0, 1.55), lookDur=0.05),
         *beat(TK1, JAW1, antic={**HOLD1, 'sq': [1.1, 0.87, 1.1], 'scl': {'head': [1.12, 0.88, 1.0]}, 'face': {'lid': 0.7, 'mouth': 'clench', 'brow': -0.5}}, hold=0.3,
               over={**HOLD1, 'sq': [1.04, 0.97, 1.04], 'face': {'lid': 0.1, 'mouth': 'o', 'jaw': 0.3, 'brow': 0.8}}, settle={**HOLD1, 'face': {'lid': 0.1, 'mouth': 'o', 'jaw': 0.15, 'brow': 0.7}}, settle_f=5),
         k(1.42, look='camera', lookDur=0.12), k(1.42, toon={'reach': {'R': FORKOUT}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.14),
         *blink(1.72, {'lid': 0.45, 'mouth': 'line', 'brow': -0.1})]
GLOB0 = off(ME1, RY1, 0.36, 0.11, 1.78)
GEND1 = add(STAIN1, [0, 0.03, 0.03]); FALL1 = r(LAND1 - DROP1)
GLOBK1 = [k(0.0, visible=False), k(DROP1, visible=True), k(DROP1, squash=[0.85, 1.25, 0.85], dur=4.0)]
for i_ in range(4):
    u0_, u1_ = i_ / 4, (i_ + 1) / 4
    GLOBK1.append(k(r(DROP1 + FALL1 * u0_), to=[r(GLOB0[j] + (GEND1[j] - GLOB0[j]) * u1_ * u1_) for j in range(3)], dur=r(FALL1 / 4), ease='linear'))
GLOBK1 += [k(r(DROP1 + 0.09), squash=[0.78, 1.45, 0.78], dur=4.0), k(r(DROP1 + 0.17), squash=[0.68, 1.7, 0.68], dur=4.0),
           k(LAND1, squash=[1.6, 1.25, 0.3], dur=2.0), k(r(LAND1 + 0.04), visible=False)]
st.shot('S01', 'kitchenDay', setOpts=KIT, actors=[act('mec', ME1, RY1, 'stand', 'neutral', keys=HERO1)],
        props=[FRONT('chemise1', 'mec', stainAt=LAND1),
               P('comptoir1', 'table', pos=off(ME1, RY1, 0.62, 0, 0), ry=RY1, opts={'w': 1.5, 'd': 0.6, 'h': 1.0, 'color': '#E8A97E'}),
               P('assiette1', 'tachePastaPlate', pos=off(ME1, RY1, 0.55, 0.05, 1.0), ry=RY1, opts={'s': 1.2}),
               P('fourchette1', 'tacheFork', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.02, 0.04], 'face': 'camera'}, opts={'s': 1.5, 'emptyAt': DROP1}),
               P('miette1', 'tachePastaGlob', pos=GLOB0, opts={'s': 1.6}, keys=GLOBK1)],
        cams=[C1, C1T, C1E])
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
# (round 1) the scrub speeds up: strokes from 0.15 s apart down to 0.045 s, each one pressing the sponge flat against his chest (the hand squashed,
#     the body squashed) or dragging it away long (the hand and the arm drawn out, the body stretched), wider and harder each time
SCRUB2 = lambda f, dx, dy=0.0: R5(off(ME2, RY2, f, 0.085 + dx, 1.31 + dy), 1, 0.04)
STROKES2 = []
t_, dt_ = 0.04, 0.15
while t_ < BREAK2 - 0.05:
    STROKES2.append(r(t_)); t_ += dt_; dt_ = max(0.045, dt_ * 0.82)
HERO2 = [k(0.0, look=STAIN2), k(0.0, toon={'reach': {'R': SCRUB(0.0)}, 'touch': {'L': ['torso', 0.22, 0.05, 0.12, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'open'}, 'bend': {'neck': [0.3, 0, 0, 1, None]}, 'face': EFF}, toonDur=0.0)]
for i, t_ in enumerate(STROKES2):
    a_ = 0.4 + 0.6 * i / max(1, len(STROKES2) - 1); press = i % 2 == 0; d_ = r((STROKES2[i + 1] if i + 1 < len(STROKES2) else BREAK2) - t_)
    HERO2.append(k(t_, toon={'reach': {'R': SCRUB2(0.16, -0.07 * a_, -0.03 * a_) if press else SCRUB2(0.24 + 0.3 * a_, 0.1 * a_, 0.06 * a_)}, 'hose': 0.1,
                              'sq': [1 + 0.08 * a_, 1 - 0.09 * a_, 1 + 0.08 * a_] if press else [1 - 0.05 * a_, 1 + 0.07 * a_, 1 - 0.05 * a_],
                              'scl': {'handR': [1 + 0.35 * a_, 1 - 0.3 * a_, 1 + 0.35 * a_] if press else [1 - 0.2 * a_, 1 + 0.4 * a_, 1 - 0.2 * a_]},
                              'face': {**EFF, 'lid': 0.55 + 0.3 * a_, 'brow': -0.7 - 0.3 * a_, 'mouth': 'clench' if press else 'grimace'}}, toonDur=r(min(0.07, d_ * 0.7)), toonEase='out', keepPose=True))
HERO2 += [k(BREAK2, toon={'reach': {'R': R5(off(ME2, RY2, 0.34, 0.12, 1.36), 1, 0.05)}, 'hands': {'R': 'spread'}, 'sq': [1.05, 0.95, 1.05], 'scl': {'handR': [1.15, 1.15, 1.15]}, 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'o', 'brow': 0.8}}, toonDur=0.06, toonEase='out', keepPose=True),
          k(r(BREAK2 + 0.12), toon={'sq': [1, 1, 1], 'scl': {'handR': [1, 1, 1]}}, toonDur=0.15, keepPose=True),
          k(r(BREAK2 + 0.04), look=off(ME2, RY2, 0.34, 0.12, 1.36), lookDur=0.08),
          k(r(BREAK2 + 0.42), look='camera', lookDur=0.12), k(r(BREAK2 + 0.42), toon={'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.12, keepPose=True)]
st.shot('S02', 'salleDeBain', setOpts={'half': 3.4}, actors=[act('mec', ME2, RY2, 'stand', 'neutral', keys=HERO2)],
        props=[FRONT('chemise2', 'mec'), P('eponge2', 'tacheSponge', on={'actor': 'mec', 'hand': 'R', 'offset': [0.0, -0.05, 0.05]}, opts={'s': 1.0, 'breakAt': BREAK2, 'hang': 0.24, 'strokes': [[t_, 1 if i % 2 == 0 else -1] for i, t_ in enumerate(STROKES2)]})],
        cams=[C2])
for t_ in STROKES2[::2]: st.cue('sfx:scratch', 'S02', t_, 0.16)
CHECKS.append(f'S02 strokes {STROKES2} break {BREAK2}')
st.cue('sfx:crunch', 'S02', BREAK2, 0.4)

# ============================== the court (replicaCourt: the judge's bench at z -14)
JG = [-0.35, -0.3, -14.0]; RYJ = 0
RACK3 = [0.45, 0, -11.6]; RYR3 = 200
# 3: the judge signed its eviction. Over the shirt's shoulder (it hangs on a rack in the dock, facing the bench): the judge strikes the gavel on
#    « signé »; reverse on the shirt's front: the eviction order pops up beside it and is stamped EXPULSÉE on « expulsion »
D3 = st.dur('S03'); HIT3 = r(st.at('S03', 'L03', 3) + 0.04); CUT3 = 0.92; STAMP3 = r(st.at('S03', 'L03', 5) + 0.02)
# (round 2) the judge large and clear of the shirt: the camera close behind the shirt's left shoulder, the shirt a sliver at the right edge,
#     the judge in the middle with room above him for the raised gavel
F3A = [-0.7, 1.7, -10.0]; L3A = [-0.2, 1.8, -14.0]; LENS3A = 44
C3A = cam(0.0, F3A, add(F3A, [0.0, 0.0, -0.12]), L3A, add(L3A, [0, -0.02, 0]), lens=LENS3A)
GV_REST = R5([0.05, 1.45, -13.45], 1, 0.04); GV_UP = R5([-0.05, 2.5, -13.85], 1, 0.04); GV_HIT = R5([0.08, 1.33, -13.32], 1, 0.04)
chk('S03a', F3A, L3A, LENS3A, {'jtop': add(JG, [0, 2.5, 0]), 'raised': [-0.05, 2.8, -13.85], 'block': [0.1, 1.18, -13.3], 'jL': add(JG, [-0.45, 1.7, 0]), 'jR': add(JG, [0.5, 1.7, 0]), 'shL': add(RACK3, [-0.31, 1.5, 0]), 'sleeve': add(RACK3, [-0.45, 1.2, 0])})
ORDER3 = off(RACK3, RYR3, 0.2, -0.58, 1.12)
OYAW3 = yaw(ORDER3, [-2.05, 1.5, -13.55])
F3B = [-2.05, 1.5, -13.55]
# (round 2) the whole shirt in frame on the reverse: its sleeve tips (they flare out, and jump on the stamp) are part of the fit
L3B, LENS3B, W3B = fit(F3B, {'collarL': add(RACK3, [0.33, 1.88, 0]), 'collarR': add(RACK3, [-0.33, 1.88, 0]), 'hem': add(RACK3, [0, 1.05, 0]), 'orderTL': off(ORDER3, OYAW3, 0, 0.24, 0.62), 'orderBR': off(ORDER3, OYAW3, 0, -0.24, 0.0),
                         'sleeveL': off(RACK3, RYR3, 0.0, 0.62, 1.3), 'sleeveR': off(RACK3, RYR3, 0.0, -0.62, 1.3), 'hookTop': add(RACK3, [0, 2.12, 0])}, margin=0.05, top=0.19, bottom=0.76, lenses=range(30, 72))
C3B = cam(CUT3, F3B, add(F3B, [0.0, 0.0, 0.15]), L3B, L3B, lens=LENS3B)
CHECKS.append(f'S03b fit lens {LENS3B} {W3B}')
chkc('S03b', C3B, {'stain': off(RACK3, RYR3, 0.05, -0.1, 1.5), 'collar': add(RACK3, [0, 1.85, 0]), 'hem': add(RACK3, [0, 1.07, 0]), 'orderTop': add(ORDER3, [0, 0.82, 0]), 'orderL': add(ORDER3, [-0.31, 0.4, 0]), 'orderR': add(ORDER3, [0.31, 0.4, 0])})
# (round 2) the gavel: a raise with the body stretched and leaning back (anticipation, a short hang up there), a strike in two frames with three
#     ghost gavels along the arc (the smear), the impact pose (squashed, leaning in, eyes screwed shut) with a camera shake and chips off the block
JF3 = {'lid': 0.4, 'mouth': 'line', 'brow': -0.4}
JUGEK = [k(0.0, look=add(RACK3, [0, 1.5, 0])), k(0.0, toon={'reach': {'L': GV_REST}, 'hands': {'L': 'grip'}, 'face': JF3}, toonDur=0.0),
         k(0.12, toon={'reach': {'L': GV_UP}, 'hands': {'L': 'grip'}, 'sq': [0.95, 1.07, 0.95], 'bend': {'spine': [-0.14, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'clench', 'brow': -0.8}}, toonDur=0.26, toonEase='out'),
         k(0.45, toon={'reach': {'L': R5(add(GV_UP[:3], [0, 0.04, -0.02]), 1, 0.04)}, 'hands': {'L': 'grip'}, 'sq': [0.94, 1.08, 0.94], 'bend': {'spine': [-0.16, 0, 0, 1, None]}, 'face': {'lid': 0.15, 'mouth': 'clench', 'brow': -0.9}}, toonDur=0.12),
         k(r(HIT3 - 0.067), toon={'reach': {'L': GV_HIT}, 'hands': {'L': 'grip'}, 'sq': [1.0, 1.0, 1.0], 'bend': {'spine': [0.1, 0, 0, 1, None]}, 'face': {'lid': 0.3, 'mouth': 'clench', 'brow': -0.9}}, toonDur=0.06, toonEase='in'),
         k(HIT3, toon={'reach': {'L': GV_HIT}, 'hands': {'L': 'grip'}, 'sq': [1.12, 0.86, 1.12], 'bend': {'spine': [0.28, 0, 0, 1, None]}, 'face': {'lid': 0.85, 'mouth': 'grimace', 'brow': -1.0}}, toonDur=0.03, toonEase='out'),
         k(r(HIT3 + 0.13), toon={'reach': {'L': GV_HIT}, 'hands': {'L': 'grip'}, 'sq': [1.08, 0.9, 1.08], 'bend': {'spine': [0.26, 0, 0, 1, None]}, 'face': {'lid': 0.8, 'mouth': 'grimace', 'brow': -1.0}}, toonDur=0.04),
         k(r(HIT3 + 0.18), toon={'reach': {'L': R5([0.05, 1.42, -13.4], 1, 0.04)}, 'hands': {'L': 'open'}, 'sq': [0.98, 1.02, 0.98], 'bend': {'spine': [0.05, 0, 0, 1, None]}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.12)]
SMEAR3 = [P(f'gavelS3_{i}', 'gavel', pos=[r(0.07 - 0.03 * (2 - i)), r(1.42 + 0.33 * (2 - i)), r(-13.38 - 0.16 * (2 - i))], rot=[0, 0, r(-1.5708 + 0.42 * (2 - i))], keys=[k(0.0, visible=False), k(r(HIT3 - 0.06), visible=True), k(r(HIT3 - 0.005), visible=False)]) for i in range(3)]
st.shot('S03', 'replicaCourt', setOpts={'handle': 'TRIBUNAL', 'windowX': -1.5, 'chairW': 1.2, 'chairH': 2.75, 'chairX': 0.15, 'benchGlow': '#5A564A'},
        actors=[act('juge', JG, RYJ, 'stand', 'neutral', keys=JUGEK)],
        props=[P('specs3', 'glasses', on={'actor': 'juge', 'joint': 'head', 'offset': [0.02, 0.17, 0.15]}, opts={'r': 0.042, 'dx': 0.07}),
               P('gavelUp3', 'gavel', on={'actor': 'juge', 'hand': 'L'}, keys=[k(0.0, visible=True), k(r(HIT3 - 0.01), visible=False)]),
               P('gavel3', 'gavel', pos=[0.1, 1.27, -13.3], rot=[0, 0, -1.5708], keys=[k(0.0, visible=False), k(r(HIT3 - 0.01), visible=True)]),
               *SMEAR3,
               P('block3', 'soundBlock', pos=[0.1, 1.18, -13.3]),
               P('dossier3', 'tacheScalesPanel', pos=[0.15, 0.8, -14.44], opts={'w': 1.26, 'h': 1.98}),
               P('pilier3', 'tacheBox', pos=[0.0, 5.25, -15.42], opts={'w': 0.58, 'h': 4.6, 'd': 0.04, 'color': '#EEEBE4', 'outline': 0}),
               # (round 3) the set's red wainscot on the side wall showed as a saturated red block behind the shirt's sleeve on the reverse: covered
               P('lambris3', 'tacheBox', pos=[11.72, 0.79, -9.0], opts={'w': 0.04, 'h': 1.6, 'd': 12.3, 'color': '#EEEBE4', 'outline': 0}),
               P('eclats3', 'tacheDust', pos=[0.1, 1.18, -13.3], opts={'pts': [[0.0, 0.0, HIT3, 0.22]], 'n': 7, 'color': '#F2EBDD', 'dur': 0.35}),
               P('portant3', 'tacheRack', pos=RACK3, ry=RYR3, opts={'w': 0.9, 'shirt': {'stain': 'splat', 'sway': 0.02, 'jumpAt': [STAMP3], 'hitAt': [STAMP3], 'hitAmp': 1.4, 'flinchAt': [STAMP3]}}),
               P('barre3', 'table', pos=add(RACK3, [0.0, 0, -0.75]), ry=RYR3, opts={'w': 1.4, 'd': 0.12, 'h': 1.0, 'color': '#8A5A3A'}),
               P('ordre3', 'tacheEvictOrder', pos=ORDER3, ry=yaw(ORDER3, C3B['from']), scale=0.01, opts={'stampAt': STAMP3}, keys=[k(r(CUT3 + 0.06), scale=0.62, dur=0.14, ease='out')])],
        fx=[{'type': 'shake', 'at': HIT3, 'dur': 0.2, 'amount': 0.032}, {'type': 'shake', 'at': STAMP3, 'dur': 0.12, 'amount': 0.012}],
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
WHITESET = {'clouds': 0, 'grass': '#DCE5D3', 'treeColors': ['#E9EEF3', '#F6F8FA', '#D3DCE6']}   # (round 1) the field's own trees bleached too
def SHIRT_RACK(pid, **o): return P(pid, 'tacheRack', pos=RACK, ry=0, opts={'w': 1.0, 'h': 1.95, 'shirt': {'s': 1.0, **o}})
SH_TOP = 1.95 + 0.06 - 0.13                                    # the shirt's shoulders (the torso from 1.88 down to 1.08)
def SHP(u, v): return [r(-0.31 + 0.62 * u), r(SH_TOP - 0.62 * v), 0.03]   # a point on the shirt's front (u across, v in widths from the top)

# (round 1) the charge accelerates (ease in) from the end of the street and skids to a stop just behind the rack (leaning back, a squash), the
#     line of shields filling the frame behind the shirt, which flinches on the stop
# (round 2) the line waits at the end of the street (shields up, stamping on the spot), braces back two frames before « chargé » and leans in
#     on it, the run kicking up dust; the shields ride on their chests (they grow as they come); they skid to a stop behind the rack (leaning
#     back, a squash, a burst of dust) and the shirt recoils hard: the sleeves fly up, the stain winces
# (round 3) the line starts nearer and marches in from the first frame (it reaches the middle distance by about 1 s, so the middle of the shot
#     is no longer dead), halts and braces 0.2 s before « chargé » (6 frames at 30 fps), runs on « chargé » and skids to a stop behind the rack at
#     1.74 s: the shields grow on their chests, the shirt recoils, and the recoil gets 0.66 s to read and hang before the cut
CRS = [('crs1', -1.5, -11.0), ('crs2', -0.5, -10.4), ('crs3', 0.55, -10.7), ('crs4', 1.6, -11.3), ('crs5', -2.4, -11.8)]
ADV4, MARCH4 = 4.4, (0.1, 0.95)
STOP4 = 1.74; CHG4 = st.at('S04', 'L04', 4)
CHECKS.append(f"S04 « {st.L['L04']['words'][4]['w']} » at {CHG4}, stop {STOP4}")
def crs_end(x, z0): return [r(0.25 + x * 0.6), 0, r(-1.45 - 0.22 * abs(x))]
CRSF = {'lid': 0.0, 'mouth': 'clench', 'brow': -0.6}
SHT = {'L': ['torso', 0.15, 0.33, 0.36, 1, 0.03], 'R': ['torso', -0.15, 0.3, 0.36, 1, 0.03]}
def CRS_KEYS(j, x, z0, start=None, stop=STOP4):
    start = CHG4 if start is None else start; b = crs_end(x, z0); dj = r(0.02 * j)
    pose = lambda sq_, lay_=0.0, face=CRSF: {'touch': SHT, 'hands': {'L': 'grip', 'R': 'grip'}, 'sq': list(sq_), 'lay': [lay_, 0.0], 'face': face}
    ks = [k(0.0, look='camera'), k(0.0, toon=pose((1, 1, 1)), toonDur=0.0), k(r(MARCH4[0] + dj), to=[x, 0, r(z0 + ADV4)], dur=r(MARCH4[1] - MARCH4[0]), clip='walk', ease='inOut')]
    for i in range(4):
        ks.append(k(r(0.12 + 0.22 * i + 0.05 * (j % 2)), toon=pose((1.03, 0.97, 1.03) if i % 2 == 0 else (0.99, 1.02, 0.99)), toonDur=0.1))
    ks += [k(r(start - 0.2 + dj), toon=pose((1.1, 0.88, 1.1), -0.16, {**CRSF, 'lid': 0.4, 'brow': -0.9}), toonDur=0.12, toonEase='inOut'),
           k(r(start + dj), to=b, dur=r(stop - start), clip='run', ease='inOut'), k(r(start + dj), toon=pose((0.96, 1.05, 0.96), 0.3), toonDur=0.08, toonEase='out'),
           k(r(stop + 0.03 * j), toon=pose((1.16, 0.84, 1.1), -0.3), toonDur=0.05), k(r(stop + 0.03 * j + 0.16), toon=pose((0.96, 1.05, 0.96), 0.06), toonDur=0.1),
           k(r(stop + 0.03 * j + 0.3), toon=pose((1, 1, 1), 0.0), toonDur=0.12)]
    return ks
def SHIELD(pid, j, n, start=None, stop=STOP4):
    start = CHG4 if start is None else start
    return P(pid, 'tacheRoundShield', on={'actor': n, 'joint': 'torso', 'offset': [0.0, 0.33, 0.42]}, opts={'riot': True}, keys=[k(r(start + 0.02 * j), scale=1.18, dur=r(stop - start)), k(r(stop + 0.03 * j), squash=[1.14, 0.84, 1.0], dur=0.4)])
def DUST4():
    pts = []
    for j, (n, x, z0) in enumerate(CRS):
        b = crs_end(x, z0); t0 = CHG4 + 0.02 * j; zm = z0 + ADV4
        for f in (0.06, 0.2, 0.34, 0.46):
            u = f / (STOP4 - CHG4); e = 2 * u * u if u < 0.5 else 1 - (2 - 2 * u) ** 2 / 2; pts.append([r(x + (b[0] - x) * e), r(zm + (b[2] - zm) * e - 0.2), r(t0 + f), 0.35])
        pts.append([b[0], r(b[2] + 0.35), r(STOP4 + 0.03 * j), 0.6])
    return P('poussiere4', 'tacheDust', pos=[0, 0, 0], opts={'pts': pts, 'n': 5, 'dur': 0.5})
# 4: the riot police charged the shirt. Low in the road: the shirt hangs alone on its rack in the right foreground (its stain to us) and a line of
#    riot police with round shields and dark visors charges at it from the end of the street; the camera trucks slowly to the left
D4 = st.dur('S04')
# (round 3) aimed higher: the horizon drops and the empty road at the bottom of the frame shrinks
C4 = cam(0.0, [-0.85, 0.55, 3.5], [-1.05, 0.55, 3.2], [0.5, 3.15, -12.0], [0.45, 3.05, -12.0], lens=50)
chkc('S04', C4, {'stain': SHP(0.34, 0.47), 'collar': SHP(0.5, 0.0), 'hem': SHP(0.5, 1.29), 'hook': [0, 2.12, 0], **{n: [x, 2.0, z0] for n, x, z0 in CRS}, **{n + 'Mid': [x, 2.0, r(z0 + ADV4)] for n, x, z0 in CRS}, 'horizon': [0, 0.0, -300.0]})
chkc('S04', C4, {'stain': SHP(0.34, 0.47), **{n: add(crs_end(x, z0), [0, 2.0, 0]) for n, x, z0 in CRS}, **{n + 'sh': add(crs_end(x, z0), [0, 1.25, 0.5]) for n, x, z0 in CRS}}, end=True)
st.shot('S04', 'grassland', setOpts=TOWNSET, actors=[act(n, [x, 0, z0], 0, 'stand', 'determined', keys=CRS_KEYS(j, x, z0)) for j, (n, x, z0) in enumerate(CRS)],
        props=[*TOWN('S04', 'colour', zmin=-60, zmax=10), SHIRT_RACK('portant4', stain='splat', sway=0.03, hitAt=[r(STOP4 + 0.02)], hitAmp=2.6, flinchAt=[r(STOP4 + 0.02)]),
               *[SHIELD(f'bouclier4_{j}', j, n) for j, (n, x, z0) in enumerate(CRS)], *[VISOR(f'casque4_{j}', n) for j, (n, x, z0) in enumerate(CRS)], DUST4()],
        cams=[C4])
st.cue('sfx:stepRun', 'S04', 0.15, 0.2); st.cue('sfx:stepRun', 'S04', r(CHG4 + 0.02), 0.45); st.cue('sfx:stepRun', 'S04', r(CHG4 + 0.3), 0.45); st.cue('sfx:siren', 'S04', 0.0, 0.1); st.cue('thud', 'S04', STOP4, 0.4); st.cue('sfx:brake', 'S04', r(STOP4 - 0.12), 0.3)

# 5: the stain dug in under the pocket. Macro on the shirt's chest: the splat slides up and under the pocket flap on « retranchée », one drip left
#    peeking out; behind the collar the riot police stand with their shields raised
# (round 1) the stain crouches and wriggles first (0.45 s), stretches into a smear along its way as it dives under the pocket, then the drip,
#     bigger, peeks out, ducks back in and peeks again during the hold, while the camera pushes in on the pocket
D5 = st.dur('S05'); SLIDE5 = r(st.at('S05', 'L05', 3) - 0.02); SLD5 = 0.36; E5 = r(SLIDE5 + SLD5)
C5 = cam(0.0, [0.12, 2.2, 2.6], [0.1, 2.17, 2.35], [0.0, 1.62, 0.0], [0.03, 1.64, 0.0], lens=46)
C5B = cam(E5, [0.1, 2.17, 2.35], [0.16, 2.0, 1.55], [0.03, 1.64, 0.0], [0.13, 1.66, 0.0], lens=46, ease='inOut')
PEEK5 = [[E5, 0.0], [r(E5 + 0.1), 1.25], [r(E5 + 0.22), 1.0], [r(E5 + 0.36), 1.0], [r(E5 + 0.44), 0.0], [r(E5 + 0.58), 0.0], [r(E5 + 0.66), 1.35], [r(E5 + 0.8), 1.05]]
CRS5 = [('crs1', -0.78, -2.7), ('crs2', 0.05, -3.1), ('crs3', 0.82, -2.8)]
chkc('S05', C5, {'stain': SHP(0.34, 0.47), 'pocket': SHP(0.71, 0.31), 'collar': SHP(0.5, 0.0), 'stainLow': SHP(0.34, 0.6), **{n: [x, 2.05, z] for n, x, z in CRS5}, **{n + 'sh': [x, 1.45, z + 0.5] for n, x, z in CRS5}})
def CRS5K(j, p):
    UP = {'reach': {'L': R5(off(p, 0, 0.42, -0.14, 1.5), 1, 0.03), 'R': R5(off(p, 0, 0.42, 0.14, 1.45), 1, 0.03)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': {'lid': 0.1, 'mouth': 'clench', 'brow': -0.7}}
    return [k(0.0, look=[0, 1.6, 0]), k(0.0, toon={**UP, 'sq': [1.08, 0.93, 1.08]}, toonDur=0.0), k(0.12, toon={**UP, 'sq': [1, 1, 1]}, toonDur=0.15),
            k(r(SLIDE5 + 0.3 + 0.07 * j), toon={**UP, 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.0, 'mouth': 'O', 'brow': 0.6}}, toonDur=0.08), k(r(SLIDE5 + 0.5 + 0.07 * j), toon={**UP, 'sq': [1, 1, 1]}, toonDur=0.12)]
st.shot('S05', 'grassland', setOpts=TOWNSET, actors=[act(n, [x, 0, z], 0, 'stand', 'determined', keys=CRS5K(j, [x, 0, z])) for j, (n, x, z) in enumerate(CRS5)],
        props=[*TOWN('S05', 'colour', zmin=-30, zmax=0, cars=False), SHIRT_RACK('portant5', stain='splat', wigAt=r(SLIDE5 - 0.45), slideAt=SLIDE5, slideDur=SLD5, peek=1.0, peekKeys=PEEK5, sway=0.012),
               *[P(f'bouclier5_{j}', 'tacheRoundShield', pos=[x, 1.45, r(z + 0.5)], opts={'riot': True}) for j, (n, x, z) in enumerate(CRS5)], *[VISOR(f'casque5_{j}', n) for j, (n, x, z) in enumerate(CRS5)]],
        cams=[C5, C5B])
chkc('S05', C5B, {'pocket': SHP(0.71, 0.31), 'drip': SHP(0.73, 0.5), 'collar': SHP(0.5, 0.0)}, end=True)
st.cue('sfx:slideUp', 'S05', SLIDE5, 0.35); st.cue('sfx:squeak', 'S05', r(E5 + 0.1), 0.25); st.cue('sfx:squeak', 'S05', r(E5 + 0.66), 0.2)

# ============================== the tank, in the side street (x -24), facing +x, firing at the rack
TANK = [-24.0, 0, 0.0]; MUZ = [r(-24.0 + 4.97), 2.38, 0.0]
SHIRT_PT = [0.0, 1.5, 0.0]
# 6: a tank fired stain remover. Three-quarter front of the tank in the side street: the giant spray bottle strapped to its barrel; on « tiré » it
#    fires a thick white jet off to the right toward the rack; the hull rocks back, dust at the tracks, foam at the nozzle
D6 = st.dur('S06'); FIRE6 = r(st.at('S06', 'L06', 3) - 0.02)
# (round 2) the tank framed larger, nearly head-on from its right front quarter (the jet comes out toward the lens and leaves by the right
#     edge); a 0.3 s anticipation (the bottle swells, the hull squats) and a big recoil (props_tache.js tankRecoil): the jet's root follows the
#     nozzle as the hull slides back and the barrel stretches and springs back
# (round 3) lower and closer: the tank and its spray bottle fill the middle, the empty road at the bottom shrinks, the bottle stands against the sky
C6 = cam(0.0, [-15.2, 0.6, 2.2], [-15.35, 0.6, 2.08], [-24.5, 2.38, -0.97], [-24.5, 2.4, -0.97], lens=59)
chkc('S06', C6, {'tankBack': [-27.0, 2.4, -1.3], 'tankBackR': [-27.0, 0.0, 1.8], 'frontL': [-21.0, 0.1, 1.8], 'frontR': [-21.0, 0.1, -1.8], 'muzzle': MUZ, 'turretTop': [-24.4, 2.6, 0], 'bottle': [-20.4, 2.95, 0]})
def tank_dz(u, SL=0.7):
    if u <= 0: return 0.0
    bk = u / 0.05 if u < 0.05 else math.exp(-(u - 0.05) * 3.2)
    gs = 1 + 0.3 * u / 0.05 if u < 0.05 else (1.3 - 0.5 * (u - 0.05) / 0.08 if u < 0.13 else 1 - 0.2 * math.exp(-(u - 0.13) * 6) * math.cos((u - 0.13) * 14))
    return -SL * bk - 0.4 * bk + 3.97 * (gs - 1)
JETK6 = [k(r(FIRE6 + i / 30), to=[r(MUZ[0] + tank_dz(i / 30 + 1 / 30)), MUZ[1], MUZ[2]], dur=r(1 / 30)) for i in range(0, 30)]
st.shot('S06', 'grassland', setOpts=TOWNSET, actors=[],
        props=[*TOWN('S06', 'colour', zmin=-14, zmax=22), P('char6', 'tacheTank', pos=TANK, ry=90, opts={'fireAt': FIRE6}),
               P('jet6', 'tacheJet', pos=MUZ, opts={'fireAt': r(FIRE6 + 0.02), 'v': 40, 'r': 0.42, 'hits': [[0, sub(SHIRT_PT, MUZ)]], 'mist': 2.0}, keys=JETK6)],
        cams=[C6])
st.cue('sfx:stretch', 'S06', r(FIRE6 - 0.3), 0.2); st.cue('thunder', 'S06', FIRE6, 0.5); st.cue('sfx:splash', 'S06', r(FIRE6 + 0.03), 0.5); st.cue('whoosh', 'S06', r(FIRE6 + 0.05), 0.35, 0.5, 300, 2400)

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
# (round 2) the houses and the cars get about 0.55 s each, so the mayor's take gets 1.3 s (the review: the stalks lasted 0.3 s before the cut)
D8 = st.dur('S08'); CUT8B = 0.56; CUT8C = 1.11
C8A = cam(0.0, [-1.5, 0.9, 19.5], [-1.2, 0.95, 19.0], [10.4, 3.9, 10.5], [10.4, 4.0, 10.0], lens=46)
C8B = cam(CUT8B, [1.2, 1.25, 15.5], [1.3, 1.25, 15.0], [4.4, 1.0, 1.5], [4.4, 1.0, 1.0], lens=44)
# (round 1) the mayor further back and lower in the frame, the dark doorway behind him and the MAIRIE plate (dark rim) over his head
C8C = cam(CUT8C, [30.3, 1.75, 47.6], [30.28, 1.78, 47.25], [30.0, 2.45, 43.2], [30.0, 2.45, 43.2], lens=44)
chkc('S08a', C8A, {'roof': [10.4, 6.0, 12.0], 'door': [7.2, 1.0, 12.0], 'base': [7.2, 0.0, 10.5]})
chkc('S08b', C8B, {'car0': [4.3, 1.4, 7.5], 'car1': [4.3, 1.4, 1.0], 'car2': [4.3, 1.4, -6.5]})
chkc('S08c', C8C, {'head': add(MAIRE, [0, 2.0, 0]), 'headTop': add(MAIRE, [0, 2.32, 0]), 'sash': add(MAIRE, [0, 1.3, 0.13]), 'doorL': [29.2, 1.5, 42.6], 'doorR': [30.8, 1.5, 42.6], 'plate': [30.0, 3.5, 42.7], 'feet': MAIRE})
chk('S08a+', C8A['from'], C8A['lookAt'], 46, {'tree': [6.6, 4.5, 16.25], 'treeBase': [6.6, 0, 16.25], 'eave': [7.2, 2.85, 15.35], 'eave2': [9.5, 2.85, 15.35]})
WF = {'lid': 0.35, 'mouth': 'line', 'brow': 0.1}
# (round 1) a real double take (the film's one eyes-on-stalks take): a blink, a glance down at his white hands, back to us, a blank beat, then the
#     snap back down at them, stretched, the eyes out, held to the cut
HANDSM = {'touch': {'L': ['torso', 0.28, 0.05, 0.06, 1, 0.03], 'R': ['torso', -0.28, 0.05, 0.06, 1, 0.03]}}
# (round 2) staged over 1.3 s: a blink, a blink, a glance at his white hands and back to us, a squash down (four frames), the stalks snap out
#     past their length (overshoot) and settle, a trembling hang of eight frames, then they snap back in with a little counter-squash
T8 = CUT8C; HANDS8 = add(MAIRE, [0.12, 0.95, 0.55]); DT8 = r(T8 + 0.7)
STALK8 = lambda pl, sq: {**HANDSM, 'sq': sq, 'face': {'pop': 1.0, 'popLen': pl, 'eyeScale': 1.35, 'stalkPitch': -0.4, 'brow': 1, 'jaw': 0.35, 'lid': 0.0, 'tremble': 1, 'pupilShake': 1, 'mouth': 'o'}}
MAIREK = [k(0.0, look='camera'), k(0.0, toon={'face': WF, **HANDSM}, toonDur=0.0), *blink(r(T8 + 0.05), WF), *blink(r(T8 + 0.27), WF),
          k(r(T8 + 0.42), look=HANDS8, lookDur=0.08), k(r(T8 + 0.55), look='camera', lookDur=0.06),
          k(r(T8 + 0.57), toon={**HANDSM, 'sq': [1.15, 0.83, 1.15], 'face': {**WF, 'lid': 0.65, 'brow': -0.5, 'mouth': 'clench'}}, toonDur=0.1, toonEase='inOut'),
          k(DT8, look=HANDS8, lookDur=0.04),
          k(DT8, toon=STALK8(0.46, [0.86, 1.2, 0.86]), toonDur=0.04, toonEase='out'),
          k(r(DT8 + 0.067), toon=STALK8(0.34, [0.91, 1.12, 0.91]), toonDur=0.05),
          *[k(r(DT8 + 0.133 + 0.067 * i / 2), toon=STALK8(0.36 if i % 2 == 0 else 0.32, [0.9, 1.13, 0.9] if i % 2 == 0 else [0.92, 1.11, 0.92]), toonDur=0.03) for i in range(6)],
          k(r(DT8 + 0.33), look='camera', lookDur=0.05), k(r(DT8 + 0.33), toon={**HANDSM, 'sq': [1.07, 0.93, 1.07], 'face': {**WF, 'lid': 0.1, 'brow': 0.6}}, toonDur=0.04, toonEase='out'),
          k(r(DT8 + 0.43), toon={**HANDSM, 'face': {**WF, 'brow': 0.3}}, toonDur=0.1)]
# (round 1) lit from the front (the sun behind the camera of beat 1, a cool grade), foam flakes drifting down and dripping from the gutters
DRIP8 = [[7.4, 2.85, 15.35], [8.6, 2.85, 15.35], [10.1, 2.85, 15.35], [11.6, 2.85, 15.35], [12.9, 2.85, 15.35], [6.95, 2.2, 13.2]]
st.shot('S08', 'grassland', setOpts=WHITESET, look={'sunDir': [-0.62, 0.62, 0.48], 'warm': 0.45, 'sunColor': '#FFF1DE'}, actors=[act('maire', MAIRE, 0, 'stand', 'neutral', keys=MAIREK)],
        props=[*TOWN('S08', 'white', zmin=-10, zmax=24), P('mairie8', 'tacheBleach', pos=HALL, ry=0, opts={'prop': 'townHall', 'popts': {'w': 6, 'gable': 'v2'}, 'at': -1, 'puff': False}),
               P('arbre8w', 'tacheBleach', pos=[4.5, 0, 13.5], scale=1.7, opts={'prop': 'tree', 'popts': {'seed': 5}, 'at': -1, 'puff': False}),
               P('porte8', 'tacheDoorway', pos=[30.0, 0.4, 42.62], opts={'w': 1.6, 'h': 2.65, 'plateW': 3.5}),
               P('mousse8a', 'tacheFoamDrift', pos=[0, 0, 0], opts={'w': 0.1, 'h': 0.1, 'd': 0.1, 'n': 0, 'drips': DRIP8, 'floor': 0.0}),
               P('mousse8b', 'tacheFoamDrift', pos=[6.0, 0, 12.0], opts={'w': 7, 'h': 6, 'd': 14, 'n': 46, 'size': 0.09}),
],
        cams=[C8A, C8B, C8C])
st.cue('sfx:ding', 'S08', 0.15, 0.2); st.cue('sfx:ding', 'S08', CUT8B, 0.2); st.cue('sfx:boing', 'S08', DT8, 0.3); st.cue('sfx:boing', 'S08', r(DT8 + 0.33), 0.15)

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
# (round 1) re-staged: the officers stand either side of the rack, a step behind it at mid-ground (never in front of the shirt), in pale blue suits
#     that read on the white street; the shirt and its map fill the middle of the frame (about half its width) with nothing across them; the tape
#     runs out at waist height behind and beside the rack; the map comes down over the red stain, its coast flashes twice on « exacte »; the officers
#     start (a stretch, hands up), then step back away from the camera and apart, each on his own side
D10 = st.dur('S10'); MAP10 = 0.85; PULSE10 = r(st.at('S10', 'L10', 5) + 0.05); BACK10 = r(PULSE10 + 0.38)
C10 = cam(0.0, [0.0, 1.62, 3.15], [0.0, 1.6, 2.85], [0.0, 1.5, 0.0], [0.0, 1.52, 0.0], lens=46)
LEG = [('legiste1', [-0.64, 0, -1.5], 22), ('legiste2', [0.64, 0, -1.5], -22)]
LEGB = {'legiste1': [-0.86, 0, -2.45], 'legiste2': [0.86, 0, -2.45]}
chkc('S10', C10, {'collar': SHP(0.5, 0.0), 'stain': SHP(0.5, 0.64), 'hem': SHP(0.5, 1.29), 'shirtL': SHP(0.0, 0.5), 'shirtR': SHP(1.0, 0.5), **{n: add(p, [0, 2.05, 0]) for n, p, ry in LEG}, **{n + 'Top': add(p, [0, 2.35, 0]) for n, p, ry in LEG},
                  **{n + 'Out': add(p, [-0.3 if p[0] < 0 else 0.3, 2.05, 0]) for n, p, ry in LEG}, 'tapeBack': [0, 0.95, -0.75], 'tapeSide': [1.3, 0.95, 0.0]})
chkc('S10', C10, {**{n: add(p, [0, 2.05, 0]) for n, p in LEGB.items()}, **{n + 'Out': add(p, [-0.3 if p[0] < 0 else 0.3, 2.05, 0]) for n, p in LEGB.items()}}, end=True)
def LEGK(n, p, ry, sd):
    face = {'lid': 0.35, 'mouth': 'line', 'brow': 0.2}
    lowL, lowR = R5(off(p, ry, 0.3, 0.18, 1.0), 1, 0.04), R5(off(p, ry, 0.3, -0.18, 1.0), 1, 0.04)
    up = {'reach': {'L': R5(off(p, ry, 0.32, 0.3, 1.62), 1, 0.04), 'R': R5(off(p, ry, 0.32, -0.3, 1.62), 1, 0.04)}, 'hands': {'L': 'spread', 'R': 'spread'}}
    return [k(0.0, look=SHP(0.5, 0.55)), k(0.0, toon={'reach': {'L': lowL, 'R': lowR}, 'hands': {'L': 'open', 'R': 'open'}, 'face': face}, toonDur=0.0),
            k(r(MAP10 + 0.1), look=SHP(0.5, 0.75), lookDur=0.2), k(r(0.35 + 0.25 * (sd > 0)), toon={'reach': {'L': lowL, 'R': lowR}, 'face': {**face, 'brow': 0.4}, 'sq': [0.99, 1.01, 0.99]}, toonDur=0.2, keepPose=True),
            k(r(PULSE10 - 0.07), toon={'reach': {'L': lowL, 'R': lowR}, 'sq': [1.06, 0.93, 1.06], 'face': {**face, 'lid': 0.6}}, toonDur=0.05),
            k(PULSE10, toon={**up, 'sq': [0.9, 1.12, 0.9], 'face': {'lid': 0.0, 'eye': 0.35, 'mouth': 'O', 'brow': 1.0}}, toonDur=0.05, toonEase='out'),
            k(r(PULSE10 + 0.2), toon={**up, 'sq': [0.93, 1.08, 0.93], 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O', 'brow': 0.9}}, toonDur=0.1),
            k(BACK10, to=LEGB[n], dur=0.5, clip='walk', ease='inOut', face='keep'), k(BACK10, toon={'reach': {'L': lowL, 'R': lowR}, 'face': {'lid': 0.1, 'mouth': 'o', 'brow': 0.7}, 'sq': [1, 1, 1]}, toonDur=0.15),
            k(r(BACK10 + 0.55), look='camera', lookDur=0.12),
            # (round 2) moving holds: they breathe, glance at each other before the map comes down, and keep breathing after stepping back
            k(r(0.2 + 0.1 * (sd > 0)), look=add(LEG[1 if sd < 0 else 0][1], [0, 2.0, 0]), lookDur=0.12), k(r(0.58 + 0.08 * (sd > 0)), look=SHP(0.5, 0.55), lookDur=0.14),
            *life(0.05, r(PULSE10 - 0.1), {**face, 'brow': 0.3}, ph=0.12 * (sd > 0), blinks=[r(0.5 + 0.3 * (sd > 0))]),
            *life(r(BACK10 + 0.55), D10, {'lid': 0.2, 'mouth': 'o', 'brow': 0.6}, ph=0.1 * (sd > 0), blinks=[r(BACK10 + 0.75)])]
st.shot('S10', 'grassland', setOpts=WHITESET, look={'warm': 0.55}, actors=[act(n, p, ry, 'stand', 'neutral', keys=LEGK(n, p, ry, -1 if p[0] < 0 else 1)) for n, p, ry in LEG],
        props=[*TOWN('S10', 'white', zmin=-40, zmax=8), SHIRT_RACK('portant10', stain='country', mapAt=MAP10, mapDur=0.5, mapPulse=PULSE10, sway=0.01),
               P('ruban10', 'tacheTape', pos=[0, 0, -0.05], opts={'w': 2.6, 'd': 1.4, 'h': 0.95, 'runAt': [0.0, 0.75], 'open': True})],
        cams=[C10])
st.cue('sfx:zip', 'S10', 0.05, 0.3); st.cue('sfx:paper', 'S10', MAP10, 0.35); st.cue('sfx:ding', 'S10', PULSE10, 0.4); st.cue('sfx:ding', 'S10', r(PULSE10 + 0.28), 0.25)

# ============================== the press room
PRES = [0.0, 0, -2.45]
# (round 1) the sign held out beside his head (its inner edge clear of his face from the camera), the hand at shoulder height, elbow bent
SIGN0 = [0.42, 0.55, -2.25]; SIGN1 = off(PRES, 0, 0.3, -0.8, 1.42)
# 11: a presidential decree forbids washing it. The president in his plain sash signs the decree on the lectern, then holds up on « interdit » a
#     crossed-out washing machine on a stick, at his shoulder, elbow bent (never a straight raised arm); flashes
D11 = st.dur('S11'); UP11 = r(st.at('S11', 'L11', 3) - 0.12)
CHECKS.append(f"S11 sign up {UP11} (« {st.L['L11']['words'][3]['w']} » at {st.at('S11', 'L11', 3)})")
C11 = cam(0.0, [-0.55, 1.95, 1.75], [-0.5, 1.93, 1.5], [0.35, 1.9, -2.5], [0.32, 1.92, -2.5], lens=42)
chkc('S11', C11, {'head': add(PRES, [0, 2.0, 0]), 'headR': add(PRES, [0.22, 2.0, 0.15]), 'signTop': add(SIGN1, [0, 0.3 + 0.62, 0]), 'signC': add(SIGN1, [0, 0.3 + 0.31, 0]), 'signIn': add(SIGN1, [-0.27, 0.3 + 0.31, 0]),
                  'fl1': [-0.38, 1.5, -1.5], 'fl2': [0.95, 1.35, -2.0], 'fl3': [-0.35, 2.55, -2.1], 'decree': [0.0, 1.16, -2.05], 'title': [-0.3, 3.05, -2.96], 'titleR': [1.15, 3.05, -2.96]})
SPF = {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}
PEN = lambda dx: R5([r(0.02 + dx), 1.2, -2.02], 1, 0.03)
# the sign's path (and the hand's on it): (time, sign position, duration, ease, squash, neck bend, face)
SIGNK11 = [(r(UP11 - 0.2), SIGN0, 0.06, 'inOut', [1.0, 1.0, 1.0], 0.0, SPF),
           (r(UP11 - 0.14), add(SIGN0, [0, -0.12, 0]), 0.12, 'inOut', [1.07, 0.92, 1.07], 0.1, {'lid': 0.5, 'mouth': 'smirk', 'brow': -0.3}),
           (UP11, add(SIGN1, [0, 0.07, 0]), 0.1, 'out', [0.93, 1.09, 0.93], -0.04, {'lid': 0.1, 'mouth': 'bigsmile', 'brow': 0.8}),
           (r(UP11 + 0.1), add(SIGN1, [0, -0.02, 0]), 0.1, 'inOut', [1.02, 0.98, 1.02], 0.0, {'lid': 0.2, 'mouth': 'smile', 'brow': 0.6}),
           (r(UP11 + 0.2), SIGN1, 0.12, 'inOut', [1.0, 1.0, 1.0], 0.0, {'lid': 0.25, 'mouth': 'smile', 'brow': 0.5})]
PRESK = [k(0.0, look=[0.0, 1.15, -2.05]), k(0.0, toon={'reach': {'R': PEN(0.0), 'L': R5([0.3, 1.13, -2.08], 1, 0.04)}, 'hands': {'R': 'pinch', 'L': 'open'}, 'bend': {'neck': [0.3, 0, 0, 1, None]}, 'face': SPF}, toonDur=0.0)]
for i in range(6): PRESK.append(k(r(0.12 + 0.11 * i), toon={'reach': {'R': PEN(0.04 * (i % 3) - 0.03)}}, toonDur=0.08, keepPose=True))
PRESK += [k(0.82, look='camera', lookDur=0.12), k(0.82, toon={'reach': {'R': R5([-0.28, 1.13, -2.08], 1, 0.04), 'L': R5([0.3, 1.13, -2.08], 1, 0.04)}, 'hands': {'R': 'open', 'L': 'open'}, 'bend': {'neck': [0.0, 0, 0, 1, None]}, 'face': SPF}, toonDur=0.15),
          *blink(1.0, SPF),
          # (round 3) an anticipation dip (he sinks, the sign goes down first) before the sign snaps up past its mark in three frames and settles;
          # then a smug chin lift that overshoots and settles (the hand is keyed on the sign's own path)
          *[k(t_, toon={'reach': {'R': R5([-0.28, 1.13, -2.08], 1, 0.04), 'L': R5(add(q_, [0, 0.12, 0]), 1, 0.05)}, 'hands': {'L': 'grip', 'R': 'open'}, 'sq': sq_, 'bend': {'neck': [nk_, 0, 0, 1, None]}, 'face': f_}, toonDur=d_, toonEase=e_)
            for t_, q_, d_, e_, sq_, nk_, f_ in SIGNK11],
          k(r(UP11 + 0.36), toon={'bend': {'neck': [-0.22, 0, 0, 1, None]}, 'sq': [0.98, 1.03, 0.98], 'face': {'lid': 0.35, 'mouth': 'smirk', 'brow': 0.75}}, toonDur=0.1, toonEase='out', keepPose=True),
          k(r(UP11 + 0.47), toon={'bend': {'neck': [-0.12, 0, 0, 1, None]}, 'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.3, 'mouth': 'smirk', 'brow': 0.6}}, toonDur=0.12, toonEase='inOut', keepPose=True),
          # (round 1) a smug blink: the lids come down slowly, the brows up, the chest puffed, a smirk, then open again
          k(r(UP11 + 0.62), toon={'face': {'lid': 0.75, 'mouth': 'smirk', 'brow': 0.8, 'cheeks': 0.6}, 'sq': [1.05, 1.03, 1.05]}, toonDur=0.14, toonEase='inOut', keepPose=True),
          k(r(UP11 + 0.8), toon={'face': {'lid': 1.0, 'mouth': 'smirk', 'brow': 0.9, 'cheeks': 0.7}, 'sq': [1.06, 1.04, 1.06]}, toonDur=0.08, keepPose=True),
          k(r(UP11 + 0.98), toon={'face': {'lid': 0.3, 'mouth': 'smirk', 'brow': 0.6, 'cheeks': 0.4}, 'sq': [1.02, 1.01, 1.02]}, toonDur=0.12, keepPose=True)]
st.shot('S11', 'pressRoom', setOpts={'backdrop': ' ', 'fg': 'rgba(0,0,0,0)', 'chairs': False, 'flags': False}, actors=[act('president', PRES, 0, 'podium', 'neutral', keys=PRESK)],
        props=[P('decret11', 'tacheDecree', pos=[0.02, 1.16, -2.06], opts={'signAt': 0.12, 'signDur': 0.66}),
               P('stylo11', 'marker', on={'actor': 'president', 'hand': 'R', 'offset': [0.0, -0.03, 0.03]}, keys=[k(0.82, visible=False)]),
               P('panneau11', 'tacheNoWashSign', pos=SIGN0, ry=-14, opts={'w': 0.52}, keys=[k(0.0, visible=False), k(r(UP11 - 0.2), visible=True)] + [k(t_, to=q_, dur=d_, ease=e_) for t_, q_, d_, e_, sq_, nk_, f_ in SIGNK11[1:]]),
               P('titre11', 'wallTitle', pos=[0.42, 3.05, -2.96], opts={'w': 1.45, 'h': 0.36, 'text': 'DÉCRET PRÉSIDENTIEL', 'bg': '#7A2E3A', 'fg': '#F4F1E8', 'rule': False, 'tick': True, 'emit': 0.3}),
               # (round 1) the press flashes inside the frame, on « interdit »
               P('flash11a', 'camFlash', pos=[-0.38, 1.5, -1.5], opts={'w': 0.55, 'at': [r(UP11 + 0.08), r(UP11 + 0.5)]}),
               P('flash11b', 'camFlash', pos=[0.95, 1.35, -2.0], opts={'w': 0.5, 'at': [r(UP11 + 0.24)]}),
               P('flash11c', 'camFlash', pos=[-0.35, 2.55, -2.1], opts={'w': 0.45, 'at': [r(UP11 + 0.38), 0.4]})],
        cams=[C11])
st.cue('sfx:scratch', 'S11', 0.15, 0.2); st.cue('sfx:shutter', 'S11', r(UP11 + 0.08), 0.35); st.cue('sfx:shutter', 'S11', r(UP11 + 0.24), 0.3); st.cue('sfx:shutter', 'S11', r(UP11 + 0.38), 0.3); st.cue('sfx:shutter', 'S11', r(UP11 + 0.5), 0.25)

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
# (round 1) both soldiers kept in the frame (the bundle carrier walks off toward the back, not out of the left edge) and the hauling hands raised
#     above the caption band
C12 = cam(0.0, [1.9, RY0 + 1.1, 3.3], [1.8, RY0 + 1.1, 3.0], [0.0, RY0 + 2.75, -3.0], [0.0, RY0 + 2.95, -3.0], lens=54)
# (round 2) he carries the soft bundle out of the frame by the left edge (out by about 1.2 s); the bundle rides on his chest
S1_12 = RP(-0.9, -2.4); S2_12 = RP(0.75, -2.55); S1E_12 = RP(-2.6, -1.6); RYS1 = yaw(S1_12, S1E_12)
chkc('S12', C12, {'shirtStart': [0, SHY(1.6) - 0.6, -2.87], 'shirtEnd': [0, SHY(5.0) - 0.6, -2.87], 'hookEnd': [0, SHY(5.0), -2.87], 'hemEnd': [0, SHY(5.0) - 1.2, -2.87], 'ball': [0, RY0 + PH + 0.45, -3], 'sold1': add(S1_12, [0, 2.0, 0]), 'sold2': add(S2_12, [0, 2.0, 0]), 'sold1End': add(S1E_12, [0, 2.0, 0]), 'sold1L': add(S1E_12, [-0.35, 1.2, 0]), 'handLow': [0.07, RY0 + 1.75, -2.9], 'handHi': [0.07, RY0 + 2.3, -2.9]})
ROPE = lambda y: R5([0.07, RY0 + y, -2.9], 1, 0.03)
def HAUL():
    # (round 2) he watches the rope at his hands (looking up at the hook bent his neck back past the break)
    out = [k(0.0, look=[0, RY0 + 2.25, -2.9]), k(0.0, toon={'reach': {'R': ROPE(2.3), 'L': ROPE(1.85)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'clench', 'brow': -0.4}}, toonDur=0.0)]
    for i in range(6):
        # (round 3) each pull in step with a tug of the hoist (the shirt goes up in jerks, not an even slide)
        t_ = r(0.1 + 0.25 * i); hi, lo = (2.35, 1.8) if i % 2 == 0 else (1.8, 2.35)
        out.append(k(t_, toon={'reach': {'R': ROPE(hi), 'L': ROPE(lo)}, 'sq': [1.03, 0.97, 1.03] if i % 2 else [0.98, 1.02, 0.98]}, toonDur=0.15, toonEase='out', keepPose=True))
    return out + [k(1.75, look='camera', lookDur=0.15)]
BUND = off(S1_12, RYS1, 0.38, 0.0, 1.2)
st.shot('S12', 'grassland', setOpts={'clouds': 12}, actors=[
        act('soldat1', S1_12, RYS1, 'stand', 'neutral', keys=[k(0.0, look=add(BUND, [0, -0.1, 0])), k(0.0, toon={'touch': {'L': ['torso', 0.26, 0.16, 0.36, 1, 0.04], 'R': ['torso', -0.26, 0.16, 0.36, 1, 0.04]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': {'lid': 0.45, 'mouth': 'line'}}, toonDur=0.0),
                                                         k(0.3, to=S1E_12, dur=1.3, clip='walk', ease='linear')]),
        act('soldat2', S2_12, -95, 'stand', 'neutral', keys=HAUL())],
        props=[ROOFP('toit12'), POLEP('mat12', hoistAt=0.1, hoistDur=1.5, tugs=6, bounce=0.09, ropeR=0.02, ropeColor='#4A3A2A', shirt={'stain': 'country', 'sway': 0.04, 'hitAt': [1.6], 'hitAmp': 0.7}), KEPI('kepi12a', 'soldat1'), KEPI('kepi12b', 'soldat2'),
               P('ballot12', 'tacheBundle', on={'actor': 'soldat1', 'joint': 'torso', 'offset': [0.0, 0.1, 0.36]}, opts={'swing': 0.1, 's': 1.25})],
        cams=[C12])
st.card('S12', 'HISSÉE', at=CARD12)
st.cue('sfx:squeak', 'S12', 0.2, 0.2); st.cue('sfx:squeak', 'S12', 0.7, 0.2); st.cue('sfx:boing', 'S12', 1.6, 0.18); st.cue('sfx:fanfare', 'S12', r(CARD12 - 0.05), 0.3)

# 13: two guards salute it day and night. Low at the foot of the pole: two ceremonial guards (plumed helmets, epaulettes, sabres) salute, hand at
#     the brow, the shirt high above them; on « nuit » the sky snaps to night (a moon, stars) and they do not move; one blinks
# (round 2) the sky snaps to night on the first frame of « nuit » (word 6; word 4 is « jour »), in one frame
D13 = st.dur('S13'); NIGHT13 = r(st.at('S13', 'L13', 6) - 0.015)
G13 = [('garde1', RP(-0.85, -2.1), 0), ('garde2', RP(0.85, -2.1), 0)]
C13 = cam(0.0, [0.3, RY0 + 1.2, 3.9], [0.28, RY0 + 1.15, 3.6], [0.0, RY0 + 3.3, -2.5], [0.0, RY0 + 3.35, -2.5], lens=52)
chkc('S13', C13, {**{n: add(p, [0, 2.0, 0]) for n, p, ry in G13}, **{n + 'Top': add(p, [0, 2.75, 0]) for n, p, ry in G13}, 'feet': RP(0.85, -2.1), 'shirtTop': [0, SHY(5.0), -2.87], 'shirtHem': [0, SHY(5.0) - 1.2, -2.87], 'moon': [4.0, RY0 + 9.0, -14.0]})
# (round 2) moving holds: they breathe, one lifts his chin a touch, each blinks by day and again by night; the plumes quiver
st.shot('S13', 'grassland', setOpts={'clouds': 12}, daynight={'from': NIGHT13, 'period': 0.04, 'once': True},
        actors=[act(n, p, ry, 'stand', 'determined', keys=saluting(p, ry, life=life(0.1, D13, SAL_F, ph=0.2 * j, blinks=[r(0.55 + 0.3 * j), r(NIGHT13 + 0.3 + 0.15 * j)], chin=(0.95, 1.35) if j == 0 else None))) for j, (n, p, ry) in enumerate(G13)],
        props=[ROOFP('toit13'), POLEP('mat13', shirt={'stain': 'country', 'sway': 0.03}), *[x for j, (n, p, ry) in enumerate(G13) for x in (GUARD(f'casque13_{j}', n, 1.7 * j), EPAU(f'epau13_{j}', n), SABRE(f'sabre13_{j}', n))],
               P('lune13', 'moon', pos=[4.0, RY0 + 8.0, -14.0], opts={'radius': 1.0}, keys=[k(0.0, visible=False), k(NIGHT13, visible=True)]),
               P('etoiles13', 'stars', pos=[0, RY0, -3], opts={'count': 160, 'radius': 50}, keys=[k(0.0, visible=False), k(NIGHT13, visible=True)])],
        cams=[C13])
st.cue('sfx:crickets', 'S13', r(NIGHT13 + 0.05), 0.3)

# 14: the embassies officially recognised the stain. Wide and low under the pole: ambassadors in plain dark suits and plain sashes step up one after
#     another and sign the register on a table at its foot; two bandsmen play by the balustrade
D14 = st.dur('S14')
TAB14 = RP(0.75, -1.9)
# (round 3) a tighter group (the band nearer the pole, the ambassadors' marks closer in) seen from further in front with a longer lens: the left
#     ambassador and the tuba stay inside the frame, and the shirt flies a little lower here (1/3 down the frame) so the frame is not half sky;
#     the second ambassador signs with a pen flourish (a fast loop with three ghost pens along it, on « reconnu »), then steps back out of the
#     third one's way
AMB = [('ambassadeur1', RP(0.05, -1.25), RP(-0.8, -0.45), 0.12), ('ambassadeur2', RP(-0.8, -0.35), RP(-0.6, -2.05), 0.85), ('ambassadeur3', RP(-1.15, 0.1), RP(-0.8, -0.35), 2.04)]
BAND14 = [RP(1.15, -3.6), RP(1.5, -3.55)]; Y1_14 = 4.5
C14 = cam(0.0, [1.0, RY0 + 1.3, 6.6], [0.95, RY0 + 1.3, 6.35], [-0.28, RY0 + 1.97, -3.29], [-0.28, RY0 + 2.0, -3.29], lens=50)
chkc('S14', C14, {**{n: add(p, [0, 2.0, 0]) for n, p, q, t0 in AMB}, 'amb3L': add(AMB[2][1], [-0.3, 1.5, 0]), 'amb1end': add(AMB[0][2], [-0.3, 1.5, 0]), 'register': add(TAB14, [0, 1.05, 0]), 'shirtTop': [0, SHY(Y1_14), -2.87], 'shirtHem': [0, SHY(Y1_14) - 1.2, -2.87],
                  'band1': add(BAND14[0], [0, 2.3, 0]), 'band2': add(BAND14[1], [0, 2.3, 0]), 'tubaBell': add(BAND14[1], [0.45, 2.5, 0])})
FL14 = r(st.at('S14', 'L14', 4) - 0.02)
CHECKS.append(f"S14 flourish {FL14} (« {st.L['L14']['words'][4]['w']} »)")
SIGN14 = add(TAB14, [-0.05, 1.08, 0.1])
FLOUR14 = [(FL14, [0.12, 0.18, 0.08]), (r(FL14 + 0.033), [0.3, 0.45, 0.12]), (r(FL14 + 0.067), [0.12, 0.64, 0.14]), (r(FL14 + 0.1), [-0.08, 0.42, 0.12])]
def AMBK(p, q, t0, j):
    face = {'lid': 0.35, 'mouth': 'line', 'brow': 0.1}; sign = R5(add(TAB14, [-0.05, 1.08, 0.1]), 1, 0.04)
    ks = [k(0.0, look=add(TAB14, [0, 1.0, 0]) if j == 0 else [0, SHY(4.5), -2.9]), k(0.0, toon={'face': face}, toonDur=0.0)]
    if j == 0:
        ks += [k(0.1, toon={'reach': {'R': sign}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': face}, toonDur=0.15),
               *[k(r(0.28 + 0.09 * i), toon={'reach': {'R': R5(add(sign[:3], [0.04 * (i % 2), 0, 0]), 1, 0.04)}}, toonDur=0.07, keepPose=True) for i in range(4)],
               k(0.72, to=q, dur=0.5, clip='walk', ease='inOut'), k(0.72, toon={'face': face, 'bend': {'spine': [0, 0, 0, 1, None]}}, toonDur=0.15), k(1.1, look='camera', lookDur=0.15)]
    else:
        ks += [k(r(t0 - 0.62), to=add(TAB14, [-0.65, 0, 0.55] if j == 1 else [-0.55, 0, 0.68]), dur=0.55, clip='walk', ease='inOut'), k(r(t0 - 0.05), look=add(TAB14, [0, 1.0, 0]), lookDur=0.12),
               k(t0, toon={'reach': {'R': sign}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': face}, toonDur=0.15),
               *[k(r(t0 + 0.18 + 0.09 * i), toon={'reach': {'R': R5(add(sign[:3], [0.04 * (i % 2), 0, 0]), 1, 0.04)}}, toonDur=0.07, keepPose=True) for i in range(4)]]
        if j == 2:
            # (round 3) he waits longer now (until the second one steps back): a moving hold, a blink and a glance at the flourish
            ks += [*life(0.05, r(t0 - 0.66), face, ph=0.2, blinks=[0.6]), k(1.3, look=add(TAB14, [0, 1.3, 0]), lookDur=0.12)]
        if j == 1:
            ks += [*[k(t_, toon={'reach': {'R': R5(add(SIGN14, d_), 1, 0.04)}, 'face': {'lid': 0.3, 'mouth': 'smirk', 'brow': 0.5}}, toonDur=0.03, toonEase='linear', keepPose=True) for t_, d_ in FLOUR14],
                   k(r(FL14 + 0.16), toon={'reach': {'R': R5(add(SIGN14, [-0.04, 0.34, 0.1]), 1, 0.04)}, 'bend': {'spine': [0.12, 0, 0, 1, None]}, 'face': {'lid': 0.45, 'mouth': 'smirk', 'brow': 0.4}}, toonDur=0.12, keepPose=True),
                   k(1.5, to=q, dur=0.42, clip='walk', ease='inOut'), k(1.5, toon={'bend': {'spine': [0.0, 0, 0, 1, None]}, 'face': face}, toonDur=0.15), k(1.95, look='camera', lookDur=0.15)]
    return ks
BEAT14 = [r(0.1 + 0.42 * i) for i in range(6)]
st.shot('S14', 'grassland', setOpts={'clouds': 12}, actors=[
        *[act(n, p, yaw(p, TAB14), 'stand', 'neutral', keys=AMBK(p, q, t0, j)) for j, (n, p, q, t0) in enumerate(AMB)],
        act('musicien1', BAND14[0], -30, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': R5(off(BAND14[0], -30, 0.3, 0.12, 1.75), 1, 0.04), 'L': R5(off(BAND14[0], -30, 0.3, -0.08, 1.75), 1, 0.04)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'face': {'lid': 0.5, 'mouth': 'puff'}}, toonDur=0.0), *[k(b_, toon={'sq': [1.03, 0.97, 1.03] if i_ % 2 else [0.98, 1.02, 0.98]}, toonDur=0.1, keepPose=True) for i_, b_ in enumerate(BEAT14)]]),
        act('musicien2', BAND14[1], -30, 'stand', 'neutral', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.5, 'mouth': 'puff'}}, toonDur=0.0), *[k(b_, toon={'sq': [1.04, 0.96, 1.04] if i_ % 2 else [0.97, 1.03, 0.97]}, toonDur=0.1, keepPose=True) for i_, b_ in enumerate(BEAT14)]])],
        props=[ROOFP('toit14'), POLEP('mat14', y1=Y1_14, shirt={'stain': 'country', 'sway': 0.03}),
               P('stylo14', 'marker', on={'actor': 'ambassadeur2', 'hand': 'R', 'offset': [0.0, -0.03, 0.03]}, scale=1.8, keys=[k(0.0, visible=False), k(r(AMB[1][3] - 0.1), visible=True), k(1.55, visible=False)]),
               *[P(f'stylo14g_{i}', 'marker', pos=add(add(SIGN14, d_), [0, -0.12, 0]), rot=[0, 0, r(0.7 - 0.6 * i, 3)], scale=1.8, keys=[k(0.0, visible=False), k(t_, visible=True), k(r(t_ + 0.067), visible=False)]) for i, (t_, d_) in enumerate(FLOUR14[:3])],
               P('table14', 'table', pos=TAB14, ry=-20, opts={'w': 1.0, 'd': 0.6, 'h': 1.0, 'color': '#7A2E3A'}), P('registre14', 'register', pos=add(TAB14, [0, 1.0, 0]), ry=-20, opts={'w': 0.6, 'h': 0.42, 'right': 'OFFICIEL'}),
               P('trompette14', 'brass', on={'actor': 'musicien1', 'hand': 'R', 'offset': [0.0, 0.0, 0.05]}, opts={'kind': 'trumpet'}),
               P('tuba14', 'bandInstr', on={'actor': 'musicien2', 'joint': 'torso', 'offset': [0.0, 0.45, 0.1]}, opts={'kind': 'sousa', 'beat': BEAT14}),
               KEPI('kepi14a', 'musicien1'), KEPI('kepi14b', 'musicien2')],
        cams=[C14])
st.cue('sfx:fanfare', 'S14', 0.05, 0.35); st.cue('whoosh', 'S14', FL14, 0.18, 0.15, 900, 3000); st.cue('sfx:scratch', 'S14', 0.3, 0.15); st.cue('sfx:scratch', 'S14', r(AMB[1][3] + 0.2), 0.15); st.cue('sfx:scratch', 'S14', r(AMB[2][3] + 0.2), 0.15)

# 15: the shirt stays his. So does the upkeep. On the roof, medium close: two soldiers hand him (now in a pale blue shirt) a folded ironing board with
#     a form clipped on it and an iron; he holds them flatly; on « L'entretien » he glances at the iron, then at us, and blinks
D15 = st.dur('S15'); GIVE15 = r(st.at('S15', 'L15', 4) - 0.1); LOOK15 = r(st.at('S15', 'L15', 6) + 0.05)
# (round 1) both soldiers in the frame, a step behind him either side; the board (a long pointed nose, its iron rest) and the iron
# (round 3) the hand-over is animated: from PUSH15 the soldiers step in and push the board and the iron to him (the iron is one prop in the world,
#     keyed on the same path as the hands that hold it: the soldier's, then his), his hands come up and meet them on « ce » (GIVE15), he takes
#     them flatly and the weight settles him: a small squash (4-5 %) with the arms and the board dipping, which springs back past rest and settles
#     (the old drop of 12 % read as a pop of his whole figure); the board turns a little so its light metal legs show folded along its underside
PUSH15 = 0.36; SET15 = r(GIVE15 + 0.1); BACK15 = r(GIVE15 + 0.22); REST15 = r(GIVE15 + 0.36)
CHECKS.append(f"S15 push {PUSH15} give {GIVE15} (« {st.L['L15']['words'][4]['w']} ») look {LOOK15} (« {st.L['L15']['words'][6]['w']} ») dur {D15}")
ME15 = RP(0.0, 0.0)
SB = RP(0.7, -0.5); SI = RP(-0.7, -0.5); RYSB, RYSI = -45, 45
SBIN, SIIN = add(SB, [-0.06, 0, 0.22]), add(SI, [0.06, 0, 0.22])
BOARD0 = add(off(SB, RYSB, 0.42, 0.0, 0.0), [0, 0, 0]); BOARD1 = RP(0.42, 0.3)
# (round 2) aimed lower and the hands raised: the iron and the ENTRETIEN form sit at 60-70 % of the height, above the caption band; the board is a
#     darker cocoa (the white shirt of S16 reads on it)
BOARDC, BOARDT = '#8A6656', '#5E4438'
C15 = cam(0.0, [0.0, RY0 + 1.75, 3.45], [0.0, RY0 + 1.73, 3.2], [0.0, RY0 + 1.12, -0.2], [0.0, RY0 + 1.1, -0.2], lens=52)
chkc('S15', C15, {'head': add(ME15, [0, 2.0, 0]), 'headTop': add(ME15, [0, 2.32, 0]), 'boardTop': add(BOARD1, [0, 1.42, 0]), 'boardLow': add(BOARD1, [0, 0.3, 0]), 'iron': off(ME15, 0, 0.35, 0.3, 0.75),
                  'soldB': add(SB, [0, 2.0, 0]), 'soldI': add(SI, [0, 2.0, 0]), 'soldBout': add(SB, [0.32, 1.5, 0]), 'soldIout': add(SI, [-0.32, 1.5, 0]), 'soldBTop': add(SB, [0, 2.35, 0])})
chkc('S15', C15, {'soldB': add(SBIN, [0.25, 2.0, -0.4]), 'soldI': add(SIIN, [-0.25, 2.0, -0.4]), 'soldBout': add(SBIN, [0.57, 1.5, -0.4]), 'soldIout': add(SIIN, [-0.57, 1.5, -0.4])}, end=True)
MF = {'lid': 0.45, 'mouth': 'line', 'brow': -0.1}
IRONH = R5(off(ME15, 0, 0.32, 0.26, 1.16), 1, 0.04)
BH1 = R5(add(BOARD1, [-0.05, 1.38, 0.05]), 1, 0.04)
IOFF = [0.0, -0.23, 0.0]                                       # the iron's sole below the fist on its handle
def HANDP(dy): return add(IRONH[:3], [0, r(-dy * 1.1), 0])     # his iron hand, dipped by dy
def BRDP(dy): return add(BOARD1, [0, r(0.8 - dy), 0])          # the board's centre, dipped by dy with his left hand
SAGP = lambda dy, sq, face, sp: {'reach': {'L': R5(add(BH1[:3], [0, r(-dy), 0]), 1, 0.04), 'R': R5(HANDP(dy), 1, 0.04)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'hip': 0,
                                  'sq': sq, 'bend': {'spine': [sp, 0, 0, 1, None], 'neck': [-sp * 0.8, 0, 0, 1, None]}, 'face': face}
SAGF = {'lid': 0.55, 'mouth': 'wavy', 'brow': -0.2}
# the settle after the hand-over: (time, dip (m), squash, face, spine bend, duration, ease); the iron and the board are keyed on the same numbers
SETTLE15 = [(GIVE15, 0.07, [1.04, 0.955, 1.04], {**SAGF, 'lid': 0.65}, 0.06, 0.1, 'out'), (SET15, -0.015, [0.98, 1.025, 0.98], SAGF, 0.02, 0.12, 'inOut'),
            (BACK15, 0.025, [1.01, 0.99, 1.01], SAGF, 0.05, 0.14, 'inOut')]
HERO15 = [k(0.0, look=add(SB, [0, 1.9, 0])), k(0.0, toon={'face': MF, 'hip': 0}, toonDur=0.0), k(0.5, look=add(SI, [0, 1.9, 0]), lookDur=0.15), k(r(GIVE15 - 0.1), look='camera', lookDur=0.12),
          k(r(PUSH15 + 0.18), toon={**SAGP(0.0, [1.0, 1.0, 1.0], MF, 0.0)}, toonDur=r(GIVE15 - PUSH15 - 0.18), toonEase='out')]
HERO15 += [k(t_, toon={**SAGP(dy, sq, f, sp)}, toonDur=d_, toonEase=e_) for t_, dy, sq, f, sp, d_, e_ in SETTLE15]
HERO15 += [k(r(LOOK15 - 0.02), toon={**SAGP(0.025, [1.0, 1.0, 1.0], MF, 0.05)}, toonDur=0.12),
           k(LOOK15, look=add(IRONH[:3], [0, -0.45, 0.1]), lookDur=0.12), k(r(LOOK15 + 0.35), look='camera', lookDur=0.12),
           k(r(LOOK15 + 0.35), toon={**SAGP(0.025, [1.0, 1.0, 1.0], MF, 0.05)}, toonDur=0.15), *blink(r(LOOK15 + 0.62), MF)]
def SOLDK(p, pin, ry, sd, path):
    """path: the points his hand follows while he pushes the thing in (t, point, dur, ease); he lets go at the hand-over and steps back"""
    hold = R5(off(p, ry, 0.42, 0.0, 1.15), 1, 0.04); hd = 'R' if sd < 0 else 'L'; face = {'lid': 0.4, 'mouth': 'line', 'brow': -0.2}
    ks = [k(0.0, look=add(ME15, [0, 2.0, 0])), k(0.0, toon={'reach': {hd: hold}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': face}, toonDur=0.0),
          *blink(r(0.15 + 0.12 * (sd > 0)), face),
          k(r(PUSH15 - 0.04), to=pin, dur=0.36, clip='walk', ease='inOut', face='keep')]
    for t_, q, d_, e_ in path: ks.append(k(t_, toon={'reach': {hd: R5(q, 1, 0.04)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'bend': {'spine': [0.14, 0, 0, 1, None]}, 'face': {**face, 'brow': -0.4}}, toonDur=d_, toonEase=e_))
    ks += [k(r(GIVE15 + 0.06), toon={'reach': {hd: R5(off(pin, ry, 0.3, 0.0, 1.0), 0, 0.04)}, 'hands': {'R': 'open', 'L': 'open'}, 'bend': {'spine': [0.0, 0, 0, 1, None]}, 'face': face}, toonDur=0.2),
           k(r(GIVE15 + 0.25), to=add(pin, [r(0.08 * sd), 0, -0.6]), dur=0.45, clip='walk', ease='inOut', face='keep'),
           k(r(GIVE15 + 0.75), look=add(ME15, [0, 2.0, 0]), lookDur=0.15)]
    return ks
S1PATH = [(PUSH15, add(BOARD1, [0.07, 1.15, -0.04]), r(GIVE15 - PUSH15), 'inOut')]
S2PATH = [(PUSH15, add(IRONH[:3], [0.08, 0, 0]), r(GIVE15 - PUSH15), 'inOut')]
IRON15K = [k(PUSH15, to=add(HANDP(0.0), IOFF), dur=r(GIVE15 - PUSH15), ease='inOut')] + [k(t_, to=add(HANDP(dy), IOFF), dur=d_, ease=e_) for t_, dy, sq, f, sp, d_, e_ in SETTLE15]
BOARD15K = [k(PUSH15, to=BRDP(0.0), dur=r(GIVE15 - PUSH15), ease='inOut')] + [k(t_, to=BRDP(dy), dur=d_, ease=e_) for t_, dy, sq, f, sp, d_, e_ in SETTLE15]
IRON0 = add(off(SI, RYSI, 0.42, 0.0, 1.15), IOFF)
st.shot('S15', 'grassland', setOpts={'clouds': 12}, actors=[
        act('mecB', ME15, 0, 'stand', 'unimpressed', keys=HERO15),
        act('soldat1', SB, RYSB, 'stand', 'neutral', keys=SOLDK(SB, SBIN, RYSB, 1, S1PATH)), act('soldat2', SI, RYSI, 'stand', 'neutral', keys=SOLDK(SI, SIIN, RYSI, -1, S2PATH))],
        props=[ROOFP('toit15'), FRONT('chemise15', 'mecB', stain='none', bg='#BFD7EA'), KEPI('kepi15a', 'soldat1'), KEPI('kepi15b', 'soldat2'),
               P('planche15', 'tacheBoard', pos=add(BOARD0, [0, 0.8, 0]), rot=[0, r(PI / 2 - 0.42, 4), PI / 2], opts={'folded': True, 'form': True, 'formX': 0.32, 'legW': 0.3, 'legColor': '#D3D8DE', 'legR': 0.026, 'color': BOARDC, 'trim': BOARDT}, keys=BOARD15K),
               P('fer15', 'tacheIron', pos=IRON0, ry=-90, scale=1.6, opts={'steamAt': [r(LOOK15 + 0.05)]}, keys=IRON15K)],
        cams=[C15])
st.cue('clack', 'S15', GIVE15, 0.3); st.cue('sfx:sniff', 'S15', r(LOOK15 + 0.1), 0.2)

# 16: he irons around the stain. The payoff's own camera, static and close at dawn on the roof: he irons the shirt laid on the board, steering the
#     iron carefully round the country-shaped stain (the iron loops past it, never on it); the two guards salute behind him; a look to us at the end
D16 = st.dur('S16')
# (round 2) re-staged for the read of the payoff: the shirt is laid collar away from us, hem toward the lens, so the country's long axis runs
#     across the frame with its drips hanging down (the silhouette of S09/S13); a neutral white under a warmer, higher key, on a darker cocoa board
#     whose top tilts 12 degrees toward the lens; his torso is capped (the high angle looked into it)
# (round 3) the iron runs a clear U round the stain for most of the shot: down the left side, along the hem just under the drips (it hops over
#     the long one and hangs there trembling, on « tache »), up the right side past the tip and its drops, then it is parked on the bare board
#     and he looks at us. His right hand runs the left side and the hem up to the hop, both hands set it down past the drip, then his left hand
#     runs it on and up the right side while he sidesteps right (an arm from behind the left side, then from the right: the least of the stain
#     hidden); the
#     pole is gone from this frame (it grew out of his head) and the guards stand wide near the edges, clear of his head at the start and the
#     end; the idle weight shift is off (it jumped his torso in one frame); the shirt has cloth volume (rolled sleeve folds, a hem roll, a
#     raised collar band, a contact shadow) and the stain keeps the red of S09/S13 under the warm key (a cooler red paint)
TILT16 = math.radians(12); CT, ST = math.cos(TILT16), math.sin(TILT16)
ME16 = RP(-0.07, -0.74); ME16B = RP(0.3, -0.74); BRD = RP(0.0, 0.0); BH = 1.02; BTH = 0.035
def SURF(x, z, h=0.0): return [r(BRD[0] + x), r(BRD[1] + BH + BTH * CT - z * ST + h * CT), r(BRD[2] + BTH * ST + z * CT + h * ST)]   # a point on the tilted board top (board x, z), h above it
SHS = 1.1; SHH = 0.62; SHX = 0.0; SHD = 0.026 * SHS
SHO = SURF(SHX, r(-(0.13 + SHH / 2) * SHS), SHD / 2 + 0.001)          # the laid shirt's origin (its hook line, beyond the collar)
def ONSH(u, v, h=0.0): return SURF(r(SHX + (u - 0.5) * 0.62 * SHS), r((v - 0.5) * SHH * SHS), SHD + 0.003 + h)   # u across the panel, v down it (0 collar, 1 hem)
CAT16, CSC16 = [0.45, 0.34], 0.82
PAL16 = ['#D03A3C', '#93262E', '#EC6A62']
SC16 = ONSH(0.45, 0.36)
# the iron's way: (t, (u, v) on the shirt or a board point, lift (m), heading (deg: 0 nose to the lens, 90 to the right, 180 away), ease)
PARK = SURF(0.52, -0.06, 0.003)
# (the iron, the fist on its handle and the forearm rise off the board on screen, so the stain sits high on the laid shirt and the hem pass runs
#     at v 0.84, well under the drips; it hops over the long one all the same, and hangs)
WAY16 = [(0.0, (0.085, 0.1), 0.0, 0, None), (0.3, (0.085, 0.24), 0.0, 0, 'in'), (0.8, (0.085, 0.78), 0.0, 0, 'linear'),
         (0.98, (0.15, 0.84), 0.0, 90, 'out'), (1.12, (0.2, 0.84), 0.0, 90, 'inOut'),
         (1.24, (0.29, 0.84), 0.055, 90, 'out'), (1.31, (0.33, 0.84), 0.068, 90, 'inOut'), (1.37, (0.345, 0.84), 0.052, 90, 'inOut'), (1.43, (0.36, 0.84), 0.068, 90, 'inOut'),
         (1.49, (0.375, 0.84), 0.054, 90, 'inOut'), (1.53, (0.39, 0.84), 0.062, 90, 'inOut'),
         (1.65, (0.56, 0.84), 0.0, 90, 'in'), (2.0, (0.88, 0.84), 0.0, 90, 'linear'), (2.18, (0.955, 0.76), 0.0, 180, 'inOut'),
         (2.47, (0.955, 0.17), 0.0, 180, 'inOut'), (2.58, PARK, 0.05, 135, 'out'), (2.68, PARK, 0.0, 90, 'in')]
HOP16, LAND16, PARK16, UP16 = 1.12, 1.65, 2.68, 2.66
def WPT(w): return add(PARK, [-0.12, 0, 0]) if (w[1] is PARK and w[2] > 0) else (w[1] if w[1] is PARK else ONSH(w[1][0], w[1][1]))
def WPOS(w): p = WPT(w); return [p[0], r(p[1] + w[2] * CT), r(p[2] + w[2] * ST)]
G16 = [('garde1', RP(-1.3, -4.6), 0), ('garde2', RP(1.62, -4.6), 0)]
C16 = cam(0.0, [0.06, RY0 + 2.05, 1.85], [0.06, RY0 + 2.04, 1.82], [0.08, RY0 + 1.12, -1.0], [0.08, RY0 + 1.12, -1.0], lens=60)
chkc('S16', C16, {'head': add(ME16, [0, 2.0, 0.2]), 'headR': add(ME16, [0.2, 2.0, 0.2]), 'headEnd': add(ME16B, [0, 2.0, 0.1]), 'headEndR': add(ME16B, [0.21, 2.0, 0.1]), 'headEndL': add(ME16B, [-0.21, 2.0, 0.1]), 'headTop': add(ME16B, [0, 2.36, 0.1]),
                  'stain': SC16, 'collarL': ONSH(0, 0), 'collarR': ONSH(1, 0), 'hemL': ONSH(0, 1), 'hemR': ONSH(1, 1), 'tipL': ONSH(0.2, 0.56), 'dripLow': ONSH(0.37, 0.74),
                  'hop': ONSH(0.37, 0.81, 0.12), 'park': PARK, **{n: add(p, [0, 2.0, 0]) for n, p, ry in G16}, **{n + 'In': add(p, [-0.25 if p[0] > 0 else 0.25, 2.0, 0]) for n, p, ry in G16},
                  **{n + 'Plume': add(p, [0, 3.05, 0]) for n, p, ry in G16}, **{n + 'Out': add(p, [0.35 if p[0] > 0 else -0.35, 1.6, 0]) for n, p, ry in G16}, 'boardFoot': [0.3, RY0, 0.15]})
def HANDI(p, sd='R', dx=0.0): return [r(p[0] + dx), r(p[1] + 0.11), r(p[2] - 0.02), 1, 0.04]
HRL, HRR = R5(SURF(0.25, -0.38, 0.03), 1, 0.04), R5(SURF(-0.32, -0.38, 0.03), 1, 0.04)   # where a free hand rests: the board's far edge, behind the collar
SWAP0, SWAP1 = 1.53, 1.65
def HANDS16(t, p):
    if t <= SWAP0 + 1e-6: return {'R': HANDI(p, 'R'), 'L': HRL}
    if t <= SWAP1 + 1e-6: return {'R': HANDI(p, 'R', -0.035), 'L': HANDI(p, 'L', 0.035)}
    return {'R': HRR, 'L': HANDI(p, 'L')}
DF = {'lid': 0.5, 'mouth': 'line', 'brow': 0.1}
EF16 = {'lid': 0.45, 'mouth': 'line', 'brow': 0.0}
HERO16 = [k(0.0, look=ONSH(0.1, 0.3)), k(0.0, toon={'reach': HANDS16(0.0, WPOS(WAY16[0])), 'hip': 0, 'hose': 0.15, 'hands': {'R': 'grip', 'L': 'open'}, 'bend': {'spine': [0.32, 0, 0, 1, None], 'neck': [0.16, 0, 0, 1, None]}, 'face': DF}, toonDur=0.0)]
for i in range(1, len(WAY16)):
    w = WAY16[i]; d_ = r(w[0] - WAY16[i - 1][0])
    tn = {'reach': HANDS16(w[0], WPOS(w)), 'hip': 0, 'face': DF}
    HERO16.append(k(WAY16[i - 1][0], toon=tn, toonDur=d_, toonEase=w[4], keepPose=True))
# he sidesteps right along the board once the iron has landed past the drip (his arm then comes from behind the iron on the right side)
HERO16 += [k(1.55, to=ME16B, dur=0.5, clip='walk', ease='inOut', face='keep'),
           k(0.45, look=ONSH(0.1, 0.72), lookDur=0.2), k(0.9, look=ONSH(0.25, 0.8), lookDur=0.15), k(1.05, look=ONSH(0.37, 0.74), lookDur=0.08),
           k(1.14, toon={'face': {'lid': 0.15, 'mouth': 'o', 'brow': 0.7}, 'hip': 0}, toonDur=0.06, keepPose=True),
           k(1.55, look=ONSH(0.62, 0.81), lookDur=0.1), k(1.6, toon={'face': DF, 'hip': 0}, toonDur=0.1, keepPose=True),
           k(1.95, look=ONSH(0.95, 0.75), lookDur=0.12), k(2.2, look=ONSH(0.96, 0.4), lookDur=0.15),
           # (round 3) the final lean eases over about 0.24 s (it popped in one draft frame), the look to us leads by a frame
           k(UP16, look='camera', lookDur=0.2), k(UP16, toon={'bend': {'spine': [0.1, 0, 0, 1, None], 'neck': [-0.06, 0, 0, 1, None]}, 'face': EF16, 'hip': 0}, toonDur=0.24, toonEase='inOut', keepPose=True),
           *blink(r(D16 - 0.2), EF16)]
IRONK = []
for i in range(1, len(WAY16)):
    w, w0 = WAY16[i], WAY16[i - 1]; d_ = r(w[0] - w0[0])
    IRONK.append(k(w0[0], to=WPOS(w), dur=d_, ease=w[4]))
    if w[3] != w0[3]: IRONK.append(k(w0[0], rotTo=[r(TILT16, 4), r(math.radians(w[3]), 4), 0], dur=d_, ease='inOut'))
IRONK += [k(LAND16, squash=[1.15, 0.8, 1.15], dur=0.3), k(PARK16, squash=[1.1, 0.88, 1.1], dur=0.3)]
CHECKS.append('S16 way ' + ' '.join(f'{w[0]}:{WPOS(w)}' for w in WAY16[::3]))
st.shot('S16', 'grassland', setOpts={'clouds': 12, 'sky': ['#E9A48E', '#FBD7B0']}, look={'sunDir': [0.5, 0.75, 0.62], 'sunColor': '#FFD6A8', 'fill': 0.9},
        actors=[act('mecB', ME16, 0, 'stand', 'unimpressed', keys=HERO16),
                *[act(n, p, ry, 'stand', 'determined', keys=saluting(p, ry, life=life(0.1, D16, SAL_F, ph=0.25 * j, blinks=[r(0.6 + 0.5 * j), r(1.9 + 0.35 * j)], chin=(1.1, 1.6) if j == 1 else None))) for j, (n, p, ry) in enumerate(G16)]],
        props=[ROOFP('toit16'), FRONT('chemise16', 'mecB', stain='none', bg='#BFD7EA'),
               P('col16', 'tacheBox', on={'actor': 'mecB', 'joint': 'torso', 'offset': [0.0, 0.62, 0.0]}, opts={'w': 0.44, 'h': 0.035, 'd': 0.25, 'color': '#BFD7EA'}),
               *[x for j, (n, p, ry) in enumerate(G16) for x in (GUARD(f'casque16_{j}', n, 0.9 + 1.3 * j), EPAU(f'epau16_{j}', n), SABRE(f'sabre16_{j}', n))],
               P('planche16', 'tacheBoard', pos=BRD, opts={'h': BH, 'len': 1.7, 'w': 0.76, 'tilt': r(TILT16, 4), 'color': BOARDC, 'trim': BOARDT}),
               P('chemise16b', 'tacheHangShirt', pos=SHO, rot=[r(TILT16 - PI / 2, 4), 0, 0], opts={'s': SHS, 'stain': 'country', 'flat': True, 'flatH': SHH, 'flatD': 0.026, 'volume': True, 'pocket': [0.7, 0.88, 0.05, 0.19], 'white': True, 'countryAt': CAT16, 'countrySc': CSC16, 'pal': PAL16}),
               P('fer16', 'tacheIron', pos=WPOS(WAY16[0]), rot=[r(TILT16, 4), 0, 0], scale=0.85, opts={'steamAt': [0.3, LAND16, PARK16]}, keys=IRONK)],
        cams=[C16])
for t_ in [0.2, 0.85, 2.05]: st.cue('sfx:stretch', 'S16', t_, 0.12)
st.cue('sfx:spring', 'S16', HOP16, 0.25); st.cue('thud', 'S16', LAND16, 0.25); st.cue('clack', 'S16', PARK16, 0.2); st.cue('sfx:tick', 'S16', r(UP16 + 0.25), 0.2)

print('\n'.join(CHECKS))

TOON = {'breathe': 1.7, 'holdLife': 1.6}
MEC = {'preset': 'lemec', 'atlasBody': False, 'outfit': 'suit', 'suit': '#E2EBF8', 'pants': '#2B3550', 'shirt': '#E2EBF8', 'lapel': '#E2EBF8', 'tie': '#E2EBF8', 'cuff': '#E2EBF8',
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
    'legiste1': {'preset': 'doctor', 'seed': 951, 'suit': '#8FB6D6', 'pants': '#7FA6C6', 'shirt': '#E6EEF4', 'lapel': '#6F98BC', 'tie': '#2E5A86', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'legiste2': {'preset': 'doctor', 'seed': 952, 'suit': '#8FB6D6', 'pants': '#7FA6C6', 'shirt': '#E6EEF4', 'lapel': '#6F98BC', 'tie': '#2E5A86', 'glasses': False, 'hair': 'bun', 'lipstick': True, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    # (round 2) a plain white sash and a navy tie (black suit, yellow sash and red tie stacked like a flag)
    'president': {'preset': 'politique', 'seed': 953, 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#2C3E5C', 'hairColor': '#BDBDBD', 'sash': ['#F2F0EA'], 'sashW': 0.11, 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.06}, 'toon': EX},
    'soldat1': {**SOLD, 'seed': 960}, 'soldat2': {**SOLD, 'seed': 961, 'facial': 'mustache'},
    'garde1': {**GARD, 'seed': 962}, 'garde2': {**GARD, 'seed': 963, 'facial': 'mustache'},
    'ambassadeur1': {'preset': 'politique', 'seed': 964, 'suit': '#23262C', 'lapel': '#23262C', 'tie': '#3A3D44', 'sash': ['#6A2E5A'], 'sashW': 0.1, 'hairColor': '#2A2420', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    # (round 2) a trouser suit: the skirt suit left her back leg bare skin mid-stride
    'ambassadeur2': {'preset': 'madame', 'seed': 965, 'outfit': 'suit', 'suit': '#2A2D36', 'pants': '#2A2D36', 'lapel': '#2A2D36', 'tie': '#2A2D36', 'sash': ['#2E6B4A'], 'sashW': 0.1, 'glasses': False, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'ambassadeur3': {'preset': 'politique', 'seed': 966, 'suit': '#1F2430', 'lapel': '#1F2430', 'tie': '#3A3D44', 'sash': ['#2C4F86'], 'sashW': 0.1, 'skin': '#8A5A3A', 'faceRim': True, 'hairColor': '#1B1B1E', 'glasses': True, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'musicien1': {**SOLD, 'seed': 967, 'suit': '#7A2E3A', 'pants': '#1E2A44', 'lapel': '#1E2A44', 'cuff': '#E2B53C'}, 'musicien2': {**SOLD, 'seed': 968, 'suit': '#7A2E3A', 'pants': '#1E2A44', 'lapel': '#1E2A44', 'cuff': '#E2B53C', 'facial': 'mustache'},
})
