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
        act('mec', [CP[0], 0, round(CP[2] + 0.85, 3)], 0, 'stand', 'unimpressed', keys=[k(0.0, look=[CP[0], 1.05, CP[2]]), k(0.0, toon={'sq': [1.0, 0.985, 1.0], 'face': {'lid': 0.4}}, toonDur=0.0),   # (pass 3) alive from the first frame: he eyes the machine...
            k(0.16, toon={'sq': [1.0, 1.01, 1.0], 'face': {'lid': 1.0}}, toonDur=0.05), k(0.26, toon={'sq': [1.0, 0.99, 1.0], 'face': {'lid': 0.4}}, toonDur=0.06), k(0.24, look='camera'),   # ...a blink, a look at us
            k(round(UP1 - 0.12, 3), toon={'sq': [1.07, 0.9, 1.07]}, toonDur=0.08, toonEase='in'),   # a crouch...
            k(UP1, to=[CP[0], 0.86, round(CP[2] + 0.4, 3)], dur=0.14, clip='sit', then='sit', ease='out', face=0), k(UP1, toon={'sq': [0.92, 1.1, 0.92]}, toonDur=0.06),   # ...up he hops...
            k(round(UP1 + 0.14, 3), toon={'sq': [0.98, 1.03, 0.98]}, toonDur=0.05),   # (pass 3) ...hangs at the top four frames...
            k(round(UP1 + 0.27, 3), to=SEAT, dur=0.1, glide=True, ease='in', face=0),
            k(round(UP1 + 0.37, 3), toon={'sq': [1.08, 0.9, 1.08], 'face': {'lid': 0.4}}, toonDur=0.04), k(round(UP1 + 0.49, 3), toon={'face': {'lid': 0.45}}, toonDur=0.1),   # ...and lands on the glass, heavy-lidded
            k(round(UP1 + 0.9, 3), look=[round(CP[0] - 1.0, 3), 1.6, 0.5]), k(round(D1 - 0.5, 3), look=[CP[0], 2.3, round(CP[2] - 0.3, 3)]),   # (pass 3b, freeze check) a look up at the lid...
            k(round(D1 - 0.36, 3), toon={'sq': [1.02, 0.97, 1.02], 'face': {'lid': 1.0}}, toonDur=0.05), k(round(D1 - 0.24, 3), toon={'sq': [0.99, 1.01, 0.99], 'face': {'lid': 0.45}}, toonDur=0.08)])],   # ...a blink, the shoulders settle
        props=[COPIER()],
        cams=[FC(0.0, [round(CP[0] - 1.6, 3), 1.35, 1.4], [[CP[0], 2.5, CP[2]], [CP[0], 0.0, round(CP[2] + 0.85, 3)], [round(CP[0] + 0.6, 3), 1.0, CP[2]], [round(CP[0] - 0.6, 3), 1.0, CP[2]]], top=0.12, bottom=0.74, drift=(0.04, 0, -0.08))])
st.cue('sfx:spring', 'S01', UP1 + 0.37, 0.3)

# 2: it photocopied him whole. The light bar sweeps the glass under him, then a sheet of green light climbs over him from his seat to the top of his
#    head: his hair stands on end as it passes
D2 = st.dur('S02'); SC2 = round(st.at('S02', 'L02', 2) - 0.1, 3)
SIT2 = {'face': {'lid': 0.45}}
st.shot('S02', 'office', setOpts=OF, actors=[
        act('mec', SEAT, 0, 'sit', 'unimpressed', keys=[k(0.0, look=[CP[0], 0.9, round(CP[2] + 0.3, 3)]), k(0.0, toon=SIT2, toonDur=0.0), k(0.28, look='camera'), k(0.12, toon={'face': {'lid': 0.6}, 'sq': [1.0, 0.985, 1.0]}, toonDur=0.1), k(0.3, toon=SIT2, toonDur=0.1),   # (pass 3b) a glance down at the glass, then at us
            k(round(SC2 + 0.05, 3), toon={'face': {'lid': 0.0, 'eye': 0.3, 'brow': 0.6}}, toonDur=0.05),   # the flash under him
            *take(round(SC2 + 0.82, 3), 'hair', keep={'face': {'lid': 0.0}}, hold=0.35, antic_f=4, settle_f=7)])],   # the light passes his head: his hair stands on end   # (pass 2) the climb slower (0.95 s)
        props=[COPIER(scanAt=SC2, scanDur=0.5), P('scan2', 'scanPlane', pos=[CP[0], 0, round(CP[2] + 0.08, 3)], opts={'w': 1.0, 'd': 0.8, 'y0': 0.97, 'y1': 2.45, 'at': round(SC2 + 0.15, 3), 'dur': 0.95})],
        cams=[FC(0.0, [round(CP[0] - 0.9, 3), 1.55, 0.2], [[CP[0], 2.55, CP[2]], [CP[0], 0.85, CP[2]], [round(CP[0] - 0.55, 3), 1.6, CP[2]], [round(CP[0] + 0.55, 3), 1.6, CP[2]]], top=0.12, bottom=0.74)])
st.cue('sfx:beep', 'S02', SC2 - 0.1, 0.3); st.cue('sfx:zip', 'S02', SC2, 0.35); st.cue('sfx:zip', 'S02', SC2 + 0.15, 0.3)

# 3: the copy came out of the tray. Low at the tray: the copy slides out flat on its back, head first, black and white, drops to the floor and springs up
#    as thin as paper, fluttering; behind, on the glass, his jaw drops
D3 = st.dur('S03'); OUT3 = round(st.at('S03', 'L03', 1) - 0.1, 3); UP3 = round(st.at('S03', 'L03', 3) - 0.05, 3)
COPY3 = [round(TRAY[0] + 0.1, 3), 0, round(CP[2] + 1.4, 3)]    # (pass 2) to the side: in front of him it hid his head   # (pass 3) further toward us, clear of him from the end of the tray
st.shot('S03', 'office', setOpts=OF, actors=[
        act('copie', [round(CP[0] + 0.25, 3), 0.62, CP[2]], -90, 'stiffStand', 'neutral', keys=[k(0.0, look=None), k(0.0, toon={**FLAT, 'lay': [-1.57, 0]}, toonDur=0.0), k(0.0, visible=False),
            k(OUT3, visible=True), k(OUT3, to=[TRAY[0], 0.62, CP[2]], dur=round(UP3 - OUT3 - 0.12, 3), glide=True, ease='out', face=-90),   # out of the tray, head first
            k(round(UP3 - 0.1, 3), to=COPY3, dur=0.12, glide=True, ease='in', face=90),   # onto the floor...   # (pass 2) it springs up facing the camera at the end of the tray
            k(round(UP3 + 0.02, 3), toon={**FLAT, 'lay': [0.2, 0]}, toonDur=0.08, toonEase='out'), k(round(UP3 + 0.12, 3), toon={**FLUT(1.5), 'lay': [-0.08, 0]}, toonDur=0.08),   # ...and it springs up past upright
            k(round(UP3 + 0.24, 3), toon=FLUT(1.0), toonDur=0.1), k(round(UP3 + 0.3, 3), look='camera')]),
        act('mec', SEAT, 35, 'sit', 'unimpressed', keys=[k(0.0, look=[TRAY[0], 0.7, TRAY[2]]), k(0.0, toon={'face': {'lid': 0.3}}, toonDur=0.0), *take(round(UP3 + 0.05, 3), 'jaw', hold=0.4, antic_f=3, settle_f=6)])],   # (pass 3) turned toward the tray: his face, not the side of his head
        props=[COPIER(sheetsAt=[round(OUT3 - 0.05, 3)])],
        cams=[FC(0.0, [round(TRAY[0] + 1.35, 3), 1.3, round(CP[2] + 0.3, 3)], [[CP[0], 2.45, CP[2]], [round(CP[0] - 0.35, 3), 0.0, CP[2]], [COPY3[0], 2.35, COPY3[2]], [COPY3[0], 0.0, round(COPY3[2] + 0.3, 3)], [round(TRAY[0] + 0.45, 3), 0.62, TRAY[2]], [round(TRAY[0] + 0.45, 3), 0.62, round(TRAY[2] - 0.25, 3)]], top=0.12, bottom=0.76, drift=(-0.04, 0, -0.05))])   # (pass 3) at the end of the tray, low: the copy's face slides out toward the lens (it left past the edge)   # (pass 2) at the end of the tray, a little above it: the copy slides out toward us, him whole on the glass behind (from above the floor filled the frame)   # (first look) from above: the copy flat as a sheet reads face up (from low it was a line)
st.cue('sfx:paper', 'S03', OUT3, 0.35); st.cue('sfx:spring', 'S03', UP3 + 0.02, 0.35)

# 4: human resources hired it. (pass 2) Seen side-on: the copy faces us, flat as a sheet, and reaches across to her over the desk with its paper arm, a wave
#    running down it like a ribbon; she shakes its hand vigorously; then close above the desk: her rubber stamp comes down on the contract: EMBAUCHÉ
D4 = st.dur('S04'); EMB4 = round(st.at('S04', 'L04', 4) - 0.06, 3)
COPY4 = [round(DESK[0] + 0.3, 3), 0, round(DESK[2] + 0.8, 3)]
HAND4 = [round(DESK[0] + 0.42, 3), 1.2, round(DESK[2] + 0.22, 3)]          # the clasp over the desk, on our side of both of them
CON4 = [round(DESK[0] - 0.3, 3), 0.77, round(DESK[2] + 0.02, 3)]          # the contract on the desk
st.shot('S04', 'office', setOpts=OF, actors=[
        act('drh', DRH, 0, 'stand', 'happy', keys=[k(0.0, look=[COPY4[0], 1.9, COPY4[2]]), k(0.12, toon={'reach': {'L': [*HAND4[:3], 1, 0.06]}, 'hands': {'L': 'grip'}}, toonDur=0.15),
            *[k(round(0.28 + 0.12 * i, 3), toon={'reach': {'L': [HAND4[0], round(HAND4[1] + (0.09 if i % 2 == 0 else -0.07), 3), HAND4[2], 1, 0.06]}, 'hands': {'L': 'grip'}}, toonDur=0.1, toonEase='inOut') for i in range(5)],   # a vigorous handshake
            k(round(EMB4 - 0.22, 3), look=[CON4[0], 0.8, CON4[2]]), k(round(EMB4 - 0.22, 3), toon={'reach': {'R': [CON4[0], 1.15, CON4[2], 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.1),   # the stamp up...
            k(round(EMB4 - 0.03, 3), toon={'reach': {'R': [CON4[0], 0.84, CON4[2], 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.03, toonEase='in'),   # ...and down: EMBAUCHÉ
            k(round(EMB4 + 0.2, 3), toon={'reach': {'R': [CON4[0], 1.05, CON4[2], 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.12)]),
        act('copie', COPY4, 90, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon=FLUT(0.6), toonDur=0.0),
            *[k(round(0.28 + 0.12 * i, 3), toon={**FLAT, 'reach': {'L': [HAND4[0], round(HAND4[1] + (0.09 if i % 2 == 0 else -0.07), 3), HAND4[2], 1, 0.06]}, 'hands': {'L': 'grip'}, 'wave': {'armL': [0.12, 1.5, round(i * 0.5, 2), 1, 0.0], 'spine': [0.03, 1.5, round(i * 0.3, 2), 1, 0.0]}}, toonDur=0.1) for i in range(5)],   # its paper arm rippling in an S
            k(round(EMB4 - 0.2, 3), toon=FLUT(0.6), toonDur=0.15)])],
        props=[P('stamp4', 'rubberStamp', on={'actor': 'drh', 'hand': 'R', 'offset': [0, -0.06, 0.02]}, scale=2.2), P('desk4', 'desk', pos=DESK), P('contract4', 'paperSheet', pos=CON4, rot=[-PI / 2, 0, 0], opts={'w': 0.34, 'h': 0.46, 'head': 'CONTRAT', 'lines': ['Poste : employé', 'Salaire : papier'], 'lineSize': 0.07, 'paper': '#FFFFFF', 'bright': True, 'stamp': {'text': 'EMBAUCHÉ', 'at': EMB4, 'rot': -0.2, 'y': -0.06, 'w': 0.92}}),
               P('stamp4', 'rubberStamp', on={'actor': 'drh', 'hand': 'R', 'offset': [0, 0, 0.02], 'rot': [PI / 2, 0, 0]}, scale=2.2, opts={'color': '#C23A2E'})],   # (pass 2) her stamp
        cams=[FC(0.0, [round(DESK[0] + 2.6, 3), 1.5, round(DESK[2] + 0.35, 3)], [[DRH[0], 2.35, DRH[2]], [COPY4[0], 2.45, COPY4[2]], [COPY4[0], 0.25, COPY4[2]], [HAND4[0], 1.2, HAND4[2]], [DRH[0], 0.6, DRH[2]]], top=0.12, bottom=0.74),   # (pass 2) side-on: the clasp clear of both bodies (from behind the copy it was hidden)
              cam(round(EMB4 - 0.18, 3), [CON4[0], 1.62, round(CON4[2] + 0.36, 3)], [CON4[0], 1.55, round(CON4[2] + 0.33, 3)], [CON4[0], 0.77, round(CON4[2] - 0.02, 3)], [CON4[0], 0.77, round(CON4[2] - 0.02, 3)], lens=30)])   # (pass 2) close above the desk: the stamp comes down, EMBAUCHÉ in red
st.cue('sfx:cuff', 'S04', EMB4, 0.4)

# 5: a copy costs only paper. The price board on the wall: LUI : 2 400 € / COPIE : 0,02 €; she taps the copy's price; he sweats, the copy smiles flat.
#    (pass 2) Tighter: both of them whole, her shoulder at the left edge, the board text twice the size, the copy's price the bigger line
D5 = st.dur('S05'); CO5 = round(st.at('S05', 'L05', 4) - 0.1, 3)
BOARD = [-2.3, 1.45, -3.5]; ME5 = [-1.25, 0, -2.3]; CPY5 = [-3.35, 0, -2.3]; DRH5 = [-3.9, 0, -2.95]; TAP5 = [-2.72, 1.68, -3.44]   # (pass 3) her fingertip on 0,02   # (pass 2) both outside the board (his head hid its euro sign)
st.shot('S05', 'office', setOpts=OF, actors=[
        act('mec', ME5, -10, 'stand', 'worried', keys=[k(0.0, look=[BOARD[0], 2.1, BOARD[2]]), k(round(CO5 + 0.1, 3), look='camera'), k(round(CO5 + 0.1, 3), toon={'face': {'sweat': 1, 'brow': 0.7}}, toonDur=0.1)]),
        act('copie', CPY5, 10, 'stand', 'happy', keys=[k(0.0, look='camera'), k(0.0, toon=FLUT(0.6), toonDur=0.0), k(0.55, look=[BOARD[0], 2.0, BOARD[2]]), k(0.62, toon={**FLUT(0.9), 'face': {'lid': 1.0}}, toonDur=0.05), k(0.74, toon=FLUT(0.6), toonDur=0.06),
            k(round(CO5 + 0.2, 3), look='camera'), k(round(CO5 + 0.2, 3), toon={**FLUT(1.2), 'sq': [1.05, 0.96, 0.05]}, toonDur=0.08), k(round(CO5 + 0.4, 3), toon=FLUT(0.6), toonDur=0.12)]),   # (pass 3) it glances at its price, blinks, preens at us
        act('drh', DRH5, 50, 'stand', 'happy', keys=[k(0.0, look=[BOARD[0], 1.9, BOARD[2]]), k(round(CO5 - 0.2, 3), toon={'reach': {'R': [TAP5[0], round(TAP5[1] + 0.08, 3), round(TAP5[2] + 0.08, 3), 1, 0.15]}, 'hands': {'R': 'point'}}, toonDur=0.12),
            k(round(CO5 - 0.02, 3), toon={'reach': {'R': [*TAP5, 1, 0.15]}, 'hands': {'R': 'point'}}, toonDur=0.04, toonEase='in'), k(round(CO5 + 0.1, 3), toon={'reach': {'R': [TAP5[0], round(TAP5[1] + 0.05, 3), round(TAP5[2] + 0.07, 3), 1, 0.15]}, 'hands': {'R': 'point'}}, toonDur=0.05),
            k(round(CO5 + 0.18, 3), toon={'reach': {'R': [*TAP5, 1, 0.15]}, 'hands': {'R': 'point'}}, toonDur=0.04, toonEase='in'), k(round(CO5 + 0.4, 3), look='camera')])],   # (pass 3) two taps on 0,02
        props=[P('board5', 'lcdScreen', pos=BOARD, opts={'w': 1.6, 'h': 1.1, 'stand': 0, 'dark': False, 'pages': [[0.0, ['LUI : 2 400 €', 'COPIE :', '0,02 €'], {'sizes': [0.7, 0.8, 1.8], 'y0': 0.12, 'accent': '#C8202A'}]]})],   # (pass 3) the price on its own line: it was shrunk to fit and came out smaller than LUI
        cams=[FC(0.0, [-2.3, 1.6, 0.9], [[BOARD[0] - 0.82, 2.58, BOARD[2]], [BOARD[0] + 0.82, 2.58, BOARD[2]], [BOARD[0] - 0.82, 1.47, BOARD[2]], [ME5[0], 2.45, ME5[2]], [round(CPY5[0] - 0.35, 3), 0.3, CPY5[2]], [round(ME5[0] + 0.35, 3), 0.3, ME5[2]], [round(DRH5[0] + 0.3, 3), 1.9, DRH5[2]]], top=0.12, bottom=0.74, drift=(0.0, 0.0, -0.1))])
st.cue('sfx:cash', 'S05', CO5, 0.35)

# 6: so they ran off five hundred. (pass 2) Close on the copier's panel: her finger on the green button; cut, low in front of the office: the machine spits
#    copies of him on arcs and they land in rows filling the floor toward us
D6 = st.dur('S06'); GO6 = round(st.at('S06', 'L06', 4) - 0.35, 3)
GRID = {'x0': -2.6, 'z0': -2.2, 'dx': 0.72, 'dz': 0.75, 'cols': 7}
BTN = [round(CP[0] + 0.45, 3), 1.07, round(CP[2] + 0.38, 3)]   # (pass 3) the real place of the button (the finger aimed 10 cm short: the sleeve pressed it)
st.shot('S06', 'office', setOpts=OF, actors=[
        act('drh', [round(CP[0] + 0.35, 3), 0, round(CP[2] + 0.85, 3)], -160, 'stand', 'happy', keys=[k(0.0, look=[CP[0], 1.0, CP[2]]), k(round(GO6 - 0.3, 3), toon={'reach': {'R': [BTN[0], round(BTN[1] + 0.1, 3), round(BTN[2] + 0.06, 3), 1, 0.15]}, 'hands': {'R': 'point'}}, toonDur=0.12),
            k(GO6, toon={'reach': {'R': [BTN[0], round(BTN[1] - 0.01, 3), BTN[2], 1, 0.15]}, 'hands': {'R': 'point'}}, toonDur=0.04, toonEase='in'), k(round(GO6 + 0.25, 3), toon={}, toonDur=0.15), k(round(GO6 + 0.3, 3), look=[-0.5, 1.2, -1.0])])],
        props=[COPIER(lid=0.0, btnR=0.052, pressAt=[GO6]), P('copies6', 'copyFountain', pos=[0, 0, 0], opts={'n': 35, 'from': TRAY, 'grid': GRID, 't0': round(GO6 + 0.1, 3), 't1': round(D6 - 0.25, 3), 'flight': 0.5, 'recto': True, 'cool': '#D2DEFF', 'painted': True, 'opaque': True, 'flutter': 0.35})],
        cams=[cam(0.0, [round(CP[0] - 0.2, 3), 1.86, round(CP[2] + 1.22, 3)], [round(CP[0] - 0.17, 3), 1.83, round(CP[2] + 1.17, 3)], [round(BTN[0] - 0.05, 3), BTN[1], round(BTN[2] - 0.02, 3)], [round(BTN[0] - 0.05, 3), BTN[1], round(BTN[2] - 0.02, 3)], lens=40),   # (pass 3) from the left, above: her finger comes in from the right (from her side the sleeve filled the frame)   # (pass 2) her finger on the button (unseen in the wide)
              FC(round(GO6 + 0.12, 3), [-0.3, 1.0, 3.7], [[round(GRID['x0'] + 2 * GRID['dx'], 3), 2.3, round(GRID['z0'] + 2 * GRID['dz'], 3)], [round(GRID['x0'] + 4 * GRID['dx'], 3), 2.3, round(GRID['z0'] + 2 * GRID['dz'], 3)], [round(GRID['x0'] + 2 * GRID['dx'], 3), 0.0, round(GRID['z0'] + 4 * GRID['dz'], 3)], [round(GRID['x0'] + 4 * GRID['dx'], 3), 0.0, round(GRID['z0'] + 4 * GRID['dz'], 3)]], top=0.1, bottom=0.84, drift=(0.1, 0, -0.1))])   # (pass 2) three columns framed, the rows running out past the edges (the whole grid made them small)   # (pass 2) low in front: the rows fill the floor toward us
st.cue('sfx:beep', 'S06', GO6, 0.3); [st.cue('sfx:paper', 'S06', round(GO6 + 0.15 + 0.22 * i, 3), 0.2) for i in range(6)]

# 7: double-sided, to save. (pass 2) Close on one copy: its front held, a little squash, it turns to edge-on (a line, held three frames) and on round to
#    its back: his face printed there as well, deadpan; the printed face blinks
D7 = st.dur('S07'); VE7 = round(st.at('S07', 'L07', 1) - 0.05, 3)
CPY7 = [0.3, 0, 1.7]   # (first look) in front of the rows (among them the camera stood inside a cutout)
st.shot('S07', 'office', setOpts=OF, actors=[
        *[act(nm, [CPY7[0], 0, round(CPY7[2] + dz, 3)], f0, 'stand', 'unimpressed', keys=[k(0.0, look='camera' if nm == 'copie' else None), k(0.0, toon=FLUT(0.6), toonDur=0.0), k(round(VE7 - 0.1, 3), look=None),
            k(round(VE7 - 0.08, 3), toon={**FLAT, 'sq': [1.04, 0.94, 0.05]}, toonDur=0.07, toonEase='in'),   # a squash first...
            k(VE7, to=[CPY7[0], 0, CPY7[2]], dur=0.13, clip='stand', then='stand', face=f0 + 90), k(VE7, toon=FLUT(0.3), toonDur=0.05),   # ...round to edge-on: a line...
            k(round(VE7 + 0.23, 3), to=[CPY7[0], 0, round(CPY7[2] - dz, 3)], dur=0.13, clip='stand', then='stand', face=f0 + 180),   # ...held three frames, then on round
            k(round(VE7 + 0.36, 3), toon=FLUT(1.6), toonDur=0.06), k(round(VE7 + 0.46, 3), toon=FLUT(0.6), toonDur=0.15),
            *([k(round(VE7 + 0.5, 3), look='camera'), k(round(D7 - 0.55, 3), toon={**FLUT(0.6), 'face': {'lid': 1}}, toonDur=0.05), k(round(D7 - 0.41, 3), toon=FLUT(0.6), toonDur=0.07)] if nm == 'copie2' else [])])   # (pass 3) its other side: the same print, which blinks
          for nm, f0, dz in (('copie', 0, 0.02), ('copie2', 180, -0.02))]],
        props=[P('copies7', 'copyFountain', pos=[0, 0, 0], opts={'n': 35, 'start': 35, 'recto': True, 'grid': GRID, 'cool': '#D2DEFF', 'painted': True, 'opaque': True})],
        cams=[FC(0.0, [0.42, 1.9, 3.5], [[CPY7[0], 2.5, CPY7[2]], [CPY7[0], 1.15, CPY7[2]], [round(CPY7[0] - 0.5, 3), 1.9, CPY7[2]], [round(CPY7[0] + 0.5, 3), 1.9, CPY7[2]]], top=0.12, bottom=0.74, drift=(0.0, 0.0, -0.06))])   # (pass 2) closer: the copy apart from the crowd
st.cue('whoosh', 'S07', VE7, 0.3, 0.2, 600, 2400); st.cue('sfx:paper', 'S07', VE7 + 0.23, 0.25)

# 8: him, they fired him. She shoves a cardboard box into his arms (his plant, his mug); behind him the copies stand in their rows
D8 = st.dur('S08'); LIC8 = round(st.at('S08', 'L08', 3) - 0.12, 3)
ME8 = [0.9, 0, 1.75]; HOLD8 = {'reach': {'L': [*OFF(ME8, 0, 0.35, -0.22, 1.02), 1, 0.05], 'R': [*OFF(ME8, 0, 0.35, 0.22, 1.02), 1, 0.05]}, 'hands': {'L': 'flat', 'R': 'flat'}}
st.shot('S08', 'office', setOpts=OF, actors=[
        act('mec', ME8, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(LIC8, toon={**HOLD8, 'sq': [1.12, 0.86, 1.12], 'lay': [-0.14, 0], 'face': {'brow': 0.6, 'eye': 0.3}}, toonDur=0.04), k(LIC8, to=[ME8[0], 0, round(ME8[2] - 0.2, 3)], dur=0.12, glide=True, ease='out', face='keep'),   # (pass 2) shoved back a step, squashed
            k(round(LIC8 + 0.14, 3), toon={**HOLD8, 'sq': [0.96, 1.05, 0.96], 'lay': [0.05, 0]}, toonDur=0.1),
            k(round(LIC8 + 0.12, 3), toon={**HOLD8, 'bend': {'spine': [0.18, 0, 0, 1, None]}, 'face': {'lid': 0.55, 'brow': -0.2}}, toonDur=0.25, toonEase='inOut')]),   # the weight of it: he sags
        act('drh', [1.75, 0, 2.2], -110, 'stand', 'neutral', keys=[k(0.0, look=[ME8[0], 1.4, ME8[2]]), k(round(LIC8 - 0.2, 3), toon={'reach': {'R': [*OFF(ME8, 0, 0.55, 0.25, 1.2), 1, 0.06]}, 'hands': {'R': 'flat'}}, toonDur=0.12),
            k(LIC8, toon={'reach': {'R': [*OFF(ME8, 0, 0.38, 0.25, 1.15), 1, 0.06]}, 'hands': {'R': 'flat'}}, toonDur=0.05, toonEase='in'), k(round(LIC8 + 0.15, 3), toon={}, toonDur=0.15), k(round(LIC8 + 0.2, 3), look='camera')])],
        props=[P('copies8', 'copyFountain', pos=[0, 0, 0], opts={'n': 35, 'start': 35, 'recto': True, 'grid': GRID, 'cool': '#D2DEFF', 'painted': True, 'opaque': True}),
               P('box8', 'cardboardBox', pos=[round(ME8[0] + 0.65, 3), 0.9, round(ME8[2] + 0.55, 3)], scale=0.7, opts={'text': ''}, keys=[k(round(LIC8 - 0.15, 3), to=[ME8[0], 0.82, round(ME8[2] + 0.4, 3)], dur=0.15, ease='in')]),
               P('plant8', 'plant', pos=[round(ME8[0] + 0.6, 3), 1.2, round(ME8[2] + 0.55, 3)], scale=0.32, keys=[k(round(LIC8 - 0.15, 3), to=[round(ME8[0] - 0.12, 3), 1.12, round(ME8[2] + 0.4, 3)], dur=0.15, ease='in')]),   # (pass 2) lower and smaller: it hid his face
               P('mug8', 'mug', pos=[round(ME8[0] + 0.75, 3), 1.2, round(ME8[2] + 0.55, 3)], keys=[k(round(LIC8 - 0.15, 3), to=[round(ME8[0] + 0.1, 3), 1.14, round(ME8[2] + 0.42, 3)], dur=0.15, ease='in')])],
        cams=[FC(0.0, [0.6, 1.5, 4.2], [[ME8[0], 2.45, ME8[2]], [ME8[0], 0.55, ME8[2]], [1.75, 2.35, 2.2], [2.1, 2.2, 2.2], [round(ME8[0] - 0.55, 3), 1.5, ME8[2]]], top=0.12, bottom=0.76, drift=(0.0, 0.0, -0.1))])   # (pass 3) her whole head (the edge cut through it)   # (pass 2) a medium two-shot on the box, the rows behind (wide, the floor filled the bottom third)
st.cue('thud', 'S08', LIC8, 0.35)

# 9: reason: not conforming to the original. Close on him: her stamp comes down on his forehead: NON CONFORME; his eyes cross up at it
D9 = st.dur('S09'); NC9 = round(st.at('S09', 'L09', 1) - 0.06, 3)
ME9 = [0.9, 0, 1.75]
st.shot('S09', 'office', setOpts=OF, actors=[
        act('mec', ME9, 0, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={**HOLD8, 'face': {'lid': 0.5}}, toonDur=0.0),
            k(0.2, toon={**HOLD8, 'face': {'lid': 1.0}}, toonDur=0.05), k(0.32, toon={**HOLD8, 'face': {'lid': 0.5}}, toonDur=0.06), k(0.4, look=[1.7, 2.0, 2.15]), k(round(NC9 - 0.3, 3), look='camera'),   # (pass 3) a blink, a glance at her
            k(round(NC9 - 0.06, 3), toon={**HOLD8, 'face': {'lid': 0.0, 'brow': 0.4}}, toonDur=0.04),
            k(NC9, toon={**HOLD8, 'scl': {'head': [1.24, 0.64, 1.18]}, 'sq': [1.04, 0.95, 1.04], 'face': {'cross': 1, 'pop': 0.45, 'popLen': 0.18, 'brow': 0.9, 'eye': 0.35}}, toonDur=0.025, toonEase='out'),   # (pass 2) the head squashed like an accordion, the eyes out and crossed...
            k(round(NC9 + 0.1, 3), toon={**HOLD8, 'scl': {'head': [0.92, 1.1, 0.95]}, 'face': {'cross': 1, 'pop': 0.45, 'popLen': 0.18, 'brow': 0.9, 'tremble': 1}}, toonDur=0.06, toonEase='outBack'),   # ...back past round...
            k(round(NC9 + 0.2, 3), toon={**HOLD8, 'face': {'cross': 1, 'pop': 0.4, 'popLen': 0.16, 'brow': 0.8, 'tremble': 1}}, toonDur=0.06),   # ...held crossed, eight frames
            k(round(NC9 + 0.48, 3), toon={**HOLD8, 'face': {'cross': 0.4, 'lid': 0.3}}, toonDur=0.12), k(round(NC9 + 0.9, 3), toon={**HOLD8, 'face': {'lid': 0.55, 'brow': -0.2}}, toonDur=0.2)]),
        act('drh', [1.7, 0, 2.15], -115, 'stand', 'neutral', keys=[k(0.0, look=[ME9[0], 2.1, ME9[2]]), k(round(NC9 - 0.25, 3), toon={'reach': {'R': [round(ME9[0] + 0.15, 3), 2.45, round(ME9[2] + 0.35, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.12),
            k(round(NC9 - 0.03, 3), toon={'reach': {'R': [round(ME9[0] + 0.05, 3), 2.15, round(ME9[2] + 0.24, 3), 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.03, toonEase='in'), k(round(NC9 + 0.15, 3), toon={}, toonDur=0.15)])],
        props=[P('box9', 'cardboardBox', pos=[ME9[0], 0.82, round(ME9[2] + 0.4, 3)], scale=0.7, opts={'text': ''}), P('plant9', 'plant', pos=[round(ME9[0] - 0.12, 3), 1.12, round(ME9[2] + 0.4, 3)], scale=0.32),
               P('nc9', 'stampPop', on={'actor': 'mec', 'joint': 'head', 'offset': [0.0, 0.42, 0.22]}, opts={'text': 'NON CONFORME', 'w': 0.3, 'rot': -0.1, 'at': NC9}),   # (pass 3) bigger
               P('stamp9', 'rubberStamp', on={'actor': 'drh', 'hand': 'R', 'offset': [0, -0.06, 0.02]}, scale=2.2)],   # (pass 3) the stamp in her fist (she hit him bare-handed)   # (pass 2) on the forehead (it hung past his head)
        cams=[FC(0.0, [round(ME9[0] - 0.3, 3), 2.0, round(ME9[2] + 1.9, 3)], [[ME9[0], 2.55, ME9[2]], [ME9[0], 1.45, ME9[2]], [round(ME9[0] - 0.4, 3), 2.0, ME9[2]], [round(ME9[0] + 0.4, 3), 2.0, ME9[2]]], top=0.14, bottom=0.7)])
st.cue('sfx:cuff', 'S09', NC9, 0.45)

# 10: too thick. (pass 2) Three-quarter to us, his face in view: in the first frames her caliper snaps shut on his chest and back and squeezes him (he
#     squashes, then swells back against the jaws); the big readout: 30 cm; she stands beside him; next to him the copy, edge-on to us: a line
D10 = st.dur('S10'); EP10 = round(st.at('S10', 'L09b', 1) - 0.15, 3)
ME10 = [0.6, 0, 0.0]; CAM10 = [2.5, 1.55, 1.95]; CSC = 1.6                    # (pass 3) he faces +X, the camera 45 degrees round to his right: face and caliper both read
CPY10 = [0.48, 0, -0.72]; RY10C = -35                                         # the copy beside him, turned nearly edge-on: a sliver of its printed face
CAL10 = [0.4, 1.66, 0.0]                                                       # the caliper's back end: the fixed jaw on his back, the slide on his chest
GAP = lambda w: round(w / CSC - 0.04, 3)                                       # a gap between the jaws in metres, in the caliper's own units
SQZ10 = lambda d, x=1.0, extra=None: {**{'sq': [x, round(1 + (1 - d) * 0.2, 3), d]}, **(extra or {})}
st.shot('S10', 'office', setOpts=OF, actors=[
        act('mec', ME10, 90, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.5}}, toonDur=0.0),
            k(0.04, toon=SQZ10(0.45, 1.16, {'face': {'lid': 1.0, 'brow': -0.8, 'jaw': 0.15}}), toonDur=0.1, toonEase='in'), k(0.04, to=[0.515, 0, 0.0], dur=0.1, glide=True, ease='in', face='keep'),   # pinched to half his depth in four frames, eyes squeezed shut (pressed back against the fixed jaw)
            *[k(round(0.16 + 0.05 * i, 3), toon=SQZ10(0.45 + 0.03 * (i % 2), 1.16, {'face': {'lid': 1.0, 'brow': -0.8, 'jaw': 0.15}}), toonDur=0.04) for i in range(3)],   # held, trembling
            k(0.31, toon=SQZ10(1.18, 0.96, {'face': {'lid': 0.0, 'eye': 0.6, 'brow': 0.9}}), toonDur=0.07, toonEase='out'), k(0.31, to=[0.64, 0, 0.0], dur=0.07, glide=True, ease='out', face='keep'),   # he swells back, past round, eyes wide...
            k(0.44, toon=SQZ10(1.0, 1.0, {'face': {'lid': 0.3, 'brow': 0.3}}), toonDur=0.1, settle=0.6), k(0.44, to=list(ME10), dur=0.1, glide=True, face='keep'), k(0.62, toon={'face': {'lid': 0.5}}, toonDur=0.12)]),   # ...and settles, flat-eyed
        act('copie', CPY10, RY10C, 'stand', 'unimpressed', keys=[k(0.0, look=None), k(0.0, toon=FLAT, toonDur=0.0)]),
        act('drh', [1.55, 0, -0.35], -110, 'stand', 'neutral', keys=[k(0.0, look=[1.0, 1.95, 0.0]), k(0.0, toon={'reach': {'R': [1.42, 1.68, 0.02, 1, 0.06]}, 'hands': {'R': 'grip'}}, toonDur=0.0),
            k(0.45, look=[ME10[0], 2.05, ME10[2]]), k(0.45, toon={'reach': {'R': [1.42, 1.68, 0.02, 1, 0.06]}, 'hands': {'R': 'grip'}, 'face': {'brow': 0.7}}, toonDur=0.1)])],   # (pass 3) she reads the readout, then looks him up and down
        props=[P('cal10', 'caliper', pos=CAL10, scale=CSC, opts={'len': 1.0, 'jaw': 0.34, 'dispW': 0.24, 'dispRy': 0.62, 'gapEase': 0.06, 'gapKeys': [[0.0, GAP(0.34)], [0.04, GAP(0.17)], [0.31, GAP(0.42)], [0.44, GAP(0.34)]], 'text': '30 cm'})],
        cams=[FC(0.0, CAM10, [[ME10[0], 2.45, ME10[2]], [ME10[0], 0.75, ME10[2]], [CPY10[0], 2.42, CPY10[2]], [1.55, 2.3, -0.35], [2.0, 1.7, 0.0], [0.38, 1.7, 0.0]], top=0.2, bottom=0.74)])   # the heads below the title band
st.cue('sfx:clink', 'S10', 0.06, 0.35)
st.card('S10', '30 cm', at=round(EP10 + 0.18, 3))

# 11: he filed a complaint. (pass 2) He brandishes the form at us, RÉCLAMATION in big letters, then slaps it down on her desk, red in the face, steam; she keeps
#     her eyes down on her papers
D11 = st.dur('S11'); SL11 = round(st.at('S11', 'L10', 4) - 0.08, 3)
ME11 = [round(DESK[0] + 0.05, 3), 0, round(DESK[2] + 0.75, 3)]
st.shot('S11', 'office', setOpts=OF, actors=[
        act('mec', ME11, 180, 'stand', 'angry', keys=[k(0.0, look='camera'), k(0.0, toon={'reach': {'R': [round(ME11[0] + 0.78, 3), 1.6, round(ME11[2] + 0.12, 3), 1, 0.06]}, 'hands': {'R': 'pinch'}, 'face': {'red': 0.5, 'brow': -0.8}}, toonDur=0.0),   # (pass 3) the form held up to us by its bottom edge, nearer the lens
            k(round(SL11 - 0.16, 3), toon={'reach': {'R': [round(ME11[0] + 0.15, 3), 2.25, round(ME11[2] - 0.2, 3), 1, 0.06]}, 'hands': {'R': 'flat'}, 'face': {'red': 0.7, 'brow': -0.9}}, toonDur=0.08), k(round(SL11 - 0.1, 3), look=[DESK[0], 0.8, DESK[2]]),
            k(SL11, toon={'reach': {'R': [round(DESK[0] + 0.05, 3), 0.8, round(DESK[2] + 0.2, 3), 1, 0.06]}, 'hands': {'R': 'flat'}, 'face': {'red': 1, 'brow': -0.9, 'jaw': 0.4}, 'sq': [1.1, 0.86, 1.1]}, toonDur=0.04, toonEase='in'),   # slap: he compresses on it
            k(round(SL11 + 0.1, 3), toon={'reach': {'R': [round(DESK[0] + 0.05, 3), 0.8, round(DESK[2] + 0.2, 3), 1, 0.06]}, 'hands': {'R': 'flat'}, 'face': {'red': 1, 'brow': -0.9, 'jaw': 0.3}, 'sq': [0.97, 1.04, 0.97]}, toonDur=0.06),
            k(round(SL11 + 0.3, 3), toon={'reach': {'R': [round(DESK[0] + 0.05, 3), 0.8, round(DESK[2] + 0.2, 3), 1, 0.06]}, 'hands': {'R': 'flat'}, 'face': {'red': 1, 'brow': -0.9, 'steam': 1, 'steamInk': 1}}, toonDur=0.1)]),
        act('drh', DRH, 40, 'stand', 'unimpressed', keys=[k(0.0, look=[round(DESK[0] - 0.25, 3), 0.78, round(DESK[2] - 0.1, 3)]), k(0.0, toon={'face': {'gy': 0.8, 'lid': 0.45}}, toonDur=0.0), k(0.35, toon={'face': {'gy': 0.8, 'lid': 1.0}}, toonDur=0.05), k(0.47, toon={'face': {'gy': 0.8, 'lid': 0.45}}, toonDur=0.06),
            k(round(SL11 + 0.02, 3), toon={'face': {'gy': 0.8, 'lid': 0.55, 'brow': 0.3}, 'sq': [1.0, 1.03, 1.0]}, toonDur=0.03), k(round(SL11 + 0.12, 3), toon={'face': {'gy': 0.8, 'lid': 0.55}}, toonDur=0.08)])],   # (pass 3) a blink; at the slap only a twitch, eyes still down   # (pass 2) eyes down on her papers
        props=[P('desk11', 'desk', pos=DESK), P('papers11', 'paperReam', pos=[round(DESK[0] - 0.25, 3), 0.77, round(DESK[2] - 0.1, 3)], keys=[k(SL11, to=[round(DESK[0] - 0.25, 3), 0.87, round(DESK[2] - 0.1, 3)], dur=0.05, ease='out'), k(round(SL11 + 0.05, 3), to=[round(DESK[0] - 0.25, 3), 0.77, round(DESK[2] - 0.1, 3)], dur=0.08, ease='in')]),   # (pass 3) the ream jumps
               P('form11h', 'paperSheet', on={'actor': 'mec', 'hand': 'R', 'offset': [0, 0.2, 0.1], 'face': 'camera'}, scale=1.3, opts={'w': 0.42, 'h': 0.56, 'head': 'RÉCLAMATION', 'lines': ['Je suis', "l'original."], 'lineSize': 0.08, 'paper': '#FFFFFF', 'bright': True}, keys=[k(round(SL11 + 0.01, 3), visible=False)]),   # (pass 3) held by its edge, above the hand (the fist pushed through it), bigger
               P('form11', 'paperSheet', pos=[round(DESK[0] + 0.05, 3), 0.775, round(DESK[2] + 0.2, 3)], rot=[-PI / 2, 0, 0], opts={'w': 0.34, 'h': 0.46, 'head': 'RÉCLAMATION', 'lines': ['Je suis', "l'original."], 'lineSize': 0.08, 'paper': '#FFFFFF', 'bright': True}, keys=[k(0.0, visible=False), k(round(SL11 + 0.01, 3), visible=True)])],   # (pass 3) on the desk once the hand is down
        cams=[FC(0.0, [round(DESK[0] + 1.35, 3), 1.7, round(DESK[2] - 0.15, 3)], [[ME11[0], 2.45, ME11[2]], [DRH[0], 2.3, DRH[2]], [round(ME11[0] + 0.62, 3), 2.1, round(ME11[2] + 0.05, 3)], [round(ME11[0] + 0.7, 3), 1.45, round(ME11[2] + 0.05, 3)], [round(ME11[0] + 0.35, 3), 2.45, round(ME11[2] - 0.15, 3)], [ME11[0], 0.75, ME11[2]], [DRH[0], 0.9, DRH[2]]], top=0.12, bottom=0.74)])   # (pass 2) side-on: both faces
st.cue('thud', 'S11', SL11, 0.45)

# 12: it was photocopied in five hundred copies. (pass 2) Close at the copier: she slaps the form on the glass and hits the button; cut to him: copies of the
#     complaint rain down from above and stack up round him, jagged, to his chin; his eyes shoot out on stalks; a last sheet lands on his head
D12 = st.dur('S12'); GO12 = round(st.at('S12', 'L11', 2) - 0.15, 3); CUT12 = round(GO12 + 0.24, 3)
ME12 = [round(CP[0] - 1.25, 3), 0, round(CP[2] + 1.0, 3)]
GLASS = [CP[0], 0.975, round(CP[2] + 0.05, 3)]; BTN = [round(CP[0] + 0.45, 3), 1.07, round(CP[2] + 0.38, 3)]
st.shot('S12', 'office', setOpts=OF, actors=[
        act('mec', ME12, 30, 'stand', 'unimpressed', keys=[k(0.0, look='camera'), k(0.0, toon={'face': {'lid': 0.45}}, toonDur=0.0), *take(round(D12 - 0.85, 3), 'tongue', hold=0.3, antic_f=4, settle_f=7)]),   # (pass 3) the pile at his neck: his tongue rolls out (another take)
        act('drh', [round(CP[0] + 0.35, 3), 0, round(CP[2] + 0.85, 3)], -160, 'stand', 'neutral', keys=[k(0.0, look=[CP[0], 1.0, CP[2]]), k(round(GO12 - 0.2, 3), look='camera'), k(0.0, toon={'reach': {'R': [GLASS[0], 1.02, GLASS[2], 1, 0.06]}, 'hands': {'R': 'flat'}}, toonDur=0.0),   # the form slapped on the glass... (pass 3) then she presses without looking, at us
            k(round(GO12 - 0.1, 3), toon={'reach': {'R': [BTN[0], round(BTN[1] + 0.1, 3), round(BTN[2] + 0.05, 3), 1, 0.15]}, 'hands': {'R': 'point'}}, toonDur=0.06), k(GO12, toon={'reach': {'R': [BTN[0], round(BTN[1] - 0.01, 3), BTN[2], 1, 0.15]}, 'hands': {'R': 'point'}}, toonDur=0.04, toonEase='in'), k(round(GO12 + 0.2, 3), toon={}, toonDur=0.15)])],   # ...the button
        props=[COPIER(lid=1.25, lidKeys=[[0.0, 1.25], [round(GO12 - 0.12, 3), 0.0]], scanAt=GO12, scanDur=0.35, btnR=0.052, pressAt=[GO12]), P('form12', 'paperSheet', pos=GLASS, rot=[-PI / 2, 0, 0], scale=1.25, opts={'w': 0.34, 'h': 0.46, 'head': 'RÉCLAMATION', 'lines': ['Je suis', "l'original."], 'lineSize': 0.08, 'paper': '#FFFFFF', 'bright': True}),
               P('rain12', 'paperFountain', pos=[0, 0, 0], opts={'n': 80, 'from': [TRAY[0], 0.7, TRAY[2]], 'pile': [ME12[0], ME12[2]], 'r': 0.62, 'pileH': 1.82, 't0': round(CUT12 + 0.05, 3), 't1': round(D12 - 0.5, 3), 'text': 'RÉCLAMATION', 'stack': True, 'rain': True, 'rainH': 3.3}),   # (pass 2) raining from above, stacked sheets (a smooth cone read as a ball gown)
               P('top12', 'paperSheet', pos=[round(ME12[0] + 0.05, 3), 3.3, ME12[2]], rot=[round(-PI / 2 + 0.55, 3), 0, 0.3], opts={'w': 0.3, 'h': 0.42, 'head': 'RÉCLAMATION', 'paper': '#FFFFFF', 'bright': True}, keys=[k(0.0, visible=False), k(round(D12 - 0.42, 3), visible=True), k(round(D12 - 0.42, 3), to=[round(ME12[0] + 0.05, 3), 2.56, ME12[2]], dur=0.3, ease='in')])],   # the last one lands on his head
        cams=[FC(0.0, [round(CP[0] - 0.75, 3), 2.1, round(CP[2] + 1.75, 3)], [[GLASS[0] - 0.25, 0.98, GLASS[2]], [GLASS[0] + 0.25, 0.98, GLASS[2]], [BTN[0], 1.1, BTN[2]], [round(CP[0] + 0.35, 3), 2.25, round(CP[2] + 0.85, 3)], [round(CP[0] + 0.6, 3), 1.9, round(CP[2] + 0.85, 3)]], top=0.1, bottom=0.74),   # (pass 3) the form, her finger on the button and her whole head in one frame
              FC(CUT12, [round(ME12[0] + 0.35, 3), 1.65, round(ME12[2] + 2.7, 3)], [[ME12[0], 3.0, ME12[2]], [ME12[0], 0.0, ME12[2]], [round(ME12[0] - 0.75, 3), 0.3, ME12[2]], [round(ME12[0] + 0.75, 3), 0.3, ME12[2]]], top=0.08, bottom=0.76, drift=(0.0, 0.0, -0.1))])   # then on him, the sheets falling from the top of the frame
st.cue('sfx:beep', 'S12', GO12, 0.3); [st.cue('sfx:paper', 'S12', round(CUT12 + 0.1 + 0.25 * i, 3), 0.2) for i in range(6)]; st.cue('pop', 'S12', D12 - 0.85, 0.25)

# 13: since then he puts paper in the machine. (pass 2) One pose: on his knees beside the open drawer, three-quarter to us, he slides an oversized ream in;
#     behind him the copies in their rows; he looks at us; a slow blink before the end (no more turning round and jumping up)
D13 = st.dur('S13'); RM13 = round(st.at('S13', 'L12', 2) - 0.1, 3)
ME13 = [round(CP[0] - 0.72, 3), 0, round(CP[2] + 0.78, 3)]; RY13 = 35   # (pass 2) three-quarter to us, the drawer at his right
DRW = [round(CP[0] - 0.08, 3), 0.3, round(CP[2] + 0.48, 3)]           # the mouth of the paper drawer
IN13 = [round(ME13[0] + 0.5, 3), 0.62, round(ME13[2] + 0.12, 3)]      # the ream in his hands
REAMK = lambda c: {'reach': {'L': [round(c[0] - 0.4, 3), round(c[1] + 0.08, 3), c[2], 1, 0.05], 'R': [round(c[0] + 0.4, 3), round(c[1] + 0.08, 3), c[2], 1, 0.05]}, 'hands': {'L': 'flat', 'R': 'flat'}}   # (pass 3) by its two ends: the label clear
st.shot('S13', 'office', setOpts=OF, actors=[
        act('mec', ME13, RY13, 'kneel', 'unimpressed', keys=[k(0.0, look=DRW), k(0.0, toon={**REAMK(IN13), 'face': {'lid': 0.45}}, toonDur=0.0), k(0.3, look='camera'), k(round(RM13 - 0.25, 3), look=DRW),   # (pass 3b) a look at us, back to the drawer...
            k(round(RM13 - 0.2, 3), toon={**REAMK([round(IN13[0] - 0.06, 3), IN13[1], round(IN13[2] - 0.03, 3)]), 'sq': [1.0, 0.97, 1.0], 'face': {'lid': 0.45}}, toonDur=0.15),   # ...and a lean back before the push
            k(RM13, toon={**REAMK(DRW), 'face': {'lid': 0.45}}, toonDur=0.35, toonEase='inOut'),   # the ream slid in
            k(round(RM13 + 0.55, 3), look='camera'), k(round(RM13 + 0.55, 3), toon={**REAMK([DRW[0] - 0.06, DRW[1] + 0.04, DRW[2] + 0.06]), 'face': {'lid': 0.45}}, toonDur=0.15),   # ...his hands still on it, to us
            *[k(round(RM13 + 0.75 + 0.4 * i, 3), toon={**REAMK([DRW[0] - 0.06, DRW[1] + 0.04, DRW[2] + 0.06]), 'sq': [1.0, round(1.0 + 0.018 * (1 - 2 * (i % 2)), 3), 1.0], 'face': {'lid': 0.45}}, toonDur=0.35, toonEase='inOut') for i in range(2)],   # (pass 3) a breath in the hold
            k(round(D13 - 0.62, 3), toon={**REAMK([DRW[0] - 0.06, DRW[1] + 0.04, DRW[2] + 0.06]), 'face': {'lid': 1}}, toonDur=0.14), k(round(D13 - 0.4, 3), toon={**REAMK([DRW[0] - 0.06, DRW[1] + 0.04, DRW[2] + 0.06]), 'face': {'lid': 0.45}}, toonDur=0.16)])],   # a slow blink
        props=[COPIER(lid=0.0, drawerAt=0.0), P('ream13', 'paperReam', pos=IN13, scale=2.6, keys=[k(RM13, to=DRW, dur=0.35, ease='inOut')]),   # (pass 3) twice as big again (shoebox-sized)
               P('copies13', 'copyFountain', pos=[0, 0, 0], opts={'n': 6, 'start': 6, 'recto': True, 'cool': '#D2DEFF', 'painted': True, 'opaque': True, 'grid': {'x0': round(CP[0] - 2.75, 3), 'z0': -3.1, 'dx': 0.62, 'dz': 0.55, 'cols': 3}})],   # behind him along the wall, to his left, in the frame
        cams=[FC(0.0, [round(CP[0] - 1.05, 3), 0.95, round(CP[2] + 3.1, 3)], [[ME13[0], 1.9, ME13[2]], [ME13[0], 0.1, round(ME13[2] + 0.3, 3)], [round(CP[0] + 0.55, 3), 1.05, CP[2]], [round(ME13[0] - 0.9, 3), 1.9, round(ME13[2] - 0.4, 3)]], top=0.14, bottom=0.78, drift=(0.04, 0, -0.06))])   # (pass 2) low in front of him, three-quarter
st.cue('sfx:paper', 'S13', RM13, 0.3)

st.write("La photocopieuse", rig='toon', fingers=True, cloth=True, idleShift=1.6, holdLife=1, limbSmear=1, follow=1, pupil=0.5, extra_cast={
    'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
    'copie': {'preset': 'lemec', 'atlas': None, 'mono': 0.95, 'monoTint': [0.93, 0.97, 1.07], 'monoContrast': 1.35, 'suit': '#585858', 'pants': '#4E4E4E', 'tie': '#8E8E8E', 'lapel': '#B4B4B4', 'skin': '#C6C6C6', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},   # a black-and-white copy of him (the face desaturated by mono, the clothes given in greys)
    'copie2': {'preset': 'lemec', 'atlas': None, 'mono': 0.95, 'monoTint': [0.93, 0.97, 1.07], 'monoContrast': 1.35, 'suit': '#585858', 'pants': '#4E4E4E', 'tie': '#8E8E8E', 'lapel': '#B4B4B4', 'skin': '#C6C6C6', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},   # (pass 3) the other side of the double-sided copy: the same print
    'drh': {'preset': 'madame', 'seed': 491, 'suit': '#7A3E9C', 'hair': 'bun', 'hairColor': '#3A2A20', 'build': {'width': 0.92, 'headWidth': 1.25}},
})
