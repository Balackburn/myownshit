#!/usr/bin/env python3
"""La pelle (story 100, cycle 53; a hook, an institutional escalation, a reversal, a dry last line).
His friends bury this man in the sand up to the neck, and for the town hall someone under the ground is buried, so dead. Digging him out is an
exhumation and the permit takes six months, so the State runs the whole funeral round a live, chatty man: the funeral on the spot (he gives the
speech), a headstone (he has it moved a little to the left, and it gives him the only shade on the beach), a wreath and a replacement from his boss,
his wife on the next towel with a moustached man, his friends inherit his car; the beach becomes a cemetery (spades forbidden), the holidaymakers
tan in mourning, and at night, gates locked, he has the beach to himself. Only the tax office does not believe he is dead. Six months later the
permit comes, and he refuses to come out: he asks for a perpetual plot. In the shade.
Running gags: the crabs (one in S01, two from S03, a family later) add a row of sand blocks to a horseshoe wall round his head in every beach shot
(plCrabWall: rows 0, 1, 2, 3, 4 by S11b at his ears, 5, 6), and in S16 it is a finished sandcastle mausoleum; his skin tans one step per beach shot
(the toon skin channel, k 0 to 0.68), the sunglasses always on, until S16 where they slide up on a nod and show two pale ovals round his eyes
(plOvals); the headstone's shade, set up in S04-S05, pays off in S16; the friends who buried him come back with his car (S08, S13) and end red
and sweating in the sun he no longer shares.
Staging: the head sticks out of a smooth sand mound and faces the land; low cameras in front of him look toward the sea, so every beach shot has
the sea and the sky behind the faces. S01 the friends pat the mound flat with plastic spades (his head squashes at each pat) and walk off with
their towels, a crab beside him; S01b the clerk kneels and props a black-bordered certificate (no text) beside his chin, DÉCÉDÉ stamps and his head
flattens under it. S02 the friends run back, spades up; the clerk stops them with a flat mitten and holds up a wall calendar whose six pages fly
off one by one; their jaws drop. S03 three-quarters, his head in the foreground right, four mourners in one straight row under black parasols on
the left dab their eyes; he gives the speech (lip flaps, orator's nods). S04 two undertakers set a plain headstone behind him; on « gauche » his
eyes flick and his chin nods to his left; they shuffle it one step and its crisp shadow drops on him. S05 noon: in the shade, smiling, while two
bright-red sunbathers sweat behind. S06 his boss sets a wreath beside him and steps aside: a young man in a tie with a box of office things waves.
S07 his wife in a big sunhat on the next towel reads one magazine with a broad moustached man and waves; he blinks once and deflates. S08 the
seafront road: the friends drive past in his convertible, spades up in the back, honk (the car squashes on it). S09 workers stand tall iron
gates between the ice-cream cart and the lifeguard tower (clank); S09b a guard holds out a bin and three children drop their spades in, clunk.
S10 from a crane: holidaymakers in black swimsuits, veils and sunglasses on towels, two fanning in turn, a black ball rolling past. S11 sunset,
lit seafront windows: the guard swings the gates shut (clang) and snaps a padlock on; S11b the empty beach, his head and headstone dark against
the bright sea, a long happy sigh (the head swells and deflates). S12 a tax inspector tucks a fat envelope under his chin and holds his form up to
the lens; the glasses dip and his eyes cross down at it. S13 the friends skid up in the car and jump out: the permit up to the lens, a red stamp
pops; the other waves two spades. S14 they kneel to dig; he shakes his head so hard the sand sprays over them; they freeze, sand on their faces
(REFUSÉ). S15 the clerk kneels with a clipboard; he talks; she ticks a box and nods gravely. S16 tight and low: his head in the crabs'
mausoleum in the headstone's shade; a nod sends the sunglasses up, two pale ovals on his tan; eyes closed, blissful, then a last look at us;
behind, the friends stand red and sweating in the sun; waves lap.
Natural look; cycle 53: props_pelle.js (plWorld, plSeafront, plMound, plCrabWall, plHeadstone, plShades, plOvals, plCertificate, plWreath, plGates,
plBin, plSpade, plFan, plBall, plTower, plSwimTop, plSwimBottom, plSunHat, plVeil, plTissue, plTowelRoll, plPermit, plEnvelope, plTaxForm,
plSandSpray, plSandSpeck, plOfficeBox, plMagazine, plGulls); reused: crab (props_robinet), parasol, iceCreamCart, convertible, sweatDrop,
clipboardProp, mustache3d (props.js), monthCalendar (props_canicule), kidParasol, beachTowel (props_rayon); set grassland (sand-coloured ground).
Lessons applied from the start: `lens` is the vertical field; characters about 2.3 m tall; the head, faces and key props above the caption band
(0.77-0.83) and heads below the card band (0.07-0.18) when a card stamps; every camera and every character checked with project() (CHECKS); every
extra cast member has a preset; word timings from timeline.json through st.at (words counted from 0, the word printed beside its time); the payoff
shots (S01b card, S04 shade, S13 permit, S14 spray, S16 ovals) have their own tight cameras; mitten hands (no fingers); no raised arm held still,
no hand at the face (the mourners' tissues dab the cheek and keep moving; the spades in S14 freeze at shoulder height with a shiver); the hero is
buried, so he acts with his head only (headOnly: big squash and stretch of the head, tilts, nods, shakes, eye takes, lip flaps) and every other
character acts with the whole body; Looney deformation on every gag accent (the head flattened by the card and re-inflating, smears on the shake,
the friends' skid and jaw drops, the boss's reveal, the car's honk squash, the children's slump, the inspector's stretch to the lens, the sigh);
anticipation before each key action; moving holds (breathing, blinks, waves, gulls, crabs); one take per mechanism; new props prefixed pl; sound
names checked against audio3.py/audio.py/mix.py (gust for the waves' wash, sfx:squeak for gulls, sfx:poof for spade pats, clang for the gates,
sfx:honk); no real flag, emblem, insignia or organisation; French only on screen; nobody hurt."""
from story_kit import *
import math

st = Story('pelle', look='natural')
st.plan([('S01', 'L01', 0), ('S01b', 'L01', 8), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0),
         ('S08', 'L08', 0), ('S09', 'L09', 0), ('S09b', 'L09', 6), ('S10', 'L10', 0), ('S11', 'L11', 0), ('S11b', 'L11', 6), ('S12', 'L12', 0), ('S13', 'L13', 0),
         ('S14', 'L14', 0), ('S15', 'L15', 0), ('S16', 'L16', 0)])

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
    # (cycle 51) word timings from timeline.json: st.at counts the words from 0; the word is printed beside its time
    t = st.at(sid, lid, i); CHECKS.append(f"{sid} « {st.L[lid]['words'][i]['w']} » at {t}"); return t

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
def R5(p, w=1, s=0.04): return [*p, w, s]
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

# ============================== the hero: buried to the neck, he acts with his head only
# The actor stands 1.63 m under the sand (his chin at 0.14 m, the top of his head at 0.64 m), headOnly hides everything but the head; a key is
# built from a head squash (scl head, about the chin), a neck bend (forward nod, side tilt, twist) and a face; the sunglasses follow the squash
HP = [0.0, -1.63, 0.0]
TANC = '#6E3A1C'
TAN = {'S01': 0.0, 'S01b': 0.0, 'S02': 0.04, 'S03': 0.1, 'S04': 0.16, 'S05': 0.22, 'S06': 0.28, 'S07': 0.34, 'S11b': 0.42, 'S12': 0.48, 'S13': 0.56, 'S14': 0.6, 'S15': 0.63, 'S16': 0.68}
SHY = 0.31                                                              # the sunglasses' height on the head joint (eyes 0.255 and 0.37 above the chin)
FACE0 = {'lid': 0.3, 'mouth': 'smile', 'brow': 0.2}
class Head:
    """his head's keys for one shot, and the sunglasses' squash keys that follow them"""
    def __init__(self, sid):
        self.sid, self.keys, self.sq = sid, [k(-0.4, look='camera')], [[0.0, 1.0, 1.0]]
        self.skin = {'color': TANC, 'k': TAN.get(sid, 0.0)}
    def pose(self, t, face=None, scl=(1.0, 1.0, 1.0), neck=(0.0, 0.0, 0.0), dur=0.1, ease=None):
        tn = {'headOnly': 1, 'hip': 0, 'skin': self.skin, 'scl': {'head': [r(scl[0], 3), r(scl[1], 3), r(scl[2], 3)]}, 'bend': {'neck': [r(neck[0], 3), r(neck[1], 3), r(neck[2], 3), 1, None]}, 'face': face or FACE0}
        kk = {'toon': tn, 'toonDur': r(dur, 3)}
        if ease: kk['toonEase'] = ease
        self.keys.append(k(r(t), **kk)); self.sq.append([r(t + dur), r(scl[0], 3), r(scl[1], 3)])
        return self
    def look(self, t, target, dur=0.12): self.keys.append(k(r(t), look=target, lookDur=dur)); return self
    def breathe(self, t0, t1, face=None, per=0.9, amp=0.025, neck=(0.0, 0.0, 0.0), blinks=()):
        t_, i = t0, 0
        while t_ < t1 - 0.08:
            if not any(-0.04 < t_ - b < 0.2 for b in blinks):
                self.pose(t_, face, (1 - amp * 0.3, 1 + amp, 1.0) if i % 2 == 0 else (1 + amp * 0.2, 1 - amp * 0.4, 1.0), (neck[0], neck[1] + (0.04 if i % 4 == 1 else (-0.04 if i % 4 == 3 else 0.0)), neck[2]), dur=per * 0.45, ease='inOut')
            t_ += per / 2; i += 1
        for b in blinks: self.pose(b, {**(face or FACE0), 'lid': 1.0}, dur=0.05); self.pose(r(b + 0.1), face, dur=0.06)
        return self
    def talk(self, t0, t1, face=None, step=0.1, nod=0.06):
        t_, i = t0, 0
        while t_ < t1 - 0.04:
            m = ['open', 'o', 'line', 'open', 'smile'][i % 5]
            self.pose(t_, {**(face or FACE0), 'mouth': m, 'jaw': 0.28 if m in ('open', 'o') else 0.0}, (1.0, 1.02 if i % 2 == 0 else 0.99, 1.0), (nod if i % 3 == 0 else -nod * 0.5, 0.05 * math.sin(i * 1.3), 0.0), dur=step * 0.7)
            t_ += step; i += 1
        return self
    def actor(self): return act('mec', HP, 0, 'stand', 'neutral', keys=self.keys)
def SHADES(pid, h, lift=None, dip=None, wob=None, op=0.86):
    o = {'w': 0.34, 'tilt': -0.55, 'y0': SHY, 'sq': h.sq, 'op': op}
    if lift: o['lift'] = lift
    if dip: o['dip'] = dip
    if wob: o['wob'] = wob
    return P(pid, 'plShades', on={'actor': 'mec', 'joint': 'head', 'offset': [0.005, 0.0, 0.1]}, opts=o)
def BURIED(n, rows=0, add_=(), crabs=(), mound=None, wall=True):
    out = [P(f'dune{n}', 'plMound', pos=[0, 0, 0], opts=mound or {})]
    if wall and (rows or add_): out.append(P(f'mur{n}', 'plCrabWall', pos=[0, 0, 0], opts={'rows': rows, 'add': list(add_)}))
    for i, (path, snap, s) in enumerate(crabs): out.append(P(f'crabe{n}_{i}', 'crab', pos=[0, 0.0, 0], opts={'path': path, 'snap': list(snap), 's': s}))
    return out
SET = {'grass': '#E6CF94', 'clouds': 18, 'sky': ['#7EB9E2', '#D6ECF4']}
SUNF = {'sunDir': [0.25, 0.9, 0.85]}                                    # morning: the sun behind the camera, on the faces
SUNB = {'sunDir': [0.42, 0.8, -0.6]}                                    # noon over the sea, behind the headstone: its shadow falls on him
WORLD = lambda n, **o: P(f'monde{n}', 'plWorld', pos=[0, 0, 0], opts=o)
FRONT = lambda n, **o: P(f'front{n}', 'plSeafront', pos=[0, 0, 14.0], opts=o)
GULLS = lambda n, c=(0, 7, -6): P(f'mouettes{n}', 'plGulls', pos=list(c), opts={'R': 5, 'n': 3, 'rate': 0.4})
STONE = [0.3, 0.0, -0.36]                                               # the headstone, once moved « un peu plus à gauche » (his left: +X)
STONE0 = [-0.27, 0.0, -0.36]                                            # where the undertakers first set it
HSTONE = lambda pid, pos=STONE, **x: P(pid, 'plHeadstone', pos=pos, opts={'w': 0.82, 'h': 1.3}, **x)
def WAVES(sid, d):
    t_ = 0.15
    while t_ < d - 0.3: st.cue('gust', sid, r(t_), 0.07, 1.3); t_ += 1.6
def GULLCRY(sid, t, g=0.07): st.cue('sfx:squeak', sid, r(t), g)
SPADE = lambda pid, who, hand='R', col='#E8452E': P(pid, 'plSpade', on={'actor': who, 'hand': hand, 'offset': [0.0, -0.02, 0.0]}, opts={'color': col})

for g_ in [('S01', 1.0, 'mec', 'pats'), ('S01b', 1.0, 'mec', 'certificate flattens him'), ('S02', 2.2, 'pote1', 'jaw drop'), ('S03', 1.6, 'mec', 'speech'), ('S04', 3.0, 'mec', 'shade drops'),
           ('S06', 2.2, 'mec', 'double take'), ('S11b', 1.0, 'mec', 'sigh'), ('S12', 1.4, 'mec', 'cross-eyed'), ('S14', 0.6, 'mec', 'head shake'), ('S16', 1.0, 'mec', 'ovals')]:
    st.gag(*g_)

# 1: the hook. Low at sand level in front of him: only his box head sticks out of a smooth mound, sunglasses on, the sea behind; his two friends
#    kneel behind the mound either side and pat it flat with plastic spades (each pat squashes his head a little, a puff of sand); on « enterrer »
#    the last pat together (his head flattens and pops back, smug); they stand (stretch up) and walk off to the sides with their rolled towels;
#    a crab scuttles beside his head and snaps its claws; he tilts his head side to side, pleased, on « sable »
D1 = st.dur('S01'); ENT1 = W('S01', 'L01', 4); SAB1 = W('S01', 'L01', 7)
P1A = [-0.6, 0.0, -0.42]; P1B = [0.6, 0.0, -0.42]; RY1A = 38; RY1B = -38
PATS1 = [0.12, 0.34, 0.56, 0.76, r(ENT1 - 0.02)]
F1 = [0.3, 0.52, 3.7]; L1 = [-0.02, 0.62, 0.0]
C1 = cam(0.0, F1, add(F1, [-0.04, 0.0, -0.22]), L1, add(L1, [0, 0.01, 0]), lens=46, ease='inOut')
chkc('S01', C1, {'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'p1head': add(P1A, [0, 1.55, 0]), 'p2head': add(P1B, [0, 1.55, 0]), 'p1side': add(P1A, [-0.3, 0.8, 0]), 'p2side': add(P1B, [0.3, 0.8, 0]), 'crab': [0.42, 0.05, 0.32], 'moundL': [-0.62, 0.0, 0.0]})
H1 = Head('S01')
H1.pose(0.0, FACE0, dur=0.0)
for i, t_ in enumerate(PATS1):
    big = i == len(PATS1) - 1
    H1.pose(r(t_ - 0.04), {**FACE0, 'lid': 0.4}, (1.0, 1.0, 1.0), dur=0.04)
    H1.pose(t_, {**FACE0, 'lid': 0.6, 'mouth': 'line' if not big else 'o'}, (1.12, 0.86, 1.05) if not big else (1.32, 0.66, 1.1), (0.0, 0.06 * (1 if i % 2 else -1), 0.0), dur=0.04, ease='out')
    H1.pose(r(t_ + 0.09), {**FACE0, 'lid': 0.3}, (0.96, 1.06, 1.0) if not big else (0.88, 1.18, 0.95), dur=0.07, ease='out')
H1.pose(r(PATS1[-1] + 0.2), {**FACE0, 'lid': 0.25, 'mouth': 'smile', 'brow': 0.4}, (1.0, 1.0, 1.0), dur=0.12)
H1.pose(r(SAB1 - 0.05), {**FACE0, 'mouth': 'smile', 'brow': 0.5}, (1.04, 0.98, 1.0), (0.0, 0.2, 0.0), dur=0.14, ease='inOut')
H1.pose(r(SAB1 + 0.18), {**FACE0, 'mouth': 'smile', 'brow': 0.5}, (1.0, 1.04, 1.0), (0.0, -0.2, 0.0), dur=0.16, ease='inOut')
H1.pose(r(SAB1 + 0.38), {**FACE0, 'mouth': 'smile', 'brow': 0.4}, (1.0, 1.0, 1.0), (0.0, 0.08, 0.0), dur=0.14, ease='inOut')
H1.breathe(r(SAB1 + 0.55), D1, FACE0, blinks=[r(D1 - 0.25)])
PF = {'lid': 0.2, 'mouth': 'smile', 'brow': 0.4}
def POTE1K(p, ry, sd, ph):
    # kneeling, patting with the spade in the right mitten (down: squashed, up: stretched), then standing and walking off with the towel roll
    up = lambda: {'reach': {'R': R5(off(p, ry, 0.5, 0.15 * sd, 0.95), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'hip': 0}
    dn = lambda: {'reach': {'R': R5(off(p, ry, 0.55, 0.15 * sd, 0.5), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'hip': 0}
    ks = [k(-0.4, look=[0.0, 0.4, 0.0]), k(0.0, clip='kneel'), k(0.0, toon={**up(), 'face': PF}, toonDur=0.0)]
    for i, t_ in enumerate(PATS1):
        ks += [k(r(t_ - 0.13 + ph), toon={**up(), 'sq': [0.95, 1.07, 0.95], 'bend': {'spine': [-0.1, 0, 0, 1, None]}, 'face': {**PF, 'brow': 0.6}}, toonDur=0.08, toonEase='out'),
               k(r(t_ - 0.03 + ph), toon={**dn(), 'sq': [1.1, 0.88, 1.1], 'bend': {'spine': [0.45, 0, 0, 1, None]}, 'face': {**PF, 'mouth': 'o' if i == len(PATS1) - 1 else 'smile'}}, toonDur=0.04, toonEase='in')]
    TUP = r(PATS1[-1] + 0.22)
    ks += [k(r(TUP - 0.06), toon={**up(), 'sq': [1.08, 0.9, 1.08], 'face': PF}, toonDur=0.06),
           k(TUP, clip='stand'), k(TUP, toon={'reach': {'R': R5(off(p, ry, 0.25, 0.3 * sd, 1.05), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'sq': [0.92, 1.1, 0.92], 'face': {**PF, 'mouth': 'bigsmile'}, 'hip': 0}, toonDur=0.12, toonEase='out'),
           k(r(TUP + 0.2), look='camera', lookDur=0.12),
           k(r(TUP + 0.18), to=add(p, [1.4 * sd, 0.0, -0.9]), dur=r(D1 - TUP + 0.4), clip='walk', face=r(90 * sd + 20 * sd), ease='linear', cruise=True),
           k(r(TUP + 0.25), toon={'reach': {'R': R5(add(p, [0.35 * sd, 0.95, 0.2]), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'face': PF, 'hip': 0}, toonDur=0.15)]
    return ks
st.shot('S01', 'grassland', setOpts=SET, look=SUNF,
        actors=[H1.actor(), act('pote1', P1A, RY1A, 'kneel', 'happy', keys=POTE1K(P1A, RY1A, -1, 0.0)), act('pote2', P1B, RY1B, 'kneel', 'happy', keys=POTE1K(P1B, RY1B, 1, 0.03))],
        props=[WORLD(1), GULLS(1), SHADES('lun1', H1), *BURIED(1, mound={'pat': [[t_, -0.35 if i % 2 else 0.35, -0.15] for i, t_ in enumerate(PATS1)]},
                                                         crabs=[([[0.0, 0.42, 0.34], [0.5, 0.42, 0.34], [0.9, 0.5, 0.3], [1.3, 0.5, 0.3], [1.6, 0.4, 0.36]], [1.75], 0.24)]),
               SPADE('pelle1a', 'pote1'), SPADE('pelle1b', 'pote2', col='#2F62B5'),
               P('serviette1a', 'plTowelRoll', on={'actor': 'pote1', 'joint': 'torso', 'offset': [0.0, 0.2, -0.16]}, opts={'colors': ['#E8742E', '#F4F1E8']}),
               P('serviette1b', 'plTowelRoll', on={'actor': 'pote2', 'joint': 'torso', 'offset': [0.0, 0.2, -0.16]}, opts={'colors': ['#2E8AC9', '#F4F1E8']})],
        cams=[C1])
for t_ in PATS1: st.cue('sfx:poof', 'S01', r(t_), 0.18)
st.cue('thud', 'S01', PATS1[-1], 0.15); WAVES('S01', D1); GULLCRY('S01', 1.5)

# 1b: for the town hall he is dead. Closer: the clerk in a plain grey suit kneels bent beside him (screen right) and props a big black-bordered
#     certificate (no text) on the mound beside his chin, facing us; she sits back on her heels and nods gravely on « mort »; DÉCÉDÉ stamps and his
#     head flattens under it (wide and short, held trembling) and re-inflates with a pop and an overshoot; his brows go up behind the glasses
D1b = st.dur('S01b'); MAI1b = W('S01b', 'L01', 10); MORT1b = W('S01b', 'L01', 13)
CLK = [0.78, 0.0, 0.12]; RYCLK = -70
CERT = [0.42, 0.12, 0.2]
F1b = [-0.25, 0.62, 3.0]; L1b = [0.2, 0.62, 0.0]
C1b = cam(0.0, F1b, add(F1b, [0.03, 0.0, -0.15]), L1b, add(L1b, [0, 0.0, 0]), lens=52, ease='inOut')
chkc('S01b', C1b, {'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'clerkHead': add(CLK, [0, 1.35, 0]), 'clerkBack': add(CLK, [0.3, 0.9, -0.1]), 'certTop': add(CERT, [0, 0.58, 0]), 'certR': add(CERT, [0.22, 0.3, 0])})
STAMP1b = r(MORT1b + 0.03)
H1b = Head('S01b')
H1b.pose(0.0, FACE0, dur=0.0).look(0.0, 'camera').breathe(0.05, 0.55, FACE0)
H1b.look(0.6, add(CERT, [0, 0.3, 0]), 0.12).pose(0.6, {**FACE0, 'mouth': 'line', 'gx': -0.5, 'gy': 0.4}, neck=(0.12, -0.12, 0.0), dur=0.12)
H1b.look(0.95, 'camera', 0.1).pose(0.95, {**FACE0, 'mouth': 'line', 'brow': 0.0}, dur=0.1)
H1b.pose(r(STAMP1b - 0.05), {**FACE0, 'mouth': 'line', 'brow': 0.3}, (0.95, 1.06, 1.0), dur=0.04)
H1b.pose(STAMP1b, {'lid': 0.7, 'mouth': 'grimace', 'brow': -0.6, 'noBlink': 1}, (1.42, 0.55, 1.1), dur=0.035, ease='out')
for j in range(4): H1b.pose(r(STAMP1b + 0.05 + 0.04 * j), {'lid': 0.7, 'mouth': 'grimace', 'brow': -0.6, 'noBlink': 1}, (1.42 + (0.03 if j % 2 else -0.03), 0.55 + (-0.02 if j % 2 else 0.02), 1.1), dur=0.035)
H1b.pose(r(STAMP1b + 0.24), {'lid': 0.0, 'mouth': 'o', 'brow': 1.0, 'noBlink': 1}, (0.82, 1.24, 0.95), dur=0.06, ease='out')
H1b.pose(r(STAMP1b + 0.34), {'lid': 0.2, 'mouth': 'line', 'brow': 0.8}, (1.06, 0.95, 1.0), dur=0.07)
H1b.pose(r(STAMP1b + 0.44), {'lid': 0.3, 'mouth': 'line', 'brow': 0.6}, (1.0, 1.0, 1.0), dur=0.08)
CF = {'lid': 0.35, 'mouth': 'line', 'brow': -0.1}
CKEEP = lambda hr, sp=0.5: {'reach': {'R': R5(hr, 1, 0.0), 'L': R5(off(CLK, RYCLK, 0.3, 0.2, 0.55), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'bend': {'spine': [sp, 0, 0, 1, None]}, 'hip': 0}
CLKK = [k(-0.4, look=add(CERT, [0, 0.2, 0])), k(0.0, clip='kneel'), k(0.0, toon={**CKEEP(add(CERT, [0.12, 0.45, 0.06])), 'face': CF}, toonDur=0.0),
        k(0.25, toon={**CKEEP(add(CERT, [0.12, 0.4, 0.04]), 0.6), 'sq': [1.04, 0.96, 1.04], 'face': CF}, toonDur=0.15),
        k(0.55, toon={**CKEEP(add(CERT, [0.14, 0.42, 0.02]), 0.55), 'sq': [0.98, 1.02, 0.98], 'face': CF}, toonDur=0.1),
        k(0.72, toon={'reach': {'R': R5(off(CLK, RYCLK, 0.3, -0.15, 0.65), 1, 0.0), 'L': R5(off(CLK, RYCLK, 0.3, 0.2, 0.55), 1, 0.0)}, 'hands': {'R': 'open', 'L': 'open'}, 'bend': {'spine': [0.15, 0, 0, 1, None]}, 'face': CF, 'hip': 0}, toonDur=0.2, toonEase='inOut'),
        k(0.8, look='camera', lookDur=0.15),
        k(r(MORT1b - 0.1), toon={'bend': {'spine': [0.15, 0, 0, 1, None], 'neck': [0.55, 0, 0, 1.6, None]}, 'sq': [1.04, 0.95, 1.04], 'face': {**CF, 'lid': 0.6}, 'hip': 0}, toonDur=0.18, toonEase='inOut'),
        k(r(MORT1b + 0.25), toon={'bend': {'spine': [0.12, 0, 0, 1, None], 'neck': [-0.1, 0, 0, 0.9, None]}, 'sq': [0.98, 1.03, 0.98], 'face': CF, 'hip': 0}, toonDur=0.12, toonEase='out'),
        k(r(MORT1b + 0.38), toon={'bend': {'spine': [0.12, 0, 0, 1, None]}, 'face': CF, 'hip': 0}, toonDur=0.1), *blink(r(D1b - 0.2), CF, {'hip': 0})]
CERTK = [k(0.0, to=add(CERT, [0.05, 0.35, 0.05]), dur=0.0), k(0.25, to=add(CERT, [0.02, 0.1, 0.02]), dur=0.3, ease='inOut'), k(0.55, to=CERT, dur=0.14, ease='in')]
st.shot('S01b', 'grassland', setOpts=SET, look=SUNF, actors=[H1b.actor(), act('greffiere', CLK, RYCLK, 'kneel', 'neutral', keys=CLKK)],
        props=[WORLD('1b'), SHADES('lun1b', H1b, wob=[[STAMP1b, 0.12, 30, 6]]), *BURIED('1b', crabs=[([[0.0, 0.5, 0.32], [1.0, 0.55, 0.3]], [0.4], 0.24)]),
               P('certificat1b', 'plCertificate', pos=CERT, ry=-22, opts={'w': 0.36, 'lean': 0.12}, keys=CERTK)],
        cams=[C1b])
st.card('S01b', 'DÉCÉDÉ', at=r(MORT1b + 0.02))
st.cue('thud', 'S01b', 0.69, 0.12); st.cue('sfx:boing', 'S01b', r(STAMP1b + 0.24), 0.12); WAVES('S01b', D1b)

# 2: digging him out? An exhumation permit: six months. The friends run back in from the left, spades raised; the clerk, standing between them and
#    the mound, stops them with one flat mitten (they skid, squashed, then stretch up straight); she holds up a big wall calendar at her chest and
#    its six month pages fly off one after another on « six mois »; the friends' jaws drop to their collars, spades drooping; in the foreground,
#    low on the right, his head follows the pages with a tilt
D2 = st.dur('S02'); RES2 = W('S02', 'L02', 1); PER2 = W('S02', 'L02', 2); SIX2 = W('S02', 'L02', 4); MOIS2 = W('S02', 'L02', 5)
CL2 = [-0.55, 0.0, -1.35]; RYCL2 = 25
FR2A = [-1.35, 0.0, -2.0]; FR2B = [-1.75, 0.0, -2.65]
STOP2 = r(RES2 + 0.4)
CAL2 = off(CL2, RYCL2, 0.42, 0.0, 1.32)
F2 = [0.55, 0.62, 2.6]; L2 = [-0.75, 1.05, -1.6]
C2 = cam(0.0, F2, add(F2, [0.0, 0.0, -0.18]), L2, add(L2, [0.0, 0.0, 0.0]), lens=54, ease='inOut')
chkc('S02', C2, {'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'clerk': add(CL2, [0, 2.3, 0]), 'cal': add(CAL2, [0, 0.25, 0]), 'calBot': add(CAL2, [0, -0.25, 0]), 'f1': add(FR2A, [0, 2.35, 0]), 'f2': add(FR2B, [0, 2.35, 0]), 'f1feet': FR2A, 'f2start': add(FR2A, [-1.2, 1.5, 0.2])})
H2 = Head('S02')
H2.pose(0.0, FACE0, dur=0.0).breathe(0.05, r(SIX2 - 0.05), FACE0, blinks=[0.9])
for j in range(6):
    t_ = r(SIX2 + 0.04 + 0.17 * j)
    H2.look(t_, add(CAL2, [-0.2 - 0.12 * j, 0.6 + 0.15 * j, 0]), 0.1).pose(t_, {**FACE0, 'mouth': 'o', 'brow': 0.6, 'gy': -0.4}, (1.0, 1.05, 1.0), (-0.05, 0.08 if j % 2 else -0.04, 0.0), dur=0.1)
FF = {'lid': 0.1, 'mouth': 'open', 'brow': 0.8}
JAW = {'lid': 0.0, 'eye': 0.45, 'mouth': 'O', 'brow': 1.0, 'jaw': 1.0, 'jawLen': 1.5, 'jawBlock': 1, 'jawFwd': 0.4, 'noBlink': 1}
def FRK(p, i):
    start = add(p, [-1.5, 0.0, 0.35]); RYF = 60
    spade_up = lambda: {'reach': {'R': R5(off(p, RYF, 0.25, -0.1, 1.95), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'hip': 0}
    spade_dn = lambda: {'reach': {'R': R5(off(p, RYF, 0.35, -0.3, 1.0), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'hip': 0}
    st_ = r(STOP2 + 0.04 * i)
    ks = [k(-0.4, look=[0.0, 0.5, 0.0]), k(0.0, toon={**spade_up(), 'face': FF, 'autoSq': 0.3}, toonDur=0.0),
          k(0.0, to=p, dur=st_, clip='run', face=RYF, ease='out'),
          k(r(st_ - 0.02), clip='skidStop', blend=0.02),
          k(r(st_ - 0.02), toon={**spade_up(), 'sq': [1.18, 0.82, 1.18], 'bend': {'spine': [-0.35, 0, 0, 1, None]}, 'face': {**FF, 'mouth': 'grimace'}}, toonDur=0.04, toonEase='out'),
          k(r(st_ + 0.12), toon={**spade_up(), 'sq': [0.9, 1.12, 0.9], 'bend': {'spine': [0.08, 0, 0, 1, None]}, 'face': {**FF, 'mouth': 'o'}}, toonDur=0.08, toonEase='out'),
          k(r(st_ + 0.24), toon={**spade_up(), 'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.1),
          k(r(st_ + 0.3), look=CAL2, lookDur=0.15),
          k(r(st_ + 0.32), clip='stand'),
          k(r(PER2 + 0.1), toon={**spade_dn(), 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.3}}, toonDur=0.25, toonEase='inOut')]
    T = r(SIX2 + 0.1 + 0.06 * i)
    ks += [*beat(T, {**spade_dn(), 'sq': [0.9, 1.12, 0.9], 'bend': {'neck': [0.0, 0, 0, 1.3, None]}, 'face': JAW},
                 antic={**spade_dn(), 'sq': [1.05, 0.95, 1.05], 'face': {'lid': 0.4, 'mouth': 'line', 'brow': 0.0}}, hold=0.35,
                 over={**spade_dn(), 'sq': [1.04, 0.96, 1.04], 'face': {**JAW, 'jaw': 0.5}}, settle={**spade_dn(), 'face': {**JAW, 'jaw': 0.6, 'jawBlock': 1}}, antic_f=3, settle_f=5)]
    return ks
CLF = {'lid': 0.4, 'mouth': 'line', 'brow': -0.2}
CL2STOP = lambda: {'reach': {'L': R5(off(CL2, RYCL2, 0.45, 0.5, 1.25), 1, 0.0), 'R': R5(off(CL2, RYCL2, 0.2, -0.25, 1.0), 1, 0.0)}, 'hands': {'L': 'open', 'R': 'rest'}, 'scl': {'handL': [1.35, 1.35, 1.35]}, 'hip': 0}
CL2CAL = lambda dy=0.0: {'reach': {'L': R5(add(CAL2, [0.2, -0.24 + dy, -0.03]), 1, 0.0), 'R': R5(add(CAL2, [-0.2, -0.24 + dy, -0.03]), 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'hip': 0}
CLK2 = [k(-0.4, look=FR2A), k(0.0, toon={'reach': {'R': R5(off(CL2, RYCL2, 0.2, -0.25, 1.0), 1, 0.0)}, 'hands': {'R': 'rest'}, 'face': CLF, 'hip': 0}, toonDur=0.0),
        k(r(STOP2 - 0.3), toon={**CL2STOP(), 'sq': [1.04, 0.96, 1.04], 'bend': {'spine': [0.1, 0, 0, 1, None]}, 'face': CLF}, toonDur=0.08),
        k(r(STOP2 - 0.18), toon={**CL2STOP(), 'sq': [0.96, 1.05, 0.96], 'bend': {'spine': [-0.08, 0, 0, 1, None]}, 'face': {**CLF, 'brow': -0.5}}, toonDur=0.1, toonEase='out'),
        k(r(STOP2 + 0.1), toon={**CL2STOP(), 'face': {**CLF, 'brow': -0.5}}, toonDur=0.1),
        k(r(STOP2 + 0.35), toon={**CL2STOP(), 'sq': [1.0, 1.0, 1.0], 'face': CLF}, toonDur=0.1),
        k(r(PER2 - 0.05), look='camera', lookDur=0.15),
        k(r(PER2 - 0.05), toon={**CL2CAL(-0.1), 'face': CLF}, toonDur=0.22, toonEase='inOut'),
        k(r(PER2 + 0.25), toon={**CL2CAL(), 'face': {**CLF, 'brow': 0.3}}, toonDur=0.12, toonEase='out')]
for j in range(6): CLK2.append(k(r(SIX2 + 0.04 + 0.17 * j), toon={**CL2CAL(0.015 if j % 2 else -0.01), 'face': {**CLF, 'brow': 0.3}}, toonDur=0.08))
CALK2 = [k(0.0, scale=0.01, dur=0.0), k(r(PER2 - 0.05), to=add(CAL2, [0, -0.1, 0]), dur=0.0), k(r(PER2 - 0.05), scale=1.6, dur=0.0), k(r(PER2), to=CAL2, dur=0.3, ease='out')]
st.shot('S02', 'grassland', setOpts=SET, look=SUNF,
        actors=[H2.actor(), act('greffiere', CL2, RYCL2, 'stand', 'neutral', keys=CLK2), act('pote1', add(FR2A, [-1.5, 0, 0.35]), 60, 'run', 'happy', keys=FRK(FR2A, 0)), act('pote2', add(FR2B, [-1.5, 0, 0.35]), 60, 'run', 'happy', keys=FRK(FR2B, 1))],
        props=[WORLD(2), GULLS(2), SHADES('lun2', H2), *BURIED(2, crabs=[([[0.0, 0.45, 0.3], [1.2, 0.5, 0.25], [2.5, 0.45, 0.32]], [1.6], 0.24)]), P('certificat2', 'plCertificate', pos=CERT, ry=-22, opts={'w': 0.36, 'lean': 0.12}),
               SPADE('pelle2a', 'pote1'), SPADE('pelle2b', 'pote2', col='#2F62B5'),
               P('calendrier2', 'monthCalendar', pos=CAL2, ry=RYCL2, opts={'months': ['JUILLET', 'AOÛT', 'SEPTEMBRE', 'OCTOBRE', 'NOVEMBRE', 'DÉCEMBRE', 'JANVIER'], 'flipAt': r(SIX2 + 0.04), 'dur': 0.17}, keys=CALK2)],
        cams=[C2])
for j in range(6): st.cue('sfx:paper', 'S02', r(SIX2 + 0.06 + 0.17 * j), 0.12)
st.cue('sfx:brake', 'S02', r(STOP2 - 0.05), 0.12); st.cue('sfx:boing', 'S02', r(SIX2 + 0.12), 0.1); WAVES('S02', D2)

# 3: the funeral on the spot; he gave the speech. Three-quarters from the front right, his head in the foreground on the right; on the left four
#    mourners in black stand in one straight row going back, all heads visible, each under a black beach parasol planted behind; they dab their
#    cheeks with big white tissues (moving, below the eyes) and their shoulders heave; on « Il a fait le discours » he talks (lip flaps, orator's
#    nods, a stretch up on « discours »); two crabs now, a first row of sand blocks pops up round his head
D3 = st.dur('S03'); OBS3 = W('S03', 'L03', 0); IL3 = W('S03', 'L03', 3); DIS3 = W('S03', 'L03', 7)
MOURN = [('endeuille1', [-0.95, 0.0, -0.45]), ('endeuille2', [-1.45, 0.0, -1.2]), ('endeuille3', [-1.95, 0.0, -1.95]), ('endeuille4', [-2.45, 0.0, -2.7])]
F3 = [1.05, 0.95, 2.9]; L3 = [-1.0, 1.15, -1.2]
C3 = cam(0.0, F3, add(F3, [-0.05, 0.0, -0.15]), L3, add(L3, [0.03, 0, 0]), lens=50, ease='inOut')
pts3 = {n: add(p, [0, 2.3, 0]) for n, p in MOURN}; pts3.update({n + 'f': p for n, p in MOURN[:1]}); pts3.update({'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'parasol4': add(MOURN[3][1], [-0.4, 2.3, -0.4])})
chkc('S03', C3, pts3)
H3 = Head('S03')
H3.pose(0.0, FACE0, dur=0.0).look(0.0, add(MOURN[1][1], [0, 1.9, 0]), 0.0).breathe(0.05, r(IL3 - 0.12), {**FACE0, 'mouth': 'line', 'brow': 0.5}, blinks=[0.55])
H3.pose(r(IL3 - 0.1), {**FACE0, 'mouth': 'line', 'brow': 0.7}, (0.95, 1.06, 1.0), (-0.12, 0.0, 0.0), dur=0.08)
H3.talk(IL3, r(DIS3 - 0.04), {**FACE0, 'brow': 0.7}, step=0.09)
H3.pose(r(DIS3 - 0.04), {**FACE0, 'mouth': 'open', 'jaw': 0.45, 'brow': 1.0}, (0.9, 1.18, 1.0), (-0.22, -0.1, 0.0), dur=0.08, ease='out')
H3.talk(r(DIS3 + 0.12), r(D3 - 0.25), {**FACE0, 'brow': 0.8}, step=0.1)
H3.pose(r(D3 - 0.22), {**FACE0, 'mouth': 'smile', 'brow': 0.5}, (1.0, 1.0, 1.0), (0.1, 0.0, 0.0), dur=0.12)
MF = {'expr': 'sad', 'exprW': 1.0, 'mouth': 'line_m6', 'brow': -0.4}
def MOURNK(i, p, ry):
    side = 'R'
    dab = lambda u: {'touch': {side: ['face', -0.42, 0.22 + 0.05 * u, 0.02, 1, 0.1]}, 'reach': {'L': R5(off(p, ry, 0.25, 0.15, 0.95), 1, 0.0)}, 'hands': {'R': 'open', 'L': 'rest'}, 'hip': 0}
    ks = [k(-0.4, look=[0.0, 0.6, 0.0]), k(0.0, toon={**dab(0), 'face': MF}, toonDur=0.0)]
    t_, j = 0.05 + 0.13 * i, 0
    while t_ < D3 - 0.08:
        sob = j % 4 in (1, 2)
        ks.append(k(r(t_), toon={**dab(1 if j % 2 else -1), 'sq': [1.04, 0.95, 1.04] if sob else [0.98, 1.03, 0.98], 'bend': {'spine': [0.12 if sob else 0.02, 0, 0, 1, None], 'neck': [0.18 if sob else 0.05, 0, 0, 1, None]}, 'face': {**MF, 'mouth': 'grimace' if sob else 'line_m6'}}, toonDur=0.16, toonEase='inOut'))
        t_ += 0.22; j += 1
    if i == 0: ks.append(k(r(DIS3 + 0.1), look='mec', lookDur=0.2))
    return ks
props3 = [WORLD(3), GULLS(3), SHADES('lun3', H3), *BURIED(3, add_=[0.45], crabs=[([[0.0, -0.45, 0.25], [0.4, -0.4, 0.2], [1.2, -0.42, 0.24]], [0.9], 0.24), ([[0.0, 0.48, 0.26], [0.7, 0.45, 0.22], [1.6, 0.5, 0.26]], [1.3], 0.2)])]
for i, (n, p) in enumerate(MOURN):
    props3 += [P(f'parasol3_{i}', 'parasol', pos=add(p, [-0.35, 0, -0.4]), opts={'radius': 0.9, 'height': 2.25, 'colors': ['#16171B', '#2A2C32'], 'open': 1}),
               P(f'mouchoir3_{i}', 'plTissue', on={'actor': n, 'hand': 'R', 'offset': [0.0, -0.06, 0.04]})]
st.shot('S03', 'grassland', setOpts=SET, look=SUNF, actors=[H3.actor(), *[act(n, p, r(yaw(p, [0.6, 0, 2.0]), 1), 'stand', 'sad', keys=MOURNK(i, p, r(yaw(p, [0.6, 0, 2.0]), 1))) for i, (n, p) in enumerate(MOURN)]],
        props=props3, cams=[C3])
st.cue('sfx:sniff', 'S03', 0.4, 0.1); st.cue('sfx:sniff', 'S03', 1.9, 0.1); WAVES('S03', D3)

# 4: they set a headstone on him; he said « a little more to the left ». Low in front: two undertakers in black carry a plain grey headstone (no
#    symbol, no text) in from behind and set it down just behind his head, a little to his right (thud); he talks (lip flaps) on « Un peu plus à
#    gauche », his eyes flick to his left and his chin nods that way twice; they lift it (squashed under the weight), shuffle one step to his left
#    and set it down (thud, it rocks): its crisp shadow drops onto him; he relaxes, satisfied (the head spreads wide, a long smile)
D4 = st.dur('S04'); POSE4 = W('S04', 'L04', 3); TOMB4 = W('S04', 'L04', 6); DIT4 = W('S04', 'L04', 9); UN4 = W('S04', 'L04', 10); GAU4 = W('S04', 'L04', 14)
LAND4 = r(TOMB4 + 0.05); LIFT4 = r(GAU4 + 0.3); SET4 = r(LIFT4 + 0.42)
U4A = lambda p: [r(p[0] - 0.72), 0.0, r(p[2] - 0.12)]
U4B = lambda p: [r(p[0] + 0.72), 0.0, r(p[2] - 0.12)]
F4 = [0.08, 0.72, 3.9]; L4 = [0.02, 0.95, -0.3]
C4 = cam(0.0, F4, add(F4, [0.0, 0.0, -0.25]), L4, add(L4, [0.0, 0.0, 0.0]), lens=54, ease='inOut')
chkc('S04', C4, {'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'stoneTop0': add(STONE0, [0, 1.46, 0]), 'stoneTop': add(STONE, [0, 1.46, 0]), 'uA0': add(U4A(STONE0), [0, 2.0, 0]), 'uB': add(U4B(STONE), [0, 2.0, 0]), 'uA0side': add(U4A(STONE0), [-0.3, 1.0, 0]), 'uBside': add(U4B(STONE), [0.3, 1.0, 0])})
H4 = Head('S04')
H4.pose(0.0, FACE0, dur=0.0).breathe(0.05, r(LAND4 - 0.05), FACE0)
H4.pose(LAND4, {**FACE0, 'lid': 0.6, 'mouth': 'line'}, (1.12, 0.88, 1.05), dur=0.04, ease='out').pose(r(LAND4 + 0.1), {**FACE0, 'mouth': 'line', 'brow': 0.4}, (0.97, 1.04, 1.0), dur=0.08)
H4.breathe(r(LAND4 + 0.2), r(UN4 - 0.05), {**FACE0, 'mouth': 'line', 'brow': 0.1})
H4.talk(r(UN4 - 0.02), r(GAU4 + 0.25), {**FACE0, 'brow': 0.5}, step=0.09)
for j, t_ in enumerate([r(GAU4 - 0.02), r(GAU4 + 0.24)]):
    H4.pose(t_, {**FACE0, 'mouth': 'line', 'brow': 0.6, 'gx': -0.85}, (1.0, 1.04, 1.0), (0.12, -0.34, -0.2), dur=0.07, ease='out')
    H4.pose(r(t_ + 0.13), {**FACE0, 'mouth': 'line', 'brow': 0.5, 'gx': -0.7}, (1.0, 1.0, 1.0), (-0.02, -0.1, -0.1), dur=0.08)
H4.pose(r(SET4 + 0.04), {**FACE0, 'mouth': 'smile', 'brow': 0.3, 'lid': 0.5}, (1.16, 0.88, 1.05), (0.0, 0.0, 0.0), dur=0.12, ease='out')
H4.pose(r(SET4 + 0.25), {**FACE0, 'mouth': 'smile', 'brow': 0.4, 'lid': 0.4}, (1.08, 0.94, 1.03), dur=0.14)
H4.breathe(r(SET4 + 0.42), D4, {**FACE0, 'mouth': 'smile', 'lid': 0.4})
UF = {'lid': 0.45, 'mouth': 'line', 'brow': -0.3}
STR = {'lid': 0.6, 'mouth': 'clench', 'brow': -0.7, 'sweat': 0.5}
STONEK = [k(0.0, to=add(STONE0, [0.0, 0.38, -0.25]), dur=0.0), k(0.05, to=add(STONE0, [0.0, 0.3, -0.08]), dur=r(TOMB4 - 0.12), ease='inOut'), k(r(TOMB4 - 0.07), to=STONE0, dur=0.12, ease='in'),
          k(r(LIFT4), to=add(STONE0, [0.0, 0.16, 0.0]), dur=0.12, ease='out'), k(r(LIFT4 + 0.14), to=add(STONE, [0.0, 0.18, 0.0]), dur=0.2, ease='inOut'), k(r(SET4 - 0.06), to=STONE, dur=0.06, ease='in')]
def stone_at(t_):
    if t_ < TOMB4 + 0.05: u = smooth_((t_ - 0.05) / max(0.01, TOMB4 - 0.12)); return lerp3(add(STONE0, [0, 0.38, -0.25]), add(STONE0, [0, 0.3, -0.08]), u) if t_ < TOMB4 - 0.07 else STONE0
    if t_ < LIFT4: return STONE0
    if t_ < LIFT4 + 0.14: return add(STONE0, [0, 0.16, 0])
    if t_ < SET4 - 0.06: return lerp3(add(STONE0, [0, 0.16, 0]), add(STONE, [0, 0.18, 0]), smooth_((t_ - LIFT4 - 0.14) / 0.2))
    return STONE
def smooth_(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
def UNDK(sd):
    # both mittens on the stone's side edge at waist height; their feet follow the stone (one glide per move)
    hold = lambda s_, dy=0.0: {'reach': {'R': R5(add(s_, [0.44 * sd, 0.95 + dy, 0.05]), 1, 0.0), 'L': R5(add(s_, [0.44 * sd, 0.72 + dy, -0.05]), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'hip': 0}
    base = U4A if sd < 0 else U4B
    ks = [k(-0.4, look=add(STONE0, [0, 1.0, 0])), k(0.0, toon={**hold(add(STONE0, [0, 0.38, -0.25])), 'sq': [1.08, 0.9, 1.08], 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': STR}, toonDur=0.0),
          k(0.0, to=base(add(STONE0, [0, 0, -0.08])), dur=0.0), k(0.05, to=base(STONE0), dur=r(TOMB4 - 0.05), glide=True, face=0 if sd < 0 else 0, ease='inOut')]
    t_ = 0.12
    while t_ < LIFT4 + 0.6:
        s_ = stone_at(t_); heavy = t_ < LAND4 or LIFT4 - 0.05 < t_ < SET4
        ks.append(k(r(t_), toon={**hold(s_), 'sq': [1.08, 0.9, 1.08] if heavy else [1.0, 1.0, 1.0], 'bend': {'spine': [0.35 if heavy else 0.22, 0, 0, 1, None]}, 'face': STR if heavy else UF}, toonDur=0.08))
        t_ += 0.1
    ks += [k(r(LIFT4 + 0.12), to=base(STONE), dur=0.3, glide=True, face=0, ease='inOut'),
           k(r(SET4 + 0.12), toon={'reach': {'R': R5(off(base(STONE), 0, 0.2, 0.2 * sd, 0.95), 1, 0.0)}, 'hands': {'R': 'open'}, 'sq': [0.95, 1.06, 0.95], 'face': {**UF, 'mouth': 'smile'}, 'hip': 0}, toonDur=0.15, toonEase='out'),
           k(r(SET4 + 0.3), look='camera', lookDur=0.15), *life(r(SET4 + 0.35), D4, UF, {'hip': 0}, blinks=[r(D4 - 0.3 - 0.1 * (sd > 0))])]
    if sd < 0: ks.insert(3, k(r(GAU4 + 0.05), look='mec', lookDur=0.12))
    return ks
st.shot('S04', 'grassland', setOpts=SET, look=SUNB, actors=[H4.actor(), act('croquemort1', U4A(STONE0), 0, 'stand', 'neutral', keys=UNDK(-1)), act('croquemort2', U4B(STONE0), 0, 'stand', 'neutral', keys=UNDK(1))],
        props=[WORLD(4), SHADES('lun4', H4), *BURIED(4, rows=1, add_=[1.1], crabs=[([[0.0, -0.45, 0.25], [0.8, -0.5, 0.22], [1.8, -0.44, 0.26]], [2.2], 0.24), ([[0.0, 0.5, 0.26], [1.4, 0.45, 0.25]], [0.6], 0.2)]),
               HSTONE('stele4', STONE0, keys=STONEK)],
        cams=[C4])
st.cue('thud', 'S04', LAND4, 0.25); st.cue('thud', 'S04', SET4, 0.25); st.cue('sfx:grunt', 'S04', r(LIFT4 - 0.02), 0.08); WAVES('S04', D4)

