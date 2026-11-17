#!/usr/bin/env python3
"""La guêpe (story 81, cycle 43; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man filed a complaint against a wasp. The police charged. He demanded an air strike. A satellite found the wasp. Near the sugar bowl. An
aircraft carrier put to sea. In the sink. A fighter took off from the sink. It missed the wasp. It razed the building. And the town hall, as a
precaution. The wasp finished its sugar. The front froze between the fridge and the sink. All winter, sugar was rationed. The State asked for a
ceasefire. The wasp got the sugar bowl. The general staff gave itself medals. Even the wasp. It was a fly.
Staging: at his breakfast table he jabs a finger at a small dark insect on the rim of his sugar bowl while a policeman takes it down; riot police
burst in behind shields, the plates leap off the shelf, he ducks with his cup, the insect hovers on, untouched; he slaps a stamped air-strike
request onto the clipboard of the policeman, now in a dented riot helmet; a satellite over the Earth swivels its dish down, a green glint; seen
from straight above, a red map pin drops onto the sugar bowl; a grey aircraft carrier cuts through the sea, horn blasting; it is jammed in his
kitchen sink, water pouring over the edge; on its deck a fighter on the catapult, steam, the man beyond the bow with his cup; it shoots off and
swoops past his head (his hair blown flat, he does not blink); two missiles pass either side of the hovering insect and of his head and blow two
holes in the back wall; the building is a heap of rubble, the man on top in his chair with his cup; down the street the town hall pancakes, its
flag slides down the pole that stays standing; on the rubble the insect eats from the open sugar bowl; the front: soldiers behind sandbags by the
carrier, the fridge sandbagged opposite with the insect's black flag, the man at his table in no man's land; the insect on the fridge looks across;
snow; an officer hands each shivering soldier one sugar cube; a white handkerchief on a stick rises from the carrier's hatch; the insect plants
its flag in the sugar bowl's lid over a blank treaty (SIGNÉ); a row of generals so loaded with medals they all tip forward; a general's big
fingers pin a tiny medal on the insect, which salutes (DÉCORÉE); framed exactly like the first shot, then pushing in: it is plainly a fly, big
red eyes, rubbing its front legs, a medal on its flank; behind it the snowed-on man sips his cup.
Natural look; cycle 43: props_guepe.js (houseFly, sugarBowl, pennantFlag, carrier, waterSpill, plateShelf, riotShield, riotHelmet, armyHelmet, kitchenTap, ruinsBackdrop,
strikeForm, lensGlint, mapPin, satReticle, wallImpact, rubbleHeap, ruinFloor, collapse, medalRack, treatySheet); fighterJet, missileSalvo,
satellite (props_lunettes), earthGlobe, islandSink (props_ventouse), fridge, table, chair, mug, clipboardProp, sandbags (props_eternuement),
snowCap (props_langue), whiteFlag, toonPuff (props_bocal), kepi, sugarCube, townHall reused.
The insect is one model throughout: a dark grey fly with clear wings, no stripes and no sting; small in frame until the last shot.
Lessons applied from the start: `lens` is the vertical field (bigger = wider); hops and slides glide; main props and faces above the caption band
(0.77-0.86); the callback tops its setup (the last shot opens on the first shot's frame and pushes in to the fly)."""
from story_kit import *
import math

st = Story('guepe', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0),
         ('S08', 'L08', 0), ('S09', 'L08', 5), ('S10', 'L09', 0), ('S11', 'L10', 0), ('S12', 'L11', 0), ('S13', 'L12', 0), ('S14', 'L13', 0),
         ('S15', 'L13', 6), ('S16', 'L14', 0), ('S17', 'L14', 3), ('S18', 'L15', 0), ('S19', 'L16', 0), ('S20', 'L17', 0), ('S21', 'L18', 0),
         ('S22', 'L19', 0)])

PI = math.pi
def r(v, n=3): return round(v, n)
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(26, 60), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def loc(p, ry, v, s=1.0):
    """the world position of the local point v of something standing at p, turned ry degrees about Y and scaled s"""
    a_ = math.radians(ry); return [r(p[0] + s * (v[0] * math.cos(a_) + v[2] * math.sin(a_))), r(p[1] + s * v[1]), r(p[2] + s * (-v[0] * math.sin(a_) + v[2] * math.cos(a_)))]

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
DEAD = {'lid': 0.4, 'mouth': 'line'}
STREET = {'eiffelStyle': 'v2', 'clear': [-40.0, 10.0], 'clearL': [-40.0, 10.0]}
SNOW = {**STREET, 'snow': True, 'snowN': 5200, 'snowSize': 0.07}   # (review 2) denser snowfall
# (review 2) winter is lit as winter: an overcast, cooler, less saturated grade and a soft blue-grey light on every shot of the snowy block (S16-S21)
WINTER = {'grade': 'saturate(0.68) contrast(0.95) brightness(1.04) hue-rotate(-4deg)', 'light': {'hemi': 2.1, 'sky': '#DCE5EE', 'ground': '#9AA3AD', 'keyI': 0.75, 'key': '#E4ECF4', 'bg': '#D3DBE3'}}
KIT = {'fridge': False}

# the kitchen, and the same layout in its ruins: the table in the middle, him behind it facing us, the sink at the back left with the carrier
# jammed in it (its bow pointing at him), the fridge at the back right
TB = [0.0, 0, -1.2]; TH = 0.76
SB = [0.0, TH, -0.95]                                      # the sugar bowl, near the front edge of the table
RIM = [0.0, r(TH + 0.085), r(-0.95 + 0.074)]             # the front of its rim (where the insect lands)
LIDTOP = r(TH + 0.085 + 0.08 * 0.42)                       # the top of its lid
MAN = [0.0, 0, -1.8]; CHAIR = [0.0, 0, -1.95]
SINK = [-1.9, 0, -2.5]; SINKH = 0.9                        # islandSink, its long side along X (x -2.65 .. -1.15)
CARR = [-1.75, 0.88, -2.5]; CARRY = 90                     # the carrier: waterline 2 cm under the sink's top, the bow toward +X (toward him)
DECK = r(0.88 + 0.13 * 1.8 + 0.012 * 1.8 + 0.0015)       # its deck
CAT0 = [r(CARR[0] - 0.32 * 1.8), DECK, r(CARR[2] - 0.06 * 1.8)]; CAT1 = [r(CARR[0] + 0.45 * 1.8), DECK, CAT0[2]]   # its catapult (bow end)
HATCH = [r(CARR[0] - 0.2 * 1.8), DECK, r(CARR[2] + 0.08 * 1.8)]
FRIDGE = [1.6, 0, -2.4]; FRY = -20
CUPR = [-0.13, 0.98, -1.52]                                # his right hand (his right is -X: he faces +Z) holding the cup in front of his chest (seated)
SIP = {'touch': {'R': ['face', -0.06, 0.22, 0.1, 1, 0.03]}, 'hands': {'R': 'grip'}}

def sit_keys(face=DEAD, extra=None, look='camera'):
    t_ = {'reach': {'R': [*CUPR, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': face}
    if extra: t_.update(extra)
    return [k(0.0, look=look), k(0.0, toon=t_, toonDur=0.0)]
def MECSIT(keys, pos=MAN, ry=0, **kw): return act('mec', pos, ry, 'sit', 'unimpressed', keys=keys, **kw)
def CUP(pid='tasse'): return P(pid, 'mug', on={'actor': 'mec', 'hand': 'R', 'rot': [1.5708, 0, 0], 'offset': [0, -0.12, -0.05]}, opts={'color': '#E8452C'})
def KITCHEN(sugar=True, lidOff=False, ruins=False, snow=False, extra=(), carrier=None, fridge=True, table=True, smoke=True, rsides=None):
    ps = [*([P('table', 'table', pos=TB, opts={'w': 1.2, 'd': 0.75, 'h': TH, 'color': '#C9935C', 'legs': '#8A5A34'}),
             P('chaise', 'chair', pos=CHAIR, opts={'color': '#C9935C'})] if table else []),
          P('evier', 'islandSink', pos=SINK, opts={'w': 1.5, 'd': 0.75, 'h': SINKH}),
          P('pa', 'carrier', pos=CARR, ry=CARRY, opts={'L': 1.8, 'snow': snow, **(carrier or {})}),
          *([P('frigo', 'fridge', pos=FRIDGE, ry=FRY)] if fridge else [])]
    if sugar: ps.append(P('sucrier', 'sugarBowl', pos=SB, opts={'lid': 'off' if lidOff else 'on', 'dust': ruins, 'snow': snow and not lidOff}))
    if ruins: ps.append(P('ruines', 'ruinFloor', pos=[0.0, 0, -1.9], opts={'w': 5.6, 'd': 3.2, 'smoke': smoke and not snow, 'snow': snow, **({'sides': rsides} if rsides else {})}))
    return ps + list(extra)
# (review 1) the street after the strike: blown-out facades in front of the intact ones on both sides, rubble along their feet, smoke rising
def RUINS(snow=False, vista=False, smoke=True, holes=3, rubble=1.0):
    g_ = [-8.0, 8.0] if vista else None
    sm = lambda v: v if smoke else []   # (review 2) no smoke column and no blast holes where they sat as black blots at the top of a frame (S14, S15)
    return [P('ruinesG', 'ruinsBackdrop', pos=[-9.85, 0, -12.0], ry=90, opts={'len': 64, 'h': 21, 'seed': 41, 'snow': snow, 'smoke': sm([[-6.0, 1.5]]), 'holes': holes, 'rubble': rubble}),
            P('ruinesD', 'ruinsBackdrop', pos=[9.85, 0, -12.0], ry=-90, opts={'len': 64, 'h': 21, 'seed': 57, 'snow': snow, 'smoke': sm([[8.0, 1.5]]), 'holes': holes, 'rubble': rubble}),
            P('ruinesF', 'ruinsBackdrop', pos=[0.0, 0, -15.0], opts={'len': 20, 'h': 14, 'seed': 63, 'snow': snow, 'gap': g_ or [-2.0, 2.0], 'smoke': sm([[0.0, 1.0]]), 'holes': holes, 'rubble': rubble})]
# (review 2) the sink's stainless rim round the carrier: without it the hull sat on a counter top, not in a sink
SINKRIM = lambda pid, snow=False: P(pid, 'sinkRim', pos=[-1.9, SINKH, -2.5], opts={'w': 1.3, 'd': 0.5, 'snow': snow})
FLY = lambda pid, pos, ry=0, s=0.7, keys=None, **o: P(pid, 'houseFly', pos=pos, ry=ry, scale=s, opts=o, **({'keys': keys} if keys else {}))
HELMET = lambda pid, who, **o: P(pid, 'armyHelmet', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.46, 0.0]}, opts={'s': 0.95, **o})
KEPI = lambda pid, who, **o: P(pid, 'kepi', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'w': 0.222, 'd': 0.17, **o})
CROUCH = {'bend': {'spine': [0.35, 0, 0, 1, None], 'legL': [-0.9, 0, 0, 1, None], 'shinL': [1.6, 0, 0, 1, None], 'legR': [-0.9, 0, 0, 1, None], 'shinR': [1.6, 0, 0, 1, None]}, 'sq': [1.04, 0.9, 1.04]}

for g_ in [('S02', 0.4, 'mec', 'duck'), ('S03', 0.89, 'mec', 'slap'), ('S09', 0.3, 'mec', 'swoop'), ('S20', 1.0, 'gen3', 'tip')]:
    st.gag(*g_)
st.card('S19', 'SIGNÉ', at=0.95)
st.card('S21', 'DÉCORÉE', at=0.5)

# 1: the hook. Low at table height, the sugar bowl centred in the foreground; the small dark insect buzzes round it and lands on its rim; behind,
#    at his breakfast table, he jabs his index finger down at it again and again, deadpan, his cup in the other hand, then holds the finger on it;
#    at the left, further back and clear of his jabbing hand, a policeman writes on his clipboard and nods
D1 = st.dur('S01'); LAND1 = 1.45
FL1 = [k(0.0, to=[-0.12, 0.98, -0.88], dur=0.45, ease='inOut'), k(0.45, to=[0.1, 0.93, -0.9], dur=0.45, ease='inOut'), k(0.9, to=[0.03, 0.9, -0.88], dur=0.3, ease='inOut'),
       k(1.2, to=RIM, dur=0.25, ease='out')]
JAB = lambda t_, p_: k(t_, toon={'reach': {'R': [*CUPR, 1, 0.03], 'L': [*p_, 1, 0.06]}, 'hands': {'R': 'grip', 'L': 'point'}, 'scl': {'handL': [1.5, 1.5, 1.5]}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.1, toonEase='out')
st.shot('S01', 'kitchenDay', setOpts=KIT, actors=[
        # (review 2) every jab comes down at the bowl (the wind-up stays low over the table, clear of the policeman behind)
        MECSIT([*sit_keys(look=[0.0, 0.9, -0.95]), JAB(0.3, [0.12, 1.1, -1.28]), JAB(0.5, [0.05, 0.95, -1.0]), JAB(0.7, [0.12, 1.1, -1.28]), JAB(0.9, [0.05, 0.95, -1.0]),
                JAB(1.1, [0.12, 1.1, -1.28]), JAB(1.55, [0.04, 0.94, -0.99]), k(1.75, look='camera', lookDur=0.2)]),
        act('flic', [-0.7, 0, -3.0], 25, 'writeOnHeld', 'unimpressed', keys=[k(0.0, look=[0.0, 1.0, -1.1]), k(0.9, look=[0.2, 1.1, -1.25]), k(1.5, look=[0.0, 0.9, -0.95])])],
        props=[*KITCHEN(), CUP(), P('bloc', 'clipboardProp', on={'actor': 'flic', 'hand': 'L'}),
               FLY('mouche1', [0.08, 1.05, -0.85], ry=0, s=0.85, keys=FL1, buzz=[[0.0, LAND1]], rub=[[1.7, D1]])],
        cams=[cam(0.0, [0.0, 1.0, 0.2], [0.0, 1.0, 0.08], [0.0, 1.12, -1.4], [0.0, 1.12, -1.4], lens=56)])
st.cue('sfx:static', 'S01', 0.0, 0.05); st.cue('sfx:paper', 'S01', 0.5, 0.12)

# 2: the police charged. Wide from the front left: three riot police shoot through the kitchen door behind clear shields, stretched long and
#    smeared by their speed (the right of the room empty at first: they burst in from off the frame in a third of a second), and slam to a stop by the
#    table, squashing flat and springing back up; the plates leap off the shelf over the window;
#    he ducks over his cup; the insect hovers over the sugar bowl, untouched
D2 = st.dur('S02'); BURST2 = 0.45
# (review 2) they start off the frame at the right (the right half of the room empty for 0.1 s) and burst in, stretched and smeared, in a third of a second
CRS2 = [([5.0, 0, -3.4], [1.15, 0, -1.65], 0.1), ([5.3, 0, -3.1], [1.55, 0, -1.05], 0.15), ([4.8, 0, -3.0], [0.95, 0, -2.35], 0.2)]
STOP2 = 0.5    # (review 1) they arrive fast and stop dead: the run eases out over its first part only, then a squash on the stop and a rebound
def crs(j, a, b, d_):
    ry_ = r(math.degrees(math.atan2(b[0] - a[0], b[2] - a[2])))
    hold = lambda p_, sq_, t_, dur_, ease_='linear': k(t_, toon={'reach': {'L': [*loc(p_, ry_, [0.12, 1.15 * sq_[1], 0.38]), 1, 0.03], 'R': [*loc(p_, ry_, [-0.1, 1.1 * sq_[1], 0.35]), 1, 0.03]},
                                                          'hands': {'L': 'grip', 'R': 'grip'}, 'sq': list(sq_), 'face': {'lid': 0.0, 'mouth': 'clench', 'brow': -0.6}}, toonDur=dur_, toonEase=ease_)
    ta = r(STOP2 + 0.03 * j)
    return act(f'crs{j + 1}', a, ry_, 'stand', 'determined', keys=[k(d_, to=b, dur=r(ta - d_), clip='run', ease='linear'),
        hold(a, (1.0, 1.0, 1.0), 0.0, 0.0), hold(a, (0.8, 1.02, 1.6), r(d_ + 0.02), 0.06, 'out'),
        hold(b, (0.9, 1.0, 1.25), r(ta - 0.06), r(ta - d_ - 0.14)), hold(b, (1.3, 0.74, 0.7), ta, 0.04, 'out'),
        hold(b, (0.92, 1.1, 1.0), r(ta + 0.12), 0.08), hold(b, (1.0, 1.0, 1.0), r(ta + 0.24), 0.08)])
def shield(j, a, b, d_):
    ry_ = r(math.degrees(math.atan2(b[0] - a[0], b[2] - a[2])))
    return P(f'bouclier2{j}', 'riotShield', pos=loc(a, ry_, [0.0, 1.0, 0.42]), ry=ry_, keys=[k(d_, to=loc(b, ry_, [0.0, 1.0, 0.42]), dur=r(STOP2 + 0.03 * j - d_), ease='linear')])
st.shot('S02', 'kitchenDay', setOpts=KIT, blur=[[0.08, 0.5, 0.02]], blurSamples=3, actors=[
        MECSIT([*sit_keys(), k(0.32, toon={'reach': {'R': [0.13, 0.88, -1.45], 'L': [-0.05, 1.35, -1.6]}, 'hands': {'R': 'grip', 'L': 'open'},
                                           'bend': {'spine': [0.55, 0, 0, 1, None], 'neck': [0.3, 0, 0, 1, None]}, 'sq': [1.06, 0.88, 1.06], 'face': {'lid': 0.6, 'mouth': 'line'}}, toonDur=0.12, toonEase='out')]),
        *[crs(j, a, b, d_) for j, (a, b, d_) in enumerate(CRS2)]],
        props=[*KITCHEN(fridge=False), CUP(), *[shield(j, a, b, d_) for j, (a, b, d_) in enumerate(CRS2)],
               *[P(f'casque2{j}', 'riotHelmet', on={'actor': f'crs{j + 1}', 'joint': 'head', 'offset': [0.0, 0.46, 0.0]}, opts={'s': 0.95}) for j in range(3)],
               P('assiettes', 'plateShelf', pos=[0.2, 1.85, -3.58], opts={'w': 1.0, 'n': 5, 'burst': BURST2, 'floor': 1.85}),
               FLY('mouche2', [0.0, 1.0, -0.95], ry=20, s=0.7, buzz=[[0.0, D2]], bob=0.02)],
        fx=[{'type': 'shake', 'at': 0.48, 'dur': 0.2, 'amount': 0.015}],
        cams=[cam(0.0, [-1.45, 1.6, 2.3], [-1.4, 1.58, 2.15], [1.35, 1.15, -2.5], [1.35, 1.15, -2.5], lens=52)])
st.cue('sfx:crunch', 'S02', 0.48, 0.5); st.cue('sfx:stepRun', 'S02', 0.1, 0.3); st.cue('sfx:glass', 'S02', BURST2 + 0.3, 0.4); st.cue('sfx:siren', 'S02', 0.0, 0.12)

# 3: he demanded an air strike. Two-shot, closer: he reaches over and slaps a stamped request (a big plane pictogram, URGENT in red) onto the
#    clipboard of the policeman, who now wears a dented riot dome helmet with a neck guard (no cap) and, on the slap, squashes down into it, eyes
#    popping, then springs back up a little taller and settles; his hand lands on the request's edge, the plane and URGENT in view; the camera
#    pushes in until the request fills a quarter of the width
D3 = st.dur('S03'); SLAP3 = 0.89
FLIC3 = [0.6, 0, -1.75]; BOARD3 = [0.36, 1.2, -1.55]
st.shot('S03', 'kitchenDay', setOpts=KIT, actors=[
        MECSIT([*sit_keys(look=[0.45, 1.5, -1.3]),
                # (review 2) his hand holds the request by its left edge and lands on that edge: the plane and URGENT stay in view
                k(0.25, toon={'reach': {'R': [*CUPR, 1, 0.03], 'L': [0.1, 1.44, -1.58, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'open'}, 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.4}}, toonDur=0.3, toonEase='out'),
                k(r(SLAP3 - 0.06), toon={'reach': {'R': [*CUPR, 1, 0.03], 'L': [r(BOARD3[0] - 0.13), r(BOARD3[1] + 0.1), r(BOARD3[2] + 0.05), 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'open'}, 'sq': [1.04, 0.95, 1.04], 'face': {'lid': 0.3, 'mouth': 'line', 'brow': -0.5}}, toonDur=0.06, toonEase='in'),
                k(r(SLAP3 + 0.45), look='camera', lookDur=0.2)]),
        act('flic2', FLIC3, -45, 'stand', 'unimpressed', keys=[ k(0.0, toon={'reach': {'L': [BOARD3[0], r(BOARD3[1] - 0.05), r(BOARD3[2] - 0.02), 1, 0.03]}, 'hands': {'L': 'grip'}}, toonDur=0.0),
            k(SLAP3, toon={'sq': [1.2, 0.7, 1.2], 'scl': {'head': [1.12, 0.82, 1.12]}, 'face': {'lid': 0.0, 'pop': 0.55, 'eye': 0.5, 'mouth': 'O', 'brow': 0.9}}, toonDur=0.04, toonEase='out'),
            k(r(SLAP3 + 0.16), toon={'sq': [1.18, 0.72, 1.18], 'scl': {'head': [1.1, 0.84, 1.1]}, 'face': {'lid': 0.0, 'pop': 0.5, 'eye': 0.5, 'mouth': 'O', 'brow': 0.9}}, toonDur=0.1),
            k(r(SLAP3 + 0.3), toon={'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.1, 'eye': 0.3, 'mouth': 'o', 'brow': 0.6}}, toonDur=0.1, toonEase='out'),
            k(r(SLAP3 + 0.45), toon={'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.5, 'mouth': 'line'}}, toonDur=0.12)])],
        props=[*KITCHEN(), CUP(), P('bloc', 'clipboardProp', on={'actor': 'flic2', 'hand': 'L'}),
               P('casque3', 'riotHelmet', on={'actor': 'flic2', 'joint': 'head', 'offset': [0.0, 0.4, 0.0]}, opts={'s': 1.22, 'dent': True, 'guard': True}),
               P('demande', 'strikeForm', pos=[0.18, 1.3, -1.62], rot=[-0.3, 0, 0], opts={'w': 0.28, 'stamp': -1.0},
                 keys=[k(0.25, to=[0.22, 1.38, -1.6], dur=0.3, ease='out'), k(r(SLAP3 - 0.06), to=[BOARD3[0], r(BOARD3[1] + 0.03), r(BOARD3[2] + 0.03)], dur=0.06, ease='in')]),
               P('bouclier3a', 'riotShield', pos=[1.35, 0.03, -2.4], rot=[-1.5708, 0, 0.4], opts={'bent': 0.5}),
               P('bouclier3b', 'riotShield', pos=[1.0, 0.25, -2.75], rot=[-0.6, 0.3, 0.1], opts={'bent': 0.7}),
               P('etoiles3', 'impactStars', pos=[BOARD3[0], r(BOARD3[1] + 0.15), BOARD3[2]], opts={'at': SLAP3, 'n': 4})],
        fx=[{'type': 'shake', 'at': SLAP3, 'dur': 0.12, 'amount': 0.01}],
        cams=[cam(0.0, [0.3, 1.5, 1.05], [0.3, 1.5, 0.95], [0.32, 1.48, -1.7], [0.32, 1.48, -1.7], lens=48),
              glide([cam(r(SLAP3 + 0.1), [0.34, 1.52, 0.85], [0.34, 1.52, 0.8], [0.38, 1.56, -1.6], [0.38, 1.56, -1.6], lens=48)], 0.35)])   # (review 2) the rebound stays in the frame
st.cue('sfx:paper', 'S03', 0.3, 0.2); st.cue('sfx:punch', 'S03', SLAP3, 0.35); st.cue('sfx:squeak', 'S03', r(SLAP3 + 0.05), 0.2)

# 4: a satellite found the wasp. Space: the blue Earth fills the lower half; a satellite in the upper middle swivels its dish down toward it
#    and a green glint flashes in the dish
D4 = st.dur('S04'); GL4 = 1.25
st.shot('S04', 'spaceDark', actors=[],
        props=[P('terre4', 'earthGlobe', pos=[0.0, -9.0, -26.0], scale=7.0, opts={'spin': 0.06}),
               P('sat4', 'satellite', pos=[0.0, 1.55, -3.2], rot=[0.25, 0.4, 1.0], scale=0.32, keys=[k(0.25, rotTo=[0.25, 0.4, 0.0], dur=0.8, ease='inOut'), k(0.0, to=[0.25, 1.6, -3.2], dur=D4, ease='linear')]),
               P('eclat4', 'lensGlint', pos=[0.24, 1.22, -3.05], opts={'at': GL4, 'size': 1.3, 'dur': 0.5})],
        cams=[cam(0.0, [0.0, 1.0, 5.0], [0.1, 1.0, 4.8], [0.0, 0.3, -6.0], [0.06, 0.3, -6.0], lens=40)])
st.cue('sfx:static', 'S04', 0.1, 0.12); st.cue('sfx:click', 'S04', 0.3, 0.12); st.cue('sfx:ding', 'S04', GL4, 0.25)

# 5: near the sugar bowl. Straight down from the satellite's point of view: the table, his box head and the policeman's cap; a green reticle closes on
#    the sugar bowl and a big red map pin drops onto it beside a small dark dot (the insect on the rim)
D5 = st.dur('S05'); PIN5 = 0.45
st.shot('S05', 'kitchenDay', setOpts=KIT, actors=[
        MECSIT([*sit_keys(look=[0.0, 0.9, -0.95])]),
        act('flic2', [0.78, 0, -1.4], -40, 'writeOnHeld', 'unimpressed', keys=[k(0.0, look=[0.0, 1.0, -1.1])])],
        props=[*KITCHEN(), CUP(), P('bloc', 'clipboardProp', on={'actor': 'flic2', 'hand': 'L'}),
               P('casque5', 'riotHelmet', on={'actor': 'flic2', 'joint': 'head', 'offset': [0.0, 0.4, 0.0]}, opts={'s': 1.22, 'dent': True, 'guard': True}),
               FLY('mouche5', RIM, ry=0, s=0.7, rub=[[0.0, D5]]),
               P('cible5', 'satReticle', pos=[0.0, r(TH + 0.002), -0.95], opts={'r': 0.22, 'at': 0.05}),
               P('punaise5', 'mapPin', pos=[0.06, r(LIDTOP + 0.012), -0.95], opts={'s': 1.6, 'at': PIN5, 'drop': 1.0})],
        cams=[cam(0.0, [0.0, 2.32, -1.1], [0.0, 2.26, -1.1], [0.0, TH, -1.16], [0.0, TH, -1.16], lens=64)])
st.cue('sfx:beep', 'S05', 0.05, 0.15); st.cue('sfx:pop', 'S05', PIN5, 0.35); st.cue('thud', 'S05', PIN5, 0.15)

# 6: an aircraft carrier put to sea. Low over the waves, bow-on: the grey carrier charges straight at us through white spray, a big bow wave
#    curling off each side and a white wake trailing back to the horizon, its horn blasting; it grows fast and fills the frame by the cut, the camera
#    rocking on the swell
D6 = st.dur('S06')
st.shot('S06', 'seaSurface', setOpts={'parasols': False, 'shore': 40}, actors=[],
        # (review 2) it starts much closer and fills the frame by the cut; the camera drops low over the waves, tilted on the swell
        props=[P('pa6', 'carrier', pos=[-1.6, 0.0, -78.0], ry=8, scale=16.0, opts={'L': 1.8, 'wake': True, 'waterline': False, 'spray': True}, keys=[k(0.0, to=[-0.6, 0.0, -25.0], dur=D6, ease='linear')])],
        cams=[cam(0.0, [0.0, 6.5, 0.0], [0.0, 6.0, -1.0], [-1.2, 4.0, -60.0], [-0.8, 4.4, -30.0], lens=34, roll=-2.5)])
st.cue('sfx:honkLong', 'S06', 0.3, 0.45); st.cue('sfx:splash', 'S06', 0.1, 0.2); st.cue('whoosh', 'S06', 0.6, 0.2)

# 7: in the sink. One image, three-quarters from above the counter: the big chrome tap and the basin's rim, the grey carrier wedged in the sink
#    from end to end, its bow jutting over the counter's edge toward him, a bright white-blue sheet of water falling off the end onto the tiles in
#    the middle of the frame, a bright stainless rim round the basin; at the right, at his table, his eyes go to the water, then to us, deadpan
D7 = st.dur('S07')
TAP = [-2.25, SINKH, -2.81]   # (review 1) a big gooseneck tap behind the basin, clear of the carrier's island: it says « kitchen sink » at a glance
CAM7 = cam(0.0, [0.9, 2.8, 0.0], [0.86, 2.78, -0.06], [-0.95, 0.55, -2.25], [-0.95, 0.55, -2.25], lens=52)
# (review 2) his eyes open, go to the water pouring off the bow, then come back to us (they stayed shut for the whole second)
st.shot('S07', 'kitchenDay', setOpts=KIT, actors=[MECSIT([*sit_keys(look=[-0.9, 0.5, -2.45], face={'lid': 0.15, 'mouth': 'line'}), k(0.5, look='camera', lookDur=0.1),
                                                         k(0.5, toon={'reach': {'R': [*CUPR, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.1),
                                                         k(0.8, toon={'reach': {'R': [*CUPR, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.05),
                                                         k(0.88, toon={'reach': {'R': [*CUPR, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.07)])],
        props=[*KITCHEN(), CUP(), SINKRIM('rebord7'), P('robinet7', 'kitchenTap', pos=TAP, opts={'h': 0.42}),
               P('flot7', 'waterSpill', pos=[-1.15, SINKH, -2.5], ry=90, opts={'w': 0.62, 'h': SINKH, 'at': 0.0, 'r0': 0.55, 'r': 1.0, 'grow': 1.0, 'bright': True})],
        cams=[CAM7])
st.cue('sfx:pour', 'S07', 0.0, 0.3); st.cue('sfx:splash', 'S07', 0.2, 0.2)

# 8: a fighter... Low behind the stern of the carrier wedged in the sink: the chrome tap at the left, the counter on both sides of the hull, the
#    fighter on its catapult on the deck (its burner glowing at us, steam puffing from the track); beyond the bow, across the kitchen, he sits at his
#    table and turns his head to it
D8 = st.dur('S08')
JET = lambda pid, pos, keys=None, **o: P(pid, 'fighterJet', pos=pos, ry=90, scale=0.022, opts={'burner': o.pop('burner', 0.6), 'glow': 0.5, **o}, **({'keys': keys} if keys else {}))
JY = r(DECK + 0.045)
st.shot('S08', 'kitchenDay', setOpts=KIT, actors=[MECSIT([*sit_keys(look=[-1.8, 1.3, -1.2])])],
        props=[*KITCHEN(), CUP(), SINKRIM('rebord8'), P('robinet8', 'kitchenTap', pos=TAP, opts={'h': 0.42}), P('flot8', 'waterSpill', pos=[-1.15, SINKH, -2.5], ry=90, opts={'w': 0.62, 'h': SINKH, 'r0': 1.0, 'r': 1.0, 'bright': True}),
               JET('jet8', [r(CAT0[0] + 0.22), JY, CAT0[2]], keys=[k(r(D8 - 0.12), to=[r(CAT0[0] + 0.32), JY, CAT0[2]], dur=0.12, ease='in')], burner=0.8),
               *[P(f'vap8{j}', 'toonPuff', pos=[r(CAT0[0] + 0.36 + 0.12 * j), r(DECK + 0.01), CAT0[2]], opts={'at': r(0.1 + 0.15 * j), 'n': 4, 'size': 0.02, 'rise': 0.07, 'spread': 0.04, 'life': 0.7}) for j in range(4)]],
        cams=[cam(0.0, [-3.2, 1.5, -2.72], [-3.15, 1.49, -2.7], [-0.5, 1.0, -2.2], [-0.5, 1.0, -2.2], lens=58)])
st.cue('sfx:jet', 'S08', 0.0, 0.2); st.cue('sfx:static', 'S08', 0.1, 0.1)

# 9: ...took off from the sink. Front on him at his table: the fighter shoots off the bow in the sink at the back left (the chrome tap beside it) and swoops past his head toward us and out
#    of the frame at the right; his hair blows flat and his tie flies; he does not blink; then one slow blink at us
D9 = st.dur('S09'); PASS9 = 0.3
st.shot('S09', 'kitchenDay', setOpts=KIT, actors=[
        MECSIT([*sit_keys(), k(r(PASS9 - 0.02), toon={'reach': {'R': [*CUPR, 1, 0.03]}, 'hands': {'R': 'grip'}, 'hairUp': 1.0, 'tie': [1.2, 0.2, 0.9], 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 0.0, 'eye': 0.2, 'mouth': 'line'}}, toonDur=0.04, toonEase='out'),
                k(r(PASS9 + 0.3), toon={'reach': {'R': [*CUPR, 1, 0.03]}, 'hands': {'R': 'grip'}, 'hairUp': 0.6, 'face': DEAD}, toonDur=0.25),
                k(0.85, toon={'reach': {'R': [*CUPR, 1, 0.03]}, 'hands': {'R': 'grip'}, 'hairUp': 0.5, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.08, keepPose=True)])],
        props=[*KITCHEN(), CUP(), SINKRIM('rebord9'), P('robinet9', 'kitchenTap', pos=TAP, opts={'h': 0.42}), P('flot9', 'waterSpill', pos=[-1.15, SINKH, -2.5], ry=90, opts={'w': 0.62, 'h': SINKH, 'r0': 1.0, 'r': 1.0, 'bright': True}),
               P('jet9', 'fighterJet', pos=[r(CAT1[0] - 0.2), JY, CAT1[2]], ry=90, scale=0.03, opts={'burner': 1.0, 'glow': 0.6, 'contrail': False},
                 keys=[k(0.0, to=[CAT1[0], r(JY + 0.05), CAT1[2]], dur=0.08, ease='in'), k(0.08, to=[0.22, 1.33, -1.35], dur=0.2, ease='linear'), k(0.28, to=[1.7, 1.2, 0.3], dur=0.25, ease='linear'),
                       k(0.0, rotTo=[0.0, 1.5708, 0.0], dur=0.0), k(0.08, rotTo=[0.15, 1.0, -0.6], dur=0.2), k(0.28, rotTo=[0.1, 0.8, -0.9], dur=0.2)])],
        fx=[{'type': 'shake', 'at': PASS9, 'dur': 0.2, 'amount': 0.012}],
        cams=[cam(0.0, [0.55, 1.3, 0.75], [0.53, 1.3, 0.65], [0.0, 1.15, -1.8], [0.0, 1.15, -1.8], lens=46)])
st.cue('sfx:jet', 'S09', 0.0, 0.5); st.cue('whoosh', 'S09', PASS9, 0.45)

# 10: it missed the wasp. Slow motion, low behind the sugar bowl: the insect hovers calmly over the bowl in the middle of the frame; two big
#     missiles, crisp bodies with fins and flames, come in slowly from just behind us at the bottom corners, pass a hand's width either side of it,
#     then either side of his head, and punch two scorched holes in the back wall on either side of his head; his hair stirs; one slow blink
D10 = st.dur('S10'); HIT10 = 0.95
# (review 2) curved paths (they used to run straight from behind the lens: end-on, a white smear across his chest, the holes out of the frame):
# each passes 17 cm beside the insect, then beside his ears, and lands on the wall where the holes show on either side of his head; short thin trails
# slow past the insect and his head (v0: they ease in from the lens, then speed up to the wall), dark bodies that read on the pale kitchen
SH10 = [{'from': [-0.3, 0.9, 0.0], 'ctrl': [0.093, 1.304, -1.138], 'to': [-0.7, 1.85, -3.53], 't0': 0.0, 'dur': HIT10, 'v0': 0.3},
        {'from': [0.3, 0.9, 0.0], 'ctrl': [-0.093, 1.304, -1.138], 'to': [0.7, 1.85, -3.53], 't0': 0.08, 'dur': HIT10, 'v0': 0.3}]
HOLE10 = [(-0.7, 1.85), (0.7, 1.85)]
st.shot('S10', 'kitchenDay', setOpts=KIT, actors=[MECSIT([*sit_keys(), k(r(HIT10 + 0.04), toon={'reach': {'R': [*CUPR, 1, 0.03]}, 'hands': {'R': 'grip'}, 'hairUp': 0.55, 'face': DEAD}, toonDur=0.06, toonEase='out'),
                                                          k(r(HIT10 + 0.16), toon={'reach': {'R': [*CUPR, 1, 0.03]}, 'hands': {'R': 'grip'}, 'hairUp': 0.25, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.12),
                                                          k(r(HIT10 + 0.3), toon={'reach': {'R': [*CUPR, 1, 0.03]}, 'hands': {'R': 'grip'}, 'hairUp': 0.2, 'face': DEAD}, toonDur=0.12, keepPose=True)])],
        props=[*KITCHEN(), CUP(), FLY('mouche10', [0.0, 1.2, -0.95], ry=0, s=1.0, buzz=[[0.0, D10]], bob=0.008),
               P('missiles10', 'missileSalvo', pos=[0, 0, 0], opts={'shots': SH10, 'size': 0.12, 'trail': 0.12, 'trailWidth': 0.07, 'trailOpacity': 0.45, 'flame': 1.3, 'glow': 0.9, 'core': '#FFF0B8', 'bodyColor': '#4E555D'}),
               P('trou10a', 'wallImpact', pos=[HOLE10[0][0], HOLE10[0][1], -3.53], opts={'at': HIT10, 'r': 0.3, 'seed': 3}), P('trou10b', 'wallImpact', pos=[HOLE10[1][0], HOLE10[1][1], -3.53], opts={'at': r(HIT10 + 0.08), 'r': 0.3, 'seed': 8}),
               *[P(f'boum10{j}', 'toonPuff', pos=[x_, y_, -3.4], opts={'at': r(HIT10 + 0.08 * j), 'n': 6, 'size': 0.12, 'rise': 0.3, 'spread': 0.25, 'life': 0.5, 'color': '#E8E2D6'}) for j, (x_, y_) in enumerate(HOLE10)]],
        fx=[{'type': 'shake', 'at': HIT10, 'dur': 0.2, 'amount': 0.012}],
        cams=[cam(0.0, [0.04, 1.15, 0.45], [0.04, 1.15, 0.41], [0.0, 1.35, -2.0], [0.0, 1.35, -2.0], lens=52)])
st.cue('whoosh', 'S10', 0.1, 0.3); st.cue('thunder', 'S10', HIT10, 0.45); st.cue('sfx:crunch', 'S10', HIT10, 0.4)

# 11: it razed the building. The street, wide, from above: where his building stood, a heap of rubble with the bare kitchen floor (peach and cream
#     tiles) on top; on it, in his chair, he sits with his cup; the fridge and the sink with the carrier stick out of the heap; dust rolls off it; the
#     last piece of wall topples
D11 = st.dur('S11'); HP = [0.0, 0, -18.0]; HH = 2.2
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [0.15, HH, -17.9], 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [0.02, r(HH + 0.98), -17.62, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.0), k(0.75, toon={'reach': {'R': [0.28, r(HH + 0.98), -17.62, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 0.9, 'mouth': 'line'}}, toonDur=0.08)])],
        props=[P('tas', 'rubbleHeap', pos=HP, opts={'r': 3.4, 'h': HH, 'wall': [0.3], 'dust': True}),
               P('chaise11', 'chair', pos=[0.15, r(HH - 0.02), -18.05], opts={'color': '#C9935C'}),
               P('tasse11', 'mug', on={'actor': 'mec', 'hand': 'R', 'rot': [1.5708, 0, 0], 'offset': [0, -0.12, -0.05]}, opts={'color': '#E8452C'}),
               P('frigo11', 'fridge', pos=[1.7, 1.2, -17.6], rot=[0.25, -0.5, 0.35]),
               P('evier11', 'islandSink', pos=[-1.9, 1.05, -17.7], rot=[-0.2, 0.3, -0.3], opts={'w': 1.5, 'd': 0.75, 'h': SINKH}),
               P('pa11', 'carrier', pos=[-1.75, 1.92, -17.6], rot=[-0.2, 1.87, -0.3], opts={'L': 1.8})],
        fx=[{'type': 'shake', 'at': 0.55, 'dur': 0.2, 'amount': 0.012}],
        cams=[cam(0.0, [2.4, 4.6, -10.6], [2.3, 4.5, -10.9], [0.0, 2.0, -18.0], [0.0, 2.0, -18.0], lens=44)])
st.cue('sfx:wind', 'S11', 0.0, 0.2); st.cue('thud', 'S11', 0.55, 0.35); st.cue('sfx:crunch', 'S11', 0.55, 0.3)

# 12: and the town hall, as a precaution. Down the street: the town hall pancakes to a heap in a burst of thick, soft cartoon dust; its big MAIRIE
#     board drops with it and lands tilted on the front of the heap, still readable; the flagpole in front stays standing while its flag slides down
#     and flops onto the rubble
D12 = st.dur('S12'); COL12 = 0.4
st.shot('S12', 'parisStreet', setOpts=STREET, actors=[],
        props=[P('mairie12', 'collapse', pos=[0.0, 0, -36.0], opts={'of': 'townHall', 'opts': {'w': 8.0, 'h': 5.5, 'd': 4.5, 'gable': 'v2'}, 'at': COL12, 'dur': 0.4, 'flat': 0.12, 'pole': True, 'poleAt': [-2.6, 5.0], 'poleH': 6.0,
                                                                        'noPuffs': True, 'sign': 'MAIRIE', 'signW': 3.4}),
               *[P(f'poussiere12{j}', 'toonPuff', pos=[x_, 0.4, z_], opts={'at': r(COL12 + 0.12 + 0.05 * j), 'n': 7, 'size': 0.9, 'rise': 2.2, 'spread': 2.6, 'life': 1.15, 'flatZ': 0.6, 'color': '#E6DCC8'})
                 for j, (x_, z_) in enumerate([(-3.0, -34.0), (0.0, -33.6), (3.0, -34.0), (-1.5, -36.5), (1.8, -36.5)])]],
        fx=[{'type': 'shake', 'at': r(COL12 + 0.3), 'dur': 0.3, 'amount': 0.02}],
        cams=[cam(0.0, [2.0, 1.5, -19.5], [1.9, 1.5, -20.0], [-0.6, 3.2, -36.0], [-0.6, 3.0, -36.0], lens=48)])
st.cue('thunder', 'S12', r(COL12 + 0.3), 0.5); st.cue('sfx:crunch', 'S12', r(COL12 + 0.2), 0.4)

# 13: the wasp finished its sugar. On the open sugar bowl on the dusty table in the ruins (blown-out facades and smoke rising behind): behind
#     it, his cup lowered to the table, he watches it, deadpan; the camera pushes in to the rim until the insect fills a third of the width and it
#     dives into the sugar cubes three times, each a rear-back, a big lunge head first that squashes it on the cubes, a rock back, crumbs flying
D13 = st.dur('S13')
CUP13 = [-0.2, 0.86, -1.48]   # (review 1) his cup lowered to the table: it hid his face
DIPS13 = [0.5, 0.93, 1.36]    # (review 2) after the push-in; each dive rears back 0.1 s before it
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[MECSIT([k(0.0, look=[0.0, 0.9, -0.95]), k(0.0, toon={'reach': {'R': [*CUP13, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.0)])],
        props=[*KITCHEN(lidOff=True, ruins=True), CUP(), *RUINS(), FLY('mouche13', [-0.072, RIM[1], -0.95], ry=90, s=0.8, dips=DIPS13)],
        cams=[cam(0.0, [0.45, 1.15, 0.3], [0.43, 1.15, 0.24], [-2.529, 0.425, -9.218], [-2.529, 0.425, -9.218], lens=52),
              glide([cam(0.05, [0.3, 1.02, -0.45], [0.3, 1.02, -0.47], [-0.06, 0.87, -0.97], [-0.06, 0.87, -0.97], lens=40)], 0.35)])
st.cue('sfx:wind', 'S13', 0.0, 0.15); [st.cue('sfx:crunch', 'S13', r(t_ + 0.12), 0.12) for t_ in DIPS13]

# the front, in the ruins: sandbags along x -1.0 in front of the sink and the carrier, soldiers crouched behind them; sandbags along x 1.15 in front
# of the fridge, the insect's black flag on top of the fridge; him at his table in the middle, in no man's land
SOLDP = [(-1.05, -1.6), (-1.12, -2.0), (-1.0, -2.4)]   # (stills 4) all behind his line from the S14 camera: one at z -1.2 hid him
SINKY = -0.42   # (stills 2) the toon leg bends do not lower the pelvis: crouched behind the sandbags means sunk into the floor (the tiles hide the legs)
def soldier(j, x_, z_, keys=(), clip='stand', look=None, toon0=None):
    return act(f'sold{j + 1}', [x_, SINKY, z_], 90, clip, 'determined', keys=[k(0.0, look=look or [1.6, 1.15, z_]), k(0.0, toon=toon0 or {**CROUCH}, toonDur=0.0), *keys])
# (review 2) dark flat-topped burlap sandbags tied at both ends (the pale round ones read as loaves), a thin layer of snow on the top course in winter
FRONT = lambda snow=False: [P('sacs1', 'burlapBags', pos=[-0.7, 0, -1.7], ry=90, opts={'n': 6, 'rows': 3, 'seed': 4, 'snow': snow}),
                            P('sacs2', 'burlapBags', pos=[1.0, 0, -2.1], ry=-90, opts={'n': 5, 'rows': 3, 'seed': 7, 'snow': snow}),
                            P('drapeau', 'pennantFlag', pos=[1.45, 1.9, -2.3], scale=3.0)]
SOLD = {'outfit': 'suit', 'suit': '#5B6638', 'pants': '#4E5730', 'shirt': '#D9D3B6', 'lapel': '#4E5730', 'tie': '#3B4224', 'cuff': '#5B6638', 'hat': 'none', 'gloves': '#2E3320', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2},
        'toon': {'holdLife': 1.2, 'shift': 0.8, 'breathe': 1.4}}   # (review 1) dark gloves: the white sugar cubes read on them; calmer idle (no head tips)

# 14: the front froze... Low behind the carrier wedged in the sink and the soldiers' helmets behind their sandbags: in the gap between two helmets,
#     alone at his table in no man's land, he sips his cup; behind him, clear, the sandbagged fridge with the insect's black flag on top; one soldier's
#     helmet pops up on a long stretched neck, hangs there a beat, then snaps down and squashes into the trench; olive helmets cover the backs of
#     the soldiers' heads; no blot or smoke above
D14 = st.dur('S14')
SOLD14 = [(-1.05, -1.45), (-1.08, -2.4), (-1.0, -0.9)]   # (review 1) the two near ones frame him at the edges of the frame; the third is off to the side
POP14 = [0.25, 0.42, 0.78, 0.9]   # up, at the top, hang until, back down
RY14 = -55; CUP14 = loc(MAN, RY14, [-0.13, 0.98, 0.28])   # (review 1) turned on his chair toward the trench: seen from behind the soldiers his face reads
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[
        MECSIT([k(0.0, look=[-3.0, 1.45, -2.3]), k(0.0, toon={'reach': {'R': [*CUP14, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.0),
                k(0.5, toon={**SIP, 'face': DEAD}, toonDur=0.2), k(0.95, toon={'reach': {'R': [*CUP14, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.2)], ry=RY14),
        soldier(0, *SOLD14[0], look=[1.6, 1.2, SOLD14[0][1]], keys=[
            k(POP14[0], to=[SOLD14[0][0], -0.12, SOLD14[0][1]], dur=0.12, ease='out', glide=True, face='keep'), k(POP14[2], to=[SOLD14[0][0], -0.5, SOLD14[0][1]], dur=0.08, ease='in', glide=True, face='keep'),
            k(POP14[3], to=[SOLD14[0][0], SINKY, SOLD14[0][1]], dur=0.1, ease='out', glide=True, face='keep'),
            k(POP14[0], toon={**CROUCH, 'bend': {**CROUCH['bend'], 'neck': [0.0, 0, 0, 5.0, 0.7]}, 'sq': [0.92, 1.12, 0.92], 'face': {'lid': 0.0, 'eye': 0.35, 'mouth': 'line'}}, toonDur=0.12, toonEase='out'),
            k(POP14[1], toon={**CROUCH, 'bend': {**CROUCH['bend'], 'neck': [0.0, 0, 0, 4.6, 0.7]}, 'face': {'lid': 0.0, 'eye': 0.35, 'mouth': 'line'}}, toonDur=0.1),
            k(POP14[2], toon={**CROUCH, 'bend': {**CROUCH['bend'], 'neck': [0.0, 0, 0, 0.5, 1.4]}, 'sq': [1.2, 0.75, 1.2], 'face': {'lid': 0.5, 'mouth': 'line'}}, toonDur=0.07, toonEase='in'),
            k(POP14[3], toon={**CROUCH, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.1)]),
        soldier(1, *SOLD14[1], look=[1.6, 1.2, SOLD14[1][1]]), soldier(2, *SOLD14[2], look=[1.6, 1.2, SOLD14[2][1]])],
        # (review 2) aimed higher and a little wider: the popped head stays in the frame; no blast holes or smoke on the facades behind (a black
        # blot sat at the top right); the helmets now cover the backs of the heads
        props=[*KITCHEN(ruins=True, smoke=False), CUP(), *FRONT(), *RUINS(smoke=False, holes=0), *[HELMET(f'casque14{j}', f'sold{j + 1}') for j in range(3)], P('robinet14', 'kitchenTap', pos=TAP, opts={'h': 0.42}), SINKRIM('rebord14')],
        cams=[cam(0.0, [-5.0, 1.45, -1.95], [-4.92, 1.45, -1.96], [0.5, 1.72, -2.05], [0.5, 1.72, -2.05], lens=38)])
st.cue('sfx:wind', 'S14', 0.0, 0.2)

# 15: ...between the fridge and the sink. The reverse, from high behind the fridge: the insect in the lower left, three-quarters to us, on the
#     room-side edge of the fridge's top (a narrow strip at the bottom of the frame), its black flag planted beside it; its head turns to the man
#     first, then back, and it rubs its front legs hard four or five times; across the tiles, small but clear in the upper middle: the man at his
#     table looking up at it, the sandbag line with the soldiers' helmets, the carrier wedged in the sink at the right with its tap
D15 = st.dur('S15')
# (review 2) found by search over camera positions, with a test that nothing beyond is hidden by the fridge's own top and a score on how much of
# the frame the top fills (a camera just above it saw nothing but the top: the room lies below its edge); the heaps of rubble at the left of the
# kitchen ruins (in this sightline) are left out, the chunks along the facades made smaller
FLY15 = [1.22, 1.9, -2.379]; FLAG15 = [1.316, 1.9, -2.556]
st.shot('S15', 'parisStreet', setOpts=STREET, actors=[MECSIT([*sit_keys(look=[1.7, 1.95, -2.05])]), soldier(0, *SOLDP[0]), soldier(1, *SOLDP[1]), soldier(2, *SOLDP[2])],
        props=[*KITCHEN(ruins=True, rsides=[0, 2]), CUP(), *FRONT()[:2], P('drapeau15', 'pennantFlag', pos=FLAG15, ry=111, scale=2.6), *RUINS(smoke=False, holes=0, rubble=0.45), *[HELMET(f'casque15{j}', f'sold{j + 1}') for j in range(3)],
               P('robinet15', 'kitchenTap', pos=TAP, opts={'h': 0.42}), SINKRIM('rebord15'),
               FLY('mouche15', FLY15, ry=70, s=1.6, rub=[[0.4, D15]], rubAmp=2.3, rubHz=5.0, look=[[0.0, -0.75], [0.3, -0.75], [0.45, 0.2]])],
        cams=[cam(0.0, [2.3, 3.0, -2.8], [2.28, 2.98, -2.76], [-0.6, 1.15, -2.08], [-0.6, 1.15, -2.08], lens=58)])
st.cue('sfx:wind', 'S15', 0.0, 0.15)

# 16: all winter... The same front under falling snow, down the street to the far tower between blown-out facades: the soldiers vibrate with cold
#     behind their sandbags, their whole bodies squashing and stretching in a shiver (ghost copies), snow piling on their helmets; at his table in the
#     middle, snow piled on his head, he holds his cup, deadpan; an overcast winter light, grey-white sky, dark burlap sandbags under a thin snow
D16 = st.dur('S16')
def shiver(t0, t1, every=0.07, a=0.09):
    ks, t_, i = [], t0, 0
    while t_ < t1: ks.append(k(r(t_), toon={**CROUCH, 'buzz': 0.02, 'sq': [1.0 + a, 1.0 - a, 1.0 + a] if i % 2 == 0 else [1.0 - a * 0.6, 1.0 + a * 0.8, 1.0 - a * 0.6], 'face': {'lid': 0.3, 'mouth': 'clench', 'tremble': 1.0, 'brow': 0.6}}, toonDur=0.03)); t_ += every; i += 1
    return ks
st.shot('S16', 'parisStreet', setOpts=SNOW, **WINTER, blur=[[0.0, D16, 0.014]], blurSamples=3, actors=[
        MECSIT([*sit_keys()]), *[soldier(j, x_, z_, keys=shiver(0.02 * j, D16)) for j, (x_, z_) in enumerate(SOLDP)]],
        props=[*KITCHEN(ruins=True, snow=True), CUP(), *FRONT(snow=True), *RUINS(snow=True, vista=True), *[HELMET(f'casque16{j}', f'sold{j + 1}', snow=True) for j in range(3)],
               P('robinet16', 'kitchenTap', pos=TAP, opts={'h': 0.42, 'snow': True}), SINKRIM('rebord16', snow=True),
               P('neige16', 'snowCap', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.42, 0.0]}, opts={'w': 0.32, 'h': 0.2, 't0': 0.0, 't1': D16})],
        cams=[cam(0.0, [0.25, 1.35, 2.5], [0.24, 1.34, 2.38], [0.15, 1.0, -2.0], [0.15, 1.0, -2.0], lens=64)])
st.cue('sfx:wind', 'S16', 0.0, 0.35)

# 17: ...sugar was rationed. The line of soldiers from the front, crouched behind their sandbags, each holding out a dark glove: behind them an
#     officer in a kepi walks down the line and drops one white sugar cube into each glove in turn; as his cube lands, each soldier's eyes drop to it
D17 = st.dur('S17'); OFF17 = [-1.55, 0, -2.55]
GIVE17 = [0.3, 0.65, 1.0]
SL17 = [(-1.0, -2.1), (-1.08, -1.65), (-1.02, -1.2)]   # the line, from the back to the front; the officer walks it behind them (x -1.55)
HAND17 = lambda x_, z_: [r(x_ + 0.3), 0.8, r(z_ - 0.1)]   # a soldier's right glove held out in front of him over the sandbags (he faces +X: his right is -Z)
st.shot('S17', 'parisStreet', setOpts=SNOW, **WINTER, actors=[
        *[act(f'sold{j + 1}', [x_, SINKY, z_], 90, 'stand', 'sad', keys=[k(0.0, look=[1.0, 1.15, z_]),
            k(0.0, toon={**CROUCH, 'buzz': 0.006, 'reach': {'R': [*HAND17(x_, z_), 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': 0.6}}, toonDur=0.0),
            k(r(GIVE17[j] + 0.06), look=[r(x_ + 0.9), 0.9, z_], lookDur=0.12),
            k(r(GIVE17[j] + 0.06), toon={**CROUCH, 'buzz': 0.006, 'reach': {'R': [*HAND17(x_, z_), 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.2, 'gy': 0.9, 'mouth': 'line', 'brow': 0.8}}, toonDur=0.1)]) for j, (x_, z_) in enumerate(SL17)],
        act('officier', OFF17, 0, 'stand', 'determined', keys=[k(0.0, look=[-1.0, 0.9, -2.1]), k(0.0, to=[-1.55, 0, -0.95], dur=D17, clip='walk', ease='linear'),
            *[k(r(t_ - 0.12), look=[HAND17(*SL17[i])[0], 0.8, HAND17(*SL17[i])[2]], lookDur=0.1) for i, t_ in enumerate(GIVE17)],
            *[k(r(t_ - 0.12), toon={'reach': {'L': [*HAND17(*SL17[i])[:1], 0.9, HAND17(*SL17[i])[2], 1, 0.03]}, 'hands': {'L': 'pinch'}}, toonDur=0.12) for i, t_ in enumerate(GIVE17)],
            *[k(r(t_ + 0.08), toon={'hands': {'L': 'rest'}}, toonDur=0.12) for t_ in GIVE17]])],
        props=[*KITCHEN(ruins=True, snow=True, sugar=False, table=False), *FRONT(snow=True), *RUINS(snow=True), *[HELMET(f'casque17{j}', f'sold{j + 1}', snow=True) for j in range(3)],
               KEPI('kepi17', 'officier', color='#2B3A2A', band='#E2B53C'),
               *[P(f'morceau17{i}', 'sugarCube', pos=[HAND17(*SL17[i])[0], 0.85, HAND17(*SL17[i])[2]], scale=4.0, keys=[k(0.0, visible=False), k(t_, visible=True)]) for i, t_ in enumerate(GIVE17)]],
        cams=[cam(0.0, [1.75, 1.6, -0.55], [1.71, 1.6, -0.57], [-7.516, 0.55, -4.269], [-7.516, 0.55, -4.269], lens=54)])   # (review 2) aimed higher: the officer's kepi in the frame
for t_ in GIVE17: st.cue('sfx:pop', 'S17', t_, 0.15)
st.cue('sfx:wind', 'S17', 0.0, 0.3)

# 18: the State asked for a ceasefire. The snowy sink from the front, wide enough to hold him: the chrome tap at the left, the stainless rim round
#     the basin, the carrier wedged in it under soft drifts of snow, the burlap trench in front; a hatch halfway along the deck opens and a big white
#     handkerchief with a thin dark outline, two flaps rippling, rises slowly on its stick; at the right, snowed on at his table, his eyes go to it
D18 = st.dur('S18'); UP18 = 0.3
# (review 2) the hatch moved toward the bow (aft, it sat 2 m from him: no frame held both); a camera found by search that holds the tap, the rim,
# the flag and his face; snow drifts instead of flat slabs
HATCH18 = [r(CARR[0] + 0.25 * 1.8), DECK, r(CARR[2] + 0.08 * 1.8)]
st.shot('S18', 'parisStreet', setOpts=SNOW, **WINTER, actors=[MECSIT([*sit_keys(look=[HATCH18[0], 1.35, HATCH18[2]]), k(0.95, toon={'reach': {'R': [*CUPR, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.06),
                                                                     k(1.05, toon={'reach': {'R': [*CUPR, 1, 0.03]}, 'hands': {'R': 'grip'}, 'face': DEAD}, toonDur=0.08), k(1.6, look='camera', lookDur=0.3)])],
        props=[*KITCHEN(ruins=True, snow=True, sugar=False, carrier={'hatch': [[0.2, 1.0]], 'hatchAt': 0.25}, rsides=[2]), CUP(), *FRONT(snow=True), *RUINS(snow=True, rubble=0.5), SINKRIM('rebord18', snow=True),
               P('robinet18', 'kitchenTap', pos=TAP, opts={'h': 0.42, 'snow': True}),
               P('neige18', 'snowCap', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.42, 0.0]}, opts={'w': 0.32, 'h': 0.22, 't0': -2.0, 't1': -1.0}),
               P('blanc18', 'truceFlag', pos=[HATCH18[0], r(DECK - 0.42), HATCH18[2]], opts={'w': 0.36, 'h': 0.24, 'pole': 0.42, 'speed': 6},
                 keys=[k(UP18, to=[HATCH18[0], r(DECK - 0.01), HATCH18[2]], dur=1.3, ease='out')])],
        cams=[cam(0.0, [-0.25, 2.1, 1.7], [-0.27, 2.08, 1.6], [-0.72, 1.2, -1.9], [-0.72, 1.2, -1.9], lens=56),
              glide([cam(0.9, [-0.55, 1.95, 0.75], [-0.58, 1.93, 0.65], [-1.05, 1.3, -2.2], [-1.05, 1.3, -2.2], lens=52)], 1.1)])   # (review 2) a slow push toward the rising flag
st.cue('sfx:squeak', 'S18', 0.25, 0.25); st.cue('sfx:wind', 'S18', 0.0, 0.25)

# 19: the wasp got the sugar bowl. Close on the sugar bowl from the front left, the white fridge behind it: in front, the treaty, lines of text
#     and a blank signature line; on the lid the insect rears up on its hind legs gripping its black flag's pole, lifts it high, and rams it down
#     into the knob: the knob squashes flat and springs back, the lid jumps, the flag wobbles hard and settles (SIGNÉ); then, alive under the card, a
#     wing flick, a hard leg rub, its head turning to us, a second flick, while the camera eases in
D19 = st.dur('S19'); PL19 = 0.85; LIFT19 = [0.3, 0.62]
st.shot('S19', 'parisStreet', setOpts=SNOW, **WINTER, actors=[],
        props=[*KITCHEN(ruins=True, snow=True, sugar=False), *RUINS(snow=True),
               P('traite19', 'treatySheet', pos=[-0.07, r(TH + 0.001), -0.83], ry=-42, opts={'w': 0.26, 'text': True}),
               P('sucrier19', 'sugarBowl', pos=SB, opts={'dust': True, 'flag': PL19, 'flagFrom': 0.0, 'lift': LIFT19}),
               # (review 2) alive after the ram, under the card: a wing flick, a hard leg rub, its head turns to us and back, a second flick
               FLY('mouche19', [0.012, r(LIDTOP - 0.014), -0.95], ry=-90, s=0.55, plant=[0.0, PL19], rear=0.6,
                   grip=[[0.0, 0.0], [LIFT19[0], 0.0], [LIFT19[1], 0.064], [r(PL19 - 0.02), 0.0]],
                   flick=[[1.28, 1.42], [1.86, 1.96]], rub=[[1.45, D19]], rubAmp=2.0, rubHz=4.5, look=[[1.2, 0.0], [1.4, 0.55], [1.7, 0.55], [1.85, -0.2]])],
        cams=[cam(0.0, [-0.42, 1.12, -0.42], [-0.415, 1.115, -0.43], [5.258, -3.488, -7.241], [5.258, -3.488, -7.241], lens=52),
              glide([cam(1.1, [-0.39, 1.105, -0.46], [-0.385, 1.1, -0.47], [5.258, -3.488, -7.241], [5.258, -3.488, -7.241], lens=50)], 0.9)])
st.cue('sfx:pop', 'S19', PL19, 0.3); st.cue('sfx:ding', 'S19', 0.95, 0.2)

# 20: the general staff gave itself medals. Front, low: five generals in a row at attention in the snowy ruins, chests covered in ribbons and medals
#     from collar to belt; the medals clink, they rise on their toes, stretched tall, hang there a beat, then the whole row tips forward under the
#     weight, overshoots and stops leaning
D20 = st.dur('S20'); TIP20 = 0.7
GENS = [(-0.96, -0.45), (-0.48, -0.52), (0.0, -0.48), (0.48, -0.52), (0.96, -0.45)]
st.shot('S20', 'parisStreet', setOpts=SNOW, **WINTER, actors=[
        *[act(f'gen{j + 1}', [x_, 0, z_], 0, 'stand', 'smug', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.45, 'mouth': 'smirk'}}, toonDur=0.0),
            k(r(TIP20 - 0.45 + 0.03 * j), toon={'sq': [0.88, 1.16, 0.88], 'face': {'lid': 0.2, 'mouth': 'smirk', 'brow': 0.5}}, toonDur=0.15, toonEase='out'),
            k(r(TIP20 + 0.03 * j), toon={'sq': [1.0, 1.0, 1.0], 'lay': [0.7, 0.0], 'face': {'lid': 0.0, 'eye': 0.35, 'mouth': 'O', 'brow': 0.7}}, toonDur=0.6, toonEase='in'),
            k(r(TIP20 + 0.62 + 0.03 * j), toon={'sq': [1.06, 0.94, 1.06], 'lay': [0.56, 0.0], 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O', 'brow': 0.7}}, toonDur=0.15, toonEase='out'),
            k(r(TIP20 + 0.95 + 0.03 * j), toon={'lay': [0.6, 0.0], 'face': {'lid': 0.3, 'mouth': 'line'}}, toonDur=0.2)]) for j, (x_, z_) in enumerate(GENS)]],
        props=[*KITCHEN(ruins=True, snow=True, sugar=False), *RUINS(snow=True), *[KEPI(f'kepi20{j}', f'gen{j + 1}', color='#2B3A2A', band='#E2B53C') for j in range(5)],
               *[P(f'medailles20{j}', 'medalRack', on={'actor': f'gen{j + 1}', 'joint': 'torso', 'offset': [0.0, 0.5, 0.18]}, opts={'rows': 12, 'n': 7, 'w': 0.42, 'seed': 20 + j}) for j in range(5)]],
        # (review 2) further back and aimed higher: the faces stay in the frame through the hang on their toes
        cams=[cam(0.0, [3.8, 1.55, 3.5], [3.74, 1.55, 3.42], [-3.2, 0.7, -3.5], [-3.2, 0.7, -3.5], lens=44)])
st.cue('sfx:clink', 'S20', 0.2, 0.2); st.cue('sfx:clink', 'S20', r(TIP20 + 0.4), 0.25); st.cue('sfx:stretch', 'S20', TIP20, 0.2)

# 21: even the wasp. Over a general's shoulder, the treaty with its lines on the table: his big fingers bring a tiny medal to the insect on the sugar bowl's lid (its flag planted in the
#     knob) and pin it on its flank; it salutes with a front leg (DÉCORÉE)
D21 = st.dur('S21'); PIN21 = 0.42
GEN21 = [0.42, 0, -0.62]; FLY21 = [0.045, r(LIDTOP - 0.012), -0.95]
st.shot('S21', 'parisStreet', setOpts=SNOW, **WINTER, actors=[
        act('gen1', GEN21, -145, 'stand', 'smug', keys=[k(0.0, look=FLY21), k(0.0, toon={'bend': {'spine': [0.55, 0, 0, 1, None]}, 'reach': {'R': [0.2, 1.0, -0.8, 1, 0.03]}, 'hands': {'R': 'pinch'}}, toonDur=0.0),
            k(0.05, toon={'bend': {'spine': [0.6, 0, 0, 1, None]}, 'reach': {'R': [r(FLY21[0] + 0.05), r(FLY21[1] + 0.06), r(FLY21[2] + 0.04), 1, 0.03]}, 'hands': {'R': 'pinch'}}, toonDur=r(PIN21 - 0.05), toonEase='out'),
            k(r(PIN21 + 0.2), toon={'bend': {'spine': [0.45, 0, 0, 1, None]}, 'reach': {'R': [0.25, 1.1, -0.75, 1, 0.03]}, 'hands': {'R': 'rest'}}, toonDur=0.3)])],
        props=[*KITCHEN(ruins=True, snow=True, sugar=False), *RUINS(snow=True), P('sucrier21', 'sugarBowl', pos=SB, opts={'dust': True, 'flag': -1.0}),
               P('traite21', 'treatySheet', pos=[-0.07, r(TH + 0.001), -0.83], ry=-42, opts={'w': 0.26, 'text': True}),
               KEPI('kepi21', 'gen1', color='#2B3A2A', band='#E2B53C'), P('rack21', 'medalRack', on={'actor': 'gen1', 'joint': 'torso', 'offset': [0.0, 0.48, 0.18]}, opts={'rows': 7, 'n': 5, 'seed': 20}),
               P('petite21', 'medal', pos=[0.2, 0.98, -0.8], scale=0.3, keys=[k(0.05, to=[r(FLY21[0] + 0.03), r(FLY21[1] + 0.05), r(FLY21[2] + 0.03)], dur=r(PIN21 - 0.05), ease='out'), k(PIN21, visible=False)]),
               FLY('mouche21', FLY21, ry=-10, s=0.8, medal=PIN21, medalSide=-1, medalZ=-0.008, medalY=0.026, salute=r(PIN21 + 0.12))],
        cams=[cam(0.0, [-0.36, 1.0, -0.5], [-0.34, 0.995, -0.52], [0.04, 0.93, -0.95], [0.04, 0.93, -0.95], lens=40)])
st.cue('sfx:clink', 'S21', PIN21, 0.3); st.cue('sfx:fanfare', 'S21', r(PIN21 + 0.1), 0.15)

# 22: it was a fly. In the snowy ruins, framed exactly like the first shot (the sugar bowl centred, him behind at his table); the camera pushes in
#     slowly over a second and stops on the insect on the rim, at three fifths of the height: plainly a fly, big red eyes, a medal on its flank,
#     rubbing its front legs hard (the medal on its flank, not under its eyes); above it, snowed on, his face, deadpan, as he sips his cup and lowers
#     it to his chest
D22 = st.dur('S22')
# (review 2) after the sip the cup comes down by the same face-relative target (the switch back to a world target slid the cup off and snapped it back)
SIPDOWN = {'touch': {'R': ['face', -0.08, -0.48, 0.22, 1, 0.03]}, 'hands': {'R': 'grip'}}
st.shot('S22', 'parisStreet', setOpts=SNOW, **WINTER, actors=[
        MECSIT([*sit_keys(look='camera'), k(1.3, toon={**SIP, 'face': DEAD}, toonDur=0.3), k(2.05, toon={**SIPDOWN, 'face': DEAD}, toonDur=0.3)])],
        props=[*KITCHEN(ruins=True, snow=True, sugar=False), CUP(), *RUINS(snow=True), P('sucrier22', 'sugarBowl', pos=SB, opts={'dust': True, 'snow': True}),
               P('neige22', 'snowCap', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.42, 0.0]}, opts={'w': 0.32, 'h': 0.22, 't0': -2.0, 't1': -1.0}),
               FLY('mouche22', RIM, ry=-15, s=0.85, medal=True, medalSide=-1, medalZ=-0.008, medalY=0.026, rub=[[0.3, D22]], rubAmp=2.0)],
        cams=[cam(0.0, [0.0, 1.0, 0.2], [0.0, 1.0, 0.16], [0.0, 1.12, -1.4], [0.0, 1.12, -1.4], lens=56),
              glide([cam(0.35, [0.0, 1.0, 0.0], [0.0, 1.0, -0.02], [0.0, 0.449, -9.985], [0.0, 0.449, -9.985], lens=55)], 1.2)])
st.cue('sfx:static', 'S22', 0.0, 0.04); st.cue('sfx:sting', 'S22', 0.5, 0.25)

MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
st.write("La guêpe", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'flic': {'preset': 'cop', 'seed': 811, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'flic2': {'preset': 'cop', 'seed': 811, 'hat': 'none', 'hair': 'bald', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': {'holdLife': 1.2, 'shift': 0.8, 'breathe': 1.4}},
    **{f'crs{j + 1}': {'preset': 'swat', 'seed': 812 + j, 'hat': 'none', 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX} for j in range(3)},
    **{f'sold{j + 1}': {**SOLD, 'preset': 'cop' if j % 2 == 0 else 'cop2', 'seed': 815 + j} for j in range(3)},
    'officier': {**SOLD, 'preset': 'cop', 'seed': 818, 'suit': '#4E5A32', 'facial': 'mustache'},
    **{f'gen{j + 1}': {'preset': 'politique', 'seed': 820 + j, 'suit': '#4A5530', 'lapel': '#4A5530', 'tie': '#2E351E', 'glasses': False, **({'facial': 'mustache'} if j % 2 == 0 else {}), 'hairColor': '#9A9A96', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.12}, 'toon': EX} for j in range(5)},
})
