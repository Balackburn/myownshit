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


def street(sh, z0=-400, n=7, far=True, colors=('#F2F0EA', '#B9A6D6', '#F2D06B', '#9EC7E8', '#F2B8C6', '#F2F0EA', '#C9E3B0')):
    """suburban street along Z: road x -1050..-150 with a dashed centre line; near sidewalk, fence and houses on +X;
    far sidewalk, fence and houses on -X (facing the road)"""
    sh.ground(SIDEWALK)
    sh.box((900, 4, 20000), (-600, -1, 0), ROAD, name='road', shadows=False)
    for i in range(40): sh.box((14, 5, 160), (-600, -2, -4000 + i * 400), '#F4F1E8', name='dash', shadows=False)
    sh.box((700, 4, 20000), (650, -1, 0), LAWN, name='lawns near', shadows=False)
    sh.box((700, 4, 20000), (-1850, -1, 0), LAWN, name='lawns far', shadows=False)
    for i in range(n):
        sh.model('house', (790, 0, z0 + i * 520), rot=(0, 90, 0), name=f'house near {i}')
        if far: sh.model('house', (-1990, 0, z0 + 260 + i * 520), rot=(0, -90, 0), name=f'house far {i}')
    for i in range(n * 2):
        sh.model('fence', (300, 0, z0 - 150 + i * 300), rot=(0, 90, 0), name=f'fence near {i}')
        if far: sh.model('fence', (-1500, 0, z0 - 150 + i * 300), rot=(0, 90, 0), name=f'fence far {i}')
    for i in range(4):
        sh.model('tree', (-1380, 0, z0 + 300 + i * 900), name=f'tree {i}')


def s1(d):
    f0, f1 = FR['S1']; sh = Shot(d, 101, 'S1 walk', f0, f1)
    street(sh)
    sh.sun(rx=-48, ry=-40, irradiance=3.4)
    man = sh.model('lemec', (40, 0, 0), rot=(0, 0, 0), clip='walk', clip_rate=1.0, name='man')
    sh.anim(man, 'position', [(0, [40, 0, 0]), (sh.nframes, [40, 0, -230])])
    sh.anim(man, 'rotationY', [(0, 0), (24, 0), (44, 40, 'inout'), (sh.nframes, 60)], 'float')
    dog = sh.model('dog', (-75, 0, -110), rot=(0, 0, 0), name='dog')
    sh.anim(dog, 'position', [(0, [-75, 0, -110]), (34, [-60, 0, -290]), (42, [-20, -110, -200], 'in'), (sh.nframes, [520, -620, 1500], 'in')])
    sh.model('tornado', (700, 0, 1900), scale=210, name='tornado')
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


CAPTIONS = SPEC['captions']


def build(only=None, captions=True):
    d = Doc()
    for fn in (s1, s3):
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
