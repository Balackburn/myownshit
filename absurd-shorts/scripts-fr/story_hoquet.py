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

LR = {'tv': False}                                                  # the living room, the sofa against the back wall (its seat at 0.5 m)
SEAT = [0.0, 0, -2.75]                                              # where he sits on the sofa (the sit clip drops the hips onto the seat)
TIRED = {'face': {'lid': 0.55, 'shadow': 0.6}}                      # three days of hiccups: heavy lids, rings under the eyes
def HICK(t, base, h=1.0, keep=None):
    """A hiccup: a gather (squash), up h metres stretched, the top held four frames (hang time), the fall, a squash on landing. keep: toon channels to
    carry (a reach, a held can). (pass 1b) His face stays bored through it (cheeks puffing, a « hic » mouth, heavy lids at the top): the violence is in
    the body, not in the eyes; the eyes-on-stalks take is kept for the fright (S09) and the official's double take (S11)."""
    kp = dict(keep or {}); up = [base[0], round(base[1] + h, 3), base[2]]; fl = round(0.1 + 0.05 * h, 3)
    return [k(round(t - 0.06, 3), toon={**kp, 'sq': [1.1, 0.86, 1.1], 'face': {'puff': 0.55, 'lid': 0.45, 'brow': 0.1, 'mouth': 'kiss'}}, toonDur=0.05, toonEase='in'),   # the gather
            k(t, to=up, dur=fl, glide=True, ease='out', face='keep'), k(t, toon={**kp, 'sq': [0.86, 1.2, 0.86], 'face': {'lid': 0.5, 'brow': 0.15, 'mouth': 'O', 'jaw': 0.3}}, toonDur=0.04, toonEase='out'),   # up, stretched
            k(round(t + fl, 3), toon={**kp, 'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.62, 'brow': 0.0, 'shadow': 0.6}}, toonDur=0.06),   # the top, held
            k(round(t + fl + 0.13, 3), to=list(base), dur=fl, glide=True, ease='in', face='keep'), k(round(t + fl + 0.16, 3), toon={**kp, 'sq': [0.95, 1.06, 0.95]}, toonDur=0.05),   # the fall
            k(round(t + 2 * fl + 0.13, 3), toon={**kp, 'sq': [1.12, 0.86, 1.12], 'face': {'lid': 0.5}}, toonDur=0.03, toonEase='out'),   # landed
            k(round(t + 2 * fl + 0.22, 3), toon={**kp, **TIRED}, toonDur=0.1)]
HIC = lambda pid, pos, times, w=0.5, **o: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': list(times), 'w': w, **o})

# 1: the hook. Close on him on his sofa, three days without sleep: a small jolt on « hoquet », HIC !, then a bigger one that lifts him off the seat
D1 = st.dur('S01'); H1a = round(st.at('S01', 'L01', 4) + 0.02, 3); H1b = round(st.at('S01', 'L01', 7) + 0.05, 3)
st.shot('S01', 'livingRoom', setOpts=LR, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=TIRED, toonDur=0.0), *HICK(H1a, SEAT, 0.14), *HICK(H1b, SEAT, 0.42)])],
        props=[HIC('hic1', [0.42, 2.25, -2.6], [H1a, H1b], w=0.42)],
        cams=[FC(0.0, [0.25, 1.55, -0.6], [[SEAT[0], 2.75, SEAT[2]], [SEAT[0], 1.05, SEAT[2]], [round(SEAT[0] - 0.5, 3), 1.9, SEAT[2]], [round(SEAT[0] + 0.62, 3), 2.3, SEAT[2]]], top=0.14, bottom=0.72, drift=(0.0, 0.0, -0.08))])
st.cue('sfx:gulp', 'S01', H1a, 0.3); st.cue('sfx:boing', 'S01', H1b, 0.3)

# 2: at each hiccup he jumps a metre. Wider, room above him: two hiccups, each a metre straight up off the sofa, hang time at the top, squash on landing
D2 = st.dur('S02'); H2a = round(st.at('S02', 'L02', 2) + 0.02, 3); H2b = round(st.at('S02', 'L02', 8) + 0.02, 3)
st.shot('S02', 'livingRoom', setOpts=LR, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=TIRED, toonDur=0.0), *HICK(H2a, SEAT, 1.0), *HICK(H2b, SEAT, 1.0)])],
        props=[HIC('hic2', [0.55, 3.15, -2.6], [H2a, H2b], w=0.5), P('mark2', 'paperSheet', pos=[-0.95, 2.62, -3.42], opts={'w': 0.34, 'h': 0.2, 'big': '1 m', 'paper': '#F6E27A', 'bright': True})],   # a mark on the wall at the height of his jump
        cams=[FC(0.0, [0.3, 1.7, 1.2], [[SEAT[0], 3.65, SEAT[2]], [SEAT[0], 0.3, SEAT[2]], [-1.25, 2.0, SEAT[2]], [1.25, 2.0, SEAT[2]]], top=0.1, bottom=0.74, drift=(0.0, 0.0, -0.1))])
st.cue('sfx:boing', 'S02', H2a, 0.35); st.cue('thud', 'S02', round(H2a + 0.43, 3), 0.25); st.cue('sfx:boing', 'S02', H2b, 0.35); st.cue('thud', 'S02', round(H2b + 0.43, 3), 0.25)

# 3: the seismographs detected an earthquake. The lab: the drum turns, the pen writes a calm line, then scribbles a spike at each hiccup, the second one
#    so big the pen jumps off the paper; the seismologist leans in, then his eyes shoot out on stalks
D3 = st.dur('S03'); SP3a = round(st.at('S03', 'L03', 1) + 0.1, 3); SP3b = round(st.at('S03', 'L03', 5) - 0.05, 3)
BENCH = [0.0, 0, -2.2]; SEIS = [0.0, 0.76, -2.2]; SAV = [0.1, 0, -2.85]
st.shot('S03', 'office', setOpts={'door': False}, actors=[
        act('savant', SAV, 0, 'stand', 'neutral', keys=[k(0.0, look=[SEIS[0], 0.9, round(SEIS[2] + 0.1, 3)]), k(0.0, toon={'bend': {'spine': [0.25, 0, 0, 1, None]}}, toonDur=0.0),
            k(round(SP3a + 0.05, 3), toon={'bend': {'spine': [0.4, 0, 0, 1, None]}, 'face': {'brow': 0.6}}, toonDur=0.15),   # he leans in to the trace
            *take(round(SP3b + 0.06, 3), 'stalks', keep={'bend': {'spine': [0.1, 0, 0, 1, None]}}, hold=0.35)])],
        props=[P('bench3', 'desk', pos=BENCH), P('seis3', 'seismograph', pos=SEIS, opts={'spikes': [[SP3a, 0.7], [SP3b, 1.45]]})],
        cams=[FC(0.0, [0.55, 1.45, -0.5], [[SEIS[0], 1.15, round(SEIS[2] + 0.35, 3)], [SAV[0], 2.4, SAV[2]], [round(SEIS[0] - 0.5, 3), 0.75, round(SEIS[2] + 0.3, 3)], [round(SEIS[0] + 0.5, 3), 0.75, round(SEIS[2] + 0.3, 3)]], top=0.12, bottom=0.74, drift=(-0.03, 0, -0.06))])
st.cue('sfx:needle', 'S03', SP3a, 0.3); st.cue('sfx:needle', 'S03', SP3b, 0.4); st.cue('pop', 'S03', round(SP3b + 0.06, 3), 0.25)

# 4: magnitude four. The wall screen: a city map, MAGNITUDE 4 in red; rings pulse out from a red dot; the seismologist points at it, his arm stretching
D4 = st.dur('S04'); MAPW = [-0.2, 1.7, -3.5]
st.shot('S04', 'office', setOpts={'door': False}, actors=[
        act('savant', [1.05, 0, -2.75], -35, 'stand', 'neutral', keys=[k(0.0, look=[MAPW[0], 1.8, MAPW[2]]), k(0.15, toon={'reach': {'R': [round(MAPW[0] + 0.2, 3), 1.62, round(MAPW[2] + 0.08, 3), 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.1, 'face': {'brow': 0.8, 'eye': 0.3}}, toonDur=0.12, toonEase='outBack'),
            k(0.75, look='camera')])],
        props=[P('map4', 'quakeMap', pos=MAPW, opts={'w': 1.6, 'h': 1.0, 'head': 'MAGNITUDE 4', 'label': 'CANAPÉ', 'pulses': [0.15, 0.6, 1.05]})],
        cams=[FC(0.0, [0.4, 1.7, 0.4], [[MAPW[0] - 0.85, 2.25, MAPW[2]], [MAPW[0] + 0.85, 1.15, MAPW[2]], [1.05, 2.4, -2.75], [1.05, 1.0, -2.75]], top=0.12, bottom=0.72)])
st.cue('sfx:beep', 'S04', 0.15, 0.3)

# 5: epicentre: his sofa. Close on the map: it zooms in on the red dot, CANAPÉ, the rings pulsing out from it
D5 = st.dur('S05')
st.shot('S05', 'office', setOpts={'door': False}, actors=[],
        props=[P('map5', 'quakeMap', pos=MAPW, opts={'w': 1.6, 'h': 1.0, 'head': 'MAGNITUDE 4', 'label': 'CANAPÉ', 'pulses': [0.1, 0.45], 'zoom': [[0.05, 3.0]]})],
        cams=[cam(0.0, [MAPW[0], 1.7, -2.15], [MAPW[0], 1.7, -2.4], [MAPW[0], 1.7, MAPW[2]], [MAPW[0], 1.7, MAPW[2]], lens=38)])
st.cue('sfx:zip', 'S05', 0.05, 0.25)

# 6: the prefecture evacuated the whole building. In the street at the foot of his block: a policeman blows his whistle and waves; the neighbours file out of
#    the door one after another with their bags; a hiccup upstairs: the whole facade jolts, the neighbours hop
D6 = st.dur('S06'); H6 = round(st.at('S06', 'L05', 4) - 0.05, 3)
FX6 = 8.6; DOOR6 = [round(FX6 - 0.05, 3), 0, 30.0]; STREET = {'clear': [-80, 80], 'eiffel': False, 'paveW': 6.5}
FLATS6 = P('flats6', 'flatsWall', pos=[FX6, 0, 30.0], ry=-90, opts={'w': 6.0, 'h': 12.6, 'cols': 3, 'rows': 3, 'depth': 1.25, 'y0': 3.0}, keys=[k(H6, squash=[1.0, 1.03, 1.0], dur=0.0), k(round(H6 + 0.06, 3), squash=[1.0, 0.985, 1.0], dur=0.0), k(round(H6 + 0.14, 3), squash=[1, 1, 1], dur=0.08)])
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
        props=[FLATS6, *BAGS6, P('door6', 'door', pos=DOOR6, ry=-90, opts={'w': 1.3, 'h': 2.5, 'open': 1}), P('whistle6', 'whistle', on={'actor': 'flic', 'hand': 'R', 'offset': [0, 0.02, 0.04]})],
        fx=[{'type': 'shake', 'at': H6, 'dur': 0.18, 'amount': 0.01}],
        cams=[FC(0.0, [3.4, 1.7, 25.6], [[FX6, 4.2, 30.0], [round(FX6 - 2.6, 3), 0.0, 28.4], [round(FX6 - 1.6, 3), 2.3, 31.3], [round(FX6 - 0.6, 3), 0.0, 30.0]], top=0.12, bottom=0.74, drift=(0.06, 0, -0.08))])
st.cue('sfx:whistle', 'S06', 0.2, 0.35); st.cue('thud', 'S06', H6, 0.4); [st.cue('sfx:stepRun', 'S06', round(nb[1] + 0.2, 3), 0.2) for nb in NEIGH]

# 7: except him: one does not evacuate an epicentre. From above, his living room: red rings on the floor round the sofa, a police cordon ÉPICENTRE round
#    it; he sits alone, deadpan; a hiccup: up a metre, the tape jumps, the rings flash
D7 = st.dur('S07'); H7 = round(st.at('S07', 'L06', 6) + 0.05, 3)
st.shot('S07', 'livingRoom', setOpts={**LR, 'carpet': False}, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=TIRED, toonDur=0.0), k(0.8, look=[SEAT[0], 0.9, round(SEAT[2] + 1.0, 3)]), k(1.3, look='camera'), *HICK(H7, SEAT, 1.0)])],
        props=[P('rings7', 'quakeRings', pos=[SEAT[0], 0, round(SEAT[2] + 0.2, 3)], opts={'r': 2.2, 'n': 4, 'pulses': [0.1, H7]}),
               P('cordon7', 'cordon', pos=[SEAT[0], 0, round(SEAT[2] + 0.15, 3)], opts={'w': 3.0, 'd': 1.7, 'sign': 'ÉPICENTRE', 'signW': 1.0, 'signH': 0.3, 'jumps': [[H7, 1.0]]})],
        cams=[FC(0.0, [1.4, 4.2, 1.0], [[SEAT[0], 3.4, SEAT[2]], [-1.6, 0.0, round(SEAT[2] + 1.0, 3)], [1.6, 0.0, round(SEAT[2] + 1.0, 3)], [-1.6, 0.0, round(SEAT[2] - 0.75, 3)], [1.6, 0.0, round(SEAT[2] - 0.75, 3)]], top=0.1, bottom=0.74, drift=(0.0, -0.05, -0.08))])   # (pass 1b) framed on the cordon, not on the back wall: the man was 23 % of the frame
st.cue('sfx:boing', 'S07', H7, 0.35); st.cue('thud', 'S07', round(H7 + 0.43, 3), 0.25)

# 8: the firemen tried the glass of water upside down. Two firemen fold him over at the waist; one holds the glass to his lips, upside down; on « envers »
#    a hiccup throws him up out of their hands, the water flies
D8 = st.dur('S08'); H8 = round(st.at('S08', 'L07', 8) + 0.05, 3)
ME8 = [0.0, 0, -1.6]; BENT = {'bend': {'spine': [1.15, 0, 0, 1, None], 'neck': [-0.35, 0, 0, 1, None]}}
MOUTH8 = OFF(ME8, 0, 0.55, 0.0, 1.32)
st.shot('S08', 'livingRoom', setOpts=LR, actors=[
        act('mec', ME8, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[MOUTH8[0], 1.1, MOUTH8[2]]), k(0.0, toon={**BENT, **TIRED}, toonDur=0.0),
            *[x for t_ in (0.4, 0.8, 1.18) for x in (k(t_, toon={**BENT, 'face': {**TIRED['face'], 'puff': 0.55}}, toonDur=0.06), k(round(t_ + 0.16, 3), toon={**BENT, **TIRED}, toonDur=0.08))],   # (pass 1b) gulps, upside down
            k(round(H8 - 0.06, 3), toon={**BENT, 'sq': [1.08, 0.88, 1.08], 'face': {'eye': 0.3, 'mouth': 'O'}}, toonDur=0.05, toonEase='in'),
            k(H8, to=[ME8[0], 0.6, ME8[2]], dur=0.12, glide=True, ease='out', face='keep'), k(H8, toon={'sq': [0.86, 1.2, 0.86], 'face': {'puff': 1.0, 'lid': 0.25, 'brow': 0.7, 'mouth': 'kiss'}}, toonDur=0.04, toonEase='out'),   # up out of their hands, his cheeks full of water
            k(round(H8 + 0.25, 3), to=ME8, dur=0.12, glide=True, ease='in', face='keep'), k(round(H8 + 0.37, 3), toon={'sq': [1.1, 0.88, 1.1], 'face': {'lid': 0.5}}, toonDur=0.03), k(round(H8 + 0.46, 3), toon=TIRED, toonDur=0.1)]),
        act('pompier1', [round(ME8[0] - 0.62, 3), 0, round(ME8[2] - 0.1, 3)], 60, 'stand', 'determined', keys=[k(0.0, look=[ME8[0], 1.3, ME8[2]]), k(0.55, look=[round(ME8[0] + 0.7, 3), 1.6, round(ME8[2] + 0.55, 3)]), k(1.0, look=[ME8[0], 1.3, ME8[2]]), k(0.0, toon={'reach': {'L': [round(ME8[0] - 0.12, 3), 1.5, round(ME8[2] - 0.15, 3), 1, 0.05], 'R': [round(ME8[0] - 0.05, 3), 1.25, round(ME8[2] + 0.1, 3), 1, 0.05]}, 'hands': {'L': 'flat', 'R': 'flat'}}, toonDur=0.0),   # holding him folded
            *react(H8, 0.8, look=[ME8[0], 1.9, ME8[2]])]),
        act('pompier2', [round(ME8[0] + 0.7, 3), 0, round(ME8[2] + 0.55, 3)], -100, 'stand', 'neutral', keys=[k(0.0, look=MOUTH8), k(0.7, look='camera'), k(1.1, look=MOUTH8), k(0.0, toon={'reach': {'R': [MOUTH8[0], MOUTH8[1], round(MOUTH8[2] + 0.04, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.0),   # the glass at his lips, upside down
            *react(H8, 0.8, look=[ME8[0], 1.9, ME8[2]])])],
        props=[P('glass8', 'waterGlass', on={'actor': 'pompier2', 'hand': 'R', 'offset': [0, 0.02, 0.04], 'rot': [PI, 0, 0]}, scale=1.5, opts={'level': 0.6}),
               P('splash8', 'dustPuff', pos=[MOUTH8[0], MOUTH8[1], MOUTH8[2]], scale=0.5, opts={'once': True, 'startAt': H8, 'period': 0.45, 'color': '#BFE3F5'}, keys=[k(0.0, visible=False), k(H8, visible=True), k(round(H8 + 0.45, 3), visible=False)])],
        cams=[FC(0.0, [-1.3, 1.5, 1.6], [[ME8[0], 2.3, ME8[2]], [round(ME8[0] - 0.62, 3), 2.4, ME8[2]], [round(ME8[0] + 0.7, 3), 2.4, round(ME8[2] + 0.55, 3)], [ME8[0], 0.3, ME8[2]], [ME8[0], 3.45, ME8[2]]], top=0.08, bottom=0.74)])   # (pass 1b, probe) the top of the jump in the frame: 44 % of his head left by the top
st.cue('sfx:pour', 'S08', 0.3, 0.25); st.cue('sfx:splash', 'S08', H8, 0.4)

# 9: then the big fright. On the sofa, deadpan: a fireman springs up behind the sofa, arms high, BOUH !; his hair stands on end, eyes out on stalks, and up he
#    goes out of the top of the frame
D9 = st.dur('S09'); BOO9 = round(st.at('S09', 'L08', 2) - 0.1, 3); UP9 = round(BOO9 + 0.42, 3)
st.shot('S09', 'livingRoom', setOpts=LR, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=TIRED, toonDur=0.0), *take(round(BOO9 + 0.04, 3), 'hair', hold=0.3),
            k(round(UP9 - 0.05, 3), toon={'sq': [1.12, 0.84, 1.12], 'hairUp': 1, 'face': {'pop': 0.6, 'brow': 1}}, toonDur=0.04, toonEase='in'),
            k(UP9, to=[SEAT[0], 3.4, SEAT[2]], dur=0.18, glide=True, ease='in', face='keep'), k(UP9, toon={'sq': [0.8, 1.35, 0.8], 'hairUp': 1, 'face': {'pop': 0.6, 'brow': 1, 'jaw': 0.4}}, toonDur=0.04)]),   # up he goes
        act('pompier1', [round(SEAT[0] + 0.55, 3), -0.9, -3.3], 0, 'stand', 'determined', keys=[k(0.0, look=[SEAT[0], 1.9, SEAT[2]]),
            k(round(BOO9 - 0.16, 3), to=[round(SEAT[0] + 0.55, 3), 0, -3.3], dur=0.14, glide=True, ease='out', face='keep'),   # up from behind the sofa...
            k(BOO9, toon={'reach': {'L': [round(SEAT[0] + 0.2, 3), 2.7, -3.0, 1, 0.05], 'R': [round(SEAT[0] + 0.95, 3), 2.7, -3.0, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': {'jaw': 0.8, 'brow': -0.6}}, toonDur=0.05, toonEase='outBack')])],   # ...arms high: BOUH !
        props=[HIC('boo9', [round(SEAT[0] + 0.85, 3), 2.9, -3.0], [BOO9], w=0.62, text='BOUH !')],
        cams=[FC(0.0, [0.3, 1.6, 0.6], [[SEAT[0], 3.0, SEAT[2]], [SEAT[0], 0.6, SEAT[2]], [round(SEAT[0] + 1.0, 3), 3.0, -3.0], [round(SEAT[0] - 0.7, 3), 1.6, SEAT[2]]], top=0.1, bottom=0.74)])
st.cue('sfx:roar', 'S09', BOO9, 0.4); st.cue('whoosh', 'S09', UP9, 0.35, 0.25, 600, 2600)

# 10: he stayed stuck to the ceiling. From the floor looking up: flat on the ceiling like a starfish, his face to us, deadpan; plaster dust drifting down;
#     the two firemen below look up, jaws dropping; a hiccup bumps him against the ceiling
D10 = st.dur('S10'); H10 = round(st.at('S10', 'L09', 3) + 0.05, 3); CEIL = 3.05
STAR = {'lay': [round(PI / 2, 4), 0], 'sq': [1.06, 1.0, 0.6], 'bend': {'armL': [0, 1.35, 0, 1, None], 'armR': [0, -1.35, 0, 1, None], 'legL': [0, 0.35, 0, 1, None], 'legR': [0, -0.35, 0, 1, None]}, 'hands': {'L': 'spread', 'R': 'spread'}}
ME10 = [0.0, round(CEIL - 0.2, 3), -3.0]                            # his feet; face down he lies toward +Z along the ceiling
st.shot('S10', 'livingRoom', setOpts=LR, actors=[
        act('mec', ME10, 0, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**STAR, 'face': {'lid': 0.5}}, toonDur=0.0),
            k(round(H10 - 0.05, 3), toon={**STAR, 'face': {'lid': 0.0, 'eye': 0.3, 'mouth': 'O'}}, toonDur=0.04), k(H10, toon={**STAR, 'sq': [1.12, 1.0, 0.45], 'face': {'lid': 0.3, 'brow': 0.35, 'mouth': 'O', 'jaw': 0.3}}, toonDur=0.03, toonEase='out'),   # a hiccup: squashed flatter on the ceiling
            k(round(H10 + 0.18, 3), toon={**STAR, 'face': {'lid': 0.5, 'brow': 0.2}}, toonDur=0.12)]),
        act('pompier1', [-0.75, 0, -1.2], 20, 'stand', 'neutral', keys=[k(0.0, look=[0.0, CEIL, -2.2]), k(0.6, look=[0.8, 1.7, -1.05]), k(1.0, look=[0.0, CEIL, -2.2]), k(0.0, toon={'bend': {'neck': [-0.5, 0, 0, 1, None]}, 'face': {'jaw': 0.7, 'brow': 0.8}}, toonDur=0.0)]),
        act('pompier2', [0.8, 0, -1.05], -25, 'stand', 'neutral', keys=[k(0.0, look=[0.0, CEIL, -2.2]), k(0.0, toon={'bend': {'neck': [-0.5, 0, 0, 1, None]}, 'face': {'jaw': 0.5, 'brow': 0.9, 'eye': 0.3}}, toonDur=0.0), *react(H10, 0.8, look=[0.0, CEIL, -2.2])])],
        props=[P('ceil10', 'plainWall', pos=[0.0, round(CEIL + 0.02, 3), -3.6], rot=[round(PI / 2, 4), 0, 0], opts={'w': 7.0, 'h': 5.5, 'color': '#F2EBDD'}),
               P('dust10', 'dustPuff', pos=[0.2, round(CEIL - 0.3, 3), -2.0], scale=0.6, opts={'period': 1.2, 'color': '#F4F1EA'})],
        fx=[{'type': 'shake', 'at': H10, 'dur': 0.12, 'amount': 0.008}],
        cams=[FC(0.0, [0.25, 0.75, 0.9], [[-1.0, CEIL, -1.4], [1.0, CEIL, -3.4], [-0.75, 2.35, -1.2], [0.8, 2.35, -1.05], [0.0, CEIL, -2.2]], top=0.1, bottom=0.8)])
st.cue('thud', 'S10', 0.02, 0.4); st.cue('thud', 'S10', H10, 0.3)

# 11: yesterday the State declared him a natural disaster. His living room: an official in his sash pulls the cloth off a bronze plaque over the sofa:
#     CATASTROPHE NATURELLE; proud, he turns to us; beside him a hiccup throws the man a metre up: the official's double take
D11 = st.dur('S11'); UNV11 = round(st.at('S11', 'L10', 3) + 0.02, 3); H11 = round(st.at('S11', 'L10', 4) + 0.08, 3)
PLAQ = [round(SEAT[0] - 0.55, 3), 1.75, -3.46]; PREF = [-1.45, 0, -2.3]
st.shot('S11', 'livingRoom', setOpts=LR, actors=[
        act('mec', [round(SEAT[0] + 0.25, 3), 0, SEAT[2]], 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=TIRED, toonDur=0.0), k(0.5, look=[PREF[0], 2.0, PREF[2]]), k(1.0, look='camera'), *HICK(H11, [round(SEAT[0] + 0.25, 3), 0, SEAT[2]], 1.0)]),
        act('prefet', PREF, 40, 'stand', 'happy', keys=[k(0.0, look=PLAQ), k(round(UNV11 - 0.2, 3), toon={'reach': {'R': [round(PLAQ[0] - 0.2, 3), 2.0, round(PLAQ[2] + 0.12, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.12),
            k(UNV11, toon={'reach': {'R': [round(PLAQ[0] - 0.45, 3), 1.3, round(PLAQ[2] + 0.5, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.08, toonEase='out'), k(round(UNV11 + 0.15, 3), look='camera'), k(round(UNV11 + 0.3, 3), toon={'face': {'brow': 0.6}}, toonDur=0.15),
            *doubleTake(round(H11 + 0.08, 3), [round(SEAT[0] + 0.25, 3), 2.4, SEAT[2]])])],   # (cycle 12) the double take
        props=[P('plaque11', 'bronzePlaque', pos=PLAQ, opts={'text': 'CATASTROPHE/NATURELLE', 'w': 1.1, 'h': 0.42}),
               P('veil11', 'plainWall', pos=[PLAQ[0], round(PLAQ[1] - 0.26, 3), round(PLAQ[2] + 0.03, 3)], opts={'w': 1.25, 'h': 0.55, 'color': '#B5302A'}, keys=[k(UNV11, to=[round(PLAQ[0] - 0.45, 3), 0.3, round(PLAQ[2] + 0.5, 3)], dur=0.28, ease='in'), k(round(UNV11 + 0.3, 3), visible=False)])],   # the red cloth pulled off
        cams=[FC(0.0, [0.2, 1.6, 1.1], [[PLAQ[0] - 0.6, 2.05, PLAQ[2]], [PLAQ[0] + 0.6, 1.5, PLAQ[2]], [PREF[0], 2.35, PREF[2]], [round(SEAT[0] + 0.25, 3), 3.45, SEAT[2]], [round(SEAT[0] + 0.25, 3), 0.4, SEAT[2]], [PREF[0], 0.4, PREF[2]]], top=0.1, bottom=0.74)])
st.cue('sfx:paper', 'S11', UNV11, 0.3); st.cue('sfx:boing', 'S11', H11, 0.35); st.cue('thud', 'S11', round(H11 + 0.43, 3), 0.25)
st.card('S11', 'CATASTROPHE NATURELLE', at=round(UNV11 + 0.12, 3))

# 12: his insurance paid him three thousand euros. The insurer holds out a big cheque, 3 000 €; he takes it, deadpan; on « euros » a hiccup throws him up a
#     metre, the cheque with him; the insurer is left holding out his empty hand
D12 = st.dur('S12'); GIVE12 = round(st.at('S12', 'L11', 4) - 0.05, 3); H12 = round(st.at('S12', 'L11', 7) + 0.05, 3)
ASS = [1.25, 0, -2.15]; CHQ = [0.62, 1.38, -2.42]
HOLD12 = {'reach': {'R': [*CHQ, 1, 0.05]}, 'hands': {'R': 'pinch'}}
st.shot('S12', 'livingRoom', setOpts=LR, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look=[ASS[0], 1.8, ASS[2]]), k(0.0, toon=TIRED, toonDur=0.0), k(round(GIVE12 - 0.1, 3), toon={**HOLD12, **TIRED}, toonDur=0.12), k(round(GIVE12 + 0.3, 3), look='camera'),
            *HICK(H12, SEAT, 1.0, keep={'reach': {'R': [CHQ[0], round(CHQ[1] + 0.4, 3), CHQ[2], 0.6, 0.05]}, 'hands': {'R': 'pinch'}})]),
        act('assureur', ASS, -110, 'stand', 'happy', keys=[k(0.0, look=[SEAT[0], 1.6, SEAT[2]]), k(0.0, toon={'reach': {'L': [round(CHQ[0] + 0.25, 3), CHQ[1], round(CHQ[2] + 0.05, 3), 1, 0.05]}, 'hands': {'L': 'pinch'}}, toonDur=0.0),
            k(round(GIVE12 + 0.15, 3), toon={'reach': {'L': [round(CHQ[0] + 0.3, 3), CHQ[1], round(CHQ[2] + 0.05, 3), 1, 0.05]}, 'hands': {'L': 'flat'}}, toonDur=0.1), *react(H12, 0.8, look=[SEAT[0], 2.4, SEAT[2]])])],
        props=[P('chq12a', 'cheque', on={'actor': 'assureur', 'hand': 'L', 'offset': [0, 0.0, 0.05], 'face': 'camera'}, scale=2.6, opts={'amount': '3 000 €', 'text': 'ASSURANCE'}, keys=[k(GIVE12, visible=False)]),
               P('chq12b', 'cheque', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.0, 0.05], 'face': 'camera'}, scale=2.6, opts={'amount': '3 000 €', 'text': 'ASSURANCE'}, keys=[k(0.0, visible=False), k(GIVE12, visible=True)])],
        cams=[FC(0.0, [0.5, 1.6, 1.0], [[SEAT[0], 3.45, SEAT[2]], [SEAT[0], 0.4, SEAT[2]], [ASS[0], 2.35, ASS[2]], [ASS[0], 0.4, ASS[2]], [round(SEAT[0] - 0.55, 3), 1.8, SEAT[2]]], top=0.1, bottom=0.74)])
st.cue('sfx:paper', 'S12', GIVE12, 0.3); st.cue('sfx:cash', 'S12', round(GIVE12 + 0.1, 3), 0.25); st.cue('sfx:boing', 'S12', H12, 0.35)

# 13: since then he drinks nothing but soda. On his sofa beside a pyramid of soda cans, he sips one through a bendy straw, deadpan at us; on « soda » one more
#     hiccup lifts him a little with the can; a slow blink to finish
D13 = st.dur('S13'); H13 = round(st.at('S13', 'L12', 7) + 0.05, 3)
SIP = {'touch': {'R': ['face', 0.02, 0.18, 0.12, 1, 0.04]}, 'hands': {'R': 'grip'}}
st.shot('S13', 'livingRoom', setOpts=LR, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**SIP, **TIRED}, toonDur=0.0),
            *[x for t_ in (0.4, 1.0) for x in (k(t_, toon={**SIP, 'face': {**TIRED['face'], 'mouth': 'kiss', 'puff': 0.25}}, toonDur=0.08), k(round(t_ + 0.3, 3), toon={**SIP, **TIRED}, toonDur=0.08))],   # (pass 1b) sips
            *HICK(H13, SEAT, 0.35, keep=SIP),
            k(round(D13 - 0.7, 3), toon={**SIP, 'face': {'lid': 1}}, toonDur=0.14), k(round(D13 - 0.48, 3), toon={**SIP, **TIRED}, toonDur=0.16)]),   # a slow blink
        ],
        props=[P('can13', 'sodaCan', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.0, 0.03]}, scale=1.6, opts={'color': '#C8202A', 'text': 'SODA'}),
               P('stack13', 'sodaStack', pos=[-1.05, 0.0, -2.55], scale=1.2, opts={'rows': 4, 'cols': 6, 'pyramid': True}),
               P('stack13b', 'sodaStack', pos=[1.1, 0.0, -2.5], scale=1.0, opts={'rows': 3, 'cols': 4, 'pyramid': True}),
               HIC('hic13', [0.45, 2.45, -2.55], [H13], w=0.42)],
        cams=[FC(0.0, [0.2, 1.5, 0.6], [[SEAT[0], 2.9, SEAT[2]], [SEAT[0], 0.6, SEAT[2]], [-1.6, 1.4, -2.55], [1.55, 1.1, -2.5]], top=0.12, bottom=0.74, drift=(0.0, 0.0, -0.1))])
st.cue('sfx:pour', 'S13', 0.2, 0.2); st.cue('sfx:boing', 'S13', H13, 0.3)

# (cycle 13) the key poses, measured in the engine by render3 --probe (head in the frame, big enough, not covered, clear of the caption band and the card)
for g_ in [('S01', 1.65, 'mec', 'hic1'), ('S02', 0.68, 'mec', 'top1'), ('S02', 1.9, 'mec', 'top2'), ('S03', 1.8, 'savant', 'take'), ('S06', 1.25, 'mamie', 'jolt'),
           ('S07', 1.77, 'mec', 'cordon_jump'), ('S08', 1.68, 'mec', 'glass_up'), ('S09', 0.63, 'mec', 'boo'), ('S10', 0.82, 'mec', 'ceiling'),
           ('S11', 1.92, 'prefet', 'double_take'), ('S12', 1.88, 'mec', 'cheque_jump'), ('S13', 1.75, 'mec', 'last_hic')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
st.write("Le hoquet", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'savant': {'preset': 'savant', 'seed': 501, 'hair': 'receding', 'hairColor': '#EDEDED', 'build': {'width': 0.92, 'headWidth': 1.25}},
    'flic': {'preset': 'cop', 'seed': 502, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'voisine': {'preset': 'madame', 'seed': 503, 'suit': '#4F7F3A', 'build': {'width': 0.9, 'headWidth': 1.25}},
    'mamie': {'preset': 'mamie', 'seed': 504, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'gamin': {'preset': 'gamin', 'seed': 505},
    'voisin': {'preset': 'worker', 'seed': 506, 'hat': None, 'build': {'width': 0.95, 'headWidth': 1.2}},
    'pompier1': {'preset': 'pompier', 'seed': 507, 'build': {'width': 1.0, 'headWidth': 1.25}},
    'pompier2': {'preset': 'pompier', 'seed': 508, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'prefet': {'preset': 'politique', 'seed': 509, 'build': {'width': 0.95, 'headWidth': 1.25}},
    'assureur': {'preset': 'boss', 'seed': 510, 'build': {'width': 0.95, 'headWidth': 1.25}},
})
