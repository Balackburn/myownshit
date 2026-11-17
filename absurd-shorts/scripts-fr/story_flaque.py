#!/usr/bin/env python3
"""La flaque (story 82, cycle 44; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man stepped in a puddle. He reported a flood. The navy declared it enemy waters. A submarine dived into it. It came up with the street on its
back. Its torpedo went through the bakery. And the fire station. The puddle was unhurt. The air force promised a surgical strike. Three hundred
bombs. Three hundred craters. Then it rained. Three hundred puddles. The minister ordered three hundred submarines. One per puddle. With the town
on their backs. They parked it in the harbour. Officially, the town moved. Not him. Nor the puddle.
Staging: on a sunny Paris pavement he walks into a doormat-sized puddle that mirrors the sky (water up one trouser leg, his face unchanged); phone at
his ear, one leg soaked and dripping, he points down at it; in a navy office an officer in an anchor cap winds up and slams a big stamp on the street
plan where the puddle is circled (ENNEMIE); a full-size submarine dives nose first into the puddle, squeezes through and is gone (two tiny ripples);
a block away it surfaces through the road with a slab of street on its back, two parked cars and a lamp sliding off; a torpedo skims over the
puddle and punches through the bakery, baguettes spinning out of every window; it bursts out of the fire station, the fire engine somersaulting;
in the rubble and smoke the puddle lies perfectly still, he wrings out his sock behind it (INTACTE); at a press-room podium a general holds up one
finger and taps a tiny crosshair on a street plan; three jets carpet-bomb in neat rows; from straight above, rows of dry craters and only his
puddle shining in a corner; one small cloud drifts over and rains; every crater is now a puddle; the minister signs an order form so long it
unrolls off the podium, across the floor and out of the door; three hundred periscopes pop up, one in every puddle, and all turn to him beside his
own puddle, the only one without; all the hulls surface together and the whole town rises on their backs like a lid, except his round patch;
the town is moored in the harbour, a rope round the town hall's clock, a gendarme slipping a parking ticket under its door; the minister slides
the town's icon on the wall map from inland to the coast (DÉMÉNAGÉE); he stands alone with his briefcase on his patch of pavement in a bare plain;
framed exactly like the first shot, he steps into the same puddle again.
Natural look; cycle 44: props_flaque.js (puddle, divingSub, surfacingSub, bakeryFront, fireStation, deskMap, strikeEasel, bombCarpet, craterField,
orderForm, periscopeField, townLid, harbourQuay, townMapWall, barePlain, legDrips); submarine (props_robinet), fighterJet, missileSalvo, rainCloud,
fireTruck, rubbleHeap (props_guepe), toonPuff (props_bocal), bigStamp (props_eternuement), captainCap (props_poisson), kepi (props_conseiller),
fineTicket (props_echo), briefcase, smartPhone, sockSingle, pen, table, openDoor (props_table), explosionBurst reused.
Lessons applied from the start: `lens` is the vertical field (bigger = wider); main props and faces above the caption band (0.77-0.86); the man's
right hand is at -X when he faces +Z; every camera checked with project() before stills; the last shot is framed like the first."""
from story_kit import *
import math

st = Story('flaque', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0),
         ('S08', 'L08', 0), ('S09', 'L09', 0), ('S10', 'L10', 0), ('S11', 'L11', 0), ('S12', 'L14', 0), ('S13', 'L14', 4), ('S14', 'L15', 0),
         ('S15', 'L16', 0), ('S16', 'L17', 0), ('S17', 'L18', 0), ('S18', 'L19', 0), ('S19', 'L20', 0)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
DEAD = {'lid': 0.4, 'mouth': 'line'}
STREET = {'eiffelStyle': 'v2', 'clear': [-14.0, 30.0], 'clearL': [-14.0, 30.0]}
PRESS = {'backdrop': 'AVIATION|DÉFENSE|AVIATION|DÉFENSE', 'chairs': False, 'fg': 'rgba(255,255,255,0.2)', 'fontScale': 0.8}   # (round 1) dimmed wall words

# the street: the road along Z (x -5..5), the right-hand pavement x 5..10, the house fronts at x 10.2; his puddle on the pavement
PUD = [7.4, 0, 0.0]
MAN0 = [7.3, 0, -1.95]; MANP = [7.3, 0, -0.2]         # he walks along +Z and stops with his left foot (his left is +X) in the puddle
C1 = cam(0.0, [5.6, 1.05, 3.2], [5.62, 1.04, 3.12], [7.35, 0.65, -1.0], [7.35, 0.65, -1.0], lens=54)   # low three-quarter front, the puddle in the foreground
OFF1 = [C1['from'][i] - PUD[i] for i in range(3)]; OFFL1 = [C1['lookAt'][i] - PUD[i] for i in range(3)]

def STAND(keys, pos, ry=0, expr='unimpressed', clip='stand', **kw): return act('mec', pos, ry, clip, expr, keys=keys, **kw)
CASE = lambda pid='mallette': P(pid, 'briefcase', on={'actor': 'mec', 'hand': 'L'})
PUDDLE = lambda pid='flaque', pos=PUD, **o: P(pid, 'puddle', pos=pos, opts=o)

for g_ in [('S01', 0.95, 'mec', 'splash'), ('S03', 0.88, 'marin', 'stamp'), ('S04', 0.88, 'mec', 'take'), ('S09', 0.4, 'general', 'finger'), ('S16', 0.55, 'gendarme', 'ticket')]:
    st.gag(*g_)
st.card('S03', 'ENNEMIE', at=1.1)
st.card('S08', 'INTACTE', at=0.62)
st.card('S17', 'DÉMÉNAGÉE', at=1.25)

# 1: the hook. Low three-quarter front on the sunny pavement, the puddle in the foreground mirroring the sky: briefcase in hand, he walks straight
#    into it; his left foot lands in the middle and water splashes up that trouser leg; he stops, looks down at it, then at us, face unchanged
#    (round 1: a brisker walk from closer, so the look to camera lands by 1.5 s, before the cut; the camera aims lower, the puddle sits higher)
D1 = st.dur('S01'); STEP1 = 0.95
#    (round 2) the take in three poses: he settles on the step (a squash), looks down at the puddle for eight frames (the head bowed), then looks at us;
#    it was a one- or two-frame dip of the head
def walk_in(t0, dur, start, stop, step, look_at, lk=(0.06, 0.36)):
    return [k(0.0, look=look_at), k(t0, to=stop, dur=dur, clip='walk', ease='linear'),
            k(step, toon={'sq': [1.05, 0.94, 1.05], 'face': DEAD}, toonDur=0.05),
            k(r(step + lk[0]), look=[stop[0] + 0.1, 0.0, stop[2] + 0.3], lookDur=0.1),
            k(r(step + lk[0]), toon={'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.5, 'mouth': 'line', 'brow': -0.1}, 'bend': {'neck': [0.3, 0, 0, 1, None]}}, toonDur=0.1),
            k(r(step + lk[1]), look='camera', lookDur=0.12),
            k(r(step + lk[1]), toon={'sq': [1.0, 1.0, 1.0], 'face': DEAD, 'bend': {'neck': [0.0, 0, 0, 1, None]}}, toonDur=0.12)]
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[STAND(walk_in(0.05, 0.9, MAN0, MANP, STEP1, [7.0, 1.4, 2.0]), MAN0)],
        props=[CASE(), PUDDLE(splash=[STEP1], splashDir=[0.1, 0.2], ripple=[STEP1, r(STEP1 + 0.25)])],
        cams=[C1])
st.cue('sfx:stepRun', 'S01', 0.1, 0.12); st.cue('sfx:splash', 'S01', STEP1, 0.45)

# 2: he reported a flood. Medium shot from the front: standing with his left foot still in the puddle, that trouser leg dark and dripping, a phone
#    at his right ear, he points his left index finger straight down at the puddle, talking, deadpan
#    (round 1: the phone hand is held at the ear in the frame of his face, so it stays there when he turns his head; the pointing arm stretches all
#    the way down and the fingertip dips into the puddle; the wet trouser band is darker and glossy)
#    (round 2) he stands beside the puddle, at its back left, so his arm goes forward and down to it, clear of his legs (it hung beside them like a
#    third leg): the index finger dips into the water three times as he talks, a ring on each dip, the body bobbing; the phone in his right hand is
#    held against the side of his head (a `touch` on his face: `reach` takes no face point, so the hand had stayed at his collarbone); the soaked
#    trouser leg is a dark gloss on the trouser itself (wetShin) with drips off the hem, not a separate black sleeve
D2 = st.dur('S02'); MAN2 = [6.95, 0, -0.45]; DIP2 = [0.3, 0.66, 1.05]
#    (round 3) a big red old-style handset at his ear (the small black smartphone did not show: the hand at the side of his tipped head read as
#    scratching his head or saluting), his head nearly upright (the phoneEar clip and the forward bend tipped it 40 degrees), the wet shin darker
PT2 = lambda t_, y_, sq=(1, 1, 1), d_=0.12: k(t_, toon={'reach': {'L': [7.42, y_, 0.02, 1, 0.07]}, 'touch': {'R': ['face', -0.64, 0.42, -0.06, 1, 0.0]}, 'hands': {'L': 'point', 'R': 'grip'},
                                                       'bend': {'spine': [0.14, 0, 0, 1, None], 'neck': [-0.12, 0, 0, 1, None]}, 'sq': list(sq), 'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.2}}, toonDur=d_, toonEase='inOut')
WET = lambda pid='gouttes': P(pid, 'legDrips', on={'actor': 'mec', 'joint': 'footL', 'offset': [0.0, 0.0, 0.0]}, opts={'n': 7, 'r': 0.07, 'y0': 0.07, 'fall': 0.1})
WETSHIN = lambda pid='mouille': P(pid, 'wetShin', on={'actor': 'mec', 'joint': 'kneeL'}, opts={'h': 0.6, 'opacity': 0.82, 'color': '#010205'})   # (round 3) a stronger dark gloss
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[
        STAND([k(0.0, look='camera'), PT2(0.0, 0.16, d_=0.0), *[PT2(t_, 0.015 if j % 2 == 0 else 0.17, (1.02, 0.98, 1.02) if j % 2 == 0 else (0.99, 1.02, 0.99))
                                                              for j, t_ in enumerate([DIP2[0], 0.48, DIP2[1], 0.86, DIP2[2], 1.28])],
               *st.talk('L02', 'S02', base='unimpressed'),
               k(0.78, look=[7.3, 0.5, 0.3], lookDur=0.1), k(1.02, look='camera', lookDur=0.12)], MAN2, 25, clip='stand')],
        props=[PUDDLE(ripple=[r(d + 0.04) for d in DIP2]), P('tel', 'handset', on={'actor': 'mec', 'joint': 'head', 'offset': [-0.2, 0.2, 0.03]}, opts={'len': 0.32, 'rot': [-0.35, r(PI / 2), 0.0]}), WET(), WETSHIN()],
        cams=[cam(0.0, [6.0, 2.1, 3.9], [6.04, 2.08, 3.8], [7.15, 0.85, -0.2], [7.15, 0.85, -0.2], lens=54)])
st.cue('sfx:beep', 'S02', 0.05, 0.12)

# 3: the navy declared it enemy waters. In a navy office, from above the desk: an officer in a white anchor cap stands behind it over the street plan
#    where the puddle is circled in red; he winds a big rubber stamp up over his head and slams it down on the circle: he squashes on the hit, the
#    desk jumps, « EAUX ENNEMIES » is stamped across the plan (ENNEMIE), then he springs back up taller and lifts the stamp clear, proud
#    (round 1: a higher camera frames him lower, so the card band no longer covers his cap and brow; the hit comes earlier (0.88 s) and the stamp is
#    lifted clear of the print by 1.04 s, before the card lands)
D3 = st.dur('S03'); HIT3 = 0.88
DESK = [0.0, 0, -1.2]; DESKH = 0.76; MAP3 = [0.0, r(DESKH + 0.002), -1.15]
MARIN = [0.12, 0, -1.9]
STAMPUP = [0.12, 2.05, -1.62]; STAMPDN = [0.07, r(DESKH + 0.47), -1.15]; STAMPLIFT = [-0.32, 1.62, -1.55]
def held(p_, sq=(1, 1, 1), face=None, dur=0.12, ease='inOut', t=0.0):
    return k(t, toon={'reach': {'R': [*p_, 1, 0.03], 'L': [0.45, 0.85, -1.35, 1, 0.04]}, 'hands': {'R': 'grip', 'L': 'open'}, 'sq': list(sq), 'face': face or {'lid': 0.2, 'mouth': 'line', 'brow': -0.6}}, toonDur=dur, toonEase=ease)
st.shot('S03', 'office', setOpts={'door': False, 'printer': False, 'picture': False, 'carpet': False, 'wall': '#DCE6EE', 'band': '#2E4563', 'trim': '#1E2E44'}, actors=[
        act('marin', MARIN, 0, 'stand', 'determined', keys=[k(0.0, look=[0.05, 0.8, -1.15]),
            held([0.2, 1.25, -1.55]), held([0.15, 1.3, -1.6], t=0.15, dur=0.15),
            held(STAMPUP, (0.94, 1.12, 0.94), t=0.38, dur=0.25, ease='out'),
            held(STAMPDN, (1.02, 0.98, 1.02), t=r(HIT3 - 0.1), dur=0.1, ease='in'),
            held(STAMPDN, (1.25, 0.72, 1.25), {'lid': 0.0, 'pop': 0.35, 'mouth': 'clench', 'brow': -0.8}, t=HIT3, dur=0.04, ease='out'),
            held(STAMPLIFT, (0.94, 1.1, 0.94), {'lid': 0.1, 'mouth': 'smile', 'brow': 0.3}, t=r(HIT3 + 0.16), dur=0.12, ease='out'),
            held(STAMPLIFT, (1.0, 1.0, 1.0), {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}, t=r(HIT3 + 0.34), dur=0.12),
            k(r(HIT3 + 0.36), look='camera', lookDur=0.15)])],
        props=[P('bureau', 'table', pos=DESK, opts={'w': 1.6, 'd': 0.9, 'h': DESKH, 'color': '#6B4F3A', 'legs': '#4A3626'},
                 keys=[k(HIT3, to=[0.0, 0.03, -1.2], dur=0.04), k(r(HIT3 + 0.05), to=DESK, dur=0.1)]),
               P('plan3', 'deskMap', pos=MAP3, opts={'markAt': HIT3}),
               P('tampon', 'bigStamp', on={'actor': 'marin', 'hand': 'R'}, opts={'color': '#C8322A'}),
               P('casquette', 'captainCap', on={'actor': 'marin', 'joint': 'head', 'offset': [0.0, 0.47, 0.0]}, opts={'r': 0.13}),
               P('etoiles3', 'impactStars', pos=[0.07, r(DESKH + 0.05), -1.15], opts={'at': HIT3, 'n': 5})],
        fx=[{'type': 'shake', 'at': HIT3, 'dur': 0.15, 'amount': 0.012}],
        cams=[cam(0.0, [0.3, 3.2, 2.4], [0.3, 3.18, 2.3], [0.05, 1.4, -1.4], [0.05, 1.4, -1.4], lens=54)])
st.cue('whoosh', 'S03', 0.4, 0.2); st.cue('thud', 'S03', HIT3, 0.5); st.cue('sfx:punch', 'S03', HIT3, 0.3)

# 4: a submarine dived into it. Low on the pavement, the puddle big in the foreground: a full-size grey submarine, fatter than he is tall, plunges
#    nose first out of the sky into the doormat-sized puddle, squeezes thin through it (the blue rim shows all round the hull) and is gone, tail fins
#    last; a splash crown, two ripples, the puddle as it was. Behind it he does a double take: looks up at it, down at the puddle, eyes pop out, then
#    back to us, deadpan (round 1: was a far shot with no puddle readable and a black hole in the pavement)
D4 = st.dur('S04'); TOUCH4 = 0.62; GONE4 = 1.2
MAN4 = [8.25, 0, -0.55]
T4 = lambda t_, face, sq=(1, 1, 1), d_=0.08: k(t_, toon={'sq': list(sq), 'face': face}, toonDur=d_)
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[
        STAND([k(0.0, look='camera'), k(0.22, look=[6.4, 5.0, 0.0], lookDur=0.12), T4(0.22, {'lid': 0.0, 'brow': 0.4, 'mouth': 'line'}),
               k(0.72, look=[7.4, 0.0, 0.05], lookDur=0.1),
               T4(0.88, {'pop': 0.45, 'lid': 0.0, 'brow': 0.9, 'mouth': 'O'}, (0.92, 1.12, 0.92), 0.05),
               T4(1.1, {'pop': 0.0, 'lid': 0.1, 'brow': 0.3, 'mouth': 'line'}, (1.04, 0.96, 1.04), 0.08),
               k(1.16, look='camera', lookDur=0.1), T4(1.3, DEAD, (1, 1, 1), 0.12)], MAN4, -20)],
        props=[CASE(), PUDDLE(ripple=[GONE4, r(GONE4 + 0.22)], splash=[TOUCH4], splashDir=[0.0, 0.0]),
               P('sousmarin4', 'divingSub', pos=[PUD[0], 0, PUD[2]], opts={'L': 8.0, 'tilt': 1.0, 'at': 0.0, 'touch': TOUCH4, 'gone': GONE4, 'r': 0.18, 'ry': r(PI / 2), 'collar': True, 'collarWater': True,
                 'approach': [0.0, 3.4], 'peri': [[0.0, 1.0]]})],   # (round 3) it comes down slowly first, whole in a wide frame, periscope up; the rim bulge is water
        #    (round 3) a wide frame first (the whole submarine in the sky over the street, conning tower and periscope, him small at the right looking up),
        #    then a quick glide down to the puddle for the squeeze (it was a dark mass, then a pole: it never read as a submarine)
        cams=[cam(0.0, [6.6, 1.4, 15.5], [6.55, 1.4, 15.2], [5.2, 4.1, -0.5], [5.4, 3.9, -0.5], lens=56),
              glide([cam(0.42, [7.0, 1.4, 5.4], [7.0, 1.38, 5.25], [7.6, 0.9, -0.6], [7.6, 0.9, -0.6], lens=48)], 0.2)])
st.cue('whoosh', 'S04', 0.2, 0.35); st.cue('sfx:splash', 'S04', TOUCH4, 0.3); st.cue('sfx:pop', 'S04', GONE4, 0.3); st.cue('sfx:boing', 'S04', 0.88, 0.2)

# 5: it came up with the street on its back. Down the street, a block away: the road breaks open and the same submarine rises through it carrying a
#    slab of street, two parked cars and a lamp; the slab tips, each car slides to the low lip, teeters there, drops off and bounces on the road; the
#    lamp topples; in the right foreground, back to us, he watches, then glances at us (round 1: the cars now get off; he is in the shot)
D5 = st.dur('S05'); SUB5 = [0.0, 0, -16.0]
#    (round 2) the low lip of the slab is framed inside the picture (the payoff was half off the left edge); the tip starts at 0.45 s, the first car
#    slides the length of the slab, hangs five frames on the lip, drops and bounces by about 1.5 s; for the last 0.3 s he turns round to us
MAN5 = [3.7, 0, -3.8]
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[STAND([k(0.0, look=[0.0, 2.0, -16.0]), k(0.32, toon={'sq': [1.05, 0.94, 1.05]}, toonDur=0.06), k(0.44, toon={'sq': [1, 1, 1]}, toonDur=0.15),
                                                       k(0.8, look=[-3.5, 1.0, -16.0], lookDur=0.25), k(1.28, to=MAN5, dur=0.16, face=10, ease='out'), k(1.3, look='camera', lookDur=0.12)], MAN5, -170)],   # (round 3) the glance at 1.3 s, held (it came in the last two frames)
        props=[CASE(), PUDDLE(),
               P('sousmarin5', 'surfacingSub', pos=SUB5, opts={'L': 8.0, 'at': 0.15, 'dur': 0.42, 'y1': -0.7, 'tip': 0.5, 'tipAt': 0.45, 'slideAt': 0.5, 'carX0': [-2.5, -1.5], 'hang': 0.16, 'accK': 2.0, 'subRy': r(PI / 2)}),   # (round 3) side-on, higher: the conning tower reads
               *[P(f'poussiere5{j}', 'toonPuff', pos=[x_, 0.3, z_], opts={'at': r(0.3 + 0.05 * j), 'n': 6, 'size': 0.8, 'rise': 1.6, 'spread': 2.0, 'life': 1.0, 'color': '#D9D2C4'})
                 for j, (x_, z_) in enumerate([(-3.5, -12.0), (3.5, -12.0), (-3.5, -20.0), (3.5, -20.0)])]],
        fx=[{'type': 'shake', 'at': 0.35, 'dur': 0.4, 'amount': 0.015}],
        cams=[cam(0.0, [5.6, 1.8, 5.6], [5.55, 1.82, 5.4], [-1.2, 2.0, -16.0], [-1.2, 2.1, -16.0], lens=44)])
st.cue('thunder', 'S05', 0.35, 0.45); st.cue('sfx:crunch', 'S05', 0.35, 0.4); st.cue('sfx:splash', 'S05', 0.45, 0.25); st.cue('sfx:crunch', 'S05', 1.48, 0.35)

# 6: its torpedo went through the bakery. Low behind the puddle on the pavement, the puddle mid-frame: a torpedo rushes past the lens, skims low over
#    the puddle (its wake splashes and ripples the reflection) and the camera whips after it to the bakery: the starburst, the hole and the
#    baguettes all come on the impact frame, with a short shake (round 1: the facade stayed clean until the hit; the starburst was there from the
#    first frame; the puddle was a sliver under the captions)
D6 = st.dur('S06'); HIT6 = 0.95; PASS6 = 0.72
BAK = [10.0, 0, 4.0]; HITP6 = [9.95, 1.6, 4.0]
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[],
        props=[PUDDLE(ripple=[0.08, 0.38, PASS6, r(PASS6 + 0.18)], splash=[PASS6], splashDir=[-0.2, 1.4]),   # (round 2) the water trembles before the torpedo
               P('boulangerie', 'bakeryFront', pos=BAK, ry=-90, opts={'w': 8.0, 'h': 10.0, 'hitAt': HIT6, 'hit': [0.0, 1.6], 'n': 2}),
               P('torpille6', 'missileSalvo', pos=[0, 0, 0], opts={'shots': [{'from': [5.9, 1.0, -7.0], 'ctrl': [6.875, -0.7, 1.5], 'to': HITP6, 't0': r(HIT6 - 0.46), 'dur': 0.46, 'lin': True}],
                 'size': 0.55, 'trail': 0.45, 'trailWidth': 0.12, 'trailOpacity': 0.55, 'flame': 0.6, 'glow': 0.3, 'bodyColor': '#5E6B7A'}),
               P('boum6', 'timedBurst', pos=[9.4, 0.0, 3.7], ry=-154, opts={'at': HIT6, 'size': 1.65}),
               P('fumee6', 'toonPuff', pos=[9.4, 1.4, 4.0], opts={'at': r(HIT6 + 0.05), 'n': 8, 'size': 0.7, 'rise': 1.5, 'spread': 1.4, 'life': 1.0, 'color': '#E6DCC8'})],
        fx=[{'type': 'shake', 'at': HIT6, 'dur': 0.12, 'amount': 0.022}],
        cams=[cam(0.0, [6.3, 1.6, -2.6], [6.42, 1.45, -1.95], [7.5, 0.35, 1.2], [7.5, 0.35, 1.2], lens=58, ease='inOut'),   # (round 2) a slow push in (it was a still plate for 0.6 s)
              glide([cam(0.72, [6.38, 1.5, -2.15], [6.38, 1.52, -2.05], [9.3, 1.75, 4.0], [9.3, 1.8, 4.0], lens=58)], 0.2)])
st.cue('whoosh', 'S06', 0.55, 0.45); st.cue('sfx:splash', 'S06', PASS6, 0.25); st.cue('thunder', 'S06', HIT6, 0.5); st.cue('sfx:glass', 'S06', r(HIT6 + 0.05), 0.35)

# 7: and the fire station. Further down the street: the torpedo bursts out through the fire station's doors and the red fire engine somersaults out
#    over the road, doors spinning away, smoke rolling out (round 1: the starburst is not there before the burst)
D7 = st.dur('S07'); BURST7 = 0.3
FIRE = [10.0, 0, 26.0]
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[],
        props=[P('caserne', 'fireStation', pos=FIRE, ry=-90, opts={'w': 10.0, 'h': 7.0, 'burstAt': BURST7}),
               P('camion7', 'fireTruck', pos=[8.4, 0.2, 26.3], ry=180, keys=[k(BURST7, to=[5.0, 4.4, 25.8], dur=0.42, ease='out'), k(r(BURST7 + 0.42), to=[1.6, 0.2, 24.8], dur=0.45, ease='in'),
                                                                              k(BURST7, rotTo=[0, PI, r(-2 * PI)], dur=0.87, ease='linear')]),
               P('torpille7', 'missileSalvo', pos=[0, 0, 0], opts={'shots': [{'from': [9.4, 1.6, 26.6], 'to': [-14.0, 2.4, 21.0], 't0': BURST7, 'dur': 0.35, 'lin': True}],
                 'size': 0.42, 'trail': 0.5, 'trailWidth': 0.12, 'trailOpacity': 0.5, 'flame': 0.6, 'glow': 0.3, 'bodyColor': '#5E6B7A'}),
               P('boum7', 'timedBurst', pos=[9.3, 0.0, 26.0], ry=-124, opts={'at': BURST7, 'size': 2.0})],
        fx=[{'type': 'shake', 'at': BURST7, 'dur': 0.3, 'amount': 0.02}],
        cams=[cam(0.0, [-9.0, 2.8, 13.5], [-8.9, 2.85, 13.6], [6.0, 3.4, 25.5], [6.0, 3.4, 25.5], lens=52)])
st.cue('thunder', 'S07', BURST7, 0.5); st.cue('sfx:siren', 'S07', r(BURST7 + 0.2), 0.15); st.cue('clang', 'S07', r(BURST7 + 0.9), 0.3)

# 8: the puddle was unhurt. Low at the puddle: rubble, bricks and baguettes all round, smoke rising, and in the middle the puddle perfectly still,
#    mirroring the blue sky (INTACTE); behind it he wrings out his wet sock into a spiral, which springs back with a burst of drops; deadpan
#    (round 1: the camera sits further back and lower so his head is under the card band and the puddle above the captions; the sock is wrung;
#    the baguettes are fat golden loaves)
D8 = st.dur('S08')
MAN8 = [7.75, 0, 1.55]
WRING = lambda t_, up: k(t_, toon={'reach': {'R': [7.62, r(1.42 + 0.06 * up), 1.3, 1, 0.03], 'L': [7.9, r(1.1 - 0.06 * up), 1.3, 1, 0.03]}, 'hands': {'R': 'grip', 'L': 'grip'}, 'face': DEAD}, toonDur=0.12, toonEase='inOut')   # (round 2) higher, the hands further apart
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[STAND([k(0.0, look=[7.6, 1.1, 1.0]), WRING(0.0, 1), WRING(0.2, -1), WRING(0.4, 1), WRING(0.6, -1),
                                                             k(0.8, toon={'sq': [0.96, 1.05, 0.96], 'face': {'lid': 0.1, 'brow': 0.4, 'mouth': 'line'}}, toonDur=0.06),
                                                             k(0.95, look='camera', lookDur=0.12), k(0.98, toon={'sq': [1, 1, 1], 'face': DEAD}, toonDur=0.1), WRING(1.05, 1)], MAN8, 195)],
        props=[PUDDLE(),
               P('chaussette', 'wrungSock', on={'actor': 'mec', 'hand': 'R'}, opts={'wring': [[0.0, 0.3], [0.35, 0.8], [0.7, 1.0]], 'spring': 0.8, 'len': 0.6, 'w': 0.11, 'n': 10}),   # (round 2) a bigger sock
               WET('gouttes8'), WETSHIN('mouille8'),
               P('tas8a', 'rubbleHeap', pos=[9.4, 0, 3.6], opts={'r': 1.6, 'h': 1.1, 'dust': True, 'seed': 4}),
               P('tas8b', 'rubbleHeap', pos=[5.4, 0, 3.0], opts={'r': 1.2, 'h': 0.8, 'seed': 9}),
               P('tas8c', 'rubbleHeap', pos=[9.3, 0, -1.4], opts={'r': 0.9, 'h': 0.6, 'seed': 13}),
               *[P(f'pain8{j}', 'fatBaguette', pos=[x_, 0.0, z_], ry=a_) for j, (x_, z_, a_) in enumerate([(6.6, 0.9, 30), (8.3, 0.3, -50), (6.9, -0.9, 80), (8.6, 1.0, 10)])],
               *[P(f'fumee8{j}', 'toonPuff', pos=[x_, 0.8, z_], opts={'n': 5, 'size': 0.45, 'rise': 2.4, 'spread': 0.6, 'life': 1.6, 'color': '#9C958C'}) for j, (x_, z_) in enumerate([(8.9, 3.4), (6.0, 3.3)])]],
        cams=[cam(0.0, [7.05, 1.2, -5.4], [7.06, 1.2, -5.3], [7.6, 0.8, 1.6], [7.6, 0.8, 1.6], lens=48)])
st.cue('sfx:wind', 'S08', 0.0, 0.2); st.cue('sfx:pour', 'S08', 0.2, 0.15); st.cue('sfx:boing', 'S08', 0.8, 0.2)

# 9: the air force promised a surgical strike. Press room: at the podium an air force general snaps one finger straight up above his head (a dip,
#    then the arm shoots up, overshoots and holds), then turns and taps the tiny red crosshair on the street plan on the easel beside him: it pulses
#    on the touch (round 1: the raised hand read as a hand at his temple; the tap landed above the crosshair and late; the wall words are dimmed)
D9 = st.dur('S09'); UP9 = 0.4; TAP9 = 1.42
EASEL = [0.78, 0, -2.3]
CROSS9 = [0.686, 1.45, -2.04]
GEN = [0.0, 0, -2.45]
GK = lambda t_, L_, hand, sq=(1, 1, 1), face=None, d_=0.12, e='inOut': k(t_, toon={'reach': {'L': [*L_, 1, 0.05], 'R': [-0.25, 1.17, -2.05, 1, 0.04]}, 'hands': {'L': hand, 'R': 'grip'}, 'sq': list(sq), 'face': face or {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}}, toonDur=d_, toonEase=e)
st.shot('S09', 'pressRoom', setOpts=PRESS, actors=[
        act('general', GEN, 0, 'stand', 'determined', keys=[k(0.0, look='camera'),
            GK(0.0, [0.28, 1.2, -2.15], 'open', d_=0.0),
            GK(0.25, [0.3, 1.0, -2.2], 'fist', (1.05, 0.93, 1.05), {'lid': 0.4, 'mouth': 'line', 'brow': -0.5}),
            GK(UP9, [0.4, 2.95, -2.4], 'point', (0.95, 1.08, 0.95), {'lid': 0.1, 'mouth': 'smile', 'brow': 0.3}, 0.1, 'out'),
            GK(r(UP9 + 0.16), [0.38, 2.8, -2.42], 'point', (1, 1, 1), {'lid': 0.2, 'mouth': 'smile', 'brow': 0.2}),
            GK(0.85, [0.4, 2.85, -2.4], 'point', (1, 1, 1), {'lid': 0.25, 'mouth': 'smile', 'brow': 0.25}, 0.2),
            k(1.02, look=[0.69, 1.45, -2.06], lookDur=0.12),
            GK(1.22, [0.71, 1.53, -2.0], 'point', d_=0.2),
            GK(TAP9, CROSS9, 'point', d_=0.05),
            GK(r(TAP9 + 0.12), [0.71, 1.5, -2.0], 'point', d_=0.08),
            k(r(TAP9 + 0.25), look='camera', lookDur=0.15)])],
        props=[P('chevalet', 'strikeEasel', pos=EASEL, ry=-25, opts={'w': 0.75, 'tapAt': [TAP9]}),
               P('kepi9', 'kepi', on={'actor': 'general', 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'w': 0.222, 'd': 0.17, 'color': '#2E3C55', 'band': '#1E2846'})],
        cams=[cam(0.0, [0.25, 1.65, 1.45], [0.23, 1.65, 1.35], [0.4, 1.62, -2.3], [0.4, 1.62, -2.3], lens=52)])
st.cue('sfx:click', 'S09', UP9, 0.2); st.cue('sfx:ding', 'S09', TAP9, 0.25)

# 10: three hundred bombs. From the street, looking up: three jets in tight formation roar overhead and let go a carpet of bombs in neat rows
D10 = st.dur('S10'); REL10 = 0.3
JETS10 = [(-6.0, 0.0), (0.0, 7.0), (6.0, 0.0)]
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[],
        props=[*[P(f'jet10{j}', 'fighterJet', pos=[x_, 34.0, r(-120.0 + dz)], scale=0.6, opts={'burner': 0.8, 'glow': 0.5, 'contrail': True},
                   keys=[k(0.0, to=[x_, 34.0, r(30.0 + dz)], dur=D10, ease='linear')]) for j, (x_, dz) in enumerate(JETS10)],
               P('bombes10', 'bombCarpet', pos=[0.0, 32.5, -62.0], opts={'at': REL10, 'rows': 6, 'cols': 5, 'gap': 3.2, 'dt': 0.06, 'v': 80, 's': 2.2})],
        cams=[cam(0.0, [4.0, 1.6, 8.0], [4.0, 1.6, 7.6], [0.0, 28.0, -40.0], [0.0, 26.0, -40.0], lens=58)])
st.cue('sfx:jet', 'S10', 0.0, 0.5); st.cue('whoosh', 'S10', 0.5, 0.3)

# 11: three hundred craters / then it rained / three hundred puddles. One locked camera, high above the neighbourhood (roofed blocks between the
#     craters: the same town): the craters pop in row after row with dust puffs as the bombs land, his little puddle shines inboard in a white ring;
#     one small grey cloud drifts in over them and rains; one after another every crater fills with water; the frame holds on the three hundred
#     glittering puddles, glints flashing on them (round 1: the craters were there from the first frame and the frame froze twice)
D11 = st.dur('S11'); RAIN11 = st.at('S11', 'L12', 0); FULL11 = st.at('S11', 'L13', 0)
#     (round 2) the same Paris as the street: the blocks are the street's Haussmann buildings (cream stone, grey-blue mansard roofs), round trees,
#     and the Eiffel tower stands in the frame; the camera is still locked but tipped to about 59 degrees so the tower and the rain read; his puddle
#     sits at a third of the width, 60 % of the height; at the end every filled puddle gets travelling rings and bigger glints (it froze there)
HOME11 = [-6.8, 0.0]; EIF11 = [-10.2, 0.03, -10.0]
st.shot('S11', 'grassland', setOpts={'clouds': 0, 'grass': '#C9BFA9'}, actors=[],
        props=[P('crateres', 'craterField', pos=[0.0, 0.06, 0.0], opts={'w': 34, 'd': 60, 'nx': 5, 'nz': 9, 'r': 1.7, 'home': HOME11, 'homeW': 2.2, 'fill': [r(RAIN11 + 0.25), r(FULL11 + 0.05)],
                 'pop': [0.02, 0.8], 'blocks': True, 'paris': True, 'trees': True, 'treeS': 0.42, 'clear': [EIF11[0], EIF11[2], 2.0], 'blockS': 2.6, 'roadW': 3.2, 'twinkle': 30, 'twinkleS': 2.2, 'ripples': True}),
               P('tour11', 'eiffelTower', pos=EIF11, opts={'h': 24, 'style': 'v2', 'color': '#8C8478', 'deck': '#6E675C'}),   # (round 3) grey-taupe like the street's (it was saturated brown)
               P('nuage11', 'rainCloud', pos=[-26.0, 0.0, 3.0], opts={'h': 26.0, 'size': 8.0, 'w': 9.0, 'n': 240, 'rain': [[r(RAIN11 - 0.1), True]], 'mood': 'happy'},
                 keys=[k(r(RAIN11 - 0.4), to=[30.0, 0.0, 1.0], dur=r(FULL11 - RAIN11 + 1.2), ease='linear')])],
        cams=[cam(0.0, [0.0, 56.0, 26.0], [0.0, 56.0, 26.0], [0.0, 0.0, -8.0], [0.0, 0.0, -8.0], lens=50)])
st.cue('thunder', 'S11', 0.05, 0.3); st.cue('sfx:crunch', 'S11', 0.3, 0.25); st.cue('rain', 'S11', RAIN11, 0.4, round(FULL11 - RAIN11 + 0.6, 2))   # (final) rain needs its duration, mix.py failed without it; st.cue('sfx:ding', 'S11', r(FULL11 + 0.1), 0.2)

# 12: the minister ordered... Close on the minister at the podium: he signs the order form, an open sheet flat on the podium, pen on paper: three
#     quick strokes, then a big flourish (round 1: his head is whole in the frame; no microphones in front of the sheet; a thin roll at the edge)
D12 = st.dur('S12'); MIN = [0.0, 0, -2.45]; PODTOP = [0.0, 1.152, -2.15]
FORM_PATH = [[0, 0, -0.1], [0, 0, 0.42], [0, -1.137, 0.47], [1.2, -1.137, 1.0], [2.0, -1.137, -0.3], [2.0, -1.137, -1.6], [2.0, -1.137, -2.6]]
SIGN = lambda t_, p_, d_=0.08: k(t_, toon={'reach': {'R': [*p_, 1, 0.12], 'L': [0.2, 1.17, -2.05, 1, 0.04]}, 'hands': {'R': 'pinch', 'L': 'open'}, 'bend': {'spine': [0.18, 0, 0, 1, None]}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.2}}, toonDur=d_, toonEase='inOut')
st.shot('S12', 'pressRoom', setOpts={**PRESS, 'podium': False}, actors=[
        act('ministre', MIN, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[0.0, 1.15, -2.0]), SIGN(0.0, [-0.1, 1.17, -2.02], 0.0), SIGN(0.15, [0.0, 1.165, -1.98]), SIGN(0.3, [-0.07, 1.165, -1.96]),
            SIGN(0.45, [0.04, 1.165, -1.96]),
            k(0.62, toon={'reach': {'R': [0.3, 1.6, -1.95, 1, 0.03], 'L': [0.2, 1.17, -2.05, 1, 0.04]}, 'hands': {'R': 'pinch', 'L': 'open'}, 'bend': {'spine': [0.0, 0, 0, 1, None]}, 'sq': [0.96, 1.06, 0.96], 'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.3}}, toonDur=0.12, toonEase='out'),
            k(0.85, look='camera', lookDur=0.15)])],
        props=[P('pupitre', 'plainPodium', pos=[0.0, 0, -2.0]),
               P('bon', 'orderForm', pos=PODTOP, opts={'path': FORM_PATH, 'w': 0.5, 'unroll': [[0.0, 0.074]], 'rollR': 0.045}),
               P('stylo', 'pen', on={'actor': 'ministre', 'hand': 'R'})],
        cams=[cam(0.0, [0.3, 2.6, 0.2], [0.3, 2.58, 0.13], [0.0, 1.55, -2.2], [0.0, 1.55, -2.2], lens=56)])
st.cue('sfx:paper', 'S12', 0.1, 0.25); st.cue('sfx:squeak', 'S12', 0.62, 0.15)

# 13: ...three hundred submarines. On the press room, low and closer: the order form shoots off the podium, down its front, across the floor and out
#     through the open door, the roll bouncing once on the way; the minister's eyes follow it (round 1: the minister was tiny over empty floor; the
#     paper glowed; the roll stopped at the threshold)
D13 = st.dur('S13')
st.shot('S13', 'pressRoom', setOpts=PRESS, actors=[
        act('ministre', MIN, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[0.0, 0.3, -1.5]), k(0.4, look=[1.2, 0.0, -1.2], lookDur=0.25), k(0.85, look=[2.0, 0.3, -3.0], lookDur=0.2)])],
        props=[P('bon', 'orderForm', pos=PODTOP, opts={'path': FORM_PATH, 'w': 0.5, 'unroll': [[0.0, 0.074], [1.05, 1.0]], 'rollR': 0.06, 'hop': [0.42, 0.28, 0.3]}),
               P('porte13', 'openDoor', pos=[2.0, 0, -2.98], opts={'w': 0.95, 'h': 2.15})],
        cams=[cam(0.0, [1.0, 1.4, 3.0], [1.0, 1.38, 2.85], [1.0, 0.9, -2.2], [1.0, 0.9, -2.2], lens=56)])
st.cue('sfx:paper', 'S13', 0.05, 0.4); st.cue('whoosh', 'S13', 0.3, 0.3); st.cue('sfx:boing', 'S13', 0.42, 0.15)

# 14: one per puddle. Low in the street: three hundred periscopes shoot up at once, one out of every puddle down the road and the pavements, and on
#     one beat all their heads snap round to him (overshoot, settle); he stands three-quarter in the foreground beside his own puddle, the only one
#     without, and looks at us (round 1: the heads read as bollards and never turned; he was back-on; the puddle sat on the caption band)
D14 = st.dur('S14'); POP14 = 0.12; TURN14 = 0.5
#     (round 2) round periscope heads with a hood and a dark round lens with a glint, bigger, so the snap toward him reads (the square heads read as
#     parking meters); he stands three-quarter to us from the start, glances at them on the snap, then back to us
MAN14 = [7.95, 0, -1.0]
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[STAND([k(0.0, look='camera'), k(r(TURN14 + 0.04), look=[5.0, 1.4, -4.0], lookDur=0.08), k(0.8, look='camera', lookDur=0.1)], MAN14, -5)],
        props=[CASE(), PUDDLE(),
               P('periscopes', 'periscopeField', pos=[0.0, 0, 0.0], opts={'w': 18, 'd': 46, 'gap': 2.9, 'at': POP14, 'h': 1.35, 's': 2.1, 'headS': 1.35, 'color': '#A9B4BD', 'turnAt': [TURN14, MAN14[0], MAN14[2]], 'turnDur': 0.16, 'skip': [PUD[0], PUD[2], 1.8]})],
        cams=[cam(0.0, [9.4, 2.2, 6.5], [9.35, 2.2, 6.4], [3.8, -0.6, -12.0], [3.8, -0.6, -12.0], lens=46)])
st.cue('sfx:pop', 'S14', POP14, 0.4); st.cue('sfx:click', 'S14', TURN14, 0.3)

# 15: with the town on their backs. (round 3) Low, from outside the town, looking down its street: for 0.25 s the town stands as it was, him on
#     his patch in its street; it shudders and sinks a hand's breadth (anticipation), then rises 3.6 m in half a second, overshoots and settles: the
#     whole town (its Haussmann fronts, a clock belfry, the Eiffel tower behind) on a thin slab, carried on the conning towers of six real submarines
#     (the S04 model, the red band, bows toward the middle) that came up out of their puddles, white spray off their sides; under it, in a column of
#     sunlight that falls through his hole, he stands on his round of asphalt beside his puddle, tips his head right back and looks up, eyes popping,
#     holds, then looks at us; the camera pushes in during the hold. The ground is the brown of S18 (round 2: a thick slab like a ceiling, grey
#     capsules, grey balloons of spray, a lime lawn: it read as a man under a lifted board)
D15 = st.dur('S15'); LIFT15 = 0.35; BASE15 = 0.1
HOLE15 = [0.0, 5.0, 3.2]; PATCHY15 = 0.13
MAN15 = [0.3, r(PATCHY15 + 0.005), 5.6]; PUD15 = [-0.8, r(PATCHY15 + 0.012), 6.1]
SUBS15 = [[-3.9, 8.6, r(PI / 2)], [3.9, 8.6, r(-PI / 2)], [-3.9, -1.4, r(PI / 2)], [3.9, -1.4, r(-PI / 2)], [-3.9, -8.4, r(PI / 2)], [3.9, -8.4, r(-PI / 2)]]
UP15 = lambda t_, d_=0.1: k(t_, toon={'bend': {'neck': [-0.55, 0, 0, 1, None]}, 'sq': [0.97, 1.04, 0.97], 'face': {'pop': 0.3, 'lid': 0.0, 'brow': 0.7, 'mouth': 'O'}}, toonDur=d_)
st.shot('S15', 'grassland', setOpts={'clouds': 20, 'grass': '#B39A78'}, actors=[STAND([k(0.0, look='camera'),
                                                                  k(0.25, toon={'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.2, 'brow': 0.3, 'mouth': 'line'}}, toonDur=0.05),
                                                                  k(0.55, look=[0.3, 4.0, 4.8], lookDur=0.15), k(0.85, look=[0.3, 7.5, 4.9], lookDur=0.1), UP15(0.86),
                                                                  k(1.3, look='camera', lookDur=0.12), k(1.3, toon={'bend': {'neck': [0.0, 0, 0, 1, None]}, 'sq': [1, 1, 1], 'face': DEAD}, toonDur=0.12)], MAN15, 0)],
        props=[CASE(), PUDDLE('flaque15', PUD15),
               P('ville15', 'townLid', pos=[0.0, 0.0, 0.0], opts={'w': 20, 'd': 22, 't': 0.45, 'side': '#6E5A46', 'cap': '#6B5642', 'hole': HOLE15, 'patchR': 2.2, 'patchAt': [HOLE15[0], HOLE15[1]], 'patchY': PATCHY15,
                 'under': '#7A6248', 'underY': 0.05, 'baseY': BASE15, 'liftAt': LIFT15, 'lift': 3.6, 'dur': 0.5, 'sink': [0.1, 0.15, 0.05], 'roadX': 0.0, 'roadW': 3.0, 'blockAlign': 'road',
                 'block': 3.6, 'holeGap': 0.9, 'hMin': 5.0, 'hMax': 7.5, 'paris': True, 'subs': SUBS15, 'subLen': 5.5, 'shaft': {'r': 1.5, 'opacity': 0.3}, 'tower': [3.9, -8.7, 9, 1.3]}),
               P('tour15', 'eiffelTower', pos=[-26.0, 0.0, -150.0], opts={'h': 48, 'style': 'v2', 'color': '#8C8478', 'deck': '#6E675C'})],
        fx=[{'type': 'shake', 'at': 0.25, 'dur': 0.55, 'amount': 0.012}],
        cams=[cam(0.0, [1.6, 2.8, 30.0], [1.6, 2.8, 30.0], [0.0, 3.4, 3.0], [0.0, 3.4, 3.0], lens=54),
              cam(0.85, [1.6, 2.8, 30.0], [1.0, 2.2, 18.0], [0.0, 3.4, 3.0], [0.25, 2.6, 5.0], lens=54, ease='inOut')])
st.cue('thunder', 'S15', 0.25, 0.4); st.cue('sfx:splash', 'S15', r(LIFT15 + 0.05), 0.45)

# 16: they parked it in the harbour. (round 2) One shot from the quay, a little above it: in front of us at the quay's edge a gendarme in a kepi,
#     big in the frame, kneels with his arm stretched across a band of open water to the town hall's door, which floats low at the edge of the town
#     (grey hull bows at the waterline under it); the white ticket slides under the door and stays there; he pops back up, turns to us and taps his
#     kepi; a sagging hemp rope runs from the squat bollard beside us up to the town hall's clock belfry (round 1: a wide then a close shot, the
#     ticket only in the wide one, the bollard a black top hat, no water under the door)
#     (round 3) a black cast-iron mushroom bollard (the grey dome read as a giant kepi); the rope sags in a visible curve all the way up to the front of
#     the belfry; a big lit white ticket held at the door for 0.2 s before it slides under; a squat before he pops up; a higher camera so his head sits
#     under the MAIRIE sign (it hid the M); a small boat in the channel by the door (a harbour cue)
D16 = st.dur('S16'); TICK16 = 0.36; UP16 = 0.56
FY16 = 0.6; TOWN16 = [2.6, 0, -13.85]; THP = [-2.0, 10.7]; THD = 4.5; BH16, BW16 = 2.2, 1.4; TOWER16 = [THP[0], r(THP[1] + THD / 2 - BW16 / 2), BH16, BW16]; TOWERY16 = 3.2   # (round 2) the belfry flush with the front: set back, the rope ran behind the facade
QUAY = [0.0, 0, 1.0]; BX16 = 2.3; QH16 = 0.6
DOORX = r(TOWN16[0] + THP[0]); DOORZ = r(TOWN16[2] + THP[1] + THD / 2 + 0.06); DOORY = r(FY16 + 0.3)
GEND = [1.0, QH16, 1.3]; GEND2 = [1.5, QH16, 1.35]
ROPE_TO = [r(TOWN16[0] + TOWER16[0] - QUAY[0]), r(FY16 + TOWERY16 + BH16 * 0.45), r(TOWN16[2] + TOWER16[1] + BW16 / 2 + 0.12 - QUAY[2])]   # (round 3) on the belfry's front
TK = lambda t_, p_, sp=0.0, sq=(1, 1, 1), face=None, d_=0.15, hand='pinch': k(t_, toon={'reach': {'R': [*p_, 1, 0.03]}, 'hands': {'R': hand}, 'bend': {'spine': [sp, 0, 0, 1, None]}, 'sq': list(sq), 'face': face or DEAD}, toonDur=d_, toonEase='inOut')
st.shot('S16', 'seaSurface', setOpts={'parasols': False, 'shore': 40}, actors=[
        act('gendarme', GEND, 180, 'kneel', 'unimpressed', keys=[k(0.0, look=[DOORX, DOORY, DOORZ]),
            TK(0.0, [r(DOORX + 0.25), r(DOORY + 0.12), r(DOORZ + 0.35)], 0.55, d_=0.0),
            TK(0.12, [r(DOORX + 0.08), r(DOORY + 0.12), r(DOORZ + 0.1)], 0.6, d_=0.12),
            TK(0.24, [r(DOORX + 0.06), r(DOORY + 0.1), r(DOORZ + 0.08)], 0.6, d_=0.1),
            TK(TICK16, [DOORX, r(DOORY + 0.02), r(DOORZ - 0.02)], 0.62, d_=0.06),
            TK(0.46, [1.2, r(QH16 + 0.9), 0.9], 0.3, (1.12, 0.86, 1.12), {'lid': 0.4, 'mouth': 'line', 'brow': -0.2}, 0.08, 'open'),   # (round 3) the squat before the pop
            TK(r(UP16 + 0.02), [1.7, r(QH16 + 1.4), 1.0], 0.0, (0.9, 1.14, 0.9), {'lid': 0.3, 'mouth': 'smile', 'brow': 0.2}, 0.08, 'open'),
            k(UP16, clip='stand', blend=0.1),
            k(r(UP16 + 0.1), to=GEND2, dur=0.14, glide=True, ease='out', face=30), k(r(UP16 + 0.14), look='camera', lookDur=0.1),
            k(0.86, toon={'touch': {'R': ['face', -0.15, 0.98, 0.1, 1, 0.0]}, 'hands': {'R': 'open'}, 'bend': {'spine': [0, 0, 0, 1, None]}, 'sq': [1, 1, 1], 'face': {'lid': 0.35, 'mouth': 'smile', 'brow': 0.1}}, toonDur=0.08),
            k(0.98, toon={'touch': {'R': ['face', -0.15, 1.04, 0.12, 1, 0.0]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.4, 'mouth': 'smile', 'brow': 0.2}}, toonDur=0.06),
            k(1.08, toon={'touch': {'R': ['face', -0.15, 0.98, 0.1, 1, 0.0]}, 'hands': {'R': 'open'}}, toonDur=0.06)])],
        props=[P('quai', 'harbourQuay', pos=QUAY, opts={'len': 40, 'h': QH16, 'dep': 16, 'bxs': [-3.0, BX16], 'bollardS': 1.25, 'bollardStyle': 'mushroom', 'rope': {'to': ROPE_TO, 'sag': 1.8, 'r': 0.05, 'loopR': 0.1}}),   # (round 3) the rope comes in from a bollard off the left edge and sags across the picture up to the belfry (from the near bollard it ran along the view and read as a stiff pole); the near bollard stands free
               P('bateau16', 'harbourBoat', pos=[r(DOORX + 1.6), 0.0, r(DOORZ + 0.95)], ry=8, opts={'s': 0.42}),
               P('ville16', 'townLid', pos=TOWN16, opts={'w': 40, 'd': 26, 'float': True, 'floatY': FY16, 'bob': 0.012, 'townHall': True, 'thPos': THP, 'thW': 9, 'thH': TOWERY16, 'thD': THD, 'thDoor': {'w': 0.95, 'h': 1.9},
                 'roadX': 12.0, 'hullL': 7, 'hullGap': 5, 'noseOut': 0.9, 'tower': TOWER16, 'towerY': TOWERY16, 'hMin': 8, 'hMax': 13, 'paris': True, 'block': 9}),
               P('pv', 'bigTicket', on={'actor': 'gendarme', 'hand': 'R'}, opts={'w': 0.5},   # (round 3) a big lit white card, held at the door, then slid under it flat
                 keys=[k(r(TICK16 + 0.02), detach=True, worldRot=[r(-PI / 2), 0.0, 0.15]), k(r(TICK16 + 0.03), to=[DOORX, r(DOORY + 0.012), r(DOORZ - 0.2)], dur=0.12, ease='out')]),
               P('kepi16', 'kepi', on={'actor': 'gendarme', 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'w': 0.222, 'd': 0.17})],
        cams=[cam(0.0, [-0.6, 4.6, 6.4], [-0.55, 4.55, 6.2], [1.0, 1.6, -1.0], [1.0, 1.65, -1.0], lens=70)])   # (round 3) from the left and higher: the rope crosses the picture, his head under the sign
st.cue('sfx:wind', 'S16', 0.0, 0.2); st.cue('sfx:paper', 'S16', TICK16, 0.3); st.cue('sfx:honkLong', 'S16', 0.1, 0.2); st.cue('sfx:boing', 'S16', UP16, 0.15)

# 17: officially, the town moved. Press room, at the wall map, three-quarter front: standing beside the map, the minister stretches one arm across it,
#     puts a finger on the town's icon and slides it from inland to the coast, leaving a dotted trail (DÉMÉNAGÉE), then turns to us, chin up, his
#     finger still on the coast (round 1: he was back-on, black arm on black suit, and never turned)
D17 = st.dur('S17'); SL17 = [0.35, 1.15]
MAPC = [0.6, 1.7, -2.93]; MW, MH = 1.5, 1.05
ICON0 = [r(MAPC[0] + (0.72 - 0.5) * MW), r(MAPC[1] + (0.5 - 0.42) * MH), -2.87]; ICON1 = [r(MAPC[0] + (0.2 - 0.5) * MW), r(MAPC[1] + (0.5 - 0.55) * MH), -2.87]
SLIDE = lambda t_, p_, d_, face=None, sq=(1, 1, 1): k(t_, toon={'reach': {'R': [*p_, 1, 0.06]}, 'hands': {'R': 'point'}, 'sq': list(sq), 'face': face or {'lid': 0.35, 'mouth': 'line', 'brow': -0.1}}, toonDur=d_, toonEase='inOut')
st.shot('S17', 'pressRoom', setOpts={**PRESS, 'podium': False}, actors=[
        act('ministre', [1.75, 0, -2.45], -35, 'stand', 'unimpressed', keys=[k(0.0, look=[0.9, 1.75, -2.9]), SLIDE(0.0, [1.3, 1.5, -2.6], 0.0), SLIDE(0.2, ICON0, 0.15),
            SLIDE(SL17[0], ICON0, 0.05), SLIDE(SL17[1], ICON1, r(SL17[1] - SL17[0])), k(0.4, look=[0.3, 1.7, -2.9], lookDur=0.6),
            k(1.35, look=[2.4, 2.3, 1.4], lookDur=0.12), SLIDE(1.35, ICON1, 0.1, {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}, (0.97, 1.05, 0.97))])],
        props=[P('carte17', 'townMapWall', pos=MAPC, opts={'w': MW, 'h': MH, 'from': [0.72, 0.42], 'to': [0.2, 0.55], 'slide': SL17})],
        cams=[cam(0.0, [2.6, 1.7, 1.5], [2.55, 1.7, 1.35], [1.25, 1.55, -2.6], [1.25, 1.55, -2.6], lens=48)])   # (round 2) aimed further right: his face was half cut by the edge
st.cue('sfx:squeak', 'S17', SL17[0], 0.15); st.cue('thud', 'S17', 1.25, 0.3)

# 18: not him. High and wide: where the town stood, a bare brown plain with rows of empty pits; in the middle, alone on his little round patch of
#     pavement, he stands with his briefcase beside his puddle; a slow push in; dust drifts across; he breathes, blinks, and slowly tilts his head up
#     to us (round 1: it was a still)
D18 = st.dur('S18'); PLY = 0.3; PY = r(PLY + 0.14)   # (round 2) the plain 30 cm up (at 8 cm the grassland showed through it for a frame, twice in S19)
PUD18 = [0.1, PY, 0.6]
BL = lambda t_: [k(t_, toon={'face': {'lid': 1.0, 'mouth': 'line'}}, toonDur=0.05), k(r(t_ + 0.09), toon={'face': DEAD}, toonDur=0.07)]
st.shot('S18', 'grassland', setOpts={'clouds': 30, 'grass': '#B39A78'}, actors=[STAND([k(0.0, look=[0.2, 0.3, 0.8]), *BL(0.3), k(0.45, look='camera', lookDur=0.7),
                                                                                      k(0.7, toon={'sq': [1.02, 0.98, 1.02]}, toonDur=0.3), k(1.0, toon={'sq': [0.99, 1.02, 0.99]}, toonDur=0.3), *BL(1.05)], [0.0, PY, -0.25], 10)],
        props=[CASE(), PUDDLE('flaque18', PUD18), P('plaine', 'barePlain', pos=[0.0, PLY, 0.0], opts={'r': 95, 'patch': 2.6}),
               *[P(f'vent18{j}', 'softDust', pos=[x_, PLY, z_], opts={'n': 5, 'size': 1.6, 'opacity': 0.32, 'life': 2.0, 'drift': [2.2, 0.3], 'spread': 3.0, 'color': '#E6D6B8'})
                 for j, (x_, z_) in enumerate([(-6.0, 3.0), (-8.0, -2.0), (-4.0, 6.0)])]],   # (round 3) soft see-through dust (the toon puffs read as beige eggs)
        cams=[cam(0.0, [6.5, 9.5, 13.0], [5.6, 8.4, 11.4], [0.0, 0.4, 0.0], [0.0, 0.5, 0.0], lens=40)])
st.cue('sfx:wind', 'S18', 0.0, 0.35)

# 19: nor the puddle. Framed exactly like the first shot, on his patch in the empty plain: briefcase in hand, he walks straight into the same puddle,
#     water splashing up the same (still dark) trouser leg; he stops, looks down at it, then at us, face unchanged
D19 = st.dur('S19'); STEP19 = 0.8
MAN19_0 = add(PUD18, [-0.1, 0.0, -1.55]); MAN19_P = add(PUD18, [-0.1, 0.0, -0.2])
C19 = cam(0.0, add(PUD18, OFF1), add(PUD18, [OFF1[0] + 0.02, OFF1[1] - 0.01, OFF1[2] - 0.07]), add(PUD18, OFFL1), add(PUD18, OFFL1), lens=54)
st.shot('S19', 'grassland', setOpts={'clouds': 30, 'grass': '#B39A78'}, actors=[STAND(walk_in(0.05, 0.75, MAN19_0, MAN19_P, STEP19, add(PUD18, [-0.4, 1.4, 2.0]), lk=(0.1, 0.5)), MAN19_0)],
        props=[CASE(), PUDDLE('flaque19', PUD18, splash=[STEP19], splashDir=[0.1, 0.2], ripple=[STEP19, r(STEP19 + 0.25)]), WET('gouttes19'), WETSHIN('mouille19'),
               P('plaine', 'barePlain', pos=[0.0, PLY, 0.0], opts={'r': 95, 'patch': 2.6})],
        cams=[C19])
st.cue('sfx:stepRun', 'S19', 0.1, 0.12); st.cue('sfx:splash', 'S19', STEP19, 0.45); st.cue('sfx:sting', 'S19', r(STEP19 + 0.4), 0.25)

MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': {'breathe': 1.7, 'holdLife': 1.6}}
st.write("La flaque", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'marin': {'preset': 'cop', 'seed': 821, 'hat': 'none', 'suit': '#1E2A44', 'lapel': '#1E2A44', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'general': {'preset': 'politique', 'seed': 822, 'suit': '#4F6380', 'lapel': '#4F6380', 'tie': '#25324A', 'glasses': False, 'facial': 'mustache', 'hairColor': '#9A9A96', 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.12}, 'toon': EX},
    'ministre': {'preset': 'politique', 'seed': 823, 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#B5302A', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'gendarme': {'preset': 'cop', 'seed': 824, 'hat': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
})
