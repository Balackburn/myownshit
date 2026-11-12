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
        self.scenes = []; self.SH = {}; self.cues = []; self.cards = []

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

    def cue(self, name, sid, t=0.0, gain=0.5, *args):
        """an effect at time t inside shot sid (names: see mix.py: thud, clack, clang, pop, thunder, rain dur, whoosh dur lo hi, gust dur, engine dur, sfx:<name>)"""
        self.cues.append([name, round(self.SH[sid][0] + t, 3), gain, *args])
    def card(self, sid, word, at=None): self.cards.append(f'{sid}:{word}' if at is None else f'{sid}@{at}:{word}')   # at: seconds into the shot (default: at its cut)

    def write(self, title, extra_cast=None, **doc_extra):   # doc_extra: extra top-level keys of the script (rig='toon': the cartoon rig for every human, faces={...}: the story's own expressions)
        d = os.path.join(ROOT, 'stories7', self.name)
        json.dump(self.cues, open(os.path.join(d, 'cues.json'), 'w')); open(os.path.join(d, 'cards.txt'), 'w').write(','.join(self.cards))
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
               'voice': None, 'music': None, 'cast': cast, 'scenes': self.scenes, 'total': self.total, **({'look': self.look} if self.look else {}), **doc_extra}
        out = os.path.join(HERE, f'story_{self.name}.json')
        json.dump(doc, open(out, 'w'), indent=1, ensure_ascii=False)
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
