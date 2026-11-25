#!/usr/bin/env python3
"""Le chifoumi (story 96, cycle 51; in the manner of the first stories: a hook, an institutional escalation, a reversal, a dry last line).
This man lost at rock-paper-scissors to his wife. He contested. The federation reviewed the action on video: she had played a hundredth too late.
Match cancelled, to be replayed at the national stadium. Scientists filmed his hand at ten thousand frames a second: he always plays rock, for thirty
years. Judged too predictable, he was replaced by an unbeatable robot hand built by a factory; its first rock cost the factory two storeys. The
olympic committee selected it, the president decorated it in advance. Eighty thousand spectators, the anthem. Chi, fou, mi: the stadium split in two.
The hand played rock. His wife played well. She has trained on him for thirty years. The loser had to take out the bin. The hand contested: the well
does not count.
Running gags: the kitchen bin nobody takes out while the result is under review: full with its lid propped up in the kitchen (S01), overflowing in
the corner of the replay (S03), piled to the first-floor window by his door (S10), a mountain circled by seagulls behind the stadium (S11), taller
than his house in the reveal (S16), never mentioned before line 16. The referee's glowing rectangle drawn in the air (S02), which the robot hand
repeats at the end (S17). « Depuis trente ans » (S06: his photos and a block of tally marks) comes back the other way in S15.
Staging: in the kitchen, low across the table, his navy-sleeved fist (rock) and her flat mitten (paper) pump and meet, a quarter of the frame each;
she lays her hand over his fist and smiles; behind them, lit, the red bin with its lid propped up by a bulging bag. In a video-referee room three
referees in anthracite with headsets lean to a wall of screens looping the kitchen footage; the middle one draws a rectangle with his forearm and it
hangs in the air as a glowing trail; slow lateral pan. The replay fills the frame: the two hands frozen apart, stepping a frame at a time, a red line
drawn between them, the bin huge and overflowing in the top corner, « RALENTI » brackets. On the pitch a referee blows his whistle and waves the
match off (ANNULÉ); cut to the stadium from the air: a packed oval and, on the centre spot, a little kitchen table with a red top and two chairs.
In a white lab his fist sits in a padded clamp under two lamps, two scientists write, a big camera slides on rails toward the fist. The whiteboard:
three photos of him making a fist (a wedding veil, a bicycle, asleep on a pillow); a scientist scribbles a thick block of tally marks on « trente
ans ». At the federation an official slams a giant stamp on his file photo (a red cross, no words); he looks at his own fist. In a factory a
giant robot arm with a graphite box mitten rises among welders' sparks and closes its fist; screens loop his fist. It slams the test table (smear,
squash, dust from the roof); outside, the box factory slides two storeys into a ring of dust, two dusty workers lean out of windows now at ground
level. At his door an official moves the blank bib from his chest onto the robot's hand while the president on a stepladder pins a plain medal on
its wrist; beside the door the bags reach the first-floor window. The stadium stands up, hands on hearts (an invented anthem); the wife in her
apron faces the towering hand across the table; behind the rim a mountain of bags and seagulls; the scoreboard reads FINALE / ELLE – LA MAIN.
The arm pumps three times, the ground jumping; from the air a crack runs across the pitch and the two halves of the stadium slide apart, both
crowds cheering, while a round hole opens beside the table. Low: the fist comes down, a clean silhouette on the sky. She holds out her mitten
curled into a ring; a stone rim rises round the hole, the fist misses the table and plunges into the well, its arm stretching after it; a splash
comes up (PERDU). In the stands he lowers his fist to his waist and looks at it; insert: the kitchen, his fist under her hand. His street: the
mountain of bags taller than his house, gulls on top; the dripping robot rolls up; a quick tilt up the heap. The hand turns to us and draws the
referee's glowing rectangle; behind it one more bag rolls down; hold.
Natural look; cycle 51: props_chifoumi.js (chifHand, chifBin, chifBagHeap, chifTrail, chifScreens, chifHeadset, chifRedLine, chifHud, chifStadium,
chifClamp, chifRailCam, chifBoard, chifFile, chifRobot, chifRoom, chifSparks, chifWeldMask, chifFactoryBox, chifHouse, chifBib, chifMedal,
chifStepladder, chifApron); table, chair, desk, whistle, clipboardProp (props.js), giantStamp (props_rambarde), softDust (props_barbecue) reused.
Lessons applied from the start: `lens` is the vertical field; characters are about 2.3 m tall with the box head; faces and key props above the
caption band (0.77-0.83), heads below the card band (0.07-0.18) when a card stamps; every camera checked with project() (CHECKS); every extra cast
member has a preset; word timings come from timeline.json through st.at (words counted from 0); the payoff shots (S13, S14, S17) get their own
tight cameras; the crowd is instanced and the actors among it are checked one by one; mitten hands everywhere (fist, flat hand, a ring for the
well, never five fingers); no straight raised arm held still (every reach moves and comes down); one take per mechanism (his deadpan look at
the fist, her smile, the referee's puffed cheeks, the workers' cough); squash, stretch, smear and hang on the State's machine (the robot);
moving holds (breathing, blinks, loops on screens, gulls, drips); no flag, no rings, no emblem or insignia (plain blazer, plain medal, plain bib),
the anthem is invented (a choir and a fanfare from the effect bank); the stadium is built as two halves; no English, no brands; nobody hurt (the
workers lean out unhurt, dusty)."""
from story_kit import *
import math

st = Story('chifoumi', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0), ('S08', 'L08', 0),
         ('S09', 'L09', 0), ('S09b', 'L09', 7), ('S10', 'L10', 0), ('S11', 'L11', 0), ('S12', 'L12', 0), ('S13', 'L13', 0), ('S14', 'L14', 0), ('S15', 'L15', 0),
         ('S15b', 39.5333, 0), ('S16', 'L16', 0), ('S17', 'L17', 0)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def sub(a, b): return [r(a[i] - b[i]) for i in range(3)]
def mul(a, s): return [a[i] * s for i in range(3)]
def lerp3(a, b, u): return [r(a[i] + (b[i] - a[i]) * u) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
# a prop's local point to the world and back (prop ry in degrees, as the engine applies it)
def tow(base, ry, p): c, s_ = math.cos(math.radians(ry)), math.sin(math.radians(ry)); return [r(base[0] + p[0] * c + p[2] * s_), r(base[1] + p[1]), r(base[2] - p[0] * s_ + p[2] * c)]
def tol(base, ry, w): c, s_ = math.cos(math.radians(ry)), math.sin(math.radians(ry)); dx, dz = w[0] - base[0], w[2] - base[2]; return [r(dx * c - dz * s_), r(w[1] - base[1]), r(dx * s_ + dz * c)]
CHECKS = []
def chk(sid, frm, look, lens, pts):
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {project(frm, look, lens, p)}" for n, p in pts.items()))
def chkc(sid, c, pts, end=False):
    frm, look = (c.get('to') or c['from'], c.get('lookAt2') or c['lookAt']) if end else (c['from'], c['lookAt'])
    chk(sid + ('>' if end else ''), frm, look, c['lens'], pts)
def FC(sid, frm, pts, top=0.2, bottom=0.74, lenses=range(30, 60), margin=0.07):
    look, lens, w = fit(frm, pts, margin=margin, top=top, bottom=bottom, lenses=lenses)
    CHECKS.append(f'{sid} fit lens {lens}'); return look, lens or max(lenses)
def FB(sid, frm, pts, top=0.2, bottom=0.74, lenses=range(30, 57), margin=0.07, inside=None, level=True):
    # fitBack: back the camera away along the line from the points until a lens fits; the distance moved goes to CHECKS
    f2, look, lens = fitBack(frm, pts, margin=margin, top=top, bottom=bottom, lenses=lenses, inside=inside, level=level)
    CHECKS.append(f'{sid} fitBack {frm} -> {f2} lens {lens}'); return f2, look, lens or max(lenses)
def W(sid, lid, i):
    # (cycle 51) word timings from timeline.json: st.at counts the words from 0; the word is printed beside its time
    t = st.at(sid, lid, i); CHECKS.append(f"{sid} « {st.L[lid]['words'][i]['w']} » at {t}"); return t

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
DEAD = {'lid': 0.4, 'mouth': 'line'}
def blink(t, face=None): return [k(t, toon={'face': {**(face or DEAD), 'lid': 1.0}}, toonDur=0.05, keepPose=True), k(r(t + 0.1), toon={'face': face or DEAD}, toonDur=0.06, keepPose=True)]
def R5(p, w=1, s=0.04): return [*p, w, s]
HIDE = [0.01, 0.01, 0.01]
# a moving hold: slow breathing keys that carry the face (a keepPose key drops the face), clear of the blinks
def life(t0, t1, face, ph=0.0, blinks=(), period=0.9, amp=0.013):
    out, bl, t_, i = [], sorted(blinks), t0 + ph, 0
    while t_ < t1 - 0.1:
        if not any(-0.04 < t_ - b < 0.2 for b in bl):
            q = [r(1 - amp * 0.4, 4), r(1 + amp, 4), r(1 - amp * 0.4, 4)] if i % 2 == 0 else [r(1 + amp * 0.3, 4), r(1 - amp * 0.6, 4), r(1 + amp * 0.3, 4)]
            out.append(k(r(t_), toon={'sq': q, 'face': face}, toonDur=r(period * 0.8), toonEase='inOut', keepPose=True))
        t_ += period / 2; i += 1
    for b in bl: out += blink(r(b), face)
    return out
def HAND(pid, pos, ry, keys=None, **o): return P(pid, 'chifHand', pos=pos, ry=ry, opts=o, **({'keys': keys} if keys else {}))
def HEADSET(pid, who): return P(pid, 'chifHeadset', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={'w': 0.32})
def APRON(pid, who): return P(pid, 'chifApron', on={'actor': who, 'joint': 'torso', 'offset': [0.0, -0.1, 0.14]}, opts={'h': 1.1, 'w': 0.4})
def hand_tip(elbow, ry, s, sleeve, tilt=0.0, ahead=0.1):
    # where the middle of a chifHand's mitten is (elbow + forearm + half a hand), for the checks and to aim things at it
    d = s * (sleeve + ahead); F = fwd(ry); return [r(elbow[0] + F[0] * d * math.cos(tilt)), r(elbow[1] - d * math.sin(tilt)), r(elbow[2] + F[2] * d * math.cos(tilt))]

# the robot's two-bone arm, mirrored from props_chifoumi.js (chifRobot) to place a hand on it from the script: shoulder height and links at s = 1
def robot_wrist_world(base, ry, p): return tow(base, ry, p)

for g_ in [('S01', 1.2, 'mec', 'fist under her hand'), ('S07', 1.9, 'mec', 'looks at his fist'), ('S14', 0.5, 'femme', 'the well'), ('S15', 1.0, 'mec', 'lowers his fist')]:
    st.gag(*g_)

# ============================== the kitchen (kitchenDay: the counter along the back wall at z -3.3, the hanging lamp at (0, 2.7, -1.0))
KIT = {'fridge': False}
KT = [0.3, 0, -1.05]                                                    # the little table, 1.1 x 0.75, its top at 0.76
HK = [-0.12, 0.03, -1.62]; RYH = 22                                     # him behind the table on the left, turned three-quarters to us (a V)
FK = [0.72, 0.03, -1.62]; RYF = -22                                     # her on the right
BIN1 = [0.38, 0, -2.85]                                                 # the red bin in the gap between them, against the counter, lit by the window
SH = 1.7; SLV = 0.1                                                     # the cartoon hands: 2.2 times real size, a short forearm
RYE1, RYF1 = 55, -55                                                    # the forearms' headings: his from the left, hers from the right, angled to us
FIST_T, PAP_T = [0.2, 1.1, -0.87], [0.46, 1.1, -0.87]                # where the two hands meet, held up at chest height over the table
EH1 = [r(FIST_T[0] - fwd(RYE1)[0] * SH * (SLV + 0.1)), FIST_T[1], r(FIST_T[2] - fwd(RYE1)[2] * SH * (SLV + 0.1))]      # his right hand goes there (the prop's elbow)
EF1 = [r(PAP_T[0] - fwd(RYF1)[0] * SH * (SLV + 0.14)), PAP_T[1], r(PAP_T[2] - fwd(RYF1)[2] * SH * (SLV + 0.14))]      # her left hand
FIST1 = hand_tip(EH1, RYE1, SH, SLV)
PAP1 = hand_tip(EF1, RYF1, SH, SLV, ahead=0.14)
ONFIST1 = add(FIST1, [0.03, 0.11, 0.0])                                  # her flat hand laid over his fist: the elbow that puts the palm there
EF1B = [r(ONFIST1[0] - fwd(RYF1)[0] * SH * (SLV + 0.14)), r(ONFIST1[1] - 0.04), r(ONFIST1[2] - fwd(RYF1)[2] * SH * (SLV + 0.14))]
def KITCHEN_PROPS(n, lvl=0, binS=1.5, flies=0):
    return [P(f'table{n}', 'table', pos=KT, opts={'w': 1.1, 'd': 0.75, 'h': 0.76, 'color': '#DDB27A', 'legs': '#9A6E42'}),
            P(f'chaiseH{n}', 'chair', pos=[HK[0], 0, HK[2]], ry=RYH, opts={'color': '#7FB0C8'}), P(f'chaiseF{n}', 'chair', pos=[FK[0], 0, FK[2]], ry=RYF, opts={'color': '#7FB0C8'}),
            P(f'poubelle{n}', 'chifBin', pos=BIN1, ry=-10, opts={'level': lvl, 's': binS, 'flies': flies, 'stink': 2 if lvl else 0})]
HEROHAND = lambda: {'scl': {'handR': HIDE, 'handL': HIDE}}
WIFEHAND = lambda: {'scl': {'handL': HIDE, 'handR': HIDE}}
HANDH = lambda pid, e=EH1, **o: HAND(pid, e, RYE1, s=SH, sleeve=SLV, side='L', **o)
HANDF = lambda pid, e=EF1, **o: HAND(pid, e, RYF1, s=SH, sleeve=SLV, side='R', skin='#EBC29C', sleeveColor='#5E8C7A', **o)

# 1: the hook. Across the kitchen table, the two of them in a V behind it: both pump twice (chi, fou), and on « perdu » they throw: his fist (rock)
#    from the left, her flat mitten (paper) from the right, each a quarter of the frame; she lays her hand over his fist and smiles; he looks down
#    at it, then at us. Between them, lit, the red bin with its lid propped up by a bulging bag (the running gag, never mentioned)
D1 = st.dur('S01'); THROW1 = r(W('S01', 'L01', 3) - 0.02); LAY1 = r(THROW1 + 0.36)
F1 = [0.3, 1.82, 1.05]; L1 = [0.3, 1.25, -1.5]
C1 = cam(0.0, F1, add(F1, [0.0, -0.03, -0.15]), L1, add(L1, [0, -0.02, 0]), lens=48, ease='inOut')
chkc('S01', C1, {'fist': FIST1, 'paper': PAP1, 'binTop': add(BIN1, [0, 1.15, 0]), 'binFoot': add(BIN1, [0, 0.05, 0]), 'himHead': add(HK, [0, 1.92, 0]), 'herHead': add(FK, [0, 1.86, 0]), 'himEar': add(HK, [-0.2, 1.6, 0]), 'herEar': add(FK, [0.2, 1.6, 0])})
chkc('S01', C1, {'fist': FIST1, 'onFist': ONFIST1, 'binTop': add(BIN1, [0, 1.15, 0]), 'himHead': add(HK, [0, 1.92, 0])}, end=True)
SMUG = {'lid': 0.2, 'mouth': 'smile', 'brow': 0.45, 'cheeks': 0.6}
HERO1 = [k(-0.4, look=add(FIST1, [0, 0.3, 0.5])), k(0.0, toon={'reach': {'R': R5(EH1, 1, 0.0)}, **HEROHAND(), 'hip': 0, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.0),
         *[k(t_, toon={'sq': [1.0, 0.98, 1.0]}, toonDur=0.1, keepPose=True) for t_ in (0.05, 0.31)],
         k(r(THROW1 + 0.4), look=FIST1, lookDur=0.12), k(r(THROW1 + 0.4), toon={'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.2, 'gy': 0.5}}, toonDur=0.1, keepPose=True),
         k(1.62, look='camera', lookDur=0.12), k(1.62, toon={'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.15}}, toonDur=0.1, keepPose=True), *blink(1.95, {'lid': 0.45, 'mouth': 'line', 'brow': -0.15})]
FEMME1 = [k(-0.4, look=add(FIST1, [0, 0.3, 0.5])), k(0.0, toon={'reach': {'L': R5(EF1, 1, 0.0)}, **WIFEHAND(), 'hip': 0, 'face': {'lid': 0.2, 'mouth': 'line', 'brow': 0.2}}, toonDur=0.0),
          k(THROW1, toon={'face': SMUG}, toonDur=0.08, keepPose=True),
          k(r(THROW1 + 0.04), toon={'reach': {'L': R5(EF1B, 1, 0.0)}, 'sq': [1.02, 0.99, 1.02], 'face': SMUG}, toonDur=0.32, toonEase='inOut', keepPose=True),
          k(1.3, look='camera', lookDur=0.15), *blink(1.75, SMUG)]
st.shot('S01', 'kitchenDay', setOpts=KIT, actors=[act('mec', HK, RYH, 'sit', 'neutral', keys=HERO1), act('femme', FK, RYF, 'sit', 'neutral', keys=FEMME1)],
        props=[*KITCHEN_PROPS(1), APRON('tablier1', 'femme'),
               HANDH('mainH1', mode='rock', pumps=[0.05, 0.31], tilt=0.06),
               HANDF('mainF1', modes=[[-1, 'rock'], [THROW1, 'paper']], pumps=[0.05, 0.31], tilt=0.06, keys=[k(r(THROW1 + 0.04), to=EF1B, dur=0.32, ease='inOut')])],
        cams=[C1])
for t_ in (0.05, 0.31): st.cue('sfx:step', 'S01', t_, 0.25)
st.cue('sfx:punch', 'S01', THROW1, 0.3); st.cue('sfx:paper', 'S01', LAY1, 0.25)

# ============================== the video-referee room (whiteVoid + chifRoom: cool grey walls; the wall of screens on the left wall)
ROOM2 = {'w': 9, 'd': 9, 'h': 4.6, 'wall': '#7D8CA3', 'floor': '#4A5262', 'band': '#5E6C82', 'bandH': 1.1, 'trim': '#2E3646', 'lights': 3, 'lightY': 4.5}
R2 = [[-1.0, 0, -2.6], [0.1, 0, -2.25], [1.1, 0, -2.7]]               # three referees with their backs to us, leaning toward the wall of screens
SCR2 = [0.0, 0, -3.95]
# 2: he contested; the federation reviewed the action on video. Behind three referees in anthracite with headsets who lean toward a wall of screens
#    looping the kitchen footage, the camera trucks right; on « fédération » the middle one turns round to us and draws a rectangle in the air with
#    his forearm, low in front of his chest so his face stays clear: a glowing trail that hangs, pulsing, to the cut
D2 = st.dur('S02'); RECT2 = r(W('S02', 'L02', 4) - 0.05); RDUR2 = 1.0
F2A, F2B = [-0.45, 2.0, 3.1], [0.35, 1.98, 3.0]
L2A, L2B = [-0.2, 1.62, -3.0], [0.2, 1.6, -3.0]
C2 = cam(0.0, F2A, F2B, L2A, L2B, lens=48, ease='inOut')
REF2 = R2[1]; RYR2 = yaw(REF2, F2B)
RC2 = off(REF2, RYR2, 0.62, -0.08, 1.38)                                # the rectangle's centre, low in front of his chest, facing the camera
RR = right(RYR2)
RW2, RH2 = 0.66, 0.4
RECTPTS2 = [[r(RC2[0] + RR[0] * sx * RW2 / 2), r(RC2[1] + sy * RH2 / 2), r(RC2[2] + RR[2] * sx * RW2 / 2)] for sx, sy in [(1, 1), (-1, 1), (-1, -1), (1, -1), (1, 1)]]
chkc('S02', C2, {'ref1': add(R2[0], [0, 2.3, 0]), 'ref2': add(R2[1], [0, 2.3, 0]), 'ref3': add(R2[2], [0, 2.3, 0]), 'scrL': [-1.8, 2.55, -3.9], 'scrR': [1.8, 1.1, -3.9], 'rectL': RECTPTS2[1], 'rectR': RECTPTS2[0]})
chkc('S02', C2, {'ref1': add(R2[0], [0, 2.3, 0]), 'ref2face': add(R2[1], [0, 2.0, 0]), 'ref3': add(R2[2], [0, 2.3, 0]), 'rectL': RECTPTS2[1], 'rectR': RECTPTS2[0], 'rectLow': RECTPTS2[2]}, end=True)
# the hand rides the trail: one reach key per corner, at the times the trail gets there (constant speed, linear)
seglen = [math.dist(RECTPTS2[i], RECTPTS2[i + 1]) for i in range(4)]; TL2 = sum(seglen)
CORN2 = [RECT2] + [r(RECT2 + RDUR2 * sum(seglen[:i + 1]) / TL2) for i in range(4)]
REFF = {'lid': 0.35, 'mouth': 'line', 'brow': -0.4}
LEAN2 = {'bend': {'spine': [0.22, 0, 0, 1, None]}, 'face': REFF}
REFK2 = [k(0.0, look=[0.1, 1.8, -3.9], lookDur=0.0), k(0.0, toon=LEAN2, toonDur=0.0),
         k(r(RECT2 - 0.35), look=F2B, lookDur=0.2), k(r(RECT2 - 0.3), toon={'face': {**REFF, 'brow': 0.2}, 'reach': {'R': R5(RECTPTS2[0], 1, 0.1)}}, toonDur=0.25, toonEase='out')]
for i in range(4): REFK2.append(k(CORN2[i], toon={'face': {**REFF, 'brow': 0.3}, 'reach': {'R': R5(RECTPTS2[i + 1], 1, 0.1)}, 'hose': 0.15}, toonDur=r(CORN2[i + 1] - CORN2[i]), toonEase='linear'))
REFK2 += [k(r(CORN2[-1] + 0.05), toon={'face': {**REFF, 'brow': 0.1}, 'reach': {'R': R5(off(REF2, RYR2, 0.3, 0.25, 1.0), 0.0, 0.1)}}, toonDur=0.3, toonEase='inOut'), *blink(r(CORN2[-1] + 0.5), REFF)]
def NOD2(ph): return [k(r(ph + 0.6 * i), toon={**LEAN2, 'bend': {'spine': [0.22, 0, 0, 1, None], 'neck': [0.12 if i % 2 else 0.0, 0, 0, 1, None]}}, toonDur=0.25, toonEase='inOut') for i in range(5)]
st.shot('S02', 'whiteVoid', setOpts={'color': '#C9D0DA'}, actors=[
        act('arbitre1', R2[0], 170, 'stand', 'neutral', keys=[k(0.0, look=[-0.8, 1.9, -3.9], lookDur=0.0), k(0.0, toon=LEAN2, toonDur=0.0), *NOD2(0.2)]),
        act('arbitre2', REF2, 180, 'stand', 'neutral', keys=[k(r(RECT2 - 0.4), to=REF2, dur=0.3, glide=True, face=RYR2), *REFK2]),
        act('arbitre3', R2[2], 190, 'stand', 'neutral', keys=[k(0.0, look=[0.9, 1.7, -3.9], lookDur=0.0), k(0.0, toon=LEAN2, toonDur=0.0), *NOD2(0.5)])],
        props=[P('salle2', 'chifRoom', pos=[0, 0, -0.5], opts=ROOM2), P('ecrans2', 'chifScreens', pos=SCR2, opts={'cols': 3, 'rows': 2, 'sw': 1.15, 'sh': 0.7, 'y': 1.15}),
               P('console2', 'table', pos=[0.0, 0, -3.35], opts={'w': 3.6, 'd': 0.6, 'h': 0.95, 'color': '#2E3646', 'legs': '#1E2430'}),
               *[HEADSET(f'casque2_{i}', f'arbitre{i + 1}') for i in range(3)],
               P('trait2', 'chifTrail', pos=[0, 0, 0], opts={'pts': RECTPTS2, 'at': RECT2, 'dur': RDUR2, 'r': 0.014})],
        cams=[C2])
st.cue('sfx:beep', 'S02', 0.2, 0.15); st.cue('sfx:zip', 'S02', RECT2, 0.25); st.cue('sfx:bell', 'S02', r(RECT2 + RDUR2), 0.2)

# 3: she had played a hundredth too late. The replay fills the frame: the two hands frozen apart over the table, the playback stepping one frame at a
#    time (her flat hand creeps down in three jerks), then a red line drawn between them on « centième »; in the top corner the bin, huge now,
#    overflowing with bags; the « RALENTI » brackets over it all, a cool desaturated picture
D3 = st.dur('S03'); LINE3 = r(W('S03', 'L03', 5) - 0.1)
EF3 = add(EF1, [0.04, 0.2, 0.0])
FIST3 = FIST1; PAP3 = hand_tip(EF3, RYF1, SH, SLV, ahead=0.14)
F3 = [0.32, 1.72, 0.6]; L3 = [0.36, 1.12, -1.5]; LENS3 = 42
C3 = cam(0.0, F3, add(F3, [0.0, 0.0, -0.06]), L3, L3, lens=LENS3)
BIN3 = [0.38, 0, -2.85]
chkc('S03', C3, {'fist': FIST3, 'paper': PAP3, 'binTop': add(BIN3, [0, 1.9, 0]), 'binL': add(BIN3, [-0.45, 1.0, 0]), 'binR': add(BIN3, [0.45, 1.0, 0]), 'himHead': add(HK, [0, 1.92, 0])})
STEPS3 = [0.25, 0.55, 0.85]
# the replay brackets fill the frame exactly: a plane 0.45 m in front of the lens, as tall as the frame there, turned to face it
_d3 = [L3[i] - F3[i] for i in range(3)]; _n3 = math.sqrt(sum(v * v for v in _d3)); _d3 = [v / _n3 for v in _d3]
HUDP = [r(F3[i] + _d3[i] * 0.45) for i in range(3)]; HUDH = r(2 * 0.45 * math.tan(math.radians(LENS3) / 2) * 0.98); HUDW = r(HUDH * 9 / 16)
_yb = math.asin(-_d3[0]); HUDR = [r(math.asin(_d3[1] / math.cos(_yb)), 4), r(_yb, 4), 0.0]
st.shot('S03', 'kitchenDay', setOpts=KIT, grade='saturate(0.55) contrast(1.06) brightness(1.03)', actors=[
        act('mec', HK, RYH, 'sit', 'neutral', keys=[k(0.0, look=FIST3, lookDur=0.0), k(0.0, toon={'reach': {'R': R5(EH1, 1, 0.0)}, **HEROHAND(), 'hip': 0, 'breathe': 0, 'face': {'lid': 0.35, 'mouth': 'line'}}, toonDur=0.0)]),
        act('femme', FK, RYF, 'sit', 'neutral', keys=[k(0.0, look=FIST3, lookDur=0.0), k(0.0, toon={'reach': {'L': R5(EF3, 1, 0.0)}, **WIFEHAND(), 'hip': 0, 'face': SMUG}, toonDur=0.0),
                                                       *[k(t_, toon={'reach': {'L': R5(add(EF3, [0, -0.035 * (j + 1), 0]), 1, 0.0)}}, toonDur=0.02, keepPose=True) for j, t_ in enumerate(STEPS3)]])],
        props=[*KITCHEN_PROPS(3)[:3], P('poubelle3', 'chifBin', pos=BIN3, ry=-10, opts={'level': 2, 's': 1.45, 'flies': 5, 'stink': 3}),
               HANDH('mainH3', mode='rock', tilt=0.06),
               HANDF('mainF3', e=EF3, mode='paper', tilt=0.06, keys=[k(t_, to=add(EF3, [0, -0.035 * (j + 1), 0]), dur=0.02) for j, t_ in enumerate(STEPS3)]),
               P('ligne3', 'chifRedLine', pos=[0, 0, 0], opts={'a': add(FIST3, [0.0, 0.12, 0.06]), 'b': add(PAP3, [0.0, -0.06, 0.06]), 'at': LINE3, 'dur': 0.28, 'r': 0.01, 'ring': 0.055}),
               P('hud3', 'chifHud', pos=HUDP, rot=HUDR, opts={'w': HUDW, 'h': HUDH})],
        cams=[C3])
st.cue('sfx:scratch', 'S03', 0.0, 0.25); [st.cue('sfx:tick', 'S03', t_, 0.3) for t_ in STEPS3]; st.cue('sfx:zip', 'S03', LINE3, 0.2)

# ============================== the national stadium (grassland + chifStadium: the centre spot at the origin, the halves split along x = 0)
STAD = {'board': ['FINALE', 'ELLE – LA MAIN'], 'boardFar': -10.0, 'cheer': 0.7, 'hole': [-1.9, 0.9], 'holeR': 0.75}
GRASS = {'clouds': 14, 'grass': '#78A85A'}
TBL = [0.0, 0, 0.0]
def PITCH_TABLE(n, keys=None):
    return [P(f'tableS{n}', 'table', pos=TBL, opts={'w': 0.8, 'd': 0.6, 'h': 0.76, 'color': '#D8463A', 'legs': '#8A5A3A'}, **({'keys': keys} if keys else {})),
            P(f'chaiseA{n}', 'chair', pos=[-0.62, 0, 0.0], ry=90, opts={'color': '#7FB0C8'}), P(f'chaiseB{n}', 'chair', pos=[0.62, 0, 0.0], ry=-90, opts={'color': '#7FB0C8'})]
REFP = [1.2, 0, 6.5]
# 4: match cancelled, to be replayed at the national stadium. On the pitch a referee blows his whistle, cheeks puffed, and waves the match off with
#    both forearms crossing (ANNULÉ stamps on « annulé », his head kept under the card); cut on « À rejouer » to the stadium from the air: a packed
#    oval and, on the centre spot, a little table with a red top and two chairs, the camera sinking toward it so the table reads
D4 = st.dur('S04'); WAVE4 = r(W('S04', 'L04', 1) - 0.05); CUT4 = r(W('S04', 'L04', 2) - 0.04)
F4A = off(REFP, 20, 3.0, 0.2, 1.55)
L4A, LENS4A = FC('S04', F4A, {'refTop': add(REFP, [0, 2.38, 0]), 'refWaist': add(REFP, [0, 0.95, 0]), 'handL': off(REFP, 20, 0.45, 0.45, 1.3), 'handR': off(REFP, 20, 0.45, -0.45, 1.3)}, top=0.22, bottom=0.72, lenses=range(30, 56))
C4A = cam(0.0, F4A, add(F4A, [0, 0, -0.12]), L4A, add(L4A, [0, 0.02, 0]), lens=LENS4A)
chkc('S04', C4A, {'refTop': add(REFP, [0, 2.35, 0]), 'refFeet': REFP, 'handsUp': add(REFP, [0, 1.5, 0])})
F4B, T4B = [0.0, 62.0, 46.0], [0.0, 25.0, 25.0]
C4B = cam(CUT4, F4B, T4B, [0, 0, -4.0], [0, 0, -3.0], lens=44, ease='out')
chkc('S04', C4B, {'table': TBL, 'standsN': [0, 9, -38], 'standsS': [0, 9, 38], 'endW': [-45, 9, 0], 'endE': [45, 9, 0]})
chkc('S04', C4B, {'table': TBL, 'standsN': [0, 9, -38], 'standsS': [0, 9, 38], 'endW': [-30, 2, 0]}, end=True)
PUFF = {'lid': 0.2, 'mouth': 'O', 'jaw': 0.1, 'brow': 0.6, 'puff': 1}
WAVEP = lambda a: {'reach': {'R': R5(off(REFP, 20, 0.45, a * 0.35, 1.25), 1, 0.05), 'L': R5(off(REFP, 20, 0.42, -a * 0.35, 1.18), 1, 0.05)}, 'face': PUFF, 'scl': {'head': [1.12, 1.0, 1.0]}}
REFK4 = [k(0.0, look='camera', lookDur=0.0), k(0.0, toon={'face': {**PUFF, 'puff': 0.0}}, toonDur=0.0), k(0.12, toon={'face': PUFF, 'scl': {'head': [1.12, 1.0, 1.0]}, 'sq': [1.03, 0.98, 1.03]}, toonDur=0.08, toonEase='out')]
for i, t_ in enumerate([WAVE4, r(WAVE4 + 0.14), r(WAVE4 + 0.28), r(WAVE4 + 0.42)]): REFK4.append(k(t_, toon=WAVEP(1 if i % 2 == 0 else -1), toonDur=0.1, toonEase='inOut'))
REFK4.append(k(r(WAVE4 + 0.56), toon={'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.3}}, toonDur=0.15))
st.shot('S04', 'grassland', setOpts=GRASS, actors=[act('arbitreT', REFP, 20, 'stand', 'neutral', keys=[*REFK4, k(CUT4, visible=False)])],
        props=[P('stade4', 'chifStadium', pos=[0, 0, 0], opts={**STAD, 'cheer': 0.8}), *PITCH_TABLE(4),
               P('sifflet4', 'whistle', on={'actor': 'arbitreT', 'joint': 'head', 'offset': [0.0, 0.11, 0.16], 'rot': [0, 1.5708, 0]}, scale=3.0)],
        cams=[C4A, C4B])
st.card('S04', 'ANNULÉ', at=r(WAVE4 + 0.04))
st.cue('sfx:whistle', 'S04', 0.1, 0.5); st.cue('rain', 'S04', CUT4, 0.12, r(D4 - CUT4)); st.cue('whoosh', 'S04', CUT4, 0.2, 0.3, 400, 1800)

# ============================== the lab (whiteVoid + chifRoom: white walls, a pale blue band)
ROOM5 = {'w': 10, 'd': 9, 'h': 3.6, 'wall': '#E6ECF0', 'floor': '#CDD3D8', 'band': '#A9C8DE', 'bandH': 1.0, 'trim': '#5E7E9A', 'lights': 3}
CL5 = [0.0, 0, -1.2]; CLH = 1.2
HM5 = [-0.42, 0, -1.65]; RYM5 = 28                                        # he stands beside the clamp, his left forearm in the jaws
EH5 = [0.0, CLH + 0.02, -1.32]; RYE5 = 0                                   # the forearm in the clamp, the fist out toward +Z
FIST5 = hand_tip(EH5, RYE5, 1.5, 0.22)
SAV5 = [[1.45, 0, -2.4], [0.35, 0, -3.75]]
# 5: scientists filmed his hand at ten thousand frames a second. His fist sits in an orange padded clamp under two bright lamps; two scientists in
#    white coats write on clipboards; a big camera on rails slides slowly toward the fist (the lens a hand from it by the end); he looks at us
D5 = st.dur('S05')
F5 = [-1.95, 1.75, 2.15]; L5 = [0.0, 1.45, -1.2]
C5 = cam(0.0, F5, [-1.6, 1.7, 1.75], L5, add(L5, [0.0, -0.03, 0]), lens=46, ease='inOut')
chkc('S05', C5, {'fist': FIST5, 'himTop': add(HM5, [0, 2.32, 0]), 'sav1': add(SAV5[0], [0, 2.3, 0]), 'sav2': add(SAV5[1], [0, 2.3, 0]), 'railCamStart': [1.6, 1.3, -3.8], 'railCamEnd': [0.69, 1.3, -2.11], 'lampL': [-0.95, 1.95, -0.65]})
chkc('S05', C5, {'fist': FIST5, 'himTop': add(HM5, [0, 2.32, 0]), 'railCamEnd': [0.69, 1.3, -2.11], 'sav2': add(SAV5[1], [0, 2.3, 0])}, end=True)
SAVF = {'lid': 0.3, 'mouth': 'line', 'brow': 0.4}
def WRITE(who, p, ry, t0, n=8):
    base = off(p, ry, 0.42, 0.05, 1.25)
    ks = [k(0.0, look=FIST5, lookDur=0.0), k(0.0, toon={'reach': {'L': R5(off(p, ry, 0.4, -0.12, 1.3), 1, 0.05), 'R': R5(base, 1, 0.05)}, 'face': SAVF, 'bend': {'neck': [0.2, 0, 0, 1, None]}}, toonDur=0.0)]
    for i in range(n): ks.append(k(r(t0 + 0.13 * i), toon={'reach': {'L': R5(off(p, ry, 0.4, -0.12, 1.3), 1, 0.05), 'R': R5(off(p, ry, 0.42, 0.05 + 0.05 * (i % 2), 1.25 - 0.02 * (i % 3)), 1, 0.05)}, 'face': SAVF, 'bend': {'neck': [0.2, 0, 0, 1, None]}}, toonDur=0.1))
    return ks + [k(r(t0 + 0.13 * n + 0.2), look='camera', lookDur=0.15)] + blink(r(t0 + 0.13 * n + 0.7), SAVF)
st.shot('S05', 'whiteVoid', setOpts={'color': '#E8EEF2'}, actors=[
        act('mec', HM5, RYM5, 'stand', 'neutral', keys=[k(0.0, look='camera', lookDur=0.0), k(0.0, toon={'reach': {'L': R5(EH5, 1, 0.0)}, 'scl': {'handL': HIDE}, 'face': {'lid': 0.42, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.0),
                                                       k(1.3, look=FIST5, lookDur=0.2), k(2.2, look='camera', lookDur=0.15), *blink(2.6, {'lid': 0.42, 'mouth': 'line', 'brow': -0.1})]),
        act('savant1', SAV5[0], -35, 'stand', 'neutral', keys=WRITE('savant1', SAV5[0], -35, 0.3)),
        act('savant2', SAV5[1], 35, 'stand', 'neutral', keys=WRITE('savant2', SAV5[1], 35, 0.9, 6))],
        props=[P('labo5', 'chifRoom', pos=[0, 0, -0.5], opts=ROOM5), P('pince5', 'chifClamp', pos=CL5, opts={'h': CLH, 'lamps': False}),
               HAND('poing5', EH5, RYE5, s=1.5, sleeve=0.22, mode='rock'),
               P('rail5', 'chifRailCam', pos=[0.95, 0, -2.6], ry=-28, opts={'len': 3.4, 'z0': -1.4, 'z1': 0.55, 't0': 0.0, 't1': D5}),
               *[P(f'bloc5_{i}', 'clipboardProp', on={'actor': f'savant{i + 1}', 'hand': 'L', 'face': 'camera'}, scale=1.4) for i in range(2)]],
        cams=[C5])
st.cue('engine', 'S05', 0.0, 0.12); st.cue('sfx:shutter', 'S05', 0.6, 0.2); st.cue('sfx:shutter', 'S05', 1.6, 0.2)

# 6: conclusion: he always plays rock; for thirty years. The whiteboard in the same lab: three photos of him making a fist (a wedding veil beside
#    him, a bicycle, asleep on a pillow), the camera panning along them; on « trente ans » a scientist scribbles a thick block of tally marks under
#    them row after row, the camera sinking to it
D6 = st.dur('S06'); TALLY6 = r(W('S06', 'L06', 5) - 0.1); TDUR6 = 0.85
BRD6 = [0.0, 0, -3.3]; BW6, BH6, BY6 = 2.3, 1.55, 0.8
SAV6 = [-1.65, 0, -2.8]
F6A, F6B = [-0.7, 1.95, -0.3], [0.45, 1.92, -0.4]
C6 = cam(0.0, F6A, F6B, [-0.55, 1.85, -3.3], [0.35, 1.82, -3.3], lens=46, ease='inOut')
C6B = glide([cam(r(TALLY6 - 0.1), [-0.3, 1.6, 0.55], [-0.25, 1.58, 0.45], [-0.1, 1.42, -3.3], [-0.05, 1.4, -3.3], lens=50, ease='out')], 0.35)
chkc('S06', C6, {'ph1': [-0.83, 1.92, -3.29], 'ph2': [0.0, 1.92, -3.29], 'ph3': [0.83, 1.92, -3.29]})
chkc('S06', C6, {'ph2': [0.0, 1.92, -3.29], 'ph3T': [0.83, 2.32, -3.29], 'ph3R': [1.2, 1.92, -3.29]}, end=True)
chkc('S06', C6B, {'tallyTL': [-1.17, 1.44, -3.29], 'tallyBR': [1.17, 0.95, -3.29], 'photosLow': [0.0, 1.55, -3.29], 'savHead': add(SAV6, [0, 2.3, 0])})
TROWY = [BY6 + BH6 * 0.4 - (j + 0.5) * BH6 * 0.33 / 5 for j in range(5)]
SAVK6 = [k(0.0, look=[0.0, 1.9, -3.3], lookDur=0.0), k(0.0, toon={'reach': {'L': R5([-1.2, 1.5, -3.2], 0.0, 0.08)}, 'face': SAVF}, toonDur=0.0)]
for j, y_ in enumerate(TROWY):
    t0 = r(TALLY6 + TDUR6 * j / 5); t1 = r(TALLY6 + TDUR6 * (j + 1) / 5)
    SAVK6 += [k(r(t0 - 0.02), toon={'reach': {'L': R5([-1.0, y_, -3.22], 1, 0.12)}, 'face': {**SAVF, 'brow': 0.7}, 'hose': 0.2}, toonDur=0.03),
              k(t0, toon={'reach': {'L': R5([1.0, y_, -3.22], 1, 0.12)}, 'face': {**SAVF, 'brow': 0.7}, 'hose': 0.2}, toonDur=r(t1 - t0 - 0.02), toonEase='linear')]
SAVK6 += [k(r(TALLY6 + TDUR6 + 0.08), toon={'reach': {'L': R5([-1.4, 1.2, -3.0], 0.0, 0.08)}, 'face': SAVF}, toonDur=0.25), k(r(TALLY6 + TDUR6 + 0.15), look='camera', lookDur=0.15)]
st.shot('S06', 'whiteVoid', setOpts={'color': '#E8EEF2'}, actors=[act('savant1', SAV6, 35, 'stand', 'neutral', keys=[k(r(TALLY6 - 0.35), to=[-1.5, 0, -2.85], dur=0.3, glide=True, face=60), *SAVK6])],
        props=[P('labo6', 'chifRoom', pos=[0, 0, -0.5], opts=ROOM5), P('tableau6', 'chifBoard', pos=BRD6, opts={'w': BW6, 'h': BH6, 'y': BY6, 'tallyAt': TALLY6, 'tallyDur': TDUR6, 'rows': 5})],
        cams=[C6, C6B])
st.cue('sfx:paper', 'S06', r(TALLY6), 0.3); st.cue('sfx:scratch', 'S06', r(TALLY6 + 0.3), 0.18)

# ============================== the federation (whiteVoid + chifRoom: grey-green walls, the plaque FÉDÉRATION)
ROOM7 = {'w': 9, 'd': 8, 'h': 3.4, 'wall': '#B7C6BC', 'floor': '#C8B08C', 'band': '#8FA89A', 'bandH': 1.05, 'trim': '#3E5446', 'lights': 2, 'sign': ['FÉDÉRATION', 0.6, 2.62, 2.4, 0.46], 'signBg': '#2E4A3C'}
DESK7 = [0.0, 0, -1.5]; FILE7 = [0.1, 0.765, -1.4]
OF7 = [-0.55, 0, -2.25]; HM7 = [0.78, 0, -0.95]; RYM7 = -25
# 7: he was judged too predictable. From above the desk: the official behind it hangs a giant rubber stamp tilted toward us, then slams it down on
#    his file photo (two frames, a squash, the desk jumps); lifted off: a red cross in a slanted frame, no words; beside the desk he raises his own
#    fist to his chest and looks at it
D7 = st.dur('S07'); STAMP7 = r(W('S07', 'L07', 6) - 0.04)
F7 = [0.4, 2.4, 2.0]; L7 = [0.2, 1.4, -1.45]
C7 = cam(0.0, F7, add(F7, [0.0, -0.06, -0.15]), L7, L7, lens=50)
EH7 = off(HM7, RYM7, 0.3, 0.08, 1.42); RYE7 = RYM7 - 150; TILT7 = -1.1
FIST7 = [EH7[0], r(EH7[1] + 0.3), EH7[2]]
chkc('S07', C7, {'file': FILE7, 'fileTop': add(FILE7, [0, 0, -0.39]), 'ofHead': add(OF7, [0, 2.3, 0]), 'stampUp': [0.1, 1.9, -1.45], 'himHead': add(HM7, [0, 2.3, 0]), 'fist': FIST7})
STK7 = [k(0.0, to=[0.12, 1.75, -1.55], dur=0.01), k(0.0, rotTo=[0.55, 0, 0], dur=0.01), k(0.25, to=[0.12, 1.95, -1.5], dur=r(STAMP7 - 0.35), ease='out'),
        k(r(STAMP7 - 0.07), to=[0.12, 0.8, -1.42], dur=0.07, ease='in'), k(r(STAMP7 - 0.07), rotTo=[0, 0, 0], dur=0.07),
        k(r(STAMP7 + 0.25), to=[0.05, 1.4, -1.75], dur=0.3, ease='out'), k(r(STAMP7 + 0.25), rotTo=[-0.3, 0, 0.2], dur=0.3)]
OFK7 = [k(0.0, look=FILE7, lookDur=0.0), k(0.0, toon={'reach': {'R': R5([0.06, 1.98, -1.55], 1, 0.0), 'L': R5([0.18, 1.98, -1.55], 1, 0.0)}, 'face': {'lid': 0.3, 'mouth': 'clench', 'brow': -0.7}}, toonDur=0.0),
        k(0.25, toon={'reach': {'R': R5([0.06, 2.18, -1.5], 1, 0.0), 'L': R5([0.18, 2.18, -1.5], 1, 0.0)}, 'sq': [0.96, 1.05, 0.96], 'face': {'lid': 0.2, 'mouth': 'clench', 'brow': -0.9}}, toonDur=r(STAMP7 - 0.35), toonEase='out'),
        k(r(STAMP7 - 0.07), toon={'reach': {'R': R5([0.06, 1.03, -1.42], 1, 0.0), 'L': R5([0.18, 1.03, -1.42], 1, 0.0)}, 'sq': [1.08, 0.9, 1.08], 'face': {'lid': 0.7, 'mouth': 'clench', 'brow': -1}}, toonDur=0.07, toonEase='in'),
        k(r(STAMP7 + 0.25), toon={'reach': {'R': R5([0.0, 1.63, -1.75], 1, 0.0), 'L': R5([0.12, 1.63, -1.75], 1, 0.0)}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': -0.2}}, toonDur=0.3)]
HEROK7 = [k(0.0, look=add(FILE7, [0, 0.6, -0.4]), lookDur=0.0), k(0.0, toon={'reach': {'R': R5(EH7, 1, 0.0)}, 'scl': {'handR': HIDE}, 'face': {'lid': 0.42, 'mouth': 'line'}}, toonDur=0.0),
          k(r(STAMP7 + 0.12), look=FIST7, lookDur=0.15), k(r(STAMP7 + 0.12), toon={'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.25, 'gy': 0.4}}, toonDur=0.12, keepPose=True), *blink(r(STAMP7 + 0.55), {'lid': 0.3, 'mouth': 'line', 'brow': 0.25})]
st.shot('S07', 'whiteVoid', setOpts={'color': '#DDE3DC'}, actors=[act('officiel7', OF7, 8, 'stand', 'neutral', keys=OFK7), act('mec', HM7, RYM7, 'stand', 'neutral', keys=HEROK7)],
        props=[P('bureau7', 'chifRoom', pos=[0, 0, -0.5], opts=ROOM7), P('desk7', 'desk', pos=DESK7, opts={'w': 1.8, 'color': '#5E7A6A', 'top': '#B98A5A'}),
               P('dossier7', 'chifFile', pos=FILE7, ry=4, opts={'stampAt': STAMP7}), P('tampon7', 'giantStamp', pos=[0.12, 1.75, -1.55], opts={'s': 0.95}, keys=STK7),
               HAND('poing7', EH7, RYE7, s=1.35, sleeve=0.18, mode='rock', tilt=TILT7)],
        cams=[C7, cam(STAMP7, F7, add(F7, [0.0, -0.06, -0.15]), L7, L7, lens=50, shake=0.03)])
st.cue('whoosh', 'S07', r(STAMP7 - 0.1), 0.2, 0.15, 600, 2400); st.cue('thud', 'S07', STAMP7, 0.6); st.cue('sfx:punch', 'S07', STAMP7, 0.3)

# ============================== the factory floor (whiteVoid + chifRoom: concrete, a hazard stripe, steel columns)
ROOM8 = {'w': 20, 'd': 16, 'h': 8, 'wall': '#9AA3AB', 'floor': '#7E8389', 'lights': 4, 'lightY': 7.9, 'stripes': True, 'hazard': True, 'hazardY': 1.6, 'beams': True}
RB8 = [0.0, 0, -3.0]
W8 = [[2.4, 0, -1.6], [-2.2, 0, -1.9]]
# 8: a factory built an unbeatable robot hand. Low, looking up: among welders' sparks the giant arm rises from its pedestal with a stretch, the
#    graphite box mitten closes into a fist with a pop on « robot » and flexes on « imbattable »; two screens on stands loop his fist
D8 = st.dur('S08'); CLOSE8 = r(W('S08', 'L08', 6) - 0.05); FLEX8 = r(W('S08', 'L08', 7))
PATH8 = [{'t': 0.0, 'p': [0, 1.5, 2.6], 'hp': -1.0, 'curl': 0.0}, {'t': 0.25, 'p': [0, 1.6, 2.6], 'hp': -1.0, 'curl': 0.0, 'ease': 'inOut'},
         {'t': r(CLOSE8 - 0.1), 'p': [0.75, 4.9, 2.07], 'hp': 1.2, 'curl': 0.0, 'st': 1.08, 'ease': 'out'}, {'t': CLOSE8, 'p': [0.75, 4.85, 2.07], 'hp': 1.25, 'curl': 1.0, 'st': 1.0, 'ease': 'out'},
         {'t': FLEX8, 'p': [0.75, 4.8, 2.1], 'hp': 1.18, 'curl': 1.0, 'ease': 'inOut'}, {'t': r(FLEX8 + 0.12), 'p': [0.75, 4.92, 2.05], 'hp': 1.3, 'curl': 1.0, 'ease': 'out'}, {'t': D8, 'p': [0.75, 4.86, 2.07], 'hp': 1.25, 'curl': 1.0, 'ease': 'inOut'}]
F8 = [2.7, 1.0, 4.4]
F8, L8, LENS8 = FB('S08', F8, {'handTop': tow(RB8, 0, [0, 6.5, 2.4]), 'base': add(RB8, [0, 0, 1.2]), 'w1': add(W8[0], [0, 2.2, 0]), 'w2': add(W8[1], [0, 2.2, 0]), 'w1f': W8[0]}, top=0.12, bottom=0.74)
C8 = cam(0.0, F8, add(F8, [-0.25, 0.1, -0.2]), L8, add(L8, [0, 0.15, 0]), lens=LENS8, ease='inOut')
chkc('S08', C8, {'hand': tow(RB8, 0, [0, 5.5, 2.6]), 'handLow': tow(RB8, 0, [0, 1.5, 3.2]), 'scrA': [3.8, 2.0, -2.5], 'scrB': [-3.8, 2.0, -2.5]})
WELD = lambda p, ry, ph: [k(0.0, look=add(RB8, [0, 0.6, 0]), lookDur=0.0), k(0.0, toon={'reach': {'R': R5(off(p, ry, 0.55, 0.0, 0.85), 1, 0.05), 'L': R5(off(p, ry, 0.45, 0.15, 0.95), 1, 0.05)}, 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': DEAD}, toonDur=0.0),
                          *[k(r(ph + 0.35 * i), toon={'reach': {'R': R5(off(p, ry, 0.55, 0.05 * (i % 2), 0.85 + 0.03 * (i % 3)), 1, 0.05), 'L': R5(off(p, ry, 0.45, 0.15, 0.95), 1, 0.05)}, 'bend': {'spine': [0.35, 0, 0, 1, None]}, 'face': DEAD}, toonDur=0.25) for i in range(7)]]
st.shot('S08', 'whiteVoid', setOpts={'color': '#A9B0B6'}, actors=[act(f'soudeur{i + 1}', p, yaw(p, RB8), 'stand', 'neutral', keys=WELD(p, yaw(p, RB8), 0.1 * i)) for i, p in enumerate(W8)],
        props=[P('usine8', 'chifRoom', pos=[0, 0, 0], opts=ROOM8), P('robot8', 'chifRobot', pos=RB8, opts={'base': 'pedestal', 'path': PATH8, 'hits': [CLOSE8], 'smear': [[r(CLOSE8 - 0.5), r(CLOSE8 - 0.1)]]}),
               *[P(f'etincelles8_{i}', 'chifSparks', pos=off(p, yaw(p, RB8), 0.62, 0.0, 0.85), opts={'s': 1.0, 'ph': 0.7 * i}) for i, p in enumerate(W8)],
               P('ecranA8', 'chifScreens', pos=[3.8, 0, -2.6], ry=-30, opts={'stand': True, 'kinds': ['fist'], 'y': 1.4, 'sw': 1.1, 'sh': 0.68}),
               P('ecranB8', 'chifScreens', pos=[-3.8, 0, -2.6], ry=30, opts={'stand': True, 'kinds': ['fist'], 'y': 1.4, 'sw': 1.1, 'sh': 0.68})],
        cams=[C8])
st.cue('engine', 'S08', 0.2, 0.25); st.cue('sfx:static', 'S08', 0.0, 0.12); st.cue('clang', 'S08', CLOSE8, 0.45); st.cue('sfx:rattleShort', 'S08', FLEX8, 0.25)

# 9: on its first try it played rock. Same factory: the arm winds up high (stretched, hanging three frames), then slams its fist down on the steel
#    test table on « pierre » (two-frame smear, the fist squashes, the table crumples, the camera shakes, dust falls from the roof)
D9 = st.dur('S09'); HIT9 = r(W('S09', 'L09', 6) + 0.02)
TT9 = [0.0, 0, 1.0]
PATH9 = [{'t': 0.0, 'p': [0.75, 4.86, 2.07], 'hp': 1.25, 'curl': 1.0}, {'t': 0.6, 'p': [0, 5.0, 2.0], 'hp': 0.7, 'curl': 1.0, 'st': 1.12, 'ease': 'out'},
         {'t': r(HIT9 - 0.12), 'p': [0, 5.1, 1.95], 'hp': 0.8, 'curl': 1.0, 'st': 1.15, 'ease': 'inOut'}, {'t': HIT9, 'p': [0, 1.7, 3.55], 'hp': -0.15, 'curl': 1.0, 'st': 1.0, 'ease': 'in'},
         {'t': r(HIT9 + 0.12), 'p': [0, 1.62, 3.55], 'hp': -0.18, 'curl': 1.0, 'ease': 'out'}, {'t': D9, 'p': [0, 1.66, 3.55], 'hp': -0.16, 'curl': 1.0, 'ease': 'inOut'}]
F9 = [2.6, 1.45, 4.7]
_u, _v, _w = FB('S09', F9, {'up': tow(RB8, 0, [0, 7.6, 1.9]), 'table': add(TT9, [0.8, 0.0, 0.5]), 'tableL': add(TT9, [-0.8, 0.0, 0.5]), 'base': add(RB8, [0, 0, 1.0])}, top=0.1, bottom=0.74)
L9, LENS9 = [0.0, 2.25, 0.3], 56
C9 = cam(0.0, F9, add(F9, [-0.15, 0, -0.25]), L9, add(L9, [0, -0.1, 0]), lens=LENS9, ease='inOut')
chkc('S09', C9, {'fistHit': tow(RB8, 0, [0, 1.3, 4.0]), 'tableTop': add(TT9, [0, 1.0, 0])})
st.shot('S09', 'whiteVoid', setOpts={'color': '#A9B0B6'}, actors=[],
        props=[P('usine9', 'chifRoom', pos=[0, 0, 0], opts=ROOM8), P('robot9', 'chifRobot', pos=RB8, opts={'base': 'pedestal', 'path': PATH9, 'hits': [HIT9], 'smear': [[r(HIT9 - 0.11), r(HIT9 + 0.01)]]}),
               P('table9', 'table', pos=TT9, opts={'w': 1.6, 'd': 1.0, 'h': 1.0, 'color': '#A9B0B8', 'legs': '#6A7078'}, keys=[k(HIT9, squash=[1.25, 0.55, 1.25], dur=2.0)]),
               P('poussiere9', 'softDust', pos=[0.0, 1.0, 1.0], opts={'at': HIT9, 'n': 12, 'size': 0.9, 'spread': 2.2, 'rise': 0.5, 'life': 1.0, 'color': '#D8D2C4'}),
               P('platre9', 'softDust', pos=[0.5, 6.5, 0.0], opts={'at': r(HIT9 + 0.05), 'n': 10, 'size': 0.8, 'spread': 3.5, 'rise': -2.5, 'life': 1.3, 'color': '#E8E4DA', 'opacity': 0.7}),
               P('ecranA9', 'chifScreens', pos=[3.8, 0, -2.6], ry=-30, opts={'stand': True, 'kinds': ['fist'], 'y': 1.4, 'sw': 1.1, 'sh': 0.68})],
        cams=[C9, cam(HIT9, F9, add(F9, [-0.15, 0, -0.25]), L9, add(L9, [0, -0.1, 0]), lens=LENS9, shake=0.06)])
st.cue('sfx:zip', 'S09', r(HIT9 - 0.12), 0.25); st.cue('thunder', 'S09', HIT9, 0.5); st.cue('sfx:crunch', 'S09', HIT9, 0.5)

# 9b: the factory lost two storeys. Outside, wide: the box factory with its rows of windows slides two storeys down into the ground with a jolt on
#    « perdu », a ring of dust rolling out along the grass; then closer: two workers in white hard hats lean out of two windows now at ground level,
#    dusty, unhurt, and cough a puff of dust
D9b = st.dur('S09b'); SINK9 = r(W('S09b', 'L09', 9) - 0.12); FH = 3.2
FAC = [0.0, 0, -14.0]; FBW, FBD = 16.0, 10.0
OPEN9 = [[2, 3], [2, 4]]
def WINX(c): return r(-FBW / 2 + (c + 0.5) * FBW / math.floor(FBW / 2.2))
WK = [[r(FAC[0] + WINX(c)), 0.35, r(FAC[2] + FBD / 2 - 0.4)] for f, c in OPEN9]
SEEN9 = r(SINK9 + 0.95)
F9bA = [10.0, 2.2, 14.0]
F9bA, L9bA, LENS9bA = FB('S09b', F9bA, {'roof': add(FAC, [-FBW / 2, 4 * FH + 0.5, FBD / 2]), 'roofR': add(FAC, [FBW / 2, 4 * FH + 0.5, -FBD / 2]), 'footL': add(FAC, [-FBW / 2, 0, FBD / 2]), 'footR': add(FAC, [FBW / 2, 0, FBD / 2])}, top=0.14, bottom=0.72, lenses=range(30, 57))
C9bA = cam(0.0, F9bA, add(F9bA, [-0.4, 0, -0.3]), L9bA, L9bA, lens=LENS9bA)
F9bB = [r((WK[0][0] + WK[1][0]) / 2 + 0.5), 1.6, WK[0][2] + 8.5]
L9bB = [r((WK[0][0] + WK[1][0]) / 2), 1.3, WK[0][2]]
C9bB = cam(r(SEEN9 - 0.05), F9bB, add(F9bB, [-0.1, 0, -0.3]), L9bB, L9bB, lens=44)
chkc('S09b', C9bB, {'w1': add(WK[0], [0, 2.15, 0.6]), 'w2': add(WK[1], [0, 2.15, 0.6]), 'win1': [WK[0][0], 1.76, FAC[2] + FBD / 2], 'win2': [WK[1][0], 1.76, FAC[2] + FBD / 2]})
COUGH = {'lid': 0.6, 'mouth': 'O', 'jaw': 0.3, 'brow': 0.5, 'puff': 0.6}
def WORKER(i):
    t0 = r(SEEN9 + 0.08 * i)
    return [k(0.0, visible=False), k(t0, visible=True), k(0.0, look='camera', lookDur=0.0),
            k(t0, toon={'bend': {'spine': [0.75, 0, 0, 1, None]}, 'reach': {'R': R5(off(WK[i], 0, 0.75, -0.35, 1.05), 1, 0.05), 'L': R5(off(WK[i], 0, 0.75, 0.35, 1.05), 1, 0.05)}, 'face': {'lid': 0.1, 'mouth': 'o', 'brow': 0.7}, 'hip': 0}, toonDur=0.12, toonEase='out'),
            k(r(t0 + 0.3 + 0.06 * i), toon={'face': COUGH, 'sq': [1.04, 0.95, 1.04]}, toonDur=0.05, keepPose=True), k(r(t0 + 0.45 + 0.06 * i), toon={'face': {'lid': 0.4, 'mouth': 'line', 'brow': 0.2}, 'sq': [1, 1, 1]}, toonDur=0.12, keepPose=True)]
st.shot('S09b', 'grassland', setOpts=GRASS, actors=[act(f'ouvrier{i + 1}', WK[i], 0, 'stand', 'neutral', keys=WORKER(i)) for i in range(2)],
        props=[P('usineX9', 'chifFactoryBox', pos=FAC, opts={'w': FBW, 'd': FBD, 'floors': 4, 'fh': FH, 'sinkAt': SINK9, 'sinkDur': 0.45, 'sinkFloors': 2, 'open': OPEN9}),
               *[P(f'toux9_{i}', 'softDust', pos=off(WK[i], 0, 1.1, 0, 1.75), opts={'at': r(SEEN9 + 0.3 + 0.14 * i), 'n': 5, 'size': 0.35, 'spread': 0.4, 'rise': 0.3, 'life': 0.6, 'color': '#D9CDB4'}) for i in range(2)]],
        cams=[C9bA, C9bB])
st.cue('thunder', 'S09b', SINK9, 0.55); st.cue('sfx:crunch', 'S09b', r(SINK9 + 0.4), 0.35); st.cue('sfx:poof', 'S09b', r(SEEN9 + 0.3), 0.25)

# ============================== his street (pavillon without its house + chifHouse: the front at z -3.6, the door at x -1.2)
STREET = {'house': False, 'mailbox': False}
HOUSE = [0.0, 0, -6.6]
RBT10 = [-5.0, 0, -4.3]                                                  # the robot beside the house, its arm running along the facade behind them
HM10 = [-0.6, 0, -2.75]
OFC10 = [-1.45, 0, -2.25]; LAD10 = [-2.9, 0, -2.7]; PRS10 = [-2.9, 1.03, -2.7]
HANDW10 = [-1.85, 2.45, -3.15]                                           # the robot's wrist, its fist standing up behind them, the back of the hand turned to us
RYB10 = yaw(RBT10, HANDW10)
PATH10 = [{'t': 0.0, 'p': tol(RBT10, RYB10, HANDW10), 'hp': 1.35, 'curl': 1.0, 'roll': 3.1416}, {'t': 1.0, 'p': tol(RBT10, RYB10, add(HANDW10, [0, 0.05, 0])), 'hp': 1.32, 'curl': 1.0, 'roll': 3.1416, 'ease': 'inOut'},
          {'t': 2.0, 'p': tol(RBT10, RYB10, add(HANDW10, [0, -0.03, 0])), 'hp': 1.36, 'curl': 1.0, 'roll': 3.1416, 'ease': 'inOut'}, {'t': 3.65, 'p': tol(RBT10, RYB10, add(HANDW10, [0, 0.04, 0])), 'hp': 1.33, 'curl': 1.0, 'roll': 3.1416, 'ease': 'inOut'}]
BIBH = [-1.62, 2.95, -3.05]                                               # the bib on the back of the robot's hand (the hand stands up from the wrist)
# 10: the olympic committee selected it; the president decorated it in advance. At his door, the robot's fist standing up behind him: an
#     official in a plain blazer unpins the blank bib from his chest and pins it on the back of the robot's hand; the president on a stepladder
#     pins a plain medal on its wrist on « décorée »; beside the door the bags reach the first-floor window
D10 = st.dur('S10'); MED10 = r(W('S10', 'L10', 8) - 0.04); CUT10 = r(W('S10', 'L10', 5) - 0.1)
UNPIN10, PIN10 = 0.45, 1.25
F10A = [0.2, 1.75, 3.9]
L10A, LENS10A = FC('S10', F10A, {'him': add(HM10, [0, 2.3, 0]), 'himF': HM10, 'hand': add(HANDW10, [0, 1.25, 0]), 'of': add(OFC10, [0, 2.3, 0]), 'ofF': OFC10}, top=0.2, bottom=0.76)
C10A = cam(0.0, F10A, add(F10A, [0, 0.05, -0.2]), L10A, add(L10A, [0, 0.05, 0]), lens=LENS10A)
F10B = [1.6, 1.7, 7.4]
L10B, LENS10B = FC('S10', F10B, {'him': add(HM10, [0, 2.3, 0]), 'himF': HM10, 'hand': add(HANDW10, [0, 1.3, 0]), 'pres': add(PRS10, [0, 2.3, 0]), 'heapTop': [1.4, 4.6, -2.95], 'win': [1.6, 4.4, -3.6], 'ladF': LAD10}, top=0.12, bottom=0.76)
C10B = cam(CUT10, F10B, add(F10B, [-0.15, 0.05, -0.25]), L10B, L10B, lens=LENS10B)
chkc('S10', C10A, {'bibChest': add(HM10, [0, 1.45, 0.15]), 'bibHand': BIBH})
chkc('S10', C10B, {'wrist': HANDW10, 'bibHand': BIBH, 'robotBase': RBT10})
BIBPATH = [add(HM10, [0.0, 1.42, 0.2]), add(HM10, [0.25, 1.9, 0.1]), BIBH]
OFF10 = {'lid': 0.3, 'mouth': 'line', 'brow': 0.2}
OFK10 = [k(0.0, look=BIBPATH[0], lookDur=0.0), k(0.0, toon={'face': OFF10, 'reach': {'R': R5(off(OFC10, 50, 0.2, 0.2, 1.0), 0.0, 0.05)}}, toonDur=0.0),
         k(0.15, toon={'face': OFF10, 'reach': {'R': R5(BIBPATH[0], 1, 0.06)}}, toonDur=0.3, toonEase='inOut'),
         k(UNPIN10, toon={'face': OFF10, 'reach': {'R': R5(BIBPATH[1], 1, 0.06)}}, toonDur=0.35, toonEase='inOut'), k(r(UNPIN10 + 0.2), look=BIBH, lookDur=0.2),
         k(r(UNPIN10 + 0.35), toon={'face': OFF10, 'reach': {'R': R5(BIBPATH[2], 1, 0.06)}, 'sq': [0.97, 1.04, 0.97]}, toonDur=r(PIN10 - UNPIN10 - 0.35), toonEase='inOut'),
         k(r(PIN10 + 0.15), toon={'face': {**OFF10, 'mouth': 'smile'}, 'reach': {'R': R5(off(OFC10, 50, 0.2, 0.2, 1.0), 0.0, 0.05)}}, toonDur=0.35, toonEase='inOut'), k(r(PIN10 + 0.3), look='camera', lookDur=0.2)]
BIBK = [k(0.0, visible=False), k(UNPIN10, visible=True), k(UNPIN10, to=BIBPATH[1], dur=0.35, ease='inOut'), k(r(UNPIN10 + 0.35), to=BIBPATH[2], dur=r(PIN10 - UNPIN10 - 0.35), ease='inOut'), k(PIN10, visible=False)]
PRF = {'lid': 0.25, 'mouth': 'smile', 'brow': 0.4}
WRIST10 = add(HANDW10, [-0.12, -0.2, 0.15])
PRK10 = [k(0.0, look=WRIST10, lookDur=0.0), k(0.0, toon={'face': PRF, 'reach': {'L': R5(off(PRS10, 65, 0.25, -0.3, 1.05), 0.6, 0.05), 'R': R5(off(PRS10, 65, 0.3, 0.2, 1.1), 0.5, 0.05)}}, toonDur=0.0),
         k(r(MED10 - 0.45), toon={'face': PRF, 'reach': {'L': R5(off(PRS10, 65, 0.25, -0.3, 1.05), 0.6, 0.05), 'R': R5(WRIST10, 1, 0.06)}, 'sq': [0.97, 1.03, 0.97]}, toonDur=0.4, toonEase='inOut'),
         k(r(MED10 + 0.2), toon={'face': {**PRF, 'mouth': 'smile', 'brow': 0.6}, 'reach': {'L': R5(off(PRS10, 65, 0.25, -0.3, 1.05), 0.6, 0.05), 'R': R5(off(PRS10, 65, 0.3, 0.25, 1.0), 0.3, 0.05)}}, toonDur=0.35, toonEase='inOut'), k(r(MED10 + 0.3), look='camera', lookDur=0.2)]
HEROK10 = [k(0.0, look='camera', lookDur=0.0), k(0.0, toon={'face': {'lid': 0.45, 'mouth': 'line'}}, toonDur=0.0), k(0.2, look=BIBPATH[0], lookDur=0.2), k(r(PIN10 + 0.1), look='camera', lookDur=0.15), *blink(r(PIN10 + 0.5)), *blink(2.9)]
st.shot('S10', 'pavillon', setOpts=STREET, actors=[act('mec', HM10, 12, 'stand', 'neutral', keys=HEROK10), act('officiel10', OFC10, 50, 'stand', 'neutral', keys=OFK10),
        act('president', PRS10, 35, 'stand', 'neutral', keys=PRK10)],
        props=[P('maison10', 'chifHouse', pos=HOUSE), P('sacs10', 'chifBagHeap', pos=[1.45, 0, -2.95], opts={'h': 4.6, 'r': 1.35, 'bag': 0.62, 'flies': 6, 'flyS': 0.9}),
               P('robot10', 'chifRobot', pos=RBT10, ry=RYB10, opts={'base': 'tracks', 'path': PATH10, 'bibAt': PIN10, 'medalAt': MED10, 'medalYaw': math.radians(yaw(HANDW10, F10B) - RYB10)}),
               P('dossardH10', 'chifBib', on={'actor': 'mec', 'joint': 'torso', 'offset': [0.0, 0.32, 0.15]}, keys=[k(UNPIN10, visible=False)]),
               P('dossardV10', 'chifBib', pos=BIBPATH[0], ry=12, keys=BIBK, opts={'w': 0.34, 'h': 0.27}), P('escabeau10', 'chifStepladder', pos=LAD10, ry=65, opts={'h': 1.0})],
        cams=[C10A, C10B])
st.cue('sfx:paper', 'S10', UNPIN10, 0.2); st.cue('sfx:click', 'S10', PIN10, 0.3); st.cue('sfx:fanfare', 'S10', r(MED10 + 0.05), 0.2); st.cue('sfx:clink', 'S10', MED10, 0.3)

# ============================== the final (the stadium again: the wife at the table, the robot on tracks facing her across it)
FM = [-1.0, 0, 0.0]; RYFM = 42
RBS = [3.4, 0, -0.3]; RYRS = -90
HEAP11 = [-12.0, 0, -66.0]
UP11 = [0.6, 3.6, -0.1]                                                   # the fist towering over the table
def RS(p): return tol(RBS, RYRS, p)
# 11: eighty thousand spectators; national anthem. Low and wide from the pitch: the crowd sits cheering, then stands on « Hymne », right hands on
#     hearts (an invented anthem: a choir and a fanfare, no flags anywhere); on the centre spot the wife in her apron faces the towering fist across
#     the little table; behind the far rim a mountain of bin bags circled by seagulls; the scoreboard reads FINALE / ELLE – LA MAIN
D11 = st.dur('S11'); HYMN11 = r(W('S11', 'L11', 3) - 0.1)
F11 = [2.2, 1.25, 9.5]
F11, L11, LENS11 = FB('S11', F11, {'heapTop': add(HEAP11, [0, 46, 0]), 'fist': UP11, 'wife': add(FM, [0, 2.2, 0]), 'wifeF': FM, 'board': [-8, 20, -40]}, top=0.1, bottom=0.74, lenses=range(30, 57))
C11 = cam(0.0, F11, add(F11, [-0.3, 0.15, -0.6]), L11, add(L11, [0, 0.3, 0]), lens=LENS11, ease='inOut')
chkc('S11', C11, {'robotBase': RBS, 'table': TBL, 'standsFar': [0, 11, -38], 'standsL': [-40, 11, 5]})
PATH11 = [{'t': 0.0, 'p': RS(UP11), 'hp': -0.25, 'curl': 1.0}, {'t': 1.2, 'p': RS(add(UP11, [0, 0.12, 0])), 'hp': -0.2, 'curl': 1.0, 'ease': 'inOut'}, {'t': D11, 'p': RS(add(UP11, [0, -0.05, 0])), 'hp': -0.27, 'curl': 1.0, 'ease': 'inOut'}]
WIFEF = {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}
st.shot('S11', 'grassland', setOpts=GRASS, actors=[act('femme', FM, RYFM, 'stand', 'neutral', keys=[k(0.0, look=UP11, lookDur=0.0), k(0.0, toon={'face': WIFEF}, toonDur=0.0), *life(0.1, D11, WIFEF, blinks=[1.2])])],
        props=[P('stade11', 'chifStadium', pos=[0, 0, 0], opts={**STAD, 'cheer': 0.9, 'standAt': HYMN11, 'heartAt': r(HYMN11 + 0.35)}), *PITCH_TABLE(11), APRON('tablier11', 'femme'),
               P('montagne11', 'chifBagHeap', pos=HEAP11, opts={'h': 46, 'r': 30, 'bag': 3.2, 'gulls': 9, 'gullS': 4.0, 'gullR': 20, 'gullH': 6}),
               P('robot11', 'chifRobot', pos=RBS, ry=RYRS, opts={'base': 'tracks', 'path': PATH11})],
        cams=[C11])
st.cue('rain', 'S11', 0.0, 0.14, HYMN11); st.cue('sfx:fanfare', 'S11', HYMN11, 0.35); st.cue('sfx:choir', 'S11', r(HYMN11 + 0.3), 0.4)

# 12: chi, fou, mi: the stadium split in two. Low: the arm pumps its fist three times, on chi, fou and mi, the ground jumping on each beat (the table
#     hops, dust puffs); cut to the air: on « mi » a crack runs across the pitch past the table, a round hole opens beside it, and the two halves of
#     the stadium slide apart on « s'est fendu », both crowds still cheering
D12 = st.dur('S12'); B12 = [W('S12', 'L12', 0), W('S12', 'L12', 1), W('S12', 'L12', 2)]; SPLIT12 = r(W('S12', 'L12', 5) - 0.1)
CUT12 = r(B12[2] + 0.28)
PATH12 = [{'t': 0.0, 'p': RS(UP11), 'hp': -0.25, 'curl': 1.0}]
for b in B12: PATH12 += [{'t': r(b - 0.2), 'p': RS(add(UP11, [0, 0.7, 0])), 'hp': -0.05, 'curl': 1.0, 'ease': 'out', 'st': 1.05}, {'t': b, 'p': RS(add(UP11, [0, -0.35, 0])), 'hp': -0.4, 'curl': 1.0, 'ease': 'in'}]
PATH12 += [{'t': r(B12[2] + 0.25), 'p': RS(UP11), 'hp': -0.25, 'curl': 1.0, 'ease': 'out'}, {'t': D12, 'p': RS(add(UP11, [0, 0.1, 0])), 'hp': -0.25, 'curl': 1.0, 'ease': 'inOut'}]
F12A = [-3.6, 1.05, 5.2]
F12A, L12A, LENS12A = FB('S12', F12A, {'fistUp': add(UP11, [0.4, 1.5, 0]), 'table': TBL, 'wife': add(FM, [0, 2.2, 0]), 'wifeF': FM, 'base': RBS}, top=0.12, bottom=0.74)
C12A = cam(0.0, F12A, add(F12A, [0.15, 0.05, -0.2]), L12A, L12A, lens=LENS12A)
F12B, T12B = [0.0, 70.0, 50.0], [0.0, 74.0, 54.0]
C12B = cam(CUT12, F12B, T12B, [0.0, 0, -3.0], [0.0, 0, -3.0], lens=58)
chkc('S12', C12B, {'table': TBL, 'standsN': [0, 9, -38], 'standsS': [0, 9, 38], 'endW': [-45, 9, 0], 'endE': [45, 9, 0], 'gapN': [0, 2, -36], 'gapS': [0, 2, 36]}, end=True)
TBLK12 = [k(b, to=[0, 0.12, 0], dur=0.07, ease='out') for b in B12] + [k(r(b + 0.07), to=[0, 0, 0], dur=0.08, ease='in') for b in B12]
WIFEK12 = [k(0.0, look=UP11, lookDur=0.0), k(0.0, toon={'face': WIFEF}, toonDur=0.0)] + [k(b, toon={'sq': [1.05, 0.94, 1.05], 'face': {**WIFEF, 'lid': 0.5}}, toonDur=0.03, keepPose=True) for b in B12] + [k(r(b + 0.1), toon={'sq': [1, 1, 1], 'face': WIFEF}, toonDur=0.1, keepPose=True) for b in B12]
st.shot('S12', 'grassland', setOpts=GRASS, actors=[act('femme', FM, RYFM, 'stand', 'neutral', keys=WIFEK12)],
        props=[P('stade12', 'chifStadium', pos=[0, 0, 0], opts={**STAD, 'cheer': 1.0, 'standAt': -1, 'jumps': B12, 'crackAt': r(B12[2] + 0.3), 'crackDur': 0.5, 'holeAt': r(B12[2] + 0.75), 'split': [[SPLIT12, 0], [r(SPLIT12 + 0.9), 6.0]]}),
               *PITCH_TABLE(12, keys=TBLK12), APRON('tablier12', 'femme'),
               P('robot12', 'chifRobot', pos=RBS, ry=RYRS, opts={'base': 'tracks', 'path': PATH12, 'hits': B12}),
               *[P(f'boum12_{i}', 'softDust', pos=[0.0, 0.05, 0.0], opts={'at': b, 'n': 8, 'size': 0.6, 'spread': 2.0, 'rise': 0.3, 'life': 0.6, 'color': '#C9BFA8', 'opacity': 0.6}) for i, b in enumerate(B12)]],
        cams=[C12A, cam(B12[0], F12A, add(F12A, [0.15, 0.05, -0.2]), L12A, L12A, lens=LENS12A, shake=0.04), cam(B12[1], F12A, add(F12A, [0.15, 0.05, -0.2]), L12A, L12A, lens=LENS12A, shake=0.05), C12B])
for b in B12: st.cue('thud', 'S12', b, 0.55)
st.cue('thunder', 'S12', r(B12[2] + 0.3), 0.5); st.cue('sfx:crunch', 'S12', SPLIT12, 0.45); st.cue('rain', 'S12', CUT12, 0.16, r(D12 - CUT12))

# 13: the hand played rock. Low and close by the table, looking up: the fist hangs high a beat, trembling, then comes down (smear) and stops above
#     the table with a squash: a clean dark fist silhouette against the sky
D13 = st.dur('S13'); ROCK13 = r(W('S13', 'L13', 4) - 0.04)
HIGH13 = [0.5, 6.4, -0.1]; LOW13 = [0.2, 2.9, -0.05]
PATH13 = [{'t': 0.0, 'p': RS(HIGH13), 'hp': -0.6, 'curl': 1.0, 'st': 1.1}, {'t': r(ROCK13 - 0.28), 'p': RS(add(HIGH13, [0, 0.15, 0])), 'hp': -0.55, 'curl': 1.0, 'st': 1.12, 'ease': 'out'},
          {'t': ROCK13, 'p': RS(LOW13), 'hp': -0.75, 'curl': 1.0, 'st': 1.0, 'ease': 'in'}, {'t': r(ROCK13 + 0.12), 'p': RS(add(LOW13, [0, 0.1, 0])), 'hp': -0.72, 'curl': 1.0, 'ease': 'out'},
          {'t': D13, 'p': RS(add(LOW13, [0, 0.06, 0])), 'hp': -0.74, 'curl': 1.0, 'ease': 'inOut'}]
F13 = [-1.7, 0.7, 3.1]
_u, _v, _w = FB('S13', F13, {'fistLow': add(LOW13, [-0.5, -0.5, 0]), 'fistLowR': add(LOW13, [0.7, 0.4, 0]), 'fistHigh': add(HIGH13, [-0.3, 0.6, 0]), 'tableTop': [0.0, 0.76, 0.0]}, top=0.12, bottom=0.74)
L13, LENS13 = [0.1, 3.0, -0.1], 56
C13 = cam(0.0, F13, add(F13, [0.1, -0.03, -0.12]), L13, L13, lens=LENS13)
st.shot('S13', 'grassland', setOpts=GRASS, actors=[act('femme', FM, RYFM, 'stand', 'neutral', keys=[k(0.0, look=LOW13, lookDur=0.0), k(0.0, toon={'face': WIFEF}, toonDur=0.0)])],
        props=[P('stade13', 'chifStadium', pos=[0, 0, 0], opts={**STAD, 'cheer': 0.8, 'standAt': -1, 'crackAt': -1, 'holeAt': -1, 'split': [[0, 6.0]]}), *PITCH_TABLE(13), APRON('tablier13', 'femme'),
               P('robot13', 'chifRobot', pos=RBS, ry=RYRS, opts={'base': 'tracks', 'path': PATH13, 'hits': [ROCK13], 'smear': [[r(ROCK13 - 0.12), r(ROCK13 + 0.01)]]})],
        cams=[C13, cam(ROCK13, F13, add(F13, [0.1, -0.03, -0.12]), L13, L13, lens=LENS13, shake=0.03)])
st.cue('whoosh', 'S13', r(ROCK13 - 0.14), 0.3, 0.2, 300, 1500); st.cue('clang', 'S13', ROCK13, 0.35)

# 14: his wife played well. Close: she holds out her small mitten curled into a hollow ring, big and centred above the captions, her face behind
#     it; cut higher: a stone rim rises round the hole at her feet, the fist misses the table and plunges into the well, its arm stretching after it;
#     a distant splash comes up (PERDU, her head kept under the card)
D14 = st.dur('S14'); WELL14 = r(W('S14', 'L14', 4) - 0.1); CUT14 = r(WELL14 + 0.1)
HOLE = STAD['hole']; HW = [HOLE[0], 0, HOLE[1]]
RIM14 = r(CUT14 - 0.05); DROP14 = r(CUT14 + 0.12); IN14 = r(DROP14 + 0.2); SPL14 = r(IN14 + 0.18)
RYFW = 50
EW14 = off(FM, RYFW, 0.3, -0.14, 1.42); RYEW = RYFW
RING14 = hand_tip(EW14, RYEW, 1.7, 0.16, tilt=-0.15, ahead=0.05)
F14A = off(FM, RYFW, 2.35, 0.1, 1.72)
L14A = [r((RING14[0] + FM[0]) / 2), 1.7, r((RING14[2] + FM[2]) / 2)]
C14A = cam(0.0, F14A, off(FM, RYFW, 2.2, 0.1, 1.72), L14A, L14A, lens=38)
chkc('S14', C14A, {'ring': add(RING14, [0, 0.12, 0]), 'face': add(FM, [0, 1.95, 0]), 'headTop': add(FM, [0, 2.3, 0])})
PATH14 = [{'t': 0.0, 'p': RS(add(LOW13, [0, 0.06, 0])), 'hp': -0.74, 'curl': 1.0}, {'t': DROP14, 'p': RS(add(LOW13, [0, 0.3, 0])), 'hp': -0.7, 'curl': 1.0, 'ease': 'inOut'},
          {'t': IN14, 'p': RS([HOLE[0] + 0.25, 0.6, HOLE[1]]), 'hp': -1.4, 'curl': 1.0, 'st': 1.25, 'ease': 'in'}, {'t': r(IN14 + 0.2), 'p': RS([HOLE[0] + 0.15, -2.2, HOLE[1]]), 'hp': -1.5, 'curl': 1.0, 'st': 1.35, 'ease': 'in'},
          {'t': D14, 'p': RS([HOLE[0] + 0.15, -2.3, HOLE[1]]), 'hp': -1.5, 'curl': 1.0, 'st': 1.35, 'ease': 'linear'}]
F14B = [-4.6, 3.2, 2.2]
F14B, L14B, LENS14B = FB('S14', F14B, {'rimNear': add(HW, [0, 0, 0.9]), 'rimFar': add(HW, [0, 0.5, -0.9]), 'wifeHead': add(FM, [0, 2.3, 0]), 'tableTop': [0.4, 0.76, 0.0], 'fistTop': add(LOW13, [0, 0.8, 0])}, top=0.26, bottom=0.74)
C14B = cam(CUT14, F14B, add(F14B, [0.0, -0.1, -0.15]), L14B, add(L14B, [0, -0.15, 0]), lens=LENS14B)
chkc('S14', C14B, {'well': HW, 'wifeHead': add(FM, [0, 2.32, 0])})
RINGF = {'lid': 0.15, 'mouth': 'smile', 'brow': 0.5}
WIFEK14 = [k(0.0, look='camera', lookDur=0.0), k(0.0, toon={'face': {**WIFEF, 'lid': 0.3}, 'reach': {'L': R5(EW14, 1, 0.0)}, 'scl': {'handL': HIDE}}, toonDur=0.0),
           k(r(WELL14 - 0.1), toon={'face': RINGF, 'reach': {'L': R5(add(EW14, [0, 0.05, 0]), 1, 0.0)}, 'scl': {'handL': HIDE}, 'sq': [0.98, 1.03, 0.98]}, toonDur=0.1),
           k(CUT14, look=HW, lookDur=0.12), k(CUT14, toon={'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.3, 'gy': 0.6}, 'reach': {'L': R5(add(EW14, [0, 0.05, 0]), 1, 0.0)}, 'scl': {'handL': HIDE}}, toonDur=0.1)]
st.shot('S14', 'grassland', setOpts=GRASS, actors=[act('femme', FM, RYFW, 'stand', 'neutral', keys=WIFEK14)],
        props=[P('stade14', 'chifStadium', pos=[0, 0, 0], opts={**STAD, 'cheer': 0.8, 'standAt': -1, 'crackAt': -1, 'holeAt': -1, 'rimAt': RIM14, 'splashAt': SPL14, 'split': [[0, 6.0]]}), *PITCH_TABLE(14), APRON('tablier14', 'femme'),
               HAND('puits14', EW14, RYEW, s=1.7, sleeve=0.16, side='L', skin='#EBC29C', sleeveColor='#5E8C7A', modes=[[-1, 'rock'], [r(WELL14 - 0.08), 'well']], tilt=-0.2),
               P('robot14', 'chifRobot', pos=RBS, ry=RYRS, opts={'base': 'tracks', 'path': PATH14, 'smear': [[DROP14, IN14]]})],
        cams=[C14A, C14B])
st.card('S14', 'PERDU', at=r(CUT14 + 0.2))
st.cue('sfx:pop', 'S14', r(WELL14 - 0.08), 0.35); st.cue('sfx:slideDown', 'S14', DROP14, 0.35); st.cue('sfx:splash', 'S14', SPL14, 0.3)

# 15: she has trained on him for thirty years. In the stands (the -X half, slid away), among cheering fans, he slowly lowers his clenched fist from
#     his chest to his waist and looks at it, deadpan; his two neighbours cheer
D15 = st.dur('S15')
SPL = 6.0
HS15 = [r(-8.0 - SPL), 1.2 + 2 * 0.7, 23.6]
RYS15 = yaw(HS15, [-SPL, 0, 0]) - 12
NB15 = [off(HS15, RYS15, 0.0, -0.85, 0.0), off(HS15, RYS15, 0.0, 0.85, 0.0)]
EH15A = off(HS15, RYS15, 0.32, 0.08, 1.32); EH15B = off(HS15, RYS15, 0.3, 0.1, 0.95)
F15 = off(HS15, RYS15, 2.9, 0.3, 1.55)
F15, L15, LENS15 = FB('S15', F15, {'head': add(HS15, [0, 2.32, 0]), 'fist': add(EH15A, [0, 0.35, 0]), 'fistLow': EH15B, 'nb1': add(NB15[0], [0, 2.2, 0]), 'nb2': add(NB15[1], [0, 2.2, 0])}, top=0.15, bottom=0.74, lenses=range(30, 56))
C15 = cam(0.0, F15, off(HS15, RYS15, 2.6, 0.25, 1.45), L15, add(L15, [0, -0.08, 0]), lens=LENS15, ease='inOut')
CHEER = lambda p, ry, ph: [k(0.0, look=[-SPL, 2, 0], lookDur=0.0), *[k(r(ph + 0.22 * i), toon={'reach': {'R': R5(off(p, ry, 0.15, -0.35, 2.35 if i % 2 == 0 else 2.05), 1, 0.05), 'L': R5(off(p, ry, 0.15, 0.35, 2.05 if i % 2 == 0 else 2.35), 1, 0.05)}, 'face': {'lid': 0.0, 'mouth': 'O', 'jaw': 0.4, 'brow': 0.8}, 'sq': [1.0, 1.03 if i % 2 else 0.98, 1.0]}, toonDur=0.18, toonEase='inOut') for i in range(8)]]
HEROK15 = [k(0.0, look='camera', lookDur=0.0), k(0.0, toon={'reach': {'R': R5(EH15A, 1, 0.0)}, 'scl': {'handR': HIDE}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.0),
           k(0.3, toon={'reach': {'R': R5(EH15B, 1, 0.0)}, 'scl': {'handR': HIDE}, 'face': {'lid': 0.45, 'mouth': 'line', 'brow': -0.1}}, toonDur=0.8, toonEase='inOut'),
           k(0.55, look=EH15B, lookDur=0.35), k(0.9, toon={'face': {'lid': 0.35, 'mouth': 'line', 'brow': 0.2, 'gy': 0.5}}, toonDur=0.15, keepPose=True)]
st.shot('S15', 'grassland', setOpts=GRASS, actors=[act('mec', HS15, RYS15, 'stand', 'neutral', keys=HEROK15),
        act('supporter1', NB15[0], RYS15, 'stand', 'neutral', keys=CHEER(NB15[0], RYS15, 0.0)), act('supporter2', NB15[1], RYS15, 'stand', 'neutral', keys=CHEER(NB15[1], RYS15, 0.11))],
        props=[P('stade15', 'chifStadium', pos=[0, 0, 0], opts={**STAD, 'cheer': 1.0, 'standAt': -1, 'crackAt': -1, 'holeAt': -1, 'rimAt': -1, 'split': [[0, SPL]], 'clear': [[HS15[0] + SPL, HS15[2], 2.0]]}),
               HAND('poing15', EH15A, RYS15 + 20, s=1.35, sleeve=0.18, mode='rock', tiltK=[[0.3, -0.9], [1.1, -0.5]], keys=[k(0.3, to=EH15B, dur=0.8, ease='inOut')])],
        cams=[C15])
st.cue('rain', 'S15', 0.0, 0.16, D15)

# 15b: the insert: the kitchen again, closer, his fist under her flat hand, which pats it twice
D15b = st.dur('S15b')
F15b = [0.3, 1.78, 0.85]; L15b = [0.3, 1.2, -1.5]
C15b = cam(0.0, F15b, add(F15b, [0, -0.01, -0.06]), L15b, L15b, lens=42)
chkc('S15b', C15b, {'fist': FIST1, 'onFist': ONFIST1, 'binTop': add(BIN1, [0, 1.1, 0])})
st.shot('S15b', 'kitchenDay', setOpts=KIT, actors=[
        act('mec', HK, RYH, 'sit', 'neutral', keys=[k(0.0, look=FIST1, lookDur=0.0), k(0.0, toon={'reach': {'R': R5(EH1, 1, 0.0)}, **HEROHAND(), 'hip': 0, 'face': {'lid': 0.4, 'mouth': 'line'}}, toonDur=0.0)]),
        act('femme', FK, RYF, 'sit', 'neutral', keys=[k(0.0, look=FIST1, lookDur=0.0), k(0.0, toon={'reach': {'L': R5(EF1B, 1, 0.0)}, **WIFEHAND(), 'hip': 0, 'face': SMUG}, toonDur=0.0)])],
        props=[*KITCHEN_PROPS('15b', lvl=0), HANDH('mainH15b', mode='rock', tilt=0.06),
               HANDF('mainF15b', e=EF1B, mode='paper', tiltK=[[0.0, 0.06], [0.1, -0.08], [0.18, 0.06], [0.3, -0.08], [0.38, 0.06]])],
        cams=[C15b])
st.cue('sfx:paper', 'S15b', 0.1, 0.18); st.cue('sfx:paper', 'S15b', 0.3, 0.18)

# ============================== his street again: the bags taller than the house
HEAP16 = [3.4, 0, -3.6]
RBT16A, RBT16B = [-9.0, 0, 1.2], [-2.6, 0, 1.4]; RYB16 = 75
# 16: the loser had to take out the bin. His street: the mountain of bags beside his house, taller than its roof, gulls on top, flies; the
#     dripping robot rolls in on its tracks and stops in front of it; a quick tilt up the heap to the gulls (under a second)
D16 = st.dur('S16'); STOP16 = 0.95; TILT16 = r(W('S16', 'L16', 5) - 0.25)
PATH16 = [{'t': 0.0, 'p': [0, 2.4, 2.6], 'hp': -0.5, 'curl': 0.8}, {'t': D16, 'p': [0, 2.5, 2.6], 'hp': -0.45, 'curl': 0.8, 'ease': 'inOut'}]
F16 = [-1.2, 1.4, 14.5]
L16A = [-3.5, 2.2, 0.5]
C16A = cam(0.0, F16, add(F16, [0.2, 0, -0.2]), L16A, [-2.4, 2.4, 0.5], lens=44, ease='out')
L16B, LENS16B = FC('S16', F16, {'heapTop': add(HEAP16, [0, 11.5, 0]), 'gulls': add(HEAP16, [0, 14.5, 0]), 'roof': [0, 8.2, -6.6]}, top=0.08, bottom=0.6, lenses=range(36, 56))
C16B = glide([cam(TILT16, F16, add(F16, [0.0, 0.1, -0.1]), L16B, L16B, lens=LENS16B, ease='inOut')], 0.42)
chkc('S16', C16A, {'robotStop': add(RBT16B, [0, 3.0, 0]), 'robotStopF': RBT16B, 'heapFoot': add(HEAP16, [-6, 0, 3])})
chkc('S16', C16B, {'heapTop': add(HEAP16, [0, 11.5, 0]), 'roof': [0, 8.2, -6.6]})
st.shot('S16', 'pavillon', setOpts=STREET, actors=[],
        props=[P('maison16', 'chifHouse', pos=HOUSE), P('montagne16', 'chifBagHeap', pos=HEAP16, opts={'h': 11.5, 'r': 6.5, 'bag': 0.9, 'gulls': 5, 'gullS': 1.3, 'gullR': 4.5, 'gullH': 2.0, 'perch': 2, 'flies': 10}),
               P('robot16', 'chifRobot', pos=RBT16A, ry=RYB16, opts={'base': 'tracks', 'path': PATH16, 'drip': True}, keys=[k(0.0, to=RBT16B, dur=STOP16, ease='out')])],
        cams=[C16A, C16B])
st.cue('engine', 'S16', 0.0, 0.3); st.cue('sfx:brake', 'S16', r(STOP16 - 0.2), 0.2); st.cue('sfx:squeak', 'S16', r(TILT16 + 0.3), 0.25)

# 17: the hand contested: the well does not count. Close on the robot in front of the heap: the dripping hand turns to us, flat, and on « contesté »
#     draws the referee's rectangle in the air, the same glowing trail; behind it one more bag rolls down the heap; it holds, deadpan, the trail
#     pulsing, drips falling, the gulls circling
D17 = st.dur('S17'); RECT17 = r(W('S17', 'L17', 3) - 0.1); RDUR17 = 1.1; ROLL17 = r(W('S17', 'L17', 7) - 0.3)
RB17 = RBT16B; RY17 = 40
F17 = [-0.6, 2.7, 10.0]
FACE17 = [-0.6, 3.4, 2.4]                                                  # where the hand comes to face us: in front of the arm, between it and the camera
def R17(w): return tol(RB17, RY17, w)
RC17 = [-0.5, 3.45, 2.6]; RW17, RH17 = 1.9, 1.2
RR17 = right(yaw(RC17, F17))
RECT17P = [[r(RC17[0] + RR17[0] * sx * RW17 / 2), r(RC17[1] + sy * RH17 / 2), r(RC17[2] + RR17[2] * sx * RW17 / 2)] for sx, sy in [(1, 1), (-1, 1), (-1, -1), (1, -1), (1, 1)]]
seg17 = [math.dist(RECT17P[i], RECT17P[i + 1]) for i in range(4)]; TL17 = sum(seg17)
CORN17 = [RECT17] + [r(RECT17 + RDUR17 * sum(seg17[:i + 1]) / TL17) for i in range(4)]
YAW17 = math.radians(yaw(RB17, F17) - RY17)
PATH17 = [{'t': 0.0, 'p': R17([-1.4, 2.6, 2.4]), 'hp': -0.45, 'curl': 0.8}, {'t': 0.45, 'p': R17(RECT17P[0]), 'hp': 0.25, 'curl': 0.0, 'roll': 0.0, 'ease': 'inOut'}]
for i in range(4): PATH17.append({'t': CORN17[i + 1], 'p': R17(RECT17P[i + 1]), 'hp': 0.25, 'curl': 0.0, 'ease': 'linear'})
PATH17 += [{'t': r(CORN17[-1] + 0.35), 'p': R17(add(RC17, [0.1, -0.1, 0.2])), 'hp': 0.3, 'curl': 0.0, 'ease': 'inOut'}, {'t': D17, 'p': R17(add(RC17, [0.12, -0.05, 0.2])), 'hp': 0.28, 'curl': 0.0, 'ease': 'inOut'}]
F17, L17, LENS17 = FB('S17', F17, {'rectTL': add(RECT17P[1], [0, 0.6, 0]), 'rectBR': add(RECT17P[3], [0, -0.3, 0]), 'rectR': RECT17P[0], 'heapTop': add(HEAP16, [0, 8.0, 0]), 'base': RB17}, top=0.12, bottom=0.74, lenses=range(34, 58))
C17 = cam(0.0, F17, add(F17, [0.0, 0.0, -0.5]), L17, L17, lens=LENS17, ease='inOut')
chkc('S17', C17, {'rollStart': add(HEAP16, [0, 9.9, 0.8]), 'rollEnd': add(HEAP16, [0, 0.5, 7.0]), 'heapTop': add(HEAP16, [0, 11.5, 0])})
chkc('S17', C17, {'rectL': RECT17P[1], 'rectR': RECT17P[0], 'rectLow': RECT17P[2]}, end=True)
st.shot('S17', 'pavillon', setOpts=STREET, actors=[],
        props=[P('maison17', 'chifHouse', pos=HOUSE), P('montagne17', 'chifBagHeap', pos=HEAP16, opts={'h': 11.5, 'r': 6.5, 'bag': 0.9, 'gulls': 5, 'gullS': 1.3, 'gullR': 4.5, 'gullH': 2.0, 'perch': 2, 'flies': 10, 'rollAt': ROLL17, 'rollDur': 1.2}),
               P('robot17', 'chifRobot', pos=RB17, ry=RY17, opts={'base': 'tracks', 'path': PATH17, 'drip': True, 'trail': {'t0': RECT17, 't1': CORN17[-1], 'color': '#FFE27A'}})],
        cams=[C17])
st.cue('sfx:rattleShort', 'S17', 0.1, 0.2); st.cue('sfx:zip', 'S17', RECT17, 0.25); st.cue('sfx:bell', 'S17', CORN17[-1], 0.2); st.cue('thud', 'S17', r(ROLL17 + 1.15), 0.25); st.cue('sfx:squeak', 'S17', 3.2, 0.2)

print('\n'.join(CHECKS))

TOON = {'breathe': 1.7, 'holdLife': 1.6}
MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': TOON}
FEMME = {'preset': 'femme', 'seed': 961, 'glasses': False, 'build': {'width': 0.9, 'headWidth': 1.25, 'height': 0.94}, 'toon': TOON}
ARB = {'preset': 'boss', 'outfit': 'suit', 'suit': '#2E3138', 'pants': '#2A2C32', 'shirt': '#2E3138', 'lapel': '#454952', 'tie': '#2E3138', 'cuff': '#2E3138', 'hat': 'none', 'glasses': False, 'facial': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
SAV = {'preset': 'doctor', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
WORK = {'preset': 'worker', 'hat': 'none', 'hair': 'bald', 'facial': 'none', 'glasses': False, 'build': {'width': 1.05, 'headWidth': 1.2}, 'toon': EX}
FAN = {'preset': 'boss', 'outfit': 'suit', 'hat': 'none', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
st.write("Le chifoumi", rig='toon', fingers=False, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'femme': FEMME,
    'arbitre1': {**ARB, 'seed': 962, 'hair': 'crew'}, 'arbitre2': {**ARB, 'seed': 963, 'facial': 'mustache', 'hair': 'receding'}, 'arbitre3': {**ARB, 'seed': 964, 'hair': 'slick', 'skin': '#8A5A3A', 'faceRim': True},
    'arbitreT': {**ARB, 'seed': 965, 'hair': 'buzz', 'suit': '#1F2126', 'shirt': '#1F2126'},
    'savant1': {**SAV, 'seed': 966}, 'savant2': {**SAV, 'seed': 967, 'hair': 'bun', 'lipstick': True, 'glasses': False},
    'officiel7': {'preset': 'politique', 'seed': 968, 'suit': '#6E7480', 'lapel': '#5A606C', 'tie': '#7A2E3A', 'hairColor': '#8A8A8A', 'glasses': True, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
    'soudeur1': {**WORK, 'seed': 969}, 'soudeur2': {**WORK, 'seed': 970},
    'ouvrier1': {**WORK, 'seed': 971, 'hat': 'hardhat2', 'hatColor': '#E8E4DA', 'suit': '#8A9AAA', 'bandColor': '#C9C2B2'}, 'ouvrier2': {**WORK, 'seed': 972, 'hat': 'hardhat2', 'hatColor': '#E8E4DA', 'suit': '#8A9AAA', 'facial': 'mustache', 'bandColor': '#C9C2B2'},
    'officiel10': {'preset': 'politique', 'seed': 973, 'suit': '#3A5A8C', 'lapel': '#2E4A76', 'tie': '#E2E6EC', 'shirt': '#F2F2EE', 'hairColor': '#5A3A28', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX},
    'president': {'preset': 'politique', 'seed': 974, 'suit': '#2A2D33', 'lapel': '#2A2D33', 'tie': '#2C3E5C', 'hairColor': '#BDBDBD', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.08}, 'toon': EX},
    'supporter1': {**FAN, 'seed': 975, 'suit': '#E0413A', 'shirt': '#F4F4F0', 'lapel': '#B8302A', 'tie': '#F4F4F0', 'hair': 'crew'}, 'supporter2': {**FAN, 'seed': 976, 'suit': '#2F62B5', 'shirt': '#F2C230', 'lapel': '#244B86', 'tie': '#F2C230', 'facial': 'mustache', 'hair': 'receding'},
})
