#!/usr/bin/env python3
"""La statue (story 44, cycle 7 of the cartoon staging): this man was waiting for the bus. A pigeon landed on his head. He did not dare move. After
three hours the town hall listed him as a historic monument. Moving damages the heritage. They gave him a plaque. And railings. The tourists queue for
the photo. On Sundays he is cleaned with a jet. He blinked. Fined for vandalism. Yesterday the pigeon left. Without the pigeon the work is incomplete.
They moved him to a roundabout. The bus goes past every morning. It does not stop.
Staging: he is frozen from the moment the pigeon lands (clip stiffStand, the head a little squashed under its weight), and every gag is what is done to
a man who must not move: the creeping hand, the plinth slid under him, the railings that slam round him, the camera flash, the jet in the face (the
pigeon dry under its umbrella), the slow blink, the fine stuck on his forehead, the head that springs back when the weight leaves, the crane that lifts
him stiff as a post, the wind of the bus; and the last pigeon."""
from story_kit import *
import math

st = Story('statue', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 5), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L03', 5), ('S06', 'L04', 0), ('S07', 'L05', 0), ('S08', 'L05', 6),
         ('S09', 'L06', 0), ('S10', 'L07', 0), ('S11', 'L08', 0), ('S12', 'L08', 5), ('S13', 'L09', 0), ('S14', 'L10', 0), ('S15', 'L11', 0), ('S16', 'L12', 0),
         ('S17', 'L13', 0)])

STREET = {'clear': [-80, 80], 'eiffel': False, 'paveW': 6.5}
HX, HZ, HRY = 6.35, 0.0, -90                        # where he waits: on the right-hand pavement, facing the road (-X), the bus shelter behind him
TOP = 2.2                                            # the top of his head (a man of the series is 2.2 m to the top of his tuft)
PED = 0.9                                            # the height of the plinth they put under him
SHELTER = lambda: P('shelter', 'busStop', pos=[7.75, 0, 0.0], ry=-90)
PIG_ON = {'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.34, 0.0]}   # the pigeon on his head (in the head's frame), side-on to the road: it reads as a pigeon
SQ = {'scl': {'head': [1.07, 0.92, 1.07]}}           # his head, a little squashed under the bird
FROZEN = lambda **kw: {**SQ, **kw}
UPCAM = lambda t, frm, pts, top=0.16, bottom=0.8, drift=(0.0, 0.0, 0.0), lenses=range(26, 66): _fitcam(t, frm, pts, top, bottom, drift, lenses)
def _fitcam(t, frm, pts, top, bottom, drift, lenses):
    look, lens, _ = fit(list(frm), pts, top=top, bottom=bottom, lenses=lenses)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    return cam(t, list(frm), [round(frm[i] + drift[i], 3) for i in range(3)], look, [round(look[i] + drift[i], 3) for i in range(3)], lens=lens)
HEADP = lambda y0=0.0: [HX, TOP + y0, HZ]; FEETP = lambda y0=0.0: [HX, y0, HZ]
PIGEON = lambda keys=None, **o: P('pigeon', 'pigeon', on=PIG_ON, ry=90, opts={'ph': 0.4, **o}, **({'keys': keys} if keys else {}))
HIM = lambda y0=0.0, clip='stiffStand', expr='unimpressed', extra=(), **kw: act('mec', [HX, y0, HZ], HRY, clip, expr, keys=[k(0.0, look=None), k(0.0, toon=FROZEN(), toonDur=0.0), *extra], **kw)

# 1: the hook. The bus shelter, from across the road: he waits, a look at his watch, a foot that taps; a pigeon comes down out of the sky, wings beating
D1 = st.dur('S01')
st.shot('S01', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [HX, 0, HZ], HRY, 'checkWatch', 'unimpressed', keys=[k(0.0, look=None),
            *[x for i in range(4) for x in (k(round(0.1 + 0.3 * i, 3), toon={'bend': {'shinR': [0.45, 0, 0, 1, None]}}, toonDur=0.07), k(round(0.2 + 0.3 * i, 3), toon={}, toonDur=0.06))],
            k(0.95, clip='stand', blend=0.15), k(1.0, look=[HX - 3.0, 1.6, HZ - 12.0])])],                                             # then down the street: no bus
        props=[SHELTER(), P('pig1', 'pigeon', pos=[HX + 0.3, 5.5, HZ + 3.2], ry=-140, opts={'flap': [0, 9]}, keys=[k(0.0, to=[HX, 2.85, HZ + 0.4], dur=D1, ease='out')])],
        cams=[UPCAM(0.0, [1.4, 1.6, 3.4], [[HX, TOP + 0.75, HZ + 0.6], [HX, 0.0, HZ], [7.75, 2.6, -1.0], [7.75, 0.0, 1.0]], top=0.1, bottom=0.86, drift=(0.15, 0, -0.1))])
[st.cue('sfx:tick', 'S01', round(0.17 + 0.3 * i, 3), 0.18) for i in range(4)]

# 2: a pigeon landed on his head. Closer: it settles on his crown: his head squashes under it and comes back a little flatter; his eyes roll up to it
D2 = st.dur('S02'); LD2 = 0.42
st.shot('S02', 'parisStreet', setOpts=STREET, actors=[
        act('mec', [HX, 0, HZ], HRY, 'stand', 'neutral', keys=[k(0.0, look=[HX - 3.0, 1.6, HZ - 12.0]),
            k(LD2, toon={'scl': {'head': [1.22, 0.78, 1.22]}, 'face': {'brow': 1, 'eye': 0.45}}, toonDur=0.04, toonEase='out'), k(LD2, expr='surprised'),   # it lands: his head squashes
            k(LD2 + 0.1, toon=FROZEN(face={'brow': 1, 'eye': 0.4}), toonDur=0.12, toonEase='outBack'), k(LD2 + 0.12, look=None),
            k(LD2 + 0.3, toon=FROZEN(face={'gy': -0.95, 'brow': 0.9, 'eye': 0.35}), toonDur=0.1), k(LD2 + 0.3, expr='worried'),                          # his eyes roll up to it
            k(LD2 + 0.5, clip='stiffStand', blend=0.2)])],
        props=[SHELTER(), P('pig1', 'pigeon', pos=[HX, 2.85, HZ + 0.4], ry=-140, opts={'flap': [0, LD2]}, keys=[k(0.0, to=[HX, TOP + 0.04, HZ + 0.02], dur=LD2, ease='out'), k(LD2, visible=False)]),
               PIGEON(keys=[k(0.0, visible=False), k(LD2, visible=True)])],   # (it rides his head from the landing on)
        cams=[UPCAM(0.0, [2.9, 1.95, 0.9], [[HX, TOP + 0.35, HZ], [HX, 1.35, HZ], [HX, TOP + 0.75, HZ + 0.4]], top=0.14, bottom=0.66, drift=(0.08, 0, -0.03))])
st.cue('whoosh', 'S02', 0.0, 0.15, 0.4, 600, 2000); st.cue('sfx:bonk', 'S02', LD2, 0.35)

# 3: he did not dare move. Close on his face: stiff, trembling, a drop of sweat; only his eyes go from side to side; up there the pigeon fluffs up and dozes
D3 = st.dur('S03')
st.shot('S03', 'parisStreet', setOpts=STREET, actors=[
        HIM(extra=[k(0.0, toon=FROZEN(tremble=1, face={'sweat': 1, 'brow': 0.6}), toonDur=0.0),
                   k(0.3, toon=FROZEN(tremble=1, face={'sweat': 1, 'brow': 0.6, 'gx': -0.85}), toonDur=0.08), k(0.65, toon=FROZEN(tremble=1, face={'sweat': 1, 'brow': 0.6, 'gx': 0.85}), toonDur=0.08),
                   k(1.0, toon=FROZEN(tremble=1, face={'sweat': 1, 'brow': 0.6, 'gy': -0.9}), toonDur=0.08)], expr='worried')],
        props=[SHELTER(), PIGEON(sleep=True)],
        cams=[UPCAM(0.0, [4.75, 2.0, 0.42], [[HX, TOP + 0.38, HZ], [HX, 1.62, HZ]], top=0.12, bottom=0.66, drift=(0.06, 0, -0.02))])

# 4: after three hours. Wide, from across the road: buses go by between us and him, fast, one after the other; he has not moved; nor has the bird
D4 = st.dur('S04')
BUS = lambda pid, t0, dur=0.5, x=3.1: P(pid, 'cityBus', pos=[x, 0, -14.0], ry=-90, keys=[k(t0, to=[x, 0, 14.0], dur=dur, ease='linear')])   # (seen: 28 m in half a second; at 68 m in 0.38 s it was in no frame)
st.shot('S04', 'parisStreet', setOpts=STREET, actors=[HIM()],
        props=[SHELTER(), PIGEON(sleep=True), BUS('bus1', 0.0), BUS('bus2', 0.52, x=2.6)],
        cams=[UPCAM(0.0, [-0.6, 1.5, 2.6], [[HX, TOP + 0.5, HZ], [HX, 0.0, HZ], [7.75, 2.6, -1.4], [7.75, 2.6, 1.4]], top=0.16, bottom=0.84)])
st.cue('whoosh', 'S04', 0.05, 0.4, 0.4, 150, 900); st.cue('whoosh', 'S04', 0.55, 0.4, 0.4, 150, 900)

# 5: the town hall listed him as a historic monument. An official in a tricolour sash comes along the pavement, looks him up and down, and slaps a
#    sticker on his chest: MONUMENT HISTORIQUE (the title card)
D5 = st.dur('S05'); AR5, SL5 = 0.55, 1.05
OFF5 = [round(HX + 0.1, 3), 0, round(HZ + 1.05, 3)]   # beside him, at his left (in front of him, between him and us, he hid him)
STICK = lambda t0: P('sticker', 'paperSheet', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.06, 0.38, 0.17]}, opts={'w': 0.26, 'h': 0.16, 'big': 'MONUMENT', 'bigSize': 0.34, 'lines': ['HISTORIQUE'], 'lineSize': 0.2, 'top': 0.12, 'paper': '#F4F1E8', 'bright': True},
                     keys=[k(0.0, scale=0.01, dur=0.0), k(t0, scale=1.0, dur=0.08, ease='outBack')])
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[HIM(extra=[k(SL5, toon=FROZEN(sq=[1.04, 0.96, 1.04], face={'eye': 0.4, 'brow': 0.7}), toonDur=0.04), k(SL5 + 0.1, toon=FROZEN(face={'gy': 0.6}), toonDur=0.1)]),
        act('officiel', [round(HX - 0.3, 3), 0, round(HZ + 3.4, 3)], 180, 'stand', 'unimpressed', keys=[k(0.0, look='mec'), k(0.0, to=OFF5, dur=AR5, clip='walk', then='stand', ease='out', face=200),
            k(AR5 + 0.05, look=[HX, 0.3, HZ]), k(AR5 + 0.3, look=[HX, TOP + 0.3, HZ]),                                                                  # he looks him up and down
            k(SL5 - 0.12, toon={'reach': {'R': [round(HX - 0.2, 3), 1.62, round(HZ + 0.05, 3), 1, 0.06]}, 'hands': {'R': 'spread'}}, toonDur=0.12, toonEase='in'),   # the sticker: slap
            k(SL5 + 0.25, toon={}, toonDur=0.2)])],
        props=[SHELTER(), PIGEON(sleep=True), STICK(SL5), P('clip', 'clipboardProp', on={'actor': 'officiel', 'hand': 'L', 'offset': [0, 0, 0.05]})],
        cams=[UPCAM(0.0, [3.3, 1.7, 2.6], [[HX, TOP + 0.45, HZ], [HX, 0.45, HZ], [OFF5[0], 2.3, OFF5[2]], [OFF5[0], 0.4, OFF5[2] + 0.3]], top=0.2, bottom=0.8, drift=(0.1, 0, -0.08))])
st.cue('sfx:stepSoft', 'S05', 0.15, 0.2); st.cue('sfx:stepSoft', 'S05', 0.4, 0.2); st.cue('sfx:paper', 'S05', SL5, 0.4); st.cue('thud', 'S05', SL5, 0.25)
st.card('S05', 'MONUMENT HISTORIQUE', at=st.at('S05', 'L03', 9))

# 6: moving damages the heritage. An itch: his hand creeps up toward his nose, a centimetre at a time; the official turns: a blast of his whistle, a
#    finger that wags; the hand freezes, and creeps back down
D6 = st.dur('S06'); UP6, WH6, DN6 = 0.1, 1.05, 1.4
NOSE = [round(HX - 0.3, 3), 1.95, round(HZ + 0.06, 3)]
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        HIM(clip='stand', extra=[k(0.0, toon=FROZEN(face={'brow': 0.5, 'gy': 0.3}), toonDur=0.0),
            k(UP6, toon=FROZEN(reach={'R': [round(HX - 0.32, 3), 1.3, round(HZ + 0.18, 3), 1, 0.08]}, hands={'R': 'point'}, face={'brow': 0.6, 'gx': 0.4, 'gy': 0.5}), toonDur=0.4, toonEase='inOut'),   # creeping up
            k(0.6, toon=FROZEN(reach={'R': [round(HX - 0.34, 3), 1.7, round(HZ + 0.12, 3), 1, 0.08]}, hands={'R': 'point'}, face={'brow': 0.7, 'gx': 0.6, 'gy': 0.6}), toonDur=0.4, toonEase='inOut'),
            k(WH6, toon=FROZEN(reach={'R': [round(HX - 0.34, 3), 1.72, round(HZ + 0.12, 3), 1, 0.08]}, hands={'R': 'point'}, sq=[1.03, 0.97, 1.03], face={'brow': 1, 'eye': 0.5, 'gx': -0.8}), toonDur=0.04), k(WH6, expr='scared'),   # the whistle: frozen
            k(DN6, toon=FROZEN(reach={'R': [round(HX - 0.32, 3), 1.2, round(HZ + 0.18, 3), 1, 0.08]}, hands={'R': 'point'}, face={'brow': 0.8, 'eye': 0.4, 'gx': -0.6}), toonDur=0.35, toonEase='inOut'),
            k(1.8, toon=FROZEN(face={'brow': 0.6, 'gx': -0.5}), toonDur=0.2)]),
        act('officiel', OFF5, 120, 'stand', 'unimpressed', keys=[k(0.0, look=[HX - 2.5, 1.6, HZ + 6.0]), k(WH6 - 0.12, look='mec'), k(WH6 - 0.12, face=200, turn=0.1),
            k(WH6, clip='whistleBlow', blend=0.06), k(WH6 + 0.3, clip='stand', blend=0.1),
            *[k(round(WH6 + 0.35 + 0.1 * i, 3), toon={'hands': {'R': 'point'}, 'reach': {'R': [round(OFF5[0] + (0.06 if i % 2 else -0.06), 3), 1.9, round(OFF5[2] - 0.3, 3), 1, 0.06]}}, toonDur=0.06) for i in range(4)]])],   # a finger wags
        props=[SHELTER(), PIGEON(sleep=True), STICK(0.0), P('whistle', 'whistle', on={'actor': 'officiel', 'hand': 'R', 'offset': [0, 0.02, 0.04]}, keys=[k(0.0, visible=False), k(WH6, visible=True), k(WH6 + 0.3, visible=False)]),
               P('notes', 'whistleNotes', pos=[OFF5[0] - 0.1, 2.1, OFF5[2] - 0.2], opts={'n': 2, 'from': WH6, 'every': 0.1, 'size': 0.14, 'dx': -0.3, 'dy': 0.5, 'life': 0.4, 'color': '#1B1B1E'})],
        cams=[UPCAM(0.0, [3.6, 1.75, 2.1], [[HX, TOP + 0.45, HZ], [HX, 0.9, HZ], [OFF5[0], 2.3, OFF5[2]], NOSE], top=0.2, bottom=0.72, drift=(0.12, 0, -0.06))])
st.cue('sfx:whistle', 'S06', WH6, 0.55)

# 7: they gave him a plaque. Two workmen lift him, stiff as a post, and slide a stone plinth under his feet: MONUMENT HISTORIQUE on its plaque; he lands
#    on it with a little squash; the pigeon bobs
D7 = st.dur('S07'); LF7, ON7 = 0.12, 0.62
WK = lambda n, side: [round(HX + 0.05, 3), 0, round(HZ + side * 0.62, 3)]
st.shot('S07', 'parisStreet', setOpts=STREET, actors=[
        HIM(extra=[k(LF7, to=[HX, PED + 0.12, HZ], dur=0.3, clip='stiffStand', then='stiffStand', glide=True, ease='out', face=HRY),
                   k(ON7 - 0.08, to=[HX, PED, HZ], dur=0.08, clip='stiffStand', then='stiffStand', glide=True, ease='in', face=HRY),
                   k(ON7, toon=FROZEN(sq=[1.08, 0.92, 1.08]), toonDur=0.04), k(ON7 + 0.06, toon=FROZEN(settle=0.6), toonDur=0.1)]),
        act('ouvrier1', WK(1, 1), 180, 'stand', 'determined', keys=[k(0.0, look='mec'), k(0.0, toon={'reach': {'L': [HX, 0.95, round(HZ + 0.18, 3), 1, 0.06], 'R': [HX, 1.05, round(HZ + 0.18, 3), 1, 0.06]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [0.4, 0, 0, 1, None]}}, toonDur=0.0),
            k(LF7, toon={'reach': {'L': [HX, 1.08, round(HZ + 0.18, 3), 1, 0.06], 'R': [HX, 1.18, round(HZ + 0.18, 3), 1, 0.06]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [0.1, 0, 0, 1, None]}, 'face': {'cheeks': 1}}, toonDur=0.3),
            k(ON7 + 0.1, toon={}, toonDur=0.2)]),
        act('ouvrier2', WK(2, -1), 0, 'stand', 'determined', keys=[k(0.0, look='mec'), k(0.0, toon={'reach': {'L': [HX, 1.05, round(HZ - 0.18, 3), 1, 0.06], 'R': [HX, 0.95, round(HZ - 0.18, 3), 1, 0.06]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [0.4, 0, 0, 1, None]}}, toonDur=0.0),
            k(LF7, toon={'reach': {'L': [HX, 1.18, round(HZ - 0.18, 3), 1, 0.06], 'R': [HX, 1.08, round(HZ - 0.18, 3), 1, 0.06]}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [0.1, 0, 0, 1, None]}, 'face': {'cheeks': 1}}, toonDur=0.3),
            k(ON7 + 0.1, toon={}, toonDur=0.2)])],
        props=[SHELTER(), PIGEON(sleep=True), STICK(0.0), P('plinth', 'pedestal', pos=[HX + 1.6, 0, HZ], ry=-90, opts={'h': PED, 'w': 0.7, 'text': 'MONUMENT HISTORIQUE'}, keys=[k(0.2, to=[HX, 0, HZ], dur=0.3, ease='out')])],
        cams=[UPCAM(0.0, [2.9, 1.6, 2.2], [[HX, TOP + PED + 0.45, HZ], [HX, 0.0, HZ], [HX + 1.95, 0.0, HZ], [HX, 0.0, HZ + 0.9]], top=0.12, bottom=0.86, drift=(0.1, 0, -0.06))])
st.cue('sfx:grunt', 'S07', LF7, 0.3); st.cue('sfx:slideDown', 'S07', 0.2, 0.25); st.cue('thud', 'S07', ON7, 0.45)

# 8: and railings. Four lengths of railing drop out of the sky round the plinth and slam into the pavement, one after the other; only his eyes move
D8 = st.dur('S08'); RL = (0.06, 0.2, 0.34, 0.48)
RAIL = lambda i, t0, pos, ry: P(f'rail{i}', 'fence', pos=[pos[0], 4.5, pos[1]], ry=ry, opts={'length': 1.9, 'height': 1.0, 'color': '#1E2228'}, keys=[k(t0, to=[pos[0], 0, pos[1]], dur=0.1, ease='in'), k(t0 + 0.1, squash=[1.0, 0.8, 1.0], dur=0.2)])
RAILS = lambda t=(0, 0, 0, 0): [RAIL(0, t[0], (HX - 0.95, HZ), 90), RAIL(1, t[1], (HX, HZ + 0.95), 0), RAIL(2, t[2], (HX + 0.95, HZ), 90), RAIL(3, t[3], (HX, HZ - 0.95), 0)]
st.shot('S08', 'parisStreet', setOpts=STREET, actors=[HIM(y0=PED, extra=[*[k(round(t + 0.1, 3), toon=FROZEN(face={'gx': (-0.8 if i % 2 else 0.8), 'brow': 0.7, 'eye': 0.35}), toonDur=0.04) for i, t in enumerate(RL)]])],
        props=[SHELTER(), PIGEON(sleep=True), STICK(0.0), P('plinth', 'pedestal', pos=[HX, 0, HZ], ry=-90, opts={'h': PED, 'w': 0.7, 'text': 'MONUMENT HISTORIQUE'}), *RAILS(RL)],
        fx=[{'type': 'shake', 'at': t + 0.1, 'dur': 0.08, 'amount': 0.008} for t in RL],
        cams=[UPCAM(0.0, [0.9, 2.1, 3.1], [[HX, TOP + PED + 0.45, HZ], [HX - 1.0, 0.0, HZ + 1.0], [HX + 1.0, 0.0, HZ - 1.0], [HX - 1.0, 0.0, HZ - 1.0]], top=0.12, bottom=0.86)])
[st.cue('clang', 'S08', round(t + 0.1, 3), 0.35) for t in RL]

# 9: the tourists queue for the photo. A queue along the railings; the first one takes a selfie with him: the flash: his pupils shrink to dots, his
#    eyes water
D9 = st.dur('S09'); FL9 = 0.95
QUEUE = [[round(HX - 1.4, 3), 0, round(HZ + 0.6, 3)], [round(HX - 1.5, 3), 0, round(HZ + 1.5, 3)], [round(HX - 1.45, 3), 0, round(HZ + 2.4, 3)]]
st.shot('S09', 'parisStreet', setOpts=STREET, actors=[HIM(y0=PED, extra=[k(FL9, toon=FROZEN(face={'pupil': 0.35, 'brow': 1, 'eye': 0.5}), toonDur=0.03), k(FL9 + 0.25, toon=FROZEN(face={'pupil': 0.5, 'brow': 0.8, 'eye': 0.4, 'tears': 1}), toonDur=0.15)]),
        act('touriste1', QUEUE[0], -20, 'showPhone', 'happy', keys=[k(0.0, look=[HX - 1.0, 1.9, HZ + 2.5]), k(0.3, face=160, turn=0.15), k(0.45, clip='showPhone', blend=0.1), k(FL9 - 0.1, expr='bigGrin')]),
        act('touriste2', QUEUE[1], 180, 'stand', 'neutral', keys=[k(0.0, look='mec'), k(0.6, look='touriste1')]),
        act('touriste3', QUEUE[2], 180, 'readPhone', 'neutral', keys=[k(0.0, look=None)])],
        props=[SHELTER(), PIGEON(sleep=True), STICK(0.0), P('plinth', 'pedestal', pos=[HX, 0, HZ], ry=-90, opts={'h': PED, 'w': 0.7, 'text': 'MONUMENT HISTORIQUE'}), *RAILS(),
               P('tphone', 'smartPhone', on={'actor': 'touriste1', 'hand': 'R', 'offset': [0, 0.02, 0.04]}),
               P('flash', 'impactStars', pos=[QUEUE[0][0] - 0.2, 2.1, QUEUE[0][2] - 0.25], opts={'at': FL9, 'n': 8, 'r': 0.35, 'r0': 0.05, 'dur': 0.18, 'size': 0.09, 'color': '#FFFFFF'})],
        cams=[UPCAM(0.0, [2.4, 1.7, 3.6], [[HX, TOP + PED + 0.45, HZ], QUEUE[0], [QUEUE[2][0], 2.2, QUEUE[2][2]], [HX + 0.9, 0.0, HZ - 0.9]], top=0.14, bottom=0.84, drift=(0.1, 0, -0.1))])
st.cue('sfx:cash', 'S09', FL9, 0.25)

# 10: on Sundays he is cleaned with a jet. A cleaner aims a high-pressure lance at his face: his cheeks flap, his hair stands back, his tie whips;
#     up there the pigeon sits dry under a little umbrella
D10 = st.dur('S10'); JT10 = 0.3
CLN = [round(HX - 1.75, 3), 0, round(HZ + 0.35, 3)]
st.shot('S10', 'parisStreet', setOpts=STREET, actors=[
        HIM(y0=PED, extra=[*[k(round(JT10 + 0.08 * i, 3), toon=FROZEN(hairUp=1, wind=[0.9, 0.0, 0.0], face={'cheeks': (1 if i % 2 else 0.2), 'lid': 0.85, 'brow': -0.4, 'mouth': 'wavy'}, sq=[1.0 + (0.03 if i % 2 else -0.02), 1, 1]), toonDur=0.05) for i in range(18)]]),
        act('nettoyeur', CLN, 75, 'stand', 'neutral', keys=[k(0.0, look=HEADP(PED - 0.25)), k(0.0, toon={'reach': {'R': [round(CLN[0] + 0.45, 3), 1.35, round(CLN[2] - 0.05, 3), 1, 0.06], 'L': [round(CLN[0] + 0.25, 3), 1.2, round(CLN[2] + 0.05, 3), 1, 0.06]}, 'hands': {'L': 'grip', 'R': 'grip'}}, toonDur=0.0)])],
        props=[SHELTER(), PIGEON(sleep=True), STICK(0.0), P('plinth', 'pedestal', pos=[HX, 0, HZ], ry=-90, opts={'h': PED, 'w': 0.7, 'text': 'MONUMENT HISTORIQUE'}), *RAILS(),
               P('lance', 'waterJet', pos=[round(CLN[0] + 0.3, 3), 1.32, round(CLN[2] - 0.02, 3)], ry=104, rot=[-0.85, 0, 0], rotOrder='YXZ', opts={'lance': 0.75, 'len': 1.2, 'on': [JT10, 9.0]}),   # aimed at his face (yaw toward him, pitched up 49 degrees)
               P('brolly', 'umbrella', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.34, 0.06]}, scale=0.22, opts={'radius': 0.75, 'height': 1.0, 'colors': ['#E8504A', '#F4F1E8']})],
        cams=[UPCAM(0.0, [3.4, 2.7, 1.6], [[HX, TOP + PED + 0.62, HZ], [HX, PED + 1.35, HZ], [round(HX - 0.65, 3), PED + 1.85, round(HZ + 0.1, 3)]], top=0.12, bottom=0.62, drift=(0.06, 0, -0.03))])   # closer: his face in the jet, the pigeon dry under its umbrella
st.cue('rain', 'S10', JT10, 0.35, round(D10 - JT10, 3))

# 11: he blinked. Very close on his eyes: a slow blink, with a clack
D11 = st.dur('S11'); BL11 = 0.35
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[
        HIM(y0=PED, extra=[k(BL11, toon=FROZEN(face={'lid': 1}), toonDur=0.16, toonEase='inOut'), k(BL11 + 0.26, toon=FROZEN(face={'lid': 0.0}), toonDur=0.16, toonEase='inOut')])],
        props=[SHELTER(), PIGEON(sleep=True), STICK(0.0), P('plinth', 'pedestal', pos=[HX, 0, HZ], ry=-90, opts={'h': PED, 'w': 0.7, 'text': 'MONUMENT HISTORIQUE'}), *RAILS()],
        cams=[cam(0.0, [round(HX - 1.05, 3), PED + 1.97, round(HZ + 0.12, 3)], [round(HX - 0.98, 3), PED + 1.97, round(HZ + 0.11, 3)], [HX, PED + 1.95, HZ], [HX, PED + 1.95, HZ], lens=36)])
st.cue('clack', 'S11', BL11 + 0.16, 0.6)

# 12: fined for vandalism. A policeman reaches over the railings and slaps a fine on his forehead: AMENDE · VANDALISME; his head jolts; his eyes go up
#     to the paper
D12 = st.dur('S12'); SL12 = 0.45
COP = [round(HX - 1.25, 3), 0, round(HZ - 0.35, 3)]
FINE = lambda t0: P('fine', 'paperSheet', pos=[round(HX - 0.33, 3), PED + 2.03, round(HZ + 0.0, 3)], ry=-90, opts={'w': 0.26, 'h': 0.2, 'head': 'AMENDE', 'headSize': 0.16, 'lines': ['VANDALISME'], 'lineSize': 0.13, 'top': 0.24, 'paper': '#F7E9B5', 'bright': True},
                     keys=[k(0.0, scale=0.01, dur=0.0), k(t0, scale=1.0, dur=0.05, ease='outBack')])
st.shot('S12', 'parisStreet', setOpts=STREET, actors=[
        HIM(y0=PED, extra=[k(SL12, toon=FROZEN(bend={'neck': [-0.22, 0, 0, 1, None]}, face={'brow': 1, 'eye': 0.45}), toonDur=0.04), k(SL12 + 0.12, toon=FROZEN(face={'gy': -0.9, 'brow': 0.8}), toonDur=0.1)]),
        act('flic', COP, 70, 'stand', 'unimpressed', keys=[k(0.0, look=HEADP(PED - 0.2)), k(SL12 - 0.14, toon={'reach': {'R': [round(HX - 0.38, 3), PED + 2.0, round(HZ + 0.02, 3), 1, 0.06]}, 'hands': {'R': 'spread'}}, toonDur=0.14, toonEase='in'),
            k(SL12 + 0.3, toon={}, toonDur=0.2)])],
        props=[SHELTER(), PIGEON(sleep=True), STICK(0.0), P('plinth', 'pedestal', pos=[HX, 0, HZ], ry=-90, opts={'h': PED, 'w': 0.7, 'text': 'MONUMENT HISTORIQUE'}), *RAILS(), FINE(SL12)],
        cams=[UPCAM(0.0, [3.4, 2.3, 1.1], [[HX, TOP + PED + 0.45, HZ], [HX, PED + 1.0, HZ], [COP[0], 2.25, COP[2]]], top=0.16, bottom=0.72, drift=(0.08, 0, -0.04))])
st.cue('sfx:splat', 'S12', SL12, 0.35); st.cue('sfx:paper', 'S12', SL12 + 0.02, 0.3)

# 13: yesterday the pigeon left. It wakes, beats its wings and takes off: his eyes follow it up; his head, free of the weight, springs back up: boing
D13 = st.dur('S13'); FLY13 = 0.4
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[
        HIM(y0=PED, extra=[k(FLY13 - 0.05, toon=FROZEN(face={'gy': -0.9, 'brow': 0.5}), toonDur=0.08),
            k(FLY13 + 0.02, toon={'scl': {'head': [0.9, 1.16, 0.9]}, 'face': {'gy': -1, 'brow': 1, 'eye': 0.4}}, toonDur=0.05, toonEase='out'),   # boing
            k(FLY13 + 0.1, toon={'scl': {'head': [1.03, 0.97, 1.03]}, 'face': {'gy': -1, 'brow': 0.9}}, toonDur=0.06), k(FLY13 + 0.18, toon={'face': {'gy': -0.8, 'brow': 0.7}, 'settle': 0.6}, toonDur=0.1),
            k(1.2, toon={'face': {'gy': -0.6, 'lid': 0.4, 'brow': 0.4}}, toonDur=0.2)]),],
        props=[SHELTER(), STICK(0.0), P('plinth', 'pedestal', pos=[HX, 0, HZ], ry=-90, opts={'h': PED, 'w': 0.7, 'text': 'MONUMENT HISTORIQUE'}), *RAILS(), FINE(0.0),
               P('pig2', 'pigeon', pos=[HX, PED + TOP + 0.02, HZ], ry=-180, opts={'flyAt': FLY13, 'flap': [FLY13 - 0.15, 9]})],
        cams=[UPCAM(0.0, [1.93, 2.15, 1.45], [[HX, PED + TOP + 1.6, HZ + 1.0], [HX, PED + 1.0, HZ], [HX, PED + TOP + 0.3, HZ]], top=0.08, bottom=0.74)])
st.cue('sfx:spring', 'S13', FLY13 + 0.02, 0.4); st.cue('whoosh', 'S13', FLY13, 0.2, 0.3, 700, 2400)

# 14: without the pigeon the work is incomplete. Two experts round the plinth: one looks at the empty top of his head through a magnifying glass; the
#     other slaps a sticker across the plaque: INCOMPLÈTE
D14 = st.dur('S14'); ST14 = 1.25
EX1 = [round(HX - 0.8, 3), 0, round(HZ - 0.75, 3)]; EX2 = [round(HX - 1.0, 3), 0, round(HZ + 0.72, 3)]   # the expert at his right (screen left), the official at his left
CAM14 = [round(HX - 4.4, 3), PED + 1.35, round(HZ + 0.35, 3)]
RING14 = [round(HX - 0.3, 3), round(PED + TOP + 0.08, 3), round(HZ - 0.06, 3)]                              # the lens just in front of the empty crown
LS14, PHI14 = 0.95, -0.5                                                                                    # loupe scale; roll (the handle goes down toward the expert)
RY14 = math.degrees(math.atan2(CAM14[0] - RING14[0], CAM14[2] - RING14[2]))                                # the lens faces the camera
def _v14(h):   # the vector from the handle's foot to the ring's centre, h along the handle (Euler XYZ: roll, then ry)
    th = math.radians(RY14); return [-h * math.sin(PHI14) * math.cos(th), h * math.cos(PHI14), h * math.sin(PHI14) * math.sin(th)]
FOOT14 = r3([RING14[i] - _v14(0.72 * LS14)[i] for i in range(3)]); GRIP14 = r3([FOOT14[i] + _v14(0.14 * LS14)[i] for i in range(3)])
st.shot('S14', 'parisStreet', setOpts=STREET, actors=[HIM(y0=PED, extra=[k(0.0, toon={'face': {'brow': 0.6, 'gy': -0.85, 'gx': -0.3}}, toonDur=0.0),   # his eyes up at the glass
            k(0.75, toon={'face': {'brow': 0.8, 'gy': -0.9, 'gx': -0.5, 'eye': 0.4}}, toonDur=0.08), k(ST14 + 0.05, toon={'face': {'gy': 0.8, 'brow': 0.7}}, toonDur=0.1)]),
        act('expert', EX1, 47, 'stand', 'neutral', keys=[k(0.0, look=RING14), k(0.0, toon={'reach': {'R': [*GRIP14, 1, 0.06]}, 'hands': {'R': 'grip'}, 'bend': {'spine': [-0.22, 0, 0, 1, None]}, 'face': {'brow': 0.7, 'lidL': 0.6}}, toonDur=0.0),   # one eye shut, the other at the glass
            k(0.75, clip='shakeHead', blend=0.1), k(1.35, clip='stand', blend=0.1)]),
        act('officiel', EX2, 125, 'stand', 'unimpressed', keys=[k(0.0, look=[HX - 0.36, 0.5, HZ]), k(ST14 - 0.15, toon={'reach': {'R': [round(HX - 0.42, 3), 0.52, round(HZ + 0.05, 3), 1, 0.06]}, 'hands': {'R': 'spread'}, 'bend': {'spine': [0.45, 0, 0, 1, None]}}, toonDur=0.15, toonEase='in'),
            k(ST14 + 0.3, toon={}, toonDur=0.2)])],
        props=[SHELTER(), STICK(0.0), P('plinth', 'pedestal', pos=[HX, 0, HZ], ry=-90, opts={'h': PED, 'w': 0.7, 'text': 'MONUMENT HISTORIQUE'}), *RAILS(), FINE(0.0),
               P('loupe', 'magnifyingGlass', pos=FOOT14, ry=round(RY14, 2), rot=[0, 0, PHI14], scale=LS14),
               P('incomp', 'paperSheet', pos=[round(HX - 0.39, 3), 0.52, round(HZ, 3)], ry=-90, rot=[0, 0, 0.22], opts={'w': 0.62, 'h': 0.15, 'big': 'INCOMPLÈTE', 'bigSize': 0.7, 'top': 0.05, 'paper': '#F4F1E8', 'bigInk': '#C8202A', 'bright': True},
                 keys=[k(0.0, scale=0.01, dur=0.0), k(ST14, scale=1.0, dur=0.07, ease='outBack')])],
        cams=[UPCAM(0.0, CAM14, [[HX, TOP + PED + 0.42, HZ], [HX, 0.35, HZ], [EX1[0], 2.25, EX1[2]], [EX2[0], 0.2, EX2[2]], RING14], top=0.12, bottom=0.82, drift=(0.08, 0, -0.04))])
st.cue('sfx:paper', 'S14', ST14, 0.4); st.cue('thud', 'S14', ST14, 0.25)

# 15: they moved him to a roundabout. A crane's hook comes down with a sling; it goes round him and he rises out of the railings stiff as a post, his
#     feet together, his arms at his sides, slowly turning
D15 = st.dur('S15'); HK15, UP15 = 0.35, 0.7
st.shot('S15', 'parisStreet', setOpts=STREET, actors=[
        HIM(y0=PED, extra=[k(UP15, to=[HX, PED + 3.2, HZ], dur=round(D15 - UP15, 3), clip='stiffStand', then='stiffStand', glide=True, ease='in', face=-60), k(UP15, toon={'face': {'gy': -0.9, 'brow': 0.8}}, toonDur=0.1)])],
        props=[SHELTER(), STICK(0.0), P('plinth', 'pedestal', pos=[HX, 0, HZ], ry=-90, opts={'h': PED, 'w': 0.7, 'text': 'MONUMENT HISTORIQUE'}), *RAILS(), FINE(0.0),
               P('hook', 'craneHook', pos=[HX, PED + 6.5, HZ], opts={'top': 30.0, 'sling': True, 'slingLen': 0.9, 'slingW': 0.55},
                 keys=[k(0.0, to=[HX, PED + 2.75, HZ], dur=HK15, ease='out'), k(UP15, to=[HX, PED + 5.95, HZ], dur=round(D15 - UP15, 3), ease='in')])],
        cams=[UPCAM(0.0, [1.35, 1.2, 2.32], [[HX, PED + TOP + 1.8, HZ], [HX, 0.0, HZ], [HX + 1.0, 0.0, HZ - 1.0], [HX - 1.0, 0.0, HZ + 1.0]], top=0.06, bottom=0.86)])
st.cue('engine', 'S15', 0.0, 0.25, D15); st.cue('sfx:squeak', 'S15', UP15, 0.3)

# ---- the roundabout: an island in the middle of the road further down the street, flowers, his plinth in the middle
RZ = -30.0; RB = [0.0, 0, RZ]
ISLAND = lambda: [P('island', 'roundabout', pos=RB, opts={'r': 3.2}), P('plinth', 'pedestal', pos=[0.0, 0.16, RZ], ry=90, opts={'h': PED, 'w': 0.7, 'text': 'MONUMENT HISTORIQUE'})]
ON = [0.0, 0.16 + PED, RZ]
CAR = lambda pid, t0, x0, z0, x1, z1, dur, ry, col: P(pid, 'car', pos=[x0, 0, z0], ry=ry, opts={'color': col}, keys=[k(t0, to=[x1, 0, z1], dur=dur, ease='linear')])

# 16: the bus goes past every morning. The roundabout: he stands on his plinth in the flowers, alone, stiff; cars go round; down the street, a bus comes
D16 = st.dur('S16')
st.shot('S16', 'parisStreet', setOpts={**STREET, 'clear': [-90, 80]}, actors=[act('mec', ON, 90, 'stiffStand', 'unimpressed', keys=[k(0.0, look=[8.0, 1.6, RZ + 30.0]), k(0.0, toon={'face': {'lid': 0.35, 'brow': 0.3}}, toonDur=0.0)])],
        props=[*ISLAND(), P('bus16', 'cityBus', pos=[-3.0, 0, RZ - 30.0], ry=-90, keys=[k(0.0, to=[-3.0, 0, RZ - 12.0], dur=D16, ease='linear')]),
               CAR('car1', 0.0, 4.2, RZ + 4.0, 4.2, RZ - 6.0, D16, 180, '#3A6EA5'), CAR('car2', 0.0, -4.0, RZ - 5.0, -4.0, RZ + 6.0, D16, 0, '#E8A33A')],
        cams=[UPCAM(0.0, [6.2, 2.8, RZ + 9.0], [[0.0, PED + TOP + 0.9, RZ], [-2.2, 0.0, RZ + 1.4], [2.2, 0.0, RZ - 1.4], [-3.0, 3.2, RZ - 6.0]], top=0.12, bottom=0.84, drift=(-0.2, 0, -0.3))])   # closer: he reads on his plinth
st.cue('engine', 'S16', 0.0, 0.2, D16)

# 17: it does not stop. The bus sweeps past him close, without slowing: the wind of it: his tie flies, his hair stands, the flowers lie down; he does
#     not move. It has gone. A pigeon comes down and lands on his head: his eyes go up to it
D17 = st.dur('S17'); BP17, PG17 = 0.25, 1.85
st.shot('S17', 'parisStreet', setOpts={**STREET, 'clear': [-90, 80]}, actors=[act('mec', ON, 90, 'stiffStand', 'unimpressed', keys=[k(0.0, look=[8.0, 1.6, RZ + 30.0]), k(0.0, toon={'face': {'lid': 0.35, 'brow': 0.3}}, toonDur=0.0),
            *[k(round(BP17 + 0.06 * i, 3), toon={'hairUp': 1, 'wind': [0.0, 0.2, 1.0], 'face': {'lid': 0.7, 'brow': -0.3}, 'sq': [1.0, 1.0, 1.0 + (0.02 if i % 2 else -0.02)]}, toonDur=0.04) for i in range(9)],
            k(BP17 + 0.6, toon={'face': {'lid': 0.4, 'brow': 0.3}, 'settle': 0.5}, toonDur=0.2),
            k(PG17 + 0.35, toon={'scl': {'head': [1.18, 0.82, 1.18]}, 'face': {'brow': 0.6}}, toonDur=0.04, toonEase='out'), k(PG17 + 0.45, toon={**SQ, 'face': {'gy': -0.95, 'brow': 0.5, 'lid': 0.3}}, toonDur=0.12, toonEase='outBack')])],
        props=[*ISLAND(), P('bus17', 'cityBus', pos=[-3.0, 0, RZ - 14.0], ry=-90, keys=[k(0.0, to=[-3.0, 0, RZ + 16.0], dur=1.1, ease='linear')], opts={'rock': [[0.0, 0.3]]}),
               P('pig3', 'pigeon', pos=[1.6, 4.6, RZ + 2.2], ry=-60, opts={'flap': [PG17 - 0.3, PG17 + 0.4]}, keys=[k(0.0, visible=False), k(PG17 - 0.3, visible=True), k(PG17 - 0.3, to=[0.0, ON[1] + TOP + 0.04, RZ], dur=0.65, ease='out')])],
        cams=[UPCAM(0.0, [4.2, 2.0, RZ + 3.2], [[0.0, ON[1] + TOP + 0.5, RZ], [0.0, ON[1], RZ], [-3.0, 3.3, RZ - 1.0], [1.6, 3.2, RZ + 2.2]], top=0.1, bottom=0.8, drift=(-0.1, 0, -0.1))])
st.cue('whoosh', 'S17', BP17, 0.5, 0.6, 120, 900); st.cue('engine', 'S17', 0.0, 0.3, 1.2); st.cue('sfx:bonk', 'S17', PG17 + 0.35, 0.3)

st.write("La statue", rig='toon', fingers=True, cloth=True, idleShift=1, limbSmear=1, follow=1, pupil=0.5, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'officiel': {'preset': 'prefet', 'seed': 171, 'sash': ['#2A4B9B', '#F4F1E8', '#C8202A'], 'build': {'width': 0.95, 'headWidth': 1.25}},
    'ouvrier1': {'preset': 'worker', 'seed': 173, 'build': {'width': 0.95, 'headWidth': 1.2}},
    'ouvrier2': {'preset': 'worker', 'seed': 179, 'build': {'width': 0.9, 'headWidth': 1.2}},
    'touriste1': {'preset': 'tourist', 'seed': 181, 'build': {'headWidth': 1.2}},
    'touriste2': {'preset': 'femme', 'seed': 183},
    'touriste3': {'preset': 'tourist', 'seed': 187, 'build': {'headWidth': 1.15, 'height': 0.95}},
    'nettoyeur': {'preset': 'worker', 'seed': 191, 'build': {'width': 0.92, 'headWidth': 1.2}},
    'flic': {'preset': 'cop', 'seed': 193, 'build': {'width': 0.92, 'headWidth': 1.3}},
    'expert': {'preset': 'savant', 'seed': 197, 'build': {'headWidth': 1.25}}})
