#!/usr/bin/env python3
"""L'écho (story 60, cycle 22 of the cartoon staging): this man shouted in the mountains. The echo never came back. He filed a complaint. The
gendarmerie put out a missing notice. It was reported in three valleys. Yesterday the echo came home. Two years late. It shouted for three days. The
gendarmerie fined the man for the noise.
Staging: on a rocky summit he cups his hands round his mouth, fills his chest and shouts: his jaw stretches down, his own shout blows his hair and tie
forward, and big cut-out letters « OHÉ ! » burst out of his mouth and fly off over the valley; he waits with a hand cupped behind his ear, his ears
flapped out, leaning: crickets. At the gendarmerie he mimes his shout to a gendarme who takes it down; the gendarme slaps a missing notice (a speech
bubble « OHÉ ! ») on the wall; the notices are everywhere in town; a hiker and a farmer in two valleys point at the letters crossing their skies.
Yesterday, in his street, the letters come back down it, growing huge: his eyes go out on stalks; SPLAT, he is flattened on the pavement like a
sheet of paper, then peels himself up stiff as a board and pops back to his shape. At night the giant letters rattle between the buildings, people
holding their ears; by day he has rings under his eyes and holds his ears. The gendarme slaps a fine on his forehead; close on him, the ticket on his
forehead, a tiny « ohé » drifts down; a slow blink.
Natural look; cycle 22 tools: props_echo.js (shoutLetters, mountainRange, missingPoster, fineTicket, summitRock; pass 2: summitPeak, summitSign, river,
trekPole, pitchfork).
Pass 2 (reviews 6.0 / 6.2): a real summit 14 m over a valley with a river and a village, the sign in the shot, the hook in profile then over his
shoulder after the word; the cupped hand on the near ear; a two-shot at the desk; the slap beside the bubble with PAF where it lands; a double take
on the notice; a hiker (pack, pole) and a farmer (cap, pitchfork, cow) who read; the word down the open road and the stalks in profile; the pancake
lifted off the pavement and the board swung up edge-on; a darker night with lamp pools; a wind-up on the fine, the fine above his eyes; the tiny
« ohé » landing on his shoulder."""
from story_kit import *
import math

st = Story('echo', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L04', 5), ('S06', 'L05', 0), ('S07', 'L05', 4),
         ('S08', 'L06', 0), ('S09', 'L07', 0), ('S10', 'L08', 0), ('S11', 'L08', 3), ('S12', 'L09', 0), ('S13', 'L09', 4)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(28, 57), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    if lens > max(lenses): print(f'  WARNING lens {lens} from {frm}: wider than {max(lenses)}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def r(v, n=3): return round(v, n)

def FLY(pts):
    """(check) a flight through timed points [[t, x, y, z], ...] as prop keys in world space: pos at the first point, then 'to' keys between them
    (with face='camera' the whole prop turns to the lens about its origin, so a path kept inside the prop would turn with it)"""
    return {'pos': list(pts[0][1:]), 'keys': [k(pts[i][0], to=list(pts[i + 1][1:]), dur=round(pts[i + 1][0] - pts[i][0], 3), ease='linear') for i in range(len(pts) - 1)]}
DEAD = {'lid': 0.45}
BURST = lambda pid, pos, at_, text, w=0.5: P(pid, 'hicBurst', pos=pos, face='camera', opts={'at': [at_], 'w': w, 'text': text, 'inner': 0.78, 'fit': 0.56})
ALPS = {'grass': '#8DB86A', 'clouds': 28}
TOP = 14.0                                                                 # (pass 2) the summit 14 m over the valley floor (on 3 m it read as a boulder on a meadow)
ME_S = [0.0, TOP, 0.2]                                                     # him on the summit, facing the valley (-Z)
RING = lambda sid, h=36, d=62, w=150: [P(f'mtnN{sid}', 'mountainRange', pos=[0, 0, -d], opts={'n': 9, 'w': w, 'h': h, 'd': 22, 'seed': 7}),
                                      P(f'mtnW{sid}', 'mountainRange', pos=[-d, 0, 0], ry=90, opts={'n': 8, 'w': w, 'h': r(h * 0.83), 'd': 22, 'seed': 13}),
                                      P(f'mtnE{sid}', 'mountainRange', pos=[d, 0, 0], ry=-90, opts={'n': 8, 'w': w, 'h': r(h * 0.89), 'd': 22, 'seed': 19}),
                                      P(f'mtnS{sid}', 'mountainRange', pos=[0, 0, d], ry=180, opts={'n': 9, 'w': w, 'h': r(h * 0.78), 'd': 22, 'seed': 23})]
HIGH = lambda sid: RING(sid, 19, 80, 200)                                  # (pass 2) from the summit the ranges sit round the horizon, not over his head
PEAK = lambda sid: P(f'peak{sid}', 'summitPeak', pos=[0, r(TOP - 1.4), 0], opts={'h': r(TOP - 1.4), 'seed': 3})   # the mountain under the rock
SUMMIT = lambda sid: P(f'rock{sid}', 'summitRock', pos=[0, TOP, 0], opts={'r': 1.6, 'rail': False, 'sign': False})
SIGNP = [0.45, TOP, 1.35]                                                  # behind him on the left of the frame, seen from the three-quarter camera
SIGN = lambda sid, ry=155: P(f'sign{sid}', 'summitSign', pos=SIGNP, ry=ry, opts={'alt': '2 040 m', 'w': 0.64})
VILLAGE = [(-14, -62, 20), (-8, -74, -10), (6, -66, 160), (12, -80, 200), (-20, -72, 40), (-44, 30, 70), (-52, 40, 100), (-38, 44, 80), (-58, 26, 120)]   # (stills 2) farther and smaller: at 33 m one filled the shot
VALLEY = lambda sid: [P(f'riv{sid}', 'river', pos=[0, 0, -58], opts={'len': 260, 'w': 4, 'amp': 7, 'waves': 1.6}), P(f'rivb{sid}', 'river', pos=[-48, 0, 0], ry=80, opts={'len': 200, 'w': 4, 'amp': 6, 'waves': 1.3, 'phase': 1.0}),
                      *[P(f'cot{sid}{i}', 'cottage', pos=[x_, 0, z_], ry=ry_, scale=0.9) for i, (x_, z_, ry_) in enumerate(VILLAGE)],
                      *[P(f'cld{sid}{i}', 'cumulus', pos=[x_, y_, z_], opts={'w': w_, 'h': 4, 'n': 12, 'seed': 30 + i}) for i, (x_, y_, z_, w_) in enumerate([(-26, 8.5, 18, 22), (-40, 9.5, -6, 20), (-30, 7.5, 34, 24)])]]   # (stills 2) clouds under the summit: the height reads; (stills 3) none in the view over the valley (close, they were snowballs)
CUP = lambda k_: {'touch': {'L': ['face', 0.34, 0.24, r(0.05 + 0.04 * k_), 1, 0.03, [1.0, 0.2, 0.0]], 'R': ['face', -0.34, 0.24, r(0.05 + 0.04 * k_), 1, 0.03, [-1.0, 0.2, 0.0]]}, 'hands': {'L': 'open', 'R': 'open'}}
MOUTH_S = [ME_S[0], r(ME_S[1] + 1.72), r(ME_S[2] - 0.25)]

# 1: the hook. On a rocky summit high over a valley (SOMMET 2 040 m): low, in profile at the edge of the rock, he cups his hands round his mouth, fills
#    his chest (leaning back, cheeks puffed), and SHOUTS: his jaw stretches down under his hands, his own shout blows his hair and tie forward, and the
#    letters « OHÉ ! » burst out of his mouth; cut over his shoulder: the word shrinking away over the valley, the river and the village far below,
#    his tie and hair falling back
D1 = st.dur('S01'); SH1 = 0.5; CUT1 = 1.0
st.shot('S01', 'grassland', setOpts=ALPS, actors=[
        act('mec', ME_S, 180, 'stand', 'unimpressed', keys=[k(0.0, look=[0.0, r(TOP + 1.7), -10.0]), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.06, toon={**CUP(0.0), 'sq': [1.06, 1.03, 1.12], 'bend': {'spine': [-0.28, 0, 0, 1, None], 'neck': [-0.15, 0, 0, 1, None]}, 'face': {'lid': 0.7, 'puff': 1.0, 'cheeks': 1.0, 'brow': 0.4}}, toonDur=0.3, toonEase='inOut'),   # (pass 2) a big breath: the chest swelling, leaning back...
            k(r(SH1 - 0.06), toon={**CUP(0.3), 'sq': [1.08, 1.02, 1.15], 'bend': {'spine': [-0.32, 0, 0, 1, None], 'neck': [-0.2, 0, 0, 1, None]}, 'face': {'lid': 1.0, 'puff': 1.0, 'cheeks': 1.0, 'brow': 0.6}}, toonDur=0.05),   # ...held a frame...
            k(SH1, toon={**CUP(1.0), 'sq': [1.04, 0.97, 1.04], 'bend': {'spine': [0.3, 0, 0, 1, None], 'neck': [0.1, 0, 0, 1, None]}, 'wind': [0.0, 1.0, 14.0], 'hairUp': 0.6,
                          'face': {'lid': 1.0, 'brow': -0.8, 'jaw': 1.0, 'jawLen': 0.75, 'mouth': 'scream', 'tongue': 0.3}}, toonDur=0.05, toonEase='out'),   # ...SHOUT: the jaw stretched down under his hands, blown by his own shout
            *[k(r(SH1 + 0.1 + 0.06 * i), toon={**CUP(1.0), 'sq': ([1.05, 0.96, 1.05] if i % 2 else [1.02, 0.99, 1.02]), 'bend': {'spine': [0.3, 0, 0, 1, None], 'neck': [0.1, 0, 0, 1, None]}, 'wind': [0.0, 1.0, 14.0], 'hairUp': 0.6,
                                              'face': {'lid': 1.0, 'brow': -0.8, 'jaw': (1.0 if i % 2 else 0.9), 'jawLen': 0.75, 'mouth': 'scream', 'tongue': 0.3}}, toonDur=0.05) for i in range(7)],   # ...held, quivering
            k(CUT1, toon={'hairUp': 0.2, 'face': {'lid': 0.3, 'gx': -0.4, 'gy': -0.2}}, toonDur=0.25, toonEase='inOut')])],   # (pass 2) his hands down, his tie and hair falling back as he watches it go
        props=[*HIGH('1'), PEAK('1'), SUMMIT('1'), SIGN('1'), *VALLEY('1'),
               P('ohe1', 'shoutLetters', **FLY([[SH1] + MOUTH_S, [r(SH1 + 0.25), 0.0, r(TOP + 2.15), -2.4], [CUT1, -0.5, r(TOP + 2.9), -7.5], [D1, -1.2, r(TOP + 3.6), -19.0]]), face='camera', opts={'text': 'OHÉ !', 'size': 0.45, 'show': [SH1, 99.0],
                 'grow': [[SH1, 0.3], [r(SH1 + 0.15), 1.4], [r(SH1 + 0.35), 1.25], [CUT1, 1.5], [D1, 2.4]]}),   # out of his mouth, big, then away over the valley, still in the shot at the cut
               P('spd1', 'speedLines', **FLY([[SH1] + MOUTH_S, [r(SH1 + 0.3), 0.0, r(TOP + 2.0), -1.8], [r(SH1 + 0.6), -0.9, r(TOP + 2.6), -5.5]]), face='camera', opts={'n': 6, 'len': 0.9, 'w': 0.5, 'angle': 0.35, 'at': [[SH1, r(SH1 + 0.6)]]})],
        cams=[FC(0.0, [1.9, r(TOP + 1.0), -1.7], [[ME_S[0], r(TOP + 2.42), ME_S[2]], [ME_S[0], r(TOP + 0.45), ME_S[2]], [r(SIGNP[0] + 0.45), r(TOP + 1.55), SIGNP[2]], [0.0, r(TOP + 1.8), -1.2]], top=0.18, bottom=0.66, drift=(0.0, 0.04, -0.06)),   # (pass 2) low, three-quarters at the edge of the rock (in profile his box head shows no face): the jaw under his hands, the sign behind him...
              FC(CUT1, [1.0, r(TOP + 3.0), 2.4], [[0.35, r(TOP + 2.2), 0.2], [-0.5, r(TOP + 2.9), -7.5], [-1.2, r(TOP + 3.6), -19.0], [-2.0, 0.0, -62.0]], top=0.12, bottom=0.8, level=False, drift=(-0.05, 0.0, -0.1))])   # ...over his shoulder: the word shrinking over the valley
st.cue('sfx:gasp', 'S01', 0.08, 0.3); st.cue('whoosh', 'S01', SH1, 0.4, 1.1, 200, 900); st.cue('gust', 'S01', SH1, 0.35, 1.2)

# 2: the echo never came back. Low on his near side, against the sky: his near hand cupped behind his near ear, the ear flapping out three times,
#    leaning toward the valley, his eyes open wide: nothing; crickets; a blink, the ear folds back, the hand drops
D2 = st.dur('S02')
EAR = lambda lean, ears, face, cup=True: {**({'touch': {'L': ['face', 0.76, 0.48, -0.12, 1, 0.03, [1.0, -0.2, 0.0]]}, 'hands': {'L': 'open'}} if cup else {}),   # (stills 4) beside the ear, out from the head, the elbow low: behind it it read as a head scratch   # (pass 2) the near (left) hand behind the near ear: on the far side it read as a head scratch
                                          'ears': ears, 'bend': {'spine': [lean, 0, 0, 1, None], 'neck': [r(0.4 * lean), 0, 0, 1, None]}, 'face': face}
LISTEN = lambda **kw: {'expr': 'surprised', 'exprW': 0.6, 'lid': 0.0, 'eye': 0.4, 'gx': -0.5, 'gy': -0.2, 'brow': 0.6, 'mouth': 'o', **kw}   # (stills 2) wide open (slits on the painted base: the blink could not read)
st.shot('S02', 'grassland', setOpts=ALPS, actors=[
        act('mec', ME_S, 180, 'stand', 'unimpressed', keys=[k(0.0, look=[-2.0, r(TOP + 0.6), -14.0]), k(0.0, toon=EAR(0.15, 0.5, LISTEN()), toonDur=0.0),   # (stills 3) ears in radians (2.2 turned it back into his head)
            *[k(r(0.12 + 0.16 * i), toon=EAR(r(0.18 + 0.07 * i), 1.15, LISTEN()), toonDur=0.05, toonEase='out') for i in range(3)],   # the ear flaps out...
            *[k(r(0.2 + 0.16 * i), toon=EAR(r(0.2 + 0.07 * i), 0.55, LISTEN()), toonDur=0.06, toonEase='inOut') for i in range(3)],   # ...and back, three times, leaning in...
            k(0.62, toon=EAR(0.4, 1.05, LISTEN(brow=0.8)), toonDur=0.12, toonEase='out'),   # ...listening hard...
            k(0.9, toon=EAR(0.42, 1.1, LISTEN(brow=0.8, gx=-0.6)), toonDur=0.15, toonEase='inOut'),
            k(1.05, toon=EAR(0.38, 1.0, {'lid': 1.0, 'brow': 0.4}), toonDur=0.05),   # ...nothing: a blink...
            k(1.12, toon=EAR(0.15, 0.0, {'lid': 0.45, 'gx': 0.2}, cup=False), toonDur=0.22, toonEase='inOut')])],   # ...the ear folds back, the hand drops, deadpan
        props=[*HIGH('2'), PEAK('2'), SUMMIT('2'), *VALLEY('2')],
        cams=[FC(0.0, [-1.5, r(TOP + 1.25), -0.9], [[ME_S[0], r(TOP + 2.45), ME_S[2]], [ME_S[0], r(TOP + 1.3), ME_S[2]], [-0.38, r(TOP + 2.05), 0.25], [0.3, r(TOP + 2.0), ME_S[2]]], top=0.16, bottom=0.62, drift=(0.05, 0.0, 0.05))])   # (pass 2) low on the near side: the cupped ear against the sky
st.cue('sfx:crickets', 'S02', 0.6, 0.2)

# 3: he filed a complaint. A two-shot over the desk, GENDARMERIE on the wall: he mimes his shout (hands round his mouth, jaw down), three-quarters to
#    us; the gendarme looks up from his form at the silent shout, his brows up, then writes it down
D3 = st.dur('S03')
GEND = {'title': 'GENDARMERIE', 'plate': 'PLAINTES', 'map': False, 'bannerY': 2.75, 'bannerX': 0.75}   # (pass 2) the banner lower, over the gendarme: in the shot
VIS = [1.1, 0, -0.8]; GDM = [0.25, 0, -1.45]                              # (stills 3) at a right angle, him at the end of the desk: both faces three-quarters to the camera
WRITE3 = lambda dx=0.0, bend=0.25, face=None: {'reach': {'R': [r(GDM[0] - 0.05 + dx), 0.86, r(GDM[2] + 0.5), 1, 0.05]}, 'hands': {'R': 'pinch'}, 'bend': {'spine': [bend, 0, 0, 1, None]}, 'face': face or {'lid': 0.55, 'gy': 0.6}}
st.shot('S03', 'mairie', setOpts=GEND, actors=[
        act('mec', VIS, -100, 'stand', 'unimpressed', keys=[k(0.0, look={'point': [GDM[0], 1.85, GDM[2]], 'cheat': 0.4}), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.12, toon={**CUP(0.5), 'sq': [1.04, 1.02, 1.08], 'bend': {'spine': [-0.15, 0, 0, 1, None]}, 'face': {'lid': 0.5, 'puff': 0.8, 'cheeks': 0.8}}, toonDur=0.18, toonEase='inOut'),   # the mime: a breath...
            k(0.4, toon={**CUP(1.0), 'bend': {'spine': [0.18, 0, 0, 1, None]}, 'face': {'lid': 1.0, 'jaw': 0.8, 'jawLen': 0.6, 'mouth': 'scream', 'brow': -0.6}}, toonDur=0.06, toonEase='out'),   # ...the silent shout...
            k(0.85, toon={'face': {'lid': 0.45, 'mouth': 'o', 'gx': 0.4}}, toonDur=0.15)]),   # ...and back, deadpan
        act('gendarme', GDM, 10, 'stand', 'neutral', keys=[k(0.0, look=[GDM[0], 0.85, r(GDM[2] + 0.45)]), k(0.0, toon=WRITE3(), toonDur=0.0),   # (stills 2) three-quarters to the camera
            *[k(r(0.08 + 0.1 * i), toon=WRITE3(0.06 if i % 2 else -0.04), toonDur=0.08) for i in range(3)],   # writing...
            k(0.38, look={'point': [VIS[0], 1.85, VIS[2]], 'cheat': 0.4}), k(0.42, toon=WRITE3(0.0, 0.05, {'lid': 0.1, 'eye': 0.3, 'brow': 0.9, 'mouth': 'o', 'gx': -0.3}), toonDur=0.07, toonEase='out'),   # (pass 2) ...he looks up at the silent shout, his brows up...
            k(0.82, look=[GDM[0], 0.85, r(GDM[2] + 0.45)]), k(0.84, toon=WRITE3(0.03), toonDur=0.12)])],   # ...and writes it down
        props=[P('form3', 'paperSheet', pos=[r(GDM[0] - 0.05), 0.832, r(GDM[2] + 0.48)], rot=[round(-PI / 2, 4), 0, 0.2], opts={'w': 0.3, 'h': 0.4, 'head': 'PLAINTE'})],
        cams=[FC(0.0, [-0.5, 1.65, 1.5], [[r(VIS[0] + 0.32), 2.4, VIS[2]], [VIS[0], 1.2, VIS[2]], [r(GDM[0] - 0.38), 2.35, GDM[2]], [GDM[0], 0.85, r(GDM[2] + 0.5)], [0.75, 3.0, -2.57]], top=0.1, bottom=0.74, drift=(0.06, 0.0, -0.05))])   # (stills 4) both whole (he was cut by the edge)   # (stills 2) in front of him on the side: from behind we saw the back of his head   # (pass 2) both faces and the sign in one frame (they stood at opposite edges)
st.cue('sfx:paper', 'S03', 0.1, 0.15)

# 4: the gendarmerie put out a missing notice. The gendarme, facing us right of the board, looks at it, cocks his arm high and SLAPS the notice on
#    the board by its edge (the bubble « OHÉ ! » clear of his arm), PAF where his hand lands; a beat, then a look to us, pleased
D4 = st.dur('S04'); SLAP4 = 0.4
BOARD = [1.2, 1.55, -2.55]                                                 # on the back wall
GD4 = [1.95, 0, -2.05]                                                     # (pass 2) right of the notice, facing us: his right hand slaps its edge
HIT4 = [1.47, 1.55, -2.49]                                                 # the notice's right margin, beside the bubble
GR4 = lambda p_, hand='open': {'reach': {'R': [p_[0], p_[1], p_[2], 1, 0.05]}, 'hands': {'R': hand}}
st.shot('S04', 'mairie', setOpts=GEND, actors=[
        act('gendarme', GD4, -20, 'stand', 'determined', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.45, 'brow': -0.3}}, toonDur=0.0),
            k(0.04, toon={'face': {'lid': 0.45, 'brow': -0.4, 'gx': -0.8}}, toonDur=0.04), k(0.08, look=[BOARD[0], BOARD[1], BOARD[2]]),   # his eyes to the board, then his head...
            k(0.1, toon={**GR4([r(GD4[0] - 0.25), 2.3, r(GD4[2] + 0.25)]), 'bend': {'spine': [-0.16, 0, 0, 1, None]}, 'sq': [0.96, 1.05, 0.96], 'face': {'lid': 0.6, 'brow': -0.7, 'mouth': 'clench'}}, toonDur=0.16, toonEase='inOut'),   # ...his arm cocked high...
            k(r(SLAP4 - 0.06), toon={**GR4(HIT4), 'bend': {'spine': [0.14, 0, 0, 1, None]}, 'sq': [1.04, 0.96, 1.04], 'face': {'lid': 0.5, 'brow': -0.9, 'mouth': 'clench'}}, toonDur=0.06, toonEase='in'),   # ...SLAP
            k(r(SLAP4 + 0.16), toon={**GR4([HIT4[0], r(HIT4[1] - 0.02), HIT4[2]]), 'face': {'lid': 0.5, 'brow': -0.4}}, toonDur=0.1),   # ...a beat, his palm on it...
            k(r(SLAP4 + 0.3), toon={'reach': {'R': [r(GD4[0] - 0.1), 1.05, r(GD4[2] + 0.25), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.4, 'brow': 0.3, 'mouth': 'smirk'}}, toonDur=0.2, toonEase='inOut'),   # ...a step back, pleased...
            k(r(SLAP4 + 0.3), look='camera')])],   # ...to us
        props=[P('poster4', 'missingPoster', pos=BOARD, opts={'w': 0.62, 'h': 0.86}, keys=[k(0.0, scale=0.001, dur=0.0), k(SLAP4, scale=1.0, dur=0.12, ease='outBack')]),
               BURST('slap4', [r(HIT4[0] + 0.2), r(HIT4[1] + 0.08), r(HIT4[2] + 0.12)], SLAP4, 'PAF !', 0.34)],   # (pass 2) where his hand lands (by his head he seemed the one hit)
        cams=[FC(0.0, [0.4, 1.6, 0.6], [[GD4[0], 2.35, GD4[2]], [GD4[0], 0.9, GD4[2]], [r(GD4[0] + 0.35), 2.0, GD4[2]], [r(BOARD[0] - 0.35), r(BOARD[1] + 0.48), BOARD[2]], [r(BOARD[0] + 0.35), r(BOARD[1] - 0.48), BOARD[2]]], top=0.12, bottom=0.72, drift=(0.06, 0.0, -0.08))])
st.cue('sfx:punch', 'S04', SLAP4, 0.4)

# 5: ...a missing notice. In town the notices are on every lamp post; a passer-by walks toward us past one, glances, walks on, stops dead: a double
#    take, his head snapping round to it, eyes popping, hat lifting, and he leans over to read it (pass 2, stills 4: the notice beside his path facing
#    us, so his face turns three-quarters to us when he looks at it; facing it, we saw his back or he looked at us)
D5 = st.dur('S05')
STREET = {'eiffelStyle': 'v2', 'clear': [-4.0, 4.0]}
PST = [6.25, 0, 1.3]; PST1 = [6.25, 0, -0.45]
NOTE5 = [6.95, 1.55, -0.6]
POSTERS = [[NOTE5[0], NOTE5[1], NOTE5[2], 180], [6.95, 1.6, 4.4, 180], [-6.95, 1.5, 2.6, 180], [6.95, 1.5, 9.4, 180], [-6.95, 1.55, 7.8, 180]]
st.shot('S05', 'parisStreet', setOpts=STREET, actors=[
        act('passant', PST, 180, 'stand', 'neutral', keys=[k(0.0, look=None), k(0.0, to=PST1, dur=0.4, clip='walk', then='stand', ease='out', face='keep'), k(0.0, toon={'face': {'lid': 0.3}}, toonDur=0.0),
            k(0.12, look=NOTE5), k(0.12, toon={'face': {'lid': 0.3, 'gx': 0.7}}, toonDur=0.05), k(0.24, look=[PST1[0], 1.7, -6.0]), k(0.24, toon={'face': {'lid': 0.3, 'gx': 0.0}}, toonDur=0.05),   # a glance, on he walks...
            k(0.4, toon={'sq': [1.06, 0.93, 1.06], 'face': {'lid': 0.5}}, toonDur=0.04, toonEase='in'),   # ...he stops dead...
            k(0.45, look=NOTE5), k(0.45, toon={'sq': [0.94, 1.08, 0.94], 'hat': [0.16, 0.12, 0.0], 'face': {'lid': 0.0, 'eye': 0.7, 'pupilSize': -0.3, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.05, toonEase='out'),   # ...the double take: his head snaps round, eyes popping, hat up ('hat' is [lift m, tilt, spin])...
            k(0.56, toon={'bend': {'spine': [0.12, 0, -0.3, 1, None], 'neck': [0.1, 0, -0.15, 1, None]}, 'hat': [0.06, 0.05, 0.0], 'face': {'lid': 0.0, 'eye': 0.5, 'pupilSize': -0.2, 'brow': 0.9, 'mouth': 'O'}}, toonDur=0.12, toonEase='out'),   # ...he leans over to read it
            k(0.8, toon={'bend': {'spine': [0.14, 0, -0.32, 1, None], 'neck': [0.12, 0, -0.16, 1, None]}, 'face': {'lid': 0.1, 'eye': 0.45, 'brow': 0.9, 'mouth': 'o'}}, toonDur=0.15)])],
        props=[*[P(f'pole5{i}', 'streetLamp', pos=[x_, 0, r(z_ + 0.12)]) for i, (x_, y_, z_, ry_) in enumerate(POSTERS)],
               *[P(f'post5{i}', 'missingPoster', pos=[x_, y_, z_], ry=ry_, opts={'w': 0.42, 'h': 0.58}) for i, (x_, y_, z_, ry_) in enumerate(POSTERS)]],
        cams=[FC(0.0, [6.05, 1.7, -3.3], [[PST1[0], 2.35, PST1[2]], [PST1[0], 0.9, PST1[2]], [NOTE5[0], 1.9, NOTE5[2]], [NOTE5[0], 1.2, NOTE5[2]], [r(PST1[0] - 0.4), 1.9, PST1[2]]], top=0.14, bottom=0.72, drift=(0.0, 0.0, -0.08))])   # in front of him: his face and the notice facing us; more notices down the street
st.cue('sfx:boing', 'S05', 0.45, 0.2)

# 6: it was reported... In a valley between two slopes a hiker (pack, pole, beanie), low against the sky: the letters « OHÉ ! » skim over him from
#    left to right; he points up and follows them with his arm and his eyes, wide, his pupils shrinking
D6 = st.dur('S06')
HIK = [0.0, 0, 0.0]
OHE6 = [[0.0, -3.6, 4.0, -1.0], [D6, 3.2, 4.3, -1.2]]
def at6(t): u = t / D6; return [r(OHE6[0][1] + (OHE6[1][1] - OHE6[0][1]) * u), r(OHE6[0][2] + (OHE6[1][2] - OHE6[0][2]) * u), r(OHE6[0][3] + (OHE6[1][3] - OHE6[0][3]) * u)]
PT6 = lambda t: {'reach': {'R': [r(0.22 * at6(t)[0] / 4.0), 2.65, -0.2, 1, 0.08]}, 'hands': {'R': 'point'}}   # his finger up, following the word
W6 = {'lid': 0.0, 'eye': 0.7, 'pupilSize': -0.4, 'brow': 1.0, 'mouth': 'O'}
st.shot('S06', 'grassland', setOpts=ALPS, actors=[
        act('rando', HIK, 15, 'stand', 'neutral', keys=[k(0.0, look=at6(0.0)), k(0.0, toon={**PT6(0.0), 'face': {'lid': 0.3, 'brow': 0.4}}, toonDur=0.0),
            k(0.06, toon={**PT6(0.06), 'sq': [0.95, 1.06, 0.95], 'face': W6}, toonDur=0.06, toonEase='outBack'),   # his eyes pop, his finger up...
            *[k(r(0.2 + 0.2 * i), look=at6(r(0.2 + 0.2 * i))) for i in range(3)],
            *[k(r(0.2 + 0.2 * i), toon={**PT6(r(0.3 + 0.2 * i)), 'sq': [0.98, 1.02, 0.98], 'face': {**W6, 'pupilSize': r(-0.4 - 0.1 * i)}}, toonDur=0.2) for i in range(3)]])],   # ...following it across the sky
        props=[*RING('6'), P('slopeL6', 'mountainRange', pos=[-56, 0, -24], ry=90, opts={'n': 3, 'w': 60, 'h': 28, 'd': 10, 'seed': 41, 'colors': ['#7FA35E', '#6E9150', '#F4F6F8']}), P('slopeR6', 'mountainRange', pos=[58, 0, -28], ry=-90, opts={'n': 3, 'w': 60, 'h': 30, 'd': 10, 'seed': 43, 'colors': ['#7FA35E', '#6E9150', '#F4F6F8']}),   # (check) 46 m out: at 30 their 33 m cones swallowed the camera
               P('pack6', 'backpack', on={'actor': 'rando', 'joint': 'torso', 'offset': [0, 0.42, -0.24]}), P('pole6', 'trekPole', on={'actor': 'rando', 'hand': 'L'}),
               P('ohe6', 'shoutLetters', **FLY(OHE6), face='camera', opts={'text': 'OHÉ !', 'size': 0.45, 'grow': [[0.0, 2.4]]})],   # (pass 2) over him in clear sky, left to right like the way out
        cams=[FC(0.0, [0.7, 0.75, 3.2], [[HIK[0], 2.3, HIK[2]], [HIK[0], 0.2, HIK[2]], [-1.4, 4.45, -1.0], [1.4, 4.6, -1.2]], top=0.08, bottom=0.82)])   # (pass 2) low: the word skims over his head (level: backed along the line it went under the ground)
st.cue('sfx:boing', 'S06', 0.08, 0.2); st.cue('whoosh', 'S06', 0.0, 0.25, 0.8, 300, 1200)

# 7: ...in three valleys. A farm field on the other side (a cow, the farmer with his pitchfork): the letters come over low and big, skimming his head:
#    his cap springs off and hangs in the air, his jaw drops to his chest
D7 = st.dur('S07')
FARM = [0.0, 0, 0.0]; PASS7 = 0.36
OHE7 = [[0.0, -4.6, 3.7, -0.7], [PASS7, -0.3, 2.95, -0.35], [D7, 4.2, 3.4, -0.6]]
st.shot('S07', 'grassland', setOpts={**ALPS, 'grass': '#9CC46E'}, actors=[
        act('fermier', FARM, -30, 'stand', 'neutral', keys=[k(0.0, look={'point': OHE7[0][1:], 'cheat': 0.4}), k(0.0, toon={'face': {'lid': 0.4}}, toonDur=0.0),
            k(0.18, look={'point': OHE7[1][1:], 'cheat': 0.4}), k(0.5, look={'point': OHE7[2][1:], 'cheat': 0.4}),
            k(r(PASS7 - 0.06), toon={'sq': [1.05, 0.94, 1.05], 'face': {'lid': 0.2, 'brow': 0.6, 'mouth': 'o'}}, toonDur=0.05, toonEase='in'),   # a duck...
            k(PASS7, toon={'sq': [0.95, 1.07, 0.95], 'bend': {'spine': [-0.2, 0, 0, 1, None]}, 'hat': [0.55, 0.6, 2.5], 'face': {'lid': 0.0, 'eye': 0.5, 'brow': 1.0, 'jaw': 1.0, 'jawLen': 0.8, 'mouth': 'O'}}, toonDur=0.08, toonEase='out'),   # ...the word skims his head: his cap springs off, his jaw drops to his chest...
            k(r(PASS7 + 0.16), toon={'sq': [0.97, 1.04, 0.97], 'bend': {'spine': [-0.16, 0, 0, 1, None]}, 'hat': [0.9, 0.9, 4.5], 'face': {'lid': 0.0, 'eye': 0.5, 'brow': 1.0, 'jaw': 1.0, 'jawLen': 0.8, 'mouth': 'O'}}, toonDur=0.14, toonEase='out'),   # ...the cap hanging up there...
            k(r(PASS7 + 0.32), toon={'sq': [0.98, 1.02, 0.98], 'bend': {'spine': [-0.14, 0, 0, 1, None]}, 'hat': [0.98, 1.0, 5.2], 'face': {'lid': 0.0, 'eye': 0.45, 'brow': 1.0, 'jaw': 1.0, 'jawLen': 0.8, 'mouth': 'O'}}, toonDur=0.14, toonEase='inOut')]),
        act('vache', [-1.5, 0, -2.0], 75, 'idle')],   # (stills 2) beside him, side on (behind him it was hidden)
        props=[*RING('7'), P('fork7', 'pitchfork', on={'actor': 'fermier', 'hand': 'L'}, rot=[round(PI, 4), 0, 0]),   # (stills 2) the tines up (they hung down: a walking stick) P('fence7', 'fence', pos=[-1.6, 0, -3.6], ry=10, opts={'length': 5, 'color': '#C9B48A'}),
               P('ohe7', 'shoutLetters', **FLY(OHE7), face='camera', opts={'text': 'OHÉ !', 'size': 0.6, 'grow': [[0.0, 1.6]], 'wobble': 0.25})],   # (pass 2) low and big this time, left to right
        cams=[FC(0.0, [-2.4, 1.55, 2.6], [[FARM[0], 2.3, FARM[2]], [FARM[0], 0.0, FARM[2]], [-2.2, 1.4, -2.0], [-0.3, 3.4, -0.35], [0.5, 3.9, 0.0]], top=0.1, bottom=0.8, drift=(0.08, 0.0, 0.0))])   # (pass 2) from the other side, at his height: a different valley from the hiker's
st.cue('whoosh', 'S07', 0.15, 0.4, 0.7, 200, 1000); st.cue('sfx:gasp', 'S07', PASS7, 0.2)

# 8: yesterday the echo came home. His street: he walks out on the pavement; down the open road the letters come back, growing huge as they come; he
#    turns (eyes first); cut in profile: a squash and a blink, then his eyes shoot out on stalks two head lengths, his hair on end, recoiling, held
#    vibrating
D8 = st.dur('S08'); TURN8 = 0.7
ME = [7.2, 0, 0.0]
STREET8 = {**STREET, 'clear': [-16.0, 6.0]}                               # (pass 2) no tree and no lamp between the lens and the word (a tree hid it, a lamp grew out of his head)
st.shot('S08', 'parisStreet', setOpts=STREET8, actors=[
        act('mec', [7.2, 0, 1.2], 180, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={'face': DEAD}, toonDur=0.0),
            k(0.0, to=ME, dur=0.55, clip='walk', then='stand', ease='out', face='keep'),
            k(r(TURN8 - 0.12), toon={'face': {'lid': 0.3, 'gx': -0.8, 'gy': -0.2}}, toonDur=0.06), k(TURN8, look=[0.0, 2.2, -20.0]),   # his eyes first, then his head (level: looking up, the stalks left the frame)...
            k(r(TURN8 + 0.22), toon={'sq': [1.08, 0.9, 1.08], 'face': {'lid': 1.0, 'brow': -0.6, 'mouth': 'clench'}}, toonDur=0.06, toonEase='in'),   # (pass 2) ...a squash and a blink, four frames...
            k(r(TURN8 + 0.36), toon={'sq': [0.9, 1.14, 0.9], 'bend': {'spine': [-0.3, 0, 0, 1, None], 'neck': [-0.15, 0, 0, 1, None]}, 'hairUp': 1.0, 'face': {'lid': 0.0, 'pop': 1.0, 'popLen': 0.6, 'brow': 1.0, 'mouth': 'O'}}, toonDur=0.05, toonEase='out'),   # ...TAKE: eyes out on long stalks, hair on end, recoiling...
            *[k(r(TURN8 + 0.46 + 0.05 * i), toon={'sq': ([0.95, 1.06, 0.95] if i % 2 else [0.97, 1.03, 0.97]), 'bend': {'spine': [-0.24, 0, 0, 1, None]}, 'hairUp': 1.0,
                                                   'face': {'lid': 0.0, 'pop': 1.0, 'popLen': (0.62 if i % 2 else 0.54), 'brow': 1.0, 'mouth': 'O', 'tremble': 1.0}}, toonDur=0.04) for i in range(11)]])],   # ...held, vibrating
        props=[P('ohe8', 'shoutLetters', **FLY([[0.0, 1.6, 4.6, -70.0], [0.5, 2.0, 4.0, -32.0], [r(TURN8 + 0.2), 3.0, 3.4, -14.0], [D8, 4.6, 2.6, -3.0]]), face='camera', opts={'text': 'OHÉÉÉ !', 'size': 0.6, 'grow': [[0.0, 1.0], [0.5, 1.4], [D8, 3.6]], 'wobble': 0.3}),   # (pass 2) down the middle of the road
               P('spd8', 'speedLines', **FLY([[0.0, 1.6, 4.6, -68.0], [0.5, 2.0, 4.1, -30.0], [r(TURN8 + 0.2), 3.0, 3.5, -12.0]]), face='camera', opts={'n': 8, 'len': 2.2, 'w': 1.6, 'angle': 1.45, 'at': [[0.0, r(TURN8 + 0.2)]]})],
        cams=[FC(0.0, [8.4, 2.3, 4.0], [[ME[0], 2.35, ME[2]], [ME[0], 1.0, ME[2]], [2.0, 4.0, -32.0], [3.0, 3.4, -14.0]], top=0.1, bottom=0.78, drift=(0.0, 0.0, 0.1)),   # over his shoulder: the word coming down the open road beside his head...
              FC(r(TURN8 + 0.2), [5.8, 1.95, -0.7], [[ME[0], 2.45, ME[2]], [ME[0], 1.3, ME[2]], [r(ME[0] - 0.32), 2.3, -0.75], [r(ME[0] + 0.7), 2.2, r(ME[2] + 0.7)]], top=0.16, bottom=0.64)])   # (stills 3, 4) room on his side: his face sat on the edge   # (pass 2) ...in profile: the stalks stretch out (head-on they foreshortened to discs)
st.cue('whoosh', 'S08', 0.4, 0.4, 1.3, 150, 700); st.cue('sfx:boing', 'S08', r(TURN8 + 0.36), 0.3)

# 9: two years late. SPLAT: the giant letters hit him and he is flattened on the pavement like a sheet of paper, spread wide, face up (the letters bounce
#    off); stars; he swings up stiff as a board, seen edge-on, past upright, wobbling, hanging there; POP: back to his shape, past it, settling, his hair
#    on end
D9 = st.dur('S09'); HIT9 = 0.08; UP9 = 0.43; HANG9 = 0.67; POP9 = 0.85
LIFT9 = [ME[0], 0.04, ME[2]]
FLATK = lambda sq, face: {'lay': [round(-PI / 2, 4), 0.0], 'sq': sq, 'hairUp': 1.0, 'face': face}
st.shot('S09', 'parisStreet', setOpts=STREET8, actors=[
        act('mec', ME, 180, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon={'face': {'lid': 0.0, 'pop': 1.0, 'popLen': 0.5, 'brow': 1.0, 'mouth': 'O'}, 'hairUp': 1.0}, toonDur=0.0),
            k(r(HIT9 - 0.02), to=LIFT9, dur=0.04, ease='out', face='keep'),   # (pass 2) lifted 4 cm: flat at 0 he sank into the pavement (only his tie and his legs showed)
            k(HIT9, toon=FLATK([1.4, 1.1, 0.04], {'lid': 0.0, 'brow': 1.0, 'mouth': 'O'}), toonDur=0.05, toonEase='out'),   # SPLAT: flat on his back, spread wide...
            k(r(HIT9 + 0.12), toon=FLATK([1.35, 1.08, 0.04], {'lid': 0.3, 'brow': 0.4, 'stars': 1.0, 'starsScale': 1.6}), toonDur=0.1),   # ...held, stars...
            k(r(UP9 - 0.04), to=ME, dur=0.22, ease='inOut', face='keep'),
            k(UP9, toon={'lay': [0.12, 0.0], 'sq': [1.25, 1.12, 0.04], 'hairUp': 1.0, 'face': {'lid': 0.45, 'stars': 1.0, 'starsScale': 1.6}}, toonDur=0.24, toonEase='inOut'),   # ...he swings up stiff as a board, edge-on, past upright...
            k(HANG9, toon={'lay': [-0.05, 0.0], 'sq': [1.25, 1.12, 0.04], 'hairUp': 1.0, 'face': {'lid': 0.45, 'stars': 1.0, 'starsScale': 1.6}}, toonDur=0.08),   # ...wobbling...
            k(r(HANG9 + 0.08), toon={'lay': [0.0, 0.0], 'sq': [1.25, 1.12, 0.04], 'hairUp': 1.0, 'face': {'lid': 0.45, 'stars': 1.0}}, toonDur=0.06),   # ...hanging there a moment...
            k(POP9, toon={'sq': [0.84, 1.18, 1.4], 'yaw': 1.3, 'hairUp': 1.0, 'face': {'lid': 0.1, 'brow': 0.8, 'mouth': 'O'}}, toonDur=0.06, toonEase='outBack'),   # ...POP: inflated past his shape, turning to us (in profile his box head has no face)...
            k(r(POP9 + 0.12), toon={'sq': [1.06, 0.95, 0.96], 'yaw': 1.3, 'hairUp': 0.9, 'face': DEAD}, toonDur=0.1), k(r(POP9 + 0.24), toon={'sq': [0.98, 1.02, 1.0], 'yaw': 1.3, 'hairUp': 0.85, 'face': DEAD}, toonDur=0.12),
            k(r(POP9 + 0.4), toon={'yaw': 1.3, 'hairUp': 0.85, 'face': DEAD}, toonDur=0.15)])],   # ...settling, deadpan, his hair on end
        props=[P('ohe9', 'shoutLetters', **FLY([[0.0, r(ME[0] - 0.9), 1.7, -2.0], [HIT9, r(ME[0] - 0.15), 1.1, -0.35], [r(HIT9 + 0.12), r(ME[0] - 1.7), 2.7, -1.0], [r(HIT9 + 0.4), r(ME[0] - 3.6), 4.2, -2.6], [D9, r(ME[0] - 7.0), 5.5, -8.0]]), face='camera', opts={'text': 'OHÉÉÉ !', 'size': 0.6,
                 'grow': [[0.0, 2.0], [D9, 1.8]], 'squash': [[0.0, 1.0, 1.0], [HIT9, 1.35, 0.6], [r(HIT9 + 0.1), 0.9, 1.15], [r(HIT9 + 0.2), 1.0, 1.0]], 'wobble': 0.35}),   # the letters squash on him and bounce off
               BURST('splat9', [r(ME[0] - 0.45), 1.35, 0.9], HIT9, 'SPLAT !', 0.5)],   # (pass 2) above the pancake, clear of the captions
        fx=[{'type': 'shake', 'at': HIT9, 'dur': 0.2, 'amount': 0.016}],
        cams=[FC(0.0, [r(ME[0] - 2.2), 3.9, 0.85], [[ME[0], 0.0, r(ME[2] - 0.55)], [ME[0], 0.0, r(ME[2] + 2.0)], [ME[0], 2.45, r(ME[2] - 0.35)], [r(ME[0] - 0.45), 1.5, 0.9]], top=0.12, bottom=0.74)])   # (stills 2) higher: his face on the pancake (grazing it showed a strip); room left of him for the board   # (pass 2) from his side and high: the whole pancake face up, then the board edge-on
st.cue('sfx:splat', 'S09', HIT9, 0.5); st.cue('sfx:stretch', 'S09', UP9, 0.25); st.cue('sfx:pop', 'S09', POP9, 0.4)

# 10: it shouted... Night, the street dark under its lamps: the giant letters rattle between the buildings; a woman and a little boy under a lamp hold
#     their ears, shaking with every rattle, hair on end
D10 = st.dur('S10')
NIGHT = {**STREET, 'night': True}
NLOOK = {'sun': 0.3, 'sunColor': '#9DB4EC', 'fill': 0.75, 'exposure': 0.9}   # (pass 2) the natural look lights a night set like day (road 92 at night vs 89 by day)
VOI = [3.3, 0, 0.6]; GAM = [2.3, 0, 1.15]
HOLD10 = lambda s_, face: {'touch': {'L': ['face', 0.58, 0.55, -0.06, 1, 0.02], 'R': ['face', -0.58, 0.55, -0.06, 1, 0.02]}, 'hands': {'L': 'open', 'R': 'open'}, 'hairUp': 1.0, 'sq': s_, 'face': face}
st.shot('S10', 'parisStreet', setOpts=NIGHT, look=NLOOK, actors=[
        act('voisine', VOI, -10, 'stand', 'scared', keys=[k(0.0, look='camera'), *[k(r(0.06 * i), toon=HOLD10([0.94, 1.06, 0.94] if i % 2 else [1.05, 0.95, 1.05], {'lid': 1.0, 'brow': -0.8, 'mouth': 'clench', 'tremble': 1.0}), toonDur=0.05) for i in range(12)]]),   # (pass 2) shaking with each rattle
        act('gamin', GAM, 10, 'stand', 'scared', keys=[k(0.0, look='camera'), *[k(r(0.03 + 0.06 * i), toon=HOLD10([1.06, 0.94, 1.06] if i % 2 else [0.94, 1.06, 0.94], {'lid': 0.0, 'eye': 0.6, 'pupilShake': 1.0, 'brow': 1.0, 'mouth': 'scream'}), toonDur=0.05) for i in range(12)]])],
        props=[P('ohe10', 'shoutLetters', **FLY([[0.0, -1.0, 5.5, -7.0], [0.25, 6.0, 4.0, -6.5], [0.5, -0.5, 6.0, -7.5], [D10, 5.5, 4.8, -6.5]]), face='camera', opts={'text': 'OHÉÉÉ !', 'size': 0.6, 'grow': [[0.0, 3.2]], 'wobble': 0.45}),
               P('lamp10', 'streetLamp', pos=[5.4, 0, 0.3], ry=180, opts={'on': True, 'light': 5, 'pool': 1.8}), P('lamp10b', 'streetLamp', pos=[-5.4, 0, -6.0], opts={'on': True, 'light': 4, 'pool': 1.6})],
        cams=[FC(0.0, [2.6, 1.2, 4.9], [[VOI[0], 2.2, VOI[2]], [GAM[0], 1.5, GAM[2]], [VOI[0], 0.0, VOI[2]], [-1.0, 7.2, -7.0], [6.0, 7.2, -7.0]], top=0.08, bottom=0.8, drift=(0.0, 0.0, -0.1), level=False)])
st.cue('sfx:whistle', 'S10', 0.05, 0.2); st.cue('whoosh', 'S10', 0.0, 0.3, 0.7, 300, 1100)

# 11: ...for three days. By day: he stands in his street with rings under his eyes, his hair wild, his hands over his ears; the letters still shouting
#     over the roofs behind him
D11 = st.dur('S11')
EARS = lambda face, sq=None: {'touch': {'L': ['face', 0.58, 0.55, -0.06, 1, 0.02], 'R': ['face', -0.58, 0.55, -0.06, 1, 0.02]},   # (stills 1) on his ears ('head' takes metres)
                               'hands': {'L': 'open', 'R': 'open'}, 'hairUp': 0.9, **({'sq': sq} if sq else {}), 'face': face}
TIRED = {'lid': 0.6, 'shadow': 1.0, 'brow': -0.3, 'mouth': 'wavy'}
st.shot('S11', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, -50, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=EARS(TIRED), toonDur=0.0),
            *[k(r(0.1 + 0.1 * i), toon=EARS({**TIRED, 'tremble': 1.0}, [0.98, 1.02, 0.98] if i % 2 else [1.01, 0.99, 1.01]), toonDur=0.08) for i in range(6)],   # jolted by the noise
            k(0.8, toon=EARS({**TIRED, 'lid': 1.0}), toonDur=0.08), k(0.95, toon=EARS(TIRED), toonDur=0.12)])],   # a long blink
        props=[P('ohe11', 'shoutLetters', **FLY([[0.0, 8.5, 4.2, -2.0], [0.4, 9.0, 3.7, -3.0], [0.8, 8.4, 4.5, -2.4], [D11, 9.0, 3.9, -2.8]]), face='camera', opts={'text': 'OHÉÉÉ !', 'size': 0.6, 'grow': [[0.0, 2.6]], 'wobble': 0.45})],
        cams=[FC(0.0, [5.6, 1.6, 1.6], [[ME[0], 2.45, ME[2]], [ME[0], 1.1, ME[2]], [r(ME[0] - 0.45), 1.7, ME[2]], [r(ME[0] + 0.45), 1.7, ME[2]]], top=0.3, bottom=0.68)])   # (stills 1) him, the letters over the roofs above (with them in the fit the camera tipped into the sky)
st.cue('sfx:whistle', 'S11', 0.1, 0.15)

# 12: the gendarmerie fined the man... The gendarme writes the ticket (his face to us), looks up, cocks his arm high and back, and SLAPS it on the man's
#     forehead, PAF where it lands: the man's head knocked back thirty degrees, past it and back, deadpan
D12 = st.dur('S12'); STICK12 = 0.7
GD12 = [r(ME[0] - 0.85), 0, r(ME[2] + 0.35)]
FORE = [r(ME[0] - 0.2), 2.3, ME[2]]                                        # his forehead
FINE_AT = [0.0, 0.55, 0.19]                                                # (pass 2) above his eyes (on 0.42 it covered one)
WR12 = lambda i: {'reach': {'R': [r(GD12[0] + 0.2 + (0.04 if i % 2 else -0.03)), 1.15, r(GD12[2] + 0.25), 1, 0.05], 'L': [r(GD12[0] + 0.18), 1.1, r(GD12[2] + 0.12), 1, 0.05]}, 'hands': {'R': 'pinch', 'L': 'open'}, 'face': {'lid': 0.55, 'gy': 0.6}}
st.shot('S12', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, -90, 'stand', 'unimpressed', keys=[k(0.0, look=[GD12[0], 1.7, GD12[2]]), k(0.0, toon={'hairUp': 0.8, 'face': TIRED}, toonDur=0.0),
            k(STICK12, toon={'bend': {'neck': [-0.55, 0, 0, 1, None], 'spine': [-0.12, 0, 0, 1, None]}, 'sq': [1.04, 0.96, 1.04], 'hairUp': 0.9, 'face': {**TIRED, 'lid': 1.0}}, toonDur=0.04, toonEase='out'),   # (pass 2) the slap knocks his head back thirty degrees...
            k(r(STICK12 + 0.1), toon={'bend': {'neck': [0.14, 0, 0, 1, None]}, 'hairUp': 0.8, 'face': {**TIRED, 'lid': 0.7}}, toonDur=0.1, toonEase='inOut'),   # ...past it...
            k(r(STICK12 + 0.24), toon={'hairUp': 0.8, 'face': TIRED}, toonDur=0.14, toonEase='inOut')]),   # ...and back, deadpan
        act('gendarme', GD12, 100, 'stand', 'neutral', keys=[k(0.0, look={'point': [GD12[0], 1.1, r(GD12[2] + 0.3)], 'cheat': 0.5}),   # (pass 2) writing, his face cheated to us (he was in profile)
            *[k(r(0.05 + 0.1 * i), toon=WR12(i), toonDur=0.08) for i in range(4)],   # writing on his pad...
            k(0.44, look=[ME[0], 1.95, ME[2]]), k(0.46, toon={'reach': {'R': [r(GD12[0] - 0.12), 2.3, r(GD12[2] + 0.3), 1, 0.05]}, 'hands': {'R': 'open'}, 'bend': {'spine': [-0.15, 0, 0, 1, None]}, 'sq': [0.97, 1.04, 0.97], 'face': {'lid': 0.4, 'brow': -0.5, 'mouth': 'clench'}}, toonDur=0.12, toonEase='inOut'),   # ...his arm cocked high and back, held...
            k(r(STICK12 - 0.04), toon={'reach': {'R': [FORE[0], FORE[1], FORE[2], 1, 0.03]}, 'hands': {'R': 'open'}, 'bend': {'spine': [0.12, 0, 0, 1, None]}, 'sq': [1.03, 0.97, 1.03], 'face': {'lid': 0.4, 'brow': -0.7, 'mouth': 'clench'}}, toonDur=0.04, toonEase='in'),   # ...SLAP on his forehead...
            k(r(STICK12 + 0.08), toon={'reach': {'R': [r(FORE[0] + 0.08), r(FORE[1] - 0.12), r(FORE[2] - 0.12), 1, 0.03]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.4, 'brow': -0.4}}, toonDur=0.08),   # ...following through...
            k(r(STICK12 + 0.25), toon={'reach': {'R': [r(GD12[0] + 0.2), 1.2, r(GD12[2] + 0.2), 1, 0.05]}, 'hands': {'R': 'open'}, 'face': {'lid': 0.45, 'mouth': 'smirk'}}, toonDur=0.15), k(r(STICK12 + 0.3), look='camera')])],   # ...a smirk to us
        props=[P('fine12', 'fineTicket', pos=[r(GD12[0] + 0.2), 1.18, r(GD12[2] + 0.28)], rot=[-1.2, 1.2, 0], opts={'w': 0.19}, keys=[k(STICK12, attach='mec', joint='head', offset=FINE_AT, rot=[0.0, 0.0, 0.12])]),
               BURST('paf12', [r(FORE[0] - 0.12), r(FORE[1] + 0.12), r(FORE[2] + 0.12)], STICK12, 'PAF !', 0.34)],   # (pass 2) where it lands (by his cap it hit the gendarme)
        cams=[FC(0.0, [r(ME[0] - 1.6), 1.7, -2.0], [[r(ME[0] + 0.3), 2.45, ME[2]], [r(ME[0] - 0.2), 2.45, ME[2]], [r(GD12[0] - 0.3), 2.35, GD12[2]], [ME[0], 1.0, ME[2]], [GD12[0], 1.0, GD12[2]]], top=0.14, bottom=0.72, drift=(0.06, 0.0, 0.06))])   # (pass 2) both whole in the frame (he was half out of it)
st.cue('sfx:paper', 'S12', 0.1, 0.15); st.cue('sfx:punch', 'S12', STICK12, 0.35)

# 13: ...for the noise. Close on him: the fine stuck on his forehead above his eyes, his hair on end, rings under his eyes; a tiny « ohé » drifts down in
#     front of his face, his eyes following it, lands on his shoulder with a tiny bounce and pops; his eyes come back to us; a slow blink; breathing
D13 = st.dur('S13'); LAND13 = 1.35; GONE13 = 1.8
OHE13 = [[0.0, r(ME[0] - 0.55), 2.85, 0.2], [0.5, r(ME[0] - 0.5), 2.45, 0.12], [0.95, r(ME[0] - 0.52), 2.05, 0.18], [r(LAND13 - 0.05), r(ME[0] - 0.12), 1.84, 0.24], [LAND13, r(ME[0] - 0.08), 1.8, 0.24]]
BR13 = lambda i: [1.0, 1.012, 1.0] if i % 2 else [1.0, 0.996, 1.0]
st.shot('S13', 'parisStreet', setOpts=STREET, actors=[
        act('mec', ME, -90, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'hairUp': 0.8, 'face': TIRED}, toonDur=0.0),
            k(0.25, toon={'hairUp': 0.8, 'sq': BR13(1), 'face': {**TIRED, 'lid': 0.45, 'gy': -0.4, 'gx': 0.1}}, toonDur=0.2, toonEase='inOut'),   # (pass 2) his eyes up to the little shout...
            k(0.75, toon={'hairUp': 0.8, 'sq': BR13(0), 'face': {**TIRED, 'lid': 0.5, 'gy': 0.15, 'gx': 0.15}}, toonDur=0.25, toonEase='inOut'),   # ...down past his nose...
            k(1.15, toon={'hairUp': 0.8, 'sq': BR13(1), 'bend': {'spine': [0.0, 0, 0.04, 1, None]}, 'face': {**TIRED, 'lid': 0.55, 'gy': 0.7, 'gx': 0.6}}, toonDur=0.25, toonEase='inOut'),   # ...onto his shoulder...
            k(1.95, toon={'hairUp': 0.8, 'sq': BR13(0), 'bend': {'spine': [0.0, 0, 0.02, 1, None]}, 'face': {**TIRED, 'gy': 0.0, 'gx': 0.0}}, toonDur=0.2, toonEase='inOut'),   # ...his eyes back to us...
            k(2.35, toon={'hairUp': 0.8, 'sq': BR13(1), 'face': {**TIRED, 'lid': 1.0}}, toonDur=0.14), k(2.6, toon={'hairUp': 0.8, 'sq': BR13(0), 'face': TIRED}, toonDur=0.18),   # ...a slow blink...
            k(2.95, toon={'hairUp': 0.8, 'sq': BR13(1), 'bend': {'spine': [0.0, 0, -0.02, 1, None]}, 'face': TIRED}, toonDur=0.3, toonEase='inOut')])],   # ...breathing, a shift of his weight
        props=[P('fine13', 'fineTicket', on={'actor': 'mec', 'joint': 'head', 'offset': FINE_AT}, rot=[0.0, 0.0, 0.12], opts={'w': 0.19}),   # (pass 2) above both eyes; (stills 2) bigger: at 0.15 it did not read
               P('ohe13', 'shoutLetters', **FLY(OHE13), face='camera', opts={'text': 'ohé', 'size': 0.07, 'colors': ['#F5C33B', '#F08A3C', '#E8463A'], 'wobble': 0.25, 'show': [0.0, r(GONE13 + 0.09)],
                 'squash': [[0.0, 1.0, 1.0], [LAND13, 1.35, 0.6], [r(LAND13 + 0.08), 0.9, 1.15], [r(LAND13 + 0.16), 1.0, 1.0]], 'grow': [[0.0, 1.0], [GONE13, 1.0], [r(GONE13 + 0.04), 1.3], [r(GONE13 + 0.09), 0.02]]})],   # (pass 2) in front of his face, onto his shoulder, a tiny bounce, then pop
        cams=[FC(0.0, [r(ME[0] - 1.5), 1.9, 0.7], [[ME[0], 2.5, ME[2]], [ME[0], 1.45, ME[2]], [r(ME[0] - 0.55), 2.85, 0.2], [ME[0], 1.75, 0.3]], top=0.12, bottom=0.62, drift=(0.15, 0.0, -0.08))])   # a slow push-in
st.cue('sfx:pop', 'S13', GONE13, 0.12)

# (cycle 13) the key poses and the lettering, measured in the engine by render3 --probe
for g_ in [('S01', 0.7, 'mec', 'shout'), ('S02', 0.6, 'mec', 'listen'), ('S03', 0.5, 'mec', 'mime'), ('S04', 0.5, 'gendarme', 'slap'), ('S05', 0.6, 'passant', 'double'), ('S06', 0.3, 'rando', 'point'),
           ('S07', 0.5, 'fermier', 'gape'), ('S08', 1.2, 'mec', 'stalks'), ('S09', 0.3, 'mec', 'flat'), ('S10', 0.4, 'gamin', 'night'), ('S11', 0.5, 'mec', 'ears'), ('S12', 0.85, 'mec', 'fine'), ('S13', 2.0, 'mec', 'end')]:
    st.gag(g_[0], g_[1], g_[2], g_[3])
for t_ in [('S04', 0.7, 'poster4', 'avis'), ('S13', 1.0, 'fine13', 'amende')]:
    st.text(t_[0], t_[1], t_[2], t_[3])
st.card('S05', 'DISPARU')
st.card('S13', 'TAPAGE', at=0.3)

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
st.write("L'écho", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'gendarme': {'preset': 'cop', 'seed': 601, 'suit': '#1F3E6E', 'hat': 'copcap', 'mustache': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'passant': {'preset': 'boss', 'seed': 602, 'suit': '#6B5B45', 'hat': 'fedora', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},
    'rando': {'preset': 'sportif', 'seed': 603, 'suit': '#D8642E', 'hat': 'beanie', 'hatColor': '#2F5E8C', 'build': {'width': 0.95, 'headWidth': 1.2}, 'toon': EX},   # (pass 2) a plain jacket, a beanie (the tourist's shirt read as noise)
    'fermier': {'preset': 'fermier', 'seed': 604, 'suit': '#7A6A3A', 'hat': 'maocap', 'hatColor': '#4E6B3A', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},   # (pass 2) 'cap' is no hat (nothing showed); a work colour away from his navy and red
    'voisine': {'preset': 'madame', 'seed': 605, 'suit': '#8E5AA8', 'build': {'width': 0.9, 'headWidth': 1.25}, 'toon': EX},
    'gamin': {'preset': 'gamin', 'seed': 606, 'suit': '#3A9BDC', 'build': {'height': 0.55, 'headScale': 1.35}, 'toon': EX},   # (pass 2) a child's head on a short body
    'vache': {'type': 'creature', 'name': 'cow', 'opts': {'seed': 2}},
})
