#!/usr/bin/env python3
"""La statue (story 44, cycle 7 of the cartoon staging): this man was waiting for the bus. A pigeon landed on his head. He did not dare move. After
three hours the town hall listed him as a historic monument. Moving damages the heritage. They gave him a plaque. And railings. The tourists queue for
the photo. On Sundays he is cleaned with a jet. He blinked. Fined for vandalism. Yesterday the pigeon left. Without the pigeon the work is incomplete.
They moved him to a roundabout. The bus goes past every morning. It does not stop.
Staging: he is frozen from the moment the pigeon lands (clip stiffStand, the head a little squashed under its weight), and every gag is what is done to
a man who must not move: the creeping hand, the plinth slid under him, the railings that slam round him, the camera flash, the jet in the face (the
pigeon dry under its umbrella), the slow blink, the fine stuck on his forehead, the head that springs back when the weight leaves, the crane that lifts
him stiff as a post, the wind of the bus; and the last pigeon.
Pass 2 (review 1: animation 6.0, art 6.8): the railings stay put after S08; the fine is stuck on his forehead and follows the head, and every label
stays on him to the end (MONUMENT HISTORIQUE, AMENDE, INCOMPLETE across his chest like a sash); the official's sash reads; the cast turn three-quarter
to the camera; the pigeon rides side-on on top of his head (it was sunk into the skull, a grey dome); the landing flattens his head to half; the
workmen's arms carry the lift; a queue for the selfie, a white flash and a cut-in on his pupils; the jet shoots out and his eyes stay open; a slow
blink that fights; a boing to 140 %; the sling goes under his arms; the bus passes between us and him and his eyes follow it on stalks; the last
pigeon flattens him in a close-up.
Pass 3 (review 2: animation 7.0, art 7.4): the frozen man no longer shifts his weight (`hip: 0` in every frozen state: the automatic idle shift slid
him 7 cm, 70 px in the close-up); his resting face is worried, not a smirk; the fine sits above his brows (it hid an eye to the end); wide eyes with
pinpoint pupils for the flash and the jet; a blink that fights in three beats, then the uh-oh held; the supporting cast keeps moving (a queue that
shuffles, a phone raised into the flash, a real wag, a guilty hand creeping down, workmen dusting off, an officer who scribbles, a loupe that scans and
a tut-tut); the reaches vary (the officer's arm snakes over the railing); the jet splashes; the crane swings; the hook has a spreader bar, the straps go
under his arms; the last landing is new: the head goes flatter and the INCOMPLETE band pops off (the work is complete again)."""
from story_kit import *
import math

st = Story('statue', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 5), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L03', 5), ('S06', 'L04', 0), ('S07', 'L05', 0), ('S08', 'L05', 6),
         ('S09', 'L06', 0), ('S10', 'L07', 0), ('S11', 'L08', 0), ('S12', 'L08', 5), ('S13', 'L09', 0), ('S14', 'L10', 0), ('S15', 'L11', 0), ('S16', 'L12', 0),
         ('S17', 'L13', 0)])

STREET = {'clear': [-80, 80], 'eiffel': False, 'paveW': 6.5}
HX, HZ, HRY = 6.35, 0.0, -90                        # where he waits: on the right-hand pavement, facing the road (-X), the bus shelter behind him
TOP = 2.2                                            # the top of his head (a man of the series is 2.2 m to the top of his tuft)
HJ, HH = 1.77, 0.5                                   # (pass 2) his head joint above his feet, the height of his head: the top of the skull at HJ + HH
SQY = 0.92                                           # his head under the bird: 92 % of its height
PED = 0.9                                            # the height of the plinth they put under him
SHELTER = lambda: P('shelter', 'busStop', pos=[7.75, 0, 0.0], ry=-90)
BUSSIGN = [7.32, 2.45, 1.55]                         # the BUS sign of the shelter (its pole at the end toward +Z)
# (pass 2) the pigeon rides ON TOP of the skull (at 0.34 it was sunk 16 cm into it: a grey dome), side-on (an attached prop ignores its ry: rot)
PIG_ON = {'actor': 'mec', 'joint': 'head', 'offset': [0.0, round(HH - 0.035, 3), -0.01], 'rot': [0, -math.pi / 2, 0]}   # (final pass) seated on the crown, no gap
SQ = {'scl': {'head': [1.07, SQY, 1.07]}, 'hip': 0}  # his head, a little squashed under the bird; (pass 3) hip 0: a statue does not shift its weight (the idle shift slid him 7 cm)
FROZEN = lambda **kw: {**SQ, **kw}
UPCAM = lambda t, frm, pts, top=0.16, bottom=0.8, drift=(0.0, 0.0, 0.0), lenses=range(26, 66): _fitcam(t, frm, pts, top, bottom, drift, lenses)
def _fitcam(t, frm, pts, top, bottom, drift, lenses):
    look, lens, _ = fit(list(frm), pts, top=top, bottom=bottom, lenses=lenses)
    if lens is None:   # (pass 2) back away along the same angle until a lens fits (story_kit.fitBack)
        frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses)
        if lens is None: raise SystemExit(f'no lens fits from {frm}')
    return cam(t, list(frm), [round(frm[i] + drift[i], 3) for i in range(3)], look, [round(look[i] + drift[i], 3) for i in range(3)], lens=lens)
HEADP = lambda y0=0.0: [HX, TOP + y0, HZ]; FEETP = lambda y0=0.0: [HX, y0, HZ]
PIGEON = lambda keys=None, **o: P('pigeon', 'pigeon', on=PIG_ON, opts={'ph': 0.4, 'big': True, 'headYaw': 0.5, **o}, **({'keys': keys} if keys else {}))   # (pass 3) a bigger head turned a little to us (close up it read as a grey slab)
HIM = lambda y0=0.0, clip='stiffStand', expr='worried', extra=(), **kw: act('mec', [HX, y0, HZ], HRY, clip, expr, keys=[k(0.0, look=None), k(0.0, toon=FROZEN(), toonDur=0.0), *extra], **{'blink': 0, **kw})   # (final pass) no automatic blink until the one he is fined for
# (pass 2) every label stays on him to the end: the sticker on his chest, the fine on his forehead (stuck to the head: it follows the boing and the crane),
# INCOMPLETE across his chest like a sash
STICK = lambda t0: P('sticker', 'paperSheet', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.06, 0.38, 0.17]}, opts={'w': 0.26, 'h': 0.16, 'big': 'MONUMENT', 'bigSize': 0.34, 'lines': ['HISTORIQUE'], 'lineSize': 0.2, 'top': 0.12, 'paper': '#F4F1E8', 'bright': True},
                     keys=[k(0.0, scale=0.01, dur=0.0), k(t0, scale=1.0, dur=0.08, ease='outBack')])
FINE = lambda t0: P('fine', 'paperSheet', on={'actor': 'mec', 'joint': 'head', 'offset': [0.035, 0.475, 0.1], 'rot': [0, 0, 0.3]}, opts={'w': 0.19, 'h': 0.12, 'head': 'AMENDE', 'headSize': 0.2, 'lines': ['VANDALISME'], 'lineSize': 0.17, 'lineBold': True, 'lineInk': '#9A1520', 'top': 0.2, 'paper': '#F7E9B5', 'bright': True},   # (pass 3) on the hairline, above the brows
                    keys=[k(0.0, scale=0.01, dur=0.0), k(t0, scale=1.0, dur=0.05, ease='outBack')])
INCOMP = lambda t0: P('incomp', 'paperSheet', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.33, 0.2], 'rot': [0, 0, -0.5]}, opts={'w': 0.5, 'h': 0.13, 'big': 'INCOMPLÈTE', 'bigSize': 0.6, 'top': 0.14, 'paper': '#F4F1E8', 'bigInk': '#C8202A', 'bright': True},
                      keys=[k(0.0, scale=0.01, dur=0.0), k(t0, scale=1.0, dur=0.07, ease='outBack')])
PLINTH = lambda: P('plinth', 'pedestal', pos=[HX, 0, HZ], ry=-90, opts={'h': PED, 'w': 0.7, 'text': 'MONUMENT HISTORIQUE'})

# 1: the hook. The bus shelter, from across the road: he waits, a look at his watch, a foot that taps; a pigeon comes down out of the sky on an arc,
#    wings beating; a look down the street (no bus), and back to the front
D1 = st.dur('S01')
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [HX, 0, HZ], HRY, 'checkWatch', 'unimpressed', keys=[k(0.0, look=None),
            *[x for i in range(4) for x in (k(round(0.1 + 0.3 * i, 3), toon={'bend': {'shinR': [0.45, 0, 0, 1, None]}}, toonDur=0.07), k(round(0.2 + 0.3 * i, 3), toon={}, toonDur=0.06))],
            k(0.88, clip='stand', blend=0.15), k(1.15, toon={'face': {'gx': -0.9, 'brow': 0.3}}, toonDur=0.06), k(1.35, toon={'face': {'gy': -0.7, 'brow': 0.5}}, toonDur=0.06)])],   # (pass 3) his eyes alone go down the street (no bus), then up
        props=[SHELTER(), P('pig1', 'pigeon', pos=[HX + 1.4, 5.6, HZ + 3.8], ry=-165, opts={'flap': [0, 9], 'big': True},
                            keys=[k(0.0, to=[HX + 0.6, 3.9, HZ + 1.0], dur=0.8, ease='in'), k(0.8, to=[HX + 0.1, 2.95, HZ + 0.25], dur=round(D1 - 0.8, 3), ease='out')])],   # a swoop, then a glide, aimed at his crown
        cams=[UPCAM(0.0, [1.6, 1.55, 2.4], [[HX, TOP + 0.85, HZ + 0.3], [HX, 0.0, HZ], [HX - 0.45, 1.0, HZ + 0.4], [HX + 0.4, 1.0, HZ - 0.4], [7.75, 2.5, 0.9]], top=0.1, bottom=0.76, drift=(0.12, 0, -0.08))])   # (pass 3) all of him, the shelter round him, his feet above the caption band
[st.cue('sfx:tick', 'S01', round(0.17 + 0.3 * i, 3), 0.18) for i in range(4)]

# 2: a pigeon landed on his head. Closer, face to us: it settles on his crown: his head flattens to half, eyes bulging, holds two frames, fills out past
#    round and settles a little flatter; his eyes roll up to it (the head does not turn: he must not move)
D2 = st.dur('S02'); LD2 = 0.42
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [HX, 0, HZ], HRY, 'stand', 'neutral', keys=[k(0.0, look=None),
            k(LD2, toon={'scl': {'head': [1.55, 0.5, 1.55]}, 'sq': [1.04, 0.95, 1.04], 'face': {'brow': 1, 'eye': 0.7}}, toonDur=0.03, toonEase='out'), k(LD2, expr='surprised'),   # it lands: flat to half
            k(round(LD2 + 0.1, 3), toon={'scl': {'head': [1.5, 0.53, 1.5]}, 'face': {'brow': 1, 'eye': 0.65}}, toonDur=0.07),                                                  # held
            k(round(LD2 + 0.17, 3), toon={'scl': {'head': [0.9, 1.16, 0.9]}, 'face': {'brow': 1, 'eye': 0.4}}, toonDur=0.07, toonEase='out'),                                 # past round
            k(round(LD2 + 0.27, 3), toon=FROZEN(face={'brow': 0.9, 'eye': 0.35}), toonDur=0.12, toonEase='outBack'),                                                           # a little flatter
            k(round(LD2 + 0.45, 3), toon=FROZEN(face={'gy': -0.95, 'brow': 0.9, 'eye': 0.35}), toonDur=0.1), k(round(LD2 + 0.45, 3), expr='worried'),                          # his eyes go up to it
            k(round(LD2 + 0.6, 3), clip='stiffStand', blend=0.2)])],
        props=[SHELTER(), P('pig1', 'pigeon', pos=[HX + 0.1, 2.95, HZ + 0.5], ry=-170, opts={'flap': [0, LD2], 'big': True}, keys=[k(0.0, to=[HX, HJ + HH, round(HZ - 0.01, 3)], dur=LD2, ease='in'), k(LD2, visible=False)]),   # (pass 3) fast into the head: the squash on contact
               PIGEON(flaps=[[LD2, round(LD2 + 0.22, 3)]], keys=[k(0.0, visible=False), k(LD2, visible=True), k(LD2, squash=[1.3, 0.65, 1.3], dur=0.3)])],   # it rides his head from the landing on, folding its wings
        cams=[UPCAM(0.0, [2.9, 2.6, 0.9], [[HX, TOP + 0.4, HZ], [HX, 1.35, HZ], [HX, TOP + 0.75, HZ + 0.4]], top=0.14, bottom=0.66, drift=(0.08, 0, -0.03))])   # (final pass) higher: the shelter's beam behind his face, the bird against the glass and the facade
st.cue('whoosh', 'S02', 0.0, 0.15, 0.4, 600, 2000); st.cue('sfx:bonk', 'S02', LD2, 0.35)

# 3: he did not dare move. Close on his face, from below (the pigeon against the facade, not the shelter's beam): stiff, trembling, a drop of sweat; only
#    his eyes go from side to side; up there the pigeon fluffs up and dozes
D3 = st.dur('S03')
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[
        HIM(extra=[k(0.0, toon=FROZEN(tremble=1, face={'sweat': 1, 'brow': 0.6}), toonDur=0.0),
                   k(0.3, toon=FROZEN(tremble=1, face={'sweat': 1, 'brow': 0.6, 'gx': -0.85}), toonDur=0.08), k(0.65, toon=FROZEN(tremble=1, face={'sweat': 1, 'brow': 0.6, 'gx': 0.85}), toonDur=0.08),
                   k(1.0, toon=FROZEN(tremble=1, face={'sweat': 1, 'brow': 0.6, 'gy': -0.9}), toonDur=0.08)], expr='worried')],
        props=[SHELTER(), PIGEON(sleep=True)],
        cams=[UPCAM(0.0, [4.55, 1.35, 0.5], [[HX, HJ + HH + 0.3, HZ], [HX, 1.6, HZ]], top=0.12, bottom=0.66, drift=(0.06, 0, -0.02))])

# 4: after three hours. Wide, from across the road: buses go by between us and him, fast, one after the other; he has not moved; nor has the bird
D4 = st.dur('S04')
BUS = lambda pid, t0, dur=0.5, x=3.1: P(pid, 'cityBus', pos=[x, 0, -14.0], ry=-90, keys=[k(t0, to=[x, 0, 14.0], dur=dur, ease='linear')])   # (seen: 28 m in half a second; at 68 m in 0.38 s it was in no frame)
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[HIM()],
        props=[SHELTER(), PIGEON(sleep=True), BUS('bus1', 0.0), BUS('bus2', 0.52, x=2.6)],
        cams=[UPCAM(0.0, [-0.6, 1.5, 2.6], [[HX, TOP + 0.5, HZ], [HX, 0.0, HZ], [7.75, 2.6, -1.4], [7.75, 2.6, 1.4]], top=0.16, bottom=0.84)])
st.cue('whoosh', 'S04', 0.05, 0.4, 0.4, 150, 900); st.cue('whoosh', 'S04', 0.55, 0.4, 0.4, 150, 900)

# 5: the town hall listed him as a historic monument. An official in a tricolour sash comes along the pavement, turns three-quarter to us, looks him up
#    and down, and slaps a sticker on his chest: MONUMENT HISTORIQUE (the title card); the slap squashes him
D5 = st.dur('S05'); AR5, SL5 = 0.55, 1.05
OFF5 = [round(HX + 0.1, 3), 0, round(HZ + 1.05, 3)]   # beside him, at his left (in front of him, between him and us, he hid him)
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[HIM(extra=[k(SL5, toon=FROZEN(sq=[1.08, 0.9, 1.08], face={'eye': 0.45, 'brow': 0.9}), toonDur=0.03), k(round(SL5 + 0.08, 3), toon=FROZEN(sq=[0.97, 1.04, 0.97], face={'eye': 0.3, 'brow': 0.7}), toonDur=0.06),
                                                 k(round(SL5 + 0.16, 3), toon=FROZEN(face={'gy': 0.6, 'brow': 0.6}), toonDur=0.1)]),
        act('officiel', [round(HX - 0.3, 3), 0, round(HZ + 3.4, 3)], 180, 'stand', 'unimpressed', keys=[k(0.0, look='mec'), k(0.0, to=OFF5, dur=AR5, clip='walk', then='stand', ease='out', face=-125),   # three-quarter to us
            k(round(AR5 + 0.05, 3), look=[HX, 0.3, HZ]), k(round(AR5 + 0.3, 3), look=[HX, TOP + 0.3, HZ]),                                                    # he looks him up and down
            k(round(SL5 - 0.12, 3), toon={'reach': {'R': [round(HX - 0.17, 3), 1.45, round(HZ + 0.06, 3), 1, 0.06]}, 'hands': {'R': 'spread'}}, toonDur=0.12, toonEase='in'),   # the sticker: slap (pass 3: on the chest, not the mouth)
            k(round(SL5 + 0.25, 3), toon={}, toonDur=0.2), k(round(SL5 + 0.35, 3), look=[3.3, 1.7, 2.6]), k(round(SL5 + 0.35, 3), expr='smug')])],   # (pass 2) then a satisfied look to us
        props=[SHELTER(), PIGEON(sleep=True), STICK(SL5), P('clip', 'clipboardProp', on={'actor': 'officiel', 'hand': 'L', 'offset': [0, 0, 0.05]})],
        cams=[UPCAM(0.0, [3.3, 1.7, 2.6], [[HX, TOP + 0.45, HZ], [HX, 0.45, HZ], [OFF5[0], 2.3, OFF5[2]], [OFF5[0], 0.4, OFF5[2] + 0.3]], top=0.2, bottom=0.8, drift=(0.1, 0, -0.08))])
st.cue('sfx:stepSoft', 'S05', 0.15, 0.2); st.cue('sfx:stepSoft', 'S05', 0.4, 0.2); st.cue('sfx:paper', 'S05', SL5, 0.4); st.cue('thud', 'S05', SL5, 0.25)
st.card('S05', 'MONUMENT HISTORIQUE', at=st.at('S05', 'L03', 9))

# 6: moving damages the heritage. The official faces us, looking down the street; behind him an itch: the man's hand creeps up toward his nose, a
#    centimetre at a time; the official whips round: a blast of the whistle in his mouth (shock lines), a finger that wags; the hand freezes in mid-air
#    beside the nose, and creeps back down
D6 = st.dur('S06'); UP6, WH6, DN6 = 0.1, 1.05, 1.4
HANDL = lambda y, side=0.3, fwd=0.2: [round(HX - fwd, 3), y, round(HZ + side, 3)]   # his left hand (toward us), in open air beside his face
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        HIM(clip='stand', extra=[k(0.0, toon=FROZEN(face={'brow': 0.5, 'gy': 0.3}), toonDur=0.0),
            k(UP6, toon=FROZEN(reach={'L': [*HANDL(1.3, 0.3, 0.12), 1, 0.08]}, hands={'L': 'point'}, face={'brow': 0.6, 'gx': 0.4, 'gy': 0.5}), toonDur=0.4, toonEase='inOut'),   # creeping up
            k(0.6, toon=FROZEN(reach={'L': [*HANDL(1.72, 0.3, 0.18), 1, 0.08]}, hands={'L': 'point'}, face={'brow': 0.7, 'gx': 0.6, 'gy': 0.6}), toonDur=0.4, toonEase='inOut'),
            k(WH6, toon=FROZEN(reach={'L': [*HANDL(1.9, 0.28, 0.22), 1, 0.08]}, hands={'L': 'point'}, sq=[1.04, 0.96, 1.04], face={'brow': 1, 'eye': 0.6, 'gx': 0.8, 'pupil': 0.35}), toonDur=0.04), k(WH6, expr='shocked'),   # the whistle: frozen, (final pass) eyes wide, pinpoint pupils
            k(DN6, toon=FROZEN(reach={'L': [*HANDL(1.25, 0.3, 0.12), 1, 0.08]}, hands={'L': 'point'}, face={'brow': 0.8, 'eye': 0.4, 'gx': 0.6}), toonDur=0.6, toonEase='inOut'),   # (pass 3) slowly, guilty
            k(1.8, toon=FROZEN(face={'brow': 0.6, 'gx': 0.5}), toonDur=0.2)]),
        act('officiel', OFF5, -30, 'stand', 'unimpressed', keys=[k(0.0, look=[HX - 2.5, 1.6, HZ + 6.0]), k(round(WH6 - 0.12, 3), look='mec'), k(round(WH6 - 0.12, 3), face=-125, turn=0.1),
            k(WH6, clip='whistleBlow', blend=0.06), k(round(WH6 + 0.3, 3), clip='stand', blend=0.1), k(WH6, expr='angry'),
            *[k(round(WH6 + 0.35 + 0.1 * i, 3), toon={'hands': {'R': 'point'}, 'reach': {'R': [round(OFF5[0] - 0.2 + (-0.1 if i % 2 else 0.1), 3), 2.3, round(OFF5[2] + 0.05 + (0.14 if i % 2 else -0.14), 3), 1, 0.06]}, 'bend': {'neck': [0, 0, (0.12 if i % 2 else -0.12), 1, None]}}, toonDur=0.06) for i in range(5)]])],   # (pass 3) a real wag, the head with it
        props=[SHELTER(), PIGEON(sleep=True), STICK(0.0),
               P('whistle', 'whistle', on={'actor': 'officiel', 'joint': 'head', 'offset': [0.0, 0.11, 0.13], 'rot': [0, math.pi / 2, 0], 'scale': 2.2}, keys=[k(0.0, visible=False), k(WH6, visible=True), k(round(WH6 + 0.35, 3), visible=False)]),
               P('blast', 'burstLines', on={'actor': 'officiel', 'joint': 'head', 'offset': [0.0, 0.12, 0.2], 'face': 'camera'}, opts={'at': WH6, 'every': 0.1, 'until': round(WH6 + 0.2, 3), 'n': 7, 'r0': 0.1, 'r1': 0.34, 'len': 0.11, 'w': 0.02, 'dur': 0.2})],
        cams=[UPCAM(0.0, [3.6, 1.75, 2.1], [[HX, TOP + 0.45, HZ], [HX, 0.9, HZ], [OFF5[0], 2.3, OFF5[2]], HANDL(1.9, 0.4, 0.22)], top=0.2, bottom=0.72, drift=(0.12, 0, -0.06))])
st.cue('sfx:whistle', 'S06', WH6, 0.55)

# 7: they gave him a plaque. Two workmen, three-quarter to us, squat and grip him under the arms, heave him up stiff as a plank (he tips a little, his
#    eyes wide), hold him up there trembling while the stone plinth slides under; they let go: he drops onto it with a squash; the pigeon bounces and
#    flaps; his eyes go up to it
D7 = st.dur('S07'); LF7, UPT, DR7, ON7 = 0.22, 0.5, 0.86, 0.94
UP7, HOLD7 = 0.24, 0.16                     # how high his feet go (above the plinth top), and where they hang while it slides under
AP = 1.45                                   # his armpits above his feet
def WK7(side, dy, crouch=0.0, up=False):   # a workman's toon state: one hand under his armpit, one at his hip, `dy` the man's lift
    z = round(HZ + side * 0.2, 3)
    st_ = {'reach': {'L': [HX, round(AP + dy, 3), z, 1, 0.06], 'R': [HX, round(1.0 + dy, 3), round(HZ + side * 0.22, 3), 1, 0.06]}, 'hands': {'L': 'grip', 'R': 'grip'}}
    if crouch: st_['bend'] = {'spine': [crouch, 0, 0, 1, None]}; st_['sq'] = [1.05, 0.9, 1.05]
    if up: st_['bend'] = {'spine': [-0.12, 0, 0, 1, None]}; st_['sq'] = [0.96, 1.07, 0.96]; st_['face'] = {'cheeks': 1, 'vein': 1}; st_['tremble'] = 1
    return st_
def WORKMAN(wid, pos, ry, side):
    lift = lambda t: 0.0 if t < LF7 else (PED + UP7 if t < UPT else PED + HOLD7)
    return act(wid, pos, ry, 'stand', 'determined', keys=[k(0.0, look='mec'), k(0.0, toon=WK7(side, 0.0, crouch=0.35), toonDur=0.0),
        k(LF7, toon=WK7(side, PED + UP7, up=True), toonDur=round(UPT - LF7, 3), toonEase='out'),
        k(0.62, toon=WK7(side, PED + HOLD7 + 0.02, up=True), toonDur=0.12), k(0.74, toon=WK7(side, PED + HOLD7, up=True), toonDur=0.12),
        k(DR7, toon={'hands': {'L': 'spread', 'R': 'spread'}, 'bend': {'spine': [-0.1, 0, 0, 1, None]}}, toonDur=0.06), k(DR7, expr='relieved'),   # (final pass) they let go (an arm ran up his face)
        k(round(DR7 + 0.02, 3), to=[round(pos[0] + 0.25 * side * 0.0 - 0.28, 3), 0, round(pos[2] + 0.22 * side, 3)], dur=0.18, clip='walk', then='stand', ease='out', face='keep'),   # and step back
        *[k(round(ON7 + 0.12 + 0.09 * i, 3), toon=CLAP7(pos, ry, i % 2 == 0), toonDur=0.05) for i in range(4)], k(round(ON7 + 0.5, 3), toon={}, toonDur=0.2)])   # (pass 3) they dust off their hands
def CLAP7(pos, ry, shut):   # both hands in front of his chest, together or apart
    f = (math.sin(math.radians(ry)), math.cos(math.radians(ry))); l = (math.cos(math.radians(ry)), -math.sin(math.radians(ry))); w = 0.03 if shut else 0.16
    pt = lambda sd: [round(pos[0] + 0.32 * f[0] + sd * w * l[0], 3), 1.2, round(pos[2] + 0.32 * f[1] + sd * w * l[1], 3), 1, 0.05]
    return {'reach': {'L': pt(1), 'R': pt(-1)}, 'hands': {'L': 'flat', 'R': 'flat'}}
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[
        HIM(extra=[k(0.0, toon=FROZEN(face={'brow': 0.7, 'eye': 0.3}), toonDur=0.0),
                   k(LF7, to=[HX, PED + UP7, HZ], dur=round(UPT - LF7, 3), clip='stiffStand', then='stiffStand', glide=True, ease='out', face=HRY),
                   k(LF7, toon=FROZEN(lay=[0, 0.26], face={'brow': 1, 'eye': 0.55}), toonDur=0.25, toonEase='out'),                                   # up like a plank, tipping
                   k(UPT, to=[HX, PED + HOLD7, HZ], dur=round(DR7 - UPT, 3), clip='stiffStand', then='stiffStand', glide=True, ease='inOut', face=HRY),
                   k(0.62, toon=FROZEN(lay=[0, 0.2], face={'brow': 1, 'eye': 0.5, 'gx': -0.7}), toonDur=0.12), k(0.74, toon=FROZEN(lay=[0, 0.28], face={'brow': 1, 'eye': 0.5, 'gx': 0.7}), toonDur=0.12),
                   k(DR7, to=[HX, PED, HZ], dur=round(ON7 - DR7, 3), clip='stiffStand', then='stiffStand', glide=True, ease='in', face=HRY),
                   k(DR7, toon=FROZEN(lay=[0, 0.0], face={'brow': 1, 'eye': 0.5}), toonDur=round(ON7 - DR7, 3)),
                   k(ON7, toon=FROZEN(sq=[1.16, 0.82, 1.16], face={'eye': 0.6, 'brow': 1}), toonDur=0.03),                                         # he lands on it: squash
                   k(round(ON7 + 0.08, 3), toon=FROZEN(sq=[0.96, 1.05, 0.96]), toonDur=0.06), k(round(ON7 + 0.16, 3), toon=FROZEN(settle=0.6, face={'gy': -0.9, 'brow': 0.6}), toonDur=0.12)]),
        WORKMAN('ouvrier1', [round(HX + 0.08, 3), 0, round(HZ + 0.66, 3)], -118, 1), WORKMAN('ouvrier2', [round(HX + 0.08, 3), 0, round(HZ - 0.66, 3)], -30, -1)],
        props=[SHELTER(), PIGEON(sleep=True, flaps=[[LF7, round(LF7 + 0.3, 3)], [ON7, round(ON7 + 0.22, 3)]], keys=[k(ON7, squash=[1.3, 0.62, 1.3], dur=0.3)]), STICK(0.0),
               P('plinth', 'pedestal', pos=[HX + 1.6, 0, HZ], ry=-90, opts={'h': PED, 'w': 0.7, 'text': 'MONUMENT HISTORIQUE'}, keys=[k(0.45, to=[HX, 0, HZ], dur=0.3, ease='out')])],
        cams=[UPCAM(0.0, [2.9, 1.6, 2.2], [[HX, TOP + PED + 0.45, HZ], [HX, 0.0, HZ], [HX + 1.95, 0.0, HZ], [HX, 0.0, HZ + 0.9], [HX, 0.0, HZ - 0.9]], top=0.12, bottom=0.86, drift=(0.1, 0, -0.06))])
st.cue('sfx:grunt', 'S07', LF7, 0.3); st.cue('sfx:slideDown', 'S07', 0.45, 0.25); st.cue('thud', 'S07', ON7, 0.45); st.cue('sfx:flap', 'S07', ON7, 0.2)

# 8: and railings. Four lengths of railing drop out of the sky round the plinth and slam into the pavement, one after the other; only his eyes move
D8 = st.dur('S08'); RL = (0.06, 0.2, 0.34, 0.48)
RAIL = lambda i, t0, pos, ry: P(f'rail{i}', 'fence', pos=[pos[0], 4.5 if t0 is not None else 0, pos[1]], ry=ry, opts={'length': 1.9, 'height': 1.0, 'color': '#1E2228'},
                                **({'keys': [k(t0, to=[pos[0], 0, pos[1]], dur=0.1, ease='in'), k(t0 + 0.1, squash=[1.0, 0.8, 1.0], dur=0.2)]} if t0 is not None else {}))
# (pass 2) RAILS() is the railings at rest: with the default drop times of pass 1 the S08 drop played again at every later cut
RAILS = lambda t=(None, None, None, None): [RAIL(0, t[0], (HX - 0.95, HZ), 90), RAIL(1, t[1], (HX, HZ + 0.95), 0), RAIL(2, t[2], (HX + 0.95, HZ), 90), RAIL(3, t[3], (HX, HZ - 0.95), 0)]
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[HIM(y0=PED, extra=[*[k(round(t + 0.1, 3), toon=FROZEN(face={'gx': (-0.8 if i % 2 else 0.8), 'brow': 0.7, 'eye': 0.35}), toonDur=0.04) for i, t in enumerate(RL)]])],
        props=[SHELTER(), PIGEON(sleep=True), STICK(0.0), PLINTH(), *RAILS(RL)],
        fx=[{'type': 'shake', 'at': t + 0.1, 'dur': 0.08, 'amount': 0.008} for t in RL],
        cams=[UPCAM(0.0, [0.9, 2.1, 3.1], [[HX, TOP + PED + 0.45, HZ], [HX - 1.0, 0.0, HZ + 1.0], [HX + 1.0, 0.0, HZ - 1.0], [HX - 1.0, 0.0, HZ - 1.0]], top=0.12, bottom=0.86)])
[st.cue('clang', 'S08', round(t + 0.1, 3), 0.35) for t in RL]

# 9: the tourists queue for the photo. A queue along the railings, three-quarter to us; at its head a tourist with his back to the statue holds his phone
#    up at arm's length, grinning: the flash (white screen, two frames): cut in on his eyes: his pupils are dots, his eyes water
D9 = st.dur('S09'); FL9 = 0.95
T1 = [round(HX - 1.3, 3), 0, round(HZ + 0.45, 3)]; T1RY = -12
PHONE9 = [round(T1[0] - 0.17, 3), 2.5, round(T1[2] + 0.78, 3)]          # at arm's length, up, turned back at him: the selfie
QUEUE = [[round(HX - 1.45, 3), 0, round(HZ - 0.55, 3)], [round(HX - 1.5, 3), 0, round(HZ - 1.45, 3)], [round(HX - 1.42, 3), 0, round(HZ - 2.35, 3)], [round(HX - 1.52, 3), 0, round(HZ - 3.25, 3)]]
EYE9 = round(PED + HJ + 0.62 * HH * SQY, 3)
LOW9 = [round(T1[0] - 0.1, 3), 1.45, round(T1[2] + 0.42, 3)]                 # the phone held low, before he raises it
CRANE9 = lambda t0, d=0.3: [k(t0, toon={'bend': {'spine': [0, round(d, 2), 0, 1, None], 'neck': [-0.15, 0, 0, 1.1, None]}}, toonDur=0.15), k(round(t0 + 0.35, 3), toon={}, toonDur=0.2)]   # craning to see
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[HIM(y0=PED, extra=[k(round(FL9 - 0.1, 3), toon=FROZEN(face={'brow': 0.4, 'gx': 0.5}), toonDur=0.1),
            k(FL9, toon=FROZEN(sq=[1.03, 0.97, 1.03], face={'pupil': 0.3, 'brow': 1, 'eye': 0.55}), toonDur=0.03), k(FL9, expr='shocked'),   # (pass 3) wide eyes, pinpoint pupils
            k(round(FL9 + 0.25, 3), toon=FROZEN(face={'pupil': 0.32, 'brow': 0.9, 'eye': 0.5, 'tears': 1, 'pupilShake': 1}), toonDur=0.15)]),
        act('touriste1', T1, T1RY, 'stand', 'happy', keys=[k(0.0, look=LOW9), k(0.0, toon={'reach': {'R': [*LOW9, 1, 0.05]}, 'hands': {'R': 'grip'}}, toonDur=0.0),
            k(0.45, look=PHONE9), k(0.45, toon={'reach': {'R': [*PHONE9, 1, 0.05]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [-0.08, 0, 0, 1, None]}}, toonDur=0.22, toonEase='outBack'),   # (pass 3) up goes the phone
            k(round(FL9 - 0.25, 3), expr='bigGrin'), k(round(FL9 - 0.25, 3), toon={'reach': {'R': [PHONE9[0], round(PHONE9[1] + 0.05, 3), PHONE9[2], 1, 0.05]}, 'hands': {'R': 'grip'}, 'bend': {'neck': [-0.15, 0.12, 0, 1, None]}}, toonDur=0.15)]),   # the selfie face
        act('touriste2', QUEUE[0], 5, 'stand', 'unimpressed', keys=[k(0.0, look='touriste1'), *CRANE9(0.2, 0.3), k(0.7, look='mec')]),   # (pass 3) the queue shuffles and cranes
        act('touriste3', QUEUE[1], 0, 'readPhone', 'neutral', keys=[k(0.0, look=None), *CRANE9(0.5, -0.25)]),
        act('touriste4', QUEUE[2], 5, 'checkWatch', 'neutral', keys=[k(0.0, look=None), k(0.3, to=[QUEUE[2][0], 0, round(QUEUE[2][2] + 0.25, 3)], dur=0.3, clip='walk', then='checkWatch', ease='inOut')]),
        act('touriste5', QUEUE[3], -5, 'stand', 'happy', keys=[k(0.0, look='mec'), *CRANE9(0.1, -0.3), *CRANE9(0.8, 0.3)])],
        props=[SHELTER(), PIGEON(sleep=True), STICK(0.0), PLINTH(), *RAILS(),
               P('tphone', 'smartPhone', on={'actor': 'touriste1', 'hand': 'R', 'offset': [0, 0.02, 0.04]}, scale=2.1, opts={'case': '#E8504A'}),   # (pass 3) bigger, a bright case
               P('flash9', 'burstLines', pos=PHONE9, face='camera', opts={'at': FL9, 'n': 10, 'r0': 0.07, 'r1': 0.45, 'len': 0.18, 'w': 0.035, 'dur': 0.26, 'color': '#F2B230'})],   # (pass 3) yellow: white on the white flash vanished
        fx=[{'type': 'flash', 'at': FL9, 'dur': 0.08}],
        cams=[UPCAM(0.0, [round(HX - 1.75, 3), 1.9, round(HZ + 3.4, 3)], [[HX, PED + HJ + HH + 0.35, HZ], [HX, 0.3, HZ], [T1[0], 2.35, T1[2]], [T1[0], 0.0, T1[2]], PHONE9, [QUEUE[3][0], 2.2, QUEUE[3][2]]], top=0.1, bottom=0.84, drift=(0.06, 0, -0.08)),   # (pass 2) down the length of the queue
              cam(round(FL9 + 0.07, 3), [round(HX - 1.12, 3), EYE9, round(HZ + 0.12, 3)], [round(HX - 1.0, 3), EYE9, round(HZ + 0.1, 3)], [HX, round(EYE9 - 0.045, 3), HZ], [HX, round(EYE9 - 0.045, 3), HZ], lens=40)])   # cut in: his pupils; (final pass) the face higher, the mouth above the caption band
st.cue('sfx:cash', 'S09', FL9, 0.25)

# 10: on Sundays he is cleaned with a jet. A cleaner, three-quarter to us, aims a high-pressure lance at his face: the jet shoots out, his cheeks
#     ripple, his hair and tie blow back; his eyes stay WIDE open, streaming (he must not blink: that is the next shot); up there the pigeon sits dry
#     under a little umbrella
D10 = st.dur('S10'); JT10 = 0.3
CLN = [round(HX - 1.55, 3), 0, round(HZ - 1.2, 3)]; CRY = 25
_f = (math.sin(math.radians(CRY)), math.cos(math.radians(CRY)))
GRIP10 = [round(CLN[0] + 0.35 * _f[0], 3), 1.25, round(CLN[2] + 0.35 * _f[1], 3)]
FACE10 = [round(HX - 0.12, 3), round(PED + HJ + 0.27, 3), HZ]
_d = [FACE10[i] - GRIP10[i] for i in range(3)]; _hd = math.hypot(_d[0], _d[2]); _len = math.hypot(_hd, _d[1])
RY10 = round(math.degrees(math.atan2(_d[0], _d[2])), 2); PIT10 = round(-math.atan2(_d[1], _hd), 3)
_u = [x / _len for x in _d]; HANDL10 = [round(GRIP10[i] + 0.35 * _u[i], 3) for i in range(3)]
JET = round(_len - 0.75 - 0.06, 3)
_wl = [_u[2] * 1.6, 0.6, -_u[0] * 1.6]                # the jet's push in his own frame (+Z his front, +X his left): back and to his left
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[
        HIM(y0=PED, extra=[k(round(JT10 + 0.12, 3), expr='scared'), k(round(JT10 + 0.12, 3), toon=FROZEN(sq=[1.03, 0.97, 1.03], hairUp=0.6, wind=[round(_wl[0] * 0.5, 2), 0.3, round(_wl[2] * 0.5, 2)], face={'eye': 0.45, 'brow': 1, 'pupil': 0.5, 'mouth': 'wavy'}), toonDur=0.12),
            *[k(round(JT10 + 0.24 + 0.08 * i, 3), toon=FROZEN(hairUp=1, wind=[round(_wl[0], 2), _wl[1], round(_wl[2], 2)], face={'cheeks': (1 if i % 2 else 0.2), 'eye': 0.35, 'lid': 0.0, 'brow': 0.9, 'pupil': 0.45, 'tears': 1, 'pupilShake': 1, 'mouth': 'wavy'}, sq=[1.0 + (0.03 if i % 2 else -0.02), 1, 1]), toonDur=0.05) for i in range(17)]]),
        act('nettoyeur', CLN, CRY, 'stand', 'neutral', keys=[k(0.0, look=FACE10), k(0.0, toon={'reach': {'R': [*GRIP10, 1, 0.06], 'L': [*HANDL10, 1, 0.06]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [-0.08, 0, 0, 1, None]}}, toonDur=0.0),
            k(JT10, toon={'reach': {'R': [*GRIP10, 1, 0.06], 'L': [*HANDL10, 1, 0.06]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [-0.16, 0, 0, 1, None]}, 'lay': [-0.08, 0]}, toonDur=0.08),   # the kick of it
            *[k(round(JT10 + 0.1 + 0.07 * i, 3), toon={'reach': {'R': [*GRIP10, 1, 0.06], 'L': [*HANDL10, 1, 0.06]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [-0.16 + (0.04 if i % 2 else -0.03), 0, 0, 1, None]}, 'lay': [-0.06 + (0.03 if i % 2 else -0.02), 0]}, toonDur=0.05) for i in range(16)]])],   # (final pass) braced, shaken by the recoil
        props=[SHELTER(), PIGEON(sleep=True), STICK(0.0), PLINTH(), *RAILS(),
               P('lance', 'waterJet', pos=GRIP10, ry=RY10, rot=[PIT10, 0, 0], rotOrder='YXZ', opts={'lance': 0.75, 'len': JET, 'on': [JT10, 9.0], 'ramp': 0.15, 'splash': 3.0, 'color': '#8FD3F5', 'opacity': 0.92},   # (pass 3) water, not a light beam
                 keys=[k(round(JT10 + 0.1 + 0.07 * i, 3), rotTo=[round(PIT10 + (0.025 if i % 2 else -0.02), 4), math.radians(RY10) + (0.02 if i % 3 == 0 else -0.015), 0], dur=0.06) for i in range(16)]),   # (final pass) the jet wobbles with the recoil
               P('brolly', 'umbrella', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, HH, 0.06]}, scale=0.22, opts={'radius': 0.75, 'height': 1.0, 'colors': ['#E8504A', '#F4F1E8']})],
        cams=[UPCAM(0.0, [3.4, 2.7, 1.6], [[HX, PED + HJ + HH + 0.55, HZ], [HX, PED + 1.35, HZ], [CLN[0], 2.25, CLN[2]], [HANDL10[0], 1.15, HANDL10[2]]], top=0.12, bottom=0.66, drift=(0.06, 0, -0.03)),   # the cleaner and the jet
              UPCAM(0.85, [round(HX - 1.75, 3), round(PED + 2.05, 3), 0.55], [[HX, PED + HJ + HH + 0.5, HZ], [HX, PED + 1.55, HZ], [round(HX - 0.6, 3), round(PED + 1.9, 3), round(HZ - 0.3, 3)]], top=0.1, bottom=0.62, drift=(0.04, 0, -0.02))])   # (pass 2) close: his eyes wide open in the jet, the pigeon dry under its umbrella
st.cue('rain', 'S10', JT10, 0.35, round(D10 - JT10, 3))

# 11: he blinked. Very close on his eyes: the lids tremble and fight, then close heavily, with a clack, and open again: uh-oh
D11 = st.dur('S11'); BL11 = 0.03
FIGHT11 = [(0.0, 'sleepy'), (0.167, 'shocked'), (0.234, 'sleepy'), (0.4, 'shocked')]   # (final pass) droop 5 frames, snap wide 2, droop 5, snap 2   # (pass 3) droop, snap wide, droop again, snap: the painted faces themselves (lid values did not move these eyes)
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[
        HIM(y0=PED, expr='scared', extra=[k(0.0, toon=FROZEN(face={'brow': 0.7, 'eye': 0.3}), toonDur=0.0),
            *[x for i, (dt, ex) in enumerate(FIGHT11) for x in (k(round(BL11 + dt, 3), expr=ex), k(round(BL11 + dt, 3), toon=FROZEN(face={'brow': 0.9 + 0.1 * (i % 2), 'pupilShake': 1, 'sweat': 1}, sq=[1.0, 1.0 + 0.015 * (i % 2), 1.0]), toonDur=0.04))],   # (pass 3) the lids fight
            k(round(BL11 + 0.467, 3), expr='blink'), k(round(BL11 + 0.467, 3), toon=FROZEN(face={'brow': 0.4, 'sweat': 1}, sq=[1.02, 0.98, 1.02]), toonDur=0.08),           # and fall shut, heavy: held 9 frames
            k(round(BL11 + 0.767, 3), expr='scared'), k(round(BL11 + 0.767, 3), toon=FROZEN(face={'brow': 1, 'eye': 0.45, 'pupil': 0.6, 'mouth': 'wavy'}), toonDur=0.08, toonEase='out')])],   # open: uh-oh, held to the cut
        props=[SHELTER(), PIGEON(sleep=True), STICK(0.0), PLINTH(), *RAILS()],
        cams=[cam(0.0, [round(HX - 1.05, 3), PED + 1.97, round(HZ + 0.12, 3)], [round(HX - 0.98, 3), PED + 1.97, round(HZ + 0.11, 3)], [HX, PED + 1.95, HZ], [HX, PED + 1.95, HZ], lens=36)])
st.cue('clack', 'S11', round(BL11 + 0.5, 3), 0.6)

# 12: fined for vandalism. A policeman, three-quarter to us outside the railings, stretches his arm over them and slaps a fine on his forehead: AMENDE
#     VANDALISME, stuck there; his head jolts; his eyes go up to the paper
D12 = st.dur('S12'); SL12 = 0.45
COP = [round(HX - 0.45, 3), 0, round(HZ - 1.2, 3)]; FH12 = [round(HX - 0.16, 3), round(PED + HJ + 0.475 * SQY, 3), round(HZ + 0.035, 3)]   # (pass 3) where the fine sits now
_cf, _cr = (math.sin(math.radians(-13)), math.cos(math.radians(-13))), (-math.cos(math.radians(-13)), math.sin(math.radians(-13)))
CAP12 = [round(COP[0] + 0.13 * _cf[0] + 0.07 * _cr[0], 3), 2.28, round(COP[2] + 0.13 * _cf[1] + 0.07 * _cr[1], 3)]   # the peak of his cap
st.shot('S12', 'parisStreet', setOpts=STREET, actors=[
        HIM(y0=PED, blink=1, extra=[k(SL12, toon=FROZEN(bend={'neck': [-0.26, 0, 0, 1, None]}, face={'brow': 1, 'eye': 0.45}), toonDur=0.04), k(round(SL12 + 0.12, 3), toon=FROZEN(face={'gy': -0.95, 'brow': 0.8, 'gx': 0.1}), toonDur=0.1),
            k(round(SL12 + 0.5, 3), toon=FROZEN(face={'gy': -0.95, 'cross': 0.6, 'brow': 0.9}), toonDur=0.1)]),   # (pass 3) cross-eyed at the paper on his brow
        act('flic', COP, -13, 'stand', 'unimpressed', keys=[k(0.0, look=HEADP(PED - 0.2)),
            k(round(SL12 - 0.16, 3), toon={'reach': {'L': [*FH12, 1, 0.06]}, 'hands': {'L': 'spread'}, 'wave': {'armL': [0.07, 1.5, 0.0, 0, 0], 'foreL': [0.06, 1.0, 0.3, 0, 0]}}, toonDur=0.16, toonEase='in'),   # (pass 3) the arm snakes over the railing
            k(round(SL12 + 0.3, 3), toon={}, toonDur=0.15), k(round(SL12 + 0.45, 3), toon={'reach': {'R': [*CAP12, 1, 0.05]}, 'hands': {'R': 'flat'}}, toonDur=0.1),   # a tip of the cap
            k(round(SL12 + 0.7, 3), toon={}, toonDur=0.15), k(round(SL12 + 0.45, 3), expr='smug')])],
        props=[SHELTER(), PIGEON(sleep=True), STICK(0.0), PLINTH(), *RAILS(), FINE(SL12)],
        cams=[UPCAM(0.0, [3.4, 2.3, 1.1], [[HX, PED + HJ + HH + 0.45, HZ], [HX, PED + 1.0, HZ], [COP[0], 2.25, COP[2]], [COP[0], 0.9, COP[2]]], top=0.16, bottom=0.72, drift=(0.08, 0, -0.04))])
st.cue('sfx:splat', 'S12', SL12, 0.35); st.cue('sfx:paper', 'S12', round(SL12 + 0.02, 3), 0.3)

# 13: yesterday the pigeon left. Close: it wakes, beats its wings and takes off: his eyes follow it up; his head, free of the weight, shoots up to
#     140 % on a stretched neck (boing) and wobbles three times, the fine flapping on his forehead
D13 = st.dur('S13'); FLY13 = 0.4
BOING = [(0.02, [0.8, 1.42, 0.8], 1.5, 0.05), (0.1, [1.2, 0.8, 1.2], 0.8, 0.06), (0.17, [0.9, 1.18, 0.9], 1.2, 0.06), (0.24, [1.07, 0.93, 1.07], 0.92, 0.06), (0.31, [0.97, 1.04, 0.97], 1.04, 0.06)]
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[
        HIM(y0=PED, blink=1, extra=[k(round(FLY13 - 0.05, 3), toon=FROZEN(face={'gy': -0.9, 'brow': 0.5}), toonDur=0.08),
            *[k(round(FLY13 + dt, 3), toon={'scl': {'head': sc}, 'bend': {'neck': [0, 0, 0, nk, None]}, 'face': {'gy': -1, 'brow': 1, 'eye': 0.45}}, toonDur=d, toonEase='out') for dt, sc, nk, d in BOING],   # boing
            k(round(FLY13 + 0.4, 3), toon={'face': {'gy': -0.8, 'brow': 0.7}, 'settle': 0.4}, toonDur=0.12),
            k(0.95, toon={'face': {'gy': -0.9, 'gx': 0.65, 'brow': 0.6}}, toonDur=0.15),                                                         # (pass 3) his eyes follow it off
            k(1.25, toon={'face': {'gy': -0.3, 'gx': 0.1, 'brow': 0.1, 'mouth': 'wavy', 'cheeks': 0.6}, 'sq': [1.03, 0.95, 1.03]}, toonDur=0.25),   # a long sigh
            k(1.6, toon={'face': {'brow': 0.3}, 'sq': [1.0, 1.0, 1.0]}, toonDur=0.2)])],
        props=[SHELTER(), STICK(0.0), PLINTH(), *RAILS(), FINE(0.0),
               P('pig2', 'pigeon', pos=[HX, round(PED + HJ + HH * SQY, 3), round(HZ - 0.01, 3)], ry=180, opts={'flyAt': FLY13, 'flap': [round(FLY13 - 0.15, 3), 9], 'big': True, 'headYaw': 0.5})],
        cams=[UPCAM(0.0, [3.3, 2.85, 0.95], [[HX, PED + HJ + HH + 1.05, HZ], [HX, PED + 1.4, HZ]], top=0.06, bottom=0.66)])
st.cue('sfx:spring', 'S13', round(FLY13 + 0.02, 3), 0.4); st.cue('whoosh', 'S13', FLY13, 0.2, 0.3, 700, 2400); st.cue('sfx:flap', 'S13', round(FLY13 - 0.1, 3), 0.25)

# 14: without the pigeon the work is incomplete. An expert beside him, three-quarter to us, looks at the empty top of his head through a big magnifying
#     glass and shakes his head; the official, at his other side, slaps a band across his chest: INCOMPLÈTE
D14 = st.dur('S14'); ST14 = 1.25
EX1 = [round(HX + 0.1, 3), 0, round(HZ - 1.1, 3)]; EX2 = [round(HX + 0.1, 3), 0, round(HZ + 1.1, 3)]   # the expert at his right (screen left), the official at his left, both outside the railings
CAM14 = [round(HX - 4.4, 3), PED + 1.35, round(HZ + 0.35, 3)]
RING14 = [round(HX - 0.3, 3), round(PED + HJ + HH * 1.0 + 0.35, 3), round(HZ - 0.04, 3)]   # (final pass) a third of a head higher: his eyes clear                 # the lens just in front of the empty crown (pass 3: higher, its rim off his eyes)
LS14, PHI14 = 1.5, -0.75                                                                                  # loupe scale (a big one); roll (the handle goes down toward the expert)
RY14 = math.degrees(math.atan2(CAM14[0] - RING14[0], CAM14[2] - RING14[2]))                              # the lens faces the camera
def _v14(h):   # the vector from the handle's foot to the ring's centre, h along the handle (Euler XYZ: roll, then ry)
    th = math.radians(RY14); return [-h * math.sin(PHI14) * math.cos(th), h * math.cos(PHI14), h * math.sin(PHI14) * math.sin(th)]
FOOT14 = r3([RING14[i] - _v14(0.72 * LS14)[i] for i in range(3)]); GRIP14 = r3([FOOT14[i] + _v14(0.14 * LS14)[i] for i in range(3)])
EXS = lambda tw=0.0, dz=0.0: {'reach': {'L': [GRIP14[0], GRIP14[1], round(GRIP14[2] + dz, 3), 1, 0.06]}, 'hands': {'L': 'grip'}, 'bend': {'spine': [-0.12, 0, 0, 1, None], 'neck': [0, 0, tw, 1, None]}, 'face': {'brow': 0.7, 'lidL': 0.6}}   # (final pass) the glass in his left hand, the statue side: his arm clear of his face
SCAN14 = [(0.15, 0.13), (0.4, -0.11), (0.62, 0.0)]                                                        # (pass 3) the glass scans the crown: (t, dz)
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[HIM(y0=PED, blink=1, extra=[k(0.0, toon=FROZEN(face={'brow': 0.6, 'gy': -0.85, 'gx': -0.4}), toonDur=0.0),   # his eyes up at the glass
            k(0.75, toon=FROZEN(face={'brow': 0.8, 'gy': -0.9, 'gx': -0.6, 'eye': 0.4}), toonDur=0.08),
            k(ST14, toon=FROZEN(sq=[1.06, 0.93, 1.06], face={'gy': 0.8, 'brow': 0.9, 'eye': 0.4}), toonDur=0.03), k(round(ST14 + 0.08, 3), toon=FROZEN(face={'gy': 0.8, 'brow': 0.7}), toonDur=0.1)]),
        act('expert', EX1, -62, 'stand', 'neutral', keys=[k(0.0, look=RING14), k(0.0, toon=EXS(), toonDur=0.0),   # one eye shut, the other at the glass; (final pass) more to us
            *[k(t, toon=EXS(0.0, dz), toonDur=0.2, toonEase='inOut') for t, dz in SCAN14],
            *[k(round(0.8 + 0.09 * i, 3), toon=EXS(0.85 if i % 2 == 0 else -0.85), toonDur=0.07) for i in range(6)], k(1.36, toon=EXS(), toonDur=0.1), k(0.78, expr='disgust')]),   # tut-tut: (final pass) a bigger shake of the head
        act('officiel', EX2, -137, 'stand', 'unimpressed', keys=[k(0.0, look=[HX - 0.2, PED + 1.4, HZ]), k(round(ST14 - 0.15, 3), toon={'reach': {'R': [round(HX - 0.2, 3), round(PED + 1.22, 3), round(HZ + 0.26, 3), 1, 0.06]}, 'hands': {'R': 'spread'}}, toonDur=0.15, toonEase='in'),   # (final pass) at the band's end: his hand off the word
            k(round(ST14 + 0.3, 3), toon={}, toonDur=0.2)])],
        props=[SHELTER(), STICK(0.0), PLINTH(), *RAILS(), FINE(0.0), INCOMP(ST14),
               P('loupe', 'magnifyingGlass', pos=FOOT14, ry=round(RY14, 2), rot=[0, 0, PHI14], scale=LS14, keys=[k(t, to=[FOOT14[0], FOOT14[1], round(FOOT14[2] + dz, 3)], dur=0.2, ease='inOut') for t, dz in SCAN14])],
        cams=[UPCAM(0.0, CAM14, [[HX, PED + HJ + HH + 0.42, HZ], [HX, PED - 0.1, HZ], [EX1[0], 2.45, round(EX1[2] - 0.35, 3)], [EX2[0], 2.45, round(EX2[2] + 0.25, 3)], [RING14[0], round(RING14[1] + 0.3, 3), RING14[2]]], top=0.12, bottom=0.76, drift=(0.08, 0, -0.04))])   # (final pass) pushed in: the railings low, both heads well inside
st.cue('sfx:paper', 'S14', ST14, 0.4); st.cue('thud', 'S14', ST14, 0.25)

# 15: they moved him to a roundabout. A crane's hook comes down high above him, its two straps going under his arms; he rises out of the railings stiff
#     as a post, feet together, arms at his sides, the fine and the labels still on him
D15 = st.dur('S15'); HK15, UP15 = 0.35, 0.7
SL15, SW15, BAR15 = 1.15, 0.42, 0.7                      # (pass 3) a spreader bar 0.7 m wide above his head, two straps from its ends to loops under his arms (from one point they ran into his head: a hanging)
HOOK15 = round(PED + AP + 0.63 + SL15, 3)                # the hook block: the straps end under his arms
UPS15 = [(0.0, 0.1, 0.6), (0.35, -0.08, 1.8), (0.7, 0.04, 3.2)]   # (pass 3) the lift swings: (t after UP15, dx, height reached)
st.shot('S15', 'parisStreet', setOpts=STREET, actors=[
        HIM(y0=PED, blink=1, extra=[*[k(round(UP15 + t, 3), to=[round(HX + dx, 3), round(PED + y, 3), HZ], dur=round(min(0.35, D15 - UP15 - t), 3), clip='stiffStand', then='stiffStand', glide=True, ease='inOut', face=HRY) for t, dx, y in UPS15],
            k(UP15, toon=FROZEN(sq=[0.97, 1.04, 0.97], face={'gy': -0.9, 'brow': 0.8}), toonDur=0.1), k(round(UP15 + 0.35, 3), toon=FROZEN(lay=[0.08, 0], face={'gy': 0.9, 'brow': 1, 'eye': 0.4}), toonDur=0.2), k(round(UP15 + 0.7, 3), toon=FROZEN(lay=[-0.05, 0], face={'gy': 0.9, 'brow': 1}), toonDur=0.2)])],   # swinging; he looks down
        props=[SHELTER(), STICK(0.0), PLINTH(), *RAILS(), FINE(0.0), INCOMP(0.0),
               P('hook', 'craneHook', pos=[HX, round(HOOK15 + 4.0, 3), HZ], ry=-90, opts={'top': 30.0, 'sling': True, 'slingLen': SL15, 'slingW': SW15, 'spreader': BAR15},
                 keys=[k(0.0, to=[HX, HOOK15, HZ], dur=HK15, ease='out'), *[k(round(UP15 + t, 3), to=[round(HX + dx, 3), round(HOOK15 + y, 3), HZ], dur=round(min(0.35, D15 - UP15 - t), 3), ease='inOut') for t, dx, y in UPS15]])],
        cams=[UPCAM(0.0, [1.35, 1.2, 2.32], [[HX, HOOK15 + 0.3, HZ], [HX, 0.0, HZ], [HX + 1.0, 0.0, HZ - 1.0], [HX - 1.0, 0.0, HZ + 1.0]], top=0.06, bottom=0.86, drift=(0.0, 0.25, 0.0))])
st.cue('engine', 'S15', 0.0, 0.25, D15); st.cue('sfx:squeak', 'S15', UP15, 0.3)

# ---- the roundabout: an island in the middle of the road further down the street, flowers, his plinth in the middle
RZ = -30.0; RB = [0.0, 0, RZ]
ISLAND = lambda: [P('island', 'roundabout', pos=RB, opts={'r': 3.2, 'grass': '#9DBB86'}), P('plinth', 'pedestal', pos=[0.0, 0.16, RZ], ry=90, opts={'h': PED, 'w': 0.7, 'text': 'MONUMENT HISTORIQUE'})]   # (final pass) a pastel sage grass (the saturated green was the loudest area of the film)
ON = [0.0, 0.16 + PED, RZ]
CAR = lambda pid, t0, x0, z0, x1, z1, dur, ry, col: P(pid, 'car', pos=[x0, 0, z0], ry=ry, opts={'color': col}, keys=[k(t0, to=[x1, 0, z1], dur=dur, ease='linear')])
LABELS = lambda: [STICK(0.0), FINE(0.0), INCOMP(0.0)]

# 16: the bus goes past every morning. The roundabout: he stands on his plinth in the flowers, alone, stiff, every label still on him; cars go round;
#     down the street, a bus comes
D16 = st.dur('S16')
st.shot('S16', 'parisStreet', setOpts={**STREET, 'clear': [-90, 80]}, actors=[act('mec', ON, 90, 'stiffStand', 'unimpressed', keys=[k(0.0, look=[8.0, 1.6, RZ + 30.0]), k(0.0, toon={'face': {'lid': 0.35, 'brow': 0.3}, 'hip': 0}, toonDur=0.0), k(round(D16 - 0.75, 3), toon={'face': {'lid': 0.2, 'brow': 0.5, 'gx': -0.9}, 'hip': 0}, toonDur=0.25)])],   # (final pass) his pupils slide to the bus
        props=[*ISLAND(), *LABELS(), P('bus16', 'cityBus', pos=[3.1, 0, RZ - 24.0], ry=-90, keys=[k(0.0, to=[3.1, 0, RZ - 8.0], dur=D16, ease='linear')]),   # (pass 3) close enough to be seen coming
               CAR('car1', 0.0, 4.2, RZ + 4.0, 4.2, RZ - 6.0, D16, 180, '#3A6EA5'), CAR('car2', 0.0, -4.0, RZ - 5.0, -4.0, RZ + 6.0, D16, 0, '#E8A33A')],
        cams=[UPCAM(0.0, [5.4, 2.2, RZ + 6.0], [[0.0, PED + TOP + 0.9, RZ], [-1.2, 0.1, RZ + 0.8], [1.2, 0.1, RZ - 0.8], [3.1, 2.9, RZ - 9.0]], top=0.12, bottom=0.8, drift=(-0.15, 0, -0.2))])   # (final pass) the bus in the frame, coming
st.cue('engine', 'S16', 0.0, 0.2, D16)

# 17: it does not stop. From the pavement: his eyes pop out on stalks to watch it come; the bus sweeps through between us and him without slowing; he
#     is there again, hair and tie blown flat, the flowers lying down, his eyes on their stalks following it away; they snap back in. Cut close: a pigeon
#     swoops down and lands on his head: it flattens him; his eyes roll up to it, resigned
D17 = st.dur('S17'); BP17, PG17 = 0.25, 1.85
BUSX = 3.1
EYES17 = [(0.0, 0.0, 0.0), (0.12, 1.0, 0.55), (0.75, 1.0, -0.55), (1.0, 1.0, -0.7)]   # (t, pop, yaw: + toward his left, where it comes from)
def S17F(t, pop, yaw, extra=None):
    f = {'lid': 0.0 if pop else 0.35, 'brow': 0.6 if pop else 0.3, 'pop': pop, 'popLen': 0.95, 'stalkYaw': yaw, 'eyeYaw': yaw * 0.5, 'stalkRed': 0.6}   # (final pass) two head-widths out; the stalks themselves swing (stalkYaw)
    return {'face': {**f, **(extra or {})}}
st.shot('S17', 'parisStreet', setOpts={**STREET, 'clear': [-90, 80]}, actors=[act('mec', ON, 90, 'stiffStand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={'face': {'lid': 0.35, 'brow': 0.3}, 'hip': 0}, toonDur=0.0),
            k(0.0, toon={'face': {'lid': 0.3, 'brow': 0.4, 'gx': 0.9}, 'hip': 0}, toonDur=0.04), k(0.09, toon={'face': {'lid': 0.3, 'brow': 0.3, 'gx': 0.0}, 'hip': 0}, toonDur=0.04),   # (final pass) a glance at it, back to us...
            k(0.16, toon=S17F(0.16, 1.0, 0.55), toonDur=0.07, toonEase='outBack'),                                                                                                            # ...and out on stalks: it comes
            *[k(round(BP17 + 0.15 + 0.06 * i, 3), toon={**S17F(0, 1.0, round(0.55 - 0.18 * i, 2)), 'hairUp': 0.3, 'wind': [-2.2, 0.2, 0.3], 'sq': [1.0, 1.0, 1.0 + (0.02 if i % 2 else -0.02)]}, toonDur=0.05) for i in range(9)],   # the wind of it: hair and tie stream after it; the stalks swing after it with drag
            k(0.95, toon={**S17F(0, 1.0, -1.25), 'hairUp': 0.2, 'wind': [-1.2, 0.1, 0.1]}, toonDur=0.08, toonEase='out'),   # past it: overshoot
            k(1.08, toon={**S17F(0, 1.0, -0.9), 'hairUp': 0.1, 'wind': [-0.4, 0.0, 0.0]}, toonDur=0.12, toonEase='inOut'),   # settle, still looking where it went
            k(1.3, toon={'face': {'lid': 0.4, 'brow': 0.2, 'pop': 0.0, 'eye': 0.15}, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.06, toonEase='outBack'), k(1.42, toon={'face': {'lid': 0.4, 'brow': 0.2}}, toonDur=0.1),   # snap back in
            k(round(PG17 + 0.35, 3), toon={'scl': {'head': [1.8, 0.3, 1.8]}, 'sq': [1.08, 0.9, 1.08], 'face': {'eye': 0.8, 'brow': 1}}, toonDur=0.03, toonEase='out'),                          # (pass 3) flatter than the first time
            k(round(PG17 + 0.45, 3), expr='neutral'), k(round(PG17 + 0.45, 3), toon={'scl': {'head': [1.2, 0.8, 1.2]}, 'face': {'gy': -0.95, 'lid': 0.1, 'brow': -0.3, 'mouth': 'wavy'}}, toonDur=0.15, toonEase='outBack'),   # two open eyes rolled up to it: resigned
            k(round(PG17 + 0.8, 3), toon={'scl': {'head': [1.12, 0.86, 1.12]}, 'face': {'gy': -0.95, 'lid': 0.12, 'brow': -0.45, 'mouth': 'wavy'}}, toonDur=0.25)])],
        props=[*ISLAND(), STICK(0.0), FINE(0.0),
               P('incomp', 'paperSheet', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.33, 0.2], 'rot': [0, 0, -0.5]}, opts={'w': 0.5, 'h': 0.13, 'big': 'INCOMPLÈTE', 'bigSize': 0.6, 'top': 0.14, 'paper': '#F4F1E8', 'bigInk': '#C8202A', 'bright': True},
                 keys=[k(round(PG17 + 0.4, 3), scale=1.35, dur=0.06, ease='out'), k(round(PG17 + 0.46, 3), scale=0.01, dur=0.07, ease='in')]),   # (pass 3) the pigeon is back: INCOMPLETE pops off (the work is complete again)
               P('pop17', 'impactStars', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.33, 0.25], 'face': 'camera'}, opts={'at': round(PG17 + 0.46, 3), 'n': 6, 'r': 0.32, 'r0': 0.1, 'dur': 0.35, 'size': 0.06}),
               P('bus17', 'cityBus', pos=[BUSX, 0, RZ - 16.0], ry=-90, keys=[k(0.0, to=[BUSX, 0, RZ + 18.0], dur=1.1, ease='linear')], opts={'rock': [[0.0, 0.3]]}),
               P('pig3', 'pigeon', pos=[0.6, ON[1] + 4.6, RZ - 2.6], ry=0, opts={'flap': [round(PG17 - 0.4, 3), round(PG17 + 0.35, 3)], 'big': True}, keys=[k(0.0, visible=False), k(round(PG17 - 0.4, 3), visible=True),
                 k(round(PG17 - 0.4, 3), to=[0.5, round(ON[1] + 2.95, 3), RZ - 0.9], dur=0.55, ease='in'), k(round(PG17 + 0.15, 3), to=[0.0, round(ON[1] + HJ + HH, 3), round(RZ - 0.01, 3)], dur=0.2, ease='out'), k(round(PG17 + 0.35, 3), visible=False)]),
               PIGEON(flaps=[[round(PG17 + 0.35, 3), round(PG17 + 0.55, 3)]], keys=[k(0.0, visible=False), k(round(PG17 + 0.35, 3), visible=True), k(round(PG17 + 0.35, 3), squash=[1.3, 0.62, 1.3], dur=0.3)])],
        cams=[UPCAM(0.0, [6.8, 1.5, RZ + 2.2], [[0.0, ON[1] + TOP + 0.5, RZ], [0.0, ON[1] - 0.1, RZ], [-1.6, 0.4, RZ + 1.2], [1.6, 0.4, RZ - 1.2]], top=0.12, bottom=0.8, drift=(-0.1, 0, -0.1)),
              UPCAM(round(PG17 - 0.4, 3), [2.7, round(ON[1] + 2.0, 3), RZ + 0.6], [[0.0, round(ON[1] + HJ + HH + 0.7, 3), RZ], [0.0, round(ON[1] + 1.4, 3), RZ]], top=0.08, bottom=0.7, drift=(-0.12, 0, -0.03))])
st.cue('whoosh', 'S17', BP17, 0.5, 0.6, 120, 900); st.cue('engine', 'S17', 0.0, 0.3, 1.2); st.cue('pop', 'S17', 0.12, 0.25); st.cue('pop', 'S17', 1.3, 0.2); st.cue('sfx:bonk', 'S17', round(PG17 + 0.35, 3), 0.3); st.cue('pop', 'S17', round(PG17 + 0.46, 3), 0.35)

st.write("La statue", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, follow=1, pupil=0.5, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'officiel': {'preset': 'prefet', 'seed': 171, 'sash': ['#2A4B9B', '#F4F1E8', '#C8202A'], 'sashW': 0.15, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'ouvrier1': {'preset': 'worker', 'seed': 173, 'build': {'width': 0.95, 'headWidth': 1.2}},
    'ouvrier2': {'preset': 'worker', 'seed': 179, 'build': {'width': 0.9, 'headWidth': 1.2}},
    'touriste1': {'preset': 'tourist', 'seed': 181, 'build': {'headWidth': 1.2}},
    'touriste2': {'preset': 'femme', 'seed': 183},
    'touriste3': {'preset': 'tourist', 'seed': 187, 'build': {'headWidth': 1.15, 'height': 0.95}},
    'touriste4': {'preset': 'tourist', 'seed': 199, 'build': {'headWidth': 1.2}},
    'touriste5': {'preset': 'femme', 'seed': 211},
    'nettoyeur': {'preset': 'worker', 'seed': 191, 'build': {'width': 0.92, 'headWidth': 1.2}},
    'flic': {'preset': 'cop', 'seed': 193, 'build': {'width': 0.92, 'headWidth': 1.3}},
    'expert': {'preset': 'savant', 'seed': 197, 'build': {'headWidth': 1.25}}})
