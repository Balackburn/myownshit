"""story_kit.py: shared helpers for tornado-style stories (.claude/skills/lowpoly-story-style).

    st = Story('sable')                       # loads stories7/sable/timeline.json
    st.plan([('S01', 'L01', 0), ('S02', 'L02', 0), ('S03', 'L02', 4), ...])   # shot ids and the word that opens each
    st.shot('S01', 'seaSurface', actors=[...], props=[...], cams=CU(0, 0))
    st.write('Le sable', extra_cast={...})     # -> scripts-fr/story_sable.json

Framings are built for the narrow 9:16 frame (horizontal half-angle 12.8° at lens 44) and all move a little (push-in / drift).
A character at (x, 0, z) facing +Z (ry 0) is framed from +Z.
"""
import json, os, math
from actu_common import act, k, P, HAND_FLAT, SIGN_UP

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
FPS = 30


def axes_euler(X, Y, Z):
    """The rotation of a prop from its three local axes given in the world (unit, orthogonal, right-handed): (rot x in rad, ry in degrees, rot z in rad),
    for P(..., ry=ry, rot=[rx, 0, rz]) (Euler XYZ, as the engine applies it). Use it for a thing held in space whose direction is set by two points
    (an umbrella from a hand to a collar, a tool that must bite a ticket): aim its long axis, choose where its side faces, take the cross product."""
    return (round(math.atan2(-Z[1], Z[2]), 4), round(math.degrees(math.asin(max(-1.0, min(1.0, Z[0])))), 2), round(math.atan2(-Y[0], X[0]), 4))
def cross3(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def unit3(a): n = math.sqrt(sum(x * x for x in a)) or 1.0; return [x / n for x in a]
def cam(at, frm, to, look, look2=None, lens=44, ease='linear', shake=None, roll=None):
    c = {'at': at, 'from': frm, 'to': to, 'lookAt': look, 'lens': lens, 'ease': ease}
    if look2: c['lookAt2'] = look2
    if shake: c['shake'] = shake
    if roll: c['roll'] = roll
    return c
def glide(c, g=0.2): return {**c[0], 'cut': False, 'glide': g}   # a camera key reached by gliding (g s) instead of cutting: glide([cam(...)], 0.3)
r3 = lambda v: [round(x, 3) for x in v]


def project(frm, look, lens, p, aspect=9 / 16):
    """Where a point of the world falls in the frame of a camera at `frm` that looks at `look` (`lens`: its vertical field in degrees): (x, y, d) with
    x and y as fractions of the width and of the height from the top-left corner (0.5, 0.5: the centre; captions sit at y 0.77-0.83, a one-line
    title card at 0.07-0.18) and d the distance along the axis (m). None when the point is behind the camera. No roll, no shake."""
    f = [look[i] - frm[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in f)) or 1e-9; f = [v / n for v in f]
    r = [-f[2], 0.0, f[0]]; n = math.hypot(r[0], r[2]) or 1e-9; r = [v / n for v in r]                      # right = forward x up
    u = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]]               # up = right x forward
    v = [p[i] - frm[i] for i in range(3)]; d = sum(v[i] * f[i] for i in range(3))
    if d <= 1e-6: return None
    th = math.tan(math.radians(lens) / 2)
    return (round(0.5 + sum(v[i] * r[i] for i in range(3)) / (2 * d * th * aspect), 3), round(0.5 - sum(v[i] * u[i] for i in range(3)) / (2 * d * th), 3), round(d, 3))


def frame_size(lens, d, aspect=9 / 16):
    """(width, height) in metres of what the frame holds at d metres from a camera of vertical field `lens` degrees"""
    h = 2 * d * math.tan(math.radians(lens) / 2); return (round(h * aspect, 3), round(h, 3))


def fit(frm, points, margin=0.07, top=0.08, bottom=0.92, lenses=range(26, 81), aspect=9 / 16):
    """(cycle 7) The aim and the lens of a camera at `frm` that holds every point of `points` ([x, y, z], or a dict name -> point): at least `margin`
    of the width from the sides, between `top` and `bottom` of the height. Returns (look, lens, where): `look` aims at the middle of the points'
    bearings and elevations, `lens` is the narrowest of `lenses` (vertical field, degrees) that fits, `where` is {name or index: (x, y)}; lens None
    when none fits. Measure the points first (script `debugJoints`), and give the extreme pose as well as the held one: a display on a head, a hand
    at full stretch, the top of a pole that bends. The frame is three times narrower than it is tall in angle: with a lens of 44 degrees, 26 degrees
    across: when nothing fits, move the camera (further, or more along the action), do not widen past 65."""
    P = points if isinstance(points, dict) else {i: q for i, q in enumerate(points)}
    yaw, el = [], []
    # (cycle 7) bearings are taken around the bearing of the points' centre: a camera that looks toward -Z sees bearings on both sides of +-180
    # degrees, and their plain average pointed it the other way
    n_ = len(P); y0 = math.atan2(sum(q[0] for q in P.values()) / n_ - frm[0], sum(q[2] for q in P.values()) / n_ - frm[2])
    for q in P.values():
        dx, dy, dz = q[0] - frm[0], q[1] - frm[1], q[2] - frm[2]; yaw.append(y0 + (math.atan2(dx, dz) - y0 + math.pi) % (2 * math.pi) - math.pi); el.append(math.atan2(dy, math.hypot(dx, dz)))
    yc, ec0 = (max(yaw) + min(yaw)) / 2, (max(el) + min(el)) / 2
    look = None
    for lens in lenses:
        # the middle of the points goes to the middle of the window they may fill, not to the middle of the frame (with a caption band to keep clear,
        # the window is the upper three quarters: aimed at the middle of the frame, the lens had to open until the lowest point cleared the band, and
        # the top quarter of the picture stayed empty)
        ec = ec0 - math.atan((0.5 - (top + bottom) / 2) * 2 * math.tan(math.radians(lens) / 2))
        look = [round(frm[0] + 10 * math.sin(yc) * math.cos(ec), 3), round(frm[1] + 10 * math.sin(ec), 3), round(frm[2] + 10 * math.cos(yc) * math.cos(ec), 3)]
        w = {k_: project(frm, look, lens, q, aspect) for k_, q in P.items()}
        if all(v and margin <= v[0] <= 1 - margin and top <= v[1] <= bottom for v in w.values()): return look, lens, {k_: v[:2] for k_, v in w.items()}
    return look, None, {}


def fitBack(frm, points, step=0.25, most=14.0, level=True, inside=None, **kw):
    """(cycle 7, story 45) fit() that backs the camera away from the points until a lens fits: it moves along the line from the points' centre to
    `frm` (so the angle on the action is kept), `step` metres at a time, at most `most` metres; level=True keeps the camera's height (along the 3D
    line a low camera that looks up sank under the floor). Returns (frm, look, lens); lens None if nothing fits.
    Prints how far it went when it had to move: put that distance back in the script when it is more than a step or two. inside=(x0, x1, y0, y1, z0,
    z1): the room the camera must stay in (backed out of the hall it filmed the back of a wall): at its edge the lens opens instead (up to 85)."""
    P = list(points.values()) if isinstance(points, dict) else list(points)
    c = [sum(q[i] for q in P) / len(P) for i in range(3)]; d = [frm[i] - c[i] for i in range(3)]
    if level: d[1] = 0.0
    n = math.sqrt(sum(v * v for v in d)) or 1.0; u = [v / n for v in d]
    back = 0.0
    while back <= most:
        f = [round(frm[i] + u[i] * back, 3) for i in range(3)]
        if inside and not all(inside[2 * i] <= f[i] <= inside[2 * i + 1] for i in range(3)):
            f = [round(frm[i] + u[i] * max(0.0, back - step), 3) for i in range(3)]
            wide = dict(kw); lo = min(kw.get('lenses', range(26, 81))); wide['lenses'] = range(lo, 86)
            look, lens, _ = fit(f, points, **wide)
            print(f'  fitBack: {frm} stopped at the wall, {back - step:.2f} m back, lens {lens}')
            return f, look, lens
        look, lens, _ = fit(f, points, **kw)
        if lens is not None:
            if back > 0: print(f'  fitBack: {frm} moved back {back:.2f} m to {f}')
            return f, look, lens
        back += step
    return frm, None, None


def react(t0, s=1.0, keep=None, look=None, kind='startle'):
    """(cycle 10) A bystander's reaction to a loud beat at t0 (the reviews: "the pound man keeps the same pose through the clack and the jump"),
    as keys to add to a secondary actor. kind 'startle': a two-frame squash, then a jump of the shoulders with the eyes popping and the hair up,
    a shiver, a settle; 'wince': eyes shut, shoulders up, head turned a little away. keep: a toon state to carry under it (toon keys are whole
    states: an actor with a working hand passes its reach here, or the hand drops); look: where his eyes go on it."""
    base = dict(keep or {}); f0 = dict(base.get('face', {}))
    def st_(**k):
        d = dict(base); d.update({x: v for x, v in k.items() if x != 'face'}); d['face'] = {**f0, **k.get('face', {})}; return d
    if kind == 'wince':
        ks = [k(round(t0, 3), toon=st_(sq=[1.04, 0.95, 1.04], face={'lid': 1, 'brow': 0.8, 'jaw': 0.2}), toonDur=0.04, toonEase='out'),
              k(round(t0 + 0.3, 3), toon=st_(face={'lid': 0.3, 'brow': 0.4}), toonDur=0.15)]
    else:
        ks = [k(round(t0, 3), toon=st_(sq=[1.0 + 0.08 * s, 1.0 - 0.08 * s, 1.0 + 0.08 * s]), toonDur=0.03),
              k(round(t0 + 0.067, 3), toon=st_(sq=[1.0 - 0.07 * s, 1.0 + 0.1 * s, 1.0 - 0.07 * s], hairUp=min(1.0, s), face={'pop': 0.35 * s, 'brow': 1, 'jaw': 0.2}), toonDur=0.03, toonEase='out'),
              k(round(t0 + 0.2, 3), toon=st_(sq=[1.0 - 0.05 * s, 1.0 + 0.07 * s, 1.0 - 0.05 * s], hairUp=min(1.0, s) * 0.8, face={'pop': 0.3 * s, 'brow': 1}), toonDur=0.04),
              k(round(t0 + 0.36, 3), toon=st_(sq=[1.02, 0.98, 1.02], face={'brow': 0.6}), toonDur=0.08, toonEase='in'),
              k(round(t0 + 0.5, 3), toon=st_(face={'brow': 0.3}), toonDur=0.12)]
    if look is not None: ks.insert(1, k(round(t0 + 0.04, 3), look=look))
    return ks

def beat(t0, extreme, antic=None, hold=0.3, over=None, settle=None, shiver=0.04, fps=FPS, antic_f=2, settle_f=4):
    """(cycle 9) The timing of a cartoon key pose in one call, as a list of keys for an actor (the reviews kept finding extremes that came and went
    in two frames: no anticipation, no hold, no settle). t0: when the extreme hits (the contact, the sound); extreme: the toon state, snapped to in one
    frame; antic: the state two frames before (default: the extreme's squash turned the other way, 12 %); hold (s, >= 0.2 = six frames): held,
    shivering every two frames by `shiver` on the squash; over: the overshoot past rest (default: a small opposite squash), three frames; settle: the
    rest state (default: no toon), three frames after. Merge the result into the actor's keys: keys=[..., *beat(SN8, JUMP)]. (cycle 13) antic_f: how many frames
    before the extreme the brace starts (2; 4 holds it two frames: the review of 49 saw takes switch on in two frames), settle_f: frames from the overshoot
    to the rest (4; 6-8 for a slower settle)."""
    sq = extreme.get('sq', [1, 1, 1]); inv = [round(1 + (1 - v) * 0.6, 3) for v in sq]
    antic = antic if antic is not None else {'sq': [round(1 + (1 - v) * 1.0, 3) if v != 1 else 1 for v in sq] if 'sq' in extreme else [1.08, 0.88, 1.08]}
    over = over if over is not None else {'sq': inv if 'sq' in extreme else [1.06, 0.94, 1.06]}
    f = 1.0 / fps; ks = [k(round(t0 - antic_f * f, 3), toon=antic, toonDur=round(max(1.5, antic_f / 2) * f, 3)), k(round(t0, 3), toon=extreme, toonDur=round(f, 3), toonEase='out')]
    n = max(0, int(hold / (2 * f)) - 1)
    for i in range(n):
        q = dict(extreme); s_ = 1 + (shiver if i % 2 == 0 else -shiver) * 0.5; q['sq'] = [round(sq[0] / math.sqrt(s_), 3), round(sq[1] * s_, 3), round(sq[2] / math.sqrt(s_), 3)]
        ks.append(k(round(t0 + 2 * f * (i + 1), 3), toon=q, toonDur=round(f, 3)))
    ks += [k(round(t0 + hold, 3), toon=over, toonDur=round(3 * f, 3), toonEase='in'), k(round(t0 + hold + settle_f * f, 3), toon=settle or {}, toonDur=round(max(3, settle_f - 1) * f, 3))]
    return ks


# (cycle 11) the hero's takes, to vary a running gag (the reviews of 48: "the eye-pop take three times in the same shape")
TAKES = {
    'stalks':    {'sq': [0.9, 1.14, 0.9], 'hairUp': 1, 'face': {'pop': 0.75, 'popLen': 0.32, 'brow': 1, 'jaw': 0.3}},          # eyes out on stalks, hair up
    'jaw':       {'sq': [0.97, 1.06, 0.97], 'face': {'jaw': 1.0, 'jawLen': 0.9, 'eye': 0.5, 'brow': 1}},                         # the jaw drops to the chest
    'accordion': {'sq': [1.28, 0.62, 1.28], 'face': {'pop': 0.35, 'brow': 1, 'eye': 0.3}},                                       # squashed down like a concertina
    'hair':      {'sq': [0.94, 1.08, 0.94], 'hairUp': 1.3, 'face': {'eye': 0.55, 'brow': 1, 'jaw': 0.15}},                       # the hair stands straight up, eyes wide
    'tongue':    {'sq': [0.96, 1.05, 0.96], 'face': {'tongue': 1, 'tongueLen': 0.55, 'jaw': 0.85, 'pop': 0.35, 'brow': 1}},      # the tongue rolls out
    'cross':     {'sq': [0.97, 1.04, 0.97], 'face': {'cross': 1, 'tremble': 1, 'brow': 0.9, 'jaw': 0.2}},                        # cross-eyed, trembling
}


def doubleTake(t0, look_at, keep=None, back='camera', pop=0.6):
    """(cycle 12) A double take, as keys for an actor: a glance at something (look_at: a point or 'camera'), back to `back`, then two frames later
    the head snaps back to it with a dip and a stretch, the eyes out on stalks, held, then a settle. keep: toon channels to carry through the take
    (a reach, a sit). The reviewers asked for one in several stories (none had it): use it when a character notices something absurd late."""
    keep = dict(keep or {})
    return [k(t0, look=look_at), k(round(t0 + 0.16, 3), look=back), k(round(t0 + 0.27, 3), look=look_at),
            k(round(t0 + 0.23, 3), toon={**keep, 'sq': [1.04, 0.95, 1.04]}, toonDur=0.03),
            k(round(t0 + 0.27, 3), toon={**keep, 'sq': [0.95, 1.06, 0.95], 'face': {'pop': pop, 'popLen': 0.25, 'brow': 1, 'jaw': 0.3}}, toonDur=0.04, toonEase='outBack'),
            k(round(t0 + 0.62, 3), toon={**keep, 'face': {'brow': 0.6}}, toonDur=0.12)]

def take(t0, kind='stalks', keep=None, hold=0.3, s=1.0, antic_f=2, settle_f=4):
    """(cycle 11) The hero's cartoon take at t0, built on beat(): two frames of anticipation, the extreme held `hold` s with a shiver (the hang time),
    the overshoot, the settle. kind: one of TAKES ('stalks', 'jaw', 'accordion', 'hair', 'tongue', 'cross'): change it from one gag to the next.
    keep: a toon state carried under the take and returned to after it (toon keys are whole states: a guided hand is kept); s doses the squash."""
    ex = dict(keep or {}); tk = TAKES[kind]; f0 = dict(ex.get('face', {}))
    ex.update({x: v for x, v in tk.items() if x != 'face'}); ex['face'] = {**f0, **tk.get('face', {})}
    if s != 1.0 and 'sq' in ex: ex['sq'] = [round(1 + (v - 1) * s, 3) for v in ex['sq']]
    an = dict(keep or {}); an['sq'] = [round(1 + (1 - v) * 0.8, 3) for v in ex.get('sq', [1, 1, 1])]   # the anticipation keeps the carried state too
    return beat(t0, ex, antic=an, hold=hold, settle=dict(keep) if keep else None, antic_f=antic_f, settle_f=settle_f)


def bands(frm, look, lens, points, card=False, aspect=9 / 16):
    """(cycle 7) Which of `points` (dict name -> [x, y, z]) fall outside the frame, in the caption band (0.77-0.83 of the height) or, with card=True,
    in the band of a one-line title card (0.07-0.18): a list of (name, 'out' | 'captions' | 'card', (x, y)). Call it on what must be read: a face, a
    stamp, the lettering of a prop, the hand that makes the gag."""
    bad = []
    for k_, q in points.items():
        v = project(frm, look, lens, q, aspect)
        if not v or not (0 <= v[0] <= 1 and 0 <= v[1] <= 1): bad.append((k_, 'out', v and v[:2]))
        elif 0.77 <= v[1] <= 0.83: bad.append((k_, 'captions', v[:2]))
        elif card and 0.07 <= v[1] <= 0.18: bad.append((k_, 'card', v[:2]))
    return bad


# standard framings: (x, z) is the subject's feet, the subject faces +Z; dx shifts the camera sideways
def CU(x=0, z=0, h=1.75, dx=0.25, d=1.7, shake=0.008, lens=44):       # face close-up
    return [cam(0.0, [x + dx, h, z + d], [x + dx * 0.9, h, z + d - 0.18], [x, h - 0.03, z], [x, h - 0.02, z], lens=lens, shake=shake)]
def MS(x=0, z=0, h=1.35, dx=0.35, d=3.0, shake=None, lens=44):         # waist up
    return [cam(0.0, [x + dx, h, z + d], [x + dx * 0.9, h + 0.02, z + d - 0.3], [x, h - 0.05, z], [x, h - 0.03, z], lens=lens, shake=shake)]
def WS(x=0, z=0, h=1.5, dx=0.6, d=7.0, look_h=1.2, lens=44, shake=None):   # full scene, 3-4 people
    return [cam(0.0, [x + dx, h, z + d], [x + dx * 0.85, h + 0.05, z + d - 0.6], [x, look_h, z], [x, look_h + 0.03, z], lens=lens, shake=shake)]
def LOW(x=0, z=0, d=2.8, dx=0.4, look_h=1.7, lens=50, shake=None):      # hero low angle, looking up
    return [cam(0.0, [x + dx, 0.45, z + d], [x + dx * 0.9, 0.48, z + d - 0.25], [x, look_h, z], [x, look_h + 0.05, z], lens=lens, shake=shake)]
def TOP(x=0, z=0, h=1.6, look_h=0.8, lens=42, shake=None):              # top-down on a desk
    return [cam(0.0, [x, h, z + 0.55], [x, h - 0.05, z + 0.5], [x, look_h, z], [x, look_h, z], lens=lens, shake=shake)]


class Story:
    def __init__(self, name, look=None):
        self.name = name; self.look = look   # look='natural' (light probe, soft shadows, auto exposure) or 'shaders' (engine/look.js)
        self.TL = json.load(open(os.path.join(ROOT, 'stories7', name, 'timeline.json')))
        self.L = {l['id']: l for l in self.TL['lines']}; self.total = self.TL['total']
        self.scenes = []; self.SH = {}; self.cues = []; self.cards = []; self.gags = []

    def ws(self, lid, w=0): return self.L[lid]['words'][w]['s']
    def cut(self, lid, w=0): return round(round((self.ws(lid, w) - 1 / FPS) * FPS) / FPS, 4)

    def plan(self, shots):
        t = [0.0] + [self.cut(l, w) if isinstance(l, str) else round(round(l * FPS) / FPS, 4) for _, l, w in shots[1:]] + [self.total]   # ('S15', 22.25, 0): a cut at a time (after the narration)
        self.SH = {sid: (t[i], t[i + 1]) for i, (sid, _, _) in enumerate(shots)}
        return self.SH

    def dur(self, sid): a, b = self.SH[sid]; return round(b - a, 3)
    def at(self, sid, lid, w=0): return round(self.ws(lid, w) - self.SH[sid][0], 3)   # a word's time inside a shot

    def talk(self, lid, sid, base='neutral'):
        t0 = self.SH[sid][0]; ks = []
        for w in self.L[lid]['words']:
            a, b = w['s'] - t0, w['e'] - t0
            if b < 0: continue
            ks += [k(round(max(0, a), 3), expr='talk'), k(round(max(0, b - 0.03), 3), expr=base)]
        return ks

    def shot(self, sid, set_=None, actors=(), props=(), cams=(), **kw):
        a, b = self.SH[sid]
        self.scenes.append({'id': sid, 'set': set_, 'lines': [], 'actors': list(actors), 'props': list(props), 'sfx': [], 'cams': list(cams),
                            'start': round(a, 4), 'duration': round(b - a, 4), **kw})

    def where(self, sid, t, p):
        """Where the point p of the world falls in the frame at t seconds into shot sid (explicit `cam(...)` keys of that shot, already declared):
        (x, y, d) as in project(). A key runs from its own time to the next key's; a glide key is taken as arrived. Use it before rendering a
        still: a head cut by the top, a text out of the frame, feet in the caption band."""
        sc = next(x for x in self.scenes if x['id'] == sid); cs = sorted([c for c in sc['cams'] if 'from' in c], key=lambda c: c['at'])
        i = max([j for j, c in enumerate(cs) if c['at'] <= t + 1e-9] or [0]); c = cs[i]; t1 = cs[i + 1]['at'] if i + 1 < len(cs) else sc['duration']
        w = 0.0 if t1 <= c['at'] else min(1.0, max(0.0, (t - c['at']) / (t1 - c['at'])))
        if c.get('ease') == 'out': w = 1 - (1 - w) ** 3
        elif c.get('ease') == 'in': w = w ** 3
        elif c.get('ease') == 'inOut': w = w * w * (3 - 2 * w)
        mix = lambda a, b_: [a[j] + (b_[j] - a[j]) * w for j in range(3)]
        return project(mix(c['from'], c.get('to') or c['from']), mix(c['lookAt'], c.get('lookAt2') or c['lookAt']), c.get('lens', 40), p)

    def audit(self, hero=('mec',), height=2.25, quiet=False):
        """(cycle 9) A staging check on the declared cameras (explicit cam(...) keys), run by write(): for each camera key, at its start, middle and
        end, where each actor's feet and head fall in the frame and which way his body faces. Warns (prints) when a whole figure has its head cut by
        the top, when the feet stand in the caption band (0.77-0.86) under a visible head, and when a hero turns his back to the camera (more than
        120 degrees: a move without face= turns the body to its heading; face='keep' keeps it). Root positions follow the 'to' keys linearly; poses,
        stretches and looks are not known here: a warning is a question to check on a still, not a verdict. Returns the list of warnings."""
        out = []
        for sc in self.scenes:
            cs = sorted([c for c in sc['cams'] if 'from' in c], key=lambda c: c['at'])
            if not cs: continue
            boxes = {}   # (cycle 10) t -> [(id, x0, x1, y0, y1, depth)]: who stands in front of the hero
            for a in sc['actors']:
                if not isinstance(a, dict) or 'pos' not in a: continue
                keys = sorted([x for x in a.get('keys', []) if isinstance(x, dict)], key=lambda x: x.get('at', 0)); seen = set()
                pp, ff = list(a['pos']), math.radians(a.get('ry', 0) or 0)   # a glide (carried, floating, sliding) that turns the body: rarely meant
                for x in keys:
                    if 'to' in x and isinstance(x['to'], (list, tuple)):
                        q = x['to']; dh = math.hypot(q[0] - pp[0], q[2] - pp[2])
                        if x.get('glide') and 'face' not in x and dh > 0.05:
                            hd_ = math.atan2(q[0] - pp[0], q[2] - pp[2]); turn = abs((hd_ - ff + math.pi) % (2 * math.pi) - math.pi)
                            if math.degrees(turn) > 45: out.append(f'{sc["id"]} t={x.get("at", 0):.2f}: {a["id"]} turned {math.degrees(turn):.0f} deg by a glide without face= (face=\'keep\' or a yaw keeps him)')
                            ff = hd_
                        elif isinstance(x.get('face'), (int, float)): ff = math.radians(x['face'])
                        elif x.get('face', 'move') == 'move' and dh > 0.05: ff = math.atan2(q[0] - pp[0], q[2] - pp[2])
                        pp = list(q)
                    elif isinstance(x.get('face'), (int, float)): ff = math.radians(x['face'])
                def state(t):
                    p = list(a['pos']); f = math.radians(a.get('ry', 0) or 0)
                    for x in keys:
                        t0 = x.get('at', 0)
                        if t0 > t: break
                        if 'to' in x and isinstance(x['to'], (list, tuple)):
                            q = list(x['to']); d = x.get('dur', 0) or 0; w = 1.0 if d <= 0 else min(1.0, max(0.0, (t - t0) / d))
                            mode = x.get('face', 'move')
                            if mode == 'move' and math.hypot(q[0] - p[0], q[2] - p[2]) > 0.05: f = math.atan2(q[0] - p[0], q[2] - p[2]) + (math.pi if x.get('back') else 0)
                            elif isinstance(mode, (int, float)): f = math.radians(mode)
                            p = [p[i] + (q[i] - p[i]) * w for i in range(3)] if w < 1 else q
                        elif isinstance(x.get('face'), (int, float)): f = math.radians(x['face'])
                    return p, f
                for i, c in enumerate(cs):
                    t1 = cs[i + 1]['at'] if i + 1 < len(cs) else sc['duration']
                    for t in sorted({round(c['at'] + 0.05, 3), round((c['at'] + t1) / 2, 3), round(max(c['at'], t1 - 0.05), 3)}):
                        p, f = state(t); sc_ = (a.get('scale') or 1.0)
                        ft = self.where(sc['id'], t, p); hd = self.where(sc['id'], t, [p[0], p[1] + height * sc_, p[2]])
                        if not ft or not hd: continue
                        inx = -0.1 <= ft[0] <= 1.1 and -0.1 <= hd[0] <= 1.1
                        if not inx: continue
                        cpos = c['from'] if not c.get('to') else [c['from'][j] + (c['to'][j] - c['from'][j]) * min(1, max(0, (t - c['at']) / max(1e-6, t1 - c['at']))) for j in range(3)]
                        vx, vz = p[0] - cpos[0], p[2] - cpos[2]; vn = math.hypot(vx, vz) or 1.0; lx, lz = -vz / vn * 0.32 * sc_, vx / vn * 0.32 * sc_
                        mid = p[1] + 0.55 * height * sc_; pl = self.where(sc['id'], t, [p[0] - lx, mid, p[2] - lz]); pr = self.where(sc['id'], t, [p[0] + lx, mid, p[2] + lz])
                        if pl and pr: boxes.setdefault(t, []).append((a['id'], min(pl[0], pr[0]), max(pl[0], pr[0]), min(hd[1], ft[1]), max(hd[1], ft[1]), ft[2] if len(ft) > 2 else 0.0))
                        msg = None
                        if hd[1] < 0.0 and 0.0 <= ft[1] <= 1.0: msg = f'{a["id"]} head cut by the top (head y {hd[1]:.2f}, feet y {ft[1]:.2f})'
                        elif 0.77 <= ft[1] <= 0.86 and 0.0 <= hd[1] < 0.77: msg = f'{a["id"]} feet in the caption band (y {ft[1]:.2f})'
                        if msg and (msg.split(' (')[0]) not in seen: seen.add(msg.split(' (')[0]); out.append(f'{sc["id"]} t={t:.2f}: {msg}')
                        lying = any('lie' in str(x.get('clip', '')) for x in keys if x.get('at', 0) <= t) or 'lie' in str(a.get('clip', ''))
                        if a['id'] in hero and 0.0 <= hd[1] <= 1.0 and not lying:
                            pos = c['from'] if not c.get('to') else [c['from'][j] + (c['to'][j] - c['from'][j]) * min(1, max(0, (t - c['at']) / max(1e-6, t1 - c['at']))) for j in range(3)]
                            tc = math.atan2(pos[0] - p[0], pos[2] - p[2]); ang = abs((f - tc + math.pi) % (2 * math.pi) - math.pi)
                            if 65 <= math.degrees(ang) <= 115 and 'profile' not in seen and 'back' not in seen: seen.add('profile'); out.append(f'{sc["id"]} t={t:.2f}: {a["id"]} in profile ({math.degrees(ang):.0f} deg): the side of a box head has no painted face, it reads as the back of his head (cycle 12)')
                            fh = abs(ft[1] - hd[1])
                            if 0.0 <= ft[1] <= 1.0 and fh < 0.28 and 'small' not in seen: seen.add('small'); out.append(f'{sc["id"]} t={t:.2f}: {a["id"]} small at phone size: the whole figure {100 * fh:.0f} % of the frame height, the head about {25 * fh:.0f} % (cycle 12: under about 7 % the reviewers stop reading the face)')
                            if math.degrees(ang) > 120 and 'back' not in seen: seen.add('back'); out.append(f'{sc["id"]} t={t:.2f}: {a["id"]} turned {math.degrees(ang):.0f} deg away from the camera (a move without face=? face=\'keep\' keeps the facing)')
            said = set()   # (cycle 10) an actor between the camera and the hero, covering a good part of him (45 S17: the pound man's back hid the swell)
            for t, bs in sorted(boxes.items()):
                for h in [b for b in bs if b[0] in hero]:
                    ha = max(1e-6, (h[2] - h[1]) * (h[4] - h[3]))
                    for o in bs:
                        if o[0] == h[0] or o[5] >= h[5] or (sc['id'], o[0]) in said: continue
                        ov = max(0.0, min(h[2], o[2]) - max(h[1], o[1])) * max(0.0, min(h[4], o[4]) - max(h[3], o[3]))
                        if ov / ha > 0.4: said.add((sc['id'], o[0])); out.append(f'{sc["id"]} t={t:.2f}: {o[0]} stands in front of {h[0]} and covers {100 * ov / ha:.0f} % of him (move one of them or the camera)')
        if not quiet:
            for w in out: print('  audit', w)
        return out

    def cue(self, name, sid, t=0.0, gain=0.5, *args):
        """an effect at time t inside shot sid (names: see mix.py: thud, clack, clang, pop, thunder, rain dur, whoosh dur lo hi, gust dur, engine dur, sfx:<name>)"""
        self.cues.append([name, round(self.SH[sid][0] + t, 3), gain, *args])
    def card(self, sid, word, at=None): self.cards.append(f'{sid}:{word}' if at is None else f'{sid}@{at}:{word}')   # at: seconds into the shot (default: at its cut)

    def gag(self, sid, t, who='mec', name=None):
        """(cycle 13) Declare the key pose of a gag: t seconds into shot sid, the actor whose face must read there. write() puts them in the script
        (script.gags, with the title-card times as script.cardTimes) and `node render/render3.mjs scripts-fr/story_X.json --timed --w 288 --h 512 --probe`
        measures each one in the engine, with the real pose, stretch and props: the head cut by the frame, too small to read, covered (and by what: a
        prop, another actor, his own arm), in the caption band or under a title card (the reviews of 47-49 found the peak hidden in each of these ways)."""
        self.gags.append({'t': round(self.SH[sid][0] + t, 3), 'who': who, 'name': name or f'{sid}+{t:g}', 'sid': sid})

    def audit_life(self, still=1.3, quiet=False):
        """(cycle 13) Two checks the reviews kept asking for, on the keys alone (run by write()):
        - an actor in the frame who gets no key for `still` seconds or more on a static clip (stand, sit, idle): "frozen" (the mother still for 1.7 s,
          the row frozen until the word); give him a blink, a glance, a breath or a weight shift;
        - the eyes-on-stalks take (face pop >= 0.3) in more than three shots: "the take is the default, at the same size"; vary it (a jaw drop, a
          squash, the hair standing up, a dazed wobble, a ta-da, crossed eyes, doubleTake())."""
        out, stalks = [], []
        static = (None, 'stand', 'sit', 'idle')
        for sc in self.scenes:
            sid, D = sc['id'], sc['duration']
            for a in sc['actors']:
                if not isinstance(a, dict) or 'pos' not in a: continue
                keys = sorted([x for x in a.get('keys', []) if isinstance(x, dict)], key=lambda x: x.get('at', 0))
                if any((x.get('toon') or {}).get('face', {}).get('pop', 0) >= 0.3 for x in keys): stalks.append((sid, a['id']))
                busy, clip, clip_t = [], a.get('clip'), 0.0
                vis = [(0.0, a.get('visible', True) is not False)] + [(x.get('at', 0), bool(x['visible'])) for x in keys if 'visible' in x]
                for x in keys:
                    t0 = x.get('at', 0); busy.append((t0, t0 + 0.05))
                    if 'to' in x: busy.append((t0, t0 + (x.get('dur', 0) or 0)))
                    if 'clip' in x:
                        if clip not in static: busy.append((clip_t, t0))
                        clip, clip_t = x['clip'], t0
                        if x.get('then') and x['then'] not in static: busy.append((t0, D))
                if clip not in static: busy.append((clip_t, D))
                busy.sort(); edge, gaps = 0.0, []
                for b0, b1 in busy + [(D, D)]:
                    if b0 - edge >= still: gaps.append((edge, b0))
                    edge = max(edge, b1)
                for g0, g1 in gaps:
                    tm = (g0 + g1) / 2; shown = [v for tv, v in vis if tv <= tm]
                    if shown and not shown[-1]: continue
                    p = a['pos']
                    for x in keys:
                        if 'to' in x and x.get('at', 0) <= tm and isinstance(x['to'], (list, tuple)): p = x['to']
                    try: hd = self.where(sid, tm, [p[0], p[1] + 1.9 * (a.get('scale') or 1.0), p[2]])
                    except Exception: hd = None
                    if not hd or not (0.0 <= hd[0] <= 1.0 and 0.0 <= hd[1] <= 1.0): continue
                    out.append(f'{sid} {a["id"]} still from {g0:.2f} to {g1:.2f} s ({g1 - g0:.1f} s with no key on a static clip): a blink, a glance, a breath or a weight shift (cycle 13)')
        shots = sorted({s_ for s_, _ in stalks})
        if len(shots) > 3: out.append(f'eyes-on-stalks take (face pop >= 0.3) in {len(shots)} shots ({", ".join(shots)}): keep the big one for the peak and vary the others (cycle 13)')
        if not quiet:
            for w in out: print('  audit', w)
        return out

    def write(self, title, extra_cast=None, **doc_extra):   # doc_extra: extra top-level keys of the script (rig='toon': the cartoon rig for every human, faces={...}: the story's own expressions)
        d = os.path.join(ROOT, 'stories7', self.name)
        try:   # (cycle 10) a cue the final mix cannot play fails only after the 1080p render (45: 'splat' without 'sfx:'): say it now
            import re as _re
            _a3 = open(os.path.join(ROOT, 'tools', 'audio3.py')).read() + open(os.path.join(ROOT, 'tools', 'audio.py')).read()
            _sfx = set(_re.findall(r"name == '([a-zA-Z]+)'", _a3)) | set(_re.findall(r"['\"]([a-zA-Z]+)['\"]\s*:", _a3))
            _mix = {'thunder', 'thud', 'clack', 'clang', 'pop', 'rain', 'whoosh', 'gust', 'engine'}
            for _c in self.cues:
                _n = _c[0]
                if (_n.startswith('sfx:') and _n[4:] not in _sfx) or (not _n.startswith('sfx:') and _n not in _mix): print(f'  audit cue {_n!r} at {_c[1]:.2f} s: the mix has no such sound (built-ins: {sorted(_mix)}; others as sfx:<name>)')
        except OSError: pass
        json.dump(self.cues, open(os.path.join(d, 'cues.json'), 'w')); open(os.path.join(d, 'cards.txt'), 'w').write(','.join(self.cards))
        cardT = []   # (cycle 13) the title-card times, for the key-pose probe (a gag's peak under the card)
        for c_ in self.cards:
            h_ = c_.split(':', 1)[0]
            if '@' in h_: s_, a_ = h_.split('@'); cardT.append(round(self.SH[s_][0] + float(a_), 3))
            elif h_ in self.SH: cardT.append(round(self.SH[h_][0], 3))
        json.dump({sid: [round(a, 4), round(b, 4)] for sid, (a, b) in self.SH.items()}, open(os.path.join(d, 'shots.json'), 'w'))
        for sc in self.scenes:
            for p in sc['props']:
                if 'rot' in p and 'ry' not in p: p['ry'] = round(math.degrees(p['rot'][1]), 3)
            s = sc['set']; dry = sc.get('setOpts', {}).get('dry')
            if self.look: sc.setdefault('grade', 'none'); sc.setdefault('soften', 0.3)
            sc.setdefault('grade', {'spaceDark': 'contrast(0.95) saturate(1.1) brightness(1.02)', 'seabed': 'contrast(0.92) saturate(1.12) brightness(1.06)' if not dry else 'contrast(0.9) saturate(1.08) brightness(1.08)'}
                          .get(s, 'contrast(0.9) saturate(1.06) brightness(1.1)' if s in ('office', 'brightCell', 'poste', 'livingRoom', 'replicaCourt', 'pressRoom', 'chambre', 'interrogation') else 'contrast(0.9) saturate(1.08) brightness(1.08)'))
            sc.setdefault('soften', 0.84)
        cast = {'mec': {'preset': 'lemec', 'tint': '#E6F2FF', 'build': {'width': 0.82, 'headWidth': 1.3, 'headScale': 1.0}},
                'flic': {'preset': 'cop', 'suit': '#1E2D4A', 'pants': '#1E2D4A', 'facial': 'none', 'atlas': 'lemec', 'atlasBody': False, 'build': {'width': 0.82, 'headWidth': 1.3}},
                'flic2': {'preset': 'cop', 'suit': '#1E2D4A', 'pants': '#1E2D4A', 'facial': 'mustache', 'hair': 'receding', 'seed': 41, 'build': {'width': 0.86, 'headWidth': 1.3, 'belly': 0.08}},
                'juge': {'preset': 'judge', 'facial': 'stubble', 'atlas': 'lemec', 'atlasBody': False, 'build': {'width': 0.86, 'headWidth': 1.3, 'headScale': 1.05}},
                **(extra_cast or {})}
        doc = {'version': 3, 'title': title, 'grade': 'contrast(0.9) saturate(1.05) brightness(1.06)', 'captionWords': 0, 'captionY': 0.81, 'tempo': 1.0,
               'voice': None, 'music': None, 'cast': cast, 'scenes': self.scenes, 'total': self.total, **({'look': self.look} if self.look else {}),
               **({'gags': self.gags, 'cardTimes': cardT} if self.gags else {}), **doc_extra}
        out = os.path.join(HERE, f'story_{self.name}.json')
        json.dump(doc, open(out, 'w'), indent=1, ensure_ascii=False)
        try: self.audit()   # (cycle 9) staging warnings: heads cut, feet in the caption band, the hero's back to the camera
        except Exception as e: print('  audit failed:', e)
        try: self.audit_life()   # (cycle 13) frozen actors, the same take everywhere
        except Exception as e: print('  audit_life failed:', e)
        print(out, len(self.scenes), 'shots', self.total, 's')
        return out


def JUDGE(hit=0.4, nameplate='TRIBUNAL', extra_props=()):
    """the replica's S16 courtroom: the judge strikes the gavel at `hit` s, low on the bench, slow push-in (st.shot(sid, **JUDGE()))"""
    return dict(set_='replicaCourt', setOpts={'handle': nameplate, 'windowX': -1.5, 'chairW': 1.2, 'chairH': 2.75, 'chairX': 0.15, 'benchGlow': '#5A564A'},
                actors=[act('juge', [-0.35, -0.3, -14.0], -35, 'gavelStrikeL', params={'hit': hit})],
                props=[P('specs', 'glasses', on={'actor': 'juge', 'joint': 'head', 'offset': [0.02, 0.17, 0.15]}, opts={'r': 0.042, 'dx': 0.07}),
                       P('gavelUp', 'gavel', on={'actor': 'juge', 'hand': 'L'}, keys=[k(0.0, visible=True), k(round(hit - 0.02, 3), visible=False)]),
                       P('gavel', 'gavel', pos=[-0.37, 1.41, -13.3], rot=[0, 0, -1.5708], keys=[k(0.0, visible=False), k(round(hit - 0.02, 3), visible=True)]),
                       P('block', 'soundBlock', pos=[0.1, 1.18, -13.3]), *extra_props],
                cams=[cam(0.0, [-0.1, 1.29, -11.8], [-0.12, 1.30, -12.05], [-0.27, 1.55, -14.0], [-0.27, 1.55, -14.0], lens=45)],
                fx=[{'type': 'shake', 'at': hit, 'dur': 0.18, 'amount': 0.018}])
