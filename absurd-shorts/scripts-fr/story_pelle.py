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
TAN = {'S01': 0.0, 'S01b': 0.0, 'S02': 0.04, 'S03': 0.1, 'S04': 0.16, 'S05': 0.22, 'S06': 0.28, 'S07': 0.34, 'S11b': 0.44, 'S12': 0.52, 'S13': 0.62, 'S14': 0.66, 'S15': 0.7, 'S16': 0.78}
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
# noon over the sea, behind the headstone: its shadow falls on him; (stills 2) less fill so the shade reads crisp
SUNB = {'sunDir': [0.42, 0.8, -0.6], 'sun': 3.4, 'fill': 0.55}
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
P1A = [-0.72, 0.0, -0.62]; P1B = [0.72, 0.0, -0.62]; RY1A = 62; RY1B = -62
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
    up = lambda: {'reach': {'R': R5(off(p, ry, 0.45, 0.12 * sd, 1.0), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'hip': 0}
    dn = lambda: {'reach': {'R': R5(off(p, ry, 0.5, 0.12 * sd, 0.6), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'hip': 0}
    ks = [k(-0.4, look=[0.0, 1.1, 1.2]), k(0.0, clip='kneel'), k(0.0, toon={**up(), 'face': PF}, toonDur=0.0)]
    for i, t_ in enumerate(PATS1):
        ks += [k(r(t_ - 0.13 + ph), toon={**up(), 'sq': [0.95, 1.07, 0.95], 'bend': {'spine': [-0.1, 0, 0, 1, None]}, 'face': {**PF, 'brow': 0.6}}, toonDur=0.08, toonEase='out'),
               k(r(t_ - 0.03 + ph), toon={**dn(), 'sq': [1.1, 0.88, 1.1], 'bend': {'spine': [0.25, 0, 0, 1, None]}, 'face': {**PF, 'mouth': 'o' if i == len(PATS1) - 1 else 'smile'}}, toonDur=0.04, toonEase='in')]
    TUP = r(PATS1[-1] + 0.22)
    ks += [k(r(TUP - 0.06), toon={**up(), 'sq': [1.08, 0.9, 1.08], 'face': PF}, toonDur=0.06),
           k(TUP, clip='stand'), k(TUP, toon={'reach': {'R': R5(off(p, ry, 0.25, 0.3 * sd, 1.05), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'sq': [0.92, 1.1, 0.92], 'face': {**PF, 'mouth': 'bigsmile'}, 'hip': 0}, toonDur=0.12, toonEase='out'),
           k(r(TUP + 0.2), look='camera', lookDur=0.12),
           k(r(TUP + 0.18), to=add(p, [1.3 * sd, 0.0, -0.7]), dur=r(D1 - TUP + 0.4), clip='walk', face=r(110 * sd), ease='linear'),
           k(r(TUP + 0.25), toon={'reach': {'R': R5(add(p, [0.35 * sd, 0.95, 0.2]), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'face': PF, 'hip': 0}, toonDur=0.15)]
    return ks
def FREESPADE(pid, keys_pts, col, t_hide=None, tilt=0.0):
    # (stills 2) a spade attached to a mitten points along the forearm (two sticks crossing in front of his face): a free spade, blade down, whose
    # grip follows the reach points of the mitten at the same times (cycle 5: a tool whose orientation counts is a world prop, the hand guided on it)
    t0, p0 = keys_pts[0]
    ks = [k(r(t), to=list(pt), dur=d, ease='inOut') for t, pt, d in keys_pts[1:]]
    if t_hide is not None: ks.append(k(t_hide, scale=0.01, dur=0.0))
    return P(pid, 'plSpade', pos=list(p0), rot=[0.0, 0.0, tilt], opts={'color': col}, keys=ks)
def SP1(p, ry, sd, ph, col):
    upP, dnP = off(p, ry, 0.45, 0.12 * sd, 1.0), off(p, ry, 0.5, 0.12 * sd, 0.6)
    kp = [(0.0, upP)]
    for t_ in PATS1: kp += [(r(t_ - 0.13 + ph), upP, 0.08), (r(t_ - 0.03 + ph), dnP, 0.04)]
    kp.append((r(PATS1[-1] + 0.16), upP, 0.06))
    return FREESPADE(f'pelle1_{sd}', [kp[0]] + [(t, pt, d) for t, pt, d in kp[1:]], col, r(PATS1[-1] + 0.22), 0.35 * sd)
st.shot('S01', 'grassland', setOpts=SET, look=SUNF,
        actors=[H1.actor(), act('pote1', P1A, RY1A, 'kneel', 'happy', keys=POTE1K(P1A, RY1A, -1, 0.0)), act('pote2', P1B, RY1B, 'kneel', 'happy', keys=POTE1K(P1B, RY1B, 1, 0.03))],
        props=[WORLD(1), GULLS(1), SHADES('lun1', H1), *BURIED(1, mound={'pat': [[t_, -0.35 if i % 2 else 0.35, -0.15] for i, t_ in enumerate(PATS1)]},
                                                         crabs=[([[0.0, 0.42, 0.34], [0.5, 0.42, 0.34], [0.9, 0.5, 0.3], [1.3, 0.5, 0.3], [1.6, 0.4, 0.36]], [1.75], 0.24)]),
               SP1(P1A, RY1A, -1, 0.0, '#E8452E'), SP1(P1B, RY1B, 1, 0.03, '#2F62B5'),
               P('pelle1a', 'plSpade', on={'actor': 'pote1', 'hand': 'R', 'offset': [0.0, -0.02, 0.0]}, scale=0.01, opts={'color': '#E8452E'}, keys=[k(r(PATS1[-1] + 0.22), scale=1.0, dur=0.0)]),
               P('pelle1b', 'plSpade', on={'actor': 'pote2', 'hand': 'R', 'offset': [0.0, -0.02, 0.0]}, scale=0.01, opts={'color': '#2F62B5'}, keys=[k(r(PATS1[-1] + 0.22), scale=1.0, dur=0.0)]),
               P('serviette1a', 'plTowelRoll', on={'actor': 'pote1', 'joint': 'torso', 'offset': [0.0, 0.2, -0.16]}, opts={'colors': ['#E8742E', '#F4F1E8']}),
               P('serviette1b', 'plTowelRoll', on={'actor': 'pote2', 'joint': 'torso', 'offset': [0.0, 0.2, -0.16]}, opts={'colors': ['#2E8AC9', '#F4F1E8']})],
        cams=[C1])
for t_ in PATS1: st.cue('sfx:poof', 'S01', r(t_), 0.18)
st.cue('thud', 'S01', PATS1[-1], 0.15); WAVES('S01', D1); GULLCRY('S01', 1.5)

# 1b: for the town hall he is dead. Closer: the clerk in a plain grey suit kneels bent beside him (screen right) and props a big black-bordered
#     certificate (no text) on the mound beside his chin, facing us; she sits back on her heels and nods gravely on « mort »; DÉCÉDÉ stamps and his
#     head flattens under it (wide and short, held trembling) and re-inflates with a pop and an overshoot; his brows go up behind the glasses
D1b = st.dur('S01b'); MAI1b = W('S01b', 'L01', 10); MORT1b = W('S01b', 'L01', 13)
CLK = [0.78, 0.0, 0.12]; RYCLK = -45
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
CKEEP = lambda hr, sp=0.3: {'reach': {'R': R5(hr, 1, 0.0), 'L': R5(off(CLK, RYCLK, 0.3, 0.2, 0.55), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'bend': {'spine': [sp, 0, 0, 1, None]}, 'hip': 0}
CLKK = [k(-0.4, look='camera'), k(0.0, clip='kneel'), k(0.0, toon={**CKEEP(add(CERT, [0.12, 0.45, 0.06])), 'face': CF}, toonDur=0.0),
        k(0.25, toon={**CKEEP(add(CERT, [0.12, 0.4, 0.04]), 0.38), 'sq': [1.04, 0.96, 1.04], 'face': CF}, toonDur=0.15),
        k(0.55, toon={**CKEEP(add(CERT, [0.14, 0.42, 0.02]), 0.34), 'sq': [0.98, 1.02, 0.98], 'face': CF}, toonDur=0.1),
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
F2 = [0.65, 0.42, 3.1]; L2 = [-0.5, 0.8, -0.6]
C2 = cam(0.0, F2, add(F2, [-0.03, 0.0, -0.15]), L2, add(L2, [0.0, 0.0, 0.0]), lens=44, ease='inOut')
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
        props=[WORLD(2), GULLS(2), SHADES('lun2', H2), *BURIED(2, crabs=[([[0.0, 0.45, 0.3], [1.2, 0.5, 0.25], [2.5, 0.45, 0.32]], [1.6], 0.24)]),
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
MOURN = [('endeuille1', [-0.55, 0.0, -1.5]), ('endeuille2', [-1.15, 0.0, -1.75]), ('endeuille3', [-1.75, 0.0, -2.0]), ('endeuille4', [-2.35, 0.0, -2.25])]
F3 = [1.1, 0.64, 3.5]; L3 = [-0.54, 0.74, -0.4]
C3 = cam(0.0, F3, add(F3, [-0.05, 0.0, -0.15]), L3, add(L3, [0.03, 0, 0]), lens=44, ease='inOut')
pts3 = {n: add(p, [0, 2.3, 0]) for n, p in MOURN}; pts3.update({n + 'f': p for n, p in MOURN[:1]}); pts3.update({'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'parasol4': add(MOURN[3][1], [-0.4, 2.3, -0.4])})
chkc('S03', C3, pts3)
H3 = Head('S03')
H3.pose(0.0, FACE0, dur=0.0).look(0.0, [-0.5, 0.9, 1.4], 0.0).breathe(0.05, r(IL3 - 0.12), {**FACE0, 'mouth': 'line', 'brow': 0.5}, blinks=[0.55])
H3.pose(r(IL3 - 0.1), {**FACE0, 'mouth': 'line', 'brow': 0.7}, (0.95, 1.06, 1.0), (-0.12, 0.0, 0.0), dur=0.08)
H3.talk(IL3, r(DIS3 - 0.04), {**FACE0, 'brow': 0.7}, step=0.09)
H3.pose(r(DIS3 - 0.04), {**FACE0, 'mouth': 'open', 'jaw': 0.45, 'brow': 1.0}, (0.9, 1.18, 1.0), (-0.22, -0.1, 0.0), dur=0.08, ease='out')
H3.talk(r(DIS3 + 0.12), r(D3 - 0.25), {**FACE0, 'brow': 0.8}, step=0.1)
H3.pose(r(D3 - 0.22), {**FACE0, 'mouth': 'smile', 'brow': 0.5}, (1.0, 1.0, 1.0), (0.1, 0.0, 0.0), dur=0.12)
MF = {'expr': 'sad', 'exprW': 1.0, 'mouth': 'line_m6', 'brow': -0.4}
def MOURNK(i, p, ry):
    side = 'R'
    dab = lambda u: {'touch': {side: ['face', -0.2, 0.12 + 0.06 * u, 0.06, 1, 0.1]}, 'reach': {'L': R5(off(p, ry, 0.25, 0.15, 0.95), 1, 0.0)}, 'hands': {'R': 'open', 'L': 'rest'}, 'hip': 0}
    ks = [k(-0.4, look=[0.4, 1.0, 1.0]), k(0.0, toon={**dab(0), 'face': MF}, toonDur=0.0)]
    t_, j = 0.05 + 0.13 * i, 0
    while t_ < D3 - 0.08:
        sob = j % 4 in (1, 2)
        ks.append(k(r(t_), toon={**dab(1 if j % 2 else -1), 'sq': [1.04, 0.95, 1.04] if sob else [0.98, 1.03, 0.98], 'bend': {'spine': [0.12 if sob else 0.02, 0, 0, 1, None], 'neck': [0.18 if sob else 0.05, 0, 0, 1, None]}, 'face': {**MF, 'mouth': 'grimace' if sob else 'line_m6'}}, toonDur=0.16, toonEase='inOut'))
        t_ += 0.22; j += 1
    if i == 0: ks.append(k(r(DIS3 + 0.1), look='mec', lookDur=0.2))
    return ks
props3 = [WORLD(3), GULLS(3), SHADES('lun3', H3), *BURIED(3, add_=[0.45], crabs=[([[0.0, -0.45, 0.25], [0.4, -0.4, 0.2], [1.2, -0.42, 0.24]], [0.9], 0.24), ([[0.0, 0.48, 0.26], [0.7, 0.45, 0.22], [1.6, 0.5, 0.26]], [1.3], 0.2)])]
for i, (n, p) in enumerate(MOURN):
    props3 += [P(f'parasol3_{i}', 'parasol', pos=add(p, [-0.15, 0, -0.62]), opts={'radius': 0.6, 'height': 2.62, 'colors': ['#16171B', '#2A2C32'], 'open': 1}),
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
F4 = [0.0, 0.85, 5.6]; L4 = [0.0, 0.82, 0.0]
C4 = cam(0.0, F4, add(F4, [0.0, 0.0, -0.3]), L4, add(L4, [0.0, 0.0, 0.0]), lens=48, ease='inOut')
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
    ks = [k(-0.4, look=add(STONE0, [0, 1.7, 0.6])), k(0.0, toon={**hold(add(STONE0, [0, 0.38, -0.25])), 'sq': [1.08, 0.9, 1.08], 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': STR}, toonDur=0.0),
          k(0.0, to=base(add(STONE0, [0, 0, -0.08])), dur=0.0), k(0.05, to=base(STONE0), dur=r(TOMB4 - 0.05), glide=True, face=0 if sd < 0 else 0, ease='inOut')]
    t_ = 0.12
    while t_ < LIFT4 + 0.6:
        s_ = stone_at(t_); heavy = t_ < LAND4 or LIFT4 - 0.05 < t_ < SET4
        ks.append(k(r(t_), toon={**hold(s_), 'sq': [1.08, 0.9, 1.08] if heavy else [1.0, 1.0, 1.0], 'bend': {'spine': [0.35 if heavy else 0.22, 0, 0, 1, None]}, 'face': STR if heavy else UF}, toonDur=0.08))
        t_ += 0.1
    ks += [k(r(LIFT4 + 0.12), to=base(STONE), dur=0.3, glide=True, face=0, ease='inOut'),
           k(r(SET4 + 0.12), toon={'reach': {'R': R5(off(base(STONE), 0, 0.2, 0.2 * sd, 0.95), 1, 0.0)}, 'hands': {'R': 'open'}, 'sq': [0.95, 1.06, 0.95], 'face': {**UF, 'mouth': 'smile'}, 'hip': 0}, toonDur=0.15, toonEase='out'),
           k(r(SET4 + 0.3), look='camera', lookDur=0.15), *life(r(SET4 + 0.35), D4, UF, {'hip': 0}, blinks=[r(D4 - 0.3 - 0.1 * (sd > 0))])]
    if sd < 0: ks.insert(3, k(r(GAU4 + 0.05), look=[0.0, 1.2, 0.8], lookDur=0.12))
    return ks
F4B = [0.12, 0.6, 2.7]; L4B = [0.08, 0.72, 0.0]
C4B = glide([cam(r(SET4 - 0.12), F4B, add(F4B, [0.0, 0.0, -0.12]), L4B, L4B, lens=48, ease='out')], 0.3)
chkc('S04', C4B, {'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'stoneTop': add(STONE, [0, 1.46, 0])})
st.shot('S04', 'grassland', setOpts=SET, look=SUNB, actors=[H4.actor(), act('croquemort1', U4A(STONE0), 0, 'stand', 'neutral', keys=UNDK(-1)), act('croquemort2', U4B(STONE0), 0, 'stand', 'neutral', keys=UNDK(1))],
        props=[WORLD(4), SHADES('lun4', H4), *BURIED(4, rows=1, add_=[1.1], crabs=[([[0.0, -0.45, 0.25], [0.8, -0.5, 0.22], [1.8, -0.44, 0.26]], [2.2], 0.24), ([[0.0, 0.5, 0.26], [1.4, 0.45, 0.25]], [0.6], 0.2)]),
               HSTONE('stele4', STONE0, keys=STONEK)],
        cams=[C4, C4B])
st.cue('thud', 'S04', LAND4, 0.25); st.cue('thud', 'S04', SET4, 0.25); st.cue('sfx:grunt', 'S04', r(LIFT4 - 0.02), 0.08); WAVES('S04', D4)


# 5: it gives him shade; the best spot on the beach. Noon, medium and low: his head in the crisp cool shade of the headstone in the foreground on
#    the right, smiling; behind on the left two bright-red sunbathers sit back on their towels, sweating big drops, fanning themselves with a mitten
#    and shifting; on « Meilleure » he stretches up proud, chin high, and shimmies; a second row of blocks pops up round him; one step more tanned
D5 = st.dur('S05'); OMB5 = W('S05', 'L05', 4); MEI5 = W('S05', 'L05', 5); PLA5 = W('S05', 'L05', 9)
SB = [('rouge1', [-1.25, 0.0, -2.55], 18), ('rouge2', [-0.4, 0.0, -3.3], -8)]
F5 = [0.25, 0.62, 2.8]; L5 = [-0.25, 0.6, -0.6]
C5 = cam(0.0, F5, add(F5, [-0.03, 0.0, -0.15]), L5, add(L5, [0.0, 0.0, 0.0]), lens=44, ease='inOut')
chkc('S05', C5, {'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'stoneTop': add(STONE, [0, 1.46, 0]), 'sb1': add(SB[0][1], [0, 1.35, 0]), 'sb2': add(SB[1][1], [0, 1.35, 0]), 'sb1feet': add(SB[0][1], [0, 0.1, 0.6])})
H5 = Head('S05')
FS = {**FACE0, 'lid': 0.45, 'mouth': 'smile', 'brow': 0.3}
H5.pose(0.0, FS, dur=0.0).breathe(0.05, r(OMB5 - 0.05), FS)
H5.pose(OMB5, {**FS, 'lid': 0.6}, (1.1, 0.92, 1.03), (0.0, 0.12, 0.0), dur=0.12, ease='inOut').pose(r(OMB5 + 0.22), FS, (1.0, 1.0, 1.0), (0.0, -0.06, 0.0), dur=0.14)
H5.pose(r(MEI5 - 0.1), {**FS, 'lid': 0.5}, (1.06, 0.95, 1.0), (0.1, 0.0, 0.0), dur=0.07)
H5.pose(MEI5, {**FS, 'lid': 0.3, 'mouth': 'bigsmile', 'brow': 0.8}, (0.9, 1.16, 0.98), (-0.2, 0.0, 0.0), dur=0.09, ease='out')
for j in range(4): H5.pose(r(MEI5 + 0.18 + 0.13 * j), {**FS, 'lid': 0.3, 'mouth': 'bigsmile', 'brow': 0.8}, (0.92, 1.13, 0.98), (-0.18, 0.18 if j % 2 else -0.18, 0.0), dur=0.11, ease='inOut')
H5.pose(r(PLA5 + 0.05), {**FS, 'mouth': 'smile'}, (1.03, 0.98, 1.0), (-0.05, 0.0, 0.0), dur=0.15).breathe(r(PLA5 + 0.25), D5, FS)
HOT = {'lid': 0.5, 'mouth': 'open', 'brow': -0.5, 'sweat': 1.0}
def SBK(i, p, ry):
    fan = lambda u: {'reach': {'R': R5(off(p, ry, 0.42, -0.22 + 0.1 * u, 1.05 + 0.06 * u), 1, 0.0), 'L': R5(off(p, ry, -0.25, 0.35, 0.18), 1, 0.0)}, 'hands': {'R': 'open', 'L': 'open'}, 'hip': 0}
    ks = [k(-0.4, look='camera'), k(0.0, clip='sitFloor'), k(0.0, toon={**fan(0), 'bend': {'spine': [-0.25, 0, 0, 1, None]}, 'face': HOT}, toonDur=0.0, fx={'sweat': 1, 'sweatSize': 3})]
    t_, j = 0.05 + 0.07 * i, 0
    while t_ < D5 - 0.06:
        pant = j % 2 == 0
        ks.append(k(r(t_), toon={**fan(1 if pant else -1), 'sq': [1.04, 0.96, 1.04] if pant else [0.98, 1.03, 0.98], 'bend': {'spine': [-0.25 + (0.08 if j % 6 > 2 else 0.0), 0.06 * (1 if j % 6 > 2 else -1), 0, 1, None]}, 'face': {**HOT, 'mouth': 'open' if pant else 'o'}}, toonDur=0.1))
        t_ += 0.13; j += 1
    return ks
props5 = [WORLD(5), GULLS(5), SHADES('lun5', H5), *BURIED(5, rows=1, add_=[0.6], crabs=[([[0.0, -0.46, 0.24], [1.0, -0.42, 0.22], [2.2, -0.47, 0.25]], [1.4], 0.24), ([[0.0, 0.46, 0.25], [0.8, 0.5, 0.2], [2.4, 0.44, 0.27]], [0.5, 2.0], 0.2)]),
          HSTONE('stele5')]
for i, (n, p, ry) in enumerate(SB): props5 += [P(f'serviette5_{i}', 'beachTowel', pos=add(p, [0, 0.02, 0.2]), ry=ry, opts={'colors': [['#E8742E', '#F4F1E8'], ['#2E8AC9', '#F2C23A']][i]}),
                                             P(f'maillot5_{i}', 'plSwimTop', on={'actor': n, 'joint': 'torso'}, opts={'color': ['#2F62B5', '#E8B020'][i], 'w': [0.47, 0.54][i], 'd': [0.31, 0.44][i]}), P(f'slip5_{i}', 'plSwimBottom', on={'actor': n, 'joint': 'hips'}, opts={'color': ['#2F62B5', '#E8B020'][i], 'w': [0.47, 0.54][i], 'd': [0.32, 0.44][i]})]
st.shot('S05', 'grassland', setOpts=SET, look=SUNB, actors=[H5.actor(), *[act(n, p, ry, 'sitFloor', 'neutral', keys=SBK(i, p, ry)) for i, (n, p, ry) in enumerate(SB)]], props=props5, cams=[C5])
WAVES('S05', D5); GULLCRY('S05', 0.8); GULLCRY('S05', 2.1, 0.05)

# 6: his boss sent a wreath, and his replacement. Low in front and to the left: his boss (bald, grey beard, charcoal suit) walks in with a big funeral
#    wreath on its easel and sets it down beside him (thud, it bounces); the hero glances at it; the boss steps aside with an open-handed flourish and
#    shows a young man in a tie standing behind him with a box of office things, who gives a little wave at the lens; on « remplaçant » the hero
#    does a double take at him (blank look at us, then the head shoots up tall with an O mouth, held trembling, an overshoot, a deadpan settle)
D6 = st.dur('S06'); PAT6 = W('S06', 'L06', 1); COU6 = W('S06', 'L06', 5); ET6 = W('S06', 'L06', 6); REM6 = W('S06', 'L06', 8)
WR6 = [-0.66, 0.0, 0.12]
BO6A = [-2.1, 0.0, 0.3]; BO6B = [-1.12, 0.0, 0.02]; BO6C = [-1.8, 0.0, -0.45]
YM6 = [-1.6, 0.0, -1.5]
SETW6 = r(COU6 - 0.02); ASIDE6 = r(ET6 - 0.12)
F6 = [0.5, 0.62, 4.5]; L6 = [-0.62, 0.85, -0.25]
C6 = cam(0.0, F6, add(F6, [-0.03, 0.0, -0.18]), L6, add(L6, [0.0, 0.0, 0.0]), lens=48, ease='inOut')
chkc('S06', C6, {'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'wreath': add(WR6, [0, 1.36, 0]), 'bossA': add(BO6A, [0, 2.3, 0]), 'bossB': add(BO6B, [0, 2.3, 0]), 'bossC': add(BO6C, [0, 2.3, 0]), 'bossCside': add(BO6C, [-0.35, 1.0, 0]), 'ym': add(YM6, [0, 2.25, 0]), 'ymFeet': YM6})
H6 = Head('S06')
H6.pose(0.0, FACE0, dur=0.0).breathe(0.05, r(SETW6 - 0.05), FACE0, blinks=[0.45])
H6.look(r(SETW6 + 0.05), [-0.5, 0.8, 1.5], 0.12).pose(r(SETW6 + 0.05), {**FACE0, 'mouth': 'line', 'gx': -0.6, 'brow': 0.4}, (1.0, 1.03, 1.0), (0.0, 0.08, -0.15), dur=0.1)
H6.look(r(SETW6 + 0.45), 'camera', 0.12).pose(r(SETW6 + 0.45), {**FACE0, 'mouth': 'smile', 'brow': 0.5}, dur=0.1)
DT6 = r(REM6 + 0.12)
H6.look(r(DT6 - 0.3), [-0.7, 0.9, 1.4], 0.1).pose(r(DT6 - 0.3), {**FACE0, 'mouth': 'line', 'gx': -0.4}, (1.0, 1.0, 1.0), (0.0, 0.05, -0.12), dur=0.08)
H6.look(r(DT6 - 0.12), 'camera', 0.06).pose(r(DT6 - 0.12), {**FACE0, 'lid': 0.35, 'mouth': 'line', 'brow': 0.0}, dur=0.06)
H6.look(r(DT6 + 0.12), [-0.7, 0.9, 1.4], 0.04)
H6.pose(r(DT6 + 0.06), {'lid': 0.5, 'mouth': 'clench', 'brow': -0.5, 'noBlink': 1}, (1.14, 0.86, 1.04), dur=0.05)
H6.pose(r(DT6 + 0.12), {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0, 'gx': -0.5, 'noBlink': 1}, (0.78, 1.36, 0.95), (-0.08, 0.1, -0.15), dur=0.05, ease='out')
for j in range(4): H6.pose(r(DT6 + 0.2 + 0.05 * j), {'lid': 0.0, 'eye': 0.5, 'mouth': 'O', 'brow': 1.0, 'gx': -0.5, 'noBlink': 1}, (0.78 + (0.02 if j % 2 else -0.02), 1.36 + (-0.03 if j % 2 else 0.03), 0.95), (-0.08, 0.1, -0.15), dur=0.04)
H6.pose(r(DT6 + 0.45), {'lid': 0.2, 'mouth': 'o', 'brow': 0.6}, (1.08, 0.93, 1.0), dur=0.07, ease='out').pose(r(DT6 + 0.56), {'lid': 0.35, 'mouth': 'line', 'brow': 0.2}, dur=0.08)
H6.look(r(DT6 + 0.5), 'camera', 0.12)
BF = {'lid': 0.3, 'mouth': 'line', 'brow': -0.2}
WRK = lambda q: {'reach': {'L': R5(add(q, [0.32, 1.0, 0.05]), 1, 0.0), 'R': R5(add(q, [-0.32, 1.0, 0.05]), 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'hip': 0}
WRCARRY = add(BO6B, [0.45, 0.12, 0.25])
WRK6 = [k(0.0, to=add(BO6A, [0.5, 0.12, 0.25]), dur=0.0), k(0.0, to=WRCARRY, dur=r(SETW6 - 0.3), ease='inOut'), k(r(SETW6 - 0.25), to=add(WR6, [0, 0.12, 0]), dur=0.18, ease='inOut'), k(r(SETW6 - 0.05), to=WR6, dur=0.06, ease='in'), k(SETW6, squash=[1.1, 0.88, 1.1], dur=0.4)]
BOSSK = [k(-0.4, look=add(WR6, [0.3, 1.8, 0.8])), k(0.0, toon={**WRK(add(BO6A, [0.5, 0.12, 0.25])), 'sq': [1.05, 0.95, 1.05], 'bend': {'spine': [-0.12, 0, 0, 1, None]}, 'face': BF}, toonDur=0.0),
         k(0.0, to=BO6B, dur=r(SETW6 - 0.3), clip='walk', face=80, ease='inOut'),
         k(r(SETW6 - 0.32), toon={**WRK(WRCARRY), 'sq': [1.05, 0.95, 1.05], 'bend': {'spine': [-0.12, 0, 0, 1, None]}, 'face': BF}, toonDur=0.1),
         k(r(SETW6 - 0.25), toon={**WRK(add(WR6, [0, 0.12, 0])), 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': BF}, toonDur=0.18),
         k(r(SETW6 - 0.03), toon={**WRK(WR6), 'sq': [1.08, 0.9, 1.08], 'bend': {'spine': [0.45, 0, 0, 1, None]}, 'face': {**BF, 'mouth': 'o'}}, toonDur=0.05, toonEase='in'),
         k(r(SETW6 + 0.2), toon={'sq': [0.96, 1.05, 0.96], 'bend': {'spine': [-0.05, 0, 0, 1, None]}, 'face': BF, 'hip': 0}, toonDur=0.15, toonEase='out'),
         k(r(SETW6 + 0.25), look='camera', lookDur=0.15),
         k(r(ASIDE6 - 0.12), toon={'sq': [1.06, 0.94, 1.06], 'face': BF, 'hip': 0}, toonDur=0.08),
         k(ASIDE6, to=BO6C, dur=0.28, glide=True, face=45, ease='inOut'),
         k(ASIDE6, toon={'reach': {'L': R5(off(BO6C, 45, 0.45, -0.55, 1.3), 1, 0.0)}, 'hands': {'L': 'open'}, 'scl': {'handL': [1.3, 1.3, 1.3]}, 'sq': [0.92, 1.1, 0.92], 'bend': {'spine': [-0.12, -0.15, 0, 1, None]}, 'face': {**BF, 'mouth': 'smile', 'brow': 0.6}, 'hip': 0}, toonDur=0.14, toonEase='out'),
         k(r(ASIDE6 + 0.2), look=add(YM6, [0, 2.0, 0]), lookDur=0.15),
         *[k(r(ASIDE6 + 0.3 + 0.2 * j), toon={'reach': {'L': R5(off(BO6C, 45, 0.45, -0.55, 1.3 + (0.04 if j % 2 else -0.02)), 1, 0.0)}, 'hands': {'L': 'open'}, 'scl': {'handL': [1.3, 1.3, 1.3]}, 'sq': [0.98, 1.02, 0.98] if j % 2 else [1.0, 1.0, 1.0], 'face': {**BF, 'mouth': 'smile', 'brow': 0.6}, 'hip': 0}, toonDur=0.16, toonEase='inOut') for j in range(int((D6 - ASIDE6 - 0.3) / 0.2))]]
YMF = {'lid': 0.15, 'mouth': 'bigsmile', 'brow': 0.6}
YKEEP = lambda u=0.0: {'reach': {'L': R5(off(YM6, 0, 0.42, 0.2, 0.92), 1, 0.0), 'R': R5(off(YM6, 0, 0.32, -0.32, 1.45 + 0.06 * u), 1, 0.0)}, 'hands': {'L': 'open', 'R': 'open'}, 'hip': 0}
YMK = [k(-0.4, look='camera'), k(0.0, toon={'reach': {'L': R5(off(YM6, 0, 0.42, 0.2, 0.92), 1, 0.0), 'R': R5(off(YM6, 0, 0.42, -0.2, 0.92), 1, 0.0)}, 'hands': {'L': 'open', 'R': 'open'}, 'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.4}, 'hip': 0}, toonDur=0.0),
       *life(0.05, r(ASIDE6 + 0.3), {'lid': 0.2, 'mouth': 'smile', 'brow': 0.4}, {'reach': {'L': R5(off(YM6, 0, 0.42, 0.2, 0.92), 1, 0.0), 'R': R5(off(YM6, 0, 0.42, -0.2, 0.92), 1, 0.0)}, 'hands': {'L': 'open', 'R': 'open'}, 'hip': 0}, blinks=[0.8])]
YMK += [k(r(ASIDE6 + 0.32), toon={**YKEEP(), 'sq': [0.94, 1.08, 0.94], 'face': YMF}, toonDur=0.12, toonEase='out')]
for j in range(int((D6 - ASIDE6 - 0.45) / 0.14)): YMK.append(k(r(ASIDE6 + 0.45 + 0.14 * j), toon={**YKEEP(1 if j % 2 else -1), 'bend': {'foreR': [0.0, 0.35 if j % 2 else -0.35, 0, 1, None]}, 'face': YMF}, toonDur=0.1, toonEase='inOut'))
st.shot('S06', 'grassland', setOpts=SET, look=SUNB, actors=[H6.actor(), act('patron', BO6A, 80, 'walk', 'neutral', keys=BOSSK), act('remplacant', YM6, 0, 'stand', 'happy', keys=YMK)],
        props=[WORLD(6), GULLS(6), SHADES('lun6', H6), *BURIED(6, rows=2, crabs=[([[0.0, 0.46, 0.25], [1.0, 0.42, 0.22], [2.4, 0.47, 0.25]], [1.1], 0.24), ([[0.0, 0.3, 0.4], [1.5, 0.33, 0.38]], [2.3], 0.15)]), HSTONE('stele6'),
               P('couronne6', 'plWreath', pos=add(BO6A, [0.5, 0.12, 0.25]), ry=15, opts={'R': 0.34}, keys=WRK6),
               P('carton6', 'plOfficeBox', on={'actor': 'remplacant', 'joint': 'torso', 'offset': [0.0, -0.05, 0.36]})],
        cams=[C6])
st.cue('thud', 'S06', SETW6, 0.22); st.cue('whoosh', 'S06', r(DT6 + 0.1), 0.12, 0.25, 900, 3000); WAVES('S06', D6)

# 7: his wife rebuilt her life on the next towel. The same low camera: behind him the next towel along fills the background: his wife in a big
#    sunhat and a broad man with a moustache sit side by side on it, both reading one magazine held between them; on « serviette » she gives the
#    hero a little wave over it and the man puffs his chest; the hero blinks once, then deflates slowly (wide and short, a long sigh) and
#    re-inflates a little; a third row of blocks
D7 = st.dur('S07'); FEM7 = W('S07', 'L07', 1); SER7 = W('S07', 'L07', 8); COT7 = W('S07', 'L07', 10)
WF7 = [-1.5, 0.0, -2.1]; MN7 = [-0.78, 0.0, -2.28]; MAG7 = [-1.12, 0.84, -1.74]
F7 = [0.0, 0.7, 3.4]; L7 = [-0.5, 0.72, -1.25]
C7 = cam(0.0, F7, add(F7, [-0.02, 0.0, -0.15]), L7, add(L7, [0.0, 0.0, 0.0]), lens=48, ease='inOut')
chkc('S07', C7, {'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'wife': add(WF7, [0, 1.6, 0]), 'hat': add(WF7, [0, 1.65, 0]), 'man': add(MN7, [0, 1.45, 0]), 'mag': MAG7, 'stoneTop': add(STONE, [0, 1.46, 0])})
H7 = Head('S07')
F7F = {**FACE0, 'mouth': 'line', 'brow': 0.1}
H7.pose(0.0, F7F, dur=0.0).breathe(0.05, r(SER7 + 0.15), F7F, blinks=[r(SER7 + 0.25)])
H7.pose(r(COT7 - 0.1), {**F7F, 'lid': 0.5, 'mouth': 'line_m6', 'brow': -0.3}, (1.08, 0.92, 1.0), dur=0.12)
H7.pose(r(COT7 + 0.05), {**F7F, 'lid': 0.65, 'mouth': 'o', 'brow': -0.4}, (1.3, 0.7, 1.08), (0.15, 0.0, 0.0), dur=0.4, ease='inOut')
H7.pose(r(COT7 + 0.48), {**F7F, 'lid': 0.5, 'mouth': 'line_m6', 'brow': -0.2}, (1.14, 0.87, 1.03), (0.06, 0.0, 0.0), dur=0.12, ease='out')
WFF = {'lid': 0.2, 'mouth': 'smile', 'brow': 0.4}
MAGH = lambda who, sd, dy=0.0: R5(add(MAG7, [0.3 * sd, -0.12 + dy, 0.02]), 1, 0.0)
WFK = [k(-0.4, look=MAG7), k(0.0, clip='sitFloor'), k(0.0, toon={'reach': {'R': MAGH('w', -1), 'L': MAGH('w', -1, -0.1)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': WFF, 'hip': 0}, toonDur=0.0),
       *life(0.05, r(SER7 - 0.1), WFF, {'reach': {'R': MAGH('w', -1), 'L': MAGH('w', -1, -0.1)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'hip': 0}, blinks=[0.6]),
       k(r(SER7 - 0.1), look='mec', lookDur=0.15)]
WAVE7 = lambda u: {'reach': {'R': MAGH('w', -1), 'L': R5(off(WF7, 15, 0.3, 0.38, 1.42 + 0.05 * u), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'hip': 0}
WFK += [k(r(SER7 - 0.05 + 0.1 * j), toon={**WAVE7(1 if j % 2 else -1), 'bend': {'foreL': [0.0, 0.4 if j % 2 else -0.4, 0, 1, None]}, 'sq': [0.97, 1.04, 0.97] if j == 0 else [1.0, 1.0, 1.0], 'face': {**WFF, 'mouth': 'bigsmile'}}, toonDur=0.08) for j in range(6)]
WFK += [k(r(SER7 + 0.62), toon={'reach': {'R': MAGH('w', -1), 'L': MAGH('w', -1, -0.1)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': WFF, 'hip': 0}, toonDur=0.15), k(r(SER7 + 0.7), look=MAG7, lookDur=0.2)]
MNF = {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}
MNH = lambda: {'reach': {'L': MAGH('m', 1), 'R': MAGH('m', 1, -0.1)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'hip': 0}
MNK = [k(-0.4, look=MAG7), k(0.0, clip='sitFloor'), k(0.0, toon={**MNH(), 'face': MNF}, toonDur=0.0), *life(0.1, r(SER7 + 0.05), MNF, MNH(), ph=0.2, blinks=[1.1]),
       *beat(r(SER7 + 0.12), {**MNH(), 'bend': {'spine': [-0.15, 0, 0, 1.03, 1.6]}, 'sq': [1.08, 1.02, 1.08], 'face': {**MNF, 'mouth': 'smirk', 'brow': 0.7}}, antic={**MNH(), 'bend': {'spine': [0.15, 0, 0, 0.97, 0.9]}, 'face': MNF}, hold=0.35,
             over={**MNH(), 'face': MNF}, settle={**MNH(), 'bend': {'spine': [-0.06, 0, 0, 1.01, 1.25]}, 'face': {**MNF, 'mouth': 'smirk'}}),
       k(r(SER7 + 0.2), look='mec', lookDur=0.15), k(r(SER7 + 0.9), look=MAG7, lookDur=0.2)]
st.shot('S07', 'grassland', setOpts=SET, look=SUNB, actors=[H7.actor(), act('epouse', WF7, 15, 'sitFloor', 'happy', keys=WFK), act('costaud', MN7, -15, 'sitFloor', 'happy', keys=MNK)],
        props=[WORLD(7), GULLS(7), SHADES('lun7', H7), *BURIED(7, rows=2, add_=[0.9], crabs=[([[0.0, -0.46, 0.24], [0.9, -0.43, 0.22], [2.4, -0.46, 0.25]], [1.2], 0.24), ([[0.0, 0.47, 0.25], [1.4, 0.43, 0.24]], [0.4], 0.2), ([[0.0, 0.3, 0.42], [2.6, 0.36, 0.4]], [1.8], 0.14)]), HSTONE('stele7'),
               P('serviette7', 'beachTowel', pos=[-1.12, 0.02, -2.0], opts={'w': 1.7, 'd': 1.3, 'colors': ['#C9729A', '#F4F1E8']}), P('magazine7', 'plMagazine', pos=MAG7, rot=[-0.35, 0, 0]),
               P('chapeau7', 'plSunHat', on={'actor': 'epouse', 'joint': 'head', 'offset': [0, 0.5, 0], 'rot': [0.12, 0, 0.08]}),
               P('maillot7', 'plSwimTop', on={'actor': 'epouse', 'joint': 'torso'}, opts={'color': '#C8322A', 'w': 0.47, 'd': 0.31}), P('slip7', 'plSwimBottom', on={'actor': 'epouse', 'joint': 'hips'}, opts={'color': '#C8322A', 'w': 0.47, 'd': 0.32}),
               P('short7', 'plSwimBottom', on={'actor': 'costaud', 'joint': 'hips'}, opts={'color': '#2F62B5', 'w': 0.68, 'd': 0.5, 'h': 0.28}),
               P('moustache7', 'mustache3d', on={'actor': 'costaud', 'joint': 'head', 'offset': [0.0, 0.17, 0.1]}, scale=1.6)],
        cams=[C7])
st.cue('sfx:slideDownSlow', 'S07', r(COT7 + 0.05), 0.06); WAVES('S07', D7); GULLCRY('S07', 1.0)

# 8: his friends inherited his car. The seafront road, low on the near kerb: his red convertible comes at us three-quarters and passes, the two
#    friends in front grinning and waving, two plastic spades sticking up from the back seat; on « voiture » a cheerful honk and the whole car
#    squashes and stretches on it
D8 = st.dur('S08'); HER8 = W('S08', 'L08', 3); VOI8 = W('S08', 'L08', 6)
ROADZ = 18.6; CS = 1.25
CAR8A = [10.5, 0.0, ROADZ]; CAR8B = [-0.5, 0.0, ROADZ]
def carpt(c, loc): return [r(c[0] - loc[0] * CS), r(c[1] + loc[1] * CS), r(c[2] - loc[2] * CS)]
DRV8 = (0.15, 0.12, -0.4); PAS8 = (0.15, 0.12, 0.4); REAR8 = (-1.0, 0.61, 0.0)
HONK8 = r(VOI8 + 0.02)
F8 = [-5.6, 1.25, 15.9]; L8 = [5.0, 1.2, ROADZ]
C8 = cam(0.0, F8, add(F8, [-0.4, 0.0, 0.0]), L8, [0.6, 1.2, ROADZ], lens=40, ease='inOut')
mid8 = lerp3(CAR8A, CAR8B, VOI8 / D8)
chkc('S08', C8, {'carFrontA': add(CAR8A, [-2.7, 0.8, 0]), 'carBackA': add(CAR8A, [2.7, 0.8, 0]), 'drvA': add(carpt(CAR8A, DRV8), [0, 1.6, 0]), 'pasA': add(carpt(CAR8A, PAS8), [0, 1.6, 0])})
chk('S08@honk', lerp3(F8, add(F8, [-0.4, 0, 0]), VOI8 / D8), lerp3(L8, [0.6, 1.2, ROADZ], VOI8 / D8), 40, {'car': add(mid8, [0, 0.8, 0]), 'carFront': add(mid8, [-2.7, 0.8, 0]), 'carBack': add(mid8, [2.7, 0.8, 0]), 'drv': add(carpt(mid8, DRV8), [0, 1.65, 0]), 'pas': add(carpt(mid8, PAS8), [0, 1.65, 0])})
DRVF = {'lid': 0.1, 'mouth': 'bigsmile', 'brow': 0.6}
def RIDER(who, loc, sd):
    a, b = carpt(CAR8A, loc), carpt(CAR8B, loc)
    ks = [k(-0.4, look='camera'), k(0.0, to=a, dur=0.0), k(0.0, to=b, dur=D8, glide=True, face=-90, ease='linear'), k(0.0, toon={'face': DRVF, 'hip': 0}, toonDur=0.0)]
    for j in range(int(D8 / 0.12)):
        t_ = r(0.05 + 0.12 * j); p_ = lerp3(a, b, t_ / D8)
        ks.append(k(t_, toon={'reach': {'L' if sd > 0 else 'R': R5(add(p_, [0.0, 1.45 + (0.05 if j % 2 else 0.0), 0.25 * -sd * -1]), 1, 0.0)}, 'hands': {'L': 'open', 'R': 'open'}, 'bend': {'fore' + ('L' if sd > 0 else 'R'): [0.0, 0.4 if j % 2 else -0.4, 0, 1, None]}, 'sq': [1.0, 1.04 if j % 2 else 0.98, 1.0], 'face': DRVF, 'hip': 0}, toonDur=0.09))
    return ks
CARK8 = [k(0.0, to=CAR8B, dur=D8, ease='linear'), k(HONK8, squash=[0.88, 1.18, 0.9], dur=0.5)]
spadeK = lambda loc: [k(0.0, to=carpt(CAR8B, loc), dur=D8, ease='linear')]
st.shot('S08', 'grassland', setOpts=SET, look=SUNF,
        actors=[act('pote1', carpt(CAR8A, DRV8), -90, 'drive', 'happy', keys=RIDER('pote1', DRV8, -1)), act('pote2', carpt(CAR8A, PAS8), -90, 'drive', 'happy', keys=RIDER('pote2', PAS8, 1))],
        props=[WORLD(8), FRONT(8), GULLS(8, (0, 8, 20)), P('voiture8', 'convertible', pos=CAR8A, ry=180, scale=CS, opts={'color': '#C8322A', 'interior': '#F2E6CC', 'plate': 'PELLE 100'}, keys=CARK8),
               P('pelle8a', 'plSpade', pos=carpt(CAR8A, (-1.05, 1.25, -0.25)), rot=[0, 0, 0.25], opts={'color': '#E8452E'}, keys=spadeK((-1.05, 1.25, -0.25))), P('pelle8b', 'plSpade', pos=carpt(CAR8A, (-1.0, 1.25, 0.25)), rot=[0, 0, -0.2], opts={'color': '#2F62B5'}, keys=spadeK((-1.0, 1.25, 0.25)))],
        cams=[C8])
st.cue('engine', 'S08', 0.0, 0.2, D8); st.cue('sfx:honk', 'S08', HONK8, 0.3); st.cue('sfx:honk', 'S08', r(HONK8 + 0.32), 0.25)

# 9: the beach became a cemetery. From the beach toward the promenade: two workers in orange push a pair of tall black wrought-iron gates up from the
#    sand into the gap of the promenade wall (the leaves rise, the workers walk under them, stretched); on « cimetière » they clank upright and
#    shiver; the workers dust off their mittens; the ice-cream cart on the left in front, the lifeguard tower on the right behind
D9 = st.dur('S09'); PLA9 = W('S09', 'L09', 1); CIM9 = W('S09', 'L09', 5)
GZ = 14.6; GW = 2.8
UP9 = r(CIM9 - 0.02)
RISE9 = [[0.0, 0.0], [0.15, 0.02], [r(UP9 - 0.1), 0.86], [UP9, 1.0, 'lin']]
CART9 = [-1.9, 0.0, 12.2]; TOW9 = [2.3, 0.0, 13.0]
def rise_at(t_):
    if t_ <= RISE9[0][0]: return 0.0
    for i in range(1, len(RISE9)):
        if t_ < RISE9[i][0]:
            u = (t_ - RISE9[i - 1][0]) / (RISE9[i][0] - RISE9[i - 1][0]); u = u if len(RISE9[i]) > 2 else u * u * (3 - 2 * u)
            return RISE9[i - 1][1] + (RISE9[i][1] - RISE9[i - 1][1]) * u
    return RISE9[-1][1]
def leafpt(sd, u, along=1.5, x=0.7):
    a = u * PI / 2; return [r(sd * x), r(along * math.sin(a)), r(GZ - along * math.cos(a))]
F9 = [-1.5, 2.8, 1.2]; L9 = [0.0, 1.3, 13.0]
C9 = cam(0.0, F9, add(F9, [0.05, -0.05, 0.4]), L9, add(L9, [0, 0.0, 0]), lens=52, ease='inOut')
chkc('S09', C9, {'postL': [-1.61, 2.9, GZ], 'postR': [1.61, 2.9, GZ], 'leafFlat': [0.0, 0.05, 12.2], 'cart': add(CART9, [0, 2.3, 0]), 'cartL': add(CART9, [-0.6, 0.5, 0]), 'tower': add(TOW9, [0, 3.0, 0]), 'towerR': add(TOW9, [0.8, 1.0, 0]), 'w1': add(leafpt(-1, 0.6), [0, 0.9, -0.5]), 'w2': add(leafpt(1, 0.6), [0, 0.9, -0.5])})
WKF = {'lid': 0.5, 'mouth': 'clench', 'brow': -0.6, 'sweat': 0.4}
def WORKK(sd):
    ks = [k(-0.4, look=leafpt(sd, 0.3)), k(0.0, toon={'face': WKF, 'hip': 0}, toonDur=0.0)]
    t_ = 0.0
    while t_ < UP9 + 0.02:
        u = rise_at(t_); hp = leafpt(sd, u, 1.45, 0.75); feet = [r(sd * 0.78), 0.0, r(hp[2] - 0.62)]
        ks.append(k(r(t_), toon={'reach': {'L': R5(add(hp, [0.15, 0, 0]), 1, 0.0), 'R': R5(add(hp, [-0.15, 0, 0]), 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'sq': [1.06, 0.93, 1.06] if u < 0.5 else [0.95, 1.07, 0.95],
                                   'bend': {'spine': [r(0.55 - 0.6 * u, 3), 0, 0, 1, None]}, 'face': WKF}, toonDur=0.1))
        ks.append(k(r(t_), to=feet, dur=0.1, glide=True, face=0, ease='linear'))
        t_ += 0.1
    ks += [k(r(UP9 + 0.04), toon={'reach': {'L': R5(add(leafpt(sd, 1, 1.45, 0.75), [0.15, 0, -0.1]), 1, 0.0), 'R': R5(add(leafpt(sd, 1, 1.45, 0.75), [-0.15, 0, -0.1]), 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'sq': [0.9, 1.12, 0.9], 'face': {**WKF, 'mouth': 'o'}, 'hip': 0}, toonDur=0.05, toonEase='out'),
           k(r(UP9 + 0.25), to=[r(sd * 1.0), 0.0, r(GZ - 1.6)], dur=0.3, glide=True, face=r(-160 * sd), ease='inOut'),
           k(r(UP9 + 0.25), look='camera', lookDur=0.2)]
    for j in range(4): ks.append(k(r(UP9 + 0.3 + 0.1 * j), toon={'reach': {'L': R5([r(sd * 1.0 + 0.1), 1.05 + (0.05 if j % 2 else -0.03), r(GZ - 1.95)], 1, 0.0), 'R': R5([r(sd * 1.0 - 0.1), 1.05 + (-0.03 if j % 2 else 0.05), r(GZ - 1.95)], 1, 0.0)}, 'hands': {'L': 'open', 'R': 'open'}, 'face': {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}, 'hip': 0}, toonDur=0.08))
    return ks
st.shot('S09', 'grassland', setOpts=SET, look=SUNF, actors=[act('ouvrier1', [-0.78, 0.0, 11.8], 0, 'stand', 'neutral', keys=WORKK(-1)), act('ouvrier2', [0.78, 0.0, 11.8], 0, 'stand', 'neutral', keys=WORKK(1))],
        props=[WORLD(9), FRONT(9, gap=[-1.85, 1.85]), GULLS(9, (0, 9, 18)), P('grilles9', 'plGates', pos=[0, 0, GZ], ry=180, opts={'w': GW, 'h': 2.4, 'rise': RISE9, 'rattle': [[UP9, 0.05, 24, 5]]}),
               P('glaces9', 'iceCreamCart', pos=CART9, ry=160), P('tour9', 'plTower', pos=TOW9, ry=200)],
        cams=[C9])
st.cue('clang', 'S09', UP9, 0.3); st.cue('sfx:grunt', 'S09', 0.3, 0.07); st.cue('sfx:stretch', 'S09', 0.5, 0.08)

# 9b: spades are forbidden. At the gates: a guard in a dark green uniform and cap holds out a big galvanised bin; three children round it drop their
#     plastic spades in one after another (each lifts it high, lets go, the spade falls in, clunk, the bin bumps), then slump, chins on chests
D9b = st.dur('S09b'); PEL9b = W('S09b', 'L09', 7); INT9b = W('S09b', 'L09', 9)
GD = [0.1, 0.0, 13.25]; BIN = [0.1, 0.62, 12.78]
KIDS = [('enfant1', [0.62, 0.0, 12.7], -128, '#E8452E', 0.25), ('enfant2', [-0.45, 0.0, 12.7], 128, '#2F62B5', 0.62), ('enfant3', [-0.95, 0.0, 12.95], 150, '#F2C23A', 0.99)]
F9b = [0.8, 1.9, 7.25]; L9b = [-0.15, 1.1, 12.8]
C9b = cam(0.0, F9b, add(F9b, [-0.05, -0.02, 0.3]), L9b, add(L9b, [0, 0.0, 0]), lens=40, ease='inOut')
pts9b = {n: add(p, [0, 1.6, 0]) for n, p, *_ in KIDS}; pts9b.update({'guard': add(GD, [0, 2.4, 0]), 'bin': BIN, 'binTop': add(BIN, [0, 0.65, 0])})
chkc('S09b', C9b, pts9b)
GF9 = {'lid': 0.4, 'mouth': 'line', 'brow': -0.5}
BINH = lambda dy=0.0: {'reach': {'L': R5(add(BIN, [0.34, 0.5 + dy, 0.0]), 1, 0.0), 'R': R5(add(BIN, [-0.34, 0.5 + dy, 0.0]), 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'hip': 0}
GDK = [k(-0.4, look=add(BIN, [0, 0.7, 0])), k(0.0, toon={**BINH(), 'bend': {'spine': [0.12, 0, 0, 1, None]}, 'face': GF9}, toonDur=0.0)]
for _, _, _, _, td in KIDS: GDK += [k(r(td + 0.12), toon={**BINH(-0.04), 'sq': [1.04, 0.96, 1.04], 'bend': {'spine': [0.15, 0, 0, 1, None]}, 'face': GF9}, toonDur=0.04), k(r(td + 0.22), toon={**BINH(), 'bend': {'spine': [0.12, 0, 0, 1, None], 'neck': [0.25, 0, 0, 1, None]}, 'face': GF9}, toonDur=0.1)]
GDK.append(k(r(D9b - 0.4), look='camera', lookDur=0.15))
KF = {'lid': 0.3, 'mouth': 'line_m6', 'brow': -0.2, 'browTilt': 12}
props9b = [WORLD('9b'), FRONT('9b', gap=[-1.85, 1.85]), P('grilles9b', 'plGates', pos=[0, 0, GZ], ry=180, opts={'w': GW, 'h': 2.4}),
           P('poubelle9b', 'plBin', pos=add(BIN, [0, -0.0, 0]), opts={'r': 0.3, 'bump': [[r(td + 0.14), 0.07, 26, 7] for *_, td in KIDS]})]
def KIDK(n, p, ry, col, td):
    hold = off(p, ry, 0.42, 0.0, 1.0); over = add(lerp3(hold, BIN, 0.75), [0, 0.95, 0])
    ks = [k(-0.4, look=add(BIN, [0, 0.8, 0])), k(0.0, toon={'reach': {'R': R5(hold, 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'rest'}, 'face': KF, 'hip': 0}, toonDur=0.0),
          *life(0.05, r(td - 0.3), KF, {'reach': {'R': R5(hold, 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'rest'}, 'hip': 0}, ph=0.1 * (td > 0.5)),
          k(r(td - 0.28), toon={'reach': {'R': R5(add(over, [0, 0.15, 0]), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'rest'}, 'sq': [0.94, 1.08, 0.94], 'face': {**KF, 'mouth': 'grimace'}, 'hip': 0}, toonDur=0.2, toonEase='inOut'),
          k(r(td - 0.02), toon={'reach': {'R': R5(over, 1, 0.0)}, 'hands': {'R': 'open', 'L': 'rest'}, 'face': {**KF, 'lid': 0.6}, 'hip': 0}, toonDur=0.05),
          k(r(td + 0.18), toon={'reach': {'R': R5(off(p, ry, 0.2, -0.1, 0.75), 1, 0.0)}, 'hands': {'R': 'open', 'L': 'rest'}, 'sq': [1.12, 0.86, 1.12], 'bend': {'spine': [0.25, 0, 0, 1, None], 'neck': [0.45, 0, 0, 1, None]}, 'face': {**KF, 'lid': 0.55, 'mouth': 'line_m6', 'brow': -0.5}, 'hip': 0}, toonDur=0.18, toonEase='out'),
          k(r(td + 0.35), look='camera', lookDur=0.2)]
    sp = P(f'pelle9b_{n}', 'plSpade', pos=hold, ry=ry, opts={'color': col},
           keys=[k(r(td - 0.28), to=add(over, [0, 0.15, 0]), dur=0.2, ease='inOut'), k(r(td - 0.02), to=over, dur=0.05)] + [k(r(td + 0.2 * (u - 0.25)), to=lerp3(over, add(BIN, [0, 0.6, 0]), u * u), dur=0.05, ease='linear') for u in (0.25, 0.5, 0.75, 1.0)] + [k(r(td + 0.22), scale=0.01, dur=0.0)])
    return ks, sp
acts9b = [act('gardien', GD, 180, 'stand', 'neutral', keys=GDK)]
for n, p, ry, col, td in KIDS:
    ks, sp = KIDK(n, p, ry, col, td); acts9b.append(act(n, p, ry, 'stand', 'neutral', keys=ks)); props9b.append(sp)
    st.cue('thud', 'S09b', r(td + 0.2), 0.18); st.cue('sfx:bonk', 'S09b', r(td + 0.21), 0.12)
st.shot('S09b', 'grassland', setOpts=SET, look=SUNF, actors=acts9b, props=props9b, cams=[C9b])

# 10: the holidaymakers tan in mourning. From a crane above their feet: rows of holidaymakers on towels in black swimsuits, black veils and black
#     sunglasses, lying stiff on their backs, two sitting up in front fanning themselves in turn with black fans; a black beach ball rolls slowly
#     across the foreground
D10 = st.dur('S10'); BRO10 = W('S10', 'L10', 2); DEU10 = W('S10', 'L10', 4)
BX = 10.0
LIERS = [('vacancier1', [BX - 1.0, 0.0, -2.1]), ('vacancier2', [BX, 0.0, -2.2]), ('vacancier3', [BX + 1.0, 0.0, -2.1]), ('vacancier4', [BX + 0.3, 0.0, -0.6])]
FANS = [('vacancier5', [BX - 0.55, 0.0, -0.05], 10, 0.15), ('vacancier6', [BX + 0.62, 0.0, 0.3], -15, 0.95)]
F10 = [BX + 0.15, 3.6, 2.5]; L10 = [BX + 0.05, 0.3, -1.7]
C10 = cam(0.0, F10, add(F10, [0.0, -0.05, -0.2]), L10, add(L10, [0, 0.0, 0]), lens=50, ease='inOut')
pts10 = {n: add(p, [0, 0.25, -1.9]) for n, p in LIERS}; pts10.update({n + 'feet': add(p, [0, 0.1, 0.1]) for n, p in LIERS})
pts10.update({n: add(p, [0, 1.6, 0]) for n, p, *_ in FANS}); pts10.update({'ball0': [BX - 1.6, 0.25, 0.9], 'ball1': [BX + 1.6, 0.25, 0.9]})
chkc('S10', C10, pts10)
MRN = {'expr': 'sad', 'exprW': 1.0, 'mouth': 'line_m6', 'brow': -0.3}
def LIEK(i):
    ks = [k(0.0, look=None), k(0.0, toon={'lay': [-1.5, 0.0], 'face': MRN, 'hip': 0}, toonDur=0.0)]
    for j in range(int(D10 / 0.5)):
        t_ = r(0.1 + 0.5 * j + 0.11 * i); ks.append(k(t_, toon={'lay': [-1.5, 0.0], 'sq': [1.0, 1.0, 1.0 + (0.04 if j % 2 else -0.02)], 'face': {**MRN, 'lid': 0.55 if j % 3 == 2 else 0.2}, 'hip': 0}, toonDur=0.3, toonEase='inOut'))
    return ks
def FANK(p, ry, t0):
    hold = lambda u: {'reach': {'R': R5(off(p, ry, 0.38, -0.22, 1.12 + 0.05 * u), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'rest'}, 'hip': 0}
    ks = [k(-0.4, look='camera'), k(0.0, clip='sitFloor'), k(0.0, toon={**hold(0), 'face': MRN}, toonDur=0.0)]
    t_, j = 0.05, 0
    while t_ < D10 - 0.05:
        busy = t0 <= t_ < t0 + 0.75
        ks.append(k(r(t_), toon={**hold((1 if j % 2 else -1) if busy else 0), 'bend': {'foreR': [0.0, (0.45 if j % 2 else -0.45) if busy else 0.0, 0, 1, None], 'spine': [0.0, 0.05 * (1 if j % 2 else -1) if busy else 0.0, 0, 1, None]}, 'sq': [1.0, 1.02 if j % 2 else 0.99, 1.0], 'face': MRN}, toonDur=0.07))
        t_ += 0.08; j += 1
    return ks
SWF, SWM, SWB = {'w': 0.47, 'd': 0.31}, {'w': 0.5, 'd': 0.33}, {'w': 0.54, 'd': 0.44}
SWD = {'vacancier1': SWF, 'vacancier2': SWM, 'vacancier3': SWF, 'vacancier4': SWB, 'vacancier5': SWF, 'vacancier6': SWM}
props10 = [WORLD(10), GULLS(10, (BX, 7, -5)), P('ballon10', 'plBall', pos=[0, 0, 0], opts={'r': 0.26, 'path': [[0.0, BX - 1.15, 1.0], [D10, BX + 1.05, 0.85]]})]
for i, (n, p) in enumerate(LIERS):
    props10 += [P(f'serv10_{i}', 'beachTowel', pos=add(p, [0, 0.02, -0.85]), opts={'w': 0.9, 'd': 2.1, 'colors': ['#2A2C32', '#4A4C54']}), P(f'mail10_{i}', 'plSwimTop', on={'actor': n, 'joint': 'torso'}, opts=SWD[n]), P(f'slip10_{i}', 'plSwimBottom', on={'actor': n, 'joint': 'hips'}, opts=SWD[n]),
                P(f'lun10_{i}', 'plShades', on={'actor': n, 'joint': 'head', 'offset': [0.0, 0.0, 0.1]}, opts={'w': 0.3, 'tilt': -0.3, 'y0': 0.3, 'op': 0.95})]
    if i % 2 == 0: props10.append(P(f'voile10_{i}', 'plVeil', on={'actor': n, 'joint': 'head', 'offset': [0, 0.5, 0]}))
for i, (n, p, ry, t0) in enumerate(FANS):
    props10 += [P(f'servf10_{i}', 'beachTowel', pos=add(p, [0, 0.02, 0.3]), ry=ry, opts={'w': 0.9, 'd': 1.6, 'colors': ['#2A2C32', '#4A4C54']}), P(f'mailf10_{i}', 'plSwimTop', on={'actor': n, 'joint': 'torso'}, opts=SWD[n]), P(f'slipf10_{i}', 'plSwimBottom', on={'actor': n, 'joint': 'hips'}, opts=SWD[n]),
                P(f'lunf10_{i}', 'plShades', on={'actor': n, 'joint': 'head', 'offset': [0.0, 0.0, 0.1]}, opts={'w': 0.3, 'tilt': -0.3, 'y0': 0.3, 'op': 0.95}),
                P(f'eventail10_{i}', 'plFan', on={'actor': n, 'hand': 'R', 'offset': [0.0, -0.08, 0.02], 'face': 'camera'}, opts={'flap': [[t0, t0 + 0.75]]})]
    if i == 0: props10.append(P('voilef10', 'plVeil', on={'actor': n, 'joint': 'head', 'offset': [0, 0.5, 0]}))
st.shot('S10', 'grassland', setOpts=SET, look=SUNF, actors=[*[act(n, p, 0, 'stand', 'neutral', keys=LIEK(i)) for i, (n, p) in enumerate(LIERS)], *[act(n, p, ry, 'sitFloor', 'neutral', keys=FANK(p, ry, t0)) for n, p, ry, t0 in FANS]],
        props=props10, cams=[C10])
WAVES('S10', D10); st.cue('sfx:stepSoft', 'S10', 0.5, 0.06); st.cue('sfx:stepSoft', 'S10', 1.2, 0.06)

# 11: in the evening the gates are closed. Orange-pink sunset (not night), the seafront windows lit warm: from the beach, the guard behind the bars
#     walks both open leaves shut (arms spread wide, then together), clang on « grilles »; he snaps a big brass padlock on the meeting bars (pop,
#     the shackle drops), gives it a tug and a satisfied nod
D11 = st.dur('S11'); SOI11 = W('S11', 'L11', 1); FER11 = W('S11', 'L11', 3); GRI11 = W('S11', 'L11', 5)
SHUT11 = r(GRI11 - 0.02); LOCK11 = r(SHUT11 + 0.32); A11 = 1.15
SW11 = [[0.0, -A11], [r(FER11 - 0.12), -A11], [r(SHUT11 - 0.08), -0.12], [SHUT11, 0.0, 'lin']]
def sw_at(t_):
    if t_ <= SW11[0][0]: return SW11[0][1]
    for i in range(1, len(SW11)):
        if t_ < SW11[i][0]:
            u = (t_ - SW11[i - 1][0]) / (SW11[i][0] - SW11[i - 1][0]); u = u if len(SW11[i]) > 2 else u * u * (3 - 2 * u)
            return SW11[i - 1][1] + (SW11[i][1] - SW11[i - 1][1]) * u
    return SW11[-1][1]
def free_edge(sd, a, y=1.2, lw=GW / 2 - 0.04):
    xl = sd * GW / 2 - sd * lw * math.cos(abs(a)); zl = lw * math.sin(a)
    return [r(-xl), y, r(GZ - zl)]
GD11 = [0.0, 0.0, 15.35]
SUNSET = {'sun': 2.0, 'sunColor': '#FFB27A', 'sunDir': [-0.15, 0.3, -1.0], 'fill': 0.8}
SSET = {**SET, 'sky': ['#8A74B4', '#FFB28A'], 'clouds': 14}
F11 = [0.3, 1.6, 5.0]; L11 = [0.0, 1.9, 14.0]
C11 = cam(0.0, F11, add(F11, [-0.05, 0.0, 0.4]), L11, add(L11, [0, 0.0, 0]), lens=40, ease='inOut')
chkc('S11', C11, {'postL': [-1.61, 2.9, GZ], 'postR': [1.61, 2.9, GZ], 'guard': add(GD11, [0, 2.4, 0]), 'lock': [0.0, 1.14, GZ + 0.09], 'edgeOpen': free_edge(1, -A11), 'win': [-3.0, 5.0, 23.0]})
GF11 = {'lid': 0.35, 'mouth': 'line', 'brow': -0.3}
G11K = [k(-0.4, look=[0, 1.3, 13.0]), k(0.0, toon={'face': GF11, 'hip': 0}, toonDur=0.0)]
t_ = 0.0
while t_ < SHUT11 + 0.02:
    a = sw_at(t_); pL, pR = free_edge(-1, a), free_edge(1, a)
    G11K.append(k(r(t_), toon={'reach': {'L': R5(pR if pR[0] > 0 else pL, 1, 0.0), 'R': R5(pL if pR[0] > 0 else pR, 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'hose': 0.2, 'sq': [1.05, 0.96, 1.05] if a < -0.6 else [1.0, 1.0, 1.0], 'bend': {'spine': [0.15, 0, 0, 1, None]}, 'face': GF11}, toonDur=0.1))
    t_ += 0.1
G11K += [k(0.0, to=[0.0, 0.0, 16.05], dur=0.0), k(r(FER11 - 0.12), to=GD11, dur=r(SHUT11 - FER11 + 0.1), glide=True, face=180, ease='inOut'),
         k(r(SHUT11 + 0.02), toon={'reach': {'L': R5([0.12, 1.2, GZ + 0.12], 1, 0.0), 'R': R5([-0.12, 1.2, GZ + 0.12], 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'sq': [1.1, 0.88, 1.1], 'face': {**GF11, 'mouth': 'o'}, 'hip': 0}, toonDur=0.04, toonEase='out'),
         k(r(LOCK11 - 0.12), toon={'reach': {'R': R5([0.0, 1.05, GZ + 0.2], 1, 0.0), 'L': R5([0.25, 1.25, GZ + 0.12], 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [0.25, 0, 0, 1, None]}, 'face': GF11, 'hip': 0}, toonDur=0.1),
         k(r(LOCK11 + 0.12), toon={'reach': {'R': R5([0.0, 0.98, GZ + 0.22], 1, 0.0), 'L': R5([0.25, 1.25, GZ + 0.12], 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'sq': [1.04, 0.96, 1.04], 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': GF11, 'hip': 0}, toonDur=0.05),
         k(r(LOCK11 + 0.3), toon={'sq': [0.97, 1.04, 0.97], 'bend': {'neck': [0.35, 0, 0, 1, None]}, 'face': {**GF11, 'mouth': 'smirk'}, 'hip': 0}, toonDur=0.12, toonEase='inOut'),
         k(r(LOCK11 + 0.3), look='camera', lookDur=0.15),
         k(r(LOCK11 + 0.5), toon={'sq': [1.0, 1.0, 1.0], 'face': {**GF11, 'mouth': 'smirk'}, 'hip': 0}, toonDur=0.12)]
st.shot('S11', 'grassland', setOpts=SSET, look=SUNSET, actors=[act('gardien', [0.0, 0.0, 16.05], 180, 'stand', 'neutral', keys=G11K)],
        props=[WORLD(11, sunset=True, sunX=0.0), FRONT(11, gap=[-1.85, 1.85], lit=1, hide=[[-3.0, 3.0]], bw=6.0), P('grilles11', 'plGates', pos=[0, 0, GZ], ry=180, opts={'w': GW, 'h': 2.4, 'swing': SW11, 'rattle': [[SHUT11, 0.04, 24, 5], [r(LOCK11 + 0.12), 0.02, 24, 6]], 'lockAt': LOCK11, 'lockZ': -0.09})],
        cams=[C11])
st.cue('clang', 'S11', SHUT11, 0.32); st.cue('clack', 'S11', r(LOCK11 + 0.1), 0.25)

# 11b: he has the beach to himself. The empty beach at sunset, low in front: his head and the headstone dark against the bright pink sea and the
#      low sun; the crabs' wall has reached his ears; a long happy sigh: the head swells (a deep breath in, chin up), holds, then deflates long and
#      wide with an O mouth, and settles smiling
D11b = st.dur('S11b'); PLA11 = W('S11b', 'L11', 9); SEU11 = W('S11b', 'L11', 12)
F11b = [-0.55, 0.42, 3.0]; L11b = [0.15, 0.68, 0.0]
C11b = cam(0.0, F11b, add(F11b, [0.03, 0.0, -0.12]), L11b, add(L11b, [0.0, 0.0, 0]), lens=46, ease='inOut')
chkc('S11b', C11b, {'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'stoneTop': add(STONE, [0, 1.46, 0]), 'stoneL': add(STONE, [-0.41, 0.8, 0]), 'stoneR': add(STONE, [0.41, 0.8, 0])})
H11 = Head('S11b')
F11F = {**FACE0, 'lid': 0.5, 'mouth': 'smile', 'brow': 0.3}
IN11 = r(PLA11 - 0.15); OUT11 = r(SEU11 - 0.2)
H11.pose(0.0, F11F, dur=0.0).breathe(0.05, IN11, F11F)
H11.pose(IN11, {**F11F, 'lid': 0.3, 'mouth': 'o', 'brow': 0.7}, (1.2, 1.18, 1.1), (-0.18, 0.0, 0.0), dur=0.35, ease='inOut')
H11.pose(r(OUT11 - 0.05), {**F11F, 'lid': 0.35, 'mouth': 'o', 'brow': 0.8}, (1.22, 1.2, 1.1), (-0.2, 0.0, 0.0), dur=0.1)
H11.pose(OUT11, {**F11F, 'lid': 0.7, 'mouth': 'O', 'brow': 0.4}, (1.34, 0.72, 1.12), (0.12, 0.0, 0.0), dur=0.55, ease='inOut')
H11.pose(r(OUT11 + 0.6), {**F11F, 'lid': 0.65, 'mouth': 'bigsmile', 'brow': 0.4}, (1.12, 0.9, 1.04), (0.05, 0.08, 0.0), dur=0.15, ease='out')
H11.breathe(r(OUT11 + 0.8), D11b, {**F11F, 'lid': 0.65, 'mouth': 'smile'}, neck=(0.05, 0.0, 0.0))
SILH = {'sun': 2.2, 'sunColor': '#FFB27A', 'sunDir': [0.13, 0.15, -0.98], 'fill': 0.12, 'probe': 0.25, 'hemi': 0.25}
st.shot('S11b', 'grassland', setOpts=SSET, look=SILH, actors=[H11.actor()],
        props=[WORLD('11b', sunset=True, sunX=120.0, sunY=135.0, sunSize=110), SHADES('lun11b', H11), *BURIED('11b', rows=4, crabs=[([[0.0, -0.47, 0.25], [1.6, -0.44, 0.22]], [0.8], 0.24)]), HSTONE('stele11b')],
        cams=[C11b])
st.cue('sfx:gasp', 'S11b', IN11, 0.12); st.cue('gust', 'S11b', OUT11, 0.1, 0.8); st.cue('gust', 'S11b', 0.0, 0.05, 1.2)

# 12: only the tax office did not believe he was dead. Low, front right: a tax inspector in a grey suit and glasses crouches and tucks a fat kraft
#     envelope under his chin (it leans on the mound); the hero's sunglasses dip and his eyes cross down at it; the inspector springs up and thrusts
#     his own form at the lens (AVIS D'IMPOSITION, À PAYER), stretched toward us
D12 = st.dur('S12'); FIS12 = W('S12', 'L12', 2); MORT12 = W('S12', 'L12', 7)
IN12 = [0.66, 0.0, 0.32]; RYIN = -62
ENV12 = [0.02, 0.15, 0.3]
TUCK12 = r(FIS12 + 0.05); UP12 = r(MORT12 - 0.35)
FORM12 = [0.6, 0.95, 0.95]
F12 = [0.2, 0.72, 3.9]; L12 = [0.3, 0.8, 0.3]
C12 = cam(0.0, F12, add(F12, [0.0, 0.0, -0.15]), L12, add(L12, [0.0, 0.0, 0.0]), lens=48, ease='inOut')
chkc('S12', C12, {'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'env': ENV12, 'insp': add(IN12, [0, 1.45, 0]), 'inspUp': add(IN12, [0, 1.65, 0]), 'formTop': add(FORM12, [0, 0.31, 0]), 'formBot': add(FORM12, [0, -0.31, 0]), 'formR': add(FORM12, [0.23, 0, 0]), 'formL': add(FORM12, [-0.23, 0, 0])})
H12 = Head('S12')
F12F = {**FACE0, 'mouth': 'line', 'brow': 0.2}
H12.pose(0.0, F12F, dur=0.0).breathe(0.05, r(TUCK12 + 0.05), F12F)
H12.pose(r(TUCK12 + 0.12), {'lid': 0.0, 'eye': 0.3, 'cross': 1.0, 'gy': 0.8, 'mouth': 'o', 'brow': 0.6, 'noBlink': 1}, (0.96, 1.05, 1.0), (0.22, 0.0, 0.0), dur=0.12)
for j in range(3): H12.pose(r(TUCK12 + 0.3 + 0.12 * j), {'lid': 0.0, 'eye': 0.3, 'cross': 1.0, 'gy': 0.8, 'mouth': 'o', 'brow': 0.6, 'noBlink': 1}, (0.96, 1.05 + (0.02 if j % 2 else 0.0), 1.0), (0.24, 0.03 if j % 2 else -0.03, 0.0), dur=0.1)
H12.pose(r(UP12 + 0.12), {'lid': 0.1, 'eye': 0.2, 'mouth': 'line', 'brow': -0.4, 'gx': -0.3, 'gy': -0.3}, (1.0, 1.0, 1.0), (-0.08, 0.0, 0.0), dur=0.1)
H12.look(r(UP12 + 0.12), FORM12, 0.12).breathe(r(UP12 + 0.3), D12, {'lid': 0.1, 'eye': 0.2, 'mouth': 'line', 'brow': -0.4, 'gx': -0.3, 'gy': -0.3})
DIP12 = [[0.0, 0.0], [r(TUCK12 + 0.05), 0.0], [r(TUCK12 + 0.16), 0.085], [r(UP12 + 0.05), 0.085], [r(UP12 + 0.2), 0.0]]
IF12 = {'lid': 0.35, 'mouth': 'line', 'brow': -0.5}
INK = [k(-0.4, look='camera'), k(0.0, clip='kneel'), k(0.0, toon={'reach': {'R': R5(add(ENV12, [0.12, 0.22, 0.12]), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'rest'}, 'bend': {'spine': [0.45, 0, 0, 1, None]}, 'face': IF12, 'hip': 0}, toonDur=0.0),
       k(r(TUCK12 - 0.12), toon={'reach': {'R': R5(add(ENV12, [0.12, 0.08, 0.06]), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'rest'}, 'bend': {'spine': [0.55, 0, 0, 1, None]}, 'sq': [1.04, 0.96, 1.04], 'face': IF12, 'hip': 0}, toonDur=0.12),
       k(r(TUCK12 + 0.08), toon={'reach': {'R': R5(off(IN12, RYIN, 0.3, -0.2, 0.7), 1, 0.0)}, 'hands': {'R': 'open', 'L': 'rest'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'face': {**IF12, 'mouth': 'smirk'}, 'hip': 0}, toonDur=0.15),
       k(r(UP12 - 0.12), toon={'reach': {'R': R5(off(IN12, RYIN, 0.3, -0.2, 0.7), 1, 0.0)}, 'hands': {'R': 'open', 'L': 'rest'}, 'sq': [1.1, 0.88, 1.1], 'bend': {'spine': [0.4, 0, 0, 1, None]}, 'face': IF12, 'hip': 0}, toonDur=0.08),
       k(UP12, to=IN12, dur=0.18, glide=True, face=-30, ease='out'),
       k(UP12, toon={'reach': {'L': R5(add(FORM12, [0.22, -0.18, -0.04]), 1, 0.0), 'R': R5(add(FORM12, [-0.22, -0.18, -0.04]), 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'hose': 0.15, 'sq': [0.88, 1.16, 0.88], 'bend': {'spine': [-0.12, 0, 0, 1.08, None]}, 'face': {**IF12, 'mouth': 'smile', 'brow': 0.4}, 'hip': 0}, toonDur=0.12, toonEase='out'),
       k(r(UP12 + 0.14), look='camera', lookDur=0.12)]
for j in range(4): INK.append(k(r(UP12 + 0.25 + 0.12 * j), toon={'reach': {'L': R5(add(FORM12, [0.22, -0.18 + (0.02 if j % 2 else 0.0), -0.04]), 1, 0.0), 'R': R5(add(FORM12, [-0.22, -0.18 + (0.02 if j % 2 else 0.0), -0.04]), 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [-0.08, 0, 0, 1.04, None]}, 'face': {**IF12, 'mouth': 'smile', 'brow': 0.4}, 'hip': 0}, toonDur=0.1))
ENVK = [k(0.0, to=add(ENV12, [0.12, 0.2, 0.12]), dur=0.0), k(r(TUCK12 - 0.12), to=ENV12, dur=0.14, ease='inOut')]
FORMK = [k(0.0, scale=0.01, dur=0.0), k(r(UP12 + 0.02), to=add(FORM12, [0.1, -0.3, -0.35]), dur=0.0), k(r(UP12 + 0.02), scale=1.0, dur=0.0), k(r(UP12 + 0.03), to=FORM12, dur=0.12, ease='out')]
st.shot('S12', 'grassland', setOpts=SET, look=SUNB, actors=[H12.actor(), act('inspecteur', IN12, RYIN, 'kneel', 'neutral', keys=INK)],
        props=[WORLD(12), GULLS(12), SHADES('lun12', H12, dip=DIP12), *BURIED(12, rows=4, crabs=[([[0.0, -0.46, 0.25], [1.4, -0.43, 0.22]], [1.0], 0.24), ([[0.0, 0.47, 0.2], [1.8, 0.42, 0.24]], [0.5], 0.2)]), HSTONE('stele12'),
               P('enveloppe12', 'plEnvelope', pos=add(ENV12, [0.12, 0.2, 0.12]), rot=[-0.95, 0, 0], opts={'w': 0.34, 'fat': 0.07}, keys=ENVK),
               P('avis12', 'plTaxForm', pos=FORM12, face='camera', scale=0.01, opts={'w': 0.46}, keys=FORMK)],
        cams=[C12])
st.cue('thud', 'S12', TUCK12, 0.15); st.cue('whoosh', 'S12', r(UP12 + 0.02), 0.12, 0.2, 800, 3500); WAVES('S12', D12)

# 13: six months later the permit came. Low in front: his red convertible skids up on the beach behind him in a spray of sand; the friends vault
#     out; one runs up and holds the permit up to the lens, a big red ACCORDÉ stamp pops on it; the other waves two spades over his head; the hero,
#     deeply tanned, grins and stretches up
D13 = st.dur('S13'); SIX13 = W('S13', 'L13', 0); PER13 = W('S13', 'L13', 4); ARR13 = W('S13', 'L13', 6)
CRY13 = 243; CAR13 = [-0.6, 0.0, -4.2]; CAR13A = [2.95, 0.0, -11.2]
def carptR(c, loc, ry):
    a = math.radians(ry); lx, ly, lz = loc[0] * CS, loc[1] * CS, loc[2] * CS
    return [r(c[0] + lx * math.cos(a) + lz * math.sin(a)), r(c[1] + ly), r(c[2] - lx * math.sin(a) + lz * math.cos(a))]
STOP13 = 0.5; JUMP13 = 0.55
PERM13 = [-0.4, 0.95, 0.8]; P13A = [-0.62, 0.0, 0.1]; P13B = [-1.7, 0.0, -1.6]
F13 = [-0.1, 0.7, 3.8]; L13 = [-0.68, 0.85, -0.3]
C13 = cam(0.0, F13, add(F13, [0.0, 0.0, -0.15]), L13, add(L13, [0.0, 0.0, 0.0]), lens=48, ease='inOut')
chkc('S13', C13, {'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'carF': carptR(CAR13, (2.2, 0.8, 0), CRY13), 'carB': carptR(CAR13, (-2.2, 0.8, 0), CRY13), 'permTop': add(PERM13, [0, 0.33, 0]), 'permBot': add(PERM13, [0, -0.33, 0]), 'permL': add(PERM13, [-0.25, 0, 0]), 'permR': add(PERM13, [0.25, 0, 0]),
                  'p1': add(P13A, [0, 1.55, 0]), 'p2': add(P13B, [0, 2.3, 0]), 'p2spades': add(P13B, [0, 2.9, 0])})
CARK13 = [k(0.0, to=CAR13A, dur=0.0), k(0.0, to=CAR13, dur=STOP13, ease='out'), k(r(STOP13 - 0.04), squash=[1.08, 0.86, 1.04], dur=0.45)]
def car13(loc, t_):
    u = min(1.0, t_ / STOP13); u = 1 - (1 - u) * (1 - u); c = lerp3(CAR13A, CAR13, u); return carptR(c, loc, CRY13)
def VAULT(who, loc, land, face_):
    ks = [k(-0.4, look='camera'), k(0.0, clip='drive'), k(0.0, to=car13(loc, 0), dur=0.0)]
    ks += [k(r(0.05 + 0.1 * j), to=car13(loc, r(0.15 + 0.1 * j)), dur=0.1, glide=True, face=CRY13 + 90, ease='linear') for j in range(5)]
    top = lerp3(car13(loc, STOP13), land, 0.5); top[1] = 1.0
    ks += [k(JUMP13, clip='stand'), k(JUMP13, to=top, dur=0.12, glide=True, face=face_, ease='out'), k(r(JUMP13 + 0.12), to=land, dur=0.12, glide=True, face=face_, ease='in'),
           k(JUMP13, toon={'sq': [0.88, 1.15, 0.88], 'face': {'lid': 0.1, 'mouth': 'bigsmile', 'brow': 0.8}, 'hip': 0, 'autoSq': 0}, toonDur=0.08, toonEase='out'),
           k(r(JUMP13 + 0.24), toon={'sq': [1.15, 0.86, 1.15], 'face': {'lid': 0.1, 'mouth': 'bigsmile', 'brow': 0.8}, 'hip': 0, 'autoSq': 0}, toonDur=0.04, toonEase='in')]
    return ks
GF13 = {'lid': 0.05, 'mouth': 'bigsmile', 'brow': 0.9}
PK13 = VAULT('pote1', DRV8, [-0.95, 0.0, -1.1], 20)
PERMH = lambda dy=0.0: {'reach': {'L': R5(add(PERM13, [0.26, -0.2 + dy, -0.03]), 1, 0.0), 'R': R5(add(PERM13, [-0.26, -0.2 + dy, -0.03]), 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'hose': 0.15, 'hip': 0, 'autoSq': 0.3}
RUN13 = r(JUMP13 + 0.3)
PK13 += [k(RUN13, to=P13A, dur=0.26, clip='run', face=15, ease='out'), k(r(RUN13 + 0.24), clip='kneel', blend=0.05),
         k(r(RUN13 + 0.12), toon={**PERMH(-0.25), 'sq': [0.95, 1.05, 0.95], 'face': GF13}, toonDur=0.12),
         k(r(PER13 - 0.04), toon={**PERMH(0.03), 'sq': [0.9, 1.12, 0.9], 'bend': {'spine': [0.12, 0, 0, 1.04, None]}, 'face': GF13}, toonDur=0.07, toonEase='out')]
for j in range(int((D13 - PER13 - 0.12) / 0.14)): PK13.append(k(r(PER13 + 0.12 + 0.14 * j), toon={**PERMH(0.02 if j % 2 else -0.01), 'sq': [1.0, 1.02 if j % 2 else 0.99, 1.0], 'face': GF13}, toonDur=0.1))
PK13.append(k(r(PER13 + 0.1), look='camera', lookDur=0.1))
PK13B = VAULT('pote2', PAS8, P13B, 25)
SPW = lambda u: {'reach': {'L': R5(off(P13B, 25, 0.2, 0.4 + 0.1 * u, 2.05), 1, 0.0), 'R': R5(off(P13B, 25, 0.2, -0.4 + 0.1 * u, 2.05), 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [-0.05, 0.1 * u, 0, 1, None]}, 'hose': 0.25, 'face': GF13, 'hip': 0, 'autoSq': 0}
for j in range(int((D13 - JUMP13 - 0.3) / 0.12)): PK13B.append(k(r(JUMP13 + 0.3 + 0.12 * j), toon={**SPW(1 if j % 2 else -1), 'sq': [0.97, 1.04, 0.97] if j % 2 else [1.02, 0.98, 1.02]}, toonDur=0.09))
H13 = Head('S13')
F13F = {**FACE0, 'mouth': 'bigsmile', 'brow': 0.6}
H13.pose(0.0, {**FACE0, 'mouth': 'o', 'brow': 0.6}, (1.0, 1.0, 1.0), dur=0.0).look(0.0, add(CAR13, [0, 1.0, 0]), 0.0)
H13.pose(r(STOP13 - 0.02), {**FACE0, 'mouth': 'O', 'brow': 0.9}, (1.15, 0.85, 1.05), (0.1, 0.0, -0.2), dur=0.05).pose(r(STOP13 + 0.12), {**FACE0, 'mouth': 'o', 'brow': 0.8}, (0.95, 1.06, 1.0), (0.0, 0.0, -0.2), dur=0.08)
H13.look(r(PER13 - 0.05), 'camera', 0.12).pose(r(PER13 + 0.02), F13F, (0.86, 1.22, 0.96), (-0.15, 0.0, 0.0), dur=0.08, ease='out').pose(r(PER13 + 0.2), F13F, (0.92, 1.12, 0.98), (-0.12, 0.0, 0.0), dur=0.1)
H13.breathe(r(PER13 + 0.35), D13, F13F, neck=(-0.1, 0.0, 0.0))
st.shot('S13', 'grassland', setOpts=SET, look=SUNF,
        actors=[H13.actor(), act('pote1', car13(DRV8, 0), CRY13 + 90, 'drive', 'happy', keys=PK13), act('pote2', car13(PAS8, 0), CRY13 + 90, 'drive', 'happy', keys=PK13B)],
        props=[WORLD(13), GULLS(13), SHADES('lun13', H13), *BURIED(13, rows=4, add_=[1.6], crabs=[([[0.0, -0.46, 0.25], [1.2, -0.42, 0.22], [2.0, -0.47, 0.25]], [0.6], 0.24), ([[0.0, 0.47, 0.22], [1.0, 0.43, 0.24]], [1.5], 0.2), ([[0.0, 0.32, 0.42], [2.0, 0.28, 0.44]], [1.0], 0.14)]),
               HSTONE('stele13'), P('voiture13', 'convertible', pos=CAR13A, ry=CRY13, scale=CS, opts={'color': '#C8322A', 'interior': '#F2E6CC', 'plate': 'PELLE 100'}, keys=CARK13),
               P('gerbe13', 'plSandSpray', pos=carptR(CAR13, (-1.4, 0.1, 0.0), CRY13), opts={'at': [0.3], 'n': 45, 's': 0.045, 'fwd': 0.6}),
               P('permis13', 'plPermit', pos=PERM13, face='camera', scale=0.01, opts={'w': 0.5, 'stampAt': r(PER13 + 0.05)}, keys=[k(r(RUN13 + 0.1), to=add(PERM13, [0, -0.3, -0.3]), dur=0.0), k(r(RUN13 + 0.1), scale=1.0, dur=0.0), k(r(RUN13 + 0.12), to=PERM13, dur=0.15, ease='out')]),
               P('pelle13a', 'plSpade', on={'actor': 'pote2', 'hand': 'L', 'offset': [0.0, -0.02, 0.0], 'rot': [PI, 0, 0]}, opts={'color': '#E8452E'}), P('pelle13b', 'plSpade', on={'actor': 'pote2', 'hand': 'R', 'offset': [0.0, -0.02, 0.0], 'rot': [PI, 0, 0]}, opts={'color': '#2F62B5'})],
        cams=[C13])
st.cue('engine', 'S13', 0.0, 0.18, 0.5); st.cue('sfx:brake', 'S13', 0.25, 0.2); st.cue('thud', 'S13', r(JUMP13 + 0.24), 0.15); st.cue('thud', 'S13', r(PER13 + 0.05), 0.28); st.cue('sfx:boing', 'S13', JUMP13, 0.08)

# 14: this man refused to come out. Low in front: the friends kneel either side and jab their spades into the mound; he shakes his head so hard
#     (a smear of whips, the head stretched wide) that the sand sprays over them; they freeze, spades at shoulder height, eyes squeezed, sand all
#     over their faces, shivering; then their eyes pop open (REFUSÉ); he settles, chin up, defiant
D14 = st.dur('S14'); REF14 = W('S14', 'L14', 3); SOR14 = W('S14', 'L14', 5)
P14A = [-0.62, 0.0, -0.32]; P14B = [0.62, 0.0, -0.32]
SH14 = r(REF14 - 0.12); FRZ14 = r(SH14 + 0.36)
F14 = [0.2, 0.62, 4.3]; L14 = [0.0, 0.66, 0.0]
C14 = cam(0.0, F14, add(F14, [0.0, 0.0, -0.1]), L14, add(L14, [0, 0.0, 0]), lens=50, ease='inOut')
chkc('S14', C14, {'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'p1': add(P14A, [0, 1.55, 0]), 'p2': add(P14B, [0, 1.55, 0]), 'p1spade': add(P14A, [0.2, 1.75, 0.3]), 'p2spade': add(P14B, [-0.2, 1.75, 0.3]), 'p1side': add(P14A, [-0.3, 0.8, 0])})
H14 = Head('S14')
F14F = {**FACE0, 'mouth': 'line', 'brow': -0.3}
H14.pose(0.0, F14F, dur=0.0)
for j, t_ in enumerate([0.1, 0.25]): H14.pose(t_, {**F14F, 'lid': 0.6}, (1.08, 0.94, 1.0), dur=0.04).pose(r(t_ + 0.08), F14F, dur=0.05)
H14.pose(r(SH14 - 0.1), {**F14F, 'mouth': 'clench', 'brow': -0.7}, (1.06, 0.94, 1.0), (0.1, 0.0, 0.0), dur=0.08)
for j in range(8): H14.pose(r(SH14 + 0.045 * j), {'lid': 0.6, 'mouth': 'grimace', 'brow': -0.8, 'noBlink': 1}, (1.22 if j % 2 else 1.18, 0.88, 1.0), (0.0, 0.1 * (1 if j % 2 else -1), 0.6 * (1 if j % 2 else -1)), dur=0.04)
H14.pose(r(SH14 + 0.38), {**F14F, 'mouth': 'smirk', 'brow': -0.6}, (0.9, 1.12, 0.98), (-0.18, 0.0, 0.0), dur=0.08, ease='out').pose(r(SH14 + 0.5), {**F14F, 'mouth': 'smirk', 'brow': -0.5}, (0.95, 1.06, 1.0), (-0.15, 0.0, 0.0), dur=0.1)
H14.breathe(r(SH14 + 0.65), D14, {**F14F, 'mouth': 'smirk', 'brow': -0.5}, neck=(-0.15, 0.0, 0.0))
def DIGK(p, ry, sd, ph):
    up = lambda: {'reach': {'R': R5(off(p, ry, 0.45, 0.12 * sd, 1.0), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'hip': 0}
    dn = lambda: {'reach': {'R': R5(off(p, ry, 0.55, 0.12 * sd, 0.5), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'hip': 0}
    frz = lambda u: {'reach': {'R': R5(off(p, ry, 0.38, 0.2 * sd, 1.1 + 0.015 * u), 1, 0.0), 'L': R5(off(p, ry, 0.3, -0.25 * sd, 1.15), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'hip': 0}
    FF_ = {'lid': 0.2, 'mouth': 'smile', 'brow': 0.4}
    ks = [k(-0.4, look=[0, 0.4, 0]), k(0.0, clip='kneel'), k(0.0, toon={**up(), 'face': FF_}, toonDur=0.0)]
    for t_ in (0.1 + ph, 0.25 + ph):
        ks += [k(r(t_ - 0.06), toon={**up(), 'sq': [0.95, 1.06, 0.95], 'face': FF_}, toonDur=0.05), k(r(t_), toon={**dn(), 'sq': [1.08, 0.9, 1.08], 'bend': {'spine': [0.4, 0, 0, 1, None]}, 'face': FF_}, toonDur=0.04, toonEase='in')]
    ks += [k(r(SH14 - 0.05), toon={**up(), 'face': {**FF_, 'mouth': 'o', 'brow': 0.6}}, toonDur=0.1),
           k(r(FRZ14 - 0.06), toon={**frz(0), 'sq': [1.1, 0.88, 1.1], 'bend': {'spine': [-0.15, 0, 0, 1, None]}, 'face': {'lid': 1.0, 'mouth': 'grimace', 'brow': -0.8, 'noBlink': 1}}, toonDur=0.04, toonEase='out')]
    for j in range(int((D14 - FRZ14) / 0.05)):
        t_ = r(FRZ14 + 0.05 * j); opened = t_ > SOR14 - 0.05
        ks.append(k(t_, toon={**frz(1 if j % 2 else -1), 'sq': [1.1 + (0.01 if j % 2 else -0.01), 0.88, 1.1], 'bend': {'spine': [-0.15, 0.02 * (1 if j % 2 else -1), 0, 1, None]},
                              'face': ({'lid': 0.0, 'eye': 0.45, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1} if opened else {'lid': 1.0, 'mouth': 'grimace', 'brow': -0.8, 'noBlink': 1})}, toonDur=0.04))
    ks.append(k(r(SOR14 - 0.05), look='camera', lookDur=0.06))
    return ks
def SP14(p, ry, sd, ph, col):
    upP, dnP, fzP = off(p, ry, 0.45, 0.12 * sd, 1.0), off(p, ry, 0.55, 0.12 * sd, 0.5), off(p, ry, 0.38, 0.2 * sd, 1.1)
    kp = [(0.0, upP)]
    for t_ in (0.1 + ph, 0.25 + ph): kp += [(r(t_ - 0.06), upP, 0.05), (r(t_), dnP, 0.04)]
    kp += [(r(SH14 - 0.05), upP, 0.1), (r(FRZ14 - 0.06), fzP, 0.04)]
    return FREESPADE(f'pelle14_{sd}', kp, col, None, 0.4 * sd)
st.shot('S14', 'grassland', setOpts=SET, look=SUNF, actors=[H14.actor(), act('pote1', P14A, 40, 'kneel', 'happy', keys=DIGK(P14A, 40, -1, 0.0)), act('pote2', P14B, -40, 'kneel', 'happy', keys=DIGK(P14B, -40, 1, 0.05))],
        props=[WORLD(14), SHADES('lun14', H14, wob=[[SH14, 0.14, 40, 5]]), *BURIED(14, rows=5, crabs=[([[0.0, -0.46, 0.3], [0.4, -0.5, 0.3], [0.5, -0.7, 0.5], [1.7, -0.72, 0.52]], [0.45], 0.24)]), HSTONE('stele14'),
               SP14(P14A, 40, -1, 0.0, '#E8452E'), SP14(P14B, -40, 1, 0.05, '#2F62B5'),
               P('gerbe14', 'plSandSpray', pos=[0.0, 0.42, 0.0], opts={'at': [r(SH14 + 0.05), r(SH14 + 0.2)], 'n': 50, 's': 0.035, 'fwd': -0.6}),
               P('sable14a', 'plSandSpeck', on={'actor': 'pote1', 'joint': 'head', 'offset': [0.0, 0.28, 0.1]}, opts={'at': r(FRZ14 - 0.05)}), P('sable14b', 'plSandSpeck', on={'actor': 'pote2', 'joint': 'head', 'offset': [0.0, 0.28, 0.1]}, opts={'at': r(FRZ14 - 0.03)})],
        cams=[C14])
st.card('S14', 'REFUSÉ', at=r(REF14 + 0.02))
st.cue('sfx:cuff', 'S14', 0.1, 0.12); st.cue('sfx:cuff', 'S14', 0.25, 0.12); st.cue('whoosh', 'S14', SH14, 0.18, 0.35, 700, 3500); st.cue('sfx:poof', 'S14', r(SH14 + 0.08), 0.2); st.cue('sfx:poof', 'S14', r(SH14 + 0.22), 0.18)

# 15: he asked for a perpetual plot. Three-quarters from the left, low: the clerk from line 1 kneels by him with a clipboard; he talks (lip flaps,
#     head bobbing, a confident tilt); she writes, ticks a box with a flourish and nods gravely twice; a sixth row of blocks pops up behind him
D15 = st.dur('S15'); DEM15 = W('S15', 'L15', 2); CON15 = W('S15', 'L15', 4); PERP15 = W('S15', 'L15', 6)
CL15 = [0.72, 0.0, 0.18]; RYC15 = -72
CLIP15 = off(CL15, RYC15, 0.42, 0.05, 0.95)
TICK15 = r(PERP15 + 0.15)
F15 = [-0.5, 0.62, 3.6]; L15 = [0.3, 0.72, 0.1]
C15 = cam(0.0, F15, add(F15, [0.02, 0.0, -0.15]), L15, add(L15, [0.0, 0.0, 0.0]), lens=44, ease='inOut')
chkc('S15', C15, {'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'clerk': add(CL15, [0, 1.5, 0]), 'clip': CLIP15, 'clerkBack': add(CL15, [0.35, 0.9, -0.1]), 'stoneTop': add(STONE, [0, 1.46, 0])})
H15 = Head('S15')
H15.pose(0.0, {**FACE0, 'mouth': 'line'}, dur=0.0).look(0.0, [0.45, 0.9, 1.6], 0.0)
H15.talk(0.12, r(PERP15 + 0.55), {**FACE0, 'brow': 0.5, 'gx': -0.5}, step=0.1, nod=0.08)
H15.pose(r(PERP15 + 0.6), {**FACE0, 'mouth': 'smile', 'brow': 0.6}, (1.04, 1.04, 1.0), (-0.08, 0.15, -0.1), dur=0.12)
H15.look(r(PERP15 + 0.7), 'camera', 0.12).breathe(r(PERP15 + 0.8), D15, {**FACE0, 'mouth': 'smile'})
CF15 = {'lid': 0.4, 'mouth': 'line', 'brow': -0.1}
CK15 = lambda pen, nod=0.0, st_=0.25, sq=(1, 1, 1): {'reach': {'L': R5(add(CLIP15, [-0.1, -0.1, 0.0]), 1, 0.0), 'R': R5(pen, 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [st_, 0, 0, 1, None], 'neck': [nod, 0, 0, 1 + nod * 1.1, None]}, 'sq': list(sq), 'face': CF15, 'hip': 0}
CL15K = [k(-0.4, look='camera'), k(0.0, clip='kneel'), k(0.0, toon=CK15(add(CLIP15, [0.05, 0.02, 0.03])), toonDur=0.0)]
for j in range(int((TICK15 - 0.3) / 0.12)): CL15K.append(k(r(0.2 + 0.12 * j), toon=CK15(add(CLIP15, [0.05 + (0.04 if j % 2 else -0.03), 0.02 - 0.012 * (j % 5), 0.03])), toonDur=0.09))
CL15K += [k(r(TICK15 - 0.12), toon=CK15(add(CLIP15, [-0.02, 0.06, 0.06]), sq=(0.97, 1.04, 0.97)), toonDur=0.08), k(TICK15, toon=CK15(add(CLIP15, [0.0, -0.04, 0.03])), toonDur=0.04, toonEase='in'),
          k(r(TICK15 + 0.06), toon=CK15(add(CLIP15, [0.08, 0.06, 0.04])), toonDur=0.05, toonEase='out'),
          k(r(TICK15 + 0.2), look='camera', lookDur=0.15)]
for j in range(2):
    t_ = r(TICK15 + 0.3 + 0.42 * j)
    CL15K += [k(t_, toon={**CK15(add(CLIP15, [0.08, 0.0, 0.04]), 0.5, 0.3, (1.04, 0.95, 1.04)), 'face': {**CF15, 'lid': 0.6}}, toonDur=0.18, toonEase='inOut'),
              k(r(t_ + 0.22), toon={**CK15(add(CLIP15, [0.08, 0.0, 0.04]), -0.1, 0.25, (0.98, 1.03, 0.98)), 'face': CF15}, toonDur=0.1, toonEase='out')]
st.shot('S15', 'grassland', setOpts=SET, look=SUNB, actors=[H15.actor(), act('greffiere', CL15, RYC15, 'kneel', 'neutral', keys=CL15K)],
        props=[WORLD(15), GULLS(15), SHADES('lun15', H15), *BURIED(15, rows=5, add_=[0.7], crabs=[([[0.0, -0.46, 0.25], [1.0, -0.42, 0.22], [2.2, -0.47, 0.25]], [0.7], 0.24), ([[0.0, 0.28, 0.44], [1.6, 0.32, 0.42]], [1.4], 0.14)]), HSTONE('stele15'),
               P('bloc15', 'clipboardProp', pos=CLIP15, ry=RYC15, rot=[-0.7, 0, 0], scale=1.6)],
        cams=[C15])
st.cue('sfx:scratch', 'S15', r(TICK15 - 0.05), 0.08); WAVES('S15', D15); GULLCRY('S15', 1.7, 0.05)

# 16: in the shade. Tight and low: his head inside the finished crab-built sandcastle mausoleum, in the cool shade of the headstone; a nod (down,
#     then a flick up) sends the sunglasses sliding up onto his hair: two pale ovals on his deep tan; he looks at us, closes his eyes, blissful,
#     opens them again on us; behind him the two friends stand in the full sun, red, sweating, panting, holding their spades; waves lap; hold
D16 = st.dur('S16')
PF16A = [-1.2, 0.0, -3.3]; PF16B = [1.28, 0.0, -3.2]
NOD16 = 0.3; LIFT16 = r(NOD16 + 0.1); CLOSE16 = 1.05; OPEN16 = 1.62
F16 = [0.02, 0.6, 3.4]; L16 = [0.0, 0.62, 0.2]
C16 = cam(0.0, F16, add(F16, [0.0, 0.0, -0.45]), L16, add(L16, [0.0, 0.02, 0]), lens=48, ease='inOut')
chkc('S16', C16, {'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'lifted': [0, 0.9, 0], 'mausTop': [0, 1.2, 0.3], 'towerL': [-0.36, 1.2, 0.2], 'towerR': [0.36, 1.2, 0.2], 'fA': add(PF16A, [0, 2.3, 0]), 'fB': add(PF16B, [0, 2.3, 0]), 'fAside': add(PF16A, [-0.35, 1.0, 0])})
chkc('S16', C16, {'headTop': [0, 0.66, 0], 'chin': [0, 0.14, 0], 'fA': add(PF16A, [0, 2.3, 0]), 'fB': add(PF16B, [0, 2.3, 0])}, end=True)
H16 = Head('S16')
F16F = {**FACE0, 'lid': 0.4, 'mouth': 'smile', 'brow': 0.3}
H16.pose(0.0, F16F, dur=0.0).breathe(0.05, r(NOD16 - 0.1), F16F)
H16.pose(r(NOD16 - 0.08), {**F16F, 'lid': 0.5}, (1.06, 0.95, 1.0), (0.25, 0.0, 0.0), dur=0.08)
H16.pose(NOD16, {**F16F, 'lid': 0.2, 'brow': 0.7}, (0.94, 1.08, 0.98), (-0.22, 0.0, 0.0), dur=0.07, ease='out')
H16.pose(r(NOD16 + 0.16), {**F16F, 'lid': 0.2, 'brow': 0.6}, (1.0, 1.0, 1.0), (-0.05, 0.0, 0.0), dur=0.1)
H16.breathe(r(NOD16 + 0.3), r(CLOSE16 - 0.05), {**F16F, 'lid': 0.2, 'mouth': 'smile', 'brow': 0.5})
H16.pose(CLOSE16, {**F16F, 'lid': 1.0, 'mouth': 'bigsmile', 'brow': 0.6, 'noBlink': 1}, (1.1, 0.92, 1.03), (0.06, 0.08, 0.0), dur=0.2, ease='inOut')
H16.pose(r(CLOSE16 + 0.3), {**F16F, 'lid': 1.0, 'mouth': 'bigsmile', 'brow': 0.6, 'noBlink': 1}, (1.12, 0.9, 1.03), (0.06, 0.1, 0.0), dur=0.2, ease='inOut')
H16.pose(OPEN16, {**F16F, 'lid': 0.3, 'mouth': 'smile', 'brow': 0.5, 'noBlink': 1}, (1.02, 1.0, 1.0), (0.0, 0.04, 0.0), dur=0.12)
H16.pose(r(OPEN16 + 0.25), {**F16F, 'lid': 0.3, 'mouth': 'smile', 'brow': 0.5, 'noBlink': 1}, (1.0, 1.02, 1.0), (0.0, 0.0, 0.0), dur=0.2)
OVC = '#F4CCA4'
HOTF = {'lid': 0.55, 'mouth': 'open', 'brow': -0.6, 'sweat': 1.0}
def PANT(p, ry, ph, sd):
    keep = {'reach': {'R': R5(off(p, ry, 0.3, -0.2, 0.9), 1, 0.0), 'L': R5(off(p, ry, 0.3, 0.25, 0.85), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'hip': 0}
    keep['skin'] = {'color': '#E0503A', 'k': 0.75}
    ks = [k(-0.4, look='camera'), k(0.0, toon={**keep, 'face': HOTF}, toonDur=0.0, fx={'sweat': 1, 'sweatSize': 3})]
    t_, j = 0.05 + ph, 0
    while t_ < D16 - 0.05:
        ks.append(k(r(t_), toon={**keep, 'sq': [1.05, 0.95, 1.05] if j % 2 else [0.97, 1.04, 0.97], 'bend': {'spine': [0.15 if j % 2 else 0.05, 0, 0, 1, None], 'neck': [0.1 if j % 2 else -0.05, 0.05 * sd, 0, 1, None]}, 'face': {**HOTF, 'mouth': 'open' if j % 2 else 'o', 'lid': 0.65 if j % 4 == 3 else 0.55}}, toonDur=0.12))
        t_ += 0.16; j += 1
    return ks
st.shot('S16', 'grassland', setOpts=SET, look=SUNB,
        actors=[H16.actor(), act('pote1', PF16A, 15, 'stand', 'neutral', keys=PANT(PF16A, 15, 0.0, -1)), act('pote2', PF16B, -15, 'stand', 'neutral', keys=PANT(PF16B, -15, 0.07, 1))],
        props=[WORLD(16), GULLS(16), SHADES('lun16', H16, lift=[[0.0, 0.0], [LIFT16, 0.0], [r(LIFT16 + 0.16), 1.0]], op=0.97), P('mausolee16', 'plCrabWall', pos=[0, 0, 0], opts={'mausoleum': True, 'H': 0.72}),
               P('dune16', 'plMound', pos=[0, 0, 0]), HSTONE('stele16'),
               P('ovales16', 'plOvals', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={'color': OVC, 'eyes': [[-0.068, 0.37], [0.078, 0.258]], 'tilt': -0.2, 'ow': 0.15, 'oh': 0.105, 'sq': H16.sq, 'close': [[0.0, 0.0], [r(CLOSE16 + 0.1), 0.0], [r(CLOSE16 + 0.12), 1.0, 'lin'], [r(OPEN16 + 0.02), 1.0], [r(OPEN16 + 0.04), 0.0, 'lin']]}),
               P('crabe16', 'crab', pos=[0, 0, 0], opts={'path': [[0.0, 0.55, 0.42], [1.2, 0.5, 0.45], [2.0, 0.56, 0.42]], 'snap': [0.9], 's': 0.2}),
               SPADE('pelle16a', 'pote1'), SPADE('pelle16b', 'pote2', col='#2F62B5')],
        cams=[C16])
st.cue('sfx:whistle', 'S16', r(LIFT16 + 0.02), 0.05); WAVES('S16', D16); GULLCRY('S16', 1.3, 0.06)

print('\n'.join(CHECKS))

TOON = {'breathe': 1.7, 'holdLife': 1.6}
MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': TOON}
POTE1 = {'preset': 'tourist', 'seed': 10001, 'suit': '#E8742E', 'hat': 'none', 'hair': 'curly', 'hairColor': '#6A4A2A', 'facial': 'none', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.06}, 'toon': EX}
POTE2 = {'preset': 'sportif', 'seed': 10002, 'suit': '#F2C23A', 'pants': '#2F62B5', 'hair': 'spiky', 'hairColor': '#C9A24A', 'facial': 'none', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
RED = '#E0553C'
BLACKSUIT = {'outfit': 'suit', 'suit': '#2E3036', 'pants': '#2E3036', 'lapel': '#1E2026', 'shirt': '#F2F2EE', 'tie': '#16171B', 'cuff': '#2E3036', 'hat': 'none', 'glasses': False}
SWIM = {'naked': True, 'glasses': False, 'hat': 'none', 'suit': '#141418', 'pants': '#141418'}
st.write("La pelle", rig='toon', fingers=False, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'pote1': POTE1, 'pote2': POTE2,
    'greffiere': {'preset': 'femme', 'seed': 10003, 'suit': '#8E929A', 'lapel': '#6E727A', 'hair': 'bun', 'hairColor': '#3A2A20', 'glasses': True, 'build': {'width': 0.95, 'headWidth': 1.2, 'height': 0.95}, 'toon': EX},
    'croquemort1': {'preset': 'boss', 'seed': 10004, **BLACKSUIT, 'hair': 'slick', 'hairColor': '#2A2420', 'facial': 'mustache', 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.04}, 'toon': EX},
    'croquemort2': {'preset': 'boss', 'seed': 10005, **BLACKSUIT, 'hair': 'bald', 'facial': 'none', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.08}, 'toon': EX},
    'endeuille1': {'preset': 'femme', 'seed': 10006, 'suit': '#2E3036', 'lapel': '#1E2026', 'hair': 'bun', 'hairColor': '#5A3A28', 'glasses': False, 'build': {'width': 0.95, 'headWidth': 1.2, 'height': 0.95}, 'toon': EX},
    'endeuille2': {'preset': 'boss', 'seed': 10007, **BLACKSUIT, 'hair': 'receding', 'hairColor': '#9A9A96', 'facial': 'mustache', 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
    'endeuille3': {'preset': 'mamie', 'seed': 10008, 'suit': '#2E3036', 'lapel': '#1E2026', 'toon': EX},
    'endeuille4': {'preset': 'boss', 'seed': 10009, **BLACKSUIT, 'hair': 'afro', 'hairColor': '#2A1E18', 'skin': '#6A4430', 'faceRim': True, 'facial': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'rouge1': {'preset': 'femme', 'seed': 10010, **SWIM, 'suit': '#2F62B5', 'skin': RED, 'hair': 'long', 'hairColor': '#C9A24A', 'build': {'width': 0.95, 'headWidth': 1.2, 'height': 0.95}, 'toon': EX},
    'rouge2': {'preset': 'boss', 'seed': 10011, **SWIM, 'skin': RED, 'hair': 'crew', 'hairColor': '#5A3A28', 'facial': 'none', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.12}, 'toon': EX},
    'patron': {'preset': 'boss', 'seed': 10012, 'suit': '#3E434C', 'lapel': '#2E333C', 'tie': '#7A2E3A', 'hair': 'bald', 'facial': 'beard', 'beardColor': '#9A9A96', 'glasses': False, 'build': {'width': 1.1, 'headWidth': 1.2, 'belly': 0.14}, 'toon': EX},
    'remplacant': {'preset': 'lemec_charcoal', 'seed': 10013, 'suit': '#A9A397', 'lapel': '#8E887C', 'tie': '#2F62B5', 'hair': 'slick', 'hairColor': '#D8B048', 'facial': 'none', 'glasses': False, 'build': {'width': 0.9, 'headWidth': 1.15}, 'toon': EX},
    'epouse': {'preset': 'femme', 'seed': 10014, **SWIM, 'suit': '#C8322A', 'skin': '#E8C09A', 'hair': 'long', 'hairColor': '#3A2418', 'lipstick': True, 'build': {'width': 0.95, 'headWidth': 1.2, 'height': 0.95}, 'toon': EX},
    'costaud': {'preset': 'boss', 'seed': 10015, **SWIM, 'skin': '#D9A07A', 'hair': 'curly', 'hairColor': '#2A1E18', 'facial': 'none', 'build': {'width': 1.4, 'headWidth': 1.15, 'belly': 0.16}, 'toon': EX},
    'ouvrier1': {'preset': 'worker', 'seed': 10016, 'hat': 'hardhat2', 'hair': 'bald', 'facial': 'mustache', 'suit': '#E07A2E', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX},
    'ouvrier2': {'preset': 'worker', 'seed': 10017, 'hat': 'hardhat2', 'hair': 'bald', 'facial': 'beard', 'beardColor': '#5A3A28', 'suit': '#E07A2E', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'gardien': {'preset': 'cop', 'seed': 10018, 'outfit': 'suit', 'suit': '#3E5A3A', 'pants': '#2E4A2A', 'lapel': '#2E4A2A', 'shirt': '#E4E8E0', 'tie': '#1E2A1E', 'cuff': '#3E5A3A', 'hat': 'maocap', 'hatColor': '#2E4A2A', 'hair': 'crew', 'facial': 'mustache', 'glasses': False, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
    'enfant1': {'preset': 'gamin', 'seed': 10019, 'suit': '#E8452E', 'hat': 'none', 'hair': 'curly', 'toon': EX}, 'enfant2': {'preset': 'gamin', 'seed': 10020, 'suit': '#2F8AC9', 'hat': 'none', 'hair': 'bun', 'hairColor': '#5A3A28', 'toon': EX},
    'enfant3': {'preset': 'gamin', 'seed': 10021, 'suit': '#5E8C4A', 'hat': 'none', 'hair': 'spiky', 'hairColor': '#C9A24A', 'skin': '#8A5A3A', 'faceRim': True, 'toon': EX},
    'vacancier1': {'preset': 'femme', 'seed': 10022, **SWIM, 'hair': 'long', 'hairColor': '#5A3A28', 'build': {'width': 0.95, 'headWidth': 1.2, 'height': 0.95}, 'toon': EX},
    'vacancier2': {'preset': 'boss', 'seed': 10023, **SWIM, 'hair': 'crew', 'hairColor': '#2A2420', 'facial': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'vacancier3': {'preset': 'femme', 'seed': 10024, **SWIM, 'skin': '#8A5A3A', 'faceRim': True, 'hair': 'bun', 'hairColor': '#2A1E18', 'build': {'width': 0.95, 'headWidth': 1.2, 'height': 0.95}, 'toon': EX},
    'vacancier4': {'preset': 'boss', 'seed': 10025, **SWIM, 'hair': 'receding', 'hairColor': '#9A9A96', 'facial': 'mustache', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.12}, 'toon': EX},
    'vacancier5': {'preset': 'femme', 'seed': 10026, **SWIM, 'hair': 'long', 'hairColor': '#C9A24A', 'build': {'width': 0.95, 'headWidth': 1.2, 'height': 0.95}, 'toon': EX},
    'vacancier6': {'preset': 'boss', 'seed': 10027, **SWIM, 'hair': 'curly', 'hairColor': '#3A2418', 'facial': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'inspecteur': {'preset': 'politique', 'seed': 10028, 'suit': '#8A8E96', 'lapel': '#6E727A', 'tie': '#2C3E5C', 'hairColor': '#4A4A48', 'glasses': True, 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
})
