#!/usr/bin/env python3
"""Le faux numéro (story 94, cycle 51; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man called his barber. Wrong number. He got the general staff. He asked: take the sides off well. The army evacuated both coasts. A little
shorter at the front: the front fell back ten kilometres. A village changed country; it noticed nothing. A little fade at the back: the
excavators cut the hinterland into steps. The parting in the middle: the country was cut in two; it still is. And a little gel: the government
froze the wages. Seen from space the country has a perfect haircut. Two jets held the mirror behind. This man said « perfect » and hung up. The
same day the general called the front. Wrong number. He got the barber: « Shave it all. » This man was in the chair. He only wanted the tips.
Staging: in his living room he holds a cream handset to his ear and pats the big messy tuft standing up on his box head (low push-in). In the war
room a general in plain khaki snaps up a big red desk phone beside a board standing on an easel and tilted to the lens: a made-up country (an
oval with soft bumps, no real outline) in thick green felt hair on a sea-blue ground; colonels in plain khaki with blank shoulder boards stand
at attention (no insignia, no rank, no flag). Over the general's shoulder, the same board for every order: two colonels run big clippers down
both edges (green tufts fly at the lens: the sides buzzed to sandy stubble); a half-second insert of the buzzed map; on the beach soldiers march
inland carrying calm sunbathers still lying on their deckchairs, the sea and one parasol left behind (DÉGAGÉ). A colonel trims the top edge
with giant scissors and a strip of felt drops; on a country road a column of soldiers walks backwards carrying a striped barrier and a plain
sentry box (tracking); in a village square the barrier passes behind three old men playing pétanque, nobody looks up, one throws. A colonel
kneels and combs the bottom of the map into four ridges; two army excavators finish carving a round green hill into four tidy steps, one calm
cow on each. A colonel draws the parting down the middle with the back of the comb while the generals lean in; from straight above a line of
tanks drives nose to tail through a dark forest, a bright earth stripe growing behind the lead tank from one coast to the other, then a static
hold. Insert: a colonel squeezes a giant gel tube onto the felt (it shines); at a factory gate a minister in a plain gold sash hands each worker
a big light-blue block of ice with a yellow pay envelope frozen inside; the workers hold them flat to the lens. Space: the same country seen from
above like the top of a hairdo (sandy shaved sides, four stepped ridges at the back, a dark parting, a white gel streak), held before COIFFÉ.
Wider: two plain jets, noses up, hold a giant oval hand mirror behind it, its glass painted with the stepped back. The living room, framing of
the first shot: he nods and hangs up, tuft still up. The war room, framing of the second shot: the general dials the red phone, a colonel with
the clippers beside him. The barber shop: the barber picks up the wall phone, freezes, snaps to attention, phone at his ear, clippers buzzing
at chest height; behind him the hero in the red chair under a striped cape, tuft up. Last: frontal and held, the hero alone in the chair, his
box head shaved smooth and shining, his tuft on the floor in front of him; behind him the barber in an army helmet at attention, clippers at his
chest. Nobody else is shaved.
Natural look; cycle 51: props_numero.js (feltBoard and hairCountry on one felt-hair core with every state, redDeskPhone, bigComb, gelTube,
heroTuft, plainCap, blankEpaulettes, fieldBarrier, sentryBox, villageSquare, terraceHill, excavator, forestStripe, factoryGate, iceBlock,
mirrorJets, barberShop, barberChair, barberCape, wallPhone); handset (props_flaque), chvClippers, chvShine (props_cheveu), bigScissors
(props_baillement), armyHelmet (props_guepe), plainTank (props_place), plainJet (props_chat, inside mirrorJets, its flank lettering hidden too),
deckChair (props_soleil), shades (props_feu), roadStrip (props_elan), breathPuffs (props_pizza), twinkle, softDust (props_barbecue), table,
boule (props.js) reused; office, livingRoom, beach, grassland, spaceDark, whiteVoid sets; cows as creatures.
Lessons applied from the start: `lens` is the vertical field; characters about 2.3 m tall with the box head; faces and key props above the caption
band (0.77-0.83), heads below the card band (0.07-0.18) on the two card shots; every camera checked with project() (CHECKS printed); every
extra cast entry has a preset; no insignia, rank, flag or lettering on any army thing (plain caps, blank shoulder boards, plainTank, plainJet
with the flank lettering hidden), the barrier in many short red and white bands, the sentry box plain, the minister's sash one plain colour, no
real country outline, no currency sign or logo on the envelopes, French only on screen (USINE, GEL); the barber stands at attention (no salute),
the clippers at his chest, the helmet clear of his eyes; only the hero is shaved; the sunbathers carried calm, nobody hurt; small props on
surfaces (the phones on tables, the tuft on the floor); no glow on faces; the jets and the mirror planned for 9:16 (jets noses up, the mirror
between them); animated materials unique; timedBurst not used; no flash; one clear cartoon extreme per shot (a pat that squashes the tuft and
the head, a stretch to the phone, tufts flying at the lens, a stretched arm across the map, hops, a hang-time boule, a comb stroke, a buckling
worker, a take and a snap to attention)."""
from story_kit import *
import math

st = Story('numero', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S04b', 'L04', 2), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0),
         ('S08', 'L08', 0), ('S09', 'L09', 0), ('S10', 'L10', 0), ('S11', 'L11', 0), ('S12', 'L12', 0), ('S12b', 'L12', 5), ('S13', 'L13', 0), ('S14', 'L14', 0),
         ('S15', 'L15', 0), ('S16', 'L16', 0), ('S17', 'L17', 0), ('S18', 'L18', 0)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]   # his right hand side (at -X when he faces +Z)
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
CHECKS = []
def chk(sid, c, pts):
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {project(c['from'], c['lookAt'], c['lens'], p)}" for n, p in pts.items()))
    if c.get('to'): CHECKS.append(f"{sid}(end): " + ' | '.join(f"{n} {project(c['to'], c.get('lookAt2') or c['lookAt'], c['lens'], p)}" for n, p in pts.items()))
def R5(p, w=1, s=0.04): return [*p, w, s]
EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
def TK(t, reach=None, hands=None, face=None, sq=None, bend=None, d=0.12, e='inOut', keep=False, scl=None):
    tn = {}
    if reach: tn['reach'] = reach
    if hands: tn['hands'] = hands
    if face: tn['face'] = face
    if sq: tn['sq'] = list(sq)
    if bend: tn['bend'] = bend
    if scl: tn['scl'] = scl
    return k(t, toon=tn, toonDur=d, toonEase=e, **({'keepPose': True} if keep else {}))
def blink(t, face): return [k(t, toon={'face': {**face, 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(t + 0.1), toon={'face': face}, toonDur=0.06, keepPose=True)]
def SP(a): return [a, 0, 0, 1, None]   # a bend value (pitch)
def BREATHE(t0, t1, every=0.55, a=0.012): return [k(r(t0 + i * every), toon={'sq': [1 - a * 0.5, 1 + a, 1 - a * 0.5] if i % 2 == 0 else [1, 1, 1]}, toonDur=r(every * 0.9), toonEase='inOut', keepPose=True) for i in range(int((t1 - t0) / every) + 1)]
ATT = {'lid': 0.3, 'mouth': 'line', 'brow': -0.4}   # at attention
DEAD = {'lid': 0.4, 'mouth': 'line'}
def ATTEN(p, ry):   # hands flat at the trouser seams, chin up
    return {'R': R5(off(p, ry, 0.04, 0.3, 0.98)), 'L': R5(off(p, ry, 0.04, -0.3, 0.98))}

# ---------------------------------------------------------------- the felt board (props_numero.feltBoard): copied geometry to aim the tools
BOARD = [0.0, 0, -1.0]; BW, BH, BHC, BTL = 1.6, 1.9, 1.15, 0.2
FELT = 0.006 + 0.09          # the front of the hair, from the board's plane
def shapeR(u, v): th = math.atan2(v, u); return 1 + 0.06 * math.sin(3 * th + 0.6) + 0.045 * math.sin(5 * th + 2.1) + 0.025 * math.sin(8 * th + 0.4)
def inside(u, v): return math.hypot(u / 0.9, v / 0.94) < shapeR(u, v)
def edge(v, s):   # the u of the country's edge at height v on side s (-1 left, +1 right)
    best = 0.0
    for i in range(401):
        u = s * i * 1.2 / 400
        if inside(u, v): best = u
    return best
def bpt(u, v, n=0.0, b=BOARD):   # a point of the map (u, v) n metres in front of the hair, in the world
    x, y, z = u * BW / 2, v * BH / 2, FELT + n
    return [r(b[0] + x), r(BHC + y * math.cos(BTL) + z * math.sin(BTL)), r(b[2] - y * math.sin(BTL) + z * math.cos(BTL))]
FULL = {}
DONE_SIDES = {'sides': 1.0}
DONE_TOP = {'sides': 1.0, 'top': 1.0}
DONE_BACK = {'sides': 1.0, 'top': 1.0, 'back': 1.0}
DONE_PART = {'sides': 1.0, 'top': 1.0, 'back': 1.0, 'part': 1.0}
DONE_ALL = {'state': 1}
def BOARDP(sid, **o): return P(f'carte{sid}', 'feltBoard', pos=BOARD, opts={'w': BW, 'h': BH, 'hc': BHC, 'tilt': BTL, **o})
OFFICE = {'door': False, 'printer': False, 'picture': False, 'carpet': False, 'wall': '#4A5866', 'band': '#2E3A46', 'trim': '#1E262E'}
WARLOOK = {'sunDir': [0.3, 0.8, 0.9]}
CAP = lambda pid, who, s=1.0: P(pid, 'plainCap', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}, opts={'w': 0.25 * s, 'd': 0.19 * s})
EPA = lambda pid, who: P(pid, 'blankEpaulettes', on={'actor': who, 'joint': 'torso', 'offset': [0.0, 0.42, 0.0]}, opts={'w': 0.5})
HELMET = lambda pid, who, **o: P(pid, 'softHelmet', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.46, 0.0]}, opts={'s': 0.95, **o})
def EAR(pid, who, side=1, color=None, **kw):   # a handset held at the ear (side 1: his right ear)
    return P(pid, 'handset', on={'actor': who, 'joint': 'head', 'offset': [-0.2 * side, 0.2, 0.03]}, opts={'len': 0.32, 'rot': [-0.35, r(PI / 2 * side), 0.0], **({'color': color} if color else {})}, **kw)

# war-room positions shared by the shots over the general's shoulder (S03, S05, S08, S10)
GEN_OS = [0.62, 0, 3.5]; RY_OS = yaw(GEN_OS, [0.0, 0, -1.0])
COL_L = [-1.22, 0, -0.78]; COL_R = [1.22, 0, -0.78]
RYL = yaw(COL_L, bpt(-0.5, 0.0)); RYR = yaw(COL_R, bpt(0.5, 0.0))
C_OS = cam(0.0, [0.35, 3.0, 6.0], [0.33, 2.95, 5.75], [0.05, 1.2, -1.0], [0.05, 1.2, -1.0], lens=44)
def OSGEN(sid, keys=()):   # the general in the foreground, back three-quarters, the red handset at his right ear
    return act('general', GEN_OS, RY_OS, 'stand', 'neutral', keys=[k(0.0, look=bpt(0, 0.1)), TK(0.0, {'R': R5(off(GEN_OS, RY_OS, 0.08, 0.27, 2.0)), 'L': R5(off(GEN_OS, RY_OS, 0.05, -0.3, 1.0))}, {'R': 'grip', 'L': 'rest'}, ATT, d=0.0), *keys])
def OSGENP(sid): return [EAR(f'tel{sid}', 'general', color='#D8262C'), CAP(f'cap{sid}', 'general', 1.05), EPA(f'epa{sid}', 'general')]

for g_ in [('S01', 1.15, 'mec', 'pat'), ('S02', 0.4, 'general', 'snap'), ('S03', 1.4, 'colL', 'buzz'), ('S04', 0.5, 'bain1', 'carried'), ('S05', 0.9, 'colL', 'snip'),
           ('S06', 1.0, 'sold1', 'backwards'), ('S07', 1.3, 'pet2', 'throw'), ('S08', 0.9, 'colL', 'comb'), ('S10', 0.6, 'colL', 'part'), ('S12b', 1.0, 'ouv1', 'buckle'),
           ('S15', 1.0, 'mec', 'parfait'), ('S16', 1.5, 'general', 'dial'), ('S17', 0.55, 'barbier', 'take'), ('S18', 2.0, 'mecChauve', 'tips')]:
    st.gag(*g_)

# ================================================================= the living room (S01, S15)
HERO = [0.0, 0, -1.4]
TABLE1 = [-0.62, 0, -1.0]; PHONEB = [-0.62, 1.2, -0.98]
C1 = cam(0.0, [0.15, 1.4, 2.4], [0.12, 1.43, 2.05], [-0.2, 1.8, -1.4], [-0.2, 1.82, -1.4], lens=42)
EARR = off(HERO, 0, 0.1, 0.3, 2.02)
TUFT = lambda pid, who, **o: P(pid, 'heroTuft', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.48, 0.0]}, opts={'s': 1.15, **o})
chk('S01', C1, {'face': add(HERO, [0, 2.05, 0]), 'tuftTop': add(HERO, [0, 2.75, 0]), 'phoneBase': PHONEB, 'hipL': add(HERO, [0.3, 1.0, 0])})
LIV = {'tv': False}

# 1: the hook. In his living room, facing us, he holds the cream handset at his right ear and pats the big messy tuft on his box head with his
#    free hand; three pats, the last one squashes the tuft and his head flat, the tuft springs back taller; he smiles at us on « Faux numéro »
D1 = st.dur('S01'); PATS = [0.55, 0.8, 1.12]
TOPH = add(HERO, [0.14, 2.1, 0.06])
SMILE = {'lid': 0.2, 'mouth': 'smile', 'brow': 0.35}
pat1 = [TK(0.0, {'R': R5(EARR), 'L': R5(off(HERO, 0, 0.05, -0.3, 1.0))}, {'R': 'grip', 'L': 'rest'}, {**SMILE, 'gy': -0.6}, d=0.0),
        TK(0.38, {'L': R5(add(TOPH, [0, 0.07, 0]))}, {'L': 'open'}, {**SMILE, 'gy': -0.8}, d=0.25)]
for i, tp in enumerate(PATS):
    big = i == 2
    pat1 += [TK(r(tp - 0.07), {'L': R5(add(TOPH, [0, 0.07 if not big else 0.16, 0]))}, {'L': 'open'}, {**SMILE, 'gy': -0.8}, d=0.07, keep=True),
             TK(tp, {'L': R5(add(TOPH, [0, -0.02 if not big else -0.12, 0]))}, {'L': 'open'}, {'lid': 0.5 if big else 0.25, 'mouth': 'smile', 'brow': 0.2, 'gy': -0.9}, sq=(1.12, 0.86, 1.12) if big else (1.02, 0.98, 1.02), scl={'head': [1.16, 0.78, 1.16]} if big else None, d=0.04, e='out', keep=True)]
pat1 += [TK(1.3, {'L': R5(add(TOPH, [0, 0.08, 0]))}, {'L': 'open'}, SMILE, sq=(0.96, 1.05, 0.96), scl={'head': [0.95, 1.08, 0.95]}, d=0.12, keep=True),
         TK(1.5, {'L': R5(off(HERO, 0, 0.05, -0.3, 1.0))}, {'L': 'rest'}, SMILE, sq=(1, 1, 1), scl={'head': [1, 1, 1]}, d=0.25, keep=True)]
st.shot('S01', 'livingRoom', setOpts=LIV, look={'sunDir': [0.4, 0.8, 0.9]}, actors=[
        act('mec', HERO, 0, 'stand', 'happy', keys=[k(0.0, look=add(HERO, [0, 2.7, 1.2])), *pat1, k(1.45, look='camera', lookDur=0.15), *blink(2.05, SMILE)])],
        props=[TUFT('meche1', 'mec', pat=[r(p + 0.0) for p in PATS], patBig=2), EAR('tel1', 'mec', color='#EDE6D2'),
               P('table1', 'table', pos=TABLE1, opts={'w': 0.5, 'd': 0.5, 'h': 1.2, 'color': '#2E7A7A'}), P('base1', 'redDeskPhone', pos=PHONEB, ry=20, opts={'color': '#EDE6D2'})],
        cams=[C1])
for tp in PATS: st.cue('sfx:boing', 'S01', tp, 0.18)

# ================================================================= the war room, frontal (S02, S16)
GEN2 = [-0.98, 0, 0.55]; TAB2 = [-0.72, 0, 1.2]; PH2 = [-0.72, 0.85, 1.2]
COLB2 = [1.15, 0, -1.35]; COLA2 = [-1.6, 0, -1.55]
HS_CRADLE = add(PH2, [0.0, 0.17, -0.03])
C2 = cam(0.0, [-0.2, 1.75, 7.3], [-0.2, 1.75, 7.3], [-0.2, 1.42, -0.5], [-0.2, 1.42, -0.5], lens=40)
chk('S02', C2, {'genFace': add(GEN2, [0, 2.05, 0]), 'genTop': add(GEN2, [0, 2.6, 0]), 'phone': PH2, 'colBface': add(COLB2, [0, 2.05, 0]), 'colAface': add(COLA2, [0, 2.05, 0]), 'boardTop': bpt(0, 1.0), 'boardL': bpt(-1, 0), 'boardR': bpt(1, 0), 'boardBot': bpt(0, -1)})
RYG2 = 18
EARG2 = off(GEN2, RYG2, 0.08, 0.27, 2.0)

# 2: he got the general staff. Static medium: the general beside the board snaps up the big red phone as it rattles (his arm and body stretch up
#    with it, a squash as it lands at his ear) and barks into it; two colonels at attention, plain khaki, blank shoulder boards
D2 = st.dur('S02'); SNAP2 = 0.32
BARK = {'lid': 0.1, 'mouth': 'scream', 'brow': -0.8, 'jaw': 0.6}
st.shot('S02', 'office', setOpts=OFFICE, look=WARLOOK, actors=[
        act('general', GEN2, RYG2, 'stand', 'determined', keys=[k(0.0, look=PH2), k(r(SNAP2 + 0.1), look='camera', lookDur=0.1),
            TK(0.0, {'R': R5(off(GEN2, RYG2, 0.1, 0.32, 1.0)), 'L': R5(off(GEN2, RYG2, 0.05, -0.3, 1.0))}, {'R': 'rest', 'L': 'rest'}, ATT, d=0.0),
            TK(0.2, {'R': R5(add(HS_CRADLE, [0, 0.03, 0]))}, {'R': 'grip'}, {'lid': 0.2, 'mouth': 'line', 'brow': -0.6}, (1.05, 0.95, 1.05), d=0.14, e='in', keep=True),
            TK(SNAP2, {'R': R5(add(EARG2, [0, 0.12, 0]))}, {'R': 'grip'}, {'lid': 0.0, 'pop': 0.4, 'mouth': 'O', 'brow': 0.6}, (0.88, 1.16, 0.88), d=0.07, e='out', keep=True),
            TK(r(SNAP2 + 0.12), {'R': R5(EARG2)}, {'R': 'grip'}, BARK, (1.1, 0.9, 1.1), d=0.05, e='in', keep=True),
            TK(r(SNAP2 + 0.35), {'R': R5(EARG2)}, {'R': 'grip'}, {'lid': 0.15, 'mouth': 'O', 'brow': -0.7}, (1, 1, 1), d=0.15, keep=True),
            *blink(1.25, {'lid': 0.15, 'mouth': 'line', 'brow': -0.7}), TK(1.05, face={'lid': 0.15, 'mouth': 'O', 'brow': -0.8}, bend={'neck': SP(0.25)}, d=0.1, keep=True), TK(1.2, bend={'neck': SP(0.0)}, d=0.1, keep=True), k(1.45, look=bpt(0, 0.3), lookDur=0.12), *BREATHE(0.9, D2, 0.4, 0.02)]),
        act('colB', COLB2, -20, 'stand', 'neutral', keys=[k(0.0, look='camera'), TK(0.0, ATTEN(COLB2, -20), {'R': 'open', 'L': 'open'}, ATT, d=0.0),
            TK(SNAP2, ATTEN(COLB2, -20), {'R': 'open', 'L': 'open'}, {**ATT, 'pop': 0.2}, (0.96, 1.05, 0.96), d=0.06, keep=True), TK(0.6, sq=(1, 1, 1), face=ATT, d=0.15, keep=True), *blink(1.0, ATT), *BREATHE(0.8, D2, 0.45, 0.015), k(1.3, look=add(GEN2, [0, 2.0, 0]), lookDur=0.12)]),
        act('colA', COLA2, 20, 'stand', 'neutral', keys=[k(0.0, look='camera'), TK(0.0, ATTEN(COLA2, 20), {'R': 'open', 'L': 'open'}, ATT, d=0.0),
            TK(r(SNAP2 + 0.03), ATTEN(COLA2, 20), {'R': 'open', 'L': 'open'}, {**ATT, 'pop': 0.2}, (0.96, 1.05, 0.96), d=0.06, keep=True), TK(0.65, sq=(1, 1, 1), face=ATT, d=0.15, keep=True), *blink(1.15, ATT), *BREATHE(0.85, D2, 0.45, 0.015)])],
        props=[BOARDP('S02'), P('smear2', 'smearArc', pos=[0, 0, 0], opts={'pts': [HS_CRADLE, add([(HS_CRADLE[i] + EARG2[i]) / 2 for i in range(3)], [-0.1, 0.25, 0.1]), EARG2], 'win': [r(SNAP2 - 0.08), r(SNAP2 + 0.03)], 'color': '#4E5A34', 'r': 0.09, 'opacity': 0.65}), P('table2', 'table', pos=TAB2, opts={'w': 0.55, 'd': 0.5, 'h': 0.85, 'color': '#3A3530'}), P('rouge2', 'redDeskPhone', pos=PH2, ry=25, opts={'ring': [[0.0, SNAP2]]}),
               P('combine2a', 'handset', pos=HS_CRADLE, rot=[0, r(math.radians(25)), r(PI / 2)], opts={'len': 0.32, 'color': '#D8262C'}, keys=[k(SNAP2 - 0.12, visible=False)]),
               EAR('combine2b', 'general', color='#D8262C', keys=[k(0.0, visible=False), k(SNAP2 - 0.12, visible=True)]),
               CAP('cap2', 'general', 1.05), EPA('epa2', 'general'), CAP('capA2', 'colA'), EPA('epaA2', 'colA'), CAP('capB2', 'colB'), EPA('epaB2', 'colB')],
        cams=[C2])
st.cue('sfx:ring', 'S02', 0.0, 0.3); st.cue('whoosh', 'S02', 0.2, 0.2, 0.15, 600, 3000); st.cue('clack', 'S02', SNAP2, 0.35)

# ================================================================= over the general's shoulder (S03, S05, S08, S10): one framing for every order
chk('S03', C_OS, {'genHead': add(GEN_OS, [0, 2.05, 0]), 'genFeet': GEN_OS, 'boardTop': bpt(0, 1.05), 'boardBot': bpt(0, -1.05), 'mapL': bpt(-0.92, 0), 'mapR': bpt(0.92, 0), 'colLface': add(COL_L, [0, 2.05, 0]), 'colRface': add(COL_R, [0, 2.05, 0])})

# 3: he asked: « take the sides off well ». Over the general's shoulder (he repeats it into the red handset, a nod): the two colonels at the board
#    edges run big clippers down both sides of the felt country; green tufts fly off the board at the lens; the sides are buzzed to sandy stubble
D3 = st.dur('S03'); B3a, B3b = 0.95, 1.75
VS = [0.78, 0.4, 0.0, -0.4, -0.78]
def CLIPPATH(s, t0, t1):   # the hand's path down one edge (s -1 left, +1 right), as (time, world point): the clipper's blade on the felt
    return [(r(t0 + (t1 - t0) * i / (len(VS) - 1)), add(bpt(0.82 * edge(v, s), v, 0.12), [0, 0.22, 0])) for i, v in enumerate(VS)]
def CLIPKEYS(path): return [k(t, to=p, dur=r(path[i + 1][0] - t) if i + 1 < len(path) else 0.1, ease='linear') for i, (t, p) in enumerate(path)]
def colclip(who, p, ry, s, path, hand):
    ks = [k(0.0, look=bpt(0.8 * s, 0.6)), TK(0.0, {hand: R5(add(path[0][1], [0, 0.1, 0.12])), ('L' if hand == 'R' else 'R'): R5(off(p, ry, 0.05, 0.3 if hand == 'L' else -0.3, 1.0))}, {hand: 'grip'}, {'lid': 0.25, 'mouth': 'line', 'brow': -0.5}, d=0.0)]
    ks += [TK(r(path[0][0] - 0.25), {hand: R5(add(path[0][1], [0, 0.02, 0.0]))}, {hand: 'grip'}, {'lid': 0.2, 'mouth': 'clench', 'brow': -0.8}, (0.95, 1.06, 0.95), d=0.2, keep=True)]
    ks += [TK(t, {hand: R5(add(q, [0, 0.0, 0.0]))}, {hand: 'grip'}, {'lid': 0.15, 'mouth': 'clench', 'brow': -0.9}, (1.04, 0.96, 1.04) if i % 2 else (0.98, 1.02, 0.98), d=r(path[1][0] - path[0][0]), e='linear', keep=True) for i, (t, q) in enumerate(path)]
    ks += [TK(r(path[-1][0] + 0.15), {hand: R5(add(path[-1][1], [0.1 * s, 0.25, 0.25]))}, {hand: 'grip'}, {'lid': 0.1, 'mouth': 'smile', 'brow': 0.3}, (1, 1, 1), d=0.15, keep=True),
           k(r(path[-1][0] + 0.15), look='camera', lookDur=0.12), k(path[0][0], fx={'shiver': True}), k(path[-1][0], fx={'shiver': False})]
    return ks
PL3, PR3 = CLIPPATH(-1, B3a, B3b), CLIPPATH(1, B3a + 0.05, B3b + 0.05)
CLROT = [-BTL, 0, PI]
CLHAND = [PI, 0, 0]   # in the hand: the blade past the fingers
st.shot('S03', 'office', setOpts=OFFICE, look=WARLOOK, actors=[
        OSGEN('S03', keys=[TK(0.6, face={'lid': 0.2, 'mouth': 'O', 'brow': -0.6}, bend={'neck': SP(0.3)}, d=0.1, keep=True), TK(0.8, face=ATT, bend={'neck': SP(0.0)}, d=0.12, keep=True), *blink(1.5, ATT), TK(1.85, bend={'neck': SP(0.25)}, d=0.1, keep=True), TK(2.0, bend={'neck': SP(0.0)}, d=0.12, keep=True)]),
        act('colL', COL_L, RYL, 'stand', 'determined', keys=colclip('colL', COL_L, RYL, -1, PL3, 'L')),
        act('colR', COL_R, RYR, 'stand', 'determined', keys=colclip('colR', COL_R, RYR, 1, PR3, 'R'))],
        props=[BOARDP('S03', sides=[[B3a, 0.0], [B3b, 1.0]], fly=True, flyN=6, flyS=0.1), *OSGENP('S03'), CAP('capL3', 'colL'), EPA('epaL3', 'colL'), CAP('capR3', 'colR'), EPA('epaR3', 'colR'),
               P('tondL3', 'barberClippers', on={'actor': 'colL', 'hand': 'L', 'offset': [0.0, 0.0, 0.03], 'rot': CLHAND}, opts={'s': 1.7, 'buzz': [[r(B3a - 0.1), r(B3b + 0.1)]]}),
               P('tondR3', 'barberClippers', on={'actor': 'colR', 'hand': 'R', 'offset': [0.0, 0.0, 0.03], 'rot': CLHAND}, opts={'s': 1.7, 'buzz': [[r(B3a - 0.05), r(B3b + 0.15)]]})],
        cams=[C_OS])
st.cue('engine', 'S03', B3a, 0.22, 0.9); st.cue('sfx:pop', 'S03', 1.2, 0.15); st.cue('sfx:pop', 'S03', 1.45, 0.15)

# 4: the army evacuated both coasts. (a) Half a second on the board, square on: both coastlines buzzed off like sideburns, sandy stubble at both
#    edges; (b) the beach, low and wide: soldiers in helmets march inland toward us carrying two sunbathers still lying on their deckchairs (calm,
#    dark glasses, one waves), the sea and one lone striped parasol left behind; DÉGAGÉ stamps over the sky
D4 = st.dur('S04')
C4 = cam(0.0, [0.0, 1.22, 3.15], [0.0, 1.22, 3.05], [0.0, 1.2, -1.0], [0.0, 1.2, -1.0], lens=40)
chk('S04', C4, {'mapL': bpt(-0.95, 0), 'mapR': bpt(0.95, 0), 'top': bpt(0, 1.05), 'bot': bpt(0, -1.05)})
st.shot('S04', 'office', setOpts=OFFICE, look=WARLOOK, actors=[],
        props=[BOARDP('S04', **DONE_SIDES)], cams=[C4])

D4b = st.dur('S04b')
SEA = {}
GA0 = [2.6, 0, -1.6]; GB0 = [4.3, 0, -4.6]; WALK = 1.1
LIFT4 = 2.62
def carry_group(tag, c0, b_id, s_ids, col, wave=False):
    """a sun lounger carried overhead by two soldiers (one at each end, arms up), walking toward +Z; the sunbather lying flat on it, calm"""
    c1 = add(c0, [0, 0, WALK]); acts = []; props = []
    for j, e in enumerate((1, -1)):          # front end (+Z), back end
        p0 = add(c0, [-0.28 * e, 0, 0.62 * e]); p1 = add(p0, [0, 0, WALK])
        ks = [k(0.0, look='camera'), k(0.0, to=p1, dur=D4b, clip='walk', ease='linear', face=0)]
        for i in range(7):
            t = r(D4b * i / 6); z = r(c0[2] + 0.62 * e + WALK * i / 6)
            ks.append(TK(t, {'R': R5([r(c0[0] - 0.24), r(LIFT4 - 0.02), r(z + 0.05 * e)]), 'L': R5([r(c0[0] + 0.24), r(LIFT4 - 0.02), r(z + 0.05 * e)])}, {'R': 'grip', 'L': 'grip'}, {'lid': 0.25, 'mouth': 'line', 'brow': -0.4}, (1.04, 0.95, 1.04) if i % 2 else (0.97, 1.03, 0.97), d=r(D4b / 6), e='linear'))
        acts.append(act(s_ids[j], p0, 0, 'walk', 'neutral', keys=ks))
        props.append(HELMET(f'casque{tag}{j}', s_ids[j]))
    props.append(P(f'transat{tag}', 'sunLounger', pos=add(c0, [0, LIFT4, 0]), rot=[0, 0, -0.14], opts={'color': col, 'back': 1.0}, keys=[k(0.0, to=add(c1, [0, LIFT4, 0]), dur=D4b, ease='linear')]))
    face = {'lid': 0.45, 'mouth': 'smile', 'brow': 0.2}
    bk = [k(0.0, look='camera'), k(0.0, to=add(c1, [0, LIFT4 + 0.12, 0.05]), dur=D4b, ease='linear', glide=True, face='keep'), TK(0.0, face=face, d=0.0), *blink(0.9, face)]
    if wave: bk += [TK(0.2, {'L': R5(add(c0, [0.35, LIFT4 + 1.15, 0.45]))}, {'L': 'open'}, {'lid': 0.3, 'mouth': 'bigsmile', 'brow': 0.4}, d=0.15), TK(0.45, {'L': R5(add(c0, [0.6, LIFT4 + 1.1, 0.75]))}, {'L': 'open'}, face, d=0.15, keep=True), TK(0.7, {'L': R5(add(c0, [0.35, LIFT4 + 1.15, 0.95]))}, {'L': 'open'}, face, d=0.15, keep=True), TK(0.95, {'L': R5(add(c0, [0.6, LIFT4 + 1.1, 1.2]))}, {'L': 'open'}, face, d=0.15, keep=True)]
    acts.append(act(b_id, add(c0, [0, LIFT4 + 0.12, 0.05]), 25, 'reclineBack', 'happy', keys=bk))
    props.append(P(f'lunettes{tag}', 'shades', on={'actor': b_id, 'joint': 'head', 'offset': [0.0, 0.3, 0.095]}, opts={'ear': False}))
    return acts, props
AA, PA = carry_group('A', GA0, 'bain1', ('sold1', 'sold2'), '#2EA8A0', True)
AB, PB = carry_group('B', GB0, 'bain2', ('sold3', 'sold4'), '#E8A030')
C4b = cam(0.0, [4.6, 1.2, 6.2], [4.5, 1.22, 5.8], [3.0, 2.05, -2.4], [3.0, 2.05, -2.4], lens=46)
chk('S04b', C4b, {'loungerA': add(GA0, [0, LIFT4 + 0.3, WALK]), 'loungerA0': add(GA0, [0, LIFT4 + 0.3, 0]), 'soldAf': add(GA0, [0, 2.05, 0.62 + WALK]), 'soldAb': add(GA0, [0, 2.05, -0.62 + WALK]), 'loungerB': add(GB0, [0, LIFT4 + 0.3, WALK]), 'soldBf': add(GB0, [0, 2.05, 0.62 + WALK]), 'parasol': [2.0, 2.1, -6.6], 'feetA': add(GA0, [0, 0, 0.62 + WALK])})
st.shot('S04b', 'beach', setOpts=SEA, look={'sunDir': [0.4, 0.9, 0.8]}, actors=[*AA, *AB], props=[*PA, *PB, P('parasol4', 'umbrella', pos=[2.9, 0, -8.6], opts={'radius': 1.1, 'height': 2.1, 'colors': ['#E8A030', '#F4F1E8']})], cams=[C4b])
st.card('S04b', 'DÉGAGÉ', at=0.45)
st.cue('sfx:stepHeavy', 'S04b', 0.0, 0.2); st.cue('gust', 'S04b', 0.0, 0.12, 1.2)

# 5: « a little shorter at the front ». Same framing as 3: the colonel at the left reaches up across the top edge with giant scissors, his arm
#    stretching like rubber across the board, snip snip snip; a wide strip of green felt drops off the top toward us; the general nods into the phone
D5 = st.dur('S05'); T5a, T5b = 0.4, 1.05; DROP5 = 1.1
SC5 = [(r(T5a + (T5b - T5a) * i / 4), bpt(-0.62 + 1.24 * i / 4, 0.7, 0.1)) for i in range(5)]
sc_keys = [k(0.0, look=bpt(-0.4, 0.75))]
sc_keys += [TK(0.0, {'R': R5(add(SC5[0][1], [-0.1, -0.25, 0.15])), 'L': R5(off(COL_L, RYL, 0.05, -0.3, 1.0))}, {'R': 'grip', 'L': 'rest'}, {'lid': 0.25, 'mouth': 'line', 'brow': -0.5}, d=0.0)]
sc_keys += [TK(t, {'R': R5(q, 1, 0.06)}, {'R': 'grip'}, {'lid': 0.15, 'mouth': 'clench', 'brow': -0.8}, (0.92, 1.1, 0.92), d=0.16 if i else 0.25, e='linear' if i else 'inOut', keep=True) for i, (t, q) in enumerate(SC5)]
sc_keys += [TK(r(DROP5 + 0.1), {'R': R5(add(COL_L, [0.35, 1.5, 0.45]))}, {'R': 'grip'}, {'lid': 0.1, 'mouth': 'smile', 'brow': 0.3}, (1, 1, 1), d=0.2, keep=True), k(r(DROP5 + 0.05), look='camera', lookDur=0.12),
            *[k(t, look=q) for (t, q) in SC5[1:4]]]
st.shot('S05', 'office', setOpts=OFFICE, look=WARLOOK, actors=[
        OSGEN('S05', keys=[TK(1.15, face={'lid': 0.3, 'mouth': 'line', 'brow': 0.1}, bend={'neck': SP(0.35)}, d=0.1, keep=True), TK(1.3, face=ATT, bend={'neck': SP(0.0)}, d=0.12, keep=True)]),
        act('colL', COL_L, RYL, 'stand', 'determined', keys=sc_keys),
        act('colR', COL_R, RYR, 'stand', 'neutral', keys=[k(0.0, look=bpt(0.0, 0.7)), TK(0.0, ATTEN(COL_R, RYR), {'R': 'open', 'L': 'open'}, ATT, d=0.0), k(r(DROP5 + 0.05), look=bpt(0.0, 0.0), lookDur=0.15), *blink(0.5, ATT)])],
        props=[BOARDP('S05', sides=1.0, top=[[T5a, 0.0], [T5b, 1.0]], dropAt=DROP5), *OSGENP('S05'), CAP('capL5', 'colL'), EPA('epaL5', 'colL'), CAP('capR5', 'colR'), EPA('epaR5', 'colR'),
               *[P(f'smear5{i}', 'smearArc', pos=[0, 0, 0], opts={'pts': [add(SC5[i - 1][1], [0, 0.03, 0.05]), add(SC5[i][1], [0, 0.03, 0.05])], 'win': [r(SC5[i][0] - 0.07), r(SC5[i][0] + 0.01)], 'color': '#D9DEE3', 'r': 0.05, 'opacity': 0.6}) for i in range(1, 5)],
               P('ciseaux5', 'bigScissors', pos=add(SC5[0][1], [-0.1, -0.25, 0.15]), rot=[-BTL, 0, 0], opts={'len': 0.42, 'open': 0.4, 'snip': [[0, 1]] + [[r(T5a + 0.08 * i), (i + 1) % 2] for i in range(9)] + [[r(T5b + 0.05), 1]]},
                 keys=[k(0.0, to=SC5[0][1], dur=T5a), *[k(t, to=q, dur=0.16, ease='linear') for (t, q) in SC5[1:]], k(r(DROP5 + 0.1), to=add(COL_L, [0.45, 1.55, 0.5]), dur=0.2)])],
        cams=[C_OS])
for i in range(5): st.cue('sfx:click', 'S05', r(T5a + 0.16 * i), 0.2)
st.cue('whoosh', 'S05', DROP5, 0.2, 0.3, 300, 1500)

# ================================================================= the country road (S06): road along Z, the column walks backwards toward -Z
# 6: the front fell back ten kilometres. Tracking alongside: a column of soldiers in helmets walks backwards up the road carrying a striped
#    barrier upright by its two posts and, behind it, a plain sentry box on two poles; they hop in step on every stride, deadpan
D6 = st.dur('S06'); V6 = 1.9
Z6 = 4.0
SOLD6 = [[-1.2, 0, Z6], [1.2, 0, Z6], [0.0, 0, Z6 - 2.3], [0.0, 0, Z6 - 4.6]]
BOX6 = [0.0, 0, Z6 - 3.45]
C6 = cam(0.0, [8.0, 2.1, Z6 + 4.0], [8.0, 2.1, Z6 + 4.0 - V6 * D6], [-0.6, 1.2, Z6 - 2.4], [-0.6, 1.2, Z6 - 2.4 - V6 * D6], lens=48)
chk('S06', C6, {'s1face': add(SOLD6[0], [0, 2.05, 0]), 's2face': add(SOLD6[1], [0, 2.05, 0]), 's3face': add(SOLD6[2], [0, 2.05, 0]), 's4face': add(SOLD6[3], [0, 2.05, 0]), 'boxTop': add(BOX6, [0, 2.4, 0]), 'boom': [0, 1.15, Z6]})
def back_walk(who, p, keys_extra=(), hands=None):
    ks = [k(0.0, look='camera'), k(0.0, to=add(p, [0, 0, r(-V6 * D6)]), dur=D6, clip='walk', back=True, ease='linear', face=0), TK(0.0, face={'lid': 0.3, 'mouth': 'line', 'brow': -0.3}, d=0.0)]
    for i in range(8):
        t = r(0.12 + i * 0.26); z = r(p[2] - V6 * t)
        hd = hands(z) if hands else None
        ks.append(TK(t, hd, {'R': 'grip', 'L': 'grip'} if hd else None, {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}, (1.16, 0.84, 1.16) if i % 2 == 0 else (0.9, 1.14, 0.9), d=0.11, e='out', keep=not hd))
    return act(who, p, 0, 'walk', 'neutral', keys=[*ks, *keys_extra])
def posthands(s): return lambda z: {'R' if s < 0 else 'L': R5([r(s * 1.05), 1.2, r(z - 0.05)]), 'L' if s < 0 else 'R': R5([r(s * 1.05), 0.85, r(z - 0.05)])}
def polehands(front): return lambda z: {'R': R5([-0.52, 0.86, r(z + (-0.1 if front else 0.1))]), 'L': R5([0.52, 0.86, r(z + (-0.1 if front else 0.1))])}
st.shot('S06', 'grassland', setOpts={'clouds': 30}, look={'sunDir': [0.6, 0.8, 0.7]}, actors=[
        back_walk('sold1', SOLD6[0], hands=posthands(-1)), back_walk('sold2', SOLD6[1], hands=posthands(1)),
        back_walk('sold3', SOLD6[2], hands=polehands(True)), back_walk('sold4', SOLD6[3], hands=polehands(False))],
        props=[P('route6', 'roadStrip', pos=[0, 0, 0], opts={'len': 160, 'w': 6.5}),
               P('barriere6', 'fieldBarrier', pos=[0, 0.0, Z6 - 0.05], opts={'len': 2.4}, keys=[k(0.0, to=[0, 0.0, r(Z6 - 0.05 - V6 * D6)], dur=D6, ease='linear')]),
               P('guerite6', 'sentryBox', pos=BOX6, opts={'lift': 0.58}, keys=[k(0.0, to=add(BOX6, [0, 0, r(-V6 * D6)]), dur=D6, ease='linear')]),
               *[HELMET(f'casque6{j}', f'sold{j}') for j in (1, 2, 3, 4)]],
        cams=[C6])
st.cue('sfx:stepHeavy', 'S06', 0.0, 0.25)

# ================================================================= the village square (S07)
# 7: a village changed country; it noticed nothing. Static wide: three old men play pétanque in the foreground; one winds up and throws (a high arc,
#    hang time at the top, a thud and a puff); behind them the soldiers carry the barrier past from left to right, walking backwards; nobody looks up
D7 = st.dur('S07'); TH7 = 0.95; LAND7 = 1.78
PET = [[-1.5, 0, 0.4], [-0.75, 0, 1.3], [1.6, 0, 0.3]]
RYP = [70, 62, -70]
JACK = [0.55, 0.06, 1.0]
C7 = cam(0.0, [0.1, 1.2, 10.5], [0.1, 1.22, 10.25], [0.1, 1.5, -1.0], [0.1, 1.5, -1.0], lens=42)
BZ7 = -2.6; BX0, BX1 = -5.6, 4.6; BY7 = 0.55        # the barrier carried with its feet BY7 off the ground: the boom at head height
chk('S07', C7, {'p1face': add(PET[0], [0, 2.05, 0]), 'p2face': add(PET[1], [0, 1.75, 0]), 'p3face': add(PET[2], [0, 2.05, 0]), 'jack': JACK, 'boomL': [-1.6, 1.15 + BY7, BZ7], 'boomR': [1.6, 1.15 + BY7, BZ7], 'soldFace': [0, 2.05, BZ7], 'arcTop': [0.0, 3.0, 1.0]})
OLD = {'lid': 0.45, 'mouth': 'line', 'brow': 0.0}
B0 = off(PET[1], RYP[1], 0.4, -0.25, 1.05); BTOP = [-0.05, 3.0, 1.1]; BLAND = add(JACK, [-0.2, 0.0, 0.15])
def side_walk(who, x0, x1, z, s):
    p0 = [x0, 0, z]; ks = [k(0.0, look=[x0 - 3, 1.4, z + 3]), k(0.0, to=[x1, 0, z], dur=D7, clip='walk', back=True, ease='linear', face=-90)]
    for i in range(9):
        t = r(i * D7 / 8); x = r(x0 + (x1 - x0) * t / D7)
        ks.append(TK(t, {'R': R5([r(x + 0.12 * s), 1.45, r(z + 0.05)]), 'L': R5([r(x + 0.12 * s), 1.05, r(z + 0.05)])}, {'R': 'grip', 'L': 'grip'}, OLD, (1.06, 0.93, 1.06) if i % 2 else (0.96, 1.05, 0.96), d=r(D7 / 8), e='linear'))
    return act(who, p0, -90, 'walk', 'neutral', keys=[*ks, *blink(1.2, OLD)])
L7 = 3.2
WATCH = lambda who, t0: [k(r(TH7 + t0), look=BTOP, lookDur=0.25), k(r(TH7 + 0.5), look=BTOP, lookDur=0.1), k(r(LAND7 - 0.05 + t0), look=BLAND, lookDur=0.12)]
st.shot('S07', 'grassland', setOpts={'clouds': 20}, look={'sunDir': [0.5, 0.8, 0.8]}, actors=[
        act('pet1', PET[0], RYP[0], 'stand', 'neutral', keys=[k(0.0, look=JACK), TK(0.0, {'R': R5(off(PET[0], RYP[0], 0.2, 0.2, 1.05)), 'L': R5(off(PET[0], RYP[0], 0.25, -0.2, 1.05))}, {'R': 'rest', 'L': 'rest'}, OLD, (1, 1, 1), {'spine': SP(0.28), 'neck': SP(0.1)}, d=0.0),
            *WATCH('pet1', 0.08), *blink(2.3, OLD), *BREATHE(0.0, D7, 0.7, 0.012)]),
        act('pet2', PET[1], RYP[1], 'stand', 'determined', keys=[k(0.0, look=JACK),
            TK(0.0, {'R': R5(off(PET[1], RYP[1], 0.3, 0.3, 0.75)), 'L': R5(off(PET[1], RYP[1], 0.35, -0.2, 0.7))}, {'R': 'grip', 'L': 'rest'}, {'lid': 0.4, 'mouth': 'line', 'brow': -0.3}, (1.06, 0.86, 1.06), {'spine': SP(0.55)}, d=0.0),
            TK(r(TH7 - 0.4), {'R': R5(off(PET[1], RYP[1], -0.45, 0.3, 0.55))}, {'R': 'grip'}, {'lid': 0.3, 'mouth': 'clench', 'brow': -0.7}, (1.16, 0.78, 1.16), {'spine': SP(0.75)}, d=0.3, keep=True),
            TK(r(TH7 - 0.04), {'R': R5(off(PET[1], RYP[1], 0.2, 0.3, 0.8))}, {'R': 'grip'}, {'lid': 0.2, 'mouth': 'O', 'brow': 0.2}, (0.95, 1.05, 0.95), {'spine': SP(0.35)}, d=0.05, e='in', keep=True),
            TK(TH7, {'R': R5(B0)}, {'R': 'open'}, {'lid': 0.1, 'mouth': 'O', 'brow': 0.4}, (0.86, 1.18, 0.86), {'spine': SP(-0.05)}, d=0.06, e='out', keep=True),
            TK(r(TH7 + 0.25), {'R': R5(off(PET[1], RYP[1], 0.45, 0.25, 1.9))}, {'R': 'open'}, {'lid': 0.25, 'mouth': 'line', 'brow': 0.2}, (0.95, 1.06, 0.95), {'spine': SP(0.0)}, d=0.2, keep=True),
            TK(r(LAND7 + 0.25), {'R': R5(off(PET[1], RYP[1], 0.3, 0.3, 1.0))}, {'R': 'rest'}, OLD, (1, 1, 1), {'spine': SP(0.25)}, d=0.3, keep=True),
            k(0.0, look=JACK), *WATCH('pet2', 0.02), *blink(2.45, OLD)]),
        act('pet3', PET[2], RYP[2], 'stand', 'neutral', keys=[k(0.0, look=JACK), TK(0.0, {'R': R5(off(PET[2], RYP[2], 0.1, 0.3, 1.0)), 'L': R5(off(PET[2], RYP[2], 0.1, -0.3, 1.0))}, {'R': 'rest', 'L': 'rest'}, OLD, (1, 1, 1), {'spine': SP(0.22), 'neck': SP(0.15)}, d=0.0),
            *WATCH('pet3', 0.12), TK(r(LAND7 + 0.15), face={'lid': 0.4, 'mouth': 'smile', 'brow': 0.2}, bend={'neck': SP(0.35), 'spine': SP(0.22)}, d=0.1, keep=True), TK(r(LAND7 + 0.32), face=OLD, bend={'neck': SP(0.15), 'spine': SP(0.22)}, d=0.12, keep=True)]),
        side_walk('sold1', r(BX0 - L7 / 2 + 0.15), r(BX1 - L7 / 2 + 0.15), BZ7, 1), side_walk('sold2', r(BX0 + L7 / 2 - 0.15), r(BX1 + L7 / 2 - 0.15), BZ7, -1)],
        props=[P('place7', 'villageSquare', pos=[0, 0, -2.0], opts={'trees': [[-5.0, 1.0], [5.5, 1.5]]}),
               P('barriere7', 'fieldBarrier', pos=[BX0, BY7, BZ7], opts={'len': L7, 'sway': 0.02}, keys=[k(0.0, to=[BX1, BY7, BZ7], dur=D7, ease='linear')]),
               HELMET('casque71', 'sold1'), HELMET('casque72', 'sold2'),
               P('cochonnet7', 'boule', pos=JACK, opts={'r': 0.04, 'color': '#E8C040'}),
               *[P(f'boule7{i}', 'boule', pos=q, opts={'r': 0.06}) for i, q in enumerate([[0.85, 0.06, 0.8], [0.25, 0.06, 1.35], [1.05, 0.06, 1.3]])],
               P('boule7', 'boule', pos=B0, opts={'r': 0.07}, keys=[k(TH7, path=[B0, [r((B0[0] + BTOP[0]) / 2), r(BTOP[1] - 0.3), r((B0[2] + BTOP[2]) / 2)], BTOP], dur=0.42, ease='out'), k(r(TH7 + 0.54), to=BLAND, dur=r(LAND7 - TH7 - 0.54), ease='in'), k(LAND7, squash=[1.35, 0.65, 1.35], dur=0.25)]),
               P('poussiere7', 'softDust', pos=BLAND, opts={'at': LAND7, 'n': 12, 'size': 0.32, 'rise': 0.4, 'spread': 0.55, 'life': 0.6, 'color': '#E8DCC0', 'opacity': 0.85}),
               *[P(f'casquette7{j}', 'plainCap', on={'actor': f'pet{j}', 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}, opts={'w': 0.23, 'd': 0.19, 'color': c, 'band': c}) for j, c in ((1, '#6A5E4E'), (3, '#4E5A66'))]],
        cams=[C7])
st.cue('whoosh', 'S07', TH7, 0.15, 0.3, 500, 2500); st.cue('thud', 'S07', LAND7, 0.35); st.cue('clack', 'S07', r(LAND7 + 0.02), 0.2)

# 8: « a little fade at the back ». Same framing: the colonel at the left kneels by the board and drags the giant comb along the bottom of the map,
#    two long strokes left to right with a stretch of the arm; four big neat ridges rise behind the comb
D8 = st.dur('S08'); S8 = [(0.25, 0.8), (0.95, 1.45)]
CB = lambda u, v: bpt(u, v, 0.06)
cb_keys = [k(0.0, look=CB(-0.4, -0.6))]
comb_path = []
for (a, b), vv in zip(S8, (-0.48, -0.72)):
    for i in range(5): comb_path.append((r(a + (b - a) * i / 4), CB(-0.62 + 1.24 * i / 4, vv)))
cb_keys += [TK(0.0, {'R': R5(add(comb_path[0][1], [-0.1, 0.1, 0.12])), 'L': R5(off(COL_L, RYL, 0.3, -0.2, 0.75))}, {'R': 'grip', 'L': 'open'}, {'lid': 0.3, 'mouth': 'line', 'brow': -0.5}, (1.0, 0.8, 1.0), {'spine': SP(0.35)}, d=0.0)]
cb_keys += [TK(t, {'R': R5(q, 1, 0.06)}, {'R': 'grip'}, {'lid': 0.2, 'mouth': 'clench', 'brow': -0.7}, (1.02, 0.78, 1.02) if i % 5 else (1.08, 0.72, 1.08), {'spine': SP(0.45)}, d=0.13, e='linear', keep=True) for i, (t, q) in enumerate(comb_path)]
cb_keys += [TK(1.55, {'R': R5(add(COL_L, [0.4, 1.35, 0.5]))}, {'R': 'grip'}, {'lid': 0.15, 'mouth': 'smile', 'brow': 0.3}, (1, 0.85, 1), {'spine': SP(0.2)}, d=0.15, keep=True), k(1.5, look='camera', lookDur=0.12)]
st.shot('S08', 'office', setOpts=OFFICE, look=WARLOOK, actors=[
        OSGEN('S08', keys=[TK(1.0, face={'lid': 0.3, 'mouth': 'O', 'brow': -0.2}, d=0.1, keep=True)]),
        act('colL', add(COL_L, [0.1, 0, 0.15]), RYL, 'stand', 'determined', keys=cb_keys),
        act('colR', COL_R, RYR, 'stand', 'neutral', keys=[k(0.0, look=bpt(0.0, -0.6)), TK(0.0, ATTEN(COL_R, RYR), {'R': 'open', 'L': 'open'}, ATT, d=0.0), *blink(0.7, ATT)])],
        props=[BOARDP('S08', **DONE_TOP, back=[[S8[0][0], 0.0], [S8[0][1], 0.5], [S8[1][0], 0.5], [S8[1][1], 1.0]]), *OSGENP('S08'), CAP('capL8', 'colL'), EPA('epaL8', 'colL'), CAP('capR8', 'colR'), EPA('epaR8', 'colR'),
               P('peigne8', 'bigComb', pos=add(comb_path[0][1], [-0.1, 0.1, 0.12]), rot=[-BTL, 0, 0.12], opts={'len': 0.6}, keys=[k(0.0, to=comb_path[0][1], dur=0.25), *[k(t, to=q, dur=0.13, ease='linear') for (t, q) in comb_path[1:]], k(1.55, to=add(COL_L, [0.5, 1.4, 0.55]), dur=0.15)])],
        cams=[C_OS])
st.cue('sfx:scratch', 'S08', S8[0][0], 0.25); st.cue('sfx:scratch', 'S08', S8[1][0], 0.25)

# ================================================================= the terraced hill (S09)
# 9: the excavators cut the hinterland into steps. Close wide from a little above: two army excavators at the foot finish carving a round green hill
#    into four tidy terraced steps (the last risers sharpen, puffs of earth); one calm cow standing on each step, side on; the last bucket bites
D9 = st.dur('S09'); HR, HH, HN = 5.2, 3.6, 4
def tread(kk):   # the middle of tread kk (0 lowest .. 3 top): (radius, height)
    r0 = HR * (1 - kk / HN); r1 = HR * (1 - (kk + 1) / HN)
    return (r((r0 - (r0 - r1) * 0.12 + r1) / 2) if kk < HN - 1 else 0.0, r(HH * (kk + 1) / HN + 0.05))
COWS = []
for kk, az in zip(range(4), (-38, 34, -22, 0)):
    rr, yy = tread(kk); COWS.append(([r(rr * math.sin(math.radians(az))), r(yy - (0.08 if kk == HN - 1 else 0.0)), r(rr * math.cos(math.radians(az)))], 90 + az if kk % 2 == 0 else -90 + az))
C9 = cam(0.0, [0.0, 7.5, 31.5], [-0.8, 7.1, 29.6], [0.0, 1.9, 1.0], [-0.3, 1.8, 1.0], lens=40)
chk('S09', C9, {**{f'cow{i}': add(p, [0, 0.8, 0]) for i, (p, _) in enumerate(COWS)}, 'hillL': [-HR, 0, 0], 'hillR': [HR, 0, 0], 'top': [0, HH, 0], 'excL': [-5.6, 2.5, 3.6], 'excR': [5.8, 2.5, 3.0]})
EXL = [-4.4, 0.05, 7.4]; EXR = [4.4, 0.05, 7.6]
BITE9, BITE9b = 0.78, 1.42           # the left bucket bites the last riser (anticipation 0.3-0.7), the right one sharpens it
CUT9 = [[0.0, 0.0], [BITE9, 0.05], [r(BITE9 + 0.35), 0.7], [BITE9b, 0.75], [r(BITE9b + 0.3), 1.0]]
COW0LOW = [COWS[0][0][0], r(COWS[0][0][1] - 0.5), COWS[0][0][2]]
def cowkeys(i, p):   # head turns only, side-on bodies (no look at the lens); the lowest cow hops onto its new step: squash, rise, hang, land, squash
    ks = [k(0.0, look=[p[0] + 3 * (1 if i % 2 else -1), p[1] + 0.8, p[2] + 1.0]), k(r(BITE9 + 0.05 + 0.05 * i), look=[-4.0, 0.5, 6.0], lookDur=0.12), k(r(1.65 + 0.12 * i), look=[p[0] + 3 * (1 if i % 2 else -1), p[1] + 0.8, p[2] + 2.0], lookDur=0.25)]
    if i == 0:
        T = r(BITE9b + 0.18)
        ks += [k(T, to=add(COW0LOW, [0, -0.06, 0]), dur=0.06, glide=True, face='keep'), k(r(T + 0.06), to=add(p, [0, 0.6, 0.05]), dur=0.12, ease='out', glide=True, face='keep'),
               k(r(T + 0.18), to=add(p, [0, 0.64, 0.05]), dur=0.1, glide=True, face='keep'), k(r(T + 0.28), to=add(p, [0, -0.05, 0]), dur=0.1, ease='in', glide=True, face='keep'), k(r(T + 0.38), to=p, dur=0.08, glide=True, face='keep')]
    return ks
st.shot('S09', 'grassland', setOpts={'clouds': 30}, look={'sunDir': [0.5, 0.8, 0.9]}, actors=[
        *[act(f'vache{i + 1}', COW0LOW if i == 0 else p, ry, 'idle', None, keys=cowkeys(i, p)) for i, (p, ry) in enumerate(COWS)]],
        props=[P('colline9', 'terraceHill', pos=[0, 0, 0], opts={'r': HR, 'h': HH, 'n': HN, 'cut': CUT9}),
               P('pelle9a', 'excavator', pos=EXL, ry=yaw(EXL, [-2.0, 0, 4.8]), scale=1.0, opts={'dig': [[0, 0.35], [0.3, 0.35], [0.7, 0.0], [BITE9, 1.0], [r(BITE9 + 0.4), 1.0], [r(BITE9 + 0.7), 0.3], [2.2, 0.2], [2.5, 0.6]], 'swing': [[0, 0.0], [r(BITE9 + 0.45), 0.0], [r(BITE9 + 0.8), 0.5], [2.4, 0.5]], 'shake': [[BITE9, r(BITE9 + 0.2)]]}),
               P('pelle9b', 'excavator', pos=EXR, ry=yaw(EXR, [2.0, 0, 4.8]), scale=1.0, opts={'dig': [[0, 0.5], [0.6, 0.6], [r(BITE9b - 0.4), 0.0], [BITE9b, 1.0], [r(BITE9b + 0.35), 0.9], [r(BITE9b + 0.7), 0.2]], 'shake': [[BITE9b, r(BITE9b + 0.2)]]}),
               P('terre9a', 'softDust', pos=[-2.4, 0.6, 5.0], opts={'at': BITE9, 'n': 12, 'size': 0.6, 'rise': 0.8, 'spread': 1.2, 'life': 0.8, 'color': '#A8784A', 'opacity': 0.85}),
               P('terre9b', 'softDust', pos=[2.3, 0.6, 5.0], opts={'at': BITE9b, 'n': 12, 'size': 0.6, 'rise': 0.8, 'spread': 1.2, 'life': 0.8, 'color': '#A8784A', 'opacity': 0.85}),
               P('terre9c', 'softDust', pos=[COWS[0][0][0], r(COWS[0][0][1] - 0.1), COWS[0][0][2]], opts={'at': r(BITE9b + 0.48), 'n': 6, 'size': 0.3, 'rise': 0.3, 'spread': 0.6, 'life': 0.5, 'color': '#C8A878', 'opacity': 0.7})],
        cams=[C9])
st.cue('engine', 'S09', 0.0, 0.2, 2.4); st.cue('thud', 'S09', BITE9, 0.35); st.cue('thud', 'S09', BITE9b, 0.3); st.cue('sfx:boing', 'S09', r(BITE9b + 0.22), 0.15)

# 10: « the parting in the middle ». Same framing: the colonel at the left reaches across with the back of the comb (his arm stretching over the
#     board) and draws one straight line down the middle from top to bottom; the general in front and a second general at the right lean in
D10 = st.dur('S10'); P10a, P10b = 0.22, 0.8
PART = [(r(P10a + (P10b - P10a) * i / 4), bpt(0.0, 0.85 - 1.7 * i / 4, 0.05)) for i in range(5)]
GEN10 = [1.25, 0, -0.55]
pk = [k(0.0, look=bpt(0, 0.6)), TK(0.0, {'R': R5(add(PART[0][1], [-0.25, 0.05, 0.15])), 'L': R5(off(COL_L, RYL, 0.05, -0.3, 1.0))}, {'R': 'grip', 'L': 'rest'}, {'lid': 0.2, 'mouth': 'line', 'brow': -0.5}, d=0.0)]
pk += [TK(t, {'R': R5(q, 1, 0.06)}, {'R': 'grip'}, {'lid': 0.1, 'mouth': 'clench', 'brow': -0.8}, (0.95, 1.06, 0.95), d=0.14 if i else 0.2, e='linear', keep=True) for i, (t, q) in enumerate(PART)]
pk += [k(r(P10a + 0.15), look=PART[2][1], lookDur=0.2), k(r(P10b + 0.1), look='camera', lookDur=0.1)]
st.shot('S10', 'office', setOpts=OFFICE, look=WARLOOK, actors=[
        OSGEN('S10', keys=[TK(0.3, bend={'spine': SP(0.08), 'neck': SP(0.1)}, d=0.3, keep=True)]),
        act('colL', COL_L, RYL, 'stand', 'determined', keys=pk),
        act('general2', GEN10, yaw(GEN10, bpt(0, 0)), 'stand', 'neutral', keys=[k(0.0, look=bpt(0, 0.3)), TK(0.0, ATTEN(GEN10, -60), {'R': 'rest', 'L': 'rest'}, ATT, d=0.0),
            TK(0.25, bend={'spine': SP(0.35), 'neck': SP(0.3)}, face={'lid': 0.1, 'pop': 0.3, 'mouth': 'O', 'brow': 0.4}, d=0.3, keep=True), k(0.4, look=PART[3][1], lookDur=0.3)])],
        props=[BOARDP('S10', **DONE_BACK, part=[[P10a, 0.0], [P10b, 1.0]]), *OSGENP('S10'), CAP('capL10', 'colL'), EPA('epaL10', 'colL'), CAP('capG10', 'general2', 1.05), EPA('epaG10', 'general2'),
               P('peigne10', 'bigComb', pos=add(PART[0][1], [-0.25, 0.05, 0.15]), rot=[-BTL, 0, r(PI / 2 + 0.15)], opts={'len': 0.5}, keys=[k(0.0, to=PART[0][1], dur=P10a), *[k(t, to=q, dur=0.14, ease='linear') for (t, q) in PART[1:]]])],
        cams=[C_OS])
st.cue('sfx:scratch', 'S10', P10a, 0.3); st.cue('sfx:ding', 'S10', r(P10b + 0.05), 0.15)

# ================================================================= straight above the country (S11): the stripe along Z, the tanks driving toward -Z
# 11: the country was cut in two; it still is. Almost straight down: a single line of four plain tanks drives nose to tail up the frame through a dark
#     forest and fields; behind the lead tank a bright bare earth stripe grows from the coast at the bottom to the coast at the top; they leave the frame
#     and the camera holds on the finished stripe, static
D11 = st.dur('S11'); RUN11 = 2.2
DD = 40.0
C11 = cam(0.0, [0.0, 62.0, 5.0], [0.0, 57.5, 4.6], [0.0, 0.0, 0.0], [0.0, 0.0, -0.4], lens=40)
chk('S11', C11, {'coastTop': [0, 0, -DD / 2], 'coastBot': [0, 0, DD / 2], 'stripeL': [-1.6, 0, 0], 'stripeR': [1.6, 0, 0], 'edgeL': [-13, 0, 0], 'edgeR': [13, 0, 0]})
Z0, Z1 = 26.0, -46.0
TANKS = [(i, r(Z0 + 8.6 * i), r(Z1 + 8.6 * i)) for i in range(3)]
st.shot('S11', 'spaceDark', setOpts={'stars': 10}, look={'sunDir': [0.5, 0.9, 0.3], 'exposure': 1.1}, actors=[],
        props=[P('pays11', 'forestStripe', pos=[0, 0, 0], opts={'w': 40, 'd': DD, 'sw': 5.0, 'lead': [[0.0, Z0 + 3.4], [RUN11, Z1 + 3.4]], 'n': 1600}),
               *[P(f'char11{i}', 'plainTank', pos=[0, 0.1, z0], ry=180, scale=1.6, opts={'rumble': [[0.0, D11, 0.02]]}, keys=[k(0.0, to=[0, 0.1, z1], dur=RUN11, ease='linear')]) for i, z0, z1 in TANKS]],
        cams=[C11])
st.cue('engine', 'S11', 0.0, 0.3, 1.9)

# 12: « and a little gel ». (a) Close on the felt map: the colonel's two hands squeeze a giant gel tube nozzle-down over the country, a fat blue blob
#     swells out onto the felt; it spreads and the whole head of hair goes glossy, a white shine streak; (b) the government froze the wages: a
#     factory gate (USINE), a minister in a plain gold sash hands the first worker in the queue a big light-blue block of ice with a yellow pay
#     envelope frozen inside: his knees buckle under it (squash, shiver, his breath steams); the others hold theirs flat toward us, deadpan
D12 = st.dur('S12'); SQ12 = (0.12, 0.5); GEL12 = (0.5, 1.0)
BLOB = [-0.08, 0.15]
TUBE = bpt(-0.4, 0.56, 0.3)
_Y = unit3([bpt(*BLOB, 0.05)[i] - TUBE[i] for i in range(3)]); _N = [0.0, math.sin(BTL), math.cos(BTL)]
_X = unit3(cross3(_Y, _N)); _Z = cross3(_X, _Y)
TRX, TRY, TRZ = axes_euler(_X, _Y, _Z)
C12 = cam(0.0, add(bpt(-0.1, 0.25, 0), [0.15, 0.1, 2.2]), add(bpt(-0.1, 0.25, 0), [0.12, 0.08, 2.0]), bpt(-0.1, 0.25, 0), bpt(-0.1, 0.25, 0), lens=42)
chk('S12', C12, {'tube': TUBE, 'blob': bpt(*BLOB, 0), 'mapL': bpt(-0.9, 0.2), 'mapR': bpt(0.9, 0.2), 'top': bpt(0, 0.95), 'bot': bpt(0, -0.6)})
TH = lambda s, q=0.0: [r(TUBE[i] + _X[i] * s * (0.085 - 0.035 * q)) for i in range(3)]
st.shot('S12', 'office', setOpts=OFFICE, look=WARLOOK, actors=[
        act('colL', [-1.3, 0, -0.45], 60, 'stand', 'determined', keys=[k(0.0, look=bpt(*BLOB)),
            TK(0.0, {'R': R5(TH(1)), 'L': R5(TH(-1))}, {'R': 'open', 'L': 'open'}, {'lid': 0.3, 'mouth': 'line', 'brow': -0.5}, d=0.0),
            TK(SQ12[0], {'R': R5(TH(1, 0.2)), 'L': R5(TH(-1, 0.2))}, {'R': 'fist', 'L': 'fist'}, {'lid': 0.25, 'mouth': 'clench', 'brow': -0.7}, (1.02, 0.98, 1.02), d=0.08, keep=True),
            TK(SQ12[1], {'R': R5(TH(1, 1.0)), 'L': R5(TH(-1, 1.0))}, {'R': 'fist', 'L': 'fist'}, {'lid': 0.05, 'mouth': 'clench', 'brow': -0.9, 'puff': 1}, (1.1, 0.9, 1.1), d=0.3, e='in', keep=True),
            TK(r(SQ12[1] + 0.25), {'R': R5(TH(1, 0.6)), 'L': R5(TH(-1, 0.6))}, {'R': 'grip', 'L': 'grip'}, {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}, (1, 1, 1), d=0.2, keep=True)])],
        props=[BOARDP('S12', **DONE_PART, gel=[[GEL12[0], 0.0], [GEL12[1], 1.0]], blob=[[SQ12[0], 0.0], [SQ12[1], 1.0], [GEL12[1], 0.7]], blobAt=BLOB, blobR=0.11, sweep=True),
               P('tube12', 'gelTube', pos=TUBE, ry=TRY, rot=[TRX, 0, TRZ], opts={'squeeze': [[SQ12[0], 0.0], [SQ12[1], 1.0], [r(SQ12[1] + 0.25), 0.6]], 'drop': 0.04}),
               P('brille12', 'twinkle', pos=bpt(0.25, 0.3, 0.1), opts={'at': 0.92, 's': 0.25, 'dur': 0.3})],
        cams=[C12])
st.cue('sfx:splat', 'S12', SQ12[1], 0.3); st.cue('sfx:ding', 'S12', 0.92, 0.2)

D12b = st.dur('S12b'); PUSH, GIVE, UP12 = 0.4, 0.62, 1.32
GATE = [0.0, 0, -4.2]
MIN = [-0.6, 0, -0.75]; RYM = 55
OUV = [[0.45, 0, -0.95], [1.1, 0, -2.3], [1.75, 0, -3.5]]; RYO = [-40, -12, -8]
C12b = cam(0.0, [0.3, 1.7, 5.0], [0.28, 1.68, 4.75], [0.3, 1.45, -1.3], [0.3, 1.45, -1.3], lens=42)
def ICE(p, ry=0, y=1.32): return off(p, ry, 0.36, 0.0, y)
ICE0 = off(MIN, RYM, 0.45, 0.0, 1.28)
ICE1 = ICE(OUV[0], RYO[0])
chk('S12b', C12b, {'minFace': add(MIN, [0, 2.05, 0]), **{f'ouv{i}face': add(p, [0, 2.05, 0]) for i, p in enumerate(OUV)}, 'ice0': ICE0, 'ice1': ICE1, 'iceLow': add(ICE1, [0, -0.45, 0]), 'ice2': ICE(OUV[1], RYO[1]), 'sign': [0, 4.0, -3.8]})
DUL = {'lid': 0.45, 'mouth': 'line', 'brow': -0.1}
HB = lambda c, dy=0.0: {'R': R5(add(c, [-0.3, dy, 0.02])), 'L': R5(add(c, [0.3, dy, 0.02]))}
def holder(who, p, ry, extra=()):
    return act(who, p, ry, 'stand', 'neutral', keys=[k(0.0, look='camera'), TK(0.0, HB(ICE(p, ry)), {'R': 'open', 'L': 'open'}, DUL, d=0.0), *extra])
o1 = [k(0.0, look=ICE0), TK(0.0, {'R': R5(off(OUV[0], RYO[0], 0.15, 0.3, 1.0)), 'L': R5(off(OUV[0], RYO[0], 0.15, -0.3, 1.0))}, {'R': 'open', 'L': 'open'}, {'lid': 0.3, 'mouth': 'line', 'brow': 0.1}, d=0.0),
      TK(PUSH, HB(ICE1, 0.05), {'R': 'open', 'L': 'open'}, {'lid': 0.2, 'mouth': 'line', 'brow': 0.3}, d=0.2, keep=True),
      TK(GIVE, HB(add(ICE1, [0, -0.45, 0])), {'R': 'open', 'L': 'open'}, {'lid': 0.0, 'pop': 0.35, 'mouth': 'O', 'brow': 0.7}, (1.32, 0.58, 1.32), d=0.07, e='out', keep=True),
      TK(r(GIVE + 0.45), HB(add(ICE1, [0, -0.42, 0])), {'R': 'open', 'L': 'open'}, {'lid': 0.1, 'pop': 0.2, 'mouth': 'wavy', 'brow': 0.5}, (1.3, 0.6, 1.3), d=0.4, e='linear', keep=True),
      TK(UP12, HB(add(ICE1, [0, 0.08, 0])), {'R': 'open', 'L': 'open'}, {'lid': 0.3, 'mouth': 'wavy', 'brow': -0.1}, (0.9, 1.12, 0.9), d=0.1, e='out', keep=True),
      TK(r(UP12 + 0.18), HB(ICE1), {'R': 'open', 'L': 'open'}, {'lid': 0.45, 'mouth': 'line', 'brow': -0.1}, (1, 1, 1), d=0.14, keep=True),
      k(GIVE, fx={'shiver': True}), k(r(UP12 + 0.1), fx={'shiver': False}), k(r(GIVE + 0.1), look='camera', lookDur=0.1), *blink(1.75, DUL)]
st.shot('S12b', 'grassland', setOpts={'clouds': 20, 'grass': '#9DB87A'}, look={'sunDir': [0.4, 0.8, 0.9]}, actors=[
        act('ministre', MIN, RYM, 'stand', 'neutral', keys=[k(0.0, look=ICE1),
            TK(0.0, HB(ICE0), {'R': 'open', 'L': 'open'}, {'lid': 0.35, 'mouth': 'smile', 'brow': 0.1}, d=0.0),
            TK(PUSH, HB(add(ICE1, [0, 0.05, 0])), {'R': 'open', 'L': 'open'}, {'lid': 0.3, 'mouth': 'smile', 'brow': 0.2}, (1.0, 1.0, 1.0), {'spine': SP(0.2)}, d=0.22, keep=True),
            TK(r(GIVE + 0.25), {'R': R5(off(MIN, RYM, 0.1, 0.3, 1.0)), 'L': R5(off(MIN, RYM, 0.1, -0.3, 1.0))}, {'R': 'rest', 'L': 'rest'}, {'lid': 0.3, 'mouth': 'smile', 'brow': 0.2}, (1, 1, 1), {'spine': SP(0.0)}, d=0.3, keep=True),
            k(PUSH, to=off(MIN, RYM, 0.25), dur=0.22, face='keep'), k(r(GIVE + 0.3), to=MIN, dur=0.35, face='keep'),
            k(r(GIVE + 0.35), look='camera', lookDur=0.15), *blink(1.5, {'lid': 0.3, 'mouth': 'smile', 'brow': 0.2})]),
        act('ouv1', OUV[0], RYO[0], 'stand', 'neutral', keys=o1),
        holder('ouv2', OUV[1], RYO[1], [*blink(0.9, DUL), *BREATHE(0.0, D12b, 0.6)]), holder('ouv3', OUV[2], RYO[2], [*blink(1.3, DUL), *BREATHE(0.2, D12b, 0.6)])],
        props=[P('usine12', 'factoryGate', pos=GATE, opts={'w': 14}),
               P('glace12a', 'iceBlock', pos=ICE0, ry=r(RYM - 40), opts={'seed': 1}, keys=[k(PUSH, to=ICE1, dur=0.22), k(PUSH, rotTo=[0, math.radians(RYO[0]), 0], dur=0.22), k(GIVE, to=add(ICE1, [0, -0.45, 0]), dur=0.07, ease='out'), k(r(GIVE + 0.45), to=add(ICE1, [0, -0.42, 0]), dur=0.4), k(UP12, to=add(ICE1, [0, 0.08, 0]), dur=0.1, ease='out'), k(r(UP12 + 0.18), to=ICE1, dur=0.14)]),
               P('glace12b', 'iceBlock', pos=ICE(OUV[1], RYO[1]), ry=RYO[1], opts={'seed': 2}), P('glace12c', 'iceBlock', pos=ICE(OUV[2], RYO[2]), ry=RYO[2], opts={'seed': 3}),
               P('souffle12', 'breathPuffs', on={'actor': 'ouv1', 'joint': 'head', 'offset': [0.06, 0.1, 0.19]}, opts={'times': [r(GIVE + 0.3), r(UP12 + 0.35)], 'dir': [0.2, -0.05, 0.2], 's': 0.08, 'life': 0.8})],
        cams=[C12b])
st.cue('thud', 'S12b', GIVE, 0.4); st.cue('sfx:glass', 'S12b', r(GIVE + 0.02), 0.2); st.cue('sfx:boing', 'S12b', UP12, 0.2)

# ================================================================= space (S13, S14): the country lies flat, its back (the ridges) toward +Z
# 13: seen from space, the country has a perfect haircut. From high above: the made-up country shaped like the top of a hairdo in the same green felt:
#     sandy shaved sides, four stepped ridges at the back (nearest), a dark parting line up the middle, a white gel shine streak; the ocean curves
#     away to the horizon, black space above; held, a glint runs along the gel streak, then COIFFÉ stamps over the black sky
D13 = st.dur('S13'); HS = 10.0; PR = 90
C13 = cam(0.0, [-1.2, 30.2, 42.4], [3.4, 29.3, 40.4], [0.0, 0.0, 0.0], [0.35, 0.0, 0.0], lens=40)
chk('S13', C13, {'horizon': [0, -9.3, -40.9], 'back': [0, 0, HS * 0.95 * 0.94], 'front': [0, 0, -HS * 0.95 * 0.94], 'sideL': [-HS * 0.8 * 0.9, 0, 0], 'sideR': [HS * 0.8 * 0.9, 0, 0], 'horizon': [0, -40, -250]})
SPACE = {'stars': 900}
st.shot('S13', 'spaceDark', setOpts=SPACE, look={'sunDir': [0.4, 0.9, 0.5], 'exposure': 1.1}, actors=[],
        props=[P('pays13', 'hairCountry', pos=[0, 0, 0], opts={'s': HS, 'planetR': PR, 'clouds': 16, 'sand': '#A8945A', 'ridgeDark': '#163A16', 'ridgeLight': '#9AE07A', 'ridgeH': True}),
               P('brille13', 'twinkle', pos=[-2.2, 1.8, -1.5], opts={'at': 0.6, 's': 3.0, 'dur': 0.4}), P('brille13b', 'twinkle', pos=[-0.8, 1.8, 2.0], opts={'at': 1.35, 's': 3.0, 'dur': 0.35}), P('brille13c', 'twinkle', pos=[-1.5, 1.8, 0.3], opts={'at': 2.3, 's': 2.5, 'dur': 0.35})],
        cams=[C13])
st.card('S13', 'COIFFÉ', at=1.95)
st.cue('sfx:ding', 'S13', 1.35, 0.25); st.cue('sfx:wind', 'S13', 0.0, 0.1, 2.0)

# 14: two jets held the mirror behind. Wider and lower, over the country to the horizon: two plain jets, noses up, flank a giant oval hand mirror they
#     hold by its rim above the horizon behind the country; the mirror rises into place and tilts twice like at the barber's, its glass painted with
#     the stepped back of the hairdo
D14 = st.dur('S14')
MIR = [0.0, 14.5, -34.0]
C14 = cam(0.0, [0.0, 26.0, 46.0], [0.6, 24.6, 42.5], [0.0, 7.0, -22.0], [0.1, 7.3, -22.0], lens=40)
chk('S14', C14, {'mirTop': add(MIR, [0, 7.0, 0]), 'mirBot': add(MIR, [0, -7.0, 0]), 'handle': add(MIR, [0, -12.0, 0]), 'jetL': add(MIR, [-9.6, 0, -1]), 'jetR': add(MIR, [9.6, 0, -1]), 'wingL': add(MIR, [-12.5, 0, -1]), 'jetNose': add(MIR, [-9.6, 8.5, -1]), 'countryNear': [0, 0, 12.0], 'countryFar': [0, 0, -12.0]})
st.shot('S14', 'spaceDark', setOpts=SPACE, look={'sunDir': [0.4, 0.9, 0.6], 'exposure': 1.1}, actors=[],
        props=[P('pays14', 'hairCountry', pos=[0, 0, 0], opts={'s': HS, 'planetR': PR, 'clouds': 16, 'sand': '#A8945A', 'ridgeDark': '#163A16', 'ridgeLight': '#9AE07A', 'ridgeH': True}),
               P('miroir14', 'mirrorJets', pos=add(MIR, [0, -6.0, 0]), opts={'mw': 9, 'mh': 12, 'js': 0.5, 'tilt': 0.25, 'burner': 0.8},
                 keys=[k(0.0, to=MIR, dur=0.6, ease='out'), k(0.62, rotTo=[0.0, 0.0, 0.24], dur=0.2, ease='out'), k(1.1, rotTo=[0.0, 0.0, -0.22], dur=0.22, ease='out'), k(1.6, rotTo=[0.0, 0.0, 0.03], dur=0.25), k(1.85, rotTo=[0.0, 0.0, 0.0], dur=0.2)])],
        cams=[C14])
st.cue('sfx:jet', 'S14', 0.0, 0.35); st.cue('sfx:ding', 'S14', 1.4, 0.15)

# 15: he said « perfect » and hung up. Living room, the framing of 1: tuft still up, he nods politely twice into the handset (« parfait »), then lowers
#     it and sets it down on the cream phone on the table at his side (a little bow with it), and looks at us
D15 = st.dur('S15'); NOD15 = [0.6, 0.95]; HANG15 = 1.45
HSB = add(PHONEB, [0.0, 0.17, -0.03])
POL = {'lid': 0.25, 'mouth': 'smile', 'brow': 0.4}
k15 = [TK(0.0, {'R': R5(EARR), 'L': R5(off(HERO, 0, 0.05, -0.3, 1.0))}, {'R': 'grip', 'L': 'rest'}, POL, d=0.0)]
for tn in NOD15: k15 += [TK(tn, bend={'neck': SP(0.4), 'spine': SP(0.1)}, face={'lid': 0.5, 'mouth': 'bigsmile', 'brow': 0.5}, sq=(1.04, 0.95, 1.04), d=0.09, keep=True), TK(r(tn + 0.16), bend={'neck': SP(-0.05), 'spine': SP(0.0)}, face=POL, sq=(1, 1, 1), d=0.12, keep=True)]
k15 += [TK(r(HANG15 - 0.3), {'R': R5(add(HSB, [0.05, 0.25, 0.1]))}, {'R': 'grip'}, POL, (1.0, 0.97, 1.0), {'spine': SP(0.1), 'neck': SP(0.0)}, d=0.3, keep=True),
        TK(HANG15, {'R': R5(add(HSB, [0, 0.03, 0]))}, {'R': 'grip'}, POL, (1.03, 0.95, 1.03), {'spine': SP(0.14), 'neck': SP(-0.05)}, d=0.12, keep=True),
        TK(r(HANG15 + 0.3), {'R': R5(off(HERO, 0, 0.05, 0.3, 1.0))}, {'R': 'rest'}, POL, (1, 1, 1), {'spine': SP(0.0), 'neck': SP(0.0)}, d=0.25, keep=True),
        k(0.0, look='camera'), k(r(HANG15 - 0.3), look=add(HSB, [0.3, 0.9, 1.5]), lookDur=0.15), k(r(HANG15 + 0.15), look='camera', lookDur=0.15), *blink(2.05, POL)]
st.shot('S15', 'livingRoom', setOpts=LIV, look={'sunDir': [0.4, 0.8, 0.9]}, actors=[act('mec', HERO, 0, 'stand', 'happy', keys=k15)],
        props=[TUFT('meche15', 'mec'), EAR('tel15', 'mec', color='#EDE6D2', keys=[k(r(HANG15 - 0.02), visible=False)]),
               P('combine15', 'handset', pos=HSB, rot=[0, r(math.radians(20)), r(PI / 2)], opts={'len': 0.32, 'color': '#EDE6D2'}, keys=[k(0.0, visible=False), k(r(HANG15 - 0.02), visible=True)]),
               P('table15', 'table', pos=TABLE1, opts={'w': 0.5, 'd': 0.5, 'h': 1.2, 'color': '#2E7A7A'}), P('base15', 'redDeskPhone', pos=PHONEB, ry=20, opts={'color': '#EDE6D2'})],
        cams=[C1])
st.cue('clack', 'S15', HANG15, 0.3)

# 16: the same day the general called the front. Wrong number. War room, the framing of 2: the general dials the big red phone with a long finger
#     (the dial spins back), a colonel holding the clippers stands at attention beside him; he snaps the handset to his ear on « Faux numéro »
D16 = st.dur('S16'); DIALW = [(0.3, 1.05), (1.12, 1.78)]; UP16 = 2.05; PS16 = 1.35
C16 = cam(0.0, [-0.2, 1.75, 7.3], [-0.5, 1.8, 4.9], [-0.2, 1.42, -0.5], [-0.65, 1.45, 0.4], lens=40, ease='out')
COL16 = [-0.15, 0, -0.1]
_ry = math.radians(25)
def _rot(v): return [v[0] * math.cos(_ry) + v[2] * math.sin(_ry), v[1], -v[0] * math.sin(_ry) + v[2] * math.cos(_ry)]
DC = add(PH2, _rot([0.0, 0.108 * PS16, 0.06 * PS16]))                 # the dial's centre and its plane (the phone turned 25 degrees)
DX, DY, DN = _rot([1, 0, 0]), _rot([0, 0.454, -0.891]), _rot([0, 0.891, 0.454])
def hole(a, n=0.0, rr=0.052): return [r(DC[i] + PS16 * rr * (math.cos(a) * DX[i] + math.sin(a) * DY[i]) + n * DN[i]) for i in range(3)]
HS16 = add(PH2, _rot([0.0, 0.17 * PS16, -0.03 * PS16]))
k16 = [k(0.0, look=DC), TK(0.0, {'R': R5(off(GEN2, RYG2, 0.1, 0.32, 1.0)), 'L': R5(add(HS16, [0, 0.03, 0]))}, {'R': 'rest', 'L': 'grip'}, {'lid': 0.35, 'mouth': 'line', 'brow': -0.6}, (1, 1, 1), {'spine': SP(0.2)}, d=0.0)]
for (a, b) in DIALW:
    m = r(a + (b - a) * 0.62); A0 = 0.9
    k16 += [TK(r(a - 0.15), {'R': R5(hole(A0, 0.06), 1, 0.02)}, {'R': 'point'}, {'lid': 0.25, 'mouth': 'line', 'brow': -0.7}, (1, 1, 1), {'spine': SP(0.3)}, d=0.13, keep=True),
            TK(a, {'R': R5(hole(A0, -0.005), 1, 0.02)}, {'R': 'point'}, {'lid': 0.2, 'mouth': 'clench', 'brow': -0.8}, (1.03, 0.97, 1.03), {'spine': SP(0.34)}, d=0.06, e='in', keep=True)]
    for j in range(1, 5):
        k16.append(TK(r(a + (m - a) * j / 4), {'R': R5(hole(A0 - 2.4 * j / 4, -0.005), 1, 0.02)}, {'R': 'point'}, {'lid': 0.2, 'mouth': 'clench', 'brow': -0.8, 'gx': 0.2 * (j % 2)}, (1.03, 0.97, 1.03), {'spine': SP(0.34)}, d=r((m - a) / 4), e='linear', keep=True))
    k16.append(TK(r(m + 0.08), {'R': R5(hole(A0 - 2.4, 0.09), 1, 0.02)}, {'R': 'point'}, {'lid': 0.3, 'mouth': 'line', 'brow': -0.6}, (1, 1, 1), {'spine': SP(0.28)}, d=0.08, keep=True))
k16 += [TK(1.86, {'R': R5(off(GEN2, RYG2, 0.1, 0.32, 1.0))}, {'R': 'rest'}, {'lid': 0.2, 'mouth': 'line', 'brow': -0.8, 'gx': -0.8}, (1, 1, 1), {'spine': SP(0.15)}, d=0.1, keep=True),
        TK(1.92, face={'lid': 0.2, 'mouth': 'line', 'brow': -0.8, 'gx': 0.8}, d=0.04, keep=True),
        TK(r(UP16 - 0.1), {'L': R5(add(HS16, [0.0, -0.02, -0.06]))}, {'L': 'grip'}, {'lid': 0.3, 'mouth': 'clench', 'brow': -0.8}, (1.14, 0.84, 1.14), {'spine': SP(0.25)}, d=0.08, keep=True),
        TK(UP16, {'L': R5(off(GEN2, RYG2, 0.1, -0.25, 1.88))}, {'L': 'grip'}, {'lid': 0.1, 'mouth': 'O', 'brow': -0.5}, (0.9, 1.12, 0.9), {'spine': SP(0.0)}, d=0.07, e='out', keep=True),
        TK(r(UP16 + 0.12), face={'lid': 0.15, 'mouth': 'scream', 'brow': -0.8, 'jaw': 0.5}, sq=(1.06, 0.95, 1.06), d=0.06, keep=True), TK(r(UP16 + 0.4), face=ATT, sq=(1, 1, 1), d=0.15, keep=True),
        k(r(UP16 + 0.05), look='camera', lookDur=0.1), *blink(2.75, ATT)]
DIALS = [a for a, b in DIALW]
st.shot('S16', 'office', setOpts=OFFICE, look=WARLOOK, actors=[
        act('general', GEN2, RYG2, 'stand', 'determined', keys=k16),
        act('colB', COL16, -15, 'stand', 'neutral', keys=[k(0.0, look='camera'), TK(0.0, {'R': R5(off(COL16, -15, 0.32, 0.12, 1.38)), 'L': R5(off(COL16, -15, 0.04, -0.3, 0.98))}, {'R': 'grip', 'L': 'open'}, ATT, d=0.0),
            *blink(0.7, ATT), *blink(1.55, ATT), k(1.0, look=DC, lookDur=0.15), k(1.4, look='camera', lookDur=0.15), *BREATHE(0.0, D16, 0.5, 0.015), k(UP16, look=add(GEN2, [0, 2.0, 0]), lookDur=0.12), k(r(UP16 + 0.4), look='camera', lookDur=0.15)]),
        act('colA', COLA2, 20, 'stand', 'neutral', keys=[k(0.0, look='camera'), TK(0.0, ATTEN(COLA2, 20), {'R': 'open', 'L': 'open'}, ATT, d=0.0), *blink(0.5, ATT), *blink(1.3, ATT), *blink(2.3, ATT), *BREATHE(0.1, D16, 0.5, 0.015), k(0.8, look=DC, lookDur=0.15), k(1.2, look='camera', lookDur=0.15), k(UP16, look=add(GEN2, [0, 2.0, 0]), lookDur=0.12)])],
        props=[BOARDP('S16', **DONE_ALL), P('table16', 'table', pos=TAB2, opts={'w': 0.55, 'd': 0.5, 'h': 0.85, 'color': '#3A3530'}),
               P('rouge16', 'redDeskPhone', pos=PH2, ry=25, opts={'s': PS16, 'dial': [list(w) for w in DIALW]}),
               P('combine16a', 'handset', pos=HS16, rot=[0, r(math.radians(25)), r(PI / 2)], opts={'len': 0.36, 'color': '#D8262C'}, keys=[k(r(UP16 - 0.04), visible=False)]),
               EAR('combine16b', 'general', side=-1, color='#D8262C', keys=[k(0.0, visible=False), k(r(UP16 - 0.04), visible=True)]),
               P('tond16', 'barberClippers', on={'actor': 'colB', 'hand': 'R', 'offset': [0.0, 0.0, 0.03], 'rot': CLHAND}, opts={'s': 1.7}),
               CAP('cap16', 'general', 1.05), EPA('epa16', 'general'), CAP('capA16', 'colA'), EPA('epaA16', 'colA'), CAP('capB16', 'colB'), EPA('epaB16', 'colB')],
        cams=[C16])
for a_, b_ in DIALW: st.cue('sfx:tick', 'S16', a_, 0.2); st.cue('sfx:rattleShort', 'S16', r(a_ + (b_ - a_) * 0.62), 0.2)
st.cue('clack', 'S16', UP16, 0.3)

# ================================================================= the barber shop (S17, S18): back wall at z -2.2, the wall phone on the left wall
SHOP = {'color': '#E8E2D6'}
CAPE = {'len': 0.4, 'w': 0.42, 'fwd': 0.3}
CHAIR = [0.3, 0.03, -1.05]
HERO_SIT = [0.3, 0.12, -1.0]
BARB17 = [-0.72, 0.03, -1.6]; RYB17 = 15
WPH = [-1.02, 1.62, -2.17]
WHS = add(WPH, [0.0, 0.0, 0.11])
C17 = cam(0.0, [0.0, 1.65, 3.7], [-0.02, 1.65, 3.5], [-0.28, 1.45, -1.3], [-0.28, 1.45, -1.3], lens=42)
chk('S17', C17, {'barbFace': add(BARB17, [0, 2.05, 0]), 'barbTop': add(BARB17, [0, 2.55, 0]), 'clip': off(BARB17, RYB17, 0.38, -0.12, 1.4), 'heroFace': add(HERO_SIT, [0, 1.6, 0]), 'heroTuft': add(HERO_SIT, [0, 2.25, 0]), 'phone': WPH, 'pole': [1.9, 1.7, -2.0]})

# 17: he got the barber: « Shave it all. » The barber shop: the barber picks up the wall phone, listens, freezes (eyes out, a shiver), then snaps to
#     attention (stretched up, heels together, phone at his ear), and the clippers in his other hand buzz on at chest height on « Rasez tout »;
#     behind him the hero sits in the red chair under a striped cape, tuft up, smiling at us
D17 = st.dur('S17'); PICK17, FREEZE17, SNAP17, BUZZ17 = 0.15, 0.42, 0.85, 1.42
EARB = off(BARB17, RYB17, 0.08, 0.27, 2.0)
CLIP17 = off(BARB17, RYB17, 0.36, -0.12, 1.42)
kb = [k(0.0, look=WPH), TK(0.0, {'R': R5(add(WHS, [0.05, -0.05, 0.05])), 'L': R5(CLIP17)}, {'R': 'open', 'L': 'grip'}, {'lid': 0.3, 'mouth': 'smile', 'brow': 0.2}, d=0.0),
      TK(PICK17, {'R': R5(WHS)}, {'R': 'grip'}, {'lid': 0.3, 'mouth': 'smile', 'brow': 0.2}, d=0.12, keep=True),
      TK(r(PICK17 + 0.2), {'R': R5(EARB)}, {'R': 'grip'}, {'lid': 0.25, 'mouth': 'O', 'brow': 0.3}, d=0.15, keep=True),
      TK(FREEZE17, face={'lid': 0.0, 'pop': 0.75, 'mouth': 'O', 'brow': 1.0}, sq=(0.92, 1.1, 0.92), scl={'head': [0.92, 1.15, 0.92]}, d=0.05, e='out', keep=True),
      k(FREEZE17, fx={'shiver': True}), k(r(SNAP17 - 0.05), fx={'shiver': False}),
      TK(r(SNAP17 - 0.08), face={'lid': 0.1, 'pop': 0.3, 'mouth': 'line', 'brow': -0.6}, sq=(1.1, 0.88, 1.1), scl={'head': [1, 1, 1]}, d=0.08, keep=True),
      TK(SNAP17, face=ATT, sq=(0.88, 1.16, 0.88), d=0.05, e='out', keep=True),
      TK(r(SNAP17 + 0.18), face=ATT, sq=(1.02, 0.98, 1.02), d=0.1, keep=True), TK(r(SNAP17 + 0.32), face=ATT, sq=(1, 1, 1), d=0.1, keep=True),
      k(r(FREEZE17 + 0.05), look='camera', lookDur=0.08),
      TK(BUZZ17, face={'lid': 0.2, 'mouth': 'clench', 'brow': -0.8}, d=0.06, keep=True), *blink(2.1, {'lid': 0.2, 'mouth': 'clench', 'brow': -0.8})]
CALM = {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}
st.shot('S17', 'whiteVoid', setOpts=SHOP, lighting='interior', look={'sunDir': [0.3, 0.9, 0.8]}, actors=[
        act('barbier', BARB17, RYB17, 'stand', 'happy', keys=kb),
        act('mec', HERO_SIT, 0, 'sit', 'happy', keys=[k(0.0, look='camera'), TK(0.0, {'R': R5(add(HERO_SIT, [-0.3, 0.68, 0.25])), 'L': R5(add(HERO_SIT, [0.3, 0.68, 0.25]))}, {'R': 'rest', 'L': 'rest'}, CALM, d=0.0), *blink(1.0, CALM), *blink(2.0, CALM)])],
        props=[P('salon17', 'barberShop', pos=[0, 0, 0], opts={'w': 4.8}), P('fauteuil17', 'barberChair', pos=CHAIR),
               *[P(f'smear17{j}', 'smearArc', pos=[0, 0, 0], opts={'pts': [off(BARB17, RYB17, 0.12, sx, 1.1), off(BARB17, RYB17, 0.12, sx, 2.45)], 'win': [r(SNAP17 - 0.04), r(SNAP17 + 0.05)], 'color': '#BFDDEA', 'r': 0.07, 'opacity': 0.55}) for j, sx in enumerate((-0.22, 0.22))],
               P('cape17', 'barberCape', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.42, 0.04]}, opts=CAPE), TUFT('meche17', 'mec'),
               P('mural17', 'wallPhone', pos=WPH), P('combine17a', 'handset', pos=WHS, rot=[0, 0, 0], opts={'len': 0.28, 'color': '#EDE6D2'}, keys=[k(r(PICK17 + 0.05), visible=False)]),
               EAR('combine17b', 'barbier', color='#EDE6D2', keys=[k(0.0, visible=False), k(r(PICK17 + 0.05), visible=True)]),
               P('tond17', 'barberClippers', on={'actor': 'barbier', 'hand': 'L', 'offset': [0.0, 0.0, 0.03], 'rot': CLHAND}, opts={'s': 1.7, 'buzz': [[BUZZ17, 9]]})],
        cams=[C17])
st.cue('sfx:ring', 'S17', 0.0, 0.2); st.cue('sfx:boing', 'S17', FREEZE17, 0.2); st.cue('clack', 'S17', SNAP17, 0.35); st.cue('engine', 'S17', BUZZ17, 0.22, 0.9)

# 18: this man was in the chair. He only wanted the tips. Frontal and held: the hero alone in the red chair under the cape, his box head shaved smooth
#     and shining (a glint), his tuft on the floor in front of him; his eyes roll up to his scalp, then down to the tuft, then to us, deadpan; behind
#     him the barber in an army helmet stands at attention, the clippers at his chest; a long hold
D18 = st.dur('S18')
BARB18 = [0.95, 0.03, -2.0]
FLOORT = [-0.18, 0.035, -0.95]
C18 = cam(0.0, [0.3, 2.3, 2.6], [0.3, 2.26, 2.42], [0.35, 0.9, -1.0], [0.35, 0.9, -1.0], lens=46)
chk('S18', C18, {'heroFace': add(HERO_SIT, [0, 1.6, 0]), 'heroTop': add(HERO_SIT, [0, 1.95, 0]), 'tuft': FLOORT, 'tuftTop': add(FLOORT, [0, 0.12, 0]), 'barbFace': add(BARB18, [0, 2.05, 0]), 'helmetTop': add(BARB18, [0, 2.55, 0]), 'clip': off(BARB18, -10, 0.34, 0.0, 1.4)})
FLAT18 = {'lid': 0.45, 'mouth': 'line', 'brow': -0.1}
st.shot('S18', 'whiteVoid', setOpts=SHOP, lighting='interior', look={'sunDir': [0.3, 0.9, 0.8]}, actors=[
        act('mecChauve', HERO_SIT, 0, 'sit', 'neutral', keys=[k(0.0, look='camera'), TK(0.0, {'R': R5(add(HERO_SIT, [-0.3, 0.68, 0.25])), 'L': R5(add(HERO_SIT, [0.3, 0.68, 0.25]))}, {'R': 'rest', 'L': 'rest'}, FLAT18, d=0.0),
            TK(0.9, face={**FLAT18, 'lid': 0.15, 'gy': -1.3, 'brow': 0.4}, d=0.1, keep=True), TK(1.05, bend={'neck': SP(-0.32)}, d=0.24, keep=True), TK(1.5, face={**FLAT18, 'lid': 0.3, 'gy': 1.2, 'gx': 0.7}, bend={'neck': SP(-0.32)}, d=0.1, keep=True), TK(1.65, bend={'neck': SP(0.42), 'spine': SP(0.08)}, d=0.25, keep=True),
            TK(2.25, face={**FLAT18, 'lid': 0.5}, d=0.12, keep=True), TK(2.4, bend={'neck': SP(0.0), 'spine': SP(0.0)}, d=0.2, keep=True), *blink(2.9, {**FLAT18, 'lid': 0.5}), *BREATHE(0.0, D18, 0.7, 0.01)]),
        act('barbier', BARB18, -10, 'stand', 'neutral', keys=[k(0.0, look='camera'), TK(0.0, {'L': R5(off(BARB18, -10, 0.34, -0.1, 1.4)), 'R': R5(off(BARB18, -10, 0.04, 0.3, 0.98))}, {'L': 'grip', 'R': 'open'}, ATT, (1, 1.02, 1), d=0.0),
            *blink(1.2, ATT), *blink(2.2, ATT), *blink(3.1, ATT), *BREATHE(0.0, D18, 0.7, 0.012)])],
        props=[P('salon18', 'barberShop', pos=[0, 0, 0], opts={'w': 4.8}), P('fauteuil18', 'barberChair', pos=CHAIR),
               P('cape18', 'barberCape', on={'actor': 'mecChauve', 'joint': 'torso', 'offset': [0.0, 0.42, 0.04]}, opts=CAPE),
               P('crane18', 'baldCap', on={'actor': 'mecChauve', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={'w': 0.24, 'h': 0.5, 'd': 0.17, 'skin': '#E8A262', 'top': '#C98A52', 'shineA': 0.3}),
               P('brille18', 'chvShine', on={'actor': 'mecChauve', 'joint': 'head', 'offset': [0.0, 0.51, 0.03]}, opts={'s': 1.3, 'twinkle': [0.55, 2.35, 3.45], 'tw0': 0.0, 'flare': [[0.55, 1.8]]}),
               P('meche18', 'heroTuft', pos=FLOORT, ry=20, opts={'floor': True, 's': 1.7}),
               HELMET('casque18', 'barbier', s=1.0),
               P('tond18', 'barberClippers', on={'actor': 'barbier', 'hand': 'L', 'offset': [0.0, 0.0, 0.03], 'rot': CLHAND}, opts={'s': 1.7})],
        cams=[C18])
st.cue('sfx:ding', 'S18', 0.55, 0.2)

# a toon key that names one hand's reach replaces the whole reach (keepPose merges only the top level): carry the other hand's reach and hand
# pose from the previous keys of the same actor so a one-handed gesture never drops the other hand (the phone at his ear, the clippers at the chest)
for _sc in st.scenes:
    for _a in _sc['actors']:
        _run = {'reach': {}, 'hands': {}}
        for _kk in sorted((x for x in _a.get('keys', []) if isinstance(x, dict) and 'toon' in x), key=lambda x: x.get('at', 0)):
            for _n in ('reach', 'hands'):
                if _n in _kk['toon']: _kk['toon'][_n] = {**_run[_n], **_kk['toon'][_n]}; _run[_n] = dict(_kk['toon'][_n])
print('\n'.join(CHECKS))

MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
SOLD = {'outfit': 'suit', 'suit': '#5B6638', 'pants': '#4E5730', 'shirt': '#D9D3B6', 'lapel': '#4E5730', 'tie': '#3B4224', 'cuff': '#5B6638', 'hat': 'none', 'hair': 'bald',
        'gloves': '#E3A877', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': {'holdLife': 2.2, 'shift': 2.0, 'breathe': 2.0}}
OFF = {**SOLD, 'suit': '#4E5A34', 'lapel': '#3E4828', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.1}}
OLDM = {'hat': 'none', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX}
st.write("Le faux numéro", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'mecChauve': {**MEC, 'hairColor': '#E2B48E'},
    'general': {**OFF, 'preset': 'commissaire', 'seed': 941, 'hair': 'receding', 'facial': 'mustache'},
    'general2': {**OFF, 'preset': 'commissaire', 'seed': 942, 'hair': 'receding', 'facial': 'beard'},
    'colA': {**OFF, 'preset': 'cop', 'seed': 943, 'facial': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}},
    'colB': {**OFF, 'preset': 'cop2', 'seed': 944, 'facial': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}},
    'colL': {**OFF, 'preset': 'cop', 'seed': 945, 'facial': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}},
    'colR': {**OFF, 'preset': 'cop2', 'seed': 946, 'facial': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}},
    **{f'sold{j}': {**SOLD, 'preset': 'cop' if j % 2 else 'cop2', 'seed': 950 + j} for j in (1, 2, 3, 4)},
    'bain1': {'preset': 'tourist', 'seed': 961, 'hat': 'none', 'suit': '#F2C94C', 'shirt': '#F2C94C', 'cuff': '#E3A877', 'pants': '#F2C94C', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.14}, 'toon': EX},
    'bain2': {'preset': 'mamie', 'seed': 962, 'glasses': False, 'suit': '#E87A5A', 'lapel': '#E87A5A', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'pet1': {**OLDM, 'preset': 'proviseur', 'seed': 971, 'suit': '#B89A6A', 'lapel': '#A88A5A', 'tie': '#E8E0D0', 'hair': 'crew', 'hairColor': '#EEEEEE'},
    'pet2': {**OLDM, 'preset': 'fermier', 'seed': 972, 'hairColor': '#F2F2F2', 'facial': 'mustache', 'beardColor': '#F2F2F2', 'suit': '#8A9A6A', 'shirt': '#E8E0D0', 'lapel': '#7A8A5A'},
    'pet3': {**OLDM, 'preset': 'commissaire', 'seed': 973, 'hairColor': '#EEEEEE', 'suit': '#A86A5A', 'lapel': '#985A4A', 'tie': '#E8E0D0', 'facial': 'mustache'},
    'ministre': {'preset': 'politique', 'seed': 981, 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#3A4A6A', 'hairColor': '#BDBDBD', 'sash': '#C9A646', 'sashW': 0.12, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    **{f'ouv{j}': {'preset': 'worker', 'seed': 990 + j, 'hat': 'none', 'glasses': False, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX} for j in (1, 2, 3)},
    'barbier': {'preset': 'doctor', 'seed': 999, 'glasses': False, 'hair': 'slick', 'hairColor': '#2A2420', 'facial': 'mustache', 'suit': '#BFDDEA', 'lapel': '#A8CCDC', 'pants': '#3A3D44', 'tie': '#3A3D44', 'build': {'width': 1.0, 'headWidth': 1.2, 'height': 0.92}, 'toon': EX},
    **{f'vache{i}': {'type': 'creature', 'name': 'cow', 'opts': {'seed': 2 + i}} for i in (1, 2, 3, 4)},
})
