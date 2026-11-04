"""shots.py — the replica, shot by shot (frames from analysis/shots.json). Edit, rebuild with build.py, compare, repeat."""
import json, os
from tsx import Doc, Shot, caption, card, ms, lin, ext, euler, FPS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = json.load(open(os.path.join(ROOT, 'analysis', 'shots.json')))
FR = {s['id']: s['frames'] for s in SPEC['shots']}

SKY = '#A9CFE3'
SIDEWALK = '#E4D6BE'
ROAD = '#6E6E72'
LAWN = '#8CC063'


TOWNHOUSES = ('townhouse_white', 'townhouse_purple', 'townhouse_yellow', 'townhouse_blue', 'townhouse_pink', 'townhouse_red')


def street(sh, z0=-400, n=8, far=True, trees=True):
    """suburban street along Z: road x -1050..-150 with a dashed centre line; near sidewalk, lawn, picket fence and a row of
    pastel 2-storey townhouses on +X (fronts facing the road, rotY 90); the same on the far side (-X, rotY -90)"""
    sh.ground(SIDEWALK)
    sh.box((900, 4, 20000), (-600, -1, 0), ROAD, name='road', shadows=False)
    for i in range(50): sh.box((14, 5, 160), (-600, -2, -5000 + i * 400), '#F4F1E8', name='dash', shadows=False)
    sh.box((900, 4, 20000), (750, -1, 0), LAWN, name='lawns near', shadows=False)
    sh.box((900, 4, 20000), (-1950, -1, 0), LAWN, name='lawns far', shadows=False)
    for i in range(n):
        sh.model(TOWNHOUSES[i % 6], (900, 0, z0 + i * 560), rot=(0, 90, 0), name=f'house near {i}')
        if far: sh.model(TOWNHOUSES[(i + 3) % 6], (-2100, 0, z0 + 280 + i * 560), rot=(0, -90, 0), name=f'house far {i}')
    for i in range(n * 2):
        sh.model('fence', (300, 0, z0 - 150 + i * 300), rot=(0, 90, 0), name=f'fence near {i}')
        if far: sh.model('fence', (-1500, 0, z0 - 150 + i * 300), rot=(0, 90, 0), name=f'fence far {i}')
    if trees:
        for i in range(n // 2):
            sh.model('tree', (520, 0, z0 + 420 + i * 1120), name=f'tree near {i}')
            sh.model('tree', (-1720, 0, z0 + 700 + i * 1120), name=f'tree far {i}')


def s1(d):
    f0, f1 = FR['S1']; sh = Shot(d, 101, 'S1 walk', f0, f1)
    street(sh)
    sh.sun(rx=-48, ry=-40, irradiance=3.4)
    man = sh.model('lemec', (40, 0, 0), rot=(0, 0, 0), clip='walk', clip_rate=1.0, name='man')
    sh.anim(man, 'position', [(0, [40, 0, 0]), (sh.nframes, [40, 0, -230])])
    sh.anim(man, 'rotationY', [(0, 0), (24, 0), (44, 40, 'inout'), (sh.nframes, 60)], 'float')
    dog = sh.model('voxeldog', (-75, 0, -110), rot=(0, 0, 0), scale=125, name='dog')
    sh.anim(dog, 'position', [(0, [-75, 0, -110]), (34, [-60, 0, -290]), (42, [-20, -110, -200], 'in'), (sh.nframes, [520, -620, 1500], 'in')])
    tor = sh.model('tornado_big', (650, 0, 1700), scale=260, name='tornado')
    sh.script(tor, 'rotationY', 'return input.time.seconds * 140;')
    # low and close, tracking back with him; swings round to his right side (motion blur in the reference, f10-25)
    sh.camera((-10, -85, -260), (30, -150, 0), fov=50,
              keys=[(0, [-10, -85, -260]), (10, [-10, -85, -330]), (24, [-300, -110, -210], 'inout'), (sh.nframes, [-330, -120, -300])],
              tkeys=[(0, [30, -150, 0]), (10, [30, -150, -70]), (24, [60, -160, -40], 'inout'), (sh.nframes, [420, -330, 1300])])


def s3(d, rot=-130):
    f0, f1 = FR['S3']; sh = Shot(d, 103, 'S3 theft', f0, f1)
    street(sh, z0=-1800, n=8)
    sh.sun(rx=-48, ry=-40, irradiance=3.4)
    # on the near kerb, facing camera-left; the camera looks across the road at the far houses (low, tilted up)
    sh.model('lemec', (-120, 0, 0), rot=(0, rot, 0), clip='explain', clip_rate=1.0, name='man')
    sh.camera((40, -90, -40), (-150, -228, 20), fov=46)


def s2(d):
    """dog spinning inside the tornado wall: close tracking shot, the dog drifts left to centre, mouth opens"""
    f0, f1 = FR['S2']; sh = Shot(d, 102, 'S2 dog in tornado', f0, f1, amb=0.7)
    sh.ground(LAWN)
    sh.sun(rx=-40, ry=-30, irradiance=3.0)
    tor = sh.model('tornado_big', (0, 0, 420), scale=520, name='tornado wall')
    sh.script(tor, 'rotationY', 'return input.time.seconds * 60;')
    dog = sh.model('voxeldog_tongue', (-60, -620, 0), rot=(10, -35, -15), scale=160, name='dog')
    sh.anim(dog, 'position', [(0, [-70, -620, 0]), (sh.nframes, [10, -640, 30])])
    sh.anim(dog, 'rotationZ', [(0, -15), (sh.nframes, 10)], 'float')
    sh.camera((-40, -640, -170), (-20, -630, 0), fov=50,
              keys=[(0, [-60, -640, -170]), (sh.nframes, [0, -650, -150])], tkeys=[(0, [-40, -625, 0]), (sh.nframes, [10, -640, 20])])


def s4(d):
    """selfie close-up: phone at the ear, the street receding behind him, the tornado far down the road"""
    f0, f1 = FR['S4']; sh = Shot(d, 104, 'S4 phone', f0, f1)
    street(sh, z0=-200, n=12)
    sh.sun(rx=-48, ry=-40, irradiance=3.4)
    sh.model('lemec', (-60, 0, 0), rot=(0, 0, 0), clip='phoneCall', clip_rate=0.8, name='man')
    tor = sh.model('tornado_big', (-450, 0, 6200), scale=300, name='tornado far')
    sh.script(tor, 'rotationY', 'return input.time.seconds * 140;')
    sh.camera((-40, -175, -95), (-60, -195, 0), fov=58, keys=[(0, [-40, -175, -95]), (sh.nframes, [-35, -178, -88])])


CAPTIONS = SPEC['captions']


def build(only=None, captions=True):
    d = Doc()
    for fn in (s1, s2, s3, s4):
        sid = 'S' + fn.__name__[1:]
        if only and sid not in only: continue
        fn(d)
    if not only or 'S3' in only:
        card(d, 800, 'THEFT', 110, FR['S3'][1])    # drops in at f110 (3.67 s), lands by f115
    if captions:
        fonts = json.load(open(os.path.join(ROOT, '.tesseract-work', 'fonts.json')))
        fam = fonts.get('Nunito[wght]', ['Nunito ExtraLight', 'Regular'])[0]   # the variable font registers as 'Nunito ExtraLight' with a 'Black' instance
        for i, c in enumerate(CAPTIONS):
            caption(d, 900 + i, c['text'], c['highlight'], c['t0'], c['t1'], font=(fam, 'Black'))
    return d.acts
