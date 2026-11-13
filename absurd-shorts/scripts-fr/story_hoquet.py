#!/usr/bin/env python3
"""Le hoquet (story 50, cycle 12 of the cartoon staging): this man has had the hiccups for three days. At each hiccup he jumps a metre. The
seismographs detected an earthquake. Magnitude four; epicentre: his sofa. The prefecture evacuated the whole building, except him: one does not
evacuate an epicentre. The firemen tried the glass of water upside down. Then the big fright: he stayed stuck to the ceiling. Yesterday the State
declared him a natural disaster. His insurance paid him three thousand euros. Since then he drinks nothing but soda.
Staging: every gag is a hiccup that throws him a metre up: the gather on the sofa, the stretch on the way up, the hang time at the top, the fall and
the squash on landing; the seismograph's pen scribbling at each one; the map's rings round his sofa; the neighbours filing out while the building
jolts; the cordon ÉPICENTRE round him alone; the firemen folding him over the glass; BOUH, hair on end, and up he goes: flat on the ceiling, spread
like a starfish, the firemen's jaws dropping; the plaque CATASTROPHE NATURELLE unveiled over his sofa, the official's double take; the cheque that jumps
with him; the pyramid of soda. Natural look; cycle 12 tools: the audit's small / profile warnings, doubleTake()."""
from story_kit import *
import math

st = Story('hoquet', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L04', 2), ('S06', 'L05', 0), ('S07', 'L06', 0), ('S08', 'L07', 0),
         ('S09', 'L08', 0), ('S10', 'L09', 0), ('S11', 'L10', 0), ('S12', 'L11', 0), ('S13', 'L12', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(22, 70), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def FWDV(ry): return (math.sin(math.radians(ry)), math.cos(math.radians(ry)))
def OFF(p, ry, fwd=0.0, rgt=0.0, y=0.0):                           # a point in front of / to the right of someone facing ry
    f = FWDV(ry); r = (-f[1], f[0]); return [round(p[0] + fwd * f[0] + rgt * r[0], 3), y, round(p[2] + fwd * f[1] + rgt * r[1], 3)]

LR = {'tv': False, 'carpet': False, 'pictureX': -1.6}               # the living room, the sofa against the back wall (its seat at 0.5 m); (pass 2) no red rug (27 % of S13 and the captions on it), the painting off the axis of his jumps (his head landed in front of it)
SEAT = [0.0, 0, -2.75]                                              # where he sits on the sofa (the sit clip drops the hips onto the seat)
TIRED = {'face': {'lid': 0.55, 'shadow': 0.6}}                      # three days of hiccups: heavy lids, rings under the eyes
def HICK(t, base, h=1.0, keep=None, hang=0.13, hs=1.5):
    """A hiccup: a gather (squash), up h metres stretched, the top held four frames (hang time), the fall, a squash on landing. keep: toon channels to
    carry (a reach, a held can). (pass 1b) His face stays bored through it (cheeks puffing, a « hic » mouth, heavy lids at the top): the violence is in
    the body, not in the eyes; the eyes-on-stalks take is kept for the fright (S09) and the official's double take (S11). (pass 2) hang: the time held
    at the top (0.13 s; S11 keeps him up there 0.4 s through the official's double take, breathing: a long hang is never a still).
    (pass 3) No hitch at the top: the squash and stretch scale him about his feet, so the stretch relaxing at the top dropped his head and the fall
    stretch, keyed as the drop began (an ease-in barely moves), lifted it again: up, down, up, slam (the review measured the shoulders rising 10 to 23
    px of the strip before each drop). Now the head reaches the top on the stretch (as high as before: the 1 M mark, the card band) and stays there
    while the feet catch up (the body rises the last (stretch - 1) x hs, hs his sitting height), and the fall stretch waits until the drop is under
    way. The stretch is dosed by the height: a small jolt barely stretches."""
    kp = dict(keep or {}); fl = round(0.1 + 0.05 * h, 3); hg = round(hang, 3)
    st_ = round(1 + 0.2 * min(1.0, h / 0.6), 3); sx = round(st_ ** -0.5, 3); dH = round((st_ - 1) * hs, 3)
    fs = round(1 + 0.06 * min(1.0, h / 0.6), 3); fx = round(fs ** -0.5, 3)
    up = [base[0], round(base[1] + h - dH, 3), base[2]]; up2 = [base[0], round(base[1] + h, 3), base[2]]   # the head reaches its old top on the stretch
    ks = [k(round(t - 0.06, 3), toon={**kp, 'sq': [1.1, 0.86, 1.1], 'face': {'puff': 0.55, 'lid': 0.45, 'brow': 0.1, 'mouth': 'kiss'}}, toonDur=0.05, toonEase='in'),   # the gather
          k(t, to=up, dur=fl, glide=True, ease='out', face='keep'), k(t, toon={**kp, 'sq': [sx, st_, sx], 'face': {'lid': 0.5, 'brow': 0.15, 'mouth': 'O', 'jaw': 0.3}}, toonDur=0.04, toonEase='out'),   # up, stretched
          *([k(t, toon={**kp, 'sq': [0.76, 1.42, 0.76], 'face': {'lid': 0.5, 'brow': 0.15, 'mouth': 'O', 'jaw': 0.3}}, toonDur=0.033, toonEase='out'),
             k(round(t + 0.067, 3), toon={**kp, 'sq': [sx, st_, sx], 'face': {'lid': 0.5, 'brow': 0.15, 'mouth': 'O', 'jaw': 0.3}}, toonDur=0.033)] if h >= 0.6 else []),   # (pass 3) a smear frame at the launch of a big jump
          k(round(t + fl, 3), to=up2, dur=0.06, glide=True, ease='out', face='keep'),   # (pass 3) the feet catch up: the head stays where the stretch took it
          k(round(t + fl, 3), toon={**kp, 'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.62, 'brow': 0.0, 'shadow': 0.6}}, toonDur=0.06),   # the top, held
          k(round(t + fl + hg, 3), to=list(base), dur=round(fl + 0.02, 3), glide=True, ease='in', face='keep'),
          k(round(t + fl + hg + 0.06, 3), toon={**kp, 'sq': [fx, fs, fx]}, toonDur=0.04),   # (pass 3) the fall: the stretch once the drop is under way
          k(round(t + 2 * fl + hg + 0.02, 3), toon={**kp, 'sq': [1.12, 0.86, 1.12], 'face': {'lid': 0.5}}, toonDur=0.03, toonEase='out'),   # landed
          k(round(t + 2 * fl + hg + 0.11, 3), toon={**kp, **TIRED}, toonDur=0.1)]
    if hg > 0.2:   # up there for a while: a slow puff of the cheeks, a blink
        ks += [k(round(t + fl + 0.1, 3), toon={**kp, 'sq': [1.02, 0.98, 1.02], 'face': {'lid': 0.7, 'puff': 0.35, 'shadow': 0.6}}, toonDur=0.1),
               k(round(t + fl + hg - 0.12, 3), toon={**kp, 'sq': [0.98, 1.02, 0.98], 'face': {'lid': 1.0, 'shadow': 0.6}}, toonDur=0.04),
               k(round(t + fl + hg - 0.06, 3), toon={**kp, 'face': {'lid': 0.6, 'shadow': 0.6}}, toonDur=0.05)]
    return ks
HIC = lambda pid, pos, times, w=0.5, **o: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': list(times), 'w': w, **o})

# 1: the hook. Close on him on his sofa, three days without sleep: a small jolt on « hoquet », HIC !, then a bigger one that lifts him off the seat
D1 = st.dur('S01'); H1a = round(st.at('S01', 'L01', 4) + 0.02, 3); H1b = round(st.at('S01', 'L01', 7) + 0.05, 3)
st.shot('S01', 'livingRoom', setOpts=LR, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=TIRED, toonDur=0.0),
            k(0.05, toon={**TIRED, 'face': {'lid': 0.85, 'shadow': 0.6}, 'bend': {'neck': [0.45, 0, 0, 1, None]}}, toonDur=round(H1a - 0.3, 3), toonEase='in'),   # (pass 2, freeze check) he nods off, the head sinking...
            k(round(H1a - 0.22, 3), toon={**TIRED, 'face': {'lid': 0.3, 'shadow': 0.6, 'brow': 0.4}}, toonDur=0.06, toonEase='out'),   # ...and jerks up
            *HICK(H1a, SEAT, 0.14), *HICK(H1b, SEAT, 0.42)])],
        props=[HIC('hic1', [0.42, 2.25, -2.6], [H1a, H1b], w=0.42)],
        cams=[FC(0.0, [0.25, 1.55, -0.6], [[SEAT[0], 2.75, SEAT[2]], [SEAT[0], 1.05, SEAT[2]], [round(SEAT[0] - 0.5, 3), 1.9, SEAT[2]], [round(SEAT[0] + 0.62, 3), 2.3, SEAT[2]]], top=0.14, bottom=0.72, drift=(0.0, 0.0, -0.08))])
st.cue('sfx:gulp', 'S01', H1a, 0.3); st.cue('sfx:boing', 'S01', H1b, 0.3)

# 2: at each hiccup he jumps a metre. Wider, room above him: two hiccups, each a metre straight up off the sofa, hang time at the top, squash on landing
D2 = st.dur('S02'); H2a = round(st.at('S02', 'L02', 2) + 0.02, 3); H2b = round(st.at('S02', 'L02', 8) + 0.02, 3)
st.shot('S02', 'livingRoom', setOpts=LR, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=TIRED, toonDur=0.0), *HICK(H2a, SEAT, 1.0),
            k(round(H2a + 0.62, 3), look=[0.95, 2.45, -3.4]), k(round(H2a + 0.66, 3), toon={**TIRED, 'sq': [1.04, 0.95, 1.04], 'face': {'lid': 0.7, 'shadow': 0.6, 'puff': 0.4}}, toonDur=0.15),   # (pass 2) a glance up at the mark, a sigh...
            k(round(H2a + 0.88, 3), toon={**TIRED, 'face': {'lid': 1.0, 'shadow': 0.6}}, toonDur=0.05), k(round(H2a + 0.98, 3), toon=TIRED, toonDur=0.07), k(round(H2a + 0.95, 3), look='camera'),   # ...a blink, back to us
            *HICK(H2b, SEAT, 1.0)])],
        props=[HIC('hic2', [-0.6, 3.15, -2.6], [H2a, H2b], w=0.5),
               P('ruler2', 'heightRuler', pos=[0.95, 1.45, -3.42], opts={'h': 1.0, 'text': '1 M', 'side': -1, 'plateW': 0.46, 'pops': [round(H2a + 0.15, 3), round(H2b + 0.15, 3)]})],   # (pass 2) a yellow height ruler on the wall, « 1 M » in big capitals (the sticky note's « 1 m » was 3 px), its plate jumping when he reaches the mark
        cams=[FC(0.0, [0.3, 1.7, 1.2], [[SEAT[0], 3.65, SEAT[2]], [SEAT[0], 0.3, SEAT[2]], [-1.25, 2.0, SEAT[2]], [1.25, 2.0, SEAT[2]]], top=0.1, bottom=0.74, drift=(0.0, 0.0, -0.1))])
st.cue('sfx:boing', 'S02', H2a, 0.35); st.cue('thud', 'S02', round(H2a + 0.43, 3), 0.25); st.cue('sfx:boing', 'S02', H2b, 0.35); st.cue('thud', 'S02', round(H2b + 0.43, 3), 0.25)

# 3: the seismographs detected an earthquake. The lab: the drum turns, the pen writes a calm line, then scribbles a spike at each hiccup, the second one
#    so big the pen jumps off the paper; the seismologist leans in, then his eyes shoot out on stalks
D3 = st.dur('S03'); SP3a = round(st.at('S03', 'L03', 1) + 0.1, 3); SP3b = round(st.at('S03', 'L03', 5) - 0.05, 3)
BENCH = [0.0, 0, -2.2]; SEIS = [0.0, 0.76, -2.2]; SAV = [0.1, 0, -2.85]
READ = lambda sp, nk, **f: {'bend': {'spine': [sp, 0, 0, 1, None], 'neck': [nk, 0, 0, 1, None]}, 'face': dict(f)}
PAPER3 = [SEIS[0], round(SEIS[1] + 0.22, 3), round(SEIS[2] + 0.2, 3)]
st.shot('S03', 'office', setOpts={'door': False}, actors=[
        act('savant', SAV, 0, 'stand', 'neutral', keys=[k(0.0, look=PAPER3), k(0.0, toon=READ(0.3, 0.3, brow=0.3), toonDur=0.0),   # (pass 2) reading the paper, the head down over it from the start (the review: "faces camera, never looks at the paper")
            k(round(SP3a + 0.05, 3), toon=READ(0.45, 0.4, brow=0.6), toonDur=0.15),   # the first spike: he leans in to the trace
            k(round(SP3a + 0.35, 3), toon={**READ(0.45, 0.35, brow=0.6, lid=1.0), 'touch': {'R': ['face', 0.0, 0.62, 0.06, 1, 0.08]}, 'hands': {'R': 'point'}}, toonDur=0.1),   # a finger to the bridge of his nose, a blink...
            k(round(SP3a + 0.5, 3), toon={**READ(0.45, 0.35, brow=0.7), 'touch': {'R': ['face', 0.0, 0.66, 0.06, 1, 0.08]}, 'hands': {'R': 'point'}}, toonDur=0.08),
            k(round(SP3a + 0.68, 3), toon=READ(0.5, 0.4, brow=0.8, eye=0.2), toonDur=0.2),   # ...reading on
            k(round(SP3b - 0.25, 3), toon=READ(0.5, 0.1, brow=0.9, lid=0.3, gy=0.95), toonDur=0.08, toonEase='out'),   # (pass 2) the second spike: his nose down to the paper for eight frames...
            # (pass 3) the spine bent, the neck barely, the eyes down on the paper: bent 72 degrees the probe read his face 82 degrees away (the top of his hair)
            *take(round(SP3b + 0.06, 3), 'stalks', keep={'bend': {'spine': [0.1, 0, 0, 1, None]}}, hold=0.35),   # ...then the head snaps up, the eyes out on stalks
            k(round(SP3b + 0.45, 3), look=[0.55, 1.15, -1.9])])],   # his eyes after the pen flying off
        props=[P('board3', 'tallyBoard', pos=[SAV[0], 2.05, -3.5], opts={'w': 1.7, 'h': 1.05}),   # (pass 3) a dark board behind his head (white coat and hair on the cream wall: 1.11:1)
               P('bench3', 'desk', pos=BENCH), P('seis3', 'seismograph', pos=SEIS, opts={'spikes': [[SP3a, 1.0], [SP3b, 1.5]], 'ink': 0.03, 'clampV': 1.35, 'postX': 0.33, 'speed': 0.4, 'penOff': round(SP3b + 0.08, 3)})],   # (pass 2) thick dark ink across the paper, the pen post aside (it hid the nib), the pen thrown off in an arc on the second spike
        # (pass 3) lower: nose down to the paper his face comes toward us (from 1.45 m we saw the top of his hair, a white block with no face)
        cams=[FC(0.0, [0.55, 1.0, -0.55], [[SEIS[0], 1.15, round(SEIS[2] + 0.35, 3)], [SAV[0], 2.7, SAV[2]], [round(SEIS[0] - 0.5, 3), 0.75, round(SEIS[2] + 0.3, 3)], [round(SEIS[0] + 0.5, 3), 0.75, round(SEIS[2] + 0.3, 3)]], top=0.12, bottom=0.74, drift=(-0.03, 0, -0.06))])
st.cue('sfx:needle', 'S03', SP3a, 0.3); st.cue('sfx:needle', 'S03', SP3b, 0.4); st.cue('pop', 'S03', round(SP3b + 0.06, 3), 0.25); st.cue('sfx:boing', 'S03', round(SP3b + 0.1, 3), 0.2)

# 4: magnitude four. The wall screen: a city map, MAGNITUDE 4 in red; rings pulse out from a red dot; the seismologist points at it, his arm stretching
D4 = st.dur('S04'); MAPW = [-0.2, 1.7, -3.5]
st.shot('S04', 'office', setOpts={'door': False}, actors=[
        act('savant', [1.05, 0, -2.75], 10, 'stand', 'neutral', keys=[k(0.0, look=[MAPW[0], 1.8, MAPW[2]]), k(0.15, toon={'reach': {'R': [round(MAPW[0] + 0.05, 3), 1.6, round(MAPW[2] + 0.08, 3), 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.1, 'face': {'brow': 0.8, 'eye': 0.3}}, toonDur=0.08, toonEase='outBack'),
            k(0.32, look='camera'),   # (pass 3) three-quarters to us, he points without looking: we saw the back of his head pointing
            ])],
        props=[P('map4', 'quakeMap', pos=MAPW, opts={'w': 1.6, 'h': 1.0, 'head': 'MAGNITUDE 4', 'label': '', 'labelBelow': True, 'dotX': 0.5, 'pulses': [0.15, 0.6, 1.05]})],   # (pass 2) no label yet: CANAPÉ is S05's reveal
        cams=[FC(0.0, [0.4, 1.7, 0.4], [[MAPW[0] - 0.85, 2.25, MAPW[2]], [MAPW[0] + 0.85, 1.15, MAPW[2]], [1.05, 2.4, -2.75], [1.05, 1.0, -2.75], [1.45, 2.2, -2.75], [1.45, 1.5, -2.75]], top=0.12, bottom=0.72)])   # (pass 2) room right of his head (the edge cut it to a 35 px sliver)
st.cue('sfx:beep', 'S04', 0.15, 0.3)

# 5: epicentre: his sofa. Close on the map, MAGNITUDE 4 whole at the top: it zooms in on the red dot in 0.7 s and lands on « canapé », the label popping in
#    under the dot on the word, the rings pulsing out
D5 = st.dur('S05'); CAN5 = round(st.at('S05', 'L04', 4) - 0.04, 3); Z5 = round(CAN5 - 0.72, 3)
st.shot('S05', 'office', setOpts={'door': False}, actors=[],
        props=[P('map5', 'quakeMap', pos=MAPW, opts={'w': 1.6, 'h': 1.0, 'head': 'MAGNITUDE 4', 'label': 'CANAPÉ', 'labelBelow': True, 'labelAt': CAN5, 'labelMax': 1.6, 'dotX': 0.5, 'res': 1536,
                                                        'pulses': [0.1, round(CAN5 - 0.05, 3), round(CAN5 + 0.4, 3)], 'zoom': [[Z5, 2.6]], 'zoomDur': 0.7})],   # (pass 2) the reveal lands on the word; the label under the dot (beside it, its box bit the dot and ran off the frame); a sharper map
        cams=[cam(0.0, [MAPW[0], 1.57, round(MAPW[2] + 2.15, 3)], [MAPW[0], 1.57, round(MAPW[2] + 1.8, 3)], [MAPW[0], 1.57, MAPW[2]], [MAPW[0], 1.57, MAPW[2]], lens=50)])   # (pass 2) MAGNITUDE 4 whole at the top, the dot and the word in the middle (it ended on a red disc and a lone C)
st.cue('sfx:zip', 'S05', Z5, 0.25); st.cue('pop', 'S05', CAN5, 0.3)

# 6: the prefecture evacuated the whole building. In the street at the foot of his block: a policeman blows his whistle and waves; the neighbours file out of
#    the door one after another with their bags; a hiccup upstairs: the whole facade jolts, the neighbours hop
D6 = st.dur('S06'); H6 = round(st.at('S06', 'L05', 4) - 0.05, 3)
FX6 = 8.6; DOOR6 = [round(FX6 - 0.05, 3), 0, 30.0]; STREET = {'clear': [-80, 80], 'eiffel': False, 'paveW': 6.5}
HOP6 = lambda p0: [k(H6, to=[p0[0], 0.22, p0[2]], dur=0.03), k(round(H6 + 0.09, 3), to=list(p0), dur=0.05, ease='in')]   # (pass 2) the whole facade hops 22 cm for three frames (a 1 px jolt did not register)
FLATS6 = P('flats6', 'flatsWall', pos=[FX6, 0, 30.0], ry=-90, opts={'w': 6.0, 'h': 12.6, 'cols': 3, 'rows': 3, 'depth': 1.25, 'y0': 3.0}, keys=[*HOP6([FX6, 0, 30.0]), k(H6, squash=[1.0, 1.03, 1.0], dur=0.0), k(round(H6 + 0.14, 3), squash=[1.0, 0.985, 1.0], dur=0.0), k(round(H6 + 0.2, 3), squash=[1, 1, 1], dur=0.08)])
NEIGH = [('voisine', 0.0, 2.3, [-0.45, -0.89], 'walk'), ('mamie', 0.32, 1.4, [-0.6, -0.8], 'walk'), ('gamin', 0.6, 3.0, [-0.9, -0.44], 'run'), ('voisin', 0.88, 2.3, [-0.25, -0.97], 'walk')]
def OUT6(n, t0, v, u, clip):   # (pass 1b) out of the door and across the pavement toward us, each on his own line (fanned out, nobody stops, nobody on the spot): the kid runs off to the right, the others out on the left
    a = [round(FX6 - 0.35, 3), 0, 30.0]; dur = round(D6 - t0 - 0.05, 3); d = v * dur
    b = [round(a[0] + u[0] * d, 3), 0, round(a[2] + u[1] * d, 3)]; ry = round(math.degrees(math.atan2(u[0], u[1])), 1)
    return act(n, a, ry, 'stand', 'worried', keys=[k(0.0, visible=False), k(round(t0 + 0.05, 3), visible=True), k(round(t0 + 0.05, 3), to=b, dur=dur, clip=clip, then='stand', ease='linear', face='move'),
                                                   k(0.0, look=[b[0], 1.5, round(b[2] - 1.0, 3)]), *react(H6, 0.8, look=[FX6, 9.5, 30.0])])
BAGS6 = [P('bag6a', 'shoppingBag', on={'actor': 'voisine', 'hand': 'R'}), P('bag6b', 'shoppingBag', opts={'text': 'MARCHÉ'}, on={'actor': 'mamie', 'hand': 'L'}), P('bag6c', 'shoppingBag', on={'actor': 'voisin', 'hand': 'R'})]
st.shot('S06', 'parisStreet', setOpts=STREET, actors=[
        act('flic', [round(FX6 - 1.6, 3), 0, 31.3], -120, 'stand', 'determined', keys=[k(0.0, look=[FX6, 1.6, 30.0]), k(0.0, toon={'touch': {'R': ['face', 0.02, 0.22, 0.1, 1, 0.04]}, 'reach': {'L': [round(FX6 - 2.3, 3), 2.2, 30.6, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'pinch'}, 'face': {'puff': 0.6}}, toonDur=0.0),
            *[k(round(0.2 + 0.3 * i, 3), toon={'touch': {'R': ['face', 0.02, 0.22, 0.1, 1, 0.04]}, 'reach': {'L': [round(FX6 - 2.5 + 0.25 * (i % 2), 3), 2.0 + 0.25 * (i % 2), 30.4, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'pinch'}, 'face': {'puff': 0.6}}, toonDur=0.1) for i in range(6)]]),   # whistling, waving them out
        *[OUT6(*nb) for nb in NEIGH]],
        props=[FLATS6, *BAGS6, P('door6', 'door', pos=DOOR6, ry=-90, opts={'w': 1.3, 'h': 2.5, 'open': 1}, keys=HOP6(DOOR6)), P('whistle6', 'whistle', on={'actor': 'flic', 'hand': 'R', 'offset': [0, 0.02, 0.04]}),
               HIC('hic6', [round(FX6 - 0.75, 3), 4.35, 30.0], [H6], w=0.75),   # (pass 2) the jolt has a cause: HIC ! out of his window (first floor, over the door)
               P('dust6', 'dustPuff', pos=[round(FX6 - 0.45, 3), 4.15, 30.0], scale=0.7, opts={'once': True, 'startAt': H6, 'period': 0.5, 'color': '#EDE4D3'}, keys=[k(0.0, visible=False), k(H6, visible=True), k(round(H6 + 0.5, 3), visible=False)]),
               P('debris6', 'waterDrops', pos=[round(FX6 - 0.4, 3), 4.0, 30.0], opts={'at': H6, 'n': 14, 'dir': [-1, 0.25, 0], 'speed': 1.3, 'spread': 0.8, 'color': '#E3D8C2', 'r': 0.05, 'life': 0.9})],
        fx=[{'type': 'shake', 'at': H6, 'dur': 0.18, 'amount': 0.01}],
        cams=[FC(0.0, [3.4, 1.7, 25.6], [[FX6, 4.75, 30.0], [round(FX6 - 2.6, 3), 0.0, 28.4], [round(FX6 - 1.6, 3), 2.3, 31.3], [round(FX6 - 0.6, 3), 0.0, 30.0]], top=0.12, bottom=0.74, drift=(0.06, 0, -0.08))])   # (pass 2) up to his window
st.cue('sfx:whistle', 'S06', 0.2, 0.35); st.cue('thud', 'S06', H6, 0.4); [st.cue('sfx:stepRun', 'S06', round(nb[1] + 0.2, 3), 0.2) for nb in NEIGH]

# 7: except him: one does not evacuate an epicentre. From above, his living room: red rings on the floor round the sofa, a police cordon ÉPICENTRE round
#    it; he sits alone, deadpan; a hiccup: up a metre, the tape jumps, the rings flash
D7 = st.dur('S07'); H7 = round(st.at('S07', 'L06', 6) + 0.05, 3)
st.shot('S07', 'livingRoom', setOpts={**LR, 'carpet': False}, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=TIRED, toonDur=0.0), k(0.8, look=[SEAT[0], 0.9, round(SEAT[2] + 1.0, 3)]), k(1.3, look='camera'),
            k(1.0, toon={**TIRED, 'sq': [0.95, 1.07, 0.95], 'bend': {'armL': [0, 0.35, 0, 1, None], 'armR': [0, -0.35, 0, 1, None]}}, toonDur=0.12), k(1.32, toon=TIRED, toonDur=0.15),   # (pass 2) a shrug
            *HICK(H7, SEAT, 1.55)])],   # (pass 2) higher than the rule shot: the escalation (pass 3: 1.55 m; at 1.75 m his head left the top of the frame)
        props=[P('rings7', 'quakeRings', pos=[SEAT[0], 0, round(SEAT[2] + 0.2, 3)], opts={'r': 2.2, 'n': 4, 'pulses': [0.1, H7]}),
               P('cordon7', 'cordon', pos=[SEAT[0], 0, round(SEAT[2] + 0.15, 3)], opts={'w': 3.0, 'd': 1.7, 'sign': 'ÉPICENTRE', 'signW': 1.0, 'signH': 0.3, 'jumps': [[H7, 1.0]], 'snap': round(H7 + 0.04, 3)})],   # (pass 2) the front tape snaps under the jolt, its plate drops
        cams=[FC(0.0, [1.4, 4.2, 1.0], [[SEAT[0], 3.5, SEAT[2]], [-1.6, 0.0, round(SEAT[2] + 1.0, 3)], [1.6, 0.0, round(SEAT[2] + 1.0, 3)], [-1.6, 0.0, round(SEAT[2] - 0.75, 3)], [1.6, 0.0, round(SEAT[2] - 0.75, 3)]], top=0.1, bottom=0.74, drift=(0.0, -0.05, -0.08))])   # (pass 1b) framed on the cordon, not on the back wall: the man was 23 % of the frame
st.cue('sfx:boing', 'S07', H7, 0.35); st.cue('clack', 'S07', round(H7 + 0.04, 3), 0.3); st.cue('thud', 'S07', round(H7 + 2 * (0.1 + 0.05 * 1.55) + 0.13 + 0.02, 3), 0.3)

# 8: the firemen tried the glass of water upside down. Two firemen fold him over at the waist; one holds a big glass of blue water upside down at his lips;
#    on « envers » a hiccup jackknifes him up out of their hands in an arc, the water spraying out of his cheeks; the firemen wince
D8 = st.dur('S08'); H8 = round(st.at('S08', 'L07', 8) + 0.05, 3)
ME8 = [0.0, 0, -1.6]; BENT = {'bend': {'spine': [1.15, 0, 0, 1, None], 'neck': [-0.35, 0, 0, 1, None]}}
MOUTH8 = [0.15, 1.58, -0.99]                                        # (pass 3) measured (debugJoints: the head joint at 1.6 m, the face 46 degrees down): 0.26 m above the guess
GLASS8 = [0.15, 1.15, -0.88]                                        # (pass 3) the remedy as it is done: the glass upright under his mouth, tipped toward him, he drinks from its far rim
HOLD8 = {'reach': {'R': [0.05, 1.33, -0.84, 1, 0.06]}, 'hands': {'R': 'grip'}}
FOL8 = {'actor': 'mec', 'lag': 0.1, 'dy': -0.35, 'cheat': 0.3}   # (pass 3) the firemen's eyes on him, a tenth of a second late, their faces cheated a third toward us
st.shot('S08', 'livingRoom', setOpts=LR, actors=[
        act('mec', ME8, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[MOUTH8[0], 1.1, MOUTH8[2]]), k(0.0, toon={**BENT, **TIRED}, toonDur=0.0),
            *[x for t_ in (0.4, 0.8, 1.18) for x in (k(t_, toon={**BENT, 'scl': {'head': [1.14, 1.0, 1.14]}, 'face': {**TIRED['face'], 'puff': 1.0}}, toonDur=0.06), k(round(t_ + 0.16, 3), toon={**BENT, **TIRED}, toonDur=0.08))],   # (pass 1b) gulps, upside down (pass 3: the cheeks out, the head swelling: they were flat)
            k(round(H8 - 0.06, 3), toon={**BENT, 'sq': [1.08, 0.88, 1.08], 'face': {'eye': 0.3, 'mouth': 'O', 'puff': 0.8}}, toonDur=0.05, toonEase='in'),
            # (pass 2) the jackknife: he opens out going up and forward out of their hands, folds shut at the top, comes down folded
            k(H8, to=[ME8[0], 0.7, round(ME8[2] + 0.3, 3)], dur=0.14, glide=True, ease='out', face='keep'),
            k(H8, toon={'sq': [0.86, 1.2, 0.86], 'bend': {'spine': [-0.6, 0, 0, 1, None], 'neck': [-0.35, 0, 0, 1, None], 'legL': [-0.45, 0, 0, 1, None], 'legR': [-0.45, 0, 0, 1, None]}, 'face': {'puff': 1.0, 'lid': 0.25, 'brow': 0.7, 'mouth': 'kiss'}}, toonDur=0.05, toonEase='out'),   # (pass 2b) arched open, the legs back...
            k(round(H8 + 0.1, 3), toon={'bend': {'spine': [1.25, 0, 0, 1, None], 'neck': [-0.4, 0, 0, 1, None], 'legL': [1.1, 0, 0, 1, None], 'legR': [1.1, 0, 0, 1, None]}, 'face': {'puff': 0.1, 'lid': 0.4, 'brow': 0.3, 'mouth': 'O', 'jaw': 0.35}}, toonDur=0.07, toonEase='inOut'),   # ...then folded shut like a penknife, the legs up to meet him, the water out
            k(round(H8 + 0.27, 3), to=ME8, dur=0.13, glide=True, ease='in', face='keep'),
            k(round(H8 + 0.4, 3), toon={**BENT, 'sq': [1.1, 0.88, 1.1], 'face': {'lid': 0.5}}, toonDur=0.03, toonEase='out'), k(round(H8 + 0.5, 3), toon={**BENT, **TIRED}, toonDur=0.1)]),
        # (pass 3) both firemen on the far side of him, facing us (one at his front on our side hid him; seen from the side they were profiles)
        act('pompier1', [-0.68, 0, -1.92], 65, 'stand', 'determined', keys=[k(0.0, look=[ME8[0], 1.3, ME8[2]]), k(0.55, look='camera'), k(1.0, look=[ME8[0], 1.3, ME8[2]]), k(0.0, toon={'reach': {'L': [-0.14, 1.45, -1.78, 1, 0.05], 'R': [-0.1, 1.3, -1.45, 1, 0.05]}, 'hands': {'L': 'flat', 'R': 'flat'}}, toonDur=0.0),   # holding him folded
            k(round(H8 + 0.03, 3), look=FOL8),   # (pass 3) the eyes then the head follow him up and down, three frames late (cycle 15: a look at an actor with a lag)...
            *react(round(H8 + 0.12, 3), 0.8, look=FOL8, kind='wince')]),   # ...a wince under the spray
        act('pompier2', [-0.62, 0, -0.78], 117, 'stand', 'neutral', keys=[k(0.0, look=MOUTH8), k(0.7, look='camera'), k(1.1, look=MOUTH8), k(0.0, toon=HOLD8, toonDur=0.0),   # the glass at his lips, upside down
            k(round(H8 + 0.03, 3), look=FOL8),
            *react(round(H8 + 0.13, 3), 0.8, keep=HOLD8, look=FOL8, kind='wince')])],   # he keeps hold of the glass, wincing
        props=[P('glass8', 'waterGlass', pos=GLASS8, rot=[-0.35, 0, 0], scale=3.0, opts={'level': 0.7, 'water': '#1565C0', 'tumbler': True}),
               # (pass 3) a tumbler that reads (a thick rim, highlights, dark blue water), upright and tipped to his lips (upside down above his face it read as a pale slab)
               P('spray8', 'waterDrops', pos=[0.0, 3.36, -1.32], opts={'at': round(H8 + 0.05, 3), 'n': 28, 'dir': [0, 0.6, 0.8], 'speed': 3.2, 'spread': 0.5, 'r': 0.03, 'life': 0.7, 'color': '#1E88E5'})],
               # (pass 3) a fountain out of his mouth at the top (measured: the head at 3.26 m, arched back): it burst round the glass in the fireman's fist
        cams=[FC(0.0, [3.2, 1.45, -0.44], [[ME8[0], 2.3, ME8[2]], [-0.68, 2.4, -1.92], [-0.62, 2.4, -0.78], [ME8[0], 0.3, ME8[2]], [ME8[0], 3.7, -1.2], [GLASS8[0], GLASS8[1], GLASS8[2]]], top=0.08, bottom=0.74)])
        # (pass 3) from his side, 70 degrees: the fold is an L against the wall and the glass upside down at his lips in profile (head on, his torso
        # stacked toward the lens into a navy knot)
st.cue('sfx:pour', 'S08', 0.3, 0.25); st.cue('sfx:splash', 'S08', round(H8 + 0.09, 3), 0.4)

# 9: then the big fright. On the sofa, deadpan: a fireman springs up behind the sofa, arms up in a V, BOUH !; on the same frame his hair stands on end, his
#    eyes shoot out on stalks and his mouth screams, held eight frames; then up he goes out of the top of the frame, the fireman's head following him; off
#    the frame he hits the ceiling: the picture shakes, plaster flakes rain down
D9 = st.dur('S09'); BOO9 = round(st.at('S09', 'L08', 2) - 0.1, 3); TK9 = round(BOO9 + 0.04, 3); UP9 = round(BOO9 + 0.36, 3)
FR9 = [round(SEAT[0] - 0.6, 3), 0, -3.3]                            # (pass 2) the fireman on the left, over the red cushion (on the yellow one his yellow jacket merged with it)
SCARED = {'sq': [0.9, 1.14, 0.9], 'hairUp': 1.3, 'face': {'pop': 0.75, 'popLen': 0.32, 'brow': 1, 'jaw': 0.8}}
st.shot('S09', 'livingRoom', setOpts=LR, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=TIRED, toonDur=0.0),
            k(round(TK9 - 0.067, 3), toon={**TIRED, 'sq': [1.08, 0.9, 1.08]}, toonDur=0.05),   # two frames of brace...
            k(TK9, toon=SCARED, toonDur=0.033, toonEase='out'),   # (pass 2) ...then all on one frame: hair on end, eyes on stalks, the scream (the eyes came after the hair had dropped)
            *[k(round(TK9 + 0.067 * (i + 1), 3), toon={**SCARED, 'sq': [0.92, 1.11, 0.92] if i % 2 == 0 else [0.9, 1.15, 0.9]}, toonDur=0.033) for i in range(3)],   # held eight frames, shivering
            k(round(UP9 - 0.05, 3), toon={**SCARED, 'sq': [1.12, 0.84, 1.12]}, toonDur=0.04, toonEase='in'),
            k(UP9, to=[SEAT[0], 3.4, SEAT[2]], dur=0.18, glide=True, ease='in', face='keep'), k(UP9, toon={**SCARED, 'sq': [0.8, 1.35, 0.8], 'face': {'pop': 0.75, 'brow': 1, 'jaw': 0.6}}, toonDur=0.04)]),   # up he goes
        act('pompier1', [FR9[0], -0.9, FR9[2]], 0, 'stand', 'determined', keys=[k(0.0, look=[SEAT[0], 1.9, SEAT[2]]),
            k(round(BOO9 - 0.16, 3), to=FR9, dur=0.14, glide=True, ease='out', face='keep'),   # up from behind the sofa...
            k(BOO9, toon={'reach': {'L': [round(FR9[0] + 0.5, 3), 2.55, -3.05, 1, 0.05], 'R': [round(FR9[0] - 0.5, 3), 2.55, -3.05, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': {'jaw': 0.85, 'brow': -0.6}}, toonDur=0.05, toonEase='outBack'),   # ...arms up in a V beside his head: BOUH ! (crossed, they hid his scream)
            k(round(UP9 + 0.03, 3), look=[SEAT[0], 3.4, SEAT[2]]),
            k(round(UP9 + 0.03, 3), toon={'reach': {'L': [round(FR9[0] + 0.45, 3), 2.6, -3.05, 1, 0.05], 'R': [round(FR9[0] - 0.45, 3), 2.6, -3.05, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'bend': {'neck': [-0.45, 0, 0, 1, None]}, 'face': {'jaw': 0.5, 'brow': 0.9}}, toonDur=0.1),   # (pass 2) his head follows him up
            k(round(UP9 + 0.3, 3), toon={'touch': {'R': ['head', 0.0, 0.32, 0.05, 1, 0.06]}, 'hands': {'R': 'point'}, 'bend': {'neck': [-0.35, 0, 0, 1, None]}, 'face': {'brow': 0.9, 'jaw': 0.3}}, toonDur=0.2),   # then he scratches his head, still looking up
            k(round(UP9 + 0.52, 3), toon={'touch': {'R': ['head', 0.03, 0.34, 0.05, 1, 0.06]}, 'hands': {'R': 'point'}, 'bend': {'neck': [-0.35, 0, 0, 1, None]}, 'face': {'brow': 0.9, 'jaw': 0.3}}, toonDur=0.1),
            k(round(UP9 + 0.64, 3), toon={'touch': {'R': ['head', -0.02, 0.32, 0.05, 1, 0.06]}, 'hands': {'R': 'point'}, 'bend': {'neck': [-0.35, 0, 0, 1, None]}, 'face': {'brow': 0.9, 'jaw': 0.3}}, toonDur=0.1)])],
        props=[HIC('boo9', [FR9[0], 2.68, -3.0], [BOO9], w=0.66, text='BOUH !', inner=0.8, fit=0.52),   # (pass 3) between his raised hands, its spikes on his hair (it floated 340 px off in the corner), a rounder star (its spikes ate the « ! »)
               P('flakes9', 'waterDrops', pos=[SEAT[0], 3.15, round(SEAT[2] + 0.25, 3)], opts={'at': round(UP9 + 0.22, 3), 'n': 16, 'dir': [0, -1, 0], 'speed': 0.3, 'spread': 1.0, 'color': '#EFE8DA', 'r': 0.03, 'life': 1.0, 'g': 2.5})],   # (pass 2) plaster flakes from the ceiling he hit off the frame
        fx=[{'type': 'shake', 'at': round(UP9 + 0.2, 3), 'dur': 0.15, 'amount': 0.01}],
        cams=[FC(0.0, [0.3, 1.6, 0.6], [[SEAT[0], 3.0, SEAT[2]], [SEAT[0], 0.6, SEAT[2]], [round(FR9[0] - 0.7, 3), 3.05, -3.0], [round(SEAT[0] + 0.7, 3), 1.6, SEAT[2]]], top=0.1, bottom=0.74)])
st.cue('sfx:roar', 'S09', BOO9, 0.4); st.cue('whoosh', 'S09', UP9, 0.35, 0.25, 600, 2600); st.cue('thud', 'S09', round(UP9 + 0.2, 3), 0.35)

# 10: he stayed stuck to the ceiling. From the floor looking up: flat on the ceiling like a starfish, his face to us, deadpan; plaster dust drifting down;
#     the two firemen below look up, jaws dropping; a hiccup bumps him against the ceiling
D10 = st.dur('S10'); H10 = round(st.at('S10', 'L09', 3) + 0.05, 3); CEIL = 3.05
STAR = {'lay': [round(PI / 2, 4), 0], 'sq': [1.06, 1.0, 0.6], 'bend': {'armL': [0, 1.35, 0, 1, None], 'armR': [0, -1.35, 0, 1, None], 'legL': [0, 0.35, 0, 1, None], 'legR': [0, -0.35, 0, 1, None]}, 'hands': {'L': 'spread', 'R': 'spread'}}
ME10 = [0.0, round(CEIL - 0.2, 3), -3.0]                            # his feet; face down he lies toward +Z along the ceiling
st.shot('S10', 'livingRoom', setOpts=LR, actors=[
        act('mec', ME10, 0, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**STAR, 'face': {'lid': 0.5}}, toonDur=0.0),
            k(round(H10 - 0.05, 3), toon={**STAR, 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O'}}, toonDur=0.04),
            k(H10, toon={**STAR, 'sq': [1.32, 1.06, 0.22], 'face': {'lid': 0.3, 'brow': 0.35, 'mouth': 'O', 'jaw': 0.3}}, toonDur=0.03, toonEase='out'),   # (pass 2) the pancake: flattened into the plaster...
            k(H10, to=[ME10[0], round(ME10[1] + 0.08, 3), ME10[2]], dur=0.03, glide=True, face='keep'), k(round(H10 + 0.19, 3), to=ME10, dur=0.1, glide=True, face='keep'),
            k(round(H10 + 0.19, 3), toon={**STAR, 'sq': [0.9, 1.0, 1.0], 'face': {'lid': 0.2, 'brow': 0.5}}, toonDur=0.06, toonEase='outBack'),   # (pass 3) flat for six frames (four read as a bulge), then he pops back out, past his shape...
            k(round(H10 + 0.33, 3), toon={**STAR, 'sq': [1.04, 1.0, 0.5], 'face': {'lid': 0.4, 'brow': 0.3}}, toonDur=0.08),
            k(round(H10 + 0.45, 3), toon={**STAR, 'face': {'lid': 0.5, 'brow': 0.2}}, toonDur=0.12)]),   # ...to the starfish, bored
        # (pass 3) the firemen at the back, under his feet, looking up and toward us at him: their faces and dropped jaws turned to the lens (under his
        # chest, looking back up at him, they showed us the backs of their heads, and the right one had no head in the frame)
        act('pompier1', [-0.8, 0, -2.85], 12, 'stand', 'neutral', keys=[k(0.0, look=[-0.2, CEIL, -1.7]), k(0.6, look=[0.5, 1.9, -2.7]), k(0.95, look=[-0.2, CEIL, -1.7]), k(0.0, toon={'face': {'jaw': 0.8, 'brow': 0.8, 'eye': 0.25}}, toonDur=0.0)]),
        act('pompier2', [0.68, 0, -2.75], -12, 'stand', 'neutral', keys=[k(0.0, look=[0.2, CEIL, -1.6]), k(0.0, toon={'face': {'jaw': 0.6, 'brow': 0.9, 'eye': 0.3}}, toonDur=0.0), *react(H10, 0.8, look=[0.2, CEIL, -1.6], kind='wince')])],   # (pass 2) a wince under the flakes (no eye-pop)
        props=[P('ceil10', 'ceilingPlaster', pos=[0.0, round(CEIL + 0.02, 3), -3.1], rot=[round(PI / 2, 4), 0, 0], opts={'w': 7.0, 'h': 6.5, 'color': '#F7F2EA', 'rim': '#E2D8C8', 'cy': 0.62}),   # (pass 3) a pale plaster ceiling, evenly lit (lit by the room it came out brown, the darkest picture of the film)
               P('cracks10', 'ceilingCracks', pos=[0.0, round(CEIL + 0.012, 3), -2.05], rot=[round(PI / 2, 4), 0, 0], opts={'r': 1.45, 'n': 11, 'at': H10, 'thick': 3.2, 'edge': '#FFFDF8'}),   # (pass 3) thick dark cracks with a light chipped edge (1-2 px hairlines)
               *[P(f'flakes10{i}', 'waterDrops', pos=[x_, round(CEIL - 0.08, 3), z_], opts={'at': round(H10 + 0.02 + 0.03 * i, 3), 'n': 6, 'dir': [0, -1, 0], 'speed': 0.35, 'spread': 0.5, 'color': '#EDE6D8', 'r': 0.032, 'life': 1.0, 'g': 2.5})
                 for i, (x_, z_) in enumerate([(0.0, -0.95), (-1.05, -1.65), (1.05, -1.65), (-0.35, -2.95), (0.35, -2.95), (0.0, -2.05)])]],   # (pass 3) flakes from his outline and the cracks (from one point they made a ring of beads round his crotch)
        fx=[{'type': 'shake', 'at': H10, 'dur': 0.12, 'amount': 0.008}],
        cams=[FC(0.0, [0.25, 0.75, 0.9], [[-1.0, CEIL, -1.0], [1.0, CEIL, -3.2], [-0.8, 2.4, -2.85], [0.68, 2.45, -2.75], [-0.8, 1.55, -2.85], [0.95, 1.55, -2.75], [0.0, CEIL, -2.2]], top=0.1, bottom=0.78)])   # (pass 3) both firemen's heads whole
st.cue('thud', 'S10', 0.02, 0.4); st.cue('thud', 'S10', H10, 0.4); st.cue('clack', 'S10', round(H10 + 0.02, 3), 0.25)

# 11: yesterday the State declared him a natural disaster. His living room: an official in his tricolour sash pulls the red cloth off a bronze plaque over the
#     sofa: CATASTROPHE NATURELLE; proud, he turns to us; beside him a hiccup throws the man up and keeps him hanging there: the official's double take while
#     he is still in the air
D11 = st.dur('S11'); UNV11 = 0.55; H11 = 0.95; HG11 = 0.75; LAND11 = round(H11 + 2 * 0.15 + HG11 + 0.02, 3)
# (pass 3) the reveal at 0.55 s, not on « déclaré » (1.09 s: 0.9 s of a head turn before the arm reached the cloth), the hiccup at 0.95 s, and the time won
# goes to the hang (0.75 s, 1 m up: the feet clear the seat) and to the official's double take (a blank look at us of 0.25 s, then the eyes out 0.4 s)
PLAQ = [round(SEAT[0] - 0.8, 3), 1.75, -3.46]; PREF = [-1.45, 0, -2.3]; BASE11 = [round(SEAT[0] + 0.45, 3), 0, SEAT[2]]   # (pass 3) apart: his hand covered the last E of NATURELLE
st.shot('S11', 'livingRoom', setOpts={**LR, 'picture': False}, actors=[   # (pass 2) the plaque takes the painting's place
        act('mec', BASE11, 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=TIRED, toonDur=0.0), k(0.5, look=[PREF[0], 2.0, PREF[2]]), k(1.0, look='camera'),
            *HICK(H11, BASE11, 1.0, hang=HG11)]),   # (pass 3) a metre up, held 0.75 s (at 0.7 m his feet sat on the seat line: he seemed to stand on the sofa)
        act('prefet', PREF, 40, 'stand', 'happy', keys=[k(0.0, look=PLAQ), k(round(UNV11 - 0.2, 3), toon={'reach': {'R': [round(PLAQ[0] - 0.2, 3), 2.0, round(PLAQ[2] + 0.12, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.12),
            # (pass 3) a snap of the arm (a smear)
            k(UNV11, toon={'reach': {'R': [round(PLAQ[0] - 0.45, 3), 1.3, round(PLAQ[2] + 0.5, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.06, toonEase='out'), k(round(UNV11 + 0.15, 3), look='camera'), k(round(UNV11 + 0.3, 3), toon={'face': {'brow': 0.6}}, toonDur=0.15),
            *doubleTake(round(H11 + 0.2, 3), [BASE11[0], 2.5, BASE11[2]], blank=0.25, hold=0.4)])],   # (pass 3) a real blank beat before the snap (2-4 frames read as one take)
        props=[P('plaque11', 'bronzePlaque', pos=PLAQ, opts={'text': 'CATASTROPHE/NATURELLE', 'w': 1.1, 'h': 0.42}),
               P('veil11', 'unveilCloth', pos=[PLAQ[0], PLAQ[1], round(PLAQ[2] + 0.06, 3)], opts={'w': 1.3, 'h': 0.62, 'color': '#B5302A', 'at': UNV11, 'dur': 0.3},   # (pass 3) a soft cloth with folds that crumples as it goes (the flat sheet read as a stiff slab)
                 keys=[k(UNV11, to=[round(PLAQ[0] - 0.5, 3), 0.35, round(PLAQ[2] + 0.55, 3)], dur=0.3, ease='in'), k(UNV11, rotTo=[0.35, 0.2, 1.1], dur=0.3, ease='in'), k(round(UNV11 + 0.32, 3), visible=False)]),   # (pass 2) a thin red cloth sliding off (the box read as a stiff cream crate)
               P('sash11', 'sash', on={'actor': 'prefet', 'joint': 'torso', 'offset': [0.0, 0.3, 0.13], 'rot': [0, 0, 0.8]}, opts={'len': 0.78, 'w': 0.11})],   # (pass 2) the tricolour sash: an official, not a second hero
        cams=[FC(0.0, [0.2, 1.6, 1.1], [[PLAQ[0] - 0.6, 2.05, PLAQ[2]], [PLAQ[0] + 0.6, 1.5, PLAQ[2]], [PREF[0], 2.35, PREF[2]], [BASE11[0], 2.8, BASE11[2]], [BASE11[0], 0.4, BASE11[2]], [PREF[0], 0.4, PREF[2]]], top=0.24, bottom=0.74)])   # (pass 2) the top of his jump under the card band
st.cue('sfx:paper', 'S11', UNV11, 0.3); st.cue('sfx:boing', 'S11', H11, 0.35); st.cue('thud', 'S11', LAND11, 0.25)
st.card('S11', 'CATASTROPHE NATURELLE', at=round(st.at('S11', 'L10', 3) + 0.14, 3))   # (pass 3) still with the words (1.21 s), not with the earlier reveal

# 12: his insurance paid him three thousand euros. The insurer, three-quarters to us, holds out a giant cheque, 3 000 €; the man takes it by its corner,
#     deadpan; on « euros » a hiccup throws him up a metre; the cheque left behind in the air flutters down after him; the insurer's jaw drops, his hand
#     still held out
D12 = st.dur('S12'); GIVE12 = round(st.at('S12', 'L11', 4) - 0.05, 3); H12 = round(st.at('S12', 'L11', 7) + 0.05, 3)
ASS = [1.25, 0, -2.3]; CHQA = [0.62, 1.0, -2.08]; CHQB = [0.5, 0.98, -2.15]
GIVEH = {'reach': {'R': [round(CHQA[0] + 0.45, 3), CHQA[1], round(CHQA[2] + 0.02, 3), 1, 0.05]}, 'hands': {'R': 'pinch'}}
TAKEH = {'reach': {'L': [round(CHQB[0] - 0.45, 3), CHQB[1], round(CHQB[2] + 0.02, 3), 1, 0.05]}, 'hands': {'L': 'pinch'}}
EMPTY = {'reach': {'R': [0.98, 1.08, -2.02, 1, 0.05]}, 'hands': {'R': 'flat'}}
st.shot('S12', 'livingRoom', setOpts=LR, actors=[
        act('mec', SEAT, 25, 'sit', 'unimpressed', keys=[k(0.0, look=[CHQA[0], 1.05, CHQA[2]]), k(0.0, toon=TIRED, toonDur=0.0), k(0.35, toon={**TIRED, 'face': {'lid': 1.0, 'shadow': 0.6}}, toonDur=0.05), k(0.46, toon=TIRED, toonDur=0.07), k(0.55, look='camera'),   # (pass 2) turned three-quarters to us (in profile his face was gone)
            k(round(GIVE12 - 0.1, 3), toon={**TAKEH, **TIRED}, toonDur=0.12), k(round(GIVE12 - 0.1, 3), look=[CHQB[0], 1.05, CHQB[2]]), k(round(GIVE12 + 0.3, 3), look='camera'),
            k(round(GIVE12 + 0.42, 3), toon={**TAKEH, 'face': {'lid': 1.0, 'shadow': 0.6}}, toonDur=0.05), k(round(GIVE12 + 0.52, 3), toon={**TAKEH, **TIRED}, toonDur=0.07),
            *HICK(H12, SEAT, 1.0, keep={'reach': {'L': [round(CHQB[0] - 0.45, 3), round(CHQB[1] + 0.45, 3), CHQB[2], 0.6, 0.05]}, 'hands': {'L': 'pinch'}})]),
        # (pass 3) turned to us (-22 degrees) and his eyes do the looking at the man (his head turned to him showed us only an ear and stubble)
        act('assureur', ASS, -22, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon={**GIVEH, 'face': {'gx': -0.8}}, toonDur=0.0), k(0.75, look=[CHQA[0], 1.2, CHQA[2]]), k(1.05, look='camera'),
            k(0.3, toon={**GIVEH, 'sq': [1.0, 1.03, 1.0], 'face': {'brow': 0.5}}, toonDur=0.15),   # he beams at us, the cheque held out
            k(round(GIVE12 + 0.15, 3), toon=EMPTY, toonDur=0.1),   # lets go, the hand stays out
            k(round(H12 + 0.06, 3), toon={**EMPTY, 'face': {'jaw': 0.85, 'brow': 0.95, 'eye': 0.3, 'gx': -0.9, 'gy': -0.8}}, toonDur=0.05, toonEase='out'), k(round(H12 + 0.06, 3), look='camera'),   # (pass 3) the jaw drops at us, the eyes up after him...
            k(round(H12 + 0.45, 3), toon={**EMPTY, 'sq': [1.06, 0.92, 1.06], 'lay': [-0.12, 0], 'face': {'jaw': 0.6, 'brow': 0.9, 'lid': 0.8, 'gx': -0.6}}, toonDur=0.04, toonEase='out'),   # ...and he flinches at the crash (the landing at H12 + 0.45)
            k(round(H12 + 0.54, 3), toon={**EMPTY, 'face': {'jaw': 0.5, 'brow': 0.7, 'gx': -0.7, 'gy': 0.3}}, toonDur=0.1)])],
        props=[P('chq12', 'bigCheque', pos=CHQA, face='camera', opts={'w': 1.0, 'h': 0.46, 'amount': '3 000 €', 'text': 'ASSURANCE', 'flutter': round(H12 + 0.12, 3)},
                 keys=[k(GIVE12, to=CHQB, dur=0.15, ease='inOut'), k(H12, to=[round(CHQB[0] - 0.05, 3), round(CHQB[1] + 0.45, 3), CHQB[2]], dur=0.12, ease='out'),
                       k(round(H12 + 0.2, 3), to=[round(CHQB[0] + 0.2, 3), 0.35, round(CHQB[2] + 0.25, 3)], dur=0.75, ease='inOut')])],   # (pass 2) a giant novelty cheque (3 000 € was 7 px); left in the air, it flutters down after him
        cams=[FC(0.0, [0.5, 1.5, 1.0], [[SEAT[0], 3.3, SEAT[2]], [SEAT[0], 0.4, SEAT[2]], [ASS[0], 2.35, ASS[2]], [ASS[0], 0.4, ASS[2]], [round(ASS[0] + 0.4, 3), 2.2, ASS[2]], [round(ASS[0] + 0.4, 3), 1.5, ASS[2]], [round(SEAT[0] - 0.55, 3), 1.8, SEAT[2]], [round(CHQA[0] + 0.55, 3), 1.0, CHQA[2]]], top=0.1, bottom=0.74)])
st.cue('sfx:paper', 'S12', GIVE12, 0.3); st.cue('sfx:cash', 'S12', round(GIVE12 + 0.1, 3), 0.25); st.cue('sfx:boing', 'S12', H12, 0.35); st.cue('sfx:paper', 'S12', round(H12 + 0.25, 3), 0.2)

# 13: since then he drinks nothing but soda. A medium close on him on his sofa, the camera pushing in slowly; soda pyramids in the foreground at the edges;
#     he sips from a can through a bendy straw, deadpan at us; on « soda » one more hiccup lifts him a little with the can; he nods off and jerks awake
D13 = st.dur('S13'); H13 = round(st.at('S13', 'L12', 7) + 0.05, 3)
CAN = {'touch': {'R': ['face', 0.12, -1.25, 0.2, 1, 0.04]}, 'hands': {'R': 'grip'}}     # (pass 2) the can at his chest, the straw up in sight (at his mouth the can hid the straw and his mouth)
SIP = {'touch': {'R': ['face', 0.04, -0.75, 0.15, 1, 0.04]}, 'hands': {'R': 'grip'}}    # the straw at his lips, the can under his chin (probe: at -0.3 the can hid 5/9 of his face)
st.shot('S13', 'livingRoom', setOpts=LR, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**CAN, **TIRED}, toonDur=0.0),
            *[x for t_ in (0.25, 0.85) for x in (k(t_, toon={**SIP, 'bend': {'neck': [-0.15, 0, 0, 1, None]}, 'face': {'lid': 0.8, 'shadow': 0.6, 'mouth': 'kiss'}}, toonDur=0.14, toonEase='inOut'),
                                              k(round(t_ + 0.4, 3), toon={**CAN, **TIRED}, toonDur=0.14, toonEase='inOut'))],   # sips: the can up to the straw, the eyes half shut, back down
            *HICK(H13, SEAT, 0.12, keep=CAN),   # (pass 3) a small one: a quarter of the S01 jolt (at 0.35 his head went as high as S01's)
            k(round(D13 - 0.72, 3), toon={**CAN, 'face': {'lid': 1, 'shadow': 0.6}, 'bend': {'neck': [0.38, 0, 0, 1, None]}}, toonDur=0.3, toonEase='in'), k(round(D13 - 0.3, 3), toon={**CAN, **TIRED, 'face': {'lid': 0.3, 'shadow': 0.6, 'brow': 0.4}}, toonDur=0.06, toonEase='out')]),   # he nods off again and jerks awake (the bookend of S01)
        ],
        props=[P('can13', 'sodaCan', on={'actor': 'mec', 'hand': 'R', 'offset': [0, -0.1, 0.05], 'face': 'camera', 'faceFlat': True}, scale=1.6, opts={'color': '#C8202A', 'text': 'SODA'}),   # (pass 2b) upright and its straw up, turned to us (the hand laid it on its side)
               P('stack13', 'sodaStack', pos=[-0.66, 0.5, -2.9], scale=0.85, opts={'rows': 4, 'cols': 4, 'pyramid': True}),   # (pass 3) two full pyramids on the cushions at his
               P('stack13g', 'sodaStack', pos=[0.66, 0.5, -2.9], scale=0.85, opts={'rows': 4, 'cols': 4, 'pyramid': True}),   # sides (on the floor they showed as cut slivers in the corners)
               HIC('hic13', [0.42, 2.2, -2.55], [H13], w=0.38)],
        cams=[FC(0.0, [0.15, 1.35, 0.2], [[SEAT[0], 2.45, SEAT[2]], [SEAT[0], 0.5, round(SEAT[2] + 0.45, 3)], [-0.62, 1.4, SEAT[2]], [0.62, 1.4, SEAT[2]]], top=0.1, bottom=0.76, drift=(0.0, -0.03, -0.3))])   # (pass 2b) knees up, room for the hop, pushing in (his head was 7 % of the frame; the first close-up cut it)
st.cue('sfx:pour', 'S13', 0.2, 0.2); st.cue('sfx:boing', 'S13', H13, 0.3)

# (cycle 13) the key poses, measured in the engine by render3 --probe (head in the frame, big enough, not covered, clear of the caption band and the card)
for g_ in [('S01', 1.65, 'mec', 'hic1'), ('S02', 0.68, 'mec', 'top1'), ('S02', 1.9, 'mec', 'top2'), ('S03', 1.25, 'savant', 'nose_down'), ('S03', 1.6, 'savant', 'take'), ('S06', 1.25, 'mamie', 'jolt'),
           ('S07', 1.8, 'mec', 'cordon_jump'), ('S08', 1.69, 'mec', 'glass_up'), ('S09', 0.72, 'mec', 'scream'), ('S10', 0.81, 'mec', 'pancake'),
           ('S11', 1.8, 'mec', 'hang'), ('S11', 1.95, 'prefet', 'double_take'), ('S12', 0.6, 'assureur', 'beam'), ('S12', 1.82, 'mec', 'cheque_jump'), ('S13', 0.4, 'mec', 'sip'), ('S13', 1.65, 'mec', 'last_hic')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
for t_ in [('S02', 0.68, 'ruler2', '1M'), ('S04', 0.6, 'map4', 'magnitude'), ('S05', 1.3, 'map5', 'canape'), ('S07', 1.0, 'cordon7', 'epicentre'), ('S11', 1.6, 'plaque11', 'plaque'), ('S12', 0.6, 'chq12', 'cheque')]:
    st.text(t_[0], t_[1], t_[2], t_[3])   # (pass 2) the lettering that must read
st.write("Le hoquet", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={   # (pass 2) hairRest: still heads keep their hair block
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'savant': {'preset': 'savant', 'seed': 501, 'hair': 'receding', 'hairColor': '#A9AEB6', 'build': {'width': 0.92, 'headWidth': 1.25}},   # (pass 3) grey hair (white on the cream wall: no edge)
    'flic': {'preset': 'cop', 'seed': 502, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'voisine': {'preset': 'madame', 'seed': 503, 'suit': '#4F7F3A', 'build': {'width': 0.9, 'headWidth': 1.25}},
    'mamie': {'preset': 'mamie', 'seed': 504, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'gamin': {'preset': 'gamin', 'seed': 505},
    'voisin': {'preset': 'worker', 'seed': 506, 'hat': None, 'build': {'width': 0.95, 'headWidth': 1.2}},
    'pompier1': {'preset': 'pompier', 'seed': 507, 'hat': 'firecrest', 'bandColor': '#EEF1F4', 'bandH': 0.05, 'build': {'width': 1.0, 'headWidth': 1.25}},   # (pass 2) bright reflective bands
    'pompier2': {'preset': 'pompier', 'seed': 508, 'hat': 'firecrest', 'bandColor': '#EEF1F4', 'bandH': 0.05, 'build': {'width': 0.95, 'headWidth': 1.25}},   # (pass 3) a fireman's helmet (the red box read as a cap)
    'prefet': {'preset': 'politique', 'seed': 509, 'suit': '#6E737A', 'build': {'width': 0.95, 'headWidth': 1.25}},   # (pass 2) a grey suit (in navy he read as a second hero)
    'assureur': {'preset': 'boss', 'seed': 510, 'build': {'width': 0.95, 'headWidth': 1.25}},
})
