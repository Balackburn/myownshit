#!/usr/bin/env python3
"""Le grincement (story 98, cycle 52; a hook, an institutional escalation, a reversal, a dry last line).
This man's door squeaks; for the State it is a language. The neighbour had complained about the noise. Three linguists are formal: a language
spoken by a single door. Threatened, so oiling it is forbidden; the gendarmes seized his oil can. Closing the door would cut it off: he lives
with it open and heats the street; at night it talks in its sleep. The whole country learns the squeak, compulsory at the bac; the neighbour
failed three times and moved out. The president gave his New Year wishes squeaking. Ten years later the dictionary: a thousand pages, one word,
meaning « de l'huile ». So the president wished the whole country oil. The oil can is still under seal.
Running gags: the hero's door squeaks with one big sprite (three thick saturated arcs, at least a tenth of the frame, wobbling off the hinge) and
the squeak sound in every shot where it is visible (S01, S02, S03, S04, S06, S07, S10; the bedroom door in S08, the little doors in S09, S11, S15
squeak the same way); from S05 on, the oil can stays in its clear sealed bag and is within reach of whoever speaks the language in every
institutional shot (the invigilator's desk S09, the president's desk S11, alone on the shelf S16), nobody touches it; the neighbour who complained
about the noise (S02, pyjamas and nightcap) is the one who fails the exam in it (S10, still in his nightcap).
Staging: low beside the hinge of his teal front door: he pulls it open, a big squeak pops off the hinge, a red oil can in his other mitten, raised
toward the hinge on « l'État ». Over the low fence the neighbour in pyjamas and nightcap leans out of his window holding up a complaint form (a door
and three arcs, no words); behind him the door swings and squeaks. Three linguists in tweed kneel in a row on the path, a boom at the hinge,
headphones, a clipboard; the door squeaks, they lean in; closer, the boom man nods (LANGUE). An official in a violet-and-gold sash drives the last
screw of a bronze plaque on the door (a crossed-out oil drop, no words), then cuts a ribbon; the door squeaks as it falls. On the doorstep two
gendarmes take the can from his mitten and drop it in a clear bag that seals; his empty mitten stays up. He pushes the door shut; a gendarme stops
it with one flat mitten and slowly shakes his head; it swings back open, squeaking. Snow: he sits on his sofa in hat and scarf behind the wide-open
door, snow blowing in; two passers-by warm their mittens at the doorway, steam rising, a dark wet patch on the snowy path. Night: in bed under the
duvet in his wool hat, eyes wide, the bedroom door swings in the draught and squeaks twice; he pulls the duvet up. The exam hall: rows of grown-ups
behind little doors on stands, the invigilator beats and they all squeak at once; the sealed can on her desk. The neighbour, nightcap on, carries a
box to a moving van, his exam sheet taped on it (BAC, three red 0/20); behind him the open door squeaks in the wind. The president at his desk in a
formal office (no flag, no emblem) swings a little ornate door gravely at us, mouthing each squeak; the sealed can on the corner of the desk. In a
library hall the three linguists, white beards to the belt, set a huge leather dictionary on a lectern; a few people applaud. Top-down on the open
book: blank pages flip past and stop on IIIIIK; tighter, « de l'huile » and an oil drop write in under it (TRADUIT). A family on the sofa watches the
replay: inside the television the little president swings his door and a speech bubble with an oil drop pops out; they nod slowly. The evidence
shelf: the can alone in its sealed bag under a bare bulb that swings; far off, a squeak.
Natural look; cycle 52: props_grincement.js (grinSqueak, grinFacade, grinOilCan, grinBag, grinPlaque, grinMiniDoor, grinForm, grinExamSheet,
grinBook, grinLectern, grinTV, grinBubble, grinSnowStream, grinPatch, grinDuvet, grinScarf, grinOfficeWall, grinDesk, grinBoard, grinBookcase,
grinBedLamp); reused: nightCap (props_interrupteur), boomMic (props_feu), chifHeadset (props_chifoumi), clipboardProp, sofaProp, fence, chair, table
(props.js), ribbonCut and scissors (props_rambarde), screwdriver (props_porte), kepi (props_conseiller), longBeard (props_tournante), chvBagShelf
(props_cheveu), cellBulb (props_table), softWisp (props_barbecue), snowfall (props_canicule), deliveryVan (props_parcmetre), tacheGround and tacheBox
(props_tache); sets grassland, chambre, classroom, livingRoom, whiteVoid.
Lessons applied from the start: `lens` is the vertical field; characters are about 2.3 m tall with the box head; faces and key props above the
caption band (0.77-0.83), heads below the card band (0.07-0.18) when a card stamps; every camera checked with project() (CHECKS); every extra cast
member has a preset; word timings from timeline.json through st.at (words counted from 0, the word printed beside its time); the payoff shots
(S13, S14, S16) get their own tight cameras; the exam crowd is checked candidate by candidate; mitten hands everywhere (no fingers); no raised arm
held still and no hand at the face (the headphone hand stays at the ear cup below the eye line and moves); one take per mechanism (the linguists
lean in, the official's chest-out, the gendarme's slow head shake, the hero's deadpan look at his empty mitten, the wide eyes in bed, the family's
slow nod); squash, stretch and hang on the State's gags (the plaque's last screw, the ribbon's snip, the bag that seals, the president's door);
moving holds (breathing, blinks, the bulb swinging, snow, steam); the bleached bag film is a cool white; the can falls into the bag with u² keys;
no real flag, emblem, insignia or organisation (a plain sash in violet and gold, plain kepis, a plain formal office, an invented exam sheet);
French only on screen; nobody hurt."""
from story_kit import *
import math

st = Story('grincement', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0), ('S08', 'L08', 0),
         ('S09', 'L09', 0), ('S10', 'L10', 0), ('S11', 'L11', 0), ('S12', 'L12', 0), ('S13', 'L13', 0), ('S14', 'L14', 0), ('S15', 'L15', 0), ('S16', 'L16', 0)])

PI = math.pi
def r(v, n=3): return round(v, n)
def add(a, b): return [r(a[i] + b[i]) for i in range(3)]
def sub(a, b): return [r(a[i] - b[i]) for i in range(3)]
def lerp3(a, b, u): return [r(a[i] + (b[i] - a[i]) * u) for i in range(3)]
def yaw(src, dst): return r(math.degrees(math.atan2(dst[0] - src[0], dst[2] - src[2])), 1)
def fwd(ry): return [math.sin(math.radians(ry)), 0.0, math.cos(math.radians(ry))]
def right(ry): return [-math.cos(math.radians(ry)), 0.0, math.sin(math.radians(ry))]
def off(p, ry, f=0.0, s=0.0, y=0.0): F, R = fwd(ry), right(ry); return [r(p[0] + F[0] * f + R[0] * s), r(p[1] + y), r(p[2] + F[2] * f + R[2] * s)]
CHECKS = []
def chk(sid, frm, look, lens, pts):
    CHECKS.append(f"{sid}: " + ' | '.join(f"{n} {project(frm, look, lens, p)}" for n, p in pts.items()))
def chkc(sid, c, pts, end=False):
    frm, look = (c.get('to') or c['from'], c.get('lookAt2') or c['lookAt']) if end else (c['from'], c['lookAt'])
    chk(sid + ('>' if end else ''), frm, look, c['lens'], pts)
def W(sid, lid, i):
    # (cycle 51) word timings from timeline.json: st.at counts the words from 0; the word is printed beside its time
    t = st.at(sid, lid, i); CHECKS.append(f"{sid} « {st.L[lid]['words'][i]['w']} » at {t}"); return t

EX = {'holdLife': 2.5, 'shift': 2.4, 'breathe': 1.8}
DEAD = {'lid': 0.4, 'mouth': 'line'}
def blink(t, face=None, keep=None): return [k(t, toon={**(keep or {}), 'face': {**(face or DEAD), 'lid': 1.0}}, toonDur=0.05), k(r(t + 0.1), toon={**(keep or {}), 'face': face or DEAD}, toonDur=0.06)]
def R5(p, w=1, s=0.04): return [*p, w, s]
HIDE = [0.01, 0.01, 0.01]
def life(t0, t1, face, keep=None, ph=0.0, blinks=(), period=0.9, amp=0.013):
    # a moving hold: slow breathing keys that carry the face and the hands (a toon key is a whole state), clear of the blinks
    out, bl, t_, i = [], sorted(blinks), t0 + ph, 0
    while t_ < t1 - 0.1:
        if not any(-0.04 < t_ - b < 0.2 for b in bl):
            q = [r(1 - amp * 0.4, 4), r(1 + amp, 4), r(1 - amp * 0.4, 4)] if i % 2 == 0 else [r(1 + amp * 0.3, 4), r(1 - amp * 0.6, 4), r(1 + amp * 0.3, 4)]
            out.append(k(r(t_), toon={**(keep or {}), 'sq': q, 'face': face}, toonDur=r(period * 0.8), toonEase='inOut'))
        t_ += period / 2; i += 1
    for b in bl: out += blink(r(b), face, keep)
    return out

# the squeak: one big sprite at a hinge, always with its sound
def SQUEAK(sid, pid, pos, ts, size=0.8, side=1, amp=None, life_=0.72, gain=0.34, top=False):
    for t_ in ts: st.cue('sfx:squeak', sid, r(t_), gain)
    o = {'at': [r(t_) for t_ in ts], 'size': size, 'side': side, 'life': life_}
    if amp: o['amp'] = amp
    if top: o['onTop'] = True
    return P(pid, 'grinSqueak', pos=pos, face='camera', opts=o)
def BAG(pid, pos, keys=None, scale=None, **o):
    kw = {**({'keys': keys} if keys else {}), **({'scale': scale} if scale is not None else {})}
    return P(pid, 'grinBag', pos=pos, face='camera', faceFlat=True, opts=o, **kw)

# ============================== his street (grassland + painted ground). His house: the door's middle at x 0, z 0, the street toward +Z
HOUSE = [0.0, 0.0, 0.0]
DW, DH = 1.15, 2.6
HINGE = [r(DW / 2), 0.0, -0.06]                                          # the door is hinged on the right seen from the street: it opens inward
FLOOR_IN = 0.06                                                         # the hall floor inside
def door_pt(a, along, y, out=0.0):
    # a point on the leaf at opening a (rad), `along` metres from the hinge toward the free edge, `out` metres off its street face
    return [r(HINGE[0] - along * math.cos(a) - out * math.sin(a)), r(y), r(HINGE[2] - along * math.sin(a) + out * math.cos(a))]
def FACADE(pid, swing=None, open_=None, rattle=None, snow=False, light=3.2, ins=None, shut=True):
    d = {'w': DW, 'h': DH, 'color': '#1F6E7A', 'hinge': 'R', 'inside': {'light': light, **(ins or {})}}
    if swing: d['swing'] = swing
    if open_ is not None: d['open'] = open_
    if rattle: d['rattle'] = rattle
    return P(pid, 'grinFacade', pos=HOUSE, opts={'w': 4.7, 'x0': -1.9, 'wall': '#F2D58A', 'roof': '#B5402F', 'num': 7, 'door': d, 'snow': snow, 'box': 4.0,
                                                  'windows': [{'x': 1.9, 'y': 1.0, 'w': 1.0, 'h': 1.25, **({'shutters': '#2F7F8C'} if shut else {})}]})
# the neighbour's house stands forward on the left (its face at z 3.5, from x -5 to -0.9), the open window toward the street
NBP = [-2.95, 0.0, 3.5]
NWIN = [-1.5, 1.02, 3.5]
def NFACADE(pid, snow=False):
    return P(pid, 'grinFacade', pos=NBP, opts={'w': 4.1, 'x0': -2.05, 'wall': '#EFC7C7', 'roof': '#5E83C6', 'door': False, 'snow': snow, 'box': 3.0,
                                                'windows': [{'x': r(NWIN[0] - NBP[0]), 'y': NWIN[1], 'w': 1.05, 'h': 1.55, 'kind': 'open', 'd': 1.3}, {'x': -1.1, 'y': 1.0, 'w': 0.9, 'h': 1.1, 'shutters': '#2F62B5'}]})
def GROUND(pid, snow=False):
    pv, rd, ph = ('#E4E8EE', '#A3A8B0', '#DCE1E8') if snow else ('#D8CFB6', '#77777B', '#CFC6B4')
    return P(pid, 'tacheGround', pos=[0, 0, 0], opts={'rects': [[0, 4.6, 90, 2.2, pv], [0, 9.2, 90, 7.0, rd], [0, 1.85, 1.4, 3.3, ph], [0, 5.75, 90, 0.16, '#B9B2A2', -1.2]]})
def STREET(n, snow=False, nb=False):
    out = [GROUND(f'sol{n}', snow)]
    if nb: out += [NFACADE(f'voisins{n}', snow), P(f'cloture{n}', 'fence', pos=[-2.95, 0, 3.95], opts={'length': 4.0, 'height': 0.8, 'color': '#F4F4F0'})]
    return out
SET = {'grass': '#86BE5C'}
SNOWSET = {'grass': '#EEF2F6', 'sky': ['#AEBBC8', '#E2E7EC'], 'treeColors': ['#E8EEF2', '#F6F8FA', '#C9D3DC']}
HERO_IN = [-0.12, FLOOR_IN, -0.5]                                      # him in his doorway
def CAN(pid, who, hand='L', off_=(0.0, -0.06, -0.05), s=0.92, flip=False, keys=None):
    # the oil can held up in a mitten, turned to the camera, upright
    d = {'s': s}
    if flip: d['flip'] = True
    return P(pid, 'grinOilCan', on={'actor': who, 'hand': hand, 'offset': list(off_), 'face': 'camera', 'faceFlat': True}, opts=d, **({'keys': keys} if keys else {}))
# (round 1 fix) a rounded knit beanie with a turned-up cuff and a pompom (the engine's 'beanie' hat read as a fez)
BEANIE = lambda pid, who, col='#C8322A', w=0.34, d=0.26: P(pid, 'grinBeanie', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'color': col, 'w': w, 'd': d})
KEPI = lambda pid, who: P(pid, 'kepi', on={'actor': who, 'joint': 'head', 'offset': [0.0, 0.5, 0.0]}, opts={'w': 0.222, 'd': 0.17, 'color': '#1A2438', 'band': '#C9CDD3'})

for g_ in [('S01', 1.3, 'mec', 'door squeak'), ('S02', 0.9, 'voisin', 'complaint'), ('S05', 1.5, 'mec', 'empty mitten'), ('S06', 1.2, 'gendarme1', 'head shake'), ('S08', 1.0, 'mecHiver', 'eyes wide in bed'),
           ('S10', 1.6, 'voisin', 'the box and the sheet'), ('S11', 1.2, 'president', 'wishes')]:
    st.gag(*g_)

# 1: the hook. Low beside the hinge of his teal front door, outside: the door is ajar, his face in the gap; on « grince » he pulls it wide open
#    and the big squeak pops off the hinge with the sound; in his other mitten a red oil can; on « l'État » he raises it toward the hinge (the camera
#    slides in), a second squeak, a third on « langue »; he looks at the hinge, then at us
# (round 1 fix) low and tight on the hinge side of the panelled leaf, ajar: half his face peeks out of the narrow gap at its free edge (he leans to it);
#     a brace (the leaf eases back) and on « grince » he yanks it wide (the hinge and the whole sprite in frame, the sprite off the hinge toward the
#     doorway top, clear of his face): on the squeak his head shoots out toward the hinge on a long neck, thin and tall, held trembling, and snaps back
#     with an overshoot; two frames of dip before the can rises toward the hinge on « l'État » (the camera slides in); his eyes lead his head to the hinge
#     on « langue », then back to us. The window by the door has no shutters here (its slats read as a shutter panel beside the door)
D1 = st.dur('S01'); GR1 = r(W('S01', 'L01', 5) - 0.06); ETAT1 = W('S01', 'L01', 7); LANG1 = W('S01', 'L01', 10)
H1 = [-0.55, FLOOR_IN, -0.95]; RY1 = 17
A0 = 0.55
A1 = [[0.0, A0], [r(GR1 - 0.3), A0], [r(GR1 - 0.1), 0.47], [r(GR1 + 0.07), 1.42, 'lin'], [r(GR1 + 0.2), 1.27], [r(GR1 + 0.36), 1.36], [r(GR1 + 0.55), 1.33]]
KNOBI = lambda a: door_pt(a, DW - 0.16, 1.24, -0.08)
CANC1 = off(H1, RY1, 0.42, 0.2, 1.2)                                     # the can at his chest (his right mitten)
CANU1 = [0.05, 1.72, -0.55]                                             # raised toward the hinge
F1 = [0.6, 0.9, 2.8]; L1 = [-0.01, 1.7, -0.5]
C1 = cam(0.0, F1, add(F1, [-0.04, 0.0, -0.1]), L1, add(L1, [0, 0.02, 0]), lens=44, ease='inOut')
F1B = [0.45, 1.0, 2.4]; L1B = [0.05, 1.78, -0.5]
C1B = glide([cam(r(ETAT1 - 0.1), F1B, add(F1B, [-0.02, 0, -0.05]), L1B, L1B, lens=44, ease='out')], 0.3)
SQ1 = [0.575, 2.22, 0.05]
chkc('S01', C1, {'head': add(H1, [0, 2.05, 0]), 'headL': add(H1, [-0.16, 2.05, 0]), 'jamb': [-0.575, 1.9, 0.02], 'edgeAjar': door_pt(A0, DW, 1.9), 'top': add(H1, [0, 2.32, 0]), 'can': CANC1, 'hinge': SQ1, 'sqTip': add(SQ1, [-0.55, 0.2, 0]), 'edgeOpen': door_pt(1.35, DW, 1.3), 'doorTop': [0, 2.6, 0]})
chkc('S01', C1B, {'head': add(H1, [0, 2.05, 0]), 'top': add(H1, [0, 2.32, 0]), 'canUp': add(CANU1, [0.3, 0.3, 0]), 'hinge': SQ1, 'sqTip': add(SQ1, [-0.55, 0.2, 0]), 'chin': add(H1, [0, 1.8, 0])})
HF1 = {'lid': 0.35, 'mouth': 'line', 'brow': -0.1}
def HB1(kn=None, can=CANC1, lean=0.12, **x):
    d = {'reach': {'R': R5(can, 1, 0.0), **({'L': R5(kn, 1, 0.0)} if kn else {})}, 'hands': {'R': 'grip', 'L': 'grip' if kn else 'rest'}, 'bend': {'spine': [0.0, lean, 0, 1, None]}, 'hip': 0}
    for k_, v_ in x.items():
        if k_ == 'neck': d['bend'] = {**d['bend'], 'neck': v_}
        else: d[k_] = v_
    return d
TAKE1 = r(GR1 + 0.04)
HEAD1 = {**HB1(KNOBI(1.3), lean=0.0, neck=[0.05, -0.42, 0, 1.95, None]), 'sq': [0.93, 1.08, 0.93], 'scl': {'head': [0.84, 1.24, 1.0]}, 'face': {'lid': 0.0, 'eye': 0.55, 'mouth': 'o', 'brow': 1.0, 'gx': 0.6, 'noBlink': 1}}
HERO1 = [k(-0.4, look='camera'), k(0.0, toon={**HB1(KNOBI(A0)), 'face': HF1}, toonDur=0.0),
         *life(0.1, r(GR1 - 0.34), HF1, HB1(KNOBI(A0)), blinks=[0.42]),
         k(r(GR1 - 0.3), toon={**HB1(KNOBI(A0 - 0.02), lean=0.18), 'sq': [1.05, 0.94, 1.05], 'face': {**HF1, 'lid': 0.5, 'brow': -0.4}}, toonDur=0.15, toonEase='inOut'),
         k(r(GR1 - 0.1), toon={**HB1(KNOBI(0.47), lean=0.2), 'sq': [1.07, 0.92, 1.07], 'face': {**HF1, 'lid': 0.55, 'mouth': 'clench', 'brow': -0.5}}, toonDur=0.08),
         k(r(TAKE1 - 0.06), look=add(SQ1, [0, -0.1, 0]), lookDur=0.06),
         *beat(TAKE1, HEAD1, antic={**HB1(KNOBI(0.8), lean=0.05), 'sq': [1.04, 0.95, 1.04], 'scl': {'head': [1.08, 0.92, 1.0]}, 'face': {**HF1, 'lid': 0.4, 'brow': 0.2}}, hold=0.24,
               over={**HB1(lean=0.0, neck=[0.0, 0.1, 0, 0.85, None]), 'sq': [1.06, 0.95, 1.06], 'scl': {'head': [1.1, 0.9, 1.0]}, 'face': {**HF1, 'lid': 0.1, 'brow': 0.6}},
               settle={**HB1(lean=0.0), 'face': {**HF1, 'lid': 0.2, 'brow': 0.4}}, settle_f=5),
         k(r(TAKE1 + 0.42), look='camera', lookDur=0.12),
         *life(r(TAKE1 + 0.55), r(ETAT1 - 0.22), {**HF1, 'lid': 0.25, 'brow': 0.3}, HB1(lean=0.0)),
         k(r(ETAT1 - 0.2), toon={**HB1(add(CANC1, [0, -0.05, 0]), lean=0.0), 'sq': [1.06, 0.93, 1.06], 'face': {**HF1, 'lid': 0.4, 'brow': -0.2}}, toonDur=0.067),
         k(r(ETAT1 - 0.12), toon={**HB1(can=add(CANU1, [0.03, 0.05, 0]), lean=-0.05), 'sq': [0.96, 1.05, 0.96], 'face': {'lid': 0.2, 'mouth': 'line', 'brow': 0.45}}, toonDur=0.2, toonEase='out'),
         k(r(ETAT1 + 0.12), toon={**HB1(can=CANU1, lean=-0.03), 'sq': [1.0, 1.0, 1.0], 'face': {'lid': 0.25, 'mouth': 'line', 'brow': 0.4}}, toonDur=0.15, toonEase='inOut'),
         k(r(ETAT1 + 0.05), look=add(SQ1, [-0.1, -0.15, 0]), lookDur=0.12),
         k(r(ETAT1 + 0.5), look='camera', lookDur=0.12),
         k(r(LANG1 - 0.05), look=add(SQ1, [-0.1, -0.15, 0]), lookDur=0.14),
         k(r(LANG1 + 0.02), toon={**HB1(can=add(CANU1, [0.02, 0.03, 0]), lean=-0.03), 'face': {'lid': 0.15, 'mouth': 'line', 'brow': 0.6}}, toonDur=0.08),
         k(r(LANG1 + 0.25), look='camera', lookDur=0.14),
         *life(r(LANG1 + 0.3), D1, DEAD, HB1(can=CANU1, lean=-0.03), blinks=[r(D1 - 0.08)])]
st.shot('S01', 'grassland', setOpts=SET, actors=[act('mec', H1, RY1, 'stand', 'neutral', keys=HERO1)],
        props=[*STREET(1), FACADE('maison1', swing=A1, rattle=[[r(ETAT1 + 0.25), 0.05, 20, 4], [r(LANG1), 0.04, 20, 4]], shut=False), CAN('burette1', 'mec', hand='R', off_=(0.0, -0.05, 0.06), s=0.92),
               SQUEAK('S01', 'grince1', SQ1, [r(GR1 + 0.04), r(ETAT1 + 0.25), LANG1], size=0.5, side=-1, amp=[1.2, 0.9, 1.0], top=True)],
        cams=[C1, C1B])
st.cue('sfx:stretch', 'S01', r(TAKE1 + 0.02), 0.2)

# 2: the neighbour had complained. The neighbour's house stands forward on the left, a low fence before it: in pyjamas and a nightcap he leans out
#    of his open window and holds up a complaint form flat to us (a door and three arcs, no words), shaking it on « plainte »; behind him, down the
#    street, the hero's door swings and squeaks (a big sprite)
D2 = st.dur('S02'); PL2 = W('S02', 'L02', 4); BR2 = W('S02', 'L02', 6)
NB2 = [NWIN[0], 0.0, 3.16]; RY2 = 10
FORM2 = [-1.28, 1.24, 3.86]
F2 = [-0.67, 1.35, 7.2]; L2 = [-0.55, 1.25, 1.4]
HB2H = {'reach': {'L': R5(off(HERO_IN, 20, 0.42, -0.26, 1.18), 1, 0.0)}, 'hands': {'L': 'grip'}, 'hip': 0}
C2 = cam(0.0, F2, add(F2, [0.04, 0.0, -0.25]), L2, add(L2, [0.03, 0, 0]), lens=52, ease='inOut')
SQ2 = [0.575, 2.0, 0.08]
chkc('S02', C2, {'head': add(NB2, [0, 2.3, 0]), 'chin': add(NB2, [0, 1.8, 0]), 'formTop': add(FORM2, [0, 0.36, 0]), 'formBot': add(FORM2, [0, -0.36, 0]), 'doorL': [-0.575, 1.3, 0], 'hingeSq': SQ2, 'sqTip': add(SQ2, [0.7, 0.3, 0]), 'heroHead': add(HERO_IN, [0, 2.1, 0]), 'sill': NWIN, 'blockEdge': [-0.9, 1.5, 3.5]})
FB2 = lambda dy=0.0: {'reach': {'L': R5(add(FORM2, [0.22, -0.25 + dy, -0.03]), 1, 0.0), 'R': R5(add(FORM2, [-0.22, -0.25 + dy, -0.03]), 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'bend': {'spine': [0.3, 0, 0, 1, None]}, 'hip': 0}
ANG2 = {'expr': 'angry', 'exprW': 1.0, 'mouth': 'open', 'brow': -0.8}
ANG2b = {'expr': 'angry', 'exprW': 1.0, 'mouth': 'line', 'brow': -0.9}
SH2 = [0.15, 0.32, 0.5, r(PL2 - 0.05), r(PL2 + 0.12), r(PL2 + 0.3), r(BR2), r(BR2 + 0.2)]
VOIS2 = [k(-0.4, look='camera'), k(0.0, toon={**FB2(), 'face': ANG2b}, toonDur=0.0)]
for i, t_ in enumerate(SH2):
    VOIS2.append(k(t_, toon={**FB2(0.05 if i % 2 == 0 else -0.04), 'sq': [1.03, 0.97, 1.03] if i % 2 == 0 else [0.98, 1.03, 0.98], 'face': ANG2 if i % 2 == 0 else ANG2b}, toonDur=0.08))
VOIS2 += life(r(BR2 + 0.35), D2, ANG2b, FB2(), blinks=[r(D2 - 0.35)])
FORM2K = [k(t_, to=add(FORM2, [0, 0.05 if i % 2 == 0 else -0.04, 0]), dur=0.08) for i, t_ in enumerate(SH2)]
A2 = [[0.0, 1.32], [0.45, 0.85], [0.62, 1.4, 'lin'], [0.75, 1.3], [r(BR2 - 0.2), 1.0], [r(BR2), 1.42, 'lin'], [r(BR2 + 0.15), 1.32]]
st.shot('S02', 'grassland', setOpts=SET, actors=[act('voisin', NB2, RY2, 'stand', 'angry', keys=VOIS2), act('mec', HERO_IN, 20, 'stand', 'neutral', keys=[k(0.0, toon={**HB2H, 'face': DEAD}, toonDur=0.0), *life(0.2, D2, DEAD, HB2H, blinks=[0.9])])],
        props=[*STREET(2, nb=True), FACADE('maison2', swing=A2), CAN('burette2', 'mec'), P('bonnet2', 'nightCap', on={'actor': 'voisin', 'joint': 'head', 'offset': [0, 0.5, 0], 'rot': [0, 0, 0.15]}),
               P('plainte2', 'grinForm', pos=FORM2, face='camera', scale=1.3, keys=FORM2K),
               SQUEAK('S02', 'grince2', SQ2, [0.62, r(BR2)], size=0.7, side=1, amp=[1.0, 1.1])],
        cams=[C2])

# 3: three linguists are formal. Three-quarters at the doorstep: three box-headed linguists in tweed and round glasses kneel in a row on the path
#    on the left, the open door on the right; the first holds a boom at the hinge, the second presses a headphone cup, the third writes on a
#    clipboard; the door squeaks, the three lean in together; closer (on « une langue »), the boom man nods twice and the LANGUE card stamps
D3 = st.dur('S03'); FO3 = W('S03', 'L03', 3); UNE3 = W('S03', 'L03', 4); LG3 = W('S03', 'L03', 5); PO3 = W('S03', 'L03', 10)
LING = [[-0.25, 0.0, 0.62], [-0.82, 0.0, 1.02], [-1.42, 0.0, 1.42]]
F3 = [0.5, 1.25, 5.8]; L3 = [-0.48, 1.1, 0.9]
RYL = [r((yaw(p, [0.575, 0, 0.0]) + yaw(p, F3)) / 2, 1) for p in LING]
LOOK3 = [0.7, 1.4, 2.2]
SQ3 = [0.575, 2.3, 0.08]
C3 = cam(0.0, F3, add(F3, [-0.05, 0.0, -0.2]), L3, add(L3, [0.03, 0, 0]), lens=54, ease='inOut')
F3B = [0.0, 1.2, 4.1]; L3B = [-0.25, 1.25, 0.3]
C3B = cam(r(UNE3 - 0.03), F3B, add(F3B, [-0.03, 0.02, -0.12]), L3B, add(L3B, [0, 0.01, 0]), lens=50, ease='out')
chkc('S03', C3, {'h1': add(LING[0], [0, 1.6, 0]), 'h2': add(LING[1], [0, 1.6, 0]), 'h3': add(LING[2], [0, 1.6, 0]), 'k3': add(LING[2], [0, 0.2, 0]), 'hingeSq': SQ3, 'sqTip': add(SQ3, [-0.6, 0.2, 0]), 'doorTop': [0, 2.6, 0], 'mic': [0.42, 1.55, 0.25]})
chkc('S03', C3B, {'h1': add(LING[0], [0, 1.6, 0]), 'h2': add(LING[1], [0, 1.6, 0]), 'hingeSq': SQ3, 'sqTip': add(SQ3, [-0.6, 0.2, 0]), 'mic': [0.42, 1.55, 0.25], 'k1': add(LING[0], [0, 0.2, 0])})
MIC3 = [0.42, 1.55, 0.25]                                               # the boom's windshield, at the hinge
BOOM3 = off(LING[0], RYL[0], 0.32, -0.15, 1.1)
FL = {'lid': 0.15, 'mouth': 'line', 'brow': 0.4}
FLI = {'lid': 0.0, 'eye': 0.35, 'mouth': 'o', 'brow': 0.9, 'noBlink': 1}
SQT3 = [0.45, 1.25]
def LEAN(keep, t_, face=FLI): return [k(r(t_ - 0.05), toon={**keep, 'sq': [1.04, 0.96, 1.04], 'face': FL}, toonDur=0.05), k(r(t_ + 0.06), toon={**keep, 'bend': {'spine': [0.35, 0, 0, 1, None], 'neck': [0.15, 0, 0, 1.25, None]}, 'face': face}, toonDur=0.1, toonEase='out'),
                                      k(r(t_ + 0.5), toon={**keep, 'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': FL}, toonDur=0.2)]
KL1 = {'reach': {'R': R5(BOOM3, 1, 0.0), 'L': R5(add(BOOM3, [-0.1, -0.12, 0.1]), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'grip'}, 'hip': 0}
KL2 = lambda d=0.0: {'touch': {'R': ['face', -0.6, 0.15 + d, -0.05]}, 'reach': {'L': R5(off(LING[1], RYL[1], 0.35, -0.12, 0.95), 1, 0.0)}, 'hands': {'R': 'open', 'L': 'rest'}, 'hip': 0}
CLIP3 = off(LING[2], RYL[2], 0.4, 0.0, 1.0)
KL3 = lambda dx=0.0: {'reach': {'L': R5(add(CLIP3, [0.1, -0.05, 0]), 1, 0.0), 'R': R5(add(CLIP3, [-0.05 + dx, 0.03, 0.03]), 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'hip': 0}
L1K = [k(-0.4, look=LOOK3), k(0.0, toon={**KL1, 'face': FL}, toonDur=0.0), *LEAN(KL1, SQT3[0]), *LEAN(KL1, SQT3[1]), k(r(UNE3 + 0.02), look='camera', lookDur=0.12)]
for i, t_ in enumerate([r(LG3 + 0.1), r(LG3 + 0.42), r(PO3 - 0.05), r(PO3 + 0.25)]):
    L1K.append(k(t_, toon={**KL1, 'bend': {'neck': [0.32 if i % 2 == 0 else -0.05, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'mouth': 'line', 'brow': 0.6}}, toonDur=0.12, toonEase='inOut'))
L2K = [k(-0.4, look=LOOK3), k(0.0, toon={**KL2(), 'face': FL}, toonDur=0.0), *LEAN(KL2(), r(SQT3[0] + 0.03)), *LEAN(KL2(), r(SQT3[1] + 0.03))]
for i in range(5): L2K.append(k(r(1.85 + i * 0.36), toon={**KL2(0.03 if i % 2 == 0 else -0.02), 'face': {**FL, 'lid': 0.5}}, toonDur=0.3, toonEase='inOut'))
L3K = [k(-0.4, look=CLIP3), k(0.0, toon={**KL3(), 'face': FL}, toonDur=0.0), *LEAN(KL3(), r(SQT3[0] + 0.06)), *LEAN(KL3(), r(SQT3[1] + 0.06))]
for i in range(8): L3K.append(k(r(1.9 + i * 0.2), toon={**KL3(0.06 if i % 2 == 0 else -0.04), 'face': {**FL, 'gy': 0.6}}, toonDur=0.1))
A3 = [[0.0, 1.3], [r(SQT3[0] - 0.15), 1.12], [r(SQT3[0]), 1.42, 'lin'], [r(SQT3[0] + 0.15), 1.3], [r(SQT3[1] - 0.15), 1.1], [r(SQT3[1]), 1.42, 'lin'], [r(SQT3[1] + 0.15), 1.3]]
BOOMP = P('perche3', 'boomMic', pos=BOOM3, ry=yaw(BOOM3, MIC3), opts={'len': r(math.dist(BOOM3, MIC3) - 0.12), 'tilt': r(math.atan2(MIC3[1] - BOOM3[1], math.hypot(MIC3[0] - BOOM3[0], MIC3[2] - BOOM3[2])), 3)})
st.shot('S03', 'grassland', setOpts=SET, actors=[act('ling1', LING[0], RYL[0], 'kneel', 'neutral', keys=L1K), act('ling2', LING[1], RYL[1], 'kneel', 'neutral', keys=L2K), act('ling3', LING[2], RYL[2], 'kneel', 'neutral', keys=L3K)],
        props=[*STREET(3), FACADE('maison3', swing=A3), BOOMP, P('casque3', 'chifHeadset', on={'actor': 'ling2', 'joint': 'head', 'offset': [0.0, 0.0, 0.0]}, opts={'w': 0.32}),
               P('bloc3', 'clipboardProp', pos=CLIP3, ry=RYL[2], rot=[-0.9, 0, 0]),
               SQUEAK('S03', 'grince3', SQ3, SQT3 + [r(PO3 - 0.1)], size=0.7, side=-1, amp=[1.0, 1.1, 0.9])],
        cams=[C3, C3B])
st.card('S03', 'LANGUE', at=r(LG3 + 0.05))

# 4: threatened language, oiling forbidden. The door shut: an official in a violet-and-gold sash drives the last screw of a door-panel-sized bronze
#    plaque (a crossed-out oil drop, no words), the plaque shudders tight; he swaps to big scissors and on « l'huiler » snips the red ribbon across
#    the doorstep: the halves drop, the door shivers and squeaks; he puffs his chest
D4 = st.dur('S04'); INT4 = W('S04', 'L04', 2); HUI4 = W('S04', 'L04', 4)
PLQ4 = [0.0, 1.5, 0.035]; SCREW4 = [-0.33, 1.06, 0.07]
OFF4 = [-0.92, 0.0, 0.62]; RY4 = 62
RIB4 = [0.0, 0.0, 0.85]; CUT4 = r(HUI4 + 0.05)
SQ4 = [0.575, 2.32, 0.08]
F4 = [-0.55, 1.5, 5.6]; L4 = [-0.3, 1.32, 0.2]
C4 = cam(0.0, F4, add(F4, [0.05, 0.0, -0.3]), L4, add(L4, [0, 0.0, 0]), lens=46, ease='inOut')
chkc('S04', C4, {'head': add(OFF4, [0, 2.3, 0]), 'back': add(OFF4, [-0.3, 1.3, 0]), 'plqTop': add(PLQ4, [0, 0.5, 0]), 'plqBot': add(PLQ4, [0, -0.5, 0]), 'ribbon': add(RIB4, [0, 0.92, 0]), 'feet': OFF4, 'hingeSq': SQ4, 'sqTip': add(SQ4, [-0.55, 0.25, 0]), 'doorTop': [0, 2.6, 0]})
OF = {'lid': 0.3, 'mouth': 'line', 'brow': 0.3}
OFP = {'lid': 0.15, 'mouth': 'smirk', 'brow': 0.7}
OK4 = lambda hr, hl=None: {'reach': {'R': R5(hr, 1, 0.0), 'L': R5(hl or off(OFF4, RY4, 0.3, -0.25, 1.05), 1, 0.0)}, 'hands': {'R': 'grip', 'L': 'open'}, 'hip': 0}
DRV = add(SCREW4, [0, 0, 0.22])
OFF4K = [k(-0.4, look=SCREW4), k(0.0, toon={**OK4(DRV), 'bend': {'spine': [0.2, 0, 0, 1, None]}, 'face': OF}, toonDur=0.0)]
for i in range(5): OFF4K.append(k(r(0.12 + i * 0.13), toon={**OK4(add(DRV, [0, 0, -0.03 if i % 2 == 0 else 0.0])), 'bend': {'spine': [0.2, 0, 0.12 if i % 2 == 0 else -0.12, 1, None]}, 'face': OF}, toonDur=0.08))
OFF4K += [k(0.8, toon={**OK4(add(DRV, [-0.05, 0, 0.05])), 'sq': [0.95, 1.06, 0.95], 'face': OFP}, toonDur=0.06, toonEase='out'),
          k(1.0, look=add(RIB4, [0, 0.92, 0]), lookDur=0.2), k(1.05, toon={**OK4(off(OFF4, RY4, 0.45, 0.15, 1.15)), 'face': OF}, toonDur=0.2),
          k(r(CUT4 - 0.12), toon={**OK4(add(RIB4, [-0.02, 1.05, -0.05])), 'bend': {'spine': [0.25, 0, 0, 1, None]}, 'face': OF}, toonDur=0.15, toonEase='inOut'),
          *beat(CUT4, {**OK4(add(RIB4, [-0.02, 1.0, -0.05])), 'sq': [0.92, 1.1, 0.92], 'face': {'lid': 0.0, 'eye': 0.2, 'mouth': 'smile', 'brow': 0.9}}, hold=0.2,
                antic={**OK4(add(RIB4, [-0.02, 1.08, -0.05])), 'sq': [1.06, 0.94, 1.06], 'face': OF}),
          k(r(CUT4 + 0.12), look='camera', lookDur=0.12)]
# (round 1 fix) the chest puff is a real squash and stretch: two frames of exhale (hunched, chest thin), then the torso swells fat and tall with the
#     chin up, held trembling, an overshoot past rest and a settle still a little puffed (the hold breathes)
PUFF4 = r(CUT4 + 0.24); OKP = OK4(off(OFF4, RY4, 0.35, 0.1, 1.05))
OFF4K = [k_ for k_ in OFF4K if k_['at'] < r(CUT4 + 0.13) or 'look' in k_]
OFF4K += beat(PUFF4, {**OKP, 'sq': [1.16, 1.02, 1.16], 'bend': {'spine': [-0.02, 0, 0, 1.02, 1.7], 'neck': [-0.08, 0, 0, 1, None]}, 'face': {**OFP, 'brow': 0.9, 'lid': 0.3}},
              antic={**OKP, 'sq': [0.95, 0.95, 0.95], 'bend': {'spine': [0.18, 0, 0, 0.95, 0.85], 'neck': [0.1, 0, 0, 1, None]}, 'face': {**OF, 'mouth': 'o'}}, hold=0.12,
              over={**OKP, 'sq': [1.0, 1.0, 1.0], 'bend': {'spine': [-0.03, 0, 0, 1.0, 1.0], 'neck': [-0.08, 0, 0, 1, None]}, 'face': OFP},
              settle={**OKP, 'sq': [1.05, 1.01, 1.05], 'bend': {'spine': [-0.06, 0, 0, 1.01, 1.3], 'neck': [-0.12, 0, 0, 1, None]}, 'face': OFP}, antic_f=3, settle_f=4)
SDRV = P('tournevis4', 'screwdriver', on={'actor': 'officiel', 'hand': 'R', 'offset': [0, -0.04, -0.06], 'rot': [PI / 2, 0, 0]}, opts={'len': 0.34, 'color': '#E8B020'}, keys=[k(1.0, scale=0.01, dur=0.0)])
SCIS = P('ciseaux4', 'scissors', on={'actor': 'officiel', 'hand': 'R', 'offset': [0, -0.04, -0.04], 'rot': [PI / 2, 0, 0]}, scale=0.01, opts={'cutAt': CUT4}, keys=[k(1.0, scale=1.3, dur=0.0)])
st.shot('S04', 'grassland', setOpts=SET, actors=[act('officiel', OFF4, RY4, 'stand', 'neutral', keys=OFF4K)],
        props=[*STREET(4), FACADE('maison4', open_=0.0, rattle=[[r(CUT4 + 0.06), 0.035, 26, 5]], light=0), P('plaque4', 'grinPlaque', pos=PLQ4, opts={'screwAt': [0.1, 0.75], 'screw': 2}, keys=[k(0.78, squash=[1.05, 0.95, 1.0], dur=0.3)]),
               P('ruban4', 'ribbonCut', pos=RIB4, opts={'w': 1.5, 'h': 0.92, 'cutAt': CUT4}), SDRV, SCIS,
               SQUEAK('S04', 'grince4', SQ4, [r(CUT4 + 0.06)], size=0.55, side=-1, amp=[1.0])],
        cams=[C4])
st.cue('sfx:scratch', 'S04', 0.15, 0.15); st.cue('clack', 'S04', 0.78, 0.2); st.cue('sfx:zip', 'S04', CUT4, 0.2)

# 5: the gendarmes seized his oil can. On the doorstep: a gendarme takes the can from his mitten, lifts it over the clear bag that his colleague holds
#    open, lets go on « burette »: it drops in (u² keys), the bag seals with a squash; his empty mitten stays at chest height, he looks at it, then at us
D5 = st.dur('S05'); GEN5 = W('S05', 'L05', 1); SAI5 = W('S05', 'L05', 3); BUR5 = W('S05', 'L05', 5)
H5 = [-0.1, FLOOR_IN, -0.3]; RY5 = 0
G1P = [0.62, 0.14, 0.42]; RYG1 = -30
G2P = [-0.68, 0.14, 0.45]; RYG2 = 30
CAN0 = off(H5, RY5, 0.45, -0.2, 1.12)                                    # the can in his left mitten (its base)
LIFT5 = [0.0, 1.62, 0.55]; BAG5 = [-0.36, 1.12, 0.8]
TAKE5 = r(SAI5 - 0.05); DROP5 = r(BUR5 + 0.02); LAND5 = r(DROP5 + 0.22); SEAL5 = r(LAND5 + 0.04)
fallK = [k(r(DROP5 + 0.22 * (u - 0.25)), to=lerp3(LIFT5, add(BAG5, [0, -0.2, 0]), u * u), dur=r(0.22 / 4), ease='linear') for u in (0.25, 0.5, 0.75, 1.0)]
CANK5 = [k(TAKE5, to=add(CAN0, [0.05, 0.12, 0.2]), dur=0.25, ease='inOut'), k(r(TAKE5 + 0.3), to=LIFT5, dur=r(DROP5 - TAKE5 - 0.32), ease='inOut'), *fallK, k(SEAL5, scale=0.01, dur=0.0)]
F5 = [-0.16, 1.55, 5.5]; L5 = [-0.1, 1.55, 0.8]
C5 = cam(0.0, F5, add(F5, [0.04, 0.0, -0.25]), L5, add(L5, [0, 0.02, 0]), lens=40, ease='inOut')
chkc('S05', C5, {'hero': add(H5, [0, 2.3, 0]), 'g1': add(G1P, [0, 2.45, 0]), 'g2': add(G2P, [0, 2.45, 0]), 'can0': CAN0, 'lift': LIFT5, 'bag': BAG5, 'bagBot': add(BAG5, [0, -0.36, 0]), 'g1feet': G1P})
HF5 = {'lid': 0.35, 'mouth': 'line', 'brow': 0.0}
HB5 = lambda hl: {'reach': {'L': R5(hl, 1, 0.0)}, 'hands': {'L': 'grip'}, 'hip': 0}
EMPTY5 = add(CAN0, [0.0, 0.1, 0.05])
# (round 1 fix) a double take at the empty mitten: a glance down at it, back to us (a blank beat and a blink), then the snap back down at it with the
#     jaw dropping to his collar (the head long and thin on a stretched neck), held trembling, an overshoot and a deadpan settle to us
DT5 = r(TAKE5 + 0.56)
MIT5 = add(EMPTY5, [0, 0.05, 0.25])
JAW5 = {**HB5(EMPTY5), 'hands': {'L': 'open'}, 'sq': [0.92, 1.09, 0.92], 'scl': {'head': [0.88, 1.16, 1.0]}, 'bend': {'neck': [0.12, 0, 0, 1.5, None]},
        'face': {'lid': 0.0, 'eye': 0.45, 'gx': 0.45, 'gy': 0.7, 'jaw': 1.0, 'jawLen': 1.6, 'jawBlock': 1, 'jawFwd': 0.4, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}}
HERO5 = [k(-0.4, look=add(G1P, [0, 2.0, 0])), k(0.0, toon={**HB5(add(CAN0, [0, 0.08, 0])), 'face': HF5}, toonDur=0.0), *life(0.1, r(TAKE5 - 0.05), HF5, HB5(add(CAN0, [0, 0.08, 0])), blinks=[0.35]),
         k(TAKE5, toon={**HB5(EMPTY5), 'hands': {'L': 'open'}, 'face': {**HF5, 'brow': 0.3}}, toonDur=0.2),
         k(r(TAKE5 + 0.18), look=MIT5, lookDur=0.12),
         k(r(TAKE5 + 0.22), toon={**HB5(EMPTY5), 'hands': {'L': 'open'}, 'face': {'lid': 0.4, 'mouth': 'line', 'brow': 0.1, 'gy': 0.5}}, toonDur=0.12),
         k(r(TAKE5 + 0.36), look='camera', lookDur=0.08),
         k(r(TAKE5 + 0.4), toon={**HB5(EMPTY5), 'hands': {'L': 'open'}, 'face': {'lid': 0.35, 'mouth': 'line', 'brow': 0.0}}, toonDur=0.08),
         *blink(r(TAKE5 + 0.44), {'lid': 0.35, 'mouth': 'line', 'brow': 0.0}, {**HB5(EMPTY5), 'hands': {'L': 'open'}}),
         k(r(DT5 - 0.04), look=MIT5, lookDur=0.04),
         *beat(DT5, JAW5, antic={**HB5(EMPTY5), 'hands': {'L': 'open'}, 'sq': [1.1, 0.88, 1.1], 'scl': {'head': [1.1, 0.9, 1.0]}, 'face': {'lid': 0.7, 'mouth': 'clench', 'brow': -0.5}}, hold=0.28,
               over={**HB5(EMPTY5), 'hands': {'L': 'open'}, 'sq': [1.04, 0.97, 1.04], 'face': {'lid': 0.1, 'mouth': 'o', 'jaw': 0.3, 'brow': 0.8}},
               settle={**HB5(EMPTY5), 'hands': {'L': 'open'}, 'face': {'lid': 0.2, 'mouth': 'o', 'jaw': 0.12, 'brow': 0.6}}, antic_f=3, settle_f=5),
         k(r(DT5 + 0.5), look='camera', lookDur=0.12),
         k(r(DT5 + 0.52), toon={**HB5(EMPTY5), 'hands': {'L': 'open'}, 'face': DEAD}, toonDur=0.12)]
GF = {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}
G1K = lambda hr: {'reach': {'R': R5(hr, 1, 0.0)}, 'hands': {'R': 'grip'}, 'hip': 0}
GRIP = lambda p: add(p, [0.06, 0.14, 0.0])
G1KS = [k(-0.4, look=CAN0), k(0.0, toon={**G1K(off(G1P, RYG1, 0.3, 0.0, 1.0)), 'face': GF}, toonDur=0.0),
        k(r(GEN5), toon={**G1K(GRIP(add(CAN0, [0.05, 0.0, 0.15]))), 'face': GF}, toonDur=r(TAKE5 - GEN5)),
        k(TAKE5, toon={**G1K(GRIP(add(CAN0, [0.05, 0.12, 0.2]))), 'face': GF}, toonDur=0.25),
        k(r(TAKE5 + 0.3), toon={**G1K(GRIP(LIFT5)), 'face': GF}, toonDur=r(DROP5 - TAKE5 - 0.32), toonEase='inOut'), k(r(TAKE5 + 0.3), look=BAG5, lookDur=0.2),
        k(r(DROP5 + 0.02), toon={**G1K(add(GRIP(LIFT5), [0.12, 0.05, 0])), 'hands': {'R': 'open'}, 'face': GF}, toonDur=0.08),
        k(r(SEAL5 + 0.1), look='camera', lookDur=0.15), *life(r(SEAL5 + 0.15), D5, GF, {**G1K(add(GRIP(LIFT5), [0.12, 0.05, 0])), 'hands': {'R': 'open'}}, blinks=[r(D5 - 0.2)])]
BAGH = lambda: {'reach': {'L': R5(add(BAG5, [0.2, 0.22, -0.04]), 1, 0.0), 'R': R5(add(BAG5, [-0.2, 0.22, -0.04]), 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'hip': 0}
G2KS = [k(-0.4, look=LIFT5), k(0.0, toon={**BAGH(), 'face': GF}, toonDur=0.0), *life(0.1, D5, GF, BAGH(), blinks=[0.7])]
st.shot('S05', 'grassland', setOpts=SET, actors=[act('mec', H5, RY5, 'stand', 'neutral', keys=HERO5), act('gendarme1', G1P, RYG1, 'stand', 'neutral', keys=G1KS), act('gendarme2', G2P, RYG2, 'stand', 'neutral', keys=G2KS)],
        props=[*STREET(5), FACADE('maison5', open_=1.25), KEPI('kepi5a', 'gendarme1'), KEPI('kepi5b', 'gendarme2'),
               P('burette5', 'grinOilCan', pos=CAN0, face='camera', faceFlat=True, opts={'s': 0.92}, keys=CANK5),
               BAG('sachet5o', BAG5, open=True, can=False, keys=[k(SEAL5, scale=0.01, dur=0.0)], flat=[[0.0, 0.0], [r(LAND5 - 0.01), 0.0], [SEAL5, 1.0, 'lin']]), BAG('sachet5', BAG5, scale=0.01, keys=[k(SEAL5, scale=1.0, dur=0.0)],
                   flat=[[0.0, 1.0], [r(SEAL5 + 0.1), 1.0], [r(SEAL5 + 0.2), -0.32], [r(SEAL5 + 0.28), 0.14], [r(SEAL5 + 0.36), -0.05], [r(SEAL5 + 0.44), 0.0]])],
        cams=[C5])
st.cue('sfx:cuff', 'S05', TAKE5, 0.25); st.cue('thud', 'S05', LAND5, 0.2); st.cue('sfx:zip', 'S05', SEAL5, 0.22)

# 6: and closing the door cuts it off. He steps out onto the step facing us and pulls the door shut behind his back; a gendarme beside him stops it
#    with one flat mitten on the wood; he tugs twice, the gendarme slowly shakes his box head; on « parole » the gendarme pushes and the door swings
#    back open with a squeak, out of his hand
# (round 1 fix) seen from the front left: he steps out three-quarters to us, his right arm back on the outer knob, the door half shut behind him; the
#     gendarme's flat mitten lands on the wood (palm out, arm level, a bigger glove that reads against the teal leaf); two big tugs (he leans away,
#     stretched, the door gives a little and bounces back against the mitten); the gendarme shakes his head slowly; on « parole » the push rips the
#     door out of his hand: for two frames he smears long toward it (arm drawn out, body stretched), then snaps back with an overshoot, deadpan. The
#     squeak goes off the upper hinge toward the doorway top, clear of both faces
D6 = st.dur('S06'); FER6 = W('S06', 'L06', 1); COU6 = W('S06', 'L06', 6); PAR6 = W('S06', 'L06', 8)
H6A = [-0.18, FLOOR_IN, -0.35]; H6M = [-0.32, 0.14, 0.28]; H6B = [-0.8, 0.14, 0.3]; RY6 = -10
G6 = [0.85, 0.14, 0.5]; RYG6 = -30
STOP6 = r(FER6 + 0.45); AMIN = 0.5
TUG6 = [r(STOP6 + 0.3), r(STOP6 + 0.65)]
A6 = [[0.0, 1.25], [r(FER6 - 0.02), 1.22], [r(STOP6 - 0.02), AMIN - 0.03, 'lin'], [r(STOP6 + 0.06), AMIN + 0.05], [r(STOP6 + 0.16), AMIN]]
for t_ in TUG6: A6 += [[r(t_ - 0.04), AMIN], [r(t_ + 0.06), AMIN - 0.06, 'lin'], [r(t_ + 0.14), AMIN + 0.06], [r(t_ + 0.24), AMIN - 0.01], [r(t_ + 0.3), AMIN]]
A6 += [[r(PAR6 - 0.06), AMIN + 0.01], [r(PAR6 + 0.12), 1.42, 'lin'], [r(PAR6 + 0.26), 1.28], [r(PAR6 + 0.42), 1.34]]
KNOBO = lambda a: door_pt(a, DW - 0.16, 1.24, 0.09)
GPUSH = lambda a: door_pt(a, 0.28, 1.55, 0.08)
SQ6 = [0.575, 2.35, 0.05]
F6 = [-1.2, 1.55, 5.6]; L6 = [0.05, 1.5, 0.0]
C6 = cam(0.0, F6, add(F6, [0.04, 0.0, -0.22]), L6, add(L6, [0.0, 0, 0]), lens=48, ease='inOut')
chkc('S06', C6, {'g': add(G6, [0, 2.45, 0]), 'gHand': GPUSH(AMIN), 'heroB': add(H6B, [0, 2.4, 0]), 'heroA': add(H6A, [0, 2.3, 0]), 'knob': KNOBO(AMIN), 'hingeSq': SQ6, 'sqTip': add(SQ6, [-0.45, 0.1, 0]), 'feet': H6B, 'doorOpen': door_pt(1.4, DW, 1.3)})
HK6 = lambda a, **x: {'reach': {'L': R5(KNOBO(a), 1, 0.0)}, 'hands': {'L': 'grip'}, 'hip': 0, **x}
HF6 = {'lid': 0.3, 'mouth': 'line', 'brow': 0.0}
TUGF = {'lid': 0.5, 'mouth': 'clench', 'brow': -0.7}
HERO6 = [k(-0.4, look='camera'), k(0.0, toon={**HK6(1.25), 'face': HF5}, toonDur=0.0),
         k(r(FER6 - 0.02), to=H6M, dur=0.2, glide=True, face=RY6, ease='in'), k(r(FER6 + 0.18), to=H6B, dur=r(STOP6 - FER6 - 0.2), glide=True, face=RY6, ease='out'),
         k(r(FER6 + 0.1), toon={**HK6(0.9), 'face': {**HF5, 'brow': 0.2}}, toonDur=0.2), k(r(STOP6 - 0.02), toon={**HK6(AMIN), 'sq': [1.04, 0.96, 1.04], 'face': HF6}, toonDur=0.15)]
for t_ in TUG6:
    HERO6 += [k(r(t_ - 0.05), toon={**HK6(AMIN), 'sq': [1.06, 0.94, 1.06], 'bend': {'spine': [-0.08, 0, 0, 1, None]}, 'face': {**TUGF, 'lid': 0.3}}, toonDur=0.05),
              k(r(t_ + 0.04), toon={**HK6(AMIN - 0.06), 'sq': [0.92, 1.09, 0.92], 'bend': {'spine': [0.32, 0, 0, 1.06, None], 'neck': [0.15, 0, 0, 1.1, None]}, 'face': TUGF}, toonDur=0.07, toonEase='out'),
              k(r(t_ + 0.16), toon={**HK6(AMIN + 0.05), 'sq': [1.05, 0.95, 1.05], 'bend': {'spine': [-0.1, 0, 0, 1, None]}, 'face': {**TUGF, 'mouth': 'grimace'}}, toonDur=0.08),
              k(r(t_ + 0.27), toon={**HK6(AMIN), 'face': HF6}, toonDur=0.1)]
HERO6 += [k(r(TUG6[1] + 0.32), look=add(G6, [0, 2.1, 0]), lookDur=0.2),
          *blink(r(TUG6[1] + 0.45), HF6, HK6(AMIN)),
          k(r(PAR6 - 0.03), toon={**HK6(AMIN + 0.08), 'sq': [1.05, 0.95, 1.05], 'face': {**HF6, 'brow': 0.3}}, toonDur=0.04),
          k(r(PAR6 + 0.04), toon={**HK6(1.05), 'sq': [0.8, 1.22, 0.8], 'bend': {'spine': [-0.35, 0, 0, 1.12, None], 'neck': [-0.2, 0, 0, 1.2, None]}, 'face': {'lid': 0.0, 'eye': 0.45, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}}, toonDur=0.05, toonEase='out'),
          k(r(PAR6 + 0.1), toon={'reach': {'L': R5(add(KNOBO(1.2), [0.0, 0, 0.1]), 1, 0.0)}, 'hands': {'L': 'open'}, 'sq': [0.86, 1.16, 0.86], 'bend': {'spine': [-0.25, 0, 0, 1.08, None]}, 'face': {'lid': 0.0, 'eye': 0.4, 'mouth': 'O', 'brow': 1.0, 'noBlink': 1}, 'hip': 0}, toonDur=0.04),
          k(r(PAR6 + 0.16), toon={'reach': {'L': R5(off(H6B, RY6, 0.15, -0.3, 1.0), 1, 0.0)}, 'hands': {'L': 'open'}, 'sq': [1.14, 0.88, 1.14], 'bend': {'spine': [0.15, 0, 0, 1, None]}, 'face': {'lid': 0.2, 'eye': 0.2, 'mouth': 'o', 'brow': 0.7}, 'hip': 0}, toonDur=0.07, toonEase='out'),
          k(r(PAR6 + 0.27), toon={'sq': [0.97, 1.03, 0.97], 'face': {'lid': 0.3, 'mouth': 'line', 'brow': 0.2}, 'hip': 0}, toonDur=0.08),
          k(r(PAR6 + 0.36), toon={'face': DEAD, 'hip': 0}, toonDur=0.12), k(r(PAR6 + 0.33), look='camera', lookDur=0.12)]
GF6 = {'lid': 0.3, 'mouth': 'line', 'brow': -0.3}
GK6 = lambda a, tw=0.0, f=GF6, **x: {'reach': {'R': R5(GPUSH(a), 1, 0.0)}, 'hands': {'R': 'open'}, 'scl': {'handR': [1.3, 1.3, 1.3]}, 'bend': {'neck': [0.05, 0, tw, 1, None]}, 'face': f, 'hip': 0, **x}
GS = {'lid': 0.45, 'mouth': 'line', 'brow': -0.2}
G6REST = {'reach': {'R': R5(off(G6, RYG6, 0.3, 0.1, 1.0), 1, 0.0)}, 'hands': {'R': 'open'}, 'face': GF6, 'hip': 0}
G6K = [k(-0.4, look=add(H6B, [0, 2.1, 0])), k(0.0, toon=G6REST, toonDur=0.0), *life(0.05, r(STOP6 - 0.2), GF6, G6REST, blinks=[0.2]),
       k(r(STOP6 - 0.16), toon=GK6(AMIN + 0.04), toonDur=0.14, toonEase='out'), k(r(STOP6 - 0.02), toon={**GK6(AMIN), 'sq': [1.04, 0.97, 1.04]}, toonDur=0.04)]
for t_ in TUG6: G6K += [k(r(t_ + 0.04), toon={**GK6(AMIN - 0.06), 'sq': [0.98, 1.02, 0.98]}, toonDur=0.06), k(r(t_ + 0.14), toon=GK6(AMIN + 0.04), toonDur=0.08), k(r(t_ + 0.24), toon=GK6(AMIN), toonDur=0.08)]
for i, t_ in enumerate([r(TUG6[1] + 0.3), r(TUG6[1] + 0.58)]):
    G6K.append(k(t_, toon=GK6(AMIN, 0.45 if i % 2 == 0 else -0.45, GS), toonDur=0.26, toonEase='inOut'))
G6K += [k(r(PAR6 - 0.07), toon={**GK6(AMIN, 0.0, GS), 'sq': [1.06, 0.95, 1.06]}, toonDur=0.06), k(r(PAR6 + 0.1), toon={**GK6(1.3, 0.0, GS), 'sq': [0.96, 1.04, 0.96]}, toonDur=0.12, toonEase='out'),
        k(r(PAR6 + 0.28), look='camera', lookDur=0.2), k(r(PAR6 + 0.3), toon=G6REST, toonDur=0.25)]
st.shot('S06', 'grassland', setOpts=SET, actors=[act('mec', H6A, RY6, 'stand', 'neutral', keys=HERO6), act('gendarme1', G6, RYG6, 'stand', 'neutral', keys=G6K)],
        props=[*STREET(6), FACADE('maison6', swing=A6), KEPI('kepi6', 'gendarme1'),
               SQUEAK('S06', 'grince6', SQ6, [r(STOP6), r(PAR6 + 0.12)], size=0.45, side=-1, amp=[0.8, 1.15], top=True)],
        cams=[C6])
st.cue('thud', 'S06', STOP6, 0.15)
for t_ in TUG6: st.cue('thud', 'S06', r(t_ + 0.14), 0.1)

# 7: he lives with the door open; he heats the street. Snow: from the pavement, the wide-open door frames him on his sofa in a wool hat and scarf,
#    snow blowing in past him; two passers-by stand at the doorway warming their mittens as at a fireplace, steam rising; a dark wet patch on the
#    snowy path; the door rattles in the wind and squeaks
D7 = st.dur('S07'); OUV7 = W('S07', 'L07', 5); CH7 = W('S07', 'L07', 7)
SOFA7 = [0.0, FLOOR_IN, -3.2]; H7 = [0.0, 0.16, -3.05]
PA7 = [-0.72, 0.14, 0.42]; PB7 = [0.75, 0.14, 0.45]; RYA7 = 55; RYB7 = -55
SQ7 = [0.575, 2.3, 0.08]
F7 = [-0.08, 1.3, 5.2]; L7 = [-0.06, 1.2, 0.4]
C7 = cam(0.0, F7, add(F7, [0.03, 0.0, -0.3]), L7, add(L7, [0, 0.02, 0]), lens=40, ease='inOut')
chkc('S07', C7, {'hero': add(H7, [0, 1.85, 0]), 'heroSeat': add(H7, [0, 0.5, 0]), 'pa': add(PA7, [0, 2.35, 0]), 'pb': add(PB7, [0, 2.35, 0]), 'paFeet': PA7, 'hingeSq': SQ7, 'sqTip': add(SQ7, [-0.6, 0.2, 0]), 'patch': [0, 0.06, 1.4], 'doorTop': [0, 2.6, 0]})
# (round 1 fix) the passers-by rub their mittens together over the heat (hands close, sliding up and down against each other in quick strokes), each
#     at her or his own rate, with a slow breathing sway; the hero breathes on his sofa and blinks every 1.2 s or so
RUB = lambda p, ry, u: {'reach': {'L': R5(off(p, ry, 0.42 + 0.02 * u, -0.05, 1.13 + 0.05 * u), 1, 0.0), 'R': R5(off(p, ry, 0.42 - 0.02 * u, 0.05, 1.13 - 0.05 * u), 1, 0.0)}, 'hands': {'L': 'open', 'R': 'open'}, 'hip': 0}
PAF = {'lid': 0.7, 'mouth': 'smile', 'brow': 0.3}
def RUBK(p, ry, t0, per, blinks):
    ks = [k(-0.4, look=[0, 1.3, -0.5]), k(0.0, toon={**RUB(p, ry, 0), 'face': PAF}, toonDur=0.0)]
    t_, i = t0, 0
    while t_ < D7 - 0.05:
        if not any(-0.04 < t_ - b < 0.18 for b in blinks):
            br = 0.012 * math.sin(t_ * 2.6 + t0 * 5)
            ks.append(k(r(t_), toon={**RUB(p, ry, 1 if i % 2 == 0 else -1), 'sq': [r(1 - br * 0.5, 4), r(1 + br, 4), r(1 - br * 0.5, 4)], 'face': PAF}, toonDur=r(per * 0.85), toonEase='inOut'))
        t_ += per; i += 1
    for b in blinks: ks += blink(b, PAF, RUB(p, ry, 0))
    return ks
PAK = RUBK(PA7, RYA7, 0.05, 0.13, [0.9, 2.3])
PBK = RUBK(PB7, RYB7, 0.11, 0.16, [1.5])
PAK.append(k(r(CH7 + 0.1), look='camera', lookDur=0.2))
H7F = {'lid': 0.4, 'mouth': 'line', 'brow': 0.0}
HERO7 = [k(-0.4, look='camera'), k(0.0, toon={'face': H7F, 'hip': 0}, toonDur=0.0), *life(0.1, D7, H7F, {'hip': 0}, blinks=[0.5, 1.75, r(D7 - 0.35)], amp=0.02)]
st.shot('S07', 'grassland', setOpts=SNOWSET, look={'sun': 1.6, 'fill': 1.3}, actors=[act('mecHiver', H7, 0, 'sit', 'neutral', keys=HERO7), act('passant1', PA7, RYA7, 'stand', 'neutral', keys=PAK), act('passant2', PB7, RYB7, 'stand', 'neutral', keys=PBK)],
        props=[*STREET(7, snow=True), FACADE('maison7', open_=1.5, rattle=[[0.55, 0.07, 14, 2.5], [1.85, 0.08, 14, 2.5]], snow=True, light=4.0), P('canape7', 'sofaProp', pos=SOFA7, opts={'color': '#B5402F', 'color2': '#D8604A'}),
               P('echarpe7', 'grinScarf', on={'actor': 'mecHiver', 'joint': 'torso', 'offset': [0, 0.5, 0.02]}),
               BEANIE('bonnet7', 'mecHiver'), BEANIE('bonnet7a', 'passant1', '#2F62B5', 0.32, 0.25), BEANIE('bonnet7b', 'passant2', '#E8742E', 0.32, 0.25),
               P('neige7', 'grinSnowStream', pos=[0, 0, 0], opts={'from': [0.0, 1.4, 2.6], 'dir': [0.05, -0.35, -2.4], 'spread': [1.2, 1.8], 'n': 80, 'life': 1.9}),
               P('flocons7', 'snowfall', pos=[0, 0, 1.6], opts={'w': 8, 'h': 4.5, 'd': 5, 'n': 450}),
               P('flaque7', 'grinPatch', pos=[0.0, 0, 1.45], opts={'r': 0.62, 'color': '#6E7680', 'sx': 1.25}),
               P('vapeurA7', 'softWisp', pos=off(PA7, RYA7, 0.42, 0.0, 1.2), opts={'color': '#F4F6F8', 'opacity': 0.6, 'rise': 0.8, 's0': 0.05, 's1': 0.2, 'n': 10}),
               P('vapeurB7', 'softWisp', pos=off(PB7, RYB7, 0.42, 0.0, 1.15), opts={'color': '#F4F6F8', 'opacity': 0.6, 'rise': 0.8, 's0': 0.05, 's1': 0.2, 'n': 10, 'at': -0.5}),
               P('vapeurC7', 'softWisp', pos=[0.0, 2.45, 0.15], opts={'color': '#F4F6F8', 'opacity': 0.5, 'rise': 1.0, 's0': 0.08, 's1': 0.28, 'n': 12, 'drift': [0.0, 0.25]}),
               SQUEAK('S07', 'grince7', SQ7, [0.6, 1.9], size=0.7, side=-1, amp=[0.9, 1.0])],
        cams=[C7])
st.cue('gust', 'S07', 0.2, 0.18, 2.4)

# 8: at night it talks in its sleep. Night, a warm bedside lamp: he sits up in bed against the headboard under the duvet, wool hat on, eyes wide
#    open; the bedroom door swings in the draught and the big squeak pops off its hinge, once, twice; his pupils go to it; he pulls the duvet up to his nose
D8 = st.dur('S08'); NUIT8 = W('S08', 'L08', 1); PAR8 = W('S08', 'L08', 3); SOM8 = W('S08', 'L08', 6)
BEDX, BEDZ = -2.6, -1.95
HS8 = [BEDX, 0.16, -2.55]                                                 # sitting up on the mattress (top 0.61), his back to the headboard
BDOOR = [-1.2, 0.03, -3.0]                                                # the bedroom door in the back wall (its middle)
BHINGE = [r(BDOOR[0] - DW / 2), 1.95, -2.9]
SQT8 = [r(NUIT8 + 0.05), r(PAR8 + 0.25)]
A8 = [[0.0, 0.3], [r(SQT8[0] - 0.2), 0.32], [SQT8[0], 0.85, 'lin'], [r(SQT8[0] + 0.3), 0.55], [r(SQT8[1] - 0.12), 0.5], [SQT8[1], 1.05, 'lin'], [r(SQT8[1] + 0.35), 0.75], [D8, 0.8]]
PULL8 = r(SOM8 + 0.05)
BIB8 = [[0.0, 0.5], [PULL8, 0.5], [r(PULL8 + 0.22), 0.92, 'lin'], [r(PULL8 + 0.3), 0.88]]
DUV8 = [BEDX, 0.63, -0.95]; DUVL = 1.5                                    # the duvet from the foot of the bed to his waist (z -2.45)
def BIBTOP(h, sd): return [r(BEDX + 0.2 * sd), r(DUV8[1] + h + 0.02), r(DUV8[2] - DUVL + 0.1)]
F8 = [-3.2, 1.8, 1.4]; L8 = [-2.0, 1.48, -2.52]
C8 = cam(0.0, F8, add(F8, [0.03, -0.02, -0.2]), L8, add(L8, [0, -0.01, 0]), lens=48, ease='inOut')
chkc('S08', C8, {'face': [BEDX, 1.85, -2.5], 'top': [BEDX, 2.15, -2.55], 'hingeSq': BHINGE, 'sqTip': add(BHINGE, [0.5, 0.2, 0]), 'doorTop': add(BDOOR, [0, 2.6, 0]), 'doorR': add(BDOOR, [0.6, 1.0, 0]), 'bib': BIBTOP(0.5, 0), 'nose': BIBTOP(1.12, 0), 'lamp': [-1.93, 0.9, -2.5], 'lampBase': [-1.93, 0.03, -2.3]})
BEDF = {'expr': 'surprised', 'exprW': 1.0, 'lid': 0.0, 'eye': 0.35, 'mouth': 'line', 'brow': 0.6, 'noBlink': 1}
HB8 = lambda h: {'reach': {'L': R5(BIBTOP(h, 1), 1, 0.0), 'R': R5(BIBTOP(h, -1), 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'hip': 0}
# (round 1 fix) on the first squeak his eyes bulge to twice their size (a jolt up, stretched, held trembling, an overshoot); the second squeak only
#     sends the pupils to the door; then he deflates under the duvet: the body sinks wide and short, the back rounds, the head drops, the duvet comes up
#     to his nose and the hold breathes, squashed, the eyes still wide over the duvet
BULGE = {**HB8(0.5), 'sq': [0.93, 1.1, 0.93], 'scl': {'head': [0.95, 1.08, 1.0]}, 'face': {**BEDF, 'eye': 1.0, 'gx': -0.7, 'gy': -0.1, 'brow': 1.0, 'mouth': 'o'}}
SAG8 = lambda q=0.0: {**HB8(1.0), 'sq': [r(1.14 + q, 3), r(0.76 - q, 3), r(1.14 + q, 3)], 'bend': {'spine': [0.25, 0, 0, 0.92, None], 'neck': [0.12, 0, 0, 0.9, None]}, 'face': {**BEDF, 'eye': 0.5, 'gx': -0.35, 'brow': 0.4}}
HERO8 = [k(-0.4, look=[-1.6, 1.8, 0.0]), k(0.0, toon={**HB8(0.5), 'face': {**BEDF, 'gx': -0.2}}, toonDur=0.0),
         *beat(r(SQT8[0] + 0.06), BULGE, antic={**HB8(0.5), 'sq': [1.05, 0.95, 1.05], 'face': {**BEDF, 'eye': 0.2, 'gx': -0.3}}, hold=0.24,
               over={**HB8(0.5), 'sq': [1.02, 0.98, 1.02], 'face': {**BEDF, 'eye': 0.55, 'gx': -0.5}}, settle={**HB8(0.5), 'face': {**BEDF, 'eye': 0.45, 'gx': -0.4}}),
         k(r(SQT8[1] + 0.06), toon={**HB8(0.5), 'face': {**BEDF, 'gx': -0.8, 'gy': -0.1, 'eye': 0.6}, 'sq': [0.98, 1.03, 0.98]}, toonDur=0.06),
         k(r(PULL8), toon=SAG8(0.04), toonDur=0.22, toonEase='inOut'), k(r(PULL8 + 0.3), toon=SAG8(-0.02), toonDur=0.12, toonEase='inOut')]
for i_ in range(4):
    t_ = r(PULL8 + 0.45 + 0.42 * i_)
    if t_ < D8 - 0.05: HERO8.append(k(t_, toon=SAG8(0.012 if i_ % 2 == 0 else -0.01), toonDur=0.36, toonEase='inOut'))
NIGHTWALL = '#93A0C6'
st.shot('S08', 'whiteVoid', setOpts={'color': '#1C2234'}, look={'sun': 0.35, 'sunColor': '#9DB4EC', 'fill': 0.75, 'exposure': 1.08},
        actors=[act('mecHiver', HS8, 0, 'sit', 'surprised', blink=0, keys=HERO8)],
        props=[P('sol8', 'tacheBox', pos=[-1.5, 0.0, -0.5], opts={'w': 7.0, 'h': 0.06, 'd': 6.0, 'color': '#7A5E46'}),
               P('mur8', 'tacheBox', pos=[-4.0, 1.5, -0.5], opts={'w': 0.12, 'h': 3.0, 'd': 6.0, 'color': NIGHTWALL}),
               P('porte8', 'grinFacade', pos=BDOOR, opts={'w': 6.0, 'x0': -2.8, 'h': 3.0, 'wall': NIGHTWALL, 'roof': False, 'step': False, 'plinth': '#6A789E',
                                                           'windows': [{'x': 2.1, 'y': 1.0, 'w': 1.0, 'h': 1.1, 'kind': 'night'}],
                                                           'door': {'w': DW, 'h': DH, 'color': '#E2E8EE', 'hinge': 'L', 'swing': A8, 'inside': {'w': 1.8, 'd': 1.6, 'wall': '#1E2638', 'floor': '#1A1F2C', 'band': '#1E2638', 'light': 0}}}),
               P('lit8', 'bed', pos=[BEDX, 0.03, BEDZ], opts={'w': 0.95, 'blanket': '#5A6E8C'}),
               P('couette8', 'grinDuvet', pos=DUV8, opts={'w': 1.12, 'len': DUVL, 'color': '#6C82A8', 'fold': '#E8EEF6', 'bib': BIB8}),
               P('lampe8', 'grinBedLamp', pos=[-1.93, 0.03, -2.5], opts={'power': 3.4, 'range': 4.0, 's': 0.95, 'pool': {'wall': [-0.1, 1.2, -0.44, 2.0], 'wallRy': 0.0, 'wallOp': 0.42, 'floor': [-0.2, 0.5, 1.8], 'halo': 0.9, 'op': 0.6}}),
               BEANIE('bonnet8', 'mecHiver'),
               SQUEAK('S08', 'grince8', BHINGE, SQT8, size=0.8, side=1, amp=[1.0, 1.15])],
        cams=[C8])
st.cue('sfx:cuff', 'S08', PULL8, 0.12)

# 9: the whole country learns the squeak; compulsory at the bac. The exam hall: grown-up candidates in two columns of desks receding to the back wall,
#    each with a little door on a stand; at the back, facing us behind her desk, the invigilator beats on « grincement » and they all swing their
#    doors and squeak at once (a big sprite each), again on « bac »; on her desk, in reach, the oil can in its sealed bag; on the wall: BAC /
#    ÉPREUVE DE GRINCEMENT
D9 = st.dur('S09'); GRI9 = W('S09', 'L09', 5); BAC9 = W('S09', 'L09', 8)
BEATS9 = [r(GRI9 - 0.02), r(BAC9 - 0.02)]
CAND = []
for rw, z in enumerate([-0.9, 0.45, 1.8]):
    for c, x in enumerate([-1.6, 0.0]): CAND.append((f'candidat{rw * 2 + c + 1}', [x, 0.0, r(z + 0.55)], [r(x + (0.28 if c == 0 else -0.28)), 0.72, r(z - 0.05)]))
INV9 = [-0.8, 0.0, 3.5]; RYI9 = 180; DESK9 = [-0.8, 0.0, 3.0]
BAG9 = [-1.15, 1.18, 3.0]
F9 = [-0.85, 3.25, -3.35]; L9 = [-0.8, 1.45, 0.7]
C9 = cam(0.0, F9, add(F9, [0.0, -0.05, 0.3]), L9, add(L9, [0, 0, 0.1]), lens=56, ease='inOut')
pts9 = {n: add(p, [0, 1.85, 0]) for n, p, _ in CAND}
pts9.update({'inv': add(INV9, [0, 2.35, 0]), 'bag': BAG9, 'bagBot': add(BAG9, [0, -0.3, 0]), 'board': [-0.8, 3.05, 3.93], 'door1': add(CAND[0][2], [0, 0.55, 0])})
chkc('S09', C9, pts9)
CF = {'lid': 0.3, 'mouth': 'line', 'brow': 0.2}
CFS = {'lid': 0.0, 'eye': 0.2, 'mouth': 'O', 'brow': 0.8, 'jaw': 0.4}
def CANDK(i, p, dp):
    sd = 1 if dp[0] > p[0] else -1
    keep = {'reach': {('L' if sd > 0 else 'R'): R5(add(dp, [0.0, 0.3, 0.12]), 1, 0.0), ('R' if sd > 0 else 'L'): R5(add(p, [-0.2 * sd, 0.78, -0.45]), 1, 0.0)}, 'hands': {'L': 'open', 'R': 'open'}, 'hip': 0}
    ks = [k(-0.4, look=add(dp, [0, 0.4, 0])), k(0.0, toon={**keep, 'face': CF}, toonDur=0.0), *life(0.05 + 0.07 * i, r(BEATS9[0] - 0.1), CF, keep, period=0.8)]
    for b in BEATS9:
        hit = {**keep['reach'], ('L' if sd > 0 else 'R'): R5(add(dp, [0.05 * sd, 0.32, -0.05]), 1, 0.0)}
        ks += [k(r(b - 0.08), toon={**keep, 'sq': [1.04, 0.96, 1.04], 'face': CF}, toonDur=0.05),
               k(b, toon={**keep, 'reach': hit, 'sq': [0.95, 1.06, 0.95], 'face': CFS}, toonDur=0.06, toonEase='out'),
               k(r(b + 0.35), toon={**keep, 'face': CF}, toonDur=0.15)]
    if i == 1: ks.append(k(r(BAC9 + 0.45), look='camera', lookDur=0.15))
    return ks
IF9 = {'lid': 0.2, 'mouth': 'line', 'brow': 0.5}
IK = lambda hr, f=IF9: {'reach': {'R': R5(hr, 1, 0.0)}, 'hands': {'R': 'open'}, 'face': f, 'hip': 0}
INVK = [k(-0.4, look=[-0.8, 1.6, 0.5]), k(0.0, toon=IK(off(INV9, RYI9, 0.4, 0.15, 1.15)), toonDur=0.0)]
for b in BEATS9: INVK += [k(r(b - 0.28), toon={**IK(off(INV9, RYI9, 0.4, 0.3, 1.55)), 'sq': [0.97, 1.04, 0.97]}, toonDur=0.15), k(r(b - 0.03), toon={**IK(off(INV9, RYI9, 0.55, 0.2, 1.08), {**IF9, 'mouth': 'O'}), 'sq': [1.04, 0.96, 1.04]}, toonDur=0.06, toonEase='in'),
                          k(r(b + 0.3), toon=IK(off(INV9, RYI9, 0.4, 0.15, 1.15)), toonDur=0.2)]
props9 = [P('fond9', 'tacheBox', pos=[0.0, 2.0, 4.0], opts={'w': 12.0, 'h': 4.0, 'd': 0.1, 'color': '#E9E1CC'}),
          P('tableau9', 'grinBoard', pos=[-0.8, 2.6, 3.92], ry=180, opts={'w': 3.0, 'h': 0.95, 'lines': ['BAC', 'ÉPREUVE DE GRINCEMENT']}),
          P('bureau9', 'table', pos=DESK9, opts={'w': 1.3, 'd': 0.6, 'h': 0.76, 'color': '#7A5C3A', 'legs': '#5C4330'}), BAG('sachet9', BAG9, scale=1.3)]
for i, (n, p, dp) in enumerate(CAND):
    props9.append(P(f'petiteporte9_{i}', 'grinMiniDoor', pos=dp, ry=0, opts={'beats': BEATS9, 'amp': 1.25, 'color': ['#2F7F8C', '#B5402F', '#2F62B5', '#5E8C4A', '#C98A2E', '#7A4A8A'][i]}))
    props9.append(SQUEAK('S09', f'grince9_{i}', add(dp, [-0.17, 0.42, 0.0]), BEATS9, size=0.6, side=-1 if dp[0] < -0.8 else 1, gain=0.1 if i else 0.34))
st.shot('S09', 'classroom', setOpts={'board': 'BAC', 'board2': 'Épreuve de grincement', 'board3': 'Durée : 4 h'},
        actors=[*[act(n, p, 180, 'sit', 'neutral', keys=CANDK(i, p, dp)) for i, (n, p, dp) in enumerate(CAND)], act('surveillante', INV9, RYI9, 'stand', 'neutral', keys=INVK)],
        props=props9, cams=[C9])
st.cue('clack', 'S09', r(BEATS9[0] - 0.05), 0.15); st.cue('clack', 'S09', r(BEATS9[1] - 0.05), 0.15)

# 10: the neighbour failed three times; he moved out. In his nightcap, the neighbour walks toward us out of his front garden carrying a box to a
#     moving van at the kerb; taped to the box, facing us, his exam sheet: BAC and three red 0/20; behind him, down the street, the hero's open door
#     squeaks in the wind
D10 = st.dur('S10'); REC10 = W('S10', 'L10', 4); DEM10 = W('S10', 'L10', 9)
N10A = [-2.0, 0.0, 4.0]; N10B = [-1.0, 0.0, 5.6]; RYN10 = yaw(N10A, N10B)
VAN10 = [3.5, 0.0, 7.2]
SQ10 = [0.575, 2.0, 0.08]
F10 = [1.0, 2.0, 11.5]; L10 = [-0.7, 1.24, 2.4]
C10 = cam(0.0, F10, add(F10, [-0.05, 0.0, -0.4]), L10, add(L10, [0.0, 0, 0.3]), lens=50, ease='inOut')
chkc('S10', C10, {'headA': add(N10A, [0, 2.45, 0]), 'headB': add(N10B, [0, 2.45, 0]), 'boxB': add(N10B, [0, 1.15, 0.45]), 'feetB': N10B, 'hingeSq': SQ10, 'sqTip': add(SQ10, [-0.8, 0.25, 0]), 'doorL': [-0.575, 1.3, 0], 'vanRear': add(VAN10, [-2.6, 1.5, 0]), 'blockEdge': [-0.9, 1.5, 3.5]})
chkc('S10', C10, {'headB': add(N10B, [0, 2.45, 0]), 'boxB': add(N10B, [0, 1.15, 0.45]), 'hingeSq': SQ10, 'doorL': [-0.575, 1.3, 0]}, end=True)
BOXH = {'touch': {'L': ['torso', 0.42, 0.15, 0.5], 'R': ['torso', -0.42, 0.15, 0.5]}, 'hands': {'L': 'open', 'R': 'open'}, 'hip': 0}
NF10 = {'lid': 0.55, 'mouth': 'line_m6', 'brow': -0.5}
VOIS10 = [k(-0.4, look='camera'), k(0.0, toon={**BOXH, 'face': NF10}, toonDur=0.0), k(0.0, to=N10B, dur=r(D10 - 0.15), clip='walk', face=RYN10, ease='linear'),
          *life(0.2, D10, NF10, BOXH, period=0.6, blinks=[r(REC10 + 0.2)]), k(r(DEM10), look=add(VAN10, [-2.0, 1.5, 0]), lookDur=0.3)]
st.shot('S10', 'grassland', setOpts=SET, actors=[act('voisin', N10A, RYN10, 'stand', 'neutral', keys=VOIS10)],
        props=[*STREET(10, nb=True), FACADE('maison10', open_=1.35, rattle=[[0.5, 0.12, 12, 2.0], [r(DEM10 - 0.2), 0.12, 12, 2.0]]),
               P('bonnet10', 'nightCap', on={'actor': 'voisin', 'joint': 'head', 'offset': [0, 0.5, 0], 'rot': [0, 0, 0.15]}),
               P('carton10', 'cardboardBox', on={'actor': 'voisin', 'joint': 'torso', 'offset': [0, -0.15, 0.48]}, opts={'text': ''}),
               P('copie10', 'grinExamSheet', on={'actor': 'voisin', 'joint': 'torso', 'offset': [0, 0.12, 0.78], 'face': 'camera'}, scale=1.35),
               P('camion10', 'deliveryVan', pos=VAN10, ry=0, opts={'text': 'DÉMÉNAGEMENT'}),
               SQUEAK('S10', 'grince10', SQ10, [0.55, r(DEM10 - 0.15)], size=0.95, side=-1, amp=[1.0, 1.1])],
        cams=[C10])
for t_ in (0.3, 0.9, 1.5, 2.1, 2.7): st.cue('sfx:stepSoft', 'S10', t_, 0.15)

# 11: the president gave his wishes squeaking. A formal office, no flag, no emblem: the president in a plain dark suit at his desk looks gravely
#     into the lens and slowly swings a little ornate door set on the desk, his mouth opening with each squeak; the oil can in its sealed bag lies on
#     the corner of the desk, within reach
D11 = st.dur('S11'); VOE11 = W('S11', 'L11', 5); GRC11 = W('S11', 'L11', 7)
PRES = [0.0, 0.02, -1.45]; DESK11 = [0.0, 0.0, -0.95]; DTOP = 0.79
MD11 = [0.38, DTOP, -0.75]
BAG11 = [-0.5, r(DTOP + 0.31), -0.72]
SQT11 = [0.55, r(VOE11), r(GRC11 + 0.1)]
SW11 = [[0.0, 0.0]]
for t_ in SQT11: SW11 += [[r(t_ - 0.3), 0.05], [r(t_ + 0.05), 0.95], [r(t_ + 0.45), 0.2]]
def MDEDGE(a): return [r(MD11[0] - 0.17 + 0.3 * math.cos(a)), r(MD11[1] + 0.32), r(MD11[2] - 0.3 * math.sin(a))]
def sw_at(t_):
    if t_ <= SW11[0][0]: return SW11[0][1]
    for i in range(1, len(SW11)):
        if t_ < SW11[i][0]: u = (t_ - SW11[i - 1][0]) / (SW11[i][0] - SW11[i - 1][0]); u = u * u * (3 - 2 * u); return SW11[i - 1][1] + (SW11[i][1] - SW11[i - 1][1]) * u
    return SW11[-1][1]
F11 = [0.0, 1.55, 3.0]; L11 = [0.0, 1.33, -0.5]
C11 = cam(0.0, F11, add(F11, [0.0, -0.02, -0.4]), L11, add(L11, [0, 0.0, 0]), lens=36, ease='inOut')
chkc('S11', C11, {'head': add(PRES, [0, 1.95, 0]), 'chin': add(PRES, [0, 1.38, 0]), 'mini': add(MD11, [0, 0.55, 0]), 'bag': add(BAG11, [0, 0.31, 0]), 'bagBot': add(BAG11, [0, -0.3, 0]), 'deskL': [-1.1, DTOP, -0.45], 'deskR': [1.1, DTOP, -0.45], 'sq': [0.21, 1.35, -0.73]})
PF11 = {'lid': 0.3, 'mouth': 'line', 'brow': 0.35}
PK11 = lambda a: {'reach': {'L': R5(MDEDGE(a), 1, 0.0), 'R': R5([-0.3, r(DTOP + 0.06), -0.75], 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'open'}, 'hip': 0}
PRESK = [k(-0.4, look='camera'), k(0.0, toon={**PK11(0.0), 'face': PF11}, toonDur=0.0)]
tt = 0.1
while tt < D11 - 0.05:
    sq_ = any(abs(tt - s_) < 0.12 for s_ in SQT11)
    PRESK.append(k(r(tt), toon={**PK11(sw_at(tt + 0.08)), 'face': {**PF11, 'mouth': 'O', 'jaw': 0.45} if sq_ else PF11}, toonDur=0.08))
    tt += 0.1
st.shot('S11', 'whiteVoid', setOpts={'color': '#5A3E2E'}, actors=[act('president', PRES, 0, 'sit', 'neutral', keys=PRESK)],
        props=[P('mur11', 'grinOfficeWall', pos=[0, 0, -2.3]), P('bureau11', 'grinDesk', pos=DESK11), P('fauteuil11', 'chair', pos=[0, 0, -1.6], opts={'color': '#6A2A22'}),
               P('petiteporte11', 'grinMiniDoor', pos=MD11, opts={'ornate': True, 'swing': SW11, 'w': 0.34, 'h': 0.5}), BAG('sachet11', BAG11),
               SQUEAK('S11', 'grince11', [0.21, 1.35, -0.73], SQT11, size=0.42, side=-1, amp=[0.9, 1.0, 1.1], gain=0.3)],
        cams=[C11])

# 12: ten years later the dictionary is out. A grand library hall: the three linguists, white beards to the belt, set a huge leather dictionary down
#     on a lectern together; a few people applaud on both sides
D12 = st.dur('S12'); DIX12 = W('S12', 'L12', 0); DIC12 = W('S12', 'L12', 5)
LECT = [0.0, 0.0, -0.6]; BOOKC = [0.0, 1.21, -0.6]
LV = [[-0.85, 0.0, -0.85], [0.0, 0.0, -1.3], [0.85, 0.0, -0.85]]; RYV = [35, 0, -35]
CROWD12 = [('public1', [-1.0, 0.0, 0.6], 50), ('public2', [-1.45, 0.0, -2.1], 30), ('public3', [1.12, 0.0, 0.6], -50), ('public4', [1.5, 0.0, -2.1], -30)]
SET12 = r(DIC12 - 0.2)
BOOKK = [k(0.2, to=add(BOOKC, [0, 0.3, 0]), dur=r(SET12 - 0.25), ease='inOut'), k(SET12, to=BOOKC, dur=0.12, ease='in'), k(r(SET12 + 0.12), squash=[1.08, 0.85, 1.08], dur=0.35)]
F12 = [0.1, 2.0, 5.6]; L12 = [0.05, 1.45, 0.0]
C12 = cam(0.0, F12, add(F12, [0.0, 0.0, -0.35]), L12, add(L12, [0, 0.03, 0]), lens=46, ease='inOut')
pts12 = {f'v{i}': add(p, [0, 2.3, 0]) for i, p in enumerate(LV)}; pts12.update({n: add(p, [0, 2.3, 0]) for n, p, _ in CROWD12}); pts12.update({'book': add(BOOKC, [0, 0.2, 0]), 'beardTip': add(LV[0], [0, 0.95, 0.2])})
chkc('S12', C12, pts12)
VF = {'lid': 0.35, 'mouth': 'line', 'brow': 0.4}
def VK(i):
    g0 = add(BOOKC, [(-0.42, 0.0, 0.42)[i], 0.42, (0.15, -0.3, 0.15)[i]]); g1 = add(g0, [0, -0.3, 0])
    keep = lambda g: {'reach': {'R': R5(add(g, [0.1, 0, 0]), 1, 0.0), 'L': R5(add(g, [-0.1, 0, 0]), 1, 0.0)}, 'hands': {'L': 'grip', 'R': 'grip'}, 'hip': 0}
    return [k(-0.4, look=BOOKC), k(0.0, toon={**keep(g0), 'face': VF}, toonDur=0.0), k(0.2, toon={**keep(add(g0, [0, -0.05, 0])), 'face': VF}, toonDur=r(SET12 - 0.25), toonEase='inOut'),
            k(SET12, toon={**keep(g1), 'sq': [1.03, 0.97, 1.03], 'face': VF}, toonDur=0.12), k(r(SET12 + 0.3), toon={'face': {**VF, 'mouth': 'smile'}, 'hip': 0}, toonDur=0.3),
            k(r(SET12 + 0.35), look='camera', lookDur=0.2)]
def CLAP(p, ry, ph):
    ks = [k(-0.4, look=BOOKC), k(0.0, toon={'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.5}, 'hip': 0}, toonDur=0.0)]
    t_, i = r(SET12 + 0.05 + ph), 0
    while t_ < D12 - 0.05:
        c = off(p, ry, 0.38, 0.0, 1.25 + 0.03 * (i % 2)); w_ = 0.02 if i % 2 == 0 else 0.13
        ks.append(k(r(t_), toon={'reach': {'L': R5(off(c, ry, 0, -w_), 1, 0.0), 'R': R5(off(c, ry, 0, w_), 1, 0.0)}, 'hands': {'L': 'open', 'R': 'open'}, 'face': {'lid': 0.2, 'mouth': 'smile', 'brow': 0.5}, 'hip': 0}, toonDur=0.06))
        t_ += 0.11; i += 1
    return ks
props12 = [P('bib12a', 'grinBookcase', pos=[-2.2, 0, -3.2], opts={'w': 3.0, 'h': 3.6}), P('bib12b', 'grinBookcase', pos=[1.2, 0, -3.2], opts={'w': 3.0, 'h': 3.6}), P('bib12c', 'grinBookcase', pos=[4.2, 0, -3.2], opts={'w': 3.0, 'h': 3.6}),
           P('pupitre12', 'grinLectern', pos=LECT, opts={'h': 1.15, 'tilt': 0.0}), P('dico12', 'grinBook', pos=add(BOOKC, [0, 0.3, 0]), opts={'closed': True, 'w': 1.8, 'd': 1.15, 'thick': 0.36}, keys=BOOKK)]
for i in range(3): props12.append(P(f'barbe12_{i}', 'longBeard', on={'actor': f'lingV{i + 1}', 'joint': 'head', 'offset': [0, 0.05, 0.12], 'hang': True}, opts={'len': 1.05, 'w': 0.24, 'color': '#F2F2EE', 'wave': [0.04, 3.0]}))
st.shot('S12', 'whiteVoid', setOpts={'color': '#C9B48E'}, actors=[*[act(f'lingV{i + 1}', LV[i], RYV[i], 'stand', 'neutral', keys=VK(i)) for i in range(3)], *[act(n, p, ry, 'stand', 'happy', keys=CLAP(p, ry, 0.03 * j)) for j, (n, p, ry) in enumerate(CROWD12)]],
        props=props12, cams=[C12])
st.cue('thud', 'S12', r(SET12 + 0.1), 0.3)

# 13: a thousand pages; one word. Top-down on the open dictionary on a dark table: blank pages flip past right to left, faster, then stop on one page
#     with one big word in the middle: IIIIIK
D13 = st.dur('S13'); MOT13 = W('S13', 'L13', 4)
BOOK13 = [0.0, 0.8, 0.0]
FL13 = [0.05, r(MOT13 - 0.25), 16]
F13 = [0.2, 2.75, 0.55]; L13 = [0.2, 0.88, 0.0]
C13 = cam(0.0, F13, add(F13, [0.03, -0.12, -0.02]), L13, add(L13, [0.03, 0, 0]), lens=34, ease='inOut')
chk('S13', F13, L13, 34, {'wordL': [0.04, 0.89, -0.14], 'wordR': [0.42, 0.89, -0.14], 'pageTop': [0.22, 0.89, -0.3], 'pageBot': [0.22, 0.89, 0.3], 'spine': [0.0, 0.89, 0.0], 'leftPage': [-0.3, 0.89, 0.0]})
st.shot('S13', 'whiteVoid', setOpts={'color': '#3A2A22'}, actors=[], props=[P('table13', 'tacheBox', pos=[0, 0.77, 0], opts={'w': 2.2, 'h': 0.06, 'd': 1.6, 'color': '#5A3A28'}),
        P('dico13', 'grinBook', pos=BOOK13, opts={'flip': FL13, 'w': 0.9, 'd': 0.62})], cams=[C13])
for i in range(8): st.cue('sfx:paper', 'S13', r(0.06 + i * (FL13[1] - 0.05) / 8), 0.12)
st.cue('thud', 'S13', r(FL13[1] + 0.05), 0.15)

# 14: it means « de l'huile ». The same page, a snap zoom tighter: under IIIIIK the definition « de l'huile » and a big oil drop write in; TRADUIT
D14 = st.dur('S14'); DIR14 = W('S14', 'L14', 2); HUI14 = W('S14', 'L14', 4)
DEF14 = r(DIR14 + 0.1)
F14B = [0.22, 2.12, 0.3]; L14 = [0.22, 0.88, -0.01]
C14 = cam(0.0, add(F13, [0.03, -0.12, -0.02]), add(F13, [0.03, -0.12, -0.02]), add(L13, [0.03, 0, 0]), add(L13, [0.03, 0, 0]), lens=34)
C14B = glide([cam(0.04, F14B, add(F14B, [0, -0.04, -0.01]), L14, add(L14, [0, 0, 0.01]), lens=34, ease='out')], 0.1)
chk('S14', F14B, L14, 34, {'wordL': [0.04, 0.89, -0.14], 'wordR': [0.42, 0.89, -0.14], 'defL': [0.04, 0.89, 0.02], 'defR': [0.4, 0.89, 0.02], 'drop': [0.22, 0.89, 0.15], 'dropBot': [0.22, 0.89, 0.2], 'pageTop': [0.22, 0.89, -0.3]})
st.shot('S14', 'whiteVoid', setOpts={'color': '#3A2A22'}, actors=[], props=[P('table14', 'tacheBox', pos=[0, 0.77, 0], opts={'w': 2.2, 'h': 0.06, 'd': 1.6, 'color': '#5A3A28'}),
        P('dico14', 'grinBook', pos=BOOK13, opts={'defAt': DEF14, 'w': 0.9, 'd': 0.62})], cams=[C14, C14B])
st.cue('whoosh', 'S14', 0.0, 0.15, 0.25, 600, 3000); st.cue('sfx:scratch', 'S14', DEF14, 0.2)
st.card('S14', 'TRADUIT', at=r(HUI14 + 0.05))

# 15: so the president wished the whole country oil. A family on the sofa watches the replay: over their heads the television fills the top half;
#     inside it the little president swings his little door and a speech bubble with a big oil drop pops out of the hinge toward us (no words); cut
#     round to the family: they nod slowly, together
D15 = st.dur('S15'); SOU15 = W('S15', 'L15', 4); HUI15 = W('S15', 'L15', 6); A15 = W('S15', 'L15', 7)
TV = [0.0, 0.0, -2.4]; TVY, TVH, TVW = 1.0, 0.95, 1.5
PT = 0.45
PRES15 = [0.0, r(TVY + 0.01), -3.0]
DESK15 = [0.0, TVY, -2.7]
MD15 = [0.2, r(TVY + 0.351), -2.62]
FAM = [('pere', [-0.5, 0.1, 0.85]), ('mere', [0.1, 0.1, 0.85]), ('enfant', [0.62, 0.1, 0.88])]
POP15 = r(HUI15 - 0.1)
SW15 = [[0.0, 0.0], [r(POP15 - 0.35), 0.05], [r(POP15), 0.95], [r(POP15 + 0.5), 0.3]]
F15 = [-0.17, 3.0, 3.6]; L15A = [0.0, 1.27, -1.0]
C15 = cam(0.0, F15, add(F15, [0, -0.03, -0.3]), L15A, add(L15A, [0, 0.02, 0]), lens=36, ease='inOut')
F15B = [1.0, 1.47, -2.0]; L15B = [0.2, 1.4, 0.5]
C15B = cam(r(A15 - 0.05), F15B, add(F15B, [-0.05, 0, 0.12]), L15B, add(L15B, [0, 0.01, 0]), lens=56, ease='out')
chkc('S15', C15, {'tvTop': [0, TVY + TVH + 0.1, -2.4], 'tvBot': [0, TVY - 0.1, -2.4], 'tvL': [-0.85, 1.5, -2.4], 'tvR': [0.85, 1.5, -2.4], 'bubble': [0.55, 1.8, -2.2], 'presHead': [0, 1.85, -3.0], 'pereHead': [-0.5, 1.85, 0.85], 'mereHead': [0.1, 1.8, 0.85]})
chkc('S15', C15B, {'pere': [-0.5, 1.85, 0.85], 'mere': [0.1, 1.8, 0.85], 'enfant': [0.62, 1.4, 0.88], 'chin': [0.1, 1.35, 0.85]})
FAMF = {'lid': 0.45, 'mouth': 'line', 'brow': 0.1}
def FAMK(i):
    ks = [k(-0.4, look=[0, 1.5, -2.4]), k(0.0, toon={'face': FAMF, 'hip': 0}, toonDur=0.0), *life(0.1 + 0.1 * i, r(A15 - 0.1), FAMF, {'hip': 0})]
    for j, t_ in enumerate([r(A15 + 0.1), r(A15 + 0.5), r(A15 + 0.9)]):
        ks.append(k(r(t_ + 0.04 * i), toon={'bend': {'neck': [0.3 if j % 2 == 0 else -0.04, 0, 0, 1, None]}, 'face': FAMF, 'hip': 0}, toonDur=0.3, toonEase='inOut'))
    return ks
MDH = lambda dz: R5([MD15[0] + 0.03, MD15[1] + 0.1, MD15[2] + dz], 1, 0.0)
PRES15K = [k(-0.4, look='camera'), k(0.0, toon={'reach': {'L': MDH(-0.02)}, 'hands': {'L': 'grip'}, 'face': PF11, 'hip': 0}, toonDur=0.0),
           k(r(POP15 - 0.05), toon={'reach': {'L': MDH(-0.06)}, 'hands': {'L': 'grip'}, 'face': {**PF11, 'mouth': 'O', 'jaw': 0.45}, 'hip': 0}, toonDur=0.1),
           k(r(POP15 + 0.4), toon={'reach': {'L': MDH(-0.02)}, 'hands': {'L': 'grip'}, 'face': PF11, 'hip': 0}, toonDur=0.2)]
st.shot('S15', 'livingRoom', setOpts={'sofa': False, 'tv': False, 'carpet': False, 'picture': False},
        actors=[act('presidentTV', PRES15, 0, 'sit', 'neutral', scale=PT, keys=PRES15K), *[act(n, p, 180, 'sit', 'neutral', keys=FAMK(i), **({'scale': 0.68} if n == 'enfant' else {})) for i, (n, p) in enumerate(FAM)]],
        props=[P('tele15', 'grinTV', pos=TV, opts={'w': TVW, 'h': TVH, 'y': TVY, 'depth': 0.9}), P('bureau15', 'grinDesk', pos=DESK15, scale=PT),
               P('petiteporte15', 'grinMiniDoor', pos=MD15, scale=0.6, opts={'ornate': True, 'swing': SW15}),
               P('bulle15', 'grinBubble', pos=[0.12, 1.3, -2.25], face='camera', opts={'w': 0.62, 'popAt': POP15, 'tail': 'left'}),
               P('canape15', 'sofaProp', pos=[0.0, 0.0, 0.9], ry=180, opts={'color': '#2F7F8C', 'color2': '#5BA3AE'})],
        cams=[C15, C15B])
st.cue('sfx:squeak', 'S15', POP15, 0.22); st.cue('pop', 'S15', r(POP15 + 0.05), 0.25)

# 16: the oil can is still under seal. The evidence room: a bare grey shelf, on it the oil can alone in its sealed bag, under one bare bulb that
#     swings slowly; off screen, far away, a squeak; hold, deadpan
D16 = st.dur('S16'); SCE16 = W('S16', 'L16', 5)
SHELF = [0.0, 0.0, -0.55]; BAG16 = [0.05, 1.42, -0.5]
F16 = [0.42, 1.55, 1.55]; L16 = [0.05, 1.42, -0.5]
C16 = cam(0.0, F16, add(F16, [-0.05, 0.0, -0.35]), L16, add(L16, [0, 0.01, 0]), lens=40, ease='inOut')
chkc('S16', C16, {'bagTop': add(BAG16, [0, 0.31, 0]), 'bagBot': add(BAG16, [0, -0.31, 0]), 'bulb': [0.05, 2.0, 0.1], 'shelfL': [-1.2, 1.1, -0.55]})
chkc('S16', C16, {'bagTop': add(BAG16, [0, 0.31, 0]), 'bagBot': add(BAG16, [0, -0.31, 0])}, end=True)
st.shot('S16', 'whiteVoid', setOpts={'color': '#3E4450'}, look={'fill': 0.7}, actors=[],
        props=[P('etagere16', 'chvBagShelf', pos=SHELF, opts={'n': 0, 'w': 2.4, 'h': 2.0}), BAG('sachet16', BAG16),
               P('ampoule16', 'cellBulb', pos=[0.05, 2.75, 0.1], opts={'drop': 0.75, 'swing': 0.22, 'power': 4.5, 'range': 5})],
        cams=[C16])
st.cue('sfx:squeak', 'S16', 1.9, 0.09)

print('\n'.join(CHECKS))

TOON = {'breathe': 1.7, 'holdLife': 1.6}
MEC = {'preset': 'lemec', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}, 'toon': TOON}
LINGB = {'preset': 'boss', 'outfit': 'suit', 'suit': '#8A6E4A', 'pants': '#6E583A', 'lapel': '#6E583A', 'shirt': '#F2EDE4', 'tie': '#2E5A3A', 'cuff': '#8A6E4A', 'hat': 'none', 'glasses': True, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
# (round 1 fix) a lighter blue tunic over navy trousers, so the gendarmes do not merge with the hero's navy suit (no insignia)
GEND = {'preset': 'cop', 'outfit': 'suit', 'suit': '#5A79A8', 'pants': '#1A2438', 'shirt': '#E4E8F0', 'lapel': '#45628E', 'tie': '#1A2438', 'cuff': '#5A79A8', 'hat': 'none', 'hair': 'crew', 'facial': 'none', 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
CANDB = {'preset': 'boss', 'outfit': 'suit', 'hat': 'none', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2}, 'toon': EX}
PRESB = {'preset': 'politique', 'seed': 9811, 'suit': '#23262C', 'lapel': '#23262C', 'tie': '#2C3E5C', 'hairColor': '#BDBDBD', 'glasses': False, 'build': {'width': 1.0, 'headWidth': 1.2, 'belly': 0.08}, 'toon': EX}
st.write("Le grincement", rig='toon', fingers=False, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, hairRest=0.07, extra_cast={
    'mec': MEC,
    'mecHiver': {**MEC, 'hat': 'none'},
    'voisin': {'preset': 'pyjama', 'seed': 9801, 'suit': '#9CC2E6', 'pants': '#9CC2E6', 'hair': 'receding', 'hairColor': '#6A5A4A', 'facial': 'mustache', 'glasses': False, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
    'ling1': {**LINGB, 'seed': 9802, 'hair': 'receding', 'hairColor': '#5A3A28', 'facial': 'mustache'},
    'ling2': {**LINGB, 'seed': 9803, 'hair': 'bun', 'hairColor': '#3A2A20', 'facial': 'none', 'suit': '#7A5E3E', 'lipstick': True},
    'ling3': {**LINGB, 'seed': 9804, 'hair': 'bald', 'facial': 'beard', 'beardColor': '#6A4A2A', 'suit': '#957A52'},
    'lingV1': {**LINGB, 'seed': 9802, 'hair': 'receding', 'hairColor': '#EDEDE8', 'facial': 'none'},
    'lingV2': {**LINGB, 'seed': 9803, 'hair': 'bun', 'hairColor': '#EDEDE8', 'facial': 'none', 'suit': '#7A5E3E', 'lipstick': True},
    'lingV3': {**LINGB, 'seed': 9804, 'hair': 'bald', 'facial': 'none', 'suit': '#957A52'},
    'officiel': {'preset': 'politique', 'seed': 9805, 'suit': '#6E7480', 'lapel': '#5A606C', 'tie': '#7A2E3A', 'hairColor': '#8A8A8A', 'glasses': True, 'sash': ['#6A3A9A', '#E2B53C'], 'sashW': 0.15, 'build': {'width': 1.05, 'headWidth': 1.2, 'belly': 0.1}, 'toon': EX},
    'gendarme1': {**GEND, 'seed': 9806, 'facial': 'mustache'},
    'gendarme2': {**GEND, 'seed': 9807},
    'passant1': {'preset': 'femme', 'seed': 9808, 'suit': '#D9A030', 'lapel': '#F4F0E4', 'hat': 'none', 'hair': 'long', 'hairColor': '#2A1E18', 'glasses': False, 'build': {'width': 0.95, 'headWidth': 1.2, 'height': 0.95}, 'toon': EX},
    'passant2': {**CANDB, 'seed': 9809, 'suit': '#5E8C4A', 'lapel': '#4A7038', 'shirt': '#F4F4F0', 'tie': '#C8322A', 'hat': 'none', 'facial': 'beard', 'beardColor': '#3A2A20'},
    'candidat1': {**CANDB, 'seed': 9821, 'suit': '#4E545E', 'hair': 'crew'}, 'candidat2': {'preset': 'femme', 'seed': 9822, 'suit': '#B5402F', 'hair': 'bun', 'glasses': True, 'build': {'width': 0.95, 'headWidth': 1.2, 'height': 0.95}, 'toon': EX},
    'candidat3': {**CANDB, 'seed': 9823, 'suit': '#2F62B5', 'facial': 'mustache', 'hair': 'receding', 'hairColor': '#8A8A86'}, 'candidat4': {**CANDB, 'seed': 9824, 'suit': '#5E8C4A', 'hair': 'slick', 'skin': '#8A5A3A', 'faceRim': True},
    'candidat5': {'preset': 'mamie', 'seed': 9825, 'toon': EX}, 'candidat6': {**CANDB, 'seed': 9826, 'suit': '#7A4A8A', 'hair': 'afro', 'hairColor': '#2A1E18', 'skin': '#6A4430', 'faceRim': True},
    'surveillante': {'preset': 'journaliste', 'seed': 9827, 'suit': '#3A5A8C', 'glasses': True, 'toon': EX},
    'president': PRESB, 'presidentTV': PRESB,
    'public1': {**CANDB, 'seed': 9831, 'suit': '#8A3A2A', 'hair': 'crew'}, 'public2': {'preset': 'femme', 'seed': 9832, 'suit': '#2E5A48', 'hair': 'bun', 'build': {'width': 0.95, 'headWidth': 1.2, 'height': 0.95}, 'toon': EX},
    'public3': {**CANDB, 'seed': 9833, 'suit': '#2C4A7A', 'facial': 'mustache', 'hair': 'receding'}, 'public4': {'preset': 'mamie', 'seed': 9834, 'suit': '#C9729A', 'toon': EX},
    'pere': {**CANDB, 'seed': 9841, 'suit': '#C98A2E', 'shirt': '#F4F4F0', 'tie': '#2F62B5', 'hair': 'crew', 'facial': 'stubble'},
    'mere': {'preset': 'femme', 'seed': 9842, 'suit': '#7A4A8A', 'hair': 'long', 'hairColor': '#5A3A28', 'glasses': False, 'build': {'width': 0.95, 'headWidth': 1.2, 'height': 0.95}, 'toon': EX},
    'enfant': {'preset': 'gamin', 'seed': 9843, 'suit': '#E8742E', 'hat': 'none', 'toon': EX},
})
