#!/usr/bin/env python3
"""La photocopieuse (story 49, cycle 11 of the cartoon staging): this man sat on the photocopier. It copied him whole. The copy came out of the
tray. Human resources hired it. A copy costs only paper. So they ran off five hundred. Double-sided, to save. Him, he was fired. Reason: not
conforming to the original. Too thick. He filed a complaint. It was photocopied in five hundred copies. Since then he puts paper in the machine.
Staging: every gag treats him as an office original: the green scan that climbs over him from his seat to the top of his head, his hair standing on
end; the copy that slides out of the tray flat as a sheet, falls and springs up, black and white and thin as paper, fluttering; the handshake with a
paper arm that waves like a ribbon; the price board; the machine spitting copies of him across the office in rows; the copy that turns round with
his face printed on the back; the cardboard box; NON CONFORME stamped on his forehead (his eyes cross on it); the caliper on his chest beside a
copy thin as a line; the complaint slapped on the desk; buried up to the chin in its five hundred copies; on his knees at the paper drawer.
Natural look; cycle 11 tools: life in the holds (holdLife), varied takes (take())."""
from story_kit import *
import math

st = Story('photocopie', look='natural')
st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L03', 0), ('S04', 'L04', 0), ('S05', 'L05', 0), ('S06', 'L06', 0), ('S07', 'L07', 0), ('S08', 'L08', 0),
         ('S09', 'L09', 0), ('S10', 'L09b', 0), ('S11', 'L10', 0), ('S12', 'L11', 0), ('S13', 'L12', 0)])

PI = math.pi
def FC(t, frm, pts, top=0.14, bottom=0.76, drift=(0.0, 0.0, 0.0), lenses=range(22, 70), **kw):
    frm, look, lens = fitBack(list(frm), pts, top=top, bottom=bottom, lenses=lenses, **kw)
    if lens is None: raise SystemExit(f'no lens fits from {frm}')
    return cam(t, list(frm), r3([frm[i] + drift[i] for i in range(3)]), look, r3([look[i] + drift[i] for i in range(3)]), lens=lens)
def FWDV(ry): return (math.sin(math.radians(ry)), math.cos(math.radians(ry)))
def OFF(p, ry, fwd=0.0, rgt=0.0, y=0.0):                           # a point in front of / to the right of someone facing ry
    f = FWDV(ry); r = (-f[1], f[0]); return [round(p[0] + fwd * f[0] + rgt * r[0], 3), y, round(p[2] + fwd * f[1] + rgt * r[1], 3)]

OF = {'door': False, 'printer': False}                              # the office, its right corner free for the copier
CP = [2.6, 0, -2.95]                                                # the photocopier against the back wall (front +Z, glass at 0.96, tray on its right)
TRAY = [round(CP[0] + 0.88, 3), 0.6, CP[2]]
SEAT = [CP[0], 0.44, round(CP[2] + 0.05, 3)]                         # sitting on its glass (the sit clip drops the hips 0.45)
DESK = [-0.6, 0, -1.7]; DRH = [-0.6, 0, -2.35]                      # the HR desk and her chair behind it
FLAT = {'sq': [1.0, 1.0, 0.05]}                                     # a copy: as thin as paper
FLUT = lambda a=1.0: {**FLAT, 'wave': {'spine': [round(0.05 * a, 3), 1.5, 0.0, 1, 0.0]}}   # a paper flutter
COPIER = lambda **o: P('copier', 'photocopier', pos=CP, opts={'lid': 1.25, **o})

# 1: the hook. He hops up onto the photocopier and sits on its glass, the lid open behind him, bored
D1 = st.dur('S01'); UP1 = round(st.at('S01', 'L01', 3) - 0.12, 3)
st.shot('S01', 'office', setOpts=OF, actors=[
        act('mec', [CP[0], 0, round(CP[2] + 0.85, 3)], 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'),
            k(round(UP1 - 0.12, 3), toon={'sq': [1.07, 0.9, 1.07]}, toonDur=0.08, toonEase='in'),   # a crouch...
            k(UP1, to=SEAT, dur=0.28, clip='sit', then='sit', ease='out', face=0), k(UP1, toon={'sq': [0.92, 1.1, 0.92]}, toonDur=0.06),   # ...up he hops
            k(round(UP1 + 0.28, 3), toon={'sq': [1.08, 0.9, 1.08], 'face': {'lid': 0.4}}, toonDur=0.04), k(round(UP1 + 0.4, 3), toon={'face': {'lid': 0.45}}, toonDur=0.1),   # and lands on the glass, heavy-lidded
            k(round(UP1 + 0.9, 3), look=[round(CP[0] - 1.0, 3), 1.6, 0.5])])],
        props=[COPIER()],
        cams=[FC(0.0, [round(CP[0] - 1.6, 3), 1.35, 1.4], [[CP[0], 2.5, CP[2]], [CP[0], 0.0, round(CP[2] + 0.85, 3)], [round(CP[0] + 0.6, 3), 1.0, CP[2]], [round(CP[0] - 0.6, 3), 1.0, CP[2]]], top=0.12, bottom=0.74, drift=(0.04, 0, -0.08))])
st.cue('sfx:spring', 'S01', UP1 + 0.28, 0.3)

# 2: it photocopied him whole. The light bar sweeps the glass under him, then a sheet of green light climbs over him from his seat to the top of his
#    head: his hair stands on end as it passes
D2 = st.dur('S02'); SC2 = round(st.at('S02', 'L02', 2) - 0.1, 3)
SIT2 = {'face': {'lid': 0.45}}
st.shot('S02', 'office', setOpts=OF, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=SIT2, toonDur=0.0),
            k(round(SC2 + 0.05, 3), toon={'face': {'lid': 0.0, 'eye': 0.3, 'brow': 0.6}}, toonDur=0.05),   # the flash under him
            *take(round(SC2 + 0.62, 3), 'hair', keep={'face': {'lid': 0.0}}, hold=0.35)])],   # the light passes his head: his hair stands on end
        props=[COPIER(scanAt=SC2, scanDur=0.5), P('scan2', 'scanPlane', pos=[CP[0], 0, round(CP[2] + 0.08, 3)], opts={'w': 1.0, 'd': 0.8, 'y0': 0.97, 'y1': 2.45, 'at': round(SC2 + 0.15, 3), 'dur': 0.6})],
        cams=[FC(0.0, [round(CP[0] - 0.9, 3), 1.55, 0.2], [[CP[0], 2.55, CP[2]], [CP[0], 0.85, CP[2]], [round(CP[0] - 0.55, 3), 1.6, CP[2]], [round(CP[0] + 0.55, 3), 1.6, CP[2]]], top=0.12, bottom=0.74)])
st.cue('sfx:beep', 'S02', SC2 - 0.1, 0.3); st.cue('sfx:zip', 'S02', SC2, 0.35); st.cue('sfx:zip', 'S02', SC2 + 0.15, 0.3)

# 3: the copy came out of the tray. Low at the tray: the copy slides out flat on its back, head first, black and white, drops to the floor and springs up
#    as thin as paper, fluttering; behind, on the glass, his jaw drops
D3 = st.dur('S03'); OUT3 = round(st.at('S03', 'L03', 1) - 0.1, 3); UP3 = round(st.at('S03', 'L03', 3) - 0.05, 3)
COPY3 = [round(TRAY[0] + 0.05, 3), 0, round(CP[2] + 0.4, 3)]
st.shot('S03', 'office', setOpts=OF, actors=[
        act('copie', [round(CP[0] + 0.25, 3), 0.62, CP[2]], -90, 'stiffStand', 'neutral', keys=[k(0.0, look=None), k(0.0, toon={**FLAT, 'lay': [-1.57, 0]}, toonDur=0.0), k(0.0, visible=False),
            k(OUT3, visible=True), k(OUT3, to=[TRAY[0], 0.62, CP[2]], dur=round(UP3 - OUT3 - 0.12, 3), glide=True, ease='out', face=-90),   # out of the tray, head first
            k(round(UP3 - 0.1, 3), to=COPY3, dur=0.12, glide=True, ease='in', face=0),   # onto the floor...
            k(round(UP3 + 0.02, 3), toon={**FLAT, 'lay': [0.2, 0]}, toonDur=0.08, toonEase='out'), k(round(UP3 + 0.12, 3), toon={**FLUT(1.5), 'lay': [-0.08, 0]}, toonDur=0.08),   # ...and it springs up past upright
            k(round(UP3 + 0.24, 3), toon=FLUT(1.0), toonDur=0.1), k(round(UP3 + 0.3, 3), look='camera')]),
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look=[TRAY[0], 0.7, TRAY[2]]), k(0.0, toon={'face': {'lid': 0.3}}, toonDur=0.0), *take(round(UP3 + 0.05, 3), 'jaw', hold=0.4)])],
        props=[COPIER(sheetsAt=[round(OUT3 - 0.05, 3)])],
        cams=[FC(0.0, [round(CP[0] + 1.5, 3), 2.7, round(CP[2] + 2.3, 3)], [[COPY3[0], 2.3, COPY3[2]], [COPY3[0], 0.0, COPY3[2]], [CP[0], 2.3, CP[2]], [round(TRAY[0] + 1.6, 3), 0.62, TRAY[2]]], top=0.12, bottom=0.74, drift=(-0.04, 0, -0.06))])   # (first look) from above: the copy flat as a sheet reads face up (from low it was a line)
st.cue('sfx:paper', 'S03', OUT3, 0.35); st.cue('sfx:spring', 'S03', UP3 + 0.02, 0.35)

# 4: human resources hired it. Her desk: she reaches across and shakes the copy's hand: the paper arm waves like a ribbon; EMBAUCHÉ stamped on the contract
D4 = st.dur('S04'); EMB4 = round(st.at('S04', 'L04', 4) - 0.06, 3)
COPY4 = [round(DESK[0] + 0.25, 3), 0, round(DESK[2] + 0.75, 3)]
HAND4 = [round(DESK[0] + 0.15, 3), 1.15, round(DESK[2] + 0.28, 3)]
st.shot('S04', 'office', setOpts=OF, actors=[
        act('drh', DRH, 0, 'stand', 'happy', keys=[k(0.0, look=[COPY4[0], 1.8, COPY4[2]]), k(0.15, toon={'reach': {'R': [*HAND4[:3], 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.15),
            *[k(round(0.3 + 0.12 * i, 3), toon={'reach': {'R': [HAND4[0], round(HAND4[1] + (0.07 if i % 2 == 0 else -0.05), 3), HAND4[2], 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.1, toonEase='inOut') for i in range(5)],   # a vigorous handshake
            k(round(EMB4 - 0.15, 3), toon={'reach': {'L': [round(DESK[0] - 0.35, 3), 1.25, round(DESK[2] + 0.05, 3), 1, 0.06]}, 'hands': {'L': 'grip'}}, toonDur=0.1), k(EMB4, toon={'reach': {'L': [round(DESK[0] - 0.35, 3), 0.85, round(DESK[2] + 0.05, 3), 1, 0.06]}, 'hands': {'L': 'grip'}}, toonDur=0.04, toonEase='in'),   # and the stamp
            k(round(EMB4 + 0.2, 3), toon={}, toonDur=0.15), k(round(EMB4 + 0.2, 3), look='camera')]),
        act('copie', COPY4, 180, 'stand', 'happy', keys=[k(0.0, look=[DRH[0], 1.9, DRH[2]]), k(0.0, toon=FLUT(0.6), toonDur=0.0),
            *[k(round(0.3 + 0.12 * i, 3), toon={**FLAT, 'reach': {'R': [HAND4[0], round(HAND4[1] + (0.07 if i % 2 == 0 else -0.05), 3), HAND4[2], 1, 0.06]}, 'hands': {'R': 'grip'}, 'wave': {'armR': [0.07, 2.0, i * 0.5, 1, 0.0], 'spine': [0.03, 1.5, i * 0.3, 1, 0.0]}}, toonDur=0.1) for i in range(5)],   # its paper arm rippling
            k(round(EMB4 + 0.2, 3), toon=FLUT(0.6), toonDur=0.15)])],
        props=[P('desk4', 'desk', pos=DESK), P('contract4', 'paperSheet', pos=[round(DESK[0] - 0.35, 3), 0.77, round(DESK[2] + 0.05, 3)], rot=[-PI / 2, 0, 0], opts={'w': 0.3, 'h': 0.4, 'head': 'CONTRAT', 'lines': ['Poste : employé', 'Salaire : papier'], 'lineSize': 0.07, 'paper': '#FFFFFF', 'bright': True, 'stamp': {'text': 'EMBAUCHÉ', 'at': EMB4, 'rot': -0.2, 'y': -0.08, 'w': 0.9}})],
        cams=[FC(0.0, [round(DESK[0] + 2.2, 3), 1.6, round(DESK[2] + 2.0, 3)], [[DRH[0], 2.35, DRH[2]], [COPY4[0], 2.4, COPY4[2]], [COPY4[0], 0.3, COPY4[2]], [round(DESK[0] - 0.5, 3), 0.8, DESK[2]]], top=0.12, bottom=0.74)])
st.cue('sfx:cuff', 'S04', EMB4, 0.4)

# 5: a copy costs only paper. The price board on the wall: HIM 2 400 € / THE COPY 0,02 €; she taps it; he sweats, the copy smiles flat
D5 = st.dur('S05'); CO5 = round(st.at('S05', 'L05', 4) - 0.1, 3)
BOARD = [-2.3, 1.45, -3.5]; ME5 = [-1.3, 0, -2.2]; CPY5 = [-3.3, 0, -2.2]   # (first look) the board between them, above their shoulders
st.shot('S05', 'office', setOpts=OF, actors=[
        act('mec', ME5, -10, 'stand', 'worried', keys=[k(0.0, look=[BOARD[0], 2.1, BOARD[2]]), k(round(CO5 + 0.1, 3), look='camera'), k(round(CO5 + 0.1, 3), toon={'face': {'sweat': 1, 'brow': 0.7}}, toonDur=0.1)]),
        act('copie', CPY5, 10, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon=FLUT(0.6), toonDur=0.0)]),
        act('drh', [-4.2, 0, -2.75], 50, 'stand', 'happy', keys=[k(0.0, look=[BOARD[0], 1.9, BOARD[2]]), k(round(CO5 - 0.2, 3), toon={'reach': {'R': [round(BOARD[0] - 0.25, 3), 1.55, round(BOARD[2] + 0.06, 3), 1, 0.08]}, 'hands': {'R': 'point'}}, toonDur=0.12),
            k(round(CO5 + 0.08, 3), toon={'reach': {'R': [round(BOARD[0] - 0.25, 3), 1.35, round(BOARD[2] + 0.06, 3), 1, 0.08]}, 'hands': {'R': 'point'}}, toonDur=0.06), k(round(CO5 + 0.4, 3), look='camera')])],
        props=[P('board5', 'lcdScreen', pos=BOARD, opts={'w': 1.5, 'h': 0.85, 'stand': 0, 'dark': False, 'pages': [[0.0, ['LUI : 2 400 €', 'COPIE : 0,02 €'], {'big': 0.75, 'accent': '#C8202A'}]]})],
        cams=[FC(0.0, [-2.3, 1.55, 1.2], [[BOARD[0] - 0.8, 2.05, BOARD[2]], [BOARD[0] + 0.8, 2.05, BOARD[2]], [ME5[0], 2.4, ME5[2]], [CPY5[0], 0.4, CPY5[2]], [ME5[0], 0.4, ME5[2]]], top=0.12, bottom=0.74, drift=(0.0, 0.0, -0.1))])
st.cue('sfx:cash', 'S05', CO5, 0.35)

# 6: so they ran off five hundred. Wide on the office: she presses the green button; the machine spits copies of him across the office, landing in rows
D6 = st.dur('S06'); GO6 = round(st.at('S06', 'L06', 4) - 0.35, 3)
GRID = {'x0': -2.6, 'z0': -2.2, 'dx': 0.72, 'dz': 0.75, 'cols': 7}
st.shot('S06', 'office', setOpts=OF, actors=[
        act('drh', [round(CP[0] + 0.35, 3), 0, round(CP[2] + 0.85, 3)], -160, 'stand', 'happy', keys=[k(0.0, look=[CP[0], 1.0, CP[2]]), k(round(GO6 - 0.15, 3), toon={'reach': {'R': [round(CP[0] + 0.35, 3), 1.08, round(CP[2] + 0.33, 3), 1, 0.06]}, 'hands': {'R': 'point'}}, toonDur=0.1),
            k(GO6, toon={'reach': {'R': [round(CP[0] + 0.35, 3), 1.0, round(CP[2] + 0.33, 3), 1, 0.06]}, 'hands': {'R': 'point'}}, toonDur=0.04), k(round(GO6 + 0.25, 3), toon={}, toonDur=0.15), k(round(GO6 + 0.3, 3), look=[-0.5, 1.2, -1.0])])],
        props=[COPIER(lid=0.0), P('copies6', 'copyFountain', pos=[0, 0, 0], opts={'n': 35, 'from': TRAY, 'grid': GRID, 't0': round(GO6 + 0.1, 3), 't1': round(D6 - 0.25, 3), 'flight': 0.5})],
        cams=[FC(0.0, [-3.6, 2.4, 3.2], [[CP[0], 2.0, CP[2]], [GRID['x0'], 2.3, GRID['z0']], [GRID['x0'], 0.0, round(GRID['z0'] + 4 * GRID['dz'], 3)], [round(GRID['x0'] + 6 * GRID['dx'], 3), 0.0, round(GRID['z0'] + 4 * GRID['dz'], 3)]], top=0.1, bottom=0.74, drift=(0.1, 0, -0.1))])
st.cue('sfx:beep', 'S06', GO6, 0.3); [st.cue('sfx:paper', 'S06', round(GO6 + 0.15 + 0.22 * i, 3), 0.2) for i in range(6)]

# 7: double-sided, to save. One copy turns round: his face printed on the back of its head as well, deadpan both ways
D7 = st.dur('S07'); VE7 = round(st.at('S07', 'L07', 1) - 0.2, 3)
CPY7 = [0.3, 0, 1.7]   # (first look) in front of the rows (among them the camera stood inside a cutout)
st.shot('S07', 'office', setOpts=OF, actors=[
        act('copie', CPY7, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon=FLUT(0.6), toonDur=0.0),
            k(VE7, to=[CPY7[0], 0, round(CPY7[2] + 0.01, 3)], dur=0.22, clip='stand', then='stand', face=180), k(round(VE7 + 0.22, 3), toon=FLUT(1.6), toonDur=0.06), k(round(VE7 + 0.32, 3), toon=FLUT(0.6), toonDur=0.15)])],   # it spins round, fluttering
        props=[P('copies7', 'copyFountain', pos=[0, 0, 0], opts={'n': 35, 'start': 35, 'recto': True, 'grid': GRID}), P('back7', 'backFace', on={'actor': 'copie', 'joint': 'head', 'offset': [0.0, 0.24, -0.24], 'rot': [0, PI, 0]}, opts={'w': 0.32, 'h': 0.44})],
        cams=[FC(0.0, [0.55, 1.75, 4.4], [[CPY7[0], 2.45, CPY7[2]], [CPY7[0], 0.6, CPY7[2]], [round(CPY7[0] - 0.55, 3), 1.6, CPY7[2]], [round(CPY7[0] + 0.55, 3), 1.6, CPY7[2]]], top=0.12, bottom=0.74, drift=(0.0, 0.0, -0.08))])
st.cue('whoosh', 'S07', VE7, 0.3, 0.2, 600, 2400)

# 8: him, they fired him. She shoves a cardboard box into his arms (his plant, his mug); behind him the copies stand in their rows
D8 = st.dur('S08'); LIC8 = round(st.at('S08', 'L08', 3) - 0.12, 3)
ME8 = [0.9, 0, 1.75]; HOLD8 = {'reach': {'L': [*OFF(ME8, 0, 0.35, -0.22, 1.15), 1, 0.05], 'R': [*OFF(ME8, 0, 0.35, 0.22, 1.15), 1, 0.05]}, 'hands': {'L': 'flat', 'R': 'flat'}}
st.shot('S08', 'office', setOpts=OF, actors=[
        act('mec', ME8, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(LIC8, toon={**HOLD8, 'sq': [1.06, 0.92, 1.06], 'face': {'brow': 0.4}}, toonDur=0.04),
            k(round(LIC8 + 0.12, 3), toon={**HOLD8, 'bend': {'spine': [0.18, 0, 0, 1, None]}, 'face': {'lid': 0.55, 'brow': -0.2}}, toonDur=0.25, toonEase='inOut')]),   # the weight of it: he sags
        act('drh', [1.75, 0, 2.2], -110, 'stand', 'neutral', keys=[k(0.0, look=[ME8[0], 1.4, ME8[2]]), k(round(LIC8 - 0.2, 3), toon={'reach': {'R': [*OFF(ME8, 0, 0.55, 0.25, 1.2), 1, 0.06]}, 'hands': {'R': 'flat'}}, toonDur=0.12),
            k(LIC8, toon={'reach': {'R': [*OFF(ME8, 0, 0.38, 0.25, 1.15), 1, 0.06]}, 'hands': {'R': 'flat'}}, toonDur=0.05, toonEase='in'), k(round(LIC8 + 0.15, 3), toon={}, toonDur=0.15), k(round(LIC8 + 0.2, 3), look='camera')])],
        props=[P('copies8', 'copyFountain', pos=[0, 0, 0], opts={'n': 35, 'start': 35, 'recto': True, 'grid': GRID}),
               P('box8', 'cardboardBox', pos=[round(ME8[0] + 0.65, 3), 1.0, round(ME8[2] + 0.55, 3)], scale=0.7, opts={'text': ''}, keys=[k(round(LIC8 - 0.15, 3), to=[ME8[0], 0.95, round(ME8[2] + 0.4, 3)], dur=0.15, ease='in')]),
               P('plant8', 'plant', pos=[round(ME8[0] + 0.6, 3), 1.32, round(ME8[2] + 0.55, 3)], scale=0.45, keys=[k(round(LIC8 - 0.15, 3), to=[round(ME8[0] - 0.08, 3), 1.27, round(ME8[2] + 0.4, 3)], dur=0.15, ease='in')]),
               P('mug8', 'mug', pos=[round(ME8[0] + 0.75, 3), 1.32, round(ME8[2] + 0.55, 3)], keys=[k(round(LIC8 - 0.15, 3), to=[round(ME8[0] + 0.1, 3), 1.27, round(ME8[2] + 0.42, 3)], dur=0.15, ease='in')])],
        cams=[FC(0.0, [0.4, 1.55, 5.0], [[ME8[0], 2.45, ME8[2]], [ME8[0], 0.0, ME8[2]], [1.75, 2.3, 2.2], [GRID['x0'], 2.3, GRID['z0']], [round(GRID['x0'] + 6 * GRID['dx'], 3), 2.3, GRID['z0']]], top=0.12, bottom=0.74, drift=(0.0, 0.0, -0.1))])
st.cue('thud', 'S08', LIC8, 0.35)

# 9: reason: not conforming to the original. Close on him: her stamp comes down on his forehead: NON CONFORME; his eyes cross up at it
D9 = st.dur('S09'); NC9 = round(st.at('S09', 'L09', 1) - 0.06, 3)
ME9 = [0.9, 0, 1.75]
st.shot('S09', 'office', setOpts=OF, actors=[
        act('mec', ME9, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**HOLD8, 'face': {'lid': 0.5}}, toonDur=0.0),
            *take(NC9, 'cross', keep={**HOLD8, 'face': {'lid': 0.0}}, hold=0.5), k(round(NC9 + 0.9, 3), toon={**HOLD8, 'face': {'lid': 0.55, 'brow': -0.2}}, toonDur=0.2)]),
        act('drh', [1.7, 0, 2.15], -115, 'stand', 'neutral', keys=[k(0.0, look=[ME9[0], 2.1, ME9[2]]), k(round(NC9 - 0.25, 3), toon={'reach': {'R': [round(ME9[0] + 0.15, 3), 2.45, round(ME9[2] + 0.35, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.12),
            k(round(NC9 - 0.03, 3), toon={'reach': {'R': [round(ME9[0] + 0.05, 3), 2.15, round(ME9[2] + 0.24, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.03, toonEase='in'), k(round(NC9 + 0.15, 3), toon={}, toonDur=0.15)])],
        props=[P('box9', 'cardboardBox', pos=[ME9[0], 0.95, round(ME9[2] + 0.4, 3)], scale=0.7, opts={'text': ''}), P('plant9', 'plant', pos=[round(ME9[0] - 0.08, 3), 1.27, round(ME9[2] + 0.4, 3)], scale=0.45),
               P('nc9', 'stampMark', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.4, 0.22]}, opts={'text': 'NON CONFORME', 'w': 0.26, 'rot': -0.12, 'at': NC9})],
        cams=[FC(0.0, [round(ME9[0] - 0.3, 3), 2.0, round(ME9[2] + 1.9, 3)], [[ME9[0], 2.55, ME9[2]], [ME9[0], 1.45, ME9[2]], [round(ME9[0] - 0.4, 3), 2.0, ME9[2]], [round(ME9[0] + 0.4, 3), 2.0, ME9[2]]], top=0.14, bottom=0.7)])
st.cue('sfx:cuff', 'S09', NC9, 0.45)

# 10: too thick. In profile: her caliper closes on his chest and back: 30 cm; beside him, a copy in profile, a line
D10 = st.dur('S10'); EP10 = round(st.at('S10', 'L09b', 1) - 0.15, 3)
ME10 = [0.6, 0, 0.0]; CPY10 = [1.5, 0, 0.0]
st.shot('S10', 'office', setOpts=OF, actors=[
        act('mec', ME10, 90, 'stand', 'unimpressed', keys=[k(0.0, look=[3.0, 2.0, 0.0]), k(0.0, toon={'face': {'lid': 0.5}}, toonDur=0.0), k(round(EP10 + 0.12, 3), look='camera')]),
        act('copie', CPY10, 90, 'stand', 'unimpressed', keys=[k(0.0, look=[3.0, 2.0, 0.0]), k(0.0, toon=FLAT, toonDur=0.0)]),
        act('drh', [0.6, 0, -0.8], 0, 'stand', 'neutral', keys=[k(0.0, look=[ME10[0], 1.6, ME10[2]]), k(0.0, toon={'reach': {'R': [round(ME10[0] + 0.65, 3), 1.55, -0.05, 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.0)])],
        props=[P('cal10', 'caliper', pos=[round(ME10[0] - 0.55, 3), 1.72, round(ME10[2] + 0.05, 3)], opts={'len': 1.25, 'jaw': 0.32, 'dispW': 0.26, 'gapKeys': [[0.0, 0.85], [EP10, 0.34]], 'text': [[0.0, '…'], [round(EP10 + 0.18, 3), '30 cm']]})],
        cams=[FC(0.0, [1.0, 1.55, 3.0], [[ME10[0], 2.45, ME10[2]], [ME10[0], 0.6, ME10[2]], [CPY10[0], 2.45, CPY10[2]], [round(ME10[0] - 0.6, 3), 1.7, ME10[2]]], top=0.12, bottom=0.74)])
st.cue('sfx:clink', 'S10', EP10 + 0.18, 0.35)
st.card('S10', '30 cm', at=round(EP10 + 0.18, 3))

# 11: he filed a complaint. He slaps a form down on her desk, red in the face: RÉCLAMATION; she does not look up
D11 = st.dur('S11'); SL11 = round(st.at('S11', 'L10', 4) - 0.08, 3)
ME11 = [round(DESK[0] + 0.05, 3), 0, round(DESK[2] + 0.75, 3)]
st.shot('S11', 'office', setOpts=OF, actors=[
        act('mec', ME11, 180, 'stand', 'angry', keys=[k(0.0, look=[DESK[0], 0.8, DESK[2]]), k(round(SL11 - 0.2, 3), toon={'reach': {'R': [round(DESK[0] + 0.05, 3), 1.65, round(DESK[2] + 0.2, 3), 1, 0.06]}, 'hands': {'R': 'flat'}, 'face': {'red': 0.6, 'brow': -0.8}}, toonDur=0.12),
            k(SL11, toon={'reach': {'R': [round(DESK[0] + 0.05, 3), 0.8, round(DESK[2] + 0.2, 3), 1, 0.06]}, 'hands': {'R': 'flat'}, 'face': {'red': 1, 'brow': -0.9, 'jaw': 0.4}, 'sq': [1.05, 0.94, 1.05]}, toonDur=0.04, toonEase='in'),   # slap
            k(round(SL11 + 0.3, 3), toon={'reach': {'R': [round(DESK[0] + 0.05, 3), 0.8, round(DESK[2] + 0.2, 3), 1, 0.06]}, 'hands': {'R': 'flat'}, 'face': {'red': 1, 'brow': -0.9, 'steam': 1, 'steamInk': 1}}, toonDur=0.1)]),
        act('drh', DRH, 0, 'stand', 'unimpressed', keys=[k(0.0, look=[DESK[0], 0.8, DESK[2]]), k(round(SL11 + 0.05, 3), toon={'face': {'lid': 0.5}}, toonDur=0.05)])],
        props=[P('desk11', 'desk', pos=DESK), P('form11', 'paperSheet', pos=[round(DESK[0] + 0.05, 3), 0.775, round(DESK[2] + 0.2, 3)], rot=[-PI / 2, 0, 0], opts={'w': 0.34, 'h': 0.46, 'head': 'RÉCLAMATION', 'lines': ['Je suis', "l'original."], 'lineSize': 0.08, 'paper': '#FFFFFF', 'bright': True},
                                                       keys=[k(0.0, visible=False), k(SL11, visible=True)])],
        cams=[FC(0.0, [round(DESK[0] + 1.5, 3), 1.8, round(DESK[2] - 1.0, 3)], [[ME11[0], 2.45, ME11[2]], [DRH[0], 2.3, DRH[2]], [round(DESK[0] + 0.05, 3), 0.75, round(DESK[2] + 0.2, 3)], [ME11[0], 0.9, ME11[2]]], top=0.12, bottom=0.74)])   # from behind her shoulder: his face as he slaps it down
st.cue('thud', 'S11', SL11, 0.45)

# 12: it was photocopied in five hundred copies. She lays it on the glass and presses: copies of the complaint rain over him, piling up to his chin
D12 = st.dur('S12'); GO12 = round(st.at('S12', 'L11', 2) - 0.15, 3)
ME12 = [round(CP[0] - 1.25, 3), 0, round(CP[2] + 1.0, 3)]
st.shot('S12', 'office', setOpts=OF, actors=[
        act('mec', ME12, 30, 'stand', 'unimpressed', keys=[k(0.0, look=[CP[0], 1.0, CP[2]]), k(round(GO12 + 0.5, 3), look='camera'), k(round(GO12 + 0.5, 3), toon={'face': {'lid': 0.5}}, toonDur=0.1)]),
        act('drh', [round(CP[0] + 0.35, 3), 0, round(CP[2] + 0.85, 3)], -160, 'stand', 'neutral', keys=[k(0.0, look=[CP[0], 1.0, CP[2]]), k(round(GO12 - 0.12, 3), toon={'reach': {'R': [round(CP[0] + 0.35, 3), 1.0, round(CP[2] + 0.33, 3), 1, 0.06]}, 'hands': {'R': 'point'}}, toonDur=0.08), k(round(GO12 + 0.2, 3), toon={}, toonDur=0.15)])],
        props=[COPIER(lid=0.0, scanAt=GO12, scanDur=0.35), P('rain12', 'paperFountain', pos=[0, 0, 0], opts={'n': 80, 'from': [TRAY[0], 0.7, TRAY[2]], 'pile': [ME12[0], ME12[2]], 'r': 0.75, 'pileH': 1.75, 't0': round(GO12 + 0.15, 3), 't1': round(D12 - 0.45, 3), 'text': 'RÉCLAMATION'})],
        cams=[FC(0.0, [round(CP[0] - 2.6, 3), 1.7, round(CP[2] + 3.6, 3)], [[ME12[0], 2.5, ME12[2]], [ME12[0], 0.0, ME12[2]], [CP[0], 1.9, CP[2]], [round(ME12[0] - 0.8, 3), 0.3, ME12[2]]], top=0.12, bottom=0.74, drift=(0.06, 0, -0.08))])
st.cue('sfx:beep', 'S12', GO12, 0.3); [st.cue('sfx:paper', 'S12', round(GO12 + 0.2 + 0.25 * i, 3), 0.2) for i in range(5)]

# 13: since then he puts paper in the machine. On his knees at the open drawer, a ream in his hands, deadpan; behind him the copies in their rows; a slow
#     blink at us
D13 = st.dur('S13'); RM13 = round(st.at('S13', 'L12', 2) - 0.1, 3)
ME13 = [round(CP[0] - 0.05, 3), 0, round(CP[2] + 1.0, 3)]
REAM13 = {'reach': {'L': [round(CP[0] - 0.17, 3), 0.42, round(CP[2] + 0.62, 3), 1, 0.05], 'R': [round(CP[0] + 0.13, 3), 0.42, round(CP[2] + 0.62, 3), 1, 0.05]}, 'hands': {'L': 'flat', 'R': 'flat'}}
st.shot('S13', 'office', setOpts=OF, actors=[
        act('mec', ME13, 180, 'kneel', 'unimpressed', keys=[k(0.0, look=[CP[0], 0.3, CP[2]]), k(0.0, toon=REAM13, toonDur=0.0),
            k(RM13, toon={'reach': {'L': [round(CP[0] - 0.17, 3), 0.3, round(CP[2] + 0.45, 3), 1, 0.05], 'R': [round(CP[0] + 0.13, 3), 0.3, round(CP[2] + 0.45, 3), 1, 0.05]}, 'hands': {'L': 'flat', 'R': 'flat'}}, toonDur=0.3, toonEase='inOut'),   # the ream slid in
            k(round(RM13 + 0.35, 3), to=[ME13[0], 0, round(ME13[2] + 0.01, 3)], dur=0.3, clip='kneel', then='kneel', face=-25), k(round(RM13 + 0.35, 3), toon={}, toonDur=0.15),   # he turns round on his knees...
            k(round(RM13 + 0.45, 3), look='camera'), k(round(RM13 + 0.45, 3), toon={'face': {'lid': 0.45}}, toonDur=0.1),   # ...to us
            k(round(RM13 + 1.0, 3), toon={'face': {'lid': 1}}, toonDur=0.12), k(round(RM13 + 1.2, 3), toon={'face': {'lid': 0.45}}, toonDur=0.14)])],   # a slow blink
        props=[COPIER(lid=0.0, drawerAt=0.0), P('ream13', 'paperReam', pos=[round(CP[0] - 0.02, 3), 0.36, round(CP[2] + 0.62, 3)], keys=[k(RM13, to=[round(CP[0] - 0.02, 3), 0.24, round(CP[2] + 0.45, 3)], dur=0.3, ease='inOut')]),
               P('copies13', 'copyFountain', pos=[0, 0, 0], opts={'n': 15, 'start': 15, 'recto': True, 'grid': {'x0': -2.4, 'z0': -2.7, 'dx': 0.65, 'dz': 0.6, 'cols': 5}})],   # (first look) at the back left: the camera stood inside a cutout
        cams=[FC(0.0, [round(CP[0] - 1.3, 3), 1.25, round(CP[2] + 2.9, 3)], [[ME13[0], 2.0, ME13[2]], [ME13[0], 0.0, ME13[2]], [CP[0], 1.0, CP[2]], [round(CP[0] - 0.9, 3), 1.6, round(CP[2] + 0.5, 3)]], top=0.16, bottom=0.74, drift=(0.04, 0, -0.06))])
st.cue('sfx:paper', 'S13', RM13, 0.3)

st.write("La photocopieuse", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'copie': {'preset': 'lemec', 'atlas': None, 'mono': 0.95, 'suit': '#585858', 'pants': '#4E4E4E', 'tie': '#8E8E8E', 'lapel': '#B4B4B4', 'skin': '#C6C6C6', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},   # a black-and-white copy of him (the face desaturated by mono, the clothes given in greys)
    'drh': {'preset': 'madame', 'seed': 491, 'suit': '#7A3E9C', 'hair': 'bun', 'hairColor': '#3A2A20', 'build': {'width': 0.92, 'headWidth': 1.25}},
})
