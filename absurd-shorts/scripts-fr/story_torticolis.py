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
         ('S08', 'L05', 0), ('S09', 'L05', 5), ('S10', 'L06', 0), ('S11', 'L06', 5), ('S12', 'L07', 0), ('S13', 'L08', 0), ('S14', 'L09', 0)])

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

# 1: the hook. His bedroom, morning: sitting up in bed under the blanket, eyes shut; the alarm clock rings on the bedside table; his eyes open, a big
#    stretch, arms up, and a yawn; he slaps the clock quiet
D1 = st.dur('S01')
BED = [-2.6, 0.62, -2.35]
st.shot('S01', 'chambre', setOpts={'poster': False}, actors=[
        act('mec', BED, 0, 'sitFloor', 'sleepy', keys=[k(0.0, look=[-1.75, 0.8, -2.5]), k(0.0, toon={'face': {'lid': 1.0}}, toonDur=0.0),
            k(0.05, toon={'sq': [0.95, 1.06, 0.95], 'face': {'lid': 0.0, 'pop': 0.5, 'popLen': 0.2, 'brow': 1.0}}, toonDur=0.033, toonEase='out'),   # (pass 2) the ring: the eyes out on stalks...
            k(0.24, toon={'face': {'lid': 0.5, 'brow': 0.2}}, toonDur=0.08),   # ...and back to sleepy
            k(0.42, toon={'sq': [1.08, 0.9, 1.08], 'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': {'lid': 0.6}}, toonDur=0.1, toonEase='in'),   # a crouch...
            k(0.55, toon={'reach': {'L': [-2.25, 2.4, -2.3, 1, 0.05], 'R': [-2.95, 2.4, -2.3, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'sq': [0.88, 1.25, 0.88], 'scl': {'head': [1.0, 1.12, 1.0]},
                          'face': {'expr': 'yawn', 'exprW': 1.0, 'jaw': 1.0}}, toonDur=0.14, toonEase='outBack'),   # ...the stretch, a quarter taller, a yawn half his face
            k(0.86, toon={'sq': [1.02, 0.98, 1.02], 'face': {'lid': 0.5}}, toonDur=0.12),
            k(1.0, toon={'reach': {'L': [-1.75, 0.98, -2.5, 1, 0.05]}, 'hands': {'L': 'flat'}, 'face': {'lid': 0.45}}, toonDur=0.1, toonEase='in'), k(0.95, look=[-1.75, 0.75, -2.5])])],   # slaps the clock
        props=[P('table1', 'table', pos=[-1.75, 0, -2.5], opts={'w': 0.45, 'd': 0.45, 'h': 0.55, 'color': '#C99A62', 'legs': '#8A6A44'}),
               P('clock1', 'alarmClock', pos=[-1.75, 0.55, -2.5], ry=-60, scale=1.0, opts={'style': 'round', 'time': '07:00', 'ringAt': 0.0, 'stopAt': 1.1, 'squashAt': 1.1})],   # (pass 2) a round twin-bell clock, flattened by the slap
        cams=[FC(0.0, [-0.9, 1.45, 0.2], [[BED[0], 2.35, BED[2]], [BED[0], 0.6, r(BED[2] + 0.9)], [-1.75, 0.5, -2.5], [-2.95, 2.2, -2.3]], top=0.12, bottom=0.74, drift=(0.0, 0.0, -0.12))])
st.cue('sfx:ring', 'S01', 0.0, 0.35); st.cue('sfx:bonk', 'S01', 1.1, 0.3)

# 2: the stiff neck. Standing by the bed, his back to us: he turns to look behind him; on « torticolis » CRAC: the head snaps on round past his back,
#    overshoots and settles: his face looks at us over his own back, deadpan; a slow blink
D2 = st.dur('S02'); CR2 = 0.38
ME2 = [-1.2, 0, -1.4]
st.shot('S02', 'chambre', setOpts={'poster': False}, actors=[
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
MOUTH3 = {'touch': {'R': ['head', 0.08, 0.1, 0.27, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'hose': 0.25}   # (pass 2) at his mouth, in the frame of the turned head (the touch on the face left the hand at his chin); a rubber-hose elbow
EAR3 = {'touch': {'R': ['head', 0.3, 0.27, 0.05, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'hose': 0.25}      # (pass 2) the second spoonful: into his ear
DIP3 = {'reach': {'R': [BOWL[0], 0.86, BOWL[2], 1, 0.05]}, 'hands': {'R': 'pinch'}}
st.shot('S03', 'kitchenDay', actors=[
        act('mec', ME3, 180, 'sit', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**BACK, **DIP3}, toonDur=0.0),
            *[x for t_, TGT in ((0.3, MOUTH3), (1.2, EAR3)) for x in (
                k(t_, toon={**BACK, **TGT, 'face': {'mouth': 'O', 'jaw': 0.35}}, toonDur=0.24, toonEase='inOut'),                 # up over his shoulder to the face on his back
                k(round(t_ + 0.32, 3), toon={**BACK, **TGT, 'face': {'mouth': 'flat', 'puff': 0.4}}, toonDur=0.06),               # in
                *[k(round(t_ + 0.42 + 0.1 * j_, 3), toon={**BACK, **TGT, 'face': {'jaw': 0.18 if j_ % 2 == 0 else 0.0, 'puff': 0.3}}, toonDur=0.05) for j_ in range(3)],   # chewing
                k(round(t_ + 0.74, 3), toon={**BACK, **DIP3}, toonDur=0.16, toonEase='inOut'))],                                   # back down to the bowl
            k(1.56, toon={**BACK, **EAR3, 'face': {'lid': 1.0}}, toonDur=0.04), k(1.64, toon={**BACK, **EAR3, 'face': {'lid': 0.45, 'brow': 0.3}}, toonDur=0.06)])],   # (pass 2) the ear: a blink
        props=[P('table3', 'table', pos=[0.0, 0, -1.85], opts={'w': 1.1, 'd': 0.75, 'h': 0.74, 'color': '#F2EEE2', 'legs': '#9FD8C8'}),
               P('bench3', 'bench', pos=[0.0, 0, -1.25], ry=90), P('bowl3', 'cerealBowl', pos=BOWL, scale=1.5), SPOON('spoon3'),
               P('milk3', 'waterDrops', pos=[0.12, 1.5, -0.98], opts={'at': 0.58, 'n': 6, 'dir': [0, -1, 0.2], 'speed': 0.5, 'spread': 0.35, 'color': '#FFFFFF', 'r': 0.022, 'life': 0.6, 'tear': True, 'ink': '#9AA5B0'})],   # (pass 2) milk dripping
        cams=[FC(0.0, [1.5, 1.65, 0.25], [[ME3[0], 2.3, ME3[2]], [ME3[0], 0.6, ME3[2]], [-0.5, 1.6, ME3[2]], [0.6, 1.6, ME3[2]], [BOWL[0], BOWL[1], BOWL[2]]], top=0.12, bottom=0.74, drift=(0.0, 0.0, -0.15))])
        # (pass 2) three-quarters: the bowl beside him, the arm going up over his shoulder in profile (from behind, his body hid the bowl and the spoon)
st.cue('sfx:clink', 'S03', 0.25, 0.2); st.cue('sfx:clink', 'S03', 1.15, 0.2)

# 4: since then he walks backwards. The street from low down: he walks backwards toward us, his back first, his face leading over it, the walk played
#    in reverse; a pigeon steps aside
D4 = st.dur('S04'); X4 = 7.0
st.shot('S04', 'parisStreet', setOpts=STREETT, actors=[
        act('mec', [X4, 0, -3.2], 180, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=BACK, toonDur=0.0),
            k(0.0, to=[X4, 0, -0.6], dur=round(D4 + 0.03, 3), clip='walk', then='walk', ease='linear', face='keep', speed=-1.0)])],   # the cycle played backwards: real backward steps
        props=[],
        cams=[FC(0.0, [r(X4 - 3.0), 1.1, -1.9], [[X4, 2.4, -0.6], [X4, 0.0, -0.6], [X4, 2.4, -3.2], [X4, 0.0, -3.2]], top=0.1, bottom=0.74, drift=(0.0, 0.0, 0.9))])
        # (pass 2) in profile, tracking him: the toes point the other way from where he goes (head on, backward read as forward)

# 5: to see in front of him. From the side: he walks backwards, the face leading; a lady coming the other way says hello, he nods back; she passes, then
#    looks back: a double take, her jaw drops
D5 = st.dur('S05'); X5 = 7.4
st.shot('S05', 'parisStreet', setOpts=STREETT, actors=[
        act('mec', [r(X5 + 1.1), 0, 0.0], 90, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=BACK, toonDur=0.0),
            k(0.0, to=[r(X5 - 0.9), 0, 0.0], dur=round(D5 + 0.03, 3), clip='walk', then='walk', ease='linear', face='keep', speed=-1.0),
            k(0.45, toon=NECK(PI, bx=0.22), toonDur=0.08), k(0.6, toon=BACK, toonDur=0.1)]),                                            # a nod to her
        act('dame', [r(X5 - 1.6), 0, 0.85], 90, 'stand', 'happy', keys=[k(0.0, look={'actor': 'mec', 'dy': -0.1}),
            k(0.0, to=[r(X5 + 2.2), 0, 0.95], dur=round(D5 + 0.03, 3), clip='walk', then='walk', ease='linear', face='move'),
            k(0.3, toon={'face': {'mouth': 'smile'}}, toonDur=0.1),
            *doubleTake(0.72, {'actor': 'mec', 'cheat': 0.55}, back='camera', pop=0.65, blank=0.2, hold=0.3),
            k(1.1, toon={'face': {'pop': 0.65, 'popLen': 0.25, 'brow': 1.0, 'jaw': 0.9}, 'sq': [0.95, 1.06, 0.95]}, toonDur=0.04, toonEase='out')])],
        # (pass 2) in front of him, nearer the lens: past him, a real double take (a glance, a blank look at us, the snap back), eyes out, the jaw
        # dropped, in her own space (behind him, half hidden, it was a single small look back)
        props=[],
        cams=[FC(0.0, [r(X5 - 1.6), 1.5, 4.2], [[r(X5 - 1.2), 2.4, -0.1], [r(X5 + 1.9), 2.3, 0.9], [X5, 0.0, 0.2], [r(X5 + 1.9), 0.0, 0.9]], top=0.14, bottom=0.74, drift=(0.25, 0.0, 0.0))])   # (first look) three-quarters on his face (side on it was a profile)
st.cue('sfx:gasp', 'S05', 0.95, 0.25)

# 6: the prefecture issued him a licence. The counter, PRÉFECTURE: he stands with his back to it, his face to the clerk; she holds out the licence over
#    the counter; he takes it with his hand behind his back
D6 = st.dur('S06'); GIVE6 = 0.85
ME6 = [-0.5, 0, -1.65]; CLERK = [-0.5, 0, -2.95]; HANDOFF = [-0.5, 1.22, -2.05]   # (pass 2b) left of the title's middle: from his right side he sits in the frame, not at its edge
st.shot('S06', 'poste', setOpts={'title': 'PRÉFECTURE'}, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=BACK, toonDur=0.0),
            k(round(GIVE6 - 0.25, 3), toon={**BACK, 'reach': {'R': [HANDOFF[0], HANDOFF[1], r(HANDOFF[2] + 0.05), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'hose': 0.1}, toonDur=0.2, toonEase='inOut'),   # the arm bends back to it
            k(round(GIVE6 + 0.2, 3), toon={**BACK, 'reach': {'R': [r(ME6[0] + 0.1), 1.45, r(ME6[2] - 0.35), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'hose': 0.1}, toonDur=0.2)]),
        act('guichet', CLERK, 0, 'stand', 'neutral', keys=[k(0.0, look={'actor': 'mec', 'cheat': 0.3}), k(0.15, toon={'reach': {'R': [HANDOFF[0], HANDOFF[1], r(HANDOFF[2] - 0.05), 1, 0.05]}, 'hands': {'R': 'pinch'}}, toonDur=0.25),
            k(round(GIVE6 + 0.05, 3), toon={}, toonDur=0.2), k(round(GIVE6 + 0.1, 3), toon={'face': {'brow': 0.7}}, toonDur=0.1)])],
        props=[P('permis6', 'reversePermit', pos=[HANDOFF[0], HANDOFF[1], HANDOFF[2]], rot=[-0.3, 0, 0], opts={'s': 0.9},
                 keys=[k(round(GIVE6 + 0.05, 3), to=[r(ME6[0] + 0.1), 1.47, r(ME6[2] - 0.32)], dur=0.2, ease='inOut')])],
        cams=[FC(0.0, [-1.9, 1.8, 1.4], [[ME6[0], 2.45, ME6[2]], [ME6[0], 0.3, ME6[2]], [CLERK[0], 2.35, CLERK[2]], [HANDOFF[0], HANDOFF[1], HANDOFF[2]], [-1.75, 3.0, -3.45], [1.75, 3.42, -3.45]], top=0.06, bottom=0.74, lenses=range(30, 62))])
        # (pass 2b) from in front on his right: he stands at 60 % of the width, the clerk's head beside his, his hand going back between them (from the
        # side with the whole title he stood at the edge of the frame)   # (pass 2) the whole title (PRÉFECTUR was cut)
st.cue('sfx:paper', 'S06', GIVE6, 0.3)

# 7: back to front. Over his shoulder: he holds the licence up to the face on his back: pink, every word mirrored, the photo the back of a head; he
#    looks at it, deadpan, a slow blink
D7 = st.dur('S07')
ME7 = [0.35, 0, -0.35]
LIC7 = {'touch': {'R': ['head', 0.42, 0.18, 0.24, 1, 0.05]}, 'hands': {'R': 'pinch'}}   # (pass 2) beside the face on his back, in the frame of the turned head (his palm covered half the licence and the licence half his face)                                                # (first look) a step away from the counter: the camera fits between it and the face on his back (behind the counter it shot through the glass past the clerk)
st.shot('S07', 'poste', setOpts={'title': 'PRÉFECTURE'}, actors=[
        act('mec', ME7, 0, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**BACK, **LIC7, 'face': {'gx': -0.7, 'gy': 0.3}}, toonDur=0.0),
            k(0.75, toon={**BACK, **LIC7, 'face': {'gx': -0.7, 'gy': 0.3, 'lid': 1.0}}, toonDur=0.08),
            k(0.95, toon={**BACK, **LIC7, 'face': {'gx': 0.0, 'lid': 0.45}}, toonDur=0.12)])],   # a slow blink, then at us
        props=[P('permis7', 'reversePermit', on={'actor': 'mec', 'hand': 'R', 'offset': [0.11, 0.12, 0.03], 'face': 'camera'}, opts={'s': 1.5, 'bright': True})],   # (pass 2) bigger, held by its corner
        cams=[FC(0.0, [0.55, 1.95, -1.9], [[ME7[0], 2.4, ME7[2]], [ME7[0], 1.55, ME7[2]], [-0.1, 1.9, ME7[2]], [1.0, 1.9, ME7[2]]], top=0.18, bottom=0.66, lenses=range(30, 71), inside=(-5.8, 5.8, 0.0, 6.5, -1.95, 6.0)),
              glide([FC(0.85, [0.5, 1.95, -1.5], [[ME7[0], 2.35, ME7[2]], [ME7[0], 1.6, ME7[2]], [0.0, 1.85, ME7[2]], [0.95, 1.85, ME7[2]]], top=0.16, bottom=0.66, lenses=range(30, 71), inside=(-5.8, 5.8, 0.0, 6.5, -1.95, 6.0))], 0.3)])
        # (pass 2b) kept in front of the counter glass (backed off by the fit, the first camera stood behind a black post of the window frame: a dark bar
        # down the middle of the frame)   # (pass 2) a push in on the mirrored licence and his face

# 8: he only drives in reverse. The boulevard from high up: his little red car flies down it backwards; the traffic comes the other way
D8 = st.dur('S08'); XL8 = 1.6; ZA8, ZB8 = -17.0, -2.5
# (pass 2) along the boulevard, not across it: his open car comes at us rear first, his face over the back of it, while the car in the next lane comes
# at us front first (side on and crossing, the two cars slid sideways and overlapped: nothing said reverse)
CAR8 = lambda pid, x, z0, z1, ry, col: P(pid, 'car', pos=[x, 0, z0], ry=ry, opts={'color': col, 'convertible': True, 'interior': '#E8D2B0'}, keys=[k(0.0, to=[x, 0, z1], dur=round(D8 + 0.05, 3), ease='linear')])
st.shot('S08', 'parisStreet', setOpts=STREETT, actors=[act('mec', [r(XL8 - 0.4), 0.12, r(ZA8 - 0.15)], 180, 'drive', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**BACK, 'reach': {'L': [r(XL8 - 0.95), 1.05, r(ZA8 - 0.4), 1, 0.05]}, 'hands': {'L': 'flat'}}, toonDur=0.0),
            k(0.0, to=[r(XL8 - 0.4), 0.12, r(ZB8 - 0.15)], dur=round(D8 + 0.05, 3), glide=True, ease='linear', face='keep')])],
        props=[CAR8('car8', XL8, ZA8, ZB8, 90, '#C9473A'), CAR8('car8b', r(XL8 - 3.4), -11.0, -4.5, -90, '#3E7CC9'), CAR8('car8c', r(XL8 - 3.4), -24.0, -17.5, -90, '#E8C547')],
        cams=[cam(0.0, [r(XL8 + 1.0), 3.0, 6.5], [r(XL8 + 0.9), 2.9, 6.0], [r(XL8 - 0.8), 0.6, -8.0], [r(XL8 - 0.8), 0.6, -6.5], lens=38)])
        # (pass 2) high ahead of him on the boulevard, the cut later (on « arrière »): the wide holds 1.2 s
st.cue('engine', 'S08', 0.0, 0.3, round(D8, 3)); st.cue('sfx:beep', 'S08', 0.05, 0.2)

# 9: in reverse. Close, from behind the car: it comes at us backwards, his face in the rear window, an arm over the seat, cool; the driver he passes
#    drops his jaw
D9 = st.dur('S09'); XL9 = 1.6; ZA9 = -6.0; ZB9 = r(ZA9 + 9.0 * D9); XO9 = r(XL9 - 2.4); ZO9a = -3.4; ZO9b = r(ZO9a + 3.0 * D9)
# (pass 2) fast (9 m/s) so the street streams by, in an open car so his face is in the light (behind the rear window the cabin was a dark room)
st.shot('S09', 'parisStreet', setOpts=STREETT, actors=[
        act('mec', [r(XL9 - 0.4), 0.12, r(ZA9 - 0.15)], 180, 'drive', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**BACK, 'reach': {'L': [r(XL9 - 0.95), 1.05, r(ZA9 - 0.4), 1, 0.05]}, 'hands': {'L': 'flat'}}, toonDur=0.0),
            k(0.0, to=[r(XL9 - 0.4), 0.12, r(ZB9 - 0.15)], dur=round(D9 + 0.05, 3), glide=True, ease='linear', face='keep')]),
        act('voisin', [r(XO9 + 0.4), 0.12, r(ZO9a + 0.15)], 0, 'drive', 'neutral', keys=[k(0.0, look=[r(XO9 + 0.4), 1.4, 3.0]),
            k(0.0, to=[r(XO9 + 0.4), 0.12, r(ZO9b + 0.15)], dur=round(D9 + 0.05, 3), glide=True, ease='linear', face='keep'),
            k(0.16, look={'actor': 'mec', 'cheat': 0.55}), k(0.24, toon={'sq': [0.95, 1.07, 0.95], 'face': {'pop': 0.7, 'popLen': 0.3, 'jaw': 1.0, 'brow': 1.0}}, toonDur=0.033, toonEase='out')])],   # (pass 2b) as the red car draws level   # eyes on stalks, jaw to the floor
        props=[P('car9', 'car', pos=[XL9, 0, ZA9], ry=90, opts={'color': '#C9473A', 'convertible': True, 'interior': '#E8D2B0'}, keys=[k(0.0, to=[XL9, 0, ZB9], dur=round(D9 + 0.05, 3), ease='linear')]),
               P('car9b', 'car', pos=[XO9, 0, ZO9a], ry=-90, opts={'color': '#3E7CC9', 'convertible': True}, keys=[k(0.0, to=[XO9, 0, ZO9b], dur=round(D9 + 0.05, 3), ease='linear')])],
        cams=[cam(0.0, [r(XO9 - 0.6), 1.65, r(ZO9a + 2.4)], [r(XO9 - 0.6), 1.65, r(ZO9b + 2.4)], [r(XO9 + 1.1), 1.4, r(ZO9a - 0.4)], [r(XO9 + 1.1), 1.4, r(ZO9b - 0.4)], lens=50)])
        # (pass 2b) riding beside the overtaken driver: his take on the left, the red car streaking past behind him rear first, the face over its seat
        # (from behind the car, its boot filled the frame and hid the man)
        # (pass 2) tracking just ahead of him: his face over the back of the seat, the overtaken driver's take beside it
st.cue('sfx:honkLong', 'S09', 0.12, 0.25); st.cue('sfx:beep', 'S09', 0.0, 0.15)

# 10: yesterday an osteopath put his head straight. His room, a spine on the wall: he sits on a stool, his back to us... the osteopath stands at his
#     face, takes his head in both hands, his tongue out in concentration, and winds it up the other way
D10 = st.dur('S10')
ME10 = [0.0, 0, -1.6]; OST = [0.0, 0, -2.3]
HEAD = lambda tw: {'reach': {'L': [0.22, 1.62, r(ME10[2] - 0.05), 1, 0.05], 'R': [-0.22, 1.62, r(ME10[2] - 0.05), 1, 0.05]}, 'hands': {'L': 'flat', 'R': 'flat'}, 'face': {'tongue': 0.6, 'tongueLen': 0.1, 'brow': -0.4}}   # (first look) at the sides of his seated head (at 2 m they waved above it)
st.shot('S10', 'office', setOpts={'door': False}, actors=[
        act('mec', ME10, 0, 'sit', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=BACK, toonDur=0.0),
            *[k(t_, toon=NECK(round(PI + 0.18 * (n_ + 1), 3), extra={'sq': [1.02, 0.98, 1.02], 'face': {'lid': 0.3, 'brow': 0.3}}), toonDur=0.05, toonEase='out') for n_, t_ in enumerate((0.55, 0.8, 1.05))],
            # (pass 2) three notches the wrong way, the neck coiling tighter
            *[k(round(1.12 + 0.07 * q_, 3), toon=NECK(PI + 0.54, extra={'sq': [1.0, (1.015 if q_ % 2 else 0.99), 1.0], 'face': {'lid': 0.3, 'brow': 0.3}}), toonDur=0.033) for q_ in range(6)]]),   # held, shaking
        act('osteo', [-0.32, 0, -2.3], 12, 'stand', 'determined', keys=[k(0.0, look=[0.0, 2.0, ME10[2]]), k(0.25, toon=HEAD(0), toonDur=0.25, toonEase='out'),   # (pass 2) a step to his left: the face on the man's back seen past his shoulder
            *[k(t_, toon={**HEAD(0), 'bend': {'spine': [0, round(-0.1 * (n_ + 1), 3), 0, 1, None]}, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.05, toonEase='out') for n_, t_ in enumerate((0.55, 0.8, 1.05))],
            *[k(round(1.12 + 0.07 * q_, 3), toon={**HEAD(0), 'bend': {'spine': [0, -0.3, 0, 1, None]}, 'sq': [1.05, (0.95 if q_ % 2 else 0.97), 1.05], 'face': {'tongue': 0.85, 'tongueLen': 0.12, 'brow': -0.7, 'lid': 0.5}}, toonDur=0.033) for q_ in range(6)]])],
            # (pass 2) a notch at a time with him, then the strain held before the release, the tongue further out
        props=[P('bench10', 'bench', pos=[0.0, 0, -1.6], ry=90), P('screen10', 'plainWall', pos=[-0.75, 1.1, -0.62], ry=180, opts={'w': 1.4, 'h': 2.2, 'color': '#DCE6E8'}),
               P('poster10', 'spinePoster', pos=[-0.75, 1.5, -0.64], ry=180, opts={'w': 0.7, 'h': 1.05})],   # (pass 2) the spine poster on a screen behind him, in this view
        cams=[FC(0.0, [0.95, 2.5, -3.2], [[0.0, 2.08, -1.6], [0.0, 1.25, -1.6], [-0.3, 1.62, -1.65], [0.3, 1.62, -1.65], [0.05, 2.15, -2.3], [-0.75, 2.0, -0.64]], top=0.1, bottom=0.74, drift=(-0.06, 0.0, 0.0))])
        # (pass 2) high over the osteopath's shoulder, clear of his head: his hands on the box head, his tongue, the face on the man's back (from 1.7 m the
        # camera looked up into the dark ceiling: 40 % of the frame navy)
        # (first look) from behind the osteopath, three-quarters on the face on his back (side on, both faces were profiles)

# 11: straight. Close: CRAC! the head snaps round to the front: his face to us at last, a blink, the hint of a smile; the osteopath beams
D11 = st.dur('S11'); CR11 = 0.18; OST11 = [0.62, 0, -2.25]   # (pass 2) the osteopath to his right (his head sat on top of the man's like a totem)
st.shot('S11', 'office', setOpts={'door': False}, actors=[
        act('mec', ME10, 0, 'sit', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=NECK(PI + 0.45), toonDur=0.0),
            k(round(CR11 - 0.05, 3), toon=NECK(PI + 0.66, extra={'sq': [1.02, 0.98, 1.02]}), toonDur=0.04),   # (pass 2) one more notch: the anticipation...
            k(CR11, toon=NECK(-0.35, extra={'sq': [1.1, 0.9, 1.1], 'scl': {'head': [1.25, 0.92, 1.0]}, 'face': {'eye': 0.35, 'brow': 0.8}}), toonDur=0.033, toonEase='out'),   # ...CRAC: round in one smeared frame, 20 degrees past the front...
            k(round(CR11 + 0.1, 3), toon=NECK(0.12, extra={'sq': [1.0, 1.02, 1.0], 'face': {'lid': 0.4}}), toonDur=0.08), k(round(CR11 + 0.2, 3), toon=NECK(0.0, extra={'face': {'lid': 0.45}}), toonDur=0.08),   # ...and back
            k(round(CR11 + 0.5, 3), toon=NECK(0.0, extra={'face': {'lid': 1.0}}), toonDur=0.06), k(round(CR11 + 0.62, 3), toon=NECK(0.0, extra={'face': {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}}), toonDur=0.1),   # a blink, relief
            k(round(D11 - 0.12, 3), toon=NECK(0.6, extra={'face': {'lid': 0.3, 'mouth': 'smile'}}), toonDur=0.12, toonEase='in')]),   # ...and it is still going
        act('osteo', OST11, -25, 'stand', 'happy', keys=[k(0.0, look=[0.0, 2.0, ME10[2]]), k(0.0, toon=HEAD(0), toonDur=0.0),
            k(CR11, toon={'reach': {'L': [1.05, 2.2, -1.95, 1, 0.05], 'R': [0.2, 2.2, -1.95, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': {'mouth': 'grin', 'brow': 0.6}}, toonDur=0.08, toonEase='out')])],   # hands off: ta-da
        props=[P('bench11', 'bench', pos=[0.0, 0, -1.6], ry=90), P('poster11', 'spinePoster', pos=[-1.2, 1.75, -3.47], opts={'w': 0.7, 'h': 1.05}),
               CRAC('crac11', [0.5, 2.45, -1.5], CR11, w=0.46)],
        cams=[FC(0.0, [0.3, 1.75, 0.55], [[0.0, 2.55, ME10[2]], [0.0, 1.15, ME10[2]], [-0.55, 2.1, ME10[2]], [1.15, 2.3, OST11[2]], [OST11[0], 2.3, OST11[2]]], top=0.14, bottom=0.72)])
st.cue('clack', 'S11', CR11, 0.45); st.cue('sfx:twang', 'S11', round(CR11 + 0.02, 3), 0.25)

# 12: it went round three times. The head spins on, three turns like a top, the tie flying out, his face going by deadpan; the osteopath steps back,
#     his eyes going round with it
D12 = st.dur('S12'); SP12 = round(D12 - 0.2, 3)
st.shot('S12', 'office', setOpts={'door': False}, actors=[
        act('mec', ME10, 0, 'sit', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=NECK(0.6, extra={'face': {'mouth': 'smile'}}), toonDur=0.0),
            *[k(round(0.02 + SP12 * n_ / 6, 3), toon=NECK(round(0.6 + PI * (n_ + 1), 3), bx=(0.18 if n_ % 2 else -0.18), extra={'wind': [0.0, 0.0, 6.0], 'scl': {'head': [1.15, 1.0, 1.0]}, 'sq': [0.97, 1.03, 0.97], 'face': {'lid': 0.45}}), toonDur=round(SP12 / 6, 3), toonEase='linear') for n_ in range(6)],
            # (pass 2) three turns like a top: the head wobbles as it spins, smeared
            k(round(D12 - 0.17, 3), toon=NECK(round(0.6 + 6 * PI, 3), extra={'face': {'expr': 'dizzy', 'exprW': 1.0}, 'sq': [1.02, 0.98, 1.02]}), toonDur=0.06)]),   # dizzy eyes
        act('osteo', OST, 0, 'stand', 'surprised', keys=[k(0.0, look=[0.0, 2.0, ME10[2]]), k(0.1, to=[0.15, 0, -2.75], dur=0.3, glide=True, ease='out', face='keep'),
            k(0.1, toon={'lay': [-0.12, 0], 'face': {'jaw': 0.6, 'brow': 1.0, 'gx': 0.8}}, toonDur=0.1),
            *[k(round(0.2 + 0.11 * i, 3), toon={'lay': [-0.12, (0.06 if i % 2 else -0.06)], 'face': {'jaw': 0.6, 'brow': 1.0, 'gx': 0.9 if i % 2 else -0.9}}, toonDur=0.08) for i in range(9)],   # his eyes going round...
            *[k(round(0.25 + 0.11 * i, 3), look=[(0.45 if i % 2 else -0.45), 1.9, ME10[2]]) for i in range(8)],   # ...then his head with them
            k(round(D12 - 0.22, 3), toon={'lay': [-0.05, 0.1], 'face': {'expr': 'dizzy', 'exprW': 0.8, 'jaw': 0.4}}, toonDur=0.1)])],   # (pass 2) and he staggers, dizzy (he froze, mouth open)
        props=[P('bench12', 'bench', pos=[0.0, 0, -1.6], ry=90), P('poster12', 'spinePoster', pos=[-1.2, 1.75, -3.47], opts={'w': 0.7, 'h': 1.05})],
        cams=[FC(0.0, [0.9, 1.7, 0.35], [[0.0, 2.6, ME10[2]], [0.0, 0.9, ME10[2]], [-0.65, 2.2, ME10[2]], [0.7, 2.2, ME10[2]], [0.15, 2.2, -2.75]], top=0.12, bottom=0.72, drift=(0.0, 0.0, -0.25))])
st.cue('whoosh', 'S12', 0.05, 0.35, 0.35, 400, 1800); st.cue('whoosh', 'S12', 0.45, 0.35, 0.35, 500, 2200); st.cue('whoosh', 'S12', 0.85, 0.3, 0.35, 400, 1800)

# 13: it locked looking at the sky. From the side: the head stops with a spring, bent right back, the face to the ceiling, bobbling; deadpan; the
#     osteopath scratches his head, looking up too
D13 = st.dur('S13')
st.shot('S13', 'office', setOpts={'door': False}, actors=[
        act('mec', ME10, 0, 'sit', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=NECK(0.0, bx=-0.3), toonDur=0.0),
            k(0.12, toon=NECK(0.0, bx=-1.62, extra={'sq': [1.04, 0.96, 1.04]}), toonDur=0.06, toonEase='out'),                    # clunk: the face to the ceiling...
            *[k(round(0.2 + 0.08 * i, 3), toon=NECK(0.0, bx=round(-1.4 - 0.12 * (0.55 ** i) * (1 if i % 2 else -1), 3)), toonDur=0.07) for i in range(5)],   # ...bobbling on a spring
            k(0.62, toon=NECK(0.0, bx=-1.4, extra={'sq': [1.02, 1.03, 1.02]}), toonDur=0.2, toonEase='inOut'), k(0.86, toon=NECK(0.0, bx=-1.4), toonDur=0.15),   # (pass 2) a breath
            k(1.05, toon=NECK(0.0, bx=-1.4, extra={'face': {'lid': 1.0}}), toonDur=0.06), k(1.18, toon=NECK(0.0, bx=-1.4, extra={'face': {'lid': 0.45}}), toonDur=0.1)]),   # a blink at the ceiling
        # (pass 2) the osteopath to the side, looking at him, his own head level (tipped back too, he read as the one locked)
        act('osteo', [0.95, 0, -2.25], -56, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 1.6, ME10[2]]), k(0.35, toon={'touch': {'R': ['head', 0.0, 0.32, 0.05, 1, 0.06]}, 'hands': {'R': 'point'}, 'face': {'brow': 0.9, 'jaw': 0.3}}, toonDur=0.2),
            k(0.6, toon={'touch': {'R': ['head', 0.04, 0.34, 0.05, 1, 0.06]}, 'hands': {'R': 'point'}, 'face': {'brow': 0.9, 'jaw': 0.3}}, toonDur=0.1),
            k(0.75, toon={'touch': {'R': ['head', -0.03, 0.32, 0.05, 1, 0.06]}, 'hands': {'R': 'point'}, 'face': {'brow': 0.9, 'jaw': 0.3}}, toonDur=0.1)])],
        props=[P('bench13', 'bench', pos=[0.0, 0, -1.6], ry=90), P('poster13', 'spinePoster', pos=[-1.2, 1.75, -3.47], opts={'w': 0.7, 'h': 1.05})],
        cams=[FC(0.0, [0.8, 3.15, -0.55], [[0.0, 2.15, ME10[2]], [0.0, 1.0, ME10[2]], [-0.45, 1.5, ME10[2]], [0.45, 1.5, ME10[2]], [0.95, 2.05, -2.25]], top=0.12, bottom=0.74, drift=(-0.05, -0.05, 0.0), lenses=range(30, 52))])
        # (pass 2b) closer and higher, from the knees up: the face turned up to the ceiling read as a blank box at 70 px
        # (pass 2) high three-quarters in front: his face up to the ceiling looks at us, the man in the middle (from the side, a dark box at the edge)
st.cue('sfx:spring', 'S13', 0.12, 0.35)

# 14: he presents the weather. The TV studio from a crane above: by the map of France, his face up to the sky looks straight at us, deadpan; he points
#     at the map blind; the camera's red light; a slow blink
D14 = st.dur('S14')
ME14 = [0.8, 0, -2.0]; MAP14 = [-0.55, 1.75, -2.88]
st.shot('S14', 'pressRoom', setOpts={'backdrop': 'MÉTÉO', 'podium': False, 'flags': False, 'chairs': False, 'bg': '#26507E', 'wall': '#26507E', 'fg': '#3D6A9A'}, actors=[   # (pass 2) the backdrop words navy on blue (seven white MÉTÉO crowded his face)
        act('mec', ME14, 15, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=NECK(0.0, bx=-1.4), toonDur=0.0),
            k(0.3, toon={**NECK(0.0, bx=-1.4), 'reach': {'R': [r(MAP14[0] + 0.25), 1.75, r(MAP14[2] + 0.1), 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.1}, toonDur=0.15, toonEase='outBack'),   # points at it blind
            k(1.0, toon={**NECK(0.0, bx=-1.4), 'reach': {'R': [r(MAP14[0] - 1.15), 1.45, r(MAP14[2] + 0.1), 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.1}, toonDur=0.25, toonEase='inOut'),   # (pass 2) the blind finger lands off the map, on the wall
            k(1.5, toon={**NECK(0.0, bx=-1.4, extra={'face': {'lid': 1.0}}), 'reach': {'R': [r(MAP14[0] - 1.15), 1.45, r(MAP14[2] + 0.1), 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.1}, toonDur=0.07),
            k(1.65, toon={**NECK(0.0, bx=-1.4, extra={'face': {'lid': 0.45}}), 'reach': {'R': [r(MAP14[0] - 1.15), 1.45, r(MAP14[2] + 0.1), 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.1}, toonDur=0.12)])],
        props=[P('map14', 'weatherMap', pos=MAP14, opts={'w': 1.7, 'h': 1.05}), P('tvcam14', 'tvCamera', pos=[ME14[0], 3.05, r(ME14[2] + 0.1)], rot=[round(PI / 2, 4), 0, 0], scale=1.4, opts={'legs': False}, keys=[k(0.6, visible=False)]),   # (pass 2b) no tripod (its legs stuck out as three black bars), bigger   # (pass 2b) gone in the crane view: we are the camera
               P('rig14', 'plainWall', pos=[ME14[0], 3.85, r(ME14[2] + 0.1)], opts={'w': 0.08, 'h': 1.3, 'color': '#2A2C31'}, keys=[k(0.6, visible=False)])],   # (pass 2) the studio camera hung from the ceiling over him, pointing down
        cams=[FC(0.0, [3.0, 1.75, -0.7], [[ME14[0], 3.6, ME14[2]], [ME14[0], 0.2, ME14[2]], [MAP14[0], 1.75, MAP14[2]], [r(ME14[0] + 0.4), 1.5, ME14[2]]], top=0.08, bottom=0.74, lenses=range(30, 62)),
              # (pass 2b) tighter: the man, the camera over him and the map (with the rig's top and the far wall the man was a quarter of the frame)
              glide([FC(0.6, [0.95, 3.6, -0.55], [[ME14[0], 2.4, ME14[2]], [ME14[0], 0.2, ME14[2]], [r(MAP14[0] - 1.3), 2.25, MAP14[2]], [r(MAP14[0] + 0.9), 1.25, MAP14[2]]], top=0.12, bottom=0.74, drift=(0.0, -0.1, -0.12))], 0.4)])
        # (pass 2) first the cause, from the side: the camera hangs from the ceiling over his bent-back head; then the crane up into its view (from above
        # only, he read as an ordinary presenter); the whole map and the miss on the wall in the frame
        # (first look) closer: from 4.6 m up his upturned face was 5 % of the frame
st.cue('sfx:static', 'S14', 0.0, 0.12)

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S01', 0.75, 'mec', 'yawn'), ('S02', 0.7, 'mec', 'face_on_back'), ('S03', 0.6, 'mec', 'spoon'), ('S04', 1.0, 'mec', 'walk_back'), ('S05', 1.1, 'dame', 'double_take'),
           ('S06', 0.9, 'mec', 'counter'), ('S07', 0.5, 'mec', 'licence'), ('S09', 0.6, 'mec', 'rear_window'), ('S10', 1.0, 'mec', 'wound'), ('S11', 0.6, 'mec', 'straight'),
           ('S12', 0.7, 'osteo', 'spin'), ('S13', 0.9, 'mec', 'up'), ('S14', 1.2, 'mec', 'weather')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
for t_ in [('S06', 0.3, 'permis6', 'counter_title'), ('S07', 0.5, 'permis7', 'licence'), ('S14', 1.0, 'map14', 'meteo')]:
    st.text(t_[0], t_[1], t_[2], t_[3])

st.write("Le torticolis", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'dame': {'preset': 'madame', 'seed': 531, 'suit': '#4F7F3A', 'hair': 'bun', 'hairColor': '#8A4A22', 'build': {'width': 0.9, 'headWidth': 1.25}},
    'guichet': {'preset': 'madame', 'seed': 532, 'suit': '#7A5C9E', 'hairColor': '#2A2A2E', 'build': {'width': 0.9, 'headWidth': 1.25}},
    'voisin': {'preset': 'worker', 'seed': 533, 'hat': None, 'build': {'width': 0.95, 'headWidth': 1.2}},
    'osteo': {'preset': 'savant', 'seed': 534, 'hair': 'receding', 'hairColor': '#6B4A2A', 'build': {'width': 0.95, 'headWidth': 1.25}},
})
