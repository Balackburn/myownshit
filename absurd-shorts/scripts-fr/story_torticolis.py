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
         ('S08', 'L05', 0), ('S09', 'L05', 4), ('S10', 'L06', 0), ('S11', 'L06', 5), ('S12', 'L07', 0), ('S13', 'L08', 0), ('S14', 'L09', 0)])

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
SPOON = lambda pid: P(pid, 'spoon', on={'actor': 'mec', 'hand': 'R', 'offset': [0, -0.02, 0.06]}, scale=1.6)

# 1: the hook. His bedroom, morning: sitting up in bed under the blanket, eyes shut; the alarm clock rings on the bedside table; his eyes open, a big
#    stretch, arms up, and a yawn; he slaps the clock quiet
D1 = st.dur('S01')
BED = [-2.6, 0.62, -2.35]
st.shot('S01', 'chambre', actors=[
        act('mec', BED, 0, 'sitFloor', 'sleepy', keys=[k(0.0, look=[-1.75, 0.8, -2.5]), k(0.0, toon={'face': {'lid': 1.0}}, toonDur=0.0),
            k(0.25, toon={'face': {'lid': 0.55}}, toonDur=0.08), k(0.4, toon={'face': {'lid': 1.0}}, toonDur=0.05), k(0.48, toon={'face': {'lid': 0.5}}, toonDur=0.06),   # opens, blinks, opens
            k(0.58, toon={'reach': {'L': [-2.3, 2.15, -2.3, 1, 0.05], 'R': [-2.9, 2.15, -2.3, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'sq': [0.94, 1.08, 0.94],
                          'face': {'expr': 'yawn', 'exprW': 1.0}}, toonDur=0.22, toonEase='inOut'),   # the stretch and the yawn
            k(1.05, toon={'reach': {'L': [-1.75, 0.85, -2.5, 1, 0.05]}, 'hands': {'L': 'flat'}, 'face': {'lid': 0.45}}, toonDur=0.12, toonEase='out'), k(1.0, look=[-1.75, 0.75, -2.5])])],   # slaps the clock
        props=[P('table1', 'table', pos=[-1.75, 0, -2.5], opts={'w': 0.45, 'd': 0.45, 'h': 0.55, 'color': '#C99A62', 'legs': '#8A6A44'}),
               P('clock1', 'alarmClock', pos=[-1.75, 0.55, -2.5], ry=-60, scale=0.8, opts={'time': '07:00', 'ringAt': 0.0, 'stopAt': 1.12})],
        cams=[FC(0.0, [-0.9, 1.45, 0.2], [[BED[0], 2.35, BED[2]], [BED[0], 0.6, r(BED[2] + 0.9)], [-1.75, 0.5, -2.5], [-2.95, 2.2, -2.3]], top=0.12, bottom=0.74, drift=(0.0, 0.0, -0.12))])
st.cue('sfx:ring', 'S01', 0.0, 0.35); st.cue('sfx:bonk', 'S01', 1.12, 0.3)

# 2: the stiff neck. Standing by the bed, his back to us: he turns to look behind him; on « torticolis » CRAC: the head snaps on round past his back,
#    overshoots and settles: his face looks at us over his own back, deadpan; a slow blink
D2 = st.dur('S02'); CR2 = 0.38
ME2 = [-1.2, 0, -1.4]
st.shot('S02', 'chambre', actors=[
        act('mec', ME2, 180, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=NECK(0.0), toonDur=0.0),
            k(0.08, toon=NECK(0.35, extra={'sq': [1.02, 0.98, 1.02]}), toonDur=0.06),                                   # the anticipation: a little the other way
            k(0.16, toon=NECK(-1.9), toonDur=round(CR2 - 0.16, 3), toonEase='in'),                                    # turning to look back...
            k(CR2, toon=NECK(-3.62, extra={'sq': [0.96, 1.05, 0.96], 'face': {'eye': 0.35, 'brow': 0.6}}), toonDur=0.05, toonEase='out'),   # ...CRAC: past his back...
            k(round(CR2 + 0.1, 3), toon=NECK(-PI + 0.12, extra={'face': {'lid': 0.3}}), toonDur=0.08),
            k(round(CR2 + 0.2, 3), toon=NECK(-PI, extra={'face': {'lid': 0.45}}), toonDur=0.08),                        # ...and settles there, the face to us
            k(round(D2 - 0.32, 3), toon=NECK(-PI, extra={'face': {'lid': 1.0}}), toonDur=0.06), k(round(D2 - 0.18, 3), toon=NECK(-PI, extra={'face': {'lid': 0.45}}), toonDur=0.08)])],   # a slow blink
        props=[CRAC('crac2', [-0.75, 2.2, -1.2], CR2, w=0.46)],
        cams=[FC(0.0, [-0.75, 1.75, 0.65], [[ME2[0], 2.45, ME2[2]], [ME2[0], 0.95, ME2[2]], [r(ME2[0] - 0.45), 1.9, ME2[2]], [r(ME2[0] + 0.55), 2.3, ME2[2]]], top=0.12, bottom=0.72, drift=(0.0, 0.0, -0.08))])
st.cue('clack', 'S02', CR2, 0.45); st.cue('sfx:twang', 'S02', round(CR2 + 0.02, 3), 0.25)

# 3: his head stayed turned to the back. Breakfast in the kitchen, from behind him: his body faces the table, his face faces us; the spoon dips in the
#    bowl and goes up over his shoulder to the face on his back, the arm bending backwards; he chews, deadpan; again
D3 = st.dur('S03')
ME3 = [0.0, 0, -1.25]; BOWL = [0.08, 0.76, -1.75]
MOUTH3 = {'touch': {'R': ['face', 0.16, 0.22, 0.07, 1, 0.05]}, 'hands': {'R': 'pinch'}}   # (first look) at the corner of the mouth: in the middle the hand hid it
DIP3 = {'reach': {'R': [BOWL[0], 0.86, BOWL[2], 1, 0.05]}, 'hands': {'R': 'pinch'}}
st.shot('S03', 'kitchenDay', actors=[
        act('mec', ME3, 180, 'sit', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**BACK, **DIP3}, toonDur=0.0),
            *[x for t_ in (0.3, 1.2) for x in (
                k(t_, toon={**BACK, **MOUTH3, 'face': {'mouth': 'O', 'jaw': 0.35}}, toonDur=0.24, toonEase='inOut'),                 # up over his shoulder to the mouth on his back
                k(round(t_ + 0.32, 3), toon={**BACK, **MOUTH3, 'face': {'mouth': 'flat', 'puff': 0.4}}, toonDur=0.06),               # in
                *[k(round(t_ + 0.42 + 0.1 * j, 3), toon={**BACK, **MOUTH3, 'face': {'jaw': 0.18 if j % 2 == 0 else 0.0, 'puff': 0.3}}, toonDur=0.05) for j in range(3)],   # chewing
                k(round(t_ + 0.74, 3), toon={**BACK, **DIP3}, toonDur=0.16, toonEase='inOut'))]])],                                   # back down to the bowl
        props=[P('table3', 'table', pos=[0.0, 0, -1.85], opts={'w': 1.1, 'd': 0.75, 'h': 0.74, 'color': '#F2EEE2', 'legs': '#9FD8C8'}),
               P('bench3', 'bench', pos=[0.0, 0, -1.25], ry=90), P('bowl3', 'cerealBowl', pos=BOWL), SPOON('spoon3')],
        cams=[FC(0.0, [0.55, 1.5, 0.95], [[ME3[0], 2.25, ME3[2]], [ME3[0], 0.6, ME3[2]], [-0.5, 1.6, ME3[2]], [0.55, 1.6, ME3[2]], [BOWL[0], BOWL[1], BOWL[2]]], top=0.12, bottom=0.74, drift=(0.0, 0.0, -0.2))])
st.cue('sfx:clink', 'S03', 0.25, 0.2); st.cue('sfx:clink', 'S03', 1.15, 0.2)

# 4: since then he walks backwards. The street from low down: he walks backwards toward us, his back first, his face leading over it, the walk played
#    in reverse; a pigeon steps aside
D4 = st.dur('S04'); X4 = 7.0
st.shot('S04', 'parisStreet', actors=[
        act('mec', [X4, 0, -3.2], 180, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=BACK, toonDur=0.0),
            k(0.0, to=[X4, 0, -0.6], dur=round(D4 + 0.03, 3), clip='walk', then='walk', ease='linear', face='keep', speed=-1.0)])],   # the cycle played backwards: real backward steps
        props=[],
        cams=[FC(0.0, [r(X4 - 0.55), 0.95, 2.6], [[X4, 2.4, -0.6], [X4, 0.0, -0.6], [X4, 2.4, -3.2], [r(X4 - 0.5), 1.5, -0.6], [r(X4 + 0.5), 1.5, -0.6]], top=0.1, bottom=0.74, drift=(0.0, 0.0, 0.25))])

# 5: to see in front of him. From the side: he walks backwards, the face leading; a lady coming the other way says hello, he nods back; she passes, then
#    looks back: a double take, her jaw drops
D5 = st.dur('S05'); X5 = 7.4
st.shot('S05', 'parisStreet', actors=[
        act('mec', [r(X5 + 1.1), 0, 0.0], 90, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=BACK, toonDur=0.0),
            k(0.0, to=[r(X5 - 0.9), 0, 0.0], dur=round(D5 + 0.03, 3), clip='walk', then='walk', ease='linear', face='keep', speed=-1.0),
            k(0.45, toon=NECK(PI, bx=0.22), toonDur=0.08), k(0.6, toon=BACK, toonDur=0.1)]),                                            # a nod to her
        act('dame', [r(X5 - 1.6), 0, -0.55], 90, 'stand', 'happy', keys=[k(0.0, look={'actor': 'mec', 'dy': -0.1}),
            k(0.0, to=[r(X5 + 1.9), 0, -0.55], dur=round(D5 + 0.03, 3), clip='walk', then='walk', ease='linear', face='move'),
            k(0.4, toon={'face': {'mouth': 'smile'}}, toonDur=0.1),
            k(0.85, look={'actor': 'mec', 'dy': -0.1, 'cheat': 0.35}), k(0.95, toon={'face': {'jaw': 0.85, 'brow': 1.0, 'eye': 0.3}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.05, toonEase='out')])],   # her double take: the jaw drops
        props=[],
        cams=[FC(0.0, [r(X5 - 2.3), 1.5, 3.4], [[r(X5 - 1.2), 2.4, -0.3], [r(X5 + 1.2), 2.4, -0.3], [X5, 0.0, -0.3]], top=0.14, bottom=0.74, drift=(-0.2, 0.0, 0.0))])   # (first look) three-quarters on his face (side on it was a profile)
st.cue('sfx:gasp', 'S05', 0.95, 0.25)

# 6: the prefecture issued him a licence. The counter, PRÉFECTURE: he stands with his back to it, his face to the clerk; she holds out the licence over
#    the counter; he takes it with his hand behind his back
D6 = st.dur('S06'); GIVE6 = 0.85
ME6 = [0.35, 0, -1.65]; CLERK = [0.35, 0, -2.95]; HANDOFF = [0.35, 1.22, -2.05]
st.shot('S06', 'poste', setOpts={'title': 'PRÉFECTURE'}, actors=[
        act('mec', ME6, 0, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=BACK, toonDur=0.0),
            k(round(GIVE6 - 0.25, 3), toon={**BACK, 'reach': {'R': [HANDOFF[0], HANDOFF[1], r(HANDOFF[2] + 0.05), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'hose': 0.1}, toonDur=0.2, toonEase='inOut'),   # the arm bends back to it
            k(round(GIVE6 + 0.2, 3), toon={**BACK, 'reach': {'R': [r(ME6[0] + 0.1), 1.45, r(ME6[2] - 0.35), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'hose': 0.1}, toonDur=0.2)]),
        act('guichet', CLERK, 0, 'stand', 'neutral', keys=[k(0.0, look={'actor': 'mec', 'cheat': 0.3}), k(0.15, toon={'reach': {'R': [HANDOFF[0], HANDOFF[1], r(HANDOFF[2] - 0.05), 1, 0.05]}, 'hands': {'R': 'pinch'}}, toonDur=0.25),
            k(round(GIVE6 + 0.05, 3), toon={}, toonDur=0.2), k(round(GIVE6 + 0.1, 3), toon={'face': {'brow': 0.7}}, toonDur=0.1)])],
        props=[P('permis6', 'reversePermit', pos=[HANDOFF[0], HANDOFF[1], HANDOFF[2]], rot=[-0.3, 0, 0], opts={'s': 0.9},
                 keys=[k(round(GIVE6 + 0.05, 3), to=[r(ME6[0] + 0.1), 1.47, r(ME6[2] - 0.32)], dur=0.2, ease='inOut')])],
        cams=[FC(0.0, [2.7, 1.55, -0.55], [[ME6[0], 2.45, ME6[2]], [ME6[0], 0.3, ME6[2]], [CLERK[0], 2.35, CLERK[2]], [HANDOFF[0], HANDOFF[1], HANDOFF[2]]], top=0.12, bottom=0.74)])
st.cue('sfx:paper', 'S06', GIVE6, 0.3)

# 7: back to front. Over his shoulder: he holds the licence up to the face on his back: pink, every word mirrored, the photo the back of a head; he
#    looks at it, deadpan, a slow blink
D7 = st.dur('S07')
ME7 = [0.35, 0, -0.35]                                                # (first look) a step away from the counter: the camera fits between it and the face on his back (behind the counter it shot through the glass past the clerk)
st.shot('S07', 'poste', setOpts={'title': 'PRÉFECTURE'}, actors=[
        act('mec', ME7, 0, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**BACK, 'touch': {'R': ['face', -0.42, 0.45, 0.32, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'gx': -0.7, 'gy': 0.3}}, toonDur=0.0),
            k(0.75, toon={**BACK, 'touch': {'R': ['face', -0.42, 0.45, 0.32, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'gx': -0.7, 'gy': 0.3, 'lid': 1.0}}, toonDur=0.08),
            k(0.95, toon={**BACK, 'touch': {'R': ['face', -0.42, 0.45, 0.32, 1, 0.05]}, 'hands': {'R': 'pinch'}, 'face': {'gx': 0.0, 'lid': 0.45}}, toonDur=0.12)])],   # a slow blink, then at us
        props=[P('permis7', 'reversePermit', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.06, 0.05], 'face': 'camera'}, opts={'s': 1.15, 'bright': True})],
        cams=[FC(0.0, [0.6, 2.0, -1.45], [[ME7[0], 2.45, ME7[2]], [ME7[0], 1.45, ME7[2]], [-0.15, 1.9, ME7[2]], [0.85, 1.9, ME7[2]]], top=0.18, bottom=0.66, drift=(0.0, 0.0, 0.12))])

# 8: he only drives in reverse. The boulevard from high up: his little red car flies down it backwards; the traffic comes the other way
D8 = st.dur('S08'); Z8 = 3.0
CARS8 = [P('car8b', 'car', pos=[-14.0, 0, 6.0], opts={'color': '#3E7CC9'}, keys=[k(0.0, to=[2.0, 0, 6.0], dur=round(D8 + 0.05, 3), ease='linear')]),
         P('car8c', 'car', pos=[-26.0, 0, 6.0], opts={'color': '#E8C547'}, keys=[k(0.0, to=[-10.0, 0, 6.0], dur=round(D8 + 0.05, 3), ease='linear')])]
st.shot('S08', 'parisStreet', actors=[act('mec', [r(6.0 + 0.05), 0.12, r(Z8 - 0.4)], 90, 'drive', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=BACK, toonDur=0.0),
            k(0.0, to=[r(-6.0 + 0.05), 0.12, r(Z8 - 0.4)], dur=round(D8 + 0.05, 3), glide=True, ease='linear', face='keep')])],
        props=[P('car8', 'car', pos=[6.0, 0, Z8], opts={'color': '#C9473A'}, keys=[k(0.0, to=[-6.0, 0, Z8], dur=round(D8 + 0.05, 3), ease='linear')]), *CARS8],
        cams=[FC(0.0, [-2.0, 7.5, 16.0], [[-8.0, 0.0, Z8], [8.0, 0.0, Z8], [0.0, 1.5, 6.0], [0.0, 1.5, Z8]], top=0.2, bottom=0.7)])
st.cue('engine', 'S08', 0.0, 0.3, round(D8, 3)); st.cue('sfx:beep', 'S08', 0.05, 0.2)

# 9: in reverse. Close, from behind the car: it comes at us backwards, his face in the rear window, an arm over the seat, cool; the driver he passes
#    drops his jaw
D9 = st.dur('S09'); Z9 = 3.0
st.shot('S09', 'parisStreet', actors=[
        act('mec', [r(6.5 + 0.05), 0.12, r(Z9 - 0.4)], 90, 'drive', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={**BACK, 'reach': {'L': [r(6.5 - 0.15), 1.25, r(Z9 + 0.1), 1, 0.05]}, 'hands': {'L': 'flat'}}, toonDur=0.0),
            k(0.0, to=[r(3.0 + 0.05), 0.12, r(Z9 - 0.4)], dur=round(D9 + 0.05, 3), glide=True, ease='linear', face='keep')]),
        act('voisin', [r(-6.0 + 0.05), 0.12, r(6.0 - 0.4)], 90, 'drive', 'neutral', keys=[k(0.0, look=[4.0, 1.4, Z9]),
            k(0.0, to=[r(1.0 + 0.05), 0.12, r(6.0 - 0.4)], dur=round(D9 + 0.05, 3), glide=True, ease='linear', face='keep'),
            k(0.45, look={'actor': 'mec', 'cheat': 0.35}), k(0.55, toon={'face': {'jaw': 0.9, 'brow': 1.0, 'eye': 0.3}}, toonDur=0.05, toonEase='out')])],
        props=[P('car9', 'car', pos=[6.5, 0, Z9], opts={'color': '#C9473A'}, keys=[k(0.0, to=[3.0, 0, Z9], dur=round(D9 + 0.05, 3), ease='linear')]),
               P('car9b', 'car', pos=[-6.0, 0, 6.0], opts={'color': '#3E7CC9'}, keys=[k(0.0, to=[1.0, 0, 6.0], dur=round(D9 + 0.05, 3), ease='linear')])],
        cams=[cam(0.0, [-3.2, 2.3, 1.2], [-3.0, 2.25, 1.2], [4.6, 1.35, 2.75], [1.9, 1.3, 2.75], lens=34)])   # (first look) back and up: the rear window and his face in it (up close the car's tail filled the frame)
st.cue('sfx:honkLong', 'S09', 0.6, 0.25); st.cue('sfx:beep', 'S09', 0.0, 0.15)

# 10: yesterday an osteopath put his head straight. His room, a spine on the wall: he sits on a stool, his back to us... the osteopath stands at his
#     face, takes his head in both hands, his tongue out in concentration, and winds it up the other way
D10 = st.dur('S10')
ME10 = [0.0, 0, -1.6]; OST = [0.0, 0, -2.3]
HEAD = lambda tw: {'reach': {'L': [0.22, 1.62, r(ME10[2] - 0.05), 1, 0.05], 'R': [-0.22, 1.62, r(ME10[2] - 0.05), 1, 0.05]}, 'hands': {'L': 'flat', 'R': 'flat'}, 'face': {'tongue': 0.6, 'tongueLen': 0.1, 'brow': -0.4}}   # (first look) at the sides of his seated head (at 2 m they waved above it)
st.shot('S10', 'office', setOpts={'door': False}, actors=[
        act('mec', ME10, 0, 'sit', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=BACK, toonDur=0.0),
            k(0.75, toon=NECK(PI + 0.45, extra={'face': {'lid': 0.3, 'brow': 0.3}}), toonDur=0.4, toonEase='inOut')]),   # wound up the other way
        act('osteo', OST, 0, 'stand', 'determined', keys=[k(0.0, look=[0.0, 2.0, ME10[2]]), k(0.25, toon=HEAD(0), toonDur=0.25, toonEase='out'),
            k(0.75, toon={**HEAD(0), 'bend': {'spine': [0, -0.25, 0, 1, None]}, 'sq': [1.03, 0.97, 1.03]}, toonDur=0.4, toonEase='inOut')])],
        props=[P('bench10', 'bench', pos=[0.0, 0, -1.6], ry=90), P('poster10', 'spinePoster', pos=[-1.2, 1.75, -3.47], opts={'w': 0.7, 'h': 1.05})],
        cams=[FC(0.0, [1.75, 1.65, -3.05], [[0.0, 2.55, -1.95], [0.0, 0.3, -1.6], [-0.55, 1.8, -2.3], [0.55, 1.8, -1.6]], top=0.12, bottom=0.74, drift=(-0.1, 0.0, 0.0))])
        # (first look) from behind the osteopath, three-quarters on the face on his back (side on, both faces were profiles)

# 11: straight. Close: CRAC! the head snaps round to the front: his face to us at last, a blink, the hint of a smile; the osteopath beams
D11 = st.dur('S11'); CR11 = 0.18
st.shot('S11', 'office', setOpts={'door': False}, actors=[
        act('mec', ME10, 0, 'sit', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=NECK(PI + 0.45), toonDur=0.0),
            k(CR11, toon=NECK(0.25, extra={'sq': [0.95, 1.06, 0.95], 'face': {'eye': 0.35, 'brow': 0.8}}), toonDur=0.06, toonEase='out'),   # CRAC
            k(round(CR11 + 0.12, 3), toon=NECK(-0.08, extra={'face': {'lid': 0.4}}), toonDur=0.08), k(round(CR11 + 0.24, 3), toon=NECK(0.0, extra={'face': {'lid': 0.45}}), toonDur=0.08),
            k(round(CR11 + 0.5, 3), toon=NECK(0.0, extra={'face': {'lid': 1.0}}), toonDur=0.06), k(round(CR11 + 0.62, 3), toon=NECK(0.0, extra={'face': {'lid': 0.3, 'mouth': 'smile', 'brow': 0.3}}), toonDur=0.1),   # a blink, relief
            k(round(D11 - 0.12, 3), toon=NECK(0.6, extra={'face': {'lid': 0.3, 'mouth': 'smile'}}), toonDur=0.12, toonEase='in')]),   # ...and it is still going
        act('osteo', OST, 0, 'stand', 'happy', keys=[k(0.0, look=[0.0, 2.0, ME10[2]]), k(0.0, toon=HEAD(0), toonDur=0.0),
            k(CR11, toon={'reach': {'L': [0.45, 2.2, -2.0, 1, 0.05], 'R': [-0.45, 2.2, -2.0, 1, 0.05]}, 'hands': {'L': 'spread', 'R': 'spread'}, 'face': {'mouth': 'grin', 'brow': 0.6}}, toonDur=0.08, toonEase='out')])],   # hands off: ta-da
        props=[P('bench11', 'bench', pos=[0.0, 0, -1.6], ry=90), P('poster11', 'spinePoster', pos=[-1.2, 1.75, -3.47], opts={'w': 0.7, 'h': 1.05}),
               CRAC('crac11', [0.5, 2.45, -1.5], CR11, w=0.46)],
        cams=[FC(0.0, [0.55, 1.75, 0.55], [[0.0, 2.55, ME10[2]], [0.0, 1.15, ME10[2]], [-0.55, 2.1, ME10[2]], [0.62, 2.3, ME10[2]], [0.0, 2.3, OST[2]]], top=0.14, bottom=0.72)])
st.cue('clack', 'S11', CR11, 0.45); st.cue('sfx:twang', 'S11', round(CR11 + 0.02, 3), 0.25)

# 12: it went round three times. The head spins on, three turns like a top, the tie flying out, his face going by deadpan; the osteopath steps back,
#     his eyes going round with it
D12 = st.dur('S12'); SP12 = round(D12 - 0.2, 3)
st.shot('S12', 'office', setOpts={'door': False}, actors=[
        act('mec', ME10, 0, 'sit', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=NECK(0.6, extra={'face': {'mouth': 'smile'}}), toonDur=0.0),
            k(0.02, toon=NECK(0.6 + 6 * PI, extra={'wind': [0.0, 0.0, 6.0], 'sq': [0.97, 1.03, 0.97], 'face': {'lid': 0.45}}), toonDur=SP12, toonEase='inOut')]),   # three turns
        act('osteo', OST, 0, 'stand', 'surprised', keys=[k(0.0, look=[0.0, 2.0, ME10[2]]), k(0.1, to=[0.15, 0, -2.75], dur=0.3, glide=True, ease='out', face='keep'),
            k(0.1, toon={'lay': [-0.12, 0], 'face': {'jaw': 0.6, 'brow': 1.0, 'gx': 0.8}}, toonDur=0.1),
            *[k(round(0.25 + 0.22 * i, 3), toon={'lay': [-0.12, 0], 'face': {'jaw': 0.6, 'brow': 1.0, 'gx': 0.8 if i % 2 else -0.8}}, toonDur=0.1) for i in range(5)]])],   # his eyes going round
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
            k(1.05, toon=NECK(0.0, bx=-1.4, extra={'face': {'lid': 1.0}}), toonDur=0.06), k(1.18, toon=NECK(0.0, bx=-1.4, extra={'face': {'lid': 0.45}}), toonDur=0.1)]),   # a blink at the ceiling
        act('osteo', [0.15, 0, -2.6], 0, 'stand', 'neutral', keys=[k(0.0, look=[0.0, 3.2, ME10[2]]), k(0.35, toon={'touch': {'R': ['head', 0.0, 0.32, 0.05, 1, 0.06]}, 'hands': {'R': 'point'}, 'face': {'brow': 0.9, 'jaw': 0.3}}, toonDur=0.2),
            k(0.6, toon={'touch': {'R': ['head', 0.04, 0.34, 0.05, 1, 0.06]}, 'hands': {'R': 'point'}, 'face': {'brow': 0.9, 'jaw': 0.3}}, toonDur=0.1),
            k(0.75, toon={'touch': {'R': ['head', -0.03, 0.32, 0.05, 1, 0.06]}, 'hands': {'R': 'point'}, 'face': {'brow': 0.9, 'jaw': 0.3}}, toonDur=0.1)])],
        props=[P('bench13', 'bench', pos=[0.0, 0, -1.6], ry=90), P('poster13', 'spinePoster', pos=[-1.2, 1.75, -3.47], opts={'w': 0.7, 'h': 1.05})],
        cams=[FC(0.0, [2.4, 1.3, -1.2], [[0.0, 2.45, ME10[2]], [0.0, 0.3, ME10[2]], [0.15, 2.35, -2.6], [0.55, 1.6, ME10[2]]], top=0.12, bottom=0.74, drift=(-0.1, 0.0, 0.0))])
st.cue('sfx:spring', 'S13', 0.12, 0.35)

# 14: he presents the weather. The TV studio from a crane above: by the map of France, his face up to the sky looks straight at us, deadpan; he points
#     at the map blind; the camera's red light; a slow blink
D14 = st.dur('S14')
ME14 = [0.8, 0, -2.0]; MAP14 = [-0.55, 1.75, -2.88]
st.shot('S14', 'pressRoom', setOpts={'backdrop': 'MÉTÉO', 'podium': False, 'flags': False, 'chairs': False, 'bg': '#26507E', 'wall': '#26507E'}, actors=[
        act('mec', ME14, 15, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=NECK(0.0, bx=-1.4), toonDur=0.0),
            k(0.3, toon={**NECK(0.0, bx=-1.4), 'reach': {'R': [r(MAP14[0] + 0.25), 1.75, r(MAP14[2] + 0.1), 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.1}, toonDur=0.15, toonEase='outBack'),   # points at it blind
            k(1.0, toon={**NECK(0.0, bx=-1.4), 'reach': {'R': [r(MAP14[0] + 0.05), 1.45, r(MAP14[2] + 0.1), 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.1}, toonDur=0.25, toonEase='inOut'),
            k(1.5, toon={**NECK(0.0, bx=-1.4, extra={'face': {'lid': 1.0}}), 'reach': {'R': [r(MAP14[0] + 0.05), 1.45, r(MAP14[2] + 0.1), 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.1}, toonDur=0.07),
            k(1.65, toon={**NECK(0.0, bx=-1.4, extra={'face': {'lid': 0.45}}), 'reach': {'R': [r(MAP14[0] + 0.05), 1.45, r(MAP14[2] + 0.1), 1, 0.08]}, 'hands': {'R': 'point'}, 'hose': 0.1}, toonDur=0.12)])],
        props=[P('map14', 'weatherMap', pos=MAP14, opts={'w': 1.7, 'h': 1.05}), P('tvcam14', 'tvCamera', pos=[2.1, 0, -0.5], ry=-140)],
        cams=[FC(0.0, [0.95, 3.6, -0.55], [[ME14[0], 2.4, ME14[2]], [ME14[0], 0.2, ME14[2]], [r(MAP14[0] + 0.15), 2.25, MAP14[2]], [r(MAP14[0] + 0.85), 1.25, MAP14[2]]], top=0.12, bottom=0.74, drift=(0.0, -0.1, -0.12))])
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
