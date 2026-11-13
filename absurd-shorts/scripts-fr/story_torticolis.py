#!/usr/bin/env python3
"""Le torticolis (story 53, cycle 15 of the cartoon staging): this man woke up with a stiff neck. His head stayed turned round to the back. Since then
he walks backwards to see where he goes. The prefecture issued him a driving licence back to front. He only drives in reverse. Yesterday an osteopath
put his head straight. It went round three times. It locked looking at the sky. He presents the weather.
Staging: in bed, the alarm, a stretch and a yawn; standing, his back to us, he turns to look behind him: CRAC, the head snaps on round, past the
back, and settles there: his face looks at us over his own back; at breakfast the spoon goes from the bowl up over his shoulder to the face on his
back, the arm bending backwards like a hose; in the street he walks backwards toward us, the face leading, the walk played in reverse; a lady
crossing him does a double take, her jaw dropping; at the prefecture he stands with his back to the counter and takes the licence behind his back;
the licence: pink, every word mirrored, for photo the back of a head; his little car flies down the boulevard in reverse, the face out of the rear
window, an arm over the seat; the driver he passes drops his jaw; the osteopath takes his head in both hands, winds up, CRAC: straight! a blink of
relief, then the head carries on round, three turns like a top, the tie flying out; it stops with a spring, the face up to the ceiling; on the TV
weather he stands by the map of France, the face to the sky, and points at it blind.
Natural look; cycle 15 tools: a look that follows an actor late and cheats toward the lens, the neck twist as a gag channel."""
from story_kit import *
import math

st = Story('torticolis', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L01', 6), ('S03', 'L02', 0), ('S04', 'L03', 0), ('S05', 'L03', 4), ('S06', 'L04', 0), ('S07', 'L04', 6),
         ('S08', 'L05', 0), ('S09', 11.43, 0), ('S10', 'L06', 0), ('S11', 'L06', 5), ('S12', 'L07', 0), ('S13', 'L08', 0), ('S14', 'L09', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(22, 70), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)
def NECK(tw, bx=0.0, extra=None):
    """the head turned tw radians on its neck (PI: the face on his back), bent back by -bx; extra: more toon channels on top"""
    d = {'bend': {'neck': [r(bx), 0, r(tw), 1, None]}}
    for k_, v in (extra or {}).items():
        if k_ == 'bend': d['bend'].update(v)
        else: d[k_] = v
    return d
BACK = NECK(PI)                                                     # the head the wrong way round: the rule of the film until S11
CRAC = lambda pid, pos, at_, w=0.5: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': 'CRAC !', 'inner': 0.78, 'fit': 0.56})
SPOON = lambda pid: P(pid, 'spoon', on={'actor': 'mec', 'hand': 'R', 'offset': [0, -0.04, 0.03], 'rot': [3.1416, 0, 0]}, scale=2.7, opts={'color': '#4A5260', 'outline': 0.005})   # (pass 2b) turned out of the fist and dark (along the forearm, pale silver, it never showed)
#   # (pass 2) an oversized spoon (it never showed)
STREETT = {'eiffelStyle': 'v2'}                                     # (pass 2) the connected tower with its arch (the old one read as a giant A)
LOOKI = {'warm': 0.45}   # (pass 3) the interiors less amber: the whites stay white (the kitchen table and the osteopath's coat read cream-orange)

# 1: the hook. His bedroom, morning: sitting up in bed under the blanket, eyes shut; the alarm clock rings on the bedside table; his eyes open, a big
#    stretch and a yawn, he slaps the clock quiet
D1 = st.dur('S01')
BED = [-2.6, 0.62, -2.35]
LAP1 = [-2.78, 0.95, -2.12]   # (pass 3) his right hand back on the blanket while the left one slaps (both arms out read as the stretch frozen)
st.shot('S01', 'chambre', setOpts={'poster': False}, look=LOOKI, actors=[
        act('mec', BED, 0, 'sitFloor', 'sleepy', keys=[k(0.0, look=[-1.75, 0.8, -2.5]), k(0.0, toon={'face': {'lid': 1.0}}, toonDur=0.0),
            k(0.05, toon={'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.0, 'pop': 0.5, 'popLen': 0.2, 'brow': 1.0}}, toonDur=0.033, toonEase='out'),   # (pass 2) the ring: the eyes out on stalks...
            k(0.24, toon={'face': {'lid': 0.5, 'brow': 0.2}}, toonDur=0.08),   # ...and back to sleepy
            k(0.42, toon={'sq': [1.08, 0.9, 1.08], 'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': {'lid': 0.6}}, toonDur=0.1, toonEase='in'),   # a crouch...
            k(0.55, toon={'reach': {'L': [-2.25, 2.3, -2.3, 1, 0.05], 'R': [-2.95, 2.3, -2.3, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'sq': [0.88, 1.25, 0.88], 'scl': {'head': [1.0, 1.12, 1.0]},
                          'face': {'expr': 'yawn', 'exprW': 1.0, 'jaw': 1.0, 'mouthH': 0.9, 'mouthW': 0.35}}, toonDur=0.14, toonEase='outBack'),
            # ...the stretch, a quarter taller; (pass 3) the yawn half his face (it was a quarter of it)
            k(0.86, toon={'reach': {'R': [*LAP1, 1, 0.05]}, 'hands': {'R': 'rest'}, 'sq': [1.02, 0.98, 1.02], 'face': {'lid': 0.5}}, toonDur=0.12),
            k(1.0, toon={'reach': {'L': [-1.75, 0.92, -2.5, 1, 0.08], 'R': [*LAP1, 1, 0.05]}, 'hands': {'L': 'open', 'R': 'rest'}, 'face': {'lid': 0.45}}, toonDur=0.1, toonEase='in'), k(0.95, look=[-1.75, 0.75, -2.5]),
            k(1.1, toon={'reach': {'L': [-1.75, 0.7, -2.5, 1, 0.08], 'R': [*LAP1, 1, 0.05]}, 'hands': {'L': 'open', 'R': 'rest'}, 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 0.45, 'brow': -0.2}}, toonDur=0.04, toonEase='out')])],
            # (pass 3) the palm lands on the clock on its squash frame and follows it down (it stopped a hand above it, and 'flat' is no hand pose: 'open' is)
        props=[P('table1', 'table', pos=[-1.75, 0, -2.5], opts={'w': 0.45, 'd': 0.45, 'h': 0.55, 'color': '#C99A62', 'legs': '#8A6A44'}),
               P('clock1', 'alarmClock', pos=[-1.75, 0.55, -2.5], ry=-60, scale=1.0, opts={'style': 'round', 'time': '07:00', 'ringAt': 0.0, 'stopAt': 1.1, 'squashAt': 1.1})],   # (pass 2) a round twin-bell clock, flattened by the slap
        cams=[FC(0.0, [-0.9, 1.45, 0.2], [[BED[0], 2.62, BED[2]], [BED[0], 0.6, r(BED[2] + 0.9)], [-1.75, 0.5, -2.5], [-2.95, 2.3, -2.3]], top=0.1, bottom=0.74, drift=(0.0, 0.0, -0.12))])
        # (pass 3) the stretch's hands and crown inside the frame (the hair touched the top row)
st.cue('sfx:ring', 'S01', 0.0, 0.35); st.cue('sfx:bonk', 'S01', 1.1, 0.3)

# 2: the stiff neck. Standing by the bed, his back to us: he turns to look behind him; on « torticolis » CRAC: the head snaps on round past his back,
#    overshoots and settles: his face looks at us over his own back, deadpan; a slow blink
D2 = st.dur('S02'); CR2 = 0.38
ME2 = [-1.2, 0, -1.4]
st.shot('S02', 'chambre', setOpts={'poster': False}, look=LOOKI, actors=[
        act('mec', ME2, 180, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=NECK(0.0), toonDur=0.0),
            k(0.03, toon=NECK(-1.25, extra={'face': {'gx': -0.8}}), toonDur=0.2, toonEase='inOut'),                    # (pass 2) a slow look back over his shoulder, the eyes leading...
            k(0.25, toon=NECK(-1.36, extra={'face': {'gx': -0.9}, 'sq': [1.0, 1.01, 1.0]}), toonDur=0.07),               # ...a hitch...
            k(round(CR2 - 0.04, 3), toon=NECK(-1.2, extra={'sq': [1.02, 0.98, 1.02]}), toonDur=0.03),                  # ...back a notch (the anticipation)...
            k(CR2, toon=NECK(round(-PI - 0.38, 3), extra={'sq': [1.1, 0.9, 1.1], 'scl': {'head': [1.25, 0.92, 1.0]}, 'face': {'eye': 0.35, 'brow': 0.6}}), toonDur=0.033, toonEase='out'),
            # ...CRAC: round in one frame, smeared, 20 degrees past his back, the body squashed one frame...
            *[k(round(CR2 + 0.033 * (j_ + 1), 3), toon=NECK(round(-PI - 0.38 + 0.38 * (j_ + 1) / 5, 3), extra={'sq': [1.0, (1.02 if j_ % 2 else 0.98), 1.0], 'face': {'lid': 0.3}}), toonDur=0.033) for j_ in range(5)],
            # ...a shudder as it comes back...
            k(round(CR2 + 0.22, 3), toon=NECK(-PI, extra={'face': {'lid': 0.45}}), toonDur=0.06),                         # ...and settles there, the face to us
            k(round(D2 - 0.32, 3), toon=NECK(-PI, extra={'face': {'lid': 1.0}}), toonDur=0.06), k(round(D2 - 0.18, 3), toon=NECK(-PI, extra={'face': {'lid': 0.45}}), toonDur=0.08)])],   # a slow blink
        props=[CRAC('crac2', [-0.75, 2.2, -1.2], CR2, w=0.46)],
        cams=[FC(0.0, [-0.75, 1.75, 0.65], [[ME2[0], 2.45, ME2[2]], [ME2[0], 0.95, ME2[2]], [r(ME2[0] - 0.45), 1.9, ME2[2]], [r(ME2[0] + 0.55), 2.3, ME2[2]]], top=0.12, bottom=0.72, drift=(0.0, 0.0, -0.08))])
st.cue('clack', 'S02', CR2, 0.45); st.cue('sfx:twang', 'S02', round(CR2 + 0.02, 3), 0.25)

# 3: his head stayed turned to the back. Breakfast in the kitchen, from behind him: his body faces the table, his face faces us; the spoon dips in the
#    bowl and goes up over his shoulder to the face on his back, the arm bending backwards; he chews, deadpan; again
D3 = st.dur('S03')
ME3 = [0.0, 0, -1.25]; BOWL = [0.08, 0.76, -1.75]
def SPOONAT(bowl, out_, hollow):
    """(pass 3) a spoon held on his head (in the head joint's frame, metres): its bowl at `bowl`, its handle going off along `out_`, the hollow of the
    bowl turned to `hollow`; returns (foot, rot, fist): where the end of the handle goes, its Euler XYZ (radians) and where his fist holds it. In the
    hand the spoon pointed wherever the wrist did: both spoonfuls arrived bowl up over his head, never in the mouth or the ear"""
    u = unit3(out_); Y = [-x for x in u]; L_ = 0.378                     # the bowl is 0.14 up the spoon, at scale 2.7
    d_ = sum(a * b for a, b in zip(hollow, Y)); Z = unit3([hollow[i] - d_ * Y[i] for i in range(3)]); X = cross3(Y, Z)
    foot = [round(bowl[i] + L_ * u[i], 3) for i in range(3)]; fist = [round(foot[i] - 0.081 * u[i], 3) for i in range(3)]
    rx, ry_, rz = axes_euler(X, Y, Z)
    return foot, [rx, round(math.radians(ry_), 4), rz], fist
SPM_FOOT, SPM_ROT, SPM_FIST = SPOONAT([0.0, 0.11, 0.1], [0.55, -0.25, 0.8], [0, 1, 0])     # (pass 3) the bowl between his lips (the face is 0.085 m in front of the joint, the mouth 0.115 up), the handle out to his hand
SPE_FOOT, SPE_ROT, SPE_FIST = SPOONAT([0.135, 0.26, 0.0], [0.6, -0.45, 0.65], [-1, 0, 0])   # (pass 3) the bowl in his ear (the head box is 0.24 wide)
MOUTH3 = {'touch': {'R': ['head', *SPM_FIST, 1, 0.05]}, 'hands': {'R': 'grip'}, 'hose': 0.25}   # (pass 2) in the frame of the turned head; a rubber-hose elbow
EAR3 = {'touch': {'R': ['head', *SPE_FIST, 1, 0.05]}, 'hands': {'R': 'grip'}, 'hose': 0.25}      # (pass 2) the second spoonful: into his ear
DIP3 = {'reach': {'R': [BOWL[0], 0.86, BOWL[2], 1, 0.05]}, 'hands': {'R': 'pinch'}}
SPOONC = {'color': '#D5DAE0', 'outline': 0.006}   # (final) bright steel (dark, against his face, it read at 2.1 to 1)
st.shot('S03', 'kitchenDay', look=LOOKI, actors=[
        act('mec', ME3, 180, 'sit', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**BACK, **DIP3}, toonDur=0.0),
            # the first spoonful: up over his shoulder (0.3), in (0.54), the lips close on it (0.66), out (0.76), chewing on the way down
            k(0.3, toon={**BACK, **MOUTH3, 'face': {'mouth': 'O', 'jaw': 0.35}}, toonDur=0.24, toonEase='inOut'),
            k(0.62, toon={**BACK, **MOUTH3, 'face': {'mouth': 'pout', 'puff': 0.45}}, toonDur=0.05),
            k(0.76, toon={**BACK, **DIP3, 'face': {'puff': 0.4}}, toonDur=0.2, toonEase='inOut'),
            *[k(round(0.8 + 0.1 * j_, 3), toon={**BACK, **DIP3, 'face': {'jaw': 0.2 if j_ % 2 == 0 else 0.0, 'puff': 0.3}}, toonDur=0.05) for j_ in range(4)],
            # the second spoonful goes into his ear: a splash of milk, the head squashed, a blink (it hung upright above the ear, still)
            k(1.2, toon={**BACK, **EAR3, 'face': {'mouth': 'O', 'jaw': 0.3}}, toonDur=0.24, toonEase='inOut'),
            k(1.44, toon={**BACK, **EAR3, 'scl': {'head': [1.14, 0.86, 1.14]}, 'face': {'lidR': 0.8, 'brow': 0.5}}, toonDur=0.04, toonEase='out'),
            k(1.52, toon={**BACK, **EAR3, 'face': {'brow': 0.3}}, toonDur=0.08),
            k(1.6, toon={**BACK, **EAR3, 'face': {'lid': 1.0}}, toonDur=0.04), k(1.68, toon={**BACK, **EAR3, 'face': {'lid': 0.45, 'brow': 0.3}}, toonDur=0.06),
            k(1.9, toon={**BACK, **DIP3}, toonDur=0.2, toonEase='inOut')])],
        props=[P('table3', 'table', pos=[0.0, 0, -1.85], opts={'w': 1.1, 'd': 0.75, 'h': 0.74, 'color': '#F2EEE2', 'legs': '#9FD8C8'}),
               P('bench3', 'bench', pos=[0.0, 0, -1.25], ry=90), P('bowl3', 'cerealBowl', pos=BOWL, scale=2.1),
               P('spoon3', 'spoon', on={'actor': 'mec', 'hand': 'R', 'offset': [0, -0.04, 0.03], 'rot': [3.1416, 0, 0]}, scale=2.7, opts=SPOONC,
                 keys=[k(0.52, visible=False), k(0.76, visible=True), k(1.42, visible=False), k(1.9, visible=True)]),   # (pass 2b) the spoon in his fist...
               P('spoonM3', 'spoon', on={'actor': 'mec', 'joint': 'head', 'offset': SPM_FOOT, 'rot': SPM_ROT}, scale=2.7, opts=SPOONC, keys=[k(0.0, visible=False), k(0.52, visible=True), k(0.76, visible=False)]),
               P('spoonE3', 'spoon', on={'actor': 'mec', 'joint': 'head', 'offset': SPE_FOOT, 'rot': SPE_ROT}, scale=2.7, opts=SPOONC, keys=[k(0.0, visible=False), k(1.42, visible=True), k(1.9, visible=False)]),
               # (pass 3) ...swapped for one set in his mouth, then in his ear, while the hand holds it there
               P('milk3', 'waterDrops', pos=[0.12, 1.5, -0.98], opts={'at': 0.58, 'n': 6, 'dir': [0, -1, 0.2], 'speed': 0.5, 'spread': 0.35, 'color': '#FFFFFF', 'r': 0.022, 'life': 0.6, 'tear': False, 'ink': '#7D8A96'}),   # (pass 2) milk dripping; (final) round drops (the teardrops read as a flame)
               P('splash3', 'waterDrops', on={'actor': 'mec', 'joint': 'head', 'offset': [0.15, 0.27, 0.0]}, opts={'at': 1.45, 'n': 10, 'dir': [1, 0.7, 0.3], 'speed': 1.3, 'spread': 0.7, 'color': '#FFFFFF', 'r': 0.026, 'life': 0.5, 'tear': False, 'ink': '#7D8A96'})],
               # (pass 3) the milk splashes out of his ear
        cams=[FC(0.0, [1.5, 1.65, 0.25], [[ME3[0], 2.3, ME3[2]], [ME3[0], 0.6, ME3[2]], [-0.5, 1.6, ME3[2]], [0.6, 1.6, ME3[2]], [BOWL[0], BOWL[1], BOWL[2]]], top=0.12, bottom=0.74, drift=(0.0, 0.0, -0.15))])
        # (pass 2) three-quarters: the bowl beside him, the arm going up over his shoulder in profile (from behind, his body hid the bowl and the spoon)
st.cue('sfx:clink', 'S03', 0.25, 0.2); st.cue('sfx:clink', 'S03', 1.15, 0.2); st.cue('sfx:splash', 'S03', 1.45, 0.25)

# 4: since then he walks backwards. The street from low down: he walks backwards toward us, his back first, his face leading over it, the walk played
#    in reverse; a pigeon steps aside
D4 = st.dur('S04'); X4 = 7.0
st.shot('S04', 'parisStreet', setOpts=STREETT, actors=[
        act('mec', [X4, 0, -3.4], 180, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=BACK, toonDur=0.0),
            k(0.0, to=[X4, 0, -0.9], dur=round(D4 + 0.03, 3), clip='walk', then='walk', ease='linear', face='keep', speed=-1.0)]),   # the cycle played backwards: real backward steps
        act('passant', [r(X4 + 0.85), 0, -3.75], 0, 'stand', 'neutral', keys=[k(0.0, look=[r(X4 + 0.85), 1.9, 3.0]),
            k(0.0, to=[r(X4 + 0.85), 0, -1.25], dur=round(D4 + 0.03, 3), clip='walk', then='walk', ease='linear', face='move'),
            k(0.5, look={'actor': 'mec', 'cheat': 0.35}), k(0.95, look=[r(X4 + 0.85), 1.9, 3.0])])],   # (final) a man walking forwards beside him, the same way: his tie, his toes; a sidelong glance
        props=[P('bol4a', 'potelet', pos=[r(X4 - 0.8), 0, -1.3]), P('bol4b', 'potelet', pos=[r(X4 - 0.8), 0, -2.9]), P('bol4c', 'potelet', pos=[r(X4 - 0.8), 0, -4.5])],
        cams=[FC(0.0, [r(X4 + 0.3), 0.75, 1.5], [[X4, 2.3, -0.9], [X4, 0.0, -0.9], [r(X4 + 0.85), 2.3, -1.25], [r(X4 + 0.85), 0.0, -1.25], [r(X4 - 0.45), 1.5, -0.9]], top=0.08, bottom=0.8, drift=(0.0, 0.0, 0.3), lenses=range(30, 57))])
        # (final) on his path, at hip height and close: the back of his suit and his face over it come at us beside a man who walks the right way
        # (a small man walking in a frame two-thirds empty read as a man walking)
        # (pass 3) three-quarters in front and low: the back of his suit comes at us with the face over it, the heels leading (in profile the box head
        # showed its ear side, the face edge-on: the walk backwards did not read)
        # (pass 2) in profile, tracking him: the toes point the other way from where he goes (head on, backward read as forward)

# 5: to see in front of him. From the side: he walks backwards, the face leading; a lady coming the other way says hello, he nods back; she passes, then
#    looks back: a double take, her jaw drops
D5 = st.dur('S05'); X5 = 7.4; SN5 = 0.88   # (pass 3) her snap back to him
st.shot('S05', 'parisStreet', setOpts=STREETT, actors=[
        act('mec', [r(X5 + 1.0), 0, 0.0], 90, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=BACK, toonDur=0.0),
            k(0.0, to=[r(X5 - 0.8), 0, 0.0], dur=round(D5 + 0.03, 3), clip='walk', then='walk', ease='linear', face='keep', speed=-1.0),
            k(0.4, toon=NECK(PI, bx=0.22), toonDur=0.08), k(0.55, toon=BACK, toonDur=0.1)]),                                            # a nod to her
        act('dame', [r(X5 - 1.5), 0, 0.75], 90, 'stand', 'happy', keys=[k(0.0, look={'actor': 'mec', 'dy': -0.1}),
            k(0.0, to=[r(X5 + 0.75), 0, 0.8], dur=0.75, clip='walk', then='stand', ease='out', face='move'),   # (pass 3) she stops a step past him...
            k(0.25, toon={'face': {'mouth': 'smile'}}, toonDur=0.1),
            k(0.5, look='camera'), k(0.66, look={'actor': 'mec', 'cheat': 0.15}),   # ...a blank look ahead, then back at him over her shoulder...
            k(0.8, face='mec', turn=0.14),   # ...she turns round to him...
            k(round(SN5 - 0.06, 3), toon={'sq': [1.07, 0.9, 1.07], 'face': {'lid': 0.7, 'brow': -0.3}}, toonDur=0.04, toonEase='in'),   # ...a two-frame squash...
            k(SN5, look={'actor': 'mec', 'cheat': 0.5}),
            k(SN5, toon={'sq': [0.88, 1.16, 0.88], 'face': {'eye': 0.55, 'brow': 1.0, 'jaw': 1.0, 'jawLen': 0.5, 'mouth': 'O'}}, toonDur=0.04, toonEase='outBack'),   # (final) a stretch up, the jaw down to her collar (the eyes on stalks were the driver's take too)
            k(round(SN5 + 0.12, 3), toon={'sq': [0.97, 1.05, 0.97], 'face': {'eye': 0.5, 'brow': 1.0, 'jaw': 1.0, 'jawLen': 0.5, 'mouth': 'O'}}, toonDur=0.1),
            k(round(SN5 + 0.32, 3), toon={'sq': [1.0, 1.03, 1.0], 'face': {'eye': 0.45, 'brow': 0.9, 'jaw': 1.0, 'jawLen': 0.48, 'mouth': 'O', 'lid': 0.1}}, toonDur=0.2)])],
            # ...then the eyes out on stalks and the jaw to her chest, held to the cut, her face to us
            # (pass 3) the take turned to him and to us, held 0.6 s (her popped eyes pointed away from him, 0.3 s, she never broke her stride)
        props=[],
        cams=[FC(0.0, [r(X5 - 3.3), 1.35, 2.3], [[r(X5 - 0.8), 2.45, 0.0], [r(X5 - 0.8), 0.2, 0.0], [r(X5 + 0.75), 2.35, 0.8], [r(X5 + 0.75), 0.2, 0.8], [r(X5 + 0.3), 2.4, 0.0]], top=0.12, bottom=0.74, drift=(0.15, 0.0, -0.1), lenses=range(30, 57))])
        # (pass 3) a closer two-shot from in front of him: his back and his face come at us, she ends behind him on the right, turned to us
        # (pass 2) past him, a real double take (a glance, a blank look at us, the snap back), eyes out, the jaw dropped
st.cue('sfx:gasp', 'S05', round(SN5 + 0.02, 3), 0.25)

# 6: the prefecture issued him a licence. The counter, PRÉFECTURE: he stands with his back to it, his face to the clerk; she holds out the licence over
#    the counter; he takes it with his hand behind his back
D6 = st.dur('S06'); GIVE6 = 0.85
ME6 = [-0.5, 0, -1.65]; CLERK = [-0.5, 0, -2.95]
HANDOFF = [-0.98, 1.25, -2.1]   # (pass 3) out at his right side, clear of both bodies (between his back and her jacket the hand and the licence were hidden)
CARD6 = [-0.8, 1.105, -2.38]    # (pass 3) the licence lies on the pale counter top first: she stamps it
POSTE = {'title': 'PRÉFECTURE', 'guichets': False}   # (pass 3) no window signs (the left edge cut « CHET 1 »)
st.shot('S06', 'poste', setOpts=POSTE, look=LOOKI, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=BACK, toonDur=0.0),
            k(0.55, toon={**BACK, 'reach': {'R': [HANDOFF[0], HANDOFF[1], r(HANDOFF[2] + 0.04), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'hose': 0.12}, toonDur=0.3, toonEase='inOut'),   # the arm bends back to it
            k(round(GIVE6 + 0.05, 3), toon={**BACK, 'reach': {'R': [-0.82, 1.62, -1.98, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'hose': 0.12}, toonDur=0.3, toonEase='inOut'),   # (pass 3) and brings it up behind him
            k(1.2, toon={**BACK, 'reach': {'R': [-0.82, 1.62, -1.98, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'hose': 0.12, 'face': {'lid': 0.5, 'gx': 0.4}}, toonDur=0.15)]),
        act('guichet', CLERK, 0, 'stand', 'neutral', keys=[k(0.0, look=[CARD6[0], 1.1, CARD6[2]]),
            k(0.0, toon={'reach': {'R': [CARD6[0], 1.14, r(CARD6[2] - 0.06), 1, 0.05], 'L': [-0.35, 1.5, -2.55, 1, 0.05]}, 'hands': {'R': 'open', 'L': 'grip'}}, toonDur=0.0),
            k(0.08, toon={'reach': {'R': [CARD6[0], 1.14, r(CARD6[2] - 0.06), 1, 0.05], 'L': [r(CARD6[0] + 0.08), 1.2, CARD6[2], 1, 0.05]}, 'hands': {'R': 'open', 'L': 'grip'}, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.12, toonEase='in'),   # (pass 3) BANG: the stamp...
            k(0.28, toon={'reach': {'R': [CARD6[0], 1.14, r(CARD6[2] - 0.06), 1, 0.05], 'L': [-0.35, 1.45, -2.55, 1, 0.05]}, 'hands': {'R': 'open', 'L': 'grip'}}, toonDur=0.12),
            k(0.36, toon={'reach': {'R': [HANDOFF[0], HANDOFF[1], r(HANDOFF[2] - 0.04), 1, 0.05], 'L': [-0.35, 1.3, -2.6, 1, 0.05]}, 'hands': {'R': 'pinch', 'L': 'grip'}}, toonDur=0.22, toonEase='inOut'),   # ...then held out
            k(round(GIVE6 + 0.05, 3), toon={'reach': {'L': [-0.35, 1.3, -2.6, 1, 0.05]}, 'hands': {'L': 'grip'}}, toonDur=0.25), k(0.36, look={'actor': 'mec', 'cheat': 0.3}),
            k(round(GIVE6 + 0.12, 3), toon={'reach': {'L': [-0.35, 1.3, -2.6, 1, 0.05]}, 'hands': {'L': 'grip'}, 'face': {'brow': 0.7, 'mouth': 'smirk'}}, toonDur=0.1)])],
        props=[P('permis6', 'reversePermit', pos=CARD6, rot=[round(-PI / 2, 4), 0, 0], opts={'s': 1.3},
                 keys=[k(0.36, to=[HANDOFF[0], r(HANDOFF[1] + 0.02), r(HANDOFF[2] - 0.0)], dur=0.22, ease='inOut'), k(0.36, rotTo=[-0.35, 0, 0], dur=0.22),
                       k(round(GIVE6 + 0.05, 3), to=[-0.82, 1.66, -1.98], dur=0.3, ease='inOut')]),
               P('stamp6', 'rubberStamp', on={'actor': 'guichet', 'hand': 'L'}, scale=1.6)],
               # (pass 3) the pink licence on the pale counter, stamped, then held out at his side: the handoff in the clear
        cams=[FC(0.0, [-1.9, 2.5, 1.2], [[ME6[0], 2.45, ME6[2]], [ME6[0], 0.45, ME6[2]], [CLERK[0], 2.35, CLERK[2]], [HANDOFF[0], HANDOFF[1], HANDOFF[2]], [-1.75, 3.0, -3.45], [1.75, 3.42, -3.45]], top=0.06, bottom=0.74, lenses=range(30, 62))])
        # (pass 3) higher: the counter top shows pale under the licence
        # (pass 2b) from in front on his right: he stands at 60 % of the width, the clerk's head beside his   # (pass 2) the whole title (PRÉFECTUR was cut)
st.cue('sfx:bonk', 'S06', 0.2, 0.25); st.cue('sfx:paper', 'S06', GIVE6, 0.3)

# 7: back to front. Over his shoulder: he holds the licence up to the face on his back: pink, every word mirrored, the photo the back of a head; he
#    looks at it, deadpan, a slow blink
D7 = st.dur('S07'); AE7 = st.at('S07', 'L04', 9)   # « à l'envers »
ME7 = [0.35, 0, -0.75]
CARD7 = [0.9, 1.84, -0.45]      # (pass 3) the licence beside the face on his back, flat to the lens, as wide as his head and shoulders
LIC7 = {'reach': {'R': [1.12, 1.68, -0.43, 1, 0.04]}, 'hands': {'R': 'pinch'}, 'hose': 0.15}   # (pass 3) pinched by its bottom corner, the arm bent back over his shoulder
st.shot('S07', 'poste', setOpts=POSTE, look=LOOKI, actors=[
        act('mec', ME7, 180, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**BACK, **LIC7, 'face': {'gx': 0.7, 'gy': 0.1}}, toonDur=0.0),
            k(0.3, toon={**BACK, **LIC7, 'sq': [1.0, 1.02, 1.0], 'bend': {'spine': [0.03, 0, 0, 1, None]}, 'face': {'gx': 0.7, 'gy': 0.1}}, toonDur=0.25, toonEase='inOut'),   # (final) a breath
            k(round(AE7 - 0.1, 3), toon={**BACK, **LIC7, 'face': {'gx': 0.8, 'gy': 0.15, 'brow': 0.35}}, toonDur=0.12),   # reading it
            k(round(AE7 + 0.3, 3), toon={**BACK, **LIC7, 'face': {'gx': 0.8, 'lid': 1.0}}, toonDur=0.08),
            k(round(AE7 + 0.48, 3), toon={**BACK, **LIC7, 'face': {'gx': 0.0, 'lid': 0.45}}, toonDur=0.14),   # a slow blink, both eyes, then at us
            k(round(AE7 + 0.66, 3), toon={**BACK, **LIC7, 'sq': [1.0, 1.02, 1.0], 'bend': {'spine': [0.03, 0, 0, 1, None]}, 'face': {'gx': 0.0, 'lid': 0.45}}, toonDur=0.2, toonEase='inOut'),   # (final) a breath
            k(round(D7 - 0.1, 3), toon={**BACK, **LIC7, 'sq': [1.0, 1.01, 1.0], 'face': {'gx': 0.0, 'lid': 0.4}}, toonDur=0.1)])],
        props=[P('permis7', 'reversePermit', pos=CARD7, face='camera', opts={'s': 1.7, 'bright': True})],
        # (pass 3) its own prop in the middle of the frame: in the hand it sat at the right edge, half behind the fist, and the push in lost it
        cams=[FC(0.0, [0.95, 1.85, 1.7], [[ME7[0], 2.38, ME7[2]], [ME7[0], 1.2, ME7[2]], [-0.05, 1.9, ME7[2]], [1.2, 1.84, -0.45]], top=0.14, bottom=0.66, lenses=range(30, 62)),
              glide([FC(0.3, [0.8, 1.86, 0.95], [[ME7[0], 2.2, -0.6], [ME7[0], 1.6, -0.6], [0.1, 1.88, -0.6], [1.2, 1.84, -0.45]], top=0.18, bottom=0.66, lenses=range(30, 62))], 0.32)])
        # (pass 3) he has turned to the counter: the room behind the camera, the push in lands on the licence and his face before « à l'envers »
        # (pass 2b) kept in front of the counter glass   # (pass 2) a push in on the mirrored licence and his face

# 8: he only drives in reverse. The boulevard: his little red car flies down it backwards; the traffic comes the other way
D8 = st.dur('S08'); XL8 = 1.6; ZA8, ZB8 = -14.0, -2.5
# (pass 2) along the boulevard, not across it: his open car comes at us rear first, his face over the back of it, while the car in the next lane comes
# at us front first
BOB8 = [0.0, 0.035, 0.0, 0.03, 0.0, 0.04]   # (pass 3) the car bounces on the cobbles, him with it (it slid like a slab)
SEAT89 = {'touch': {'L': ['torso', 0.4, 0.22, -0.28, 1, 0.05]}}   # (pass 3) his arm over the seat back, in his own frame (a point of the street stayed behind the car)
def BOBKEYS(x, y0, z0, z1, dz=0.0):
    n_ = len(BOB8); return [k(round(D8 * i / n_, 3), to=[x, round(y0 + BOB8[(i + 1) % n_], 3), round(z0 + (z1 - z0) * (i + 1) / n_ + dz, 3)], dur=round(D8 / n_ + 0.01, 3), ease='inOut') for i in range(n_)]
CAR8 = lambda pid, x, z0, z1, ry, col: P(pid, 'car', pos=[x, 0, z0], ry=ry, opts={'color': col, 'convertible': True, 'interior': '#E8D2B0'}, keys=[k(0.0, to=[x, 0, z1], dur=round(D8 + 0.05, 3), ease='linear')])
st.shot('S08', 'parisStreet', setOpts=STREETT, actors=[act('mec', [r(XL8 - 0.4), 0.12, r(ZA8 - 0.15)], 180, 'drive', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**BACK, 'touch': {'L': ['torso', 0.4, 0.22, -0.28, 1, 0.05]}, 'hands': {'L': 'open'}}, toonDur=0.0),
            *[dict(x_, glide=True, face='keep') for x_ in BOBKEYS(r(XL8 - 0.4), 0.12, ZA8, ZB8, -0.15)],
            k(0.45, toon={**BACK, 'touch': {'L': ['torso', 0.4, 0.22, -0.28, 1, 0.05]}, 'hands': {'L': 'open'}, 'face': {'lid': 0.4}, 'wind': [0.0, 1.0, 6.0]}, toonDur=0.2)])],   # (pass 3) the tie and the hair streaming, a lazy blink
        props=[P('car8', 'car', pos=[XL8, 0, ZA8], ry=90, opts={'color': '#C9473A', 'convertible': True, 'interior': '#E8D2B0'}, keys=BOBKEYS(XL8, 0.0, ZA8, ZB8)),
               CAR8('car8b', r(XL8 - 3.4), -8.0, -1.5, -90, '#3E7CC9'), CAR8('car8c', r(XL8 - 3.4), -21.0, -14.5, -90, '#E8C547')],
        cams=[cam(0.0, [r(XL8 + 1.3), 2.25, r(ZA8 + 6.4)], [r(XL8 + 1.15), 1.95, r(ZB8 + 3.3)], [r(XL8 - 0.35), 1.0, r(ZA8 - 0.3)], [r(XL8 - 0.35), 1.0, r(ZB8 - 0.3)], lens=42)])
        # (pass 3) tracking just ahead of the car, closer: the boot first, his face over the seat a sixth of the frame (high and far, it was 7 %)
        # (pass 2) high ahead of him on the boulevard
st.cue('engine', 'S08', 0.0, 0.3, round(D8, 3)); st.cue('sfx:beep', 'S08', 0.05, 0.2)

# 9: in reverse. Close, from behind the car: it comes at us backwards, his face in the rear window, an arm over the seat, cool; the driver he passes
#    drops his jaw
D9 = st.dur('S09'); XL9 = 1.6; ZA9 = -6.0; ZB9 = r(ZA9 + 9.0 * D9); XO9 = r(XL9 - 2.4); ZO9a = -3.4; ZO9b = r(ZO9a + 3.0 * D9)
SN9 = 0.38   # (pass 3) the pop as the red car draws level (0.43 s)
# (pass 2) fast (9 m/s) so the street streams by, in an open car so his face is in the light
st.shot('S09', 'parisStreet', setOpts=STREETT, actors=[
        act('mec', [r(XL9 - 0.4), 0.12, r(ZA9 - 0.15)], 180, 'drive', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**BACK, 'touch': {'L': ['torso', 0.4, 0.22, -0.28, 1, 0.05]}, 'hands': {'L': 'open'}}, toonDur=0.0),
            k(0.0, to=[r(XL9 - 0.4), 0.12, r(ZB9 - 0.15)], dur=round(D9 + 0.05, 3), glide=True, ease='linear', face='keep')]),
        act('voisin', [r(XO9 + 0.4), 0.12, r(ZO9a + 0.15)], 0, 'drive', 'neutral', keys=[k(0.0, look=[r(XO9 + 0.4), 1.4, 3.0]),
            k(0.0, to=[r(XO9 + 0.4), 0.12, r(ZO9b + 0.15)], dur=round(D9 + 0.05, 3), glide=True, ease='linear', face='keep'),
            k(0.12, look={'actor': 'mec', 'cheat': 0.3}), k(0.22, look=[r(XO9 + 0.4), 1.4, 3.0]),   # (pass 3) a glance at the car behind, back to the road...
            k(round(SN9 - 0.08, 3), toon={'sq': [1.08, 0.9, 1.08], 'face': {'lid': 0.75, 'brow': -0.4}}, toonDur=0.05, toonEase='in'),   # ...a squash...
            k(round(SN9 - 0.02, 3), look={'actor': 'mec', 'cheat': 0.55}),
            k(SN9, toon={'sq': [0.94, 1.08, 0.94], 'hat': [0.3, 0.35, 1.6], 'face': {'jaw': 1.0, 'jawLen': 0.7, 'brow': 1.0, 'eye': 0.4, 'mouth': 'O'}}, toonDur=0.033, toonEase='out'),   # (final) ...the hat jumps off his head, the jaw down onto the wheel...
            *[k(round(SN9 + 0.1 + 0.08 * i, 3), toon={'hat': [round(0.3 - 0.07 * i, 3), round(0.35 - 0.1 * i, 3), round(1.6 + 0.8 * i, 3)], 'face': {'jaw': 1.0, 'jawLen': 0.7, 'brow': 1.0, 'eye': 0.4, 'mouth': 'O'}}, toonDur=0.07) for i in range(4)]])],   # ...held to the cut (the eyes on stalks were the lady's take too)
        props=[P('car9', 'car', pos=[XL9, 0, ZA9], ry=90, opts={'color': '#C9473A', 'convertible': True, 'interior': '#E8D2B0'}, keys=[k(0.0, to=[XL9, 0, ZB9], dur=round(D9 + 0.05, 3), ease='linear')]),
               P('car9b', 'car', pos=[XO9, 0, ZO9a], ry=-90, opts={'color': '#3E7CC9', 'convertible': True}, keys=[k(0.0, to=[XO9, 0, ZO9b], dur=round(D9 + 0.05, 3), ease='linear')])],
        cams=[cam(0.0, [r(XO9 - 0.6), 1.65, r(ZO9a + 2.4)], [r(XO9 - 0.6), 1.65, r(ZO9b + 2.4)], [r(XO9 + 1.1), 1.4, r(ZO9a - 0.4)], [r(XO9 + 1.1), 1.4, r(ZO9b - 0.4)], lens=50)])
        # (pass 3) a quarter of a second longer (the cut taken from S08), an anticipation before the pop, the take held 0.4 s
        # (pass 2b) riding beside the overtaken driver: his take on the left, the red car streaking past behind him rear first, the face over its seat
st.cue('sfx:honkLong', 'S09', 0.12, 0.25); st.cue('sfx:beep', 'S09', 0.0, 0.15)

# 10: yesterday an osteopath put his head straight. His room, a spine on the wall: he sits on a stool, his back to us... the osteopath stands at his
#     face, takes his head in both hands, his tongue out in concentration, and winds it up the other way
# (pass 3) a treatment room, not an office: pale walls, a white treatment table, a spine chart (desks, monitors and a slatted bench read as an office)
D10 = st.dur('S10')
HOSP = {'monitor': False, 'cross': False}   # (final) an osteopath's room: no heart monitor over the spine chart, no red cross
ME10 = [0.0, 0, -1.6]; OST10 = [0.62, 0, -1.55]   # (final) beside his head, both faces to the lens (behind it, the two box heads merged into one shape)   # (pass 3) the osteopath at his knee, facing the back of his head: from in front of the face on his back both faces show
COUCH = lambda pid: P(pid, 'table', pos=[0.0, 0, -1.6], opts={'w': 1.85, 'd': 0.62, 'h': 0.47, 'color': '#F2F4F1', 'legs': '#8F9AA0'})   # (pass 3) he sits on its edge
CHART = lambda pid: P(pid, 'spinePoster', pos=[-1.2, 1.75, -3.57], opts={'w': 0.7, 'h': 1.05})
GRIP10 = {'reach': {'L': [0.0, 1.88, -1.53, 1, 0.04], 'R': [0.17, 1.6, -1.53, 1, 0.04]}, 'hands': {'L': 'grip', 'R': 'grip'}}   # (final) a hand on the crown, a hand on the near side of the head   # (pass 3) the fingertips on the sides of the head ('flat' is no hand pose: the hands hung relaxed beside it)
STRAIN = {'face': {'tongue': 0.85, 'tongueLen': 0.12, 'tongueYaw': 0.3, 'brow': -0.7, 'lid': 0.6, 'low': 0.3}}
st.shot('S10', 'hospital', setOpts=HOSP, look=LOOKI, actors=[
        act('mec', ME10, 0, 'sit', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=BACK, toonDur=0.0),
            *[k(t_, toon=NECK(round(PI + 0.25 * (n_ + 1), 3), extra={'sq': [1.02, 0.98, 1.02], 'face': {'lid': 0.3, 'brow': 0.3}}), toonDur=0.05, toonEase='out') for n_, t_ in enumerate((0.55, 0.8, 1.05))],
            # (pass 2) three notches the wrong way, the neck coiling tighter
            *[k(round(1.12 + 0.07 * q_, 3), toon=NECK(round(PI + 0.78 + (0.03 if q_ % 2 else -0.03), 3), extra={'sq': [1.0, (1.015 if q_ % 2 else 0.99), 1.0], 'face': {'lid': 0.3, 'brow': 0.3, 'gx': (0.3 if q_ % 2 else -0.3)}}), toonDur=0.033) for q_ in range(6)]]),   # held, shaking, the eyes darting
        act('osteo', OST10, -90, 'stand', 'determined', keys=[k(0.0, look={'point': [0.0, 1.75, -1.53], 'cheat': 0.5}), k(0.0, toon={'face': {'brow': -0.3}}, toonDur=0.0),
            k(0.2, toon={**GRIP10, 'face': {'tongue': 0.6, 'tongueLen': 0.1, 'brow': -0.4}}, toonDur=0.25, toonEase='out'),   # the hands close on the head
            *[k(t_, toon={**GRIP10, **STRAIN, 'bend': {'spine': [0.08, round(-0.1 * (n_ + 1), 3), 0, 1, None]}, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.05, toonEase='out') for n_, t_ in enumerate((0.55, 0.8, 1.05))],
            *[k(round(1.12 + 0.07 * q_, 3), toon={**GRIP10, **STRAIN, 'bend': {'spine': [0.08, -0.3, 0, 1, None]}, 'sq': [1.05, (0.95 if q_ % 2 else 0.97), 1.05]}, toonDur=0.033) for q_ in range(6)]])],
            # (pass 2) a notch at a time with him, then the strain held before the release, the tongue further out; (pass 3) the eyes squeezed
        props=[COUCH('couch10'), CHART('chart10'),
               P('wall10', 'plainWall', pos=[0.0, 1.6, 0.9], ry=180, opts={'w': 6.0, 'h': 3.2, 'color': '#EEF1EC'}),
               P('poster10', 'spinePoster', pos=[-0.95, 1.7, 0.88], ry=180, opts={'w': 0.7, 'h': 1.05})],   # (pass 3) the room's near wall behind them, the spine chart on it
        cams=[FC(0.0, [-0.75, 1.7, -3.2], [[0.0, 1.98, ME10[2]], [0.0, 1.2, ME10[2]], [OST10[0], 2.48, OST10[2]], [-0.3, 1.5, ME10[2]], [r(OST10[0] + 0.3), 1.6, OST10[2]]], top=0.08, bottom=0.74,
                 drift=(0.08, 0.0, 0.06), lenses=range(30, 56), inside=(-6.8, 6.8, 0.0, 6.5, -3.45, 13.0))])   # (pass 3) from the chest up: against the wall, the knees asked for a 64 degree lens
        # (pass 3) in front of the face on his back: his face to us, the osteopath's straining face over his head, the hands clamped on it (from behind
        # the osteopath, the back of his head filled 40 % of the frame and his face never showed)

# 11: straight. Close: CRAC! the head snaps round to the front: his face to us at last, a blink, the hint of a smile; the osteopath beams
D11 = st.dur('S11'); CR11 = 0.18; OST11 = [0.75, 0, -1.25]   # (pass 3) the osteopath at his side, where S10 left him
GRIP11 = {'reach': {'L': [0.0, 1.88, -1.53, 1, 0.04], 'R': [0.17, 1.6, -1.53, 1, 0.04]}, 'hands': {'L': 'grip', 'R': 'grip'}}   # (final) as S10 left them   # (pass 3) toward the back of the head: at mid-depth a hand covered his cheek
TADA = lambda dy=0.0: {'touch': {'L': ['torso', 0.48, round(0.52 + dy, 3), 0.2, 1, 0.05], 'R': ['torso', -0.48, round(0.52 - dy, 3), 0.2, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}}
GRIN = {'mouth': 'teeth', 'mouthW': 0.4, 'cheeks': 0.6, 'brow': 0.6}
st.shot('S11', 'hospital', setOpts=HOSP, look=LOOKI, actors=[
        act('mec', ME10, 0, 'sit', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=NECK(PI + 0.45), toonDur=0.0),
            k(round(CR11 - 0.05, 3), toon=NECK(PI + 0.66, extra={'sq': [1.02, 0.98, 1.02]}), toonDur=0.04),   # (pass 2) one more notch: the anticipation...
            k(CR11, toon=NECK(-0.35, extra={'sq': [1.1, 0.9, 1.1], 'scl': {'head': [1.25, 0.92, 1.0]}, 'face': {'eye': 0.35, 'brow': 0.8}}), toonDur=0.033, toonEase='out'),   # ...CRAC: round in one smeared frame, 20 degrees past the front...
            k(round(CR11 + 0.1, 3), toon=NECK(0.12, extra={'sq': [1.0, 1.02, 1.0], 'face': {'lid': 0.4}}), toonDur=0.08), k(round(CR11 + 0.2, 3), toon=NECK(0.0, extra={'face': {'lid': 0.45}}), toonDur=0.08),   # ...and back
            k(round(CR11 + 0.5, 3), toon=NECK(0.0, extra={'face': {'lid': 1.0}}), toonDur=0.06), k(round(CR11 + 0.62, 3), toon=NECK(0.0, extra={'face': {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}}), toonDur=0.1),   # a blink, relief
            k(round(CR11 + 0.78, 3), toon=NECK(0.04, extra={'sq': [1.0, 1.02, 1.0], 'face': {'lid': 0.3, 'mouth': 'smile', 'brow': 0.35}}), toonDur=0.12),   # (pass 3) a breath of relief
            k(round(D11 - 0.12, 3), toon=NECK(0.6, extra={'face': {'lid': 0.3, 'mouth': 'smile'}}), toonDur=0.12, toonEase='in')]),   # ...and it is still going
        act('osteo', OST11, -115, 'stand', 'happy', keys=[k(0.0, look=[0.0, 1.75, ME10[2]]), k(0.0, toon={**GRIP11, **STRAIN}, toonDur=0.0),
            k(CR11, toon={**TADA(), 'face': GRIN, 'sq': [0.95, 1.08, 0.95]}, toonDur=0.08, toonEase='outBack'),   # hands off: ta-da...
            k(round(CR11 + 0.04, 3), face=[0.3, 0.55], turn=0.16), k(round(CR11 + 0.1, 3), look='camera'),   # (pass 3) ...turned to us, an open grin...
            *[k(round(CR11 + 0.22 + 0.2 * i, 3), toon={**TADA(0.05 if i % 2 else -0.05), 'face': GRIN, 'sq': [1.0, (1.02 if i % 2 else 0.99), 1.0]}, toonDur=0.18, toonEase='inOut') for i in range(4)]])],
            # (pass 3) ...the arms still drifting, a bounce in his knees (the ta-da froze both of them 0.7 s, the beam had no mouth)
        props=[COUCH('couch11'), CHART('chart11'), CRAC('crac11', [-0.28, 2.16, -1.3], CR11, w=0.36)],
        cams=[FC(0.0, [0.2, 1.85, -0.45], [[0.0, 2.2, ME10[2]], [0.0, 1.35, ME10[2]], [-0.34, 1.8, ME10[2]], [0.34, 1.8, ME10[2]]], top=0.18, bottom=0.66),
              glide([FC(round(CR11 + 0.42, 3), [0.3, 1.75, 0.55], [[0.0, 2.55, ME10[2]], [0.0, 1.15, ME10[2]], [-0.75, 2.1, ME10[2]], [1.3, 2.4, OST11[2]], [OST11[0], 2.3, OST11[2]]], top=0.14, bottom=0.72)], 0.3)])
        # (final) the crack and his straight face close up, then out for the ta-da (in the wide shot his face was 60 px)
st.cue('clack', 'S11', CR11, 0.45); st.cue('sfx:twang', 'S11', round(CR11 + 0.02, 3), 0.25)

# 12: it went round three times. The head spins on, three turns like a top, the tie flying out, his face going by deadpan; the osteopath steps back,
#     his eyes going round with it
D12 = st.dur('S12'); SP12 = round(D12 - 0.38, 3); OST12 = [1.1, 0, -1.05]   # (final) the three turns faster, room for a hang at the end
st.shot('S12', 'hospital', setOpts=HOSP, look=LOOKI, actors=[
        act('mec', ME10, 0, 'sit', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=NECK(0.6, extra={'face': {'mouth': 'smile'}}), toonDur=0.0),
            *[k(round(0.02 + SP12 * n_ / 6, 3), toon=NECK(round(0.6 + PI * (n_ + 1), 3), bx=(0.18 if n_ % 2 else -0.18), extra={'wind': [round(7 * math.sin(0.6 + PI * (n_ + 1)), 2), 1.5, round(7 * math.cos(0.6 + PI * (n_ + 1)), 2)], 'scl': {'head': [1.3, 0.95, 1.0]}, 'sq': [0.97, 1.03, 0.97], 'bend': {'spine': [0.0, (0.06 if n_ % 2 else -0.06), 0, 1, None]}, 'face': {'lid': 0.45}}), toonDur=round(SP12 / 6, 3), toonEase='linear') for n_ in range(6)],
            # (final) the tie flung round with the head (its own wind turns with it), the shoulders wobbling, the head smeared wider
            # (pass 2) three turns like a top: the head wobbles as it spins, smeared
            k(round(SP12 + 0.03, 3), toon=NECK(round(0.6 + 6 * PI + 0.42, 3), extra={'wind': [3.0, 1.0, 4.0], 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 0.45}}), toonDur=0.05, toonEase='out'),   # (final) past the third turn, hung there five frames...
            k(round(D12 - 0.13, 3), toon=NECK(round(0.6 + 6 * PI - 0.08, 3), extra={'face': {'expr': 'dizzy', 'exprW': 1.0}, 'sq': [1.02, 0.98, 1.02]}), toonDur=0.05, toonEase='in'),   # ...then it springs back...
            k(round(D12 - 0.06, 3), toon=NECK(round(0.6 + 6 * PI, 3), extra={'face': {'expr': 'dizzy', 'exprW': 1.0}}), toonDur=0.05)]),   # ...dizzy eyes
        act('osteo', OST11, -115, 'stand', 'surprised', keys=[k(0.0, look=[0.0, 2.0, ME10[2]]), k(0.1, to=OST12, dur=0.3, glide=True, ease='out', face='keep'), k(0.12, face=-30, turn=0.2),   # (pass 3) opened to us as he steps back (the probe: his back, 131 degrees)
            k(0.1, toon={'lay': [-0.12, 0], 'face': {'jaw': 0.6, 'brow': 1.0, 'gx': 0.8}}, toonDur=0.1),
            *[k(round(0.2 + 0.11 * i, 3), toon={'lay': [-0.12, (0.06 if i % 2 else -0.06)], 'face': {'jaw': 0.6, 'brow': 1.0, 'gx': [0.9, 0.0, -0.9, 0.0][i % 4], 'gy': [0.0, 0.7, 0.0, -0.7][i % 4]}}, toonDur=0.08) for i in range(9)],   # his eyes going round (final: in circles)...
            *[k(round(0.25 + 0.11 * i, 3), look={'point': [(0.45 if i % 2 else -0.45), 1.9, ME10[2]], 'cheat': 0.55}) for i in range(8)],   # ...then his head with them (final: cheated to the lens, the probe saw a profile)
            k(round(D12 - 0.22, 3), toon={'lay': [-0.05, 0.1], 'face': {'expr': 'dizzy', 'exprW': 0.8, 'jaw': 0.4}}, toonDur=0.1)])],   # (pass 2) and he staggers, dizzy
        props=[COUCH('couch12'), CHART('chart12'), P('swirl12', 'windSwirl', pos=[0.0, 1.62, -1.53], keys=[k(SP12, visible=False)])],   # (final) wind streaks round the spinning head
        cams=[FC(0.0, [0.9, 1.7, 0.35], [[0.0, 2.6, ME10[2]], [0.0, 0.9, ME10[2]], [-0.65, 2.2, ME10[2]], [0.7, 2.2, ME10[2]], [OST12[0], 2.3, OST12[2]], [r(OST12[0] + 0.35), 1.6, OST12[2]]], top=0.12, bottom=0.72, drift=(0.0, 0.0, -0.25))])
st.cue('whoosh', 'S12', 0.05, 0.35, 0.35, 400, 1800); st.cue('whoosh', 'S12', 0.45, 0.35, 0.35, 500, 2200); st.cue('whoosh', 'S12', 0.85, 0.3, 0.35, 400, 1800)

# 13: it locked looking at the sky. From the side: the head stops with a spring, bent right back, the face to the ceiling, bobbling; deadpan; the
#     osteopath scratches his head, looking up too
D13 = st.dur('S13'); OST13 = [0.82, 0, -1.25]   # (pass 3) a step nearer him: whole in the frame (at 1.0 the right edge cut him)
SCR = lambda i: {'touch': {'R': ['head', (-0.05 if i % 2 else -0.1), (0.5 if i % 2 else 0.46), 0.0, 1, 0.02], 'L': ['torso', 0.24, -0.08, 0.06, 1, 0.03]}, 'hands': {'R': 'claw', 'L': 'fist'}, 'face': {'brow': 0.9, 'browTilt': 12, 'jaw': 0.25, 'mouth': 'wavy'}}
st.shot('S13', 'hospital', setOpts=HOSP, look=LOOKI, actors=[
        act('mec', ME10, 0, 'sit', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=NECK(0.0, bx=-0.3), toonDur=0.0),
            k(0.12, toon=NECK(0.0, bx=-1.62, extra={'sq': [1.04, 0.96, 1.04]}), toonDur=0.06, toonEase='out'),                    # clunk: the face to the ceiling...
            *[k(round(0.2 + 0.08 * i, 3), toon=NECK(0.0, bx=round(-1.4 - 0.12 * (0.55 ** i) * (1 if i % 2 else -1), 3)), toonDur=0.07) for i in range(5)],   # ...bobbling on a spring
            k(0.62, toon=NECK(0.0, bx=-1.4, extra={'sq': [1.02, 1.03, 1.02]}), toonDur=0.2, toonEase='inOut'), k(0.86, toon=NECK(0.0, bx=-1.4), toonDur=0.15),   # (pass 2) a breath
            k(1.05, toon=NECK(0.0, bx=-1.4, extra={'face': {'lid': 1.0}}), toonDur=0.06), k(1.18, toon=NECK(0.0, bx=-1.4, extra={'face': {'lid': 0.45}}), toonDur=0.1),   # a blink at the ceiling
            k(1.45, toon=NECK(0.0, bx=-1.4, extra={'sq': [1.02, 1.03, 1.02], 'face': {'lid': 0.45, 'gx': 0.3}}), toonDur=0.2, toonEase='inOut')]),   # (pass 3) another breath, the eyes sliding
        act('osteo', OST13, -20, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.75, ME10[2]]), k(0.3, look={'point': [0.0, 3.2, -1.9], 'cheat': 0.5}),   # (pass 3) he looks up where the face looks...
            # (pass 3) opened to the lens (the probe: 114 degrees, his back)
            k(0.35, toon=SCR(0), toonDur=0.2, toonEase='out'),
            *[k(round(0.6 + 0.09 * i, 3), toon=SCR(i + 1), toonDur=0.08) for i in range(12)]])],
            # (pass 3) ...and scratches his head, in the frame (half out at the edge, his hand never reached his head)
        props=[COUCH('couch13'), CHART('chart13')],
        cams=[FC(0.0, [0.8, 3.15, -0.55], [[0.0, 2.15, ME10[2]], [0.0, 1.0, ME10[2]], [-0.45, 1.5, ME10[2]], [0.45, 1.5, ME10[2]], [OST13[0], 2.45, OST13[2]], [OST13[0], 0.0, OST13[2]], [r(OST13[0] + 0.45), 1.6, OST13[2]], [r(OST13[0] - 0.2), 2.5, OST13[2]]],
                 top=0.12, bottom=0.74, drift=(-0.05, -0.05, 0.0), lenses=range(30, 52))])
        # (pass 3) the osteopath whole beside him
        # (pass 2b) closer and higher, from the knees up: the face turned up to the ceiling read as a blank box at 70 px
st.cue('sfx:spring', 'S13', 0.12, 0.35)

# 14: he presents the weather. The TV studio from a crane above: by the map of France, his face up to the sky looks straight at us, deadpan; he points
#     at the map blind; the camera's red light; a slow blink
D14 = st.dur('S14')
ME14 = [0.8, 0, -2.0]; MAP14 = [-0.55, 1.75, -2.88]
st.shot('S14', 'pressRoom', setOpts={'backdrop': 'MÉTÉO', 'podium': False, 'flags': False, 'chairs': False, 'bg': '#26507E', 'wall': '#26507E', 'fg': '#3D6A9A'}, look=LOOKI, actors=[   # (pass 2) the backdrop words navy on blue
        act('mec', ME14, 15, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=NECK(0.0, bx=-1.4), toonDur=0.0),
            k(0.08, toon=NECK(0.0, bx=-1.4, extra={'face': {'lid': 1.0}, 'sq': [1.0, 1.02, 1.0]}), toonDur=0.06), k(0.18, toon=NECK(0.0, bx=-1.4, extra={'face': {'lid': 0.45}}), toonDur=0.08),   # (pass 3) a blink and a breath in the side view (it held still 0.5 s)
            k(0.3, toon={**NECK(0.0, bx=-1.4), 'reach': {'R': [r(MAP14[0] + 0.25), 1.75, r(MAP14[2] + 0.1), 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.1}, toonDur=0.15, toonEase='outBack'),   # points at it blind
            k(1.0, toon={**NECK(0.0, bx=-1.4), 'reach': {'R': [r(MAP14[0] - 1.15), 1.45, r(MAP14[2] + 0.1), 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.1, 'lay': [0.0, 0.035]}, toonDur=0.25, toonEase='inOut'),   # (pass 2) the blind finger lands off the map, on the wall
            k(1.5, toon={**NECK(0.0, bx=-1.4, extra={'face': {'lid': 1.0}}), 'reach': {'R': [r(MAP14[0] - 1.15), 1.45, r(MAP14[2] + 0.1), 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.1, 'lay': [0.0, 0.035]}, toonDur=0.07),
            k(1.65, toon={**NECK(0.0, bx=-1.4, extra={'face': {'lid': 0.45}}), 'reach': {'R': [r(MAP14[0] - 1.15), 1.45, r(MAP14[2] + 0.1), 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.1, 'lay': [0.0, 0.035]}, toonDur=0.12),
            k(1.9, toon={**NECK(0.0, bx=-1.4, extra={'face': {'lid': 0.45}, 'sq': [1.0, 1.02, 1.0]}), 'reach': {'R': [r(MAP14[0] - 1.1), 1.5, r(MAP14[2] + 0.1), 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.1}, toonDur=0.25, toonEase='inOut')])],   # (pass 3) and a breath at the end
        props=[P('map14', 'weatherMap', pos=MAP14, opts={'w': 1.7, 'h': 1.05}), P('tvcam14', 'tvCamera', pos=[ME14[0], 3.05, r(ME14[2] + 0.1)], rot=[round(PI / 2, 4), 0, 0], scale=1.4, opts={'legs': False}, keys=[k(0.6, visible=False)]),   # (pass 2b) no tripod, bigger   # (pass 2b) gone in the crane view: we are the camera
               P('rig14', 'plainWall', pos=[ME14[0], 3.85, r(ME14[2] + 0.1)], opts={'w': 0.08, 'h': 1.3, 'color': '#2A2C31'}, keys=[k(0.6, visible=False)])],   # (pass 2) the studio camera hung from the ceiling over him, pointing down
        cams=[FC(0.0, [3.0, 1.75, -0.7], [[ME14[0], 3.6, ME14[2]], [ME14[0], 0.2, ME14[2]], [MAP14[0], 1.75, MAP14[2]], [r(ME14[0] + 0.4), 1.5, ME14[2]]], top=0.08, bottom=0.74, lenses=range(30, 62), drift=(-0.12, 0.0, -0.08)),
              # (pass 2b) tighter: the man, the camera over him and the map; (pass 3) a slow push in
              glide([FC(0.6, [0.95, 3.6, -0.55], [[ME14[0], 2.4, ME14[2]], [ME14[0], 0.2, ME14[2]], [r(MAP14[0] - 1.3), 2.25, MAP14[2]], [r(MAP14[0] + 0.9), 1.25, MAP14[2]]], top=0.12, bottom=0.74, drift=(0.0, -0.1, -0.12))], 0.4)])
        # (pass 2) first the cause, from the side: the camera hangs from the ceiling over his bent-back head; then the crane up into its view
st.cue('sfx:static', 'S14', 0.0, 0.12)

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S01', 0.75, 'mec', 'yawn'), ('S02', 0.7, 'mec', 'face_on_back'), ('S03', 0.6, 'mec', 'spoon'), ('S04', 1.0, 'mec', 'walk_back'), ('S05', 1.1, 'dame', 'double_take'),
           ('S06', 0.9, 'mec', 'counter'), ('S07', 0.5, 'mec', 'licence'), ('S09', 0.6, 'mec', 'rear_window'), ('S10', 1.0, 'mec', 'wound'), ('S11', 0.6, 'mec', 'straight'),
           ('S12', 0.7, 'osteo', 'spin'), ('S13', 0.9, 'mec', 'up'), ('S14', 1.2, 'mec', 'weather'),
           ('S09', 0.5, 'voisin', 'take'), ('S10', 1.2, 'osteo', 'strain'), ('S13', 1.0, 'osteo', 'scratch'), ('S05', 1.2, 'dame', 'take_held')]:   # (pass 3) the takes and the osteopath's faces
    st.gag(g_[0], g_[1], g_[2], g_[3])
for t_ in [('S06', 0.3, 'permis6', 'counter_title'), ('S07', 0.5, 'permis7', 'licence'), ('S14', 1.0, 'map14', 'meteo')]:
    st.text(t_[0], t_[1], t_[2], t_[3])

st.write("Le torticolis", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'dame': {'preset': 'madame', 'seed': 531, 'suit': '#4F7F3A', 'hair': 'bun', 'hairColor': '#8A4A22', 'build': {'width': 0.9, 'headWidth': 1.25}},
    'guichet': {'preset': 'madame', 'seed': 532, 'suit': '#7A5C9E', 'hairColor': '#2A2A2E', 'skin': '#E2B48C', 'build': {'width': 0.9, 'headWidth': 1.25}},
    'voisin': {'preset': 'worker', 'seed': 533, 'hat': 'fedora', 'hair': 'receding', 'hairColor': '#9A9A96', 'facial': 'mustache', 'build': {'width': 0.95, 'headWidth': 1.2}},
    'passant': {'preset': 'boss', 'seed': 535, 'suit': '#A0522D', 'build': {'width': 0.95, 'headWidth': 1.2}},
    'osteo': {'preset': 'savant', 'seed': 534, 'hair': 'receding', 'hairColor': '#6B4A2A', 'build': {'width': 0.95, 'headWidth': 1.25}},
})
