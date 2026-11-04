"""shots.py — the replica, shot by shot (frames from analysis/shots.json). Edit, rebuild with build.py, compare, repeat."""
import json, os
from tsx import Doc, Shot, caption, ms, lin, ext, euler, FPS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = json.load(open(os.path.join(ROOT, 'analysis', 'shots.json')))
FR = {s['id']: s['frames'] for s in SPEC['shots']}

SKY = '#A9CFE3'
SIDEWALK = '#E4D6BE'
ROAD = '#6E6E72'
LAWN = '#8CC063'


def street(sh, x_houses=430, z0=-400, n=7, colors=('#F2F0EA', '#B9A6D6', '#F2D06B', '#9EC7E8', '#F2B8C6', '#F2F0EA', '#C9E3B0')):
    """the suburban street: sidewalk ground, road strip, lawn strip, a row of houses facing the street (-X), a fence, trees"""
    sh.ground(SIDEWALK)
    sh.box((900, 4, 20000), (-600, -1, 0), ROAD, name='road', shadows=False)
    sh.box((700, 4, 20000), (650, -1, 0), LAWN, name='lawns', shadows=False)
    for i in range(n):
        sh.model('house', (x_houses + 120, 0, z0 + i * 520), rot=(0, 90, 0), scale=100, name=f'house {i}')
    for i in range(n * 2):
        sh.model('fence', (300, 0, z0 - 150 + i * 300), rot=(0, 90, 0), name=f'fence {i}')
    for i in range(4):
        sh.model('tree', (-1150, 0, z0 + 300 + i * 900), name=f'tree {i}')


def s1(d):
    f0, f1 = FR['S1']; sh = Shot(d, 101, 'S1 walk', f0, f1)
    street(sh)
    sh.sun(rx=-48, ry=-40, irradiance=3.4)
    man = sh.model('lemec', (40, 0, 0), rot=(0, 0, 0), clip='walk', clip_rate=1.0, name='man')
    sh.anim(man, 'position', [(0, [40, 0, 0]), (sh.nframes, [40, 0, -260])])
    dog = sh.model('dog', (-70, 0, -150), rot=(0, 0, 0), name='dog')
    sh.anim(dog, 'position', [(0, [-70, 0, -150]), (30, [-60, 0, -330]), (40, [-40, -120, -100], 'in'), (sh.nframes, [600, -700, 1800], 'in')])
    sh.model('tornado', (900, 0, 2600), scale=170, name='tornado')
    sh.camera((-40, -90, -520), (40, -125, 0), fov=44,
              keys=[(0, [-40, -90, -520]), (12, [-40, -90, -600]), (24, [-420, -110, -420], 'inout'), (sh.nframes, [-520, -120, -560])],
              tkeys=[(0, [40, -125, 0]), (12, [40, -125, -60]), (24, [80, -150, 200], 'inout'), (sh.nframes, [500, -300, 1500])])


def s3(d):
    f0, f1 = FR['S3']; sh = Shot(d, 103, 'S3 theft', f0, f1)
    street(sh, z0=-1200)
    sh.sun(rx=-48, ry=-40, irradiance=3.4)
    sh.model('lemec', (0, 0, 0), rot=(0, 15, 0), clip='shrug', clip_rate=0.6, name='man')
    sh.camera((-60, -95, -330), (0, -170, 0), fov=46)


CAPTIONS = SPEC['captions']


def build(only=None, captions=True):
    d = Doc()
    for fn in (s1, s3):
        sid = 'S' + fn.__name__[1:]
        if only and sid not in only: continue
        fn(d)
    if captions:
        fonts = json.load(open(os.path.join(ROOT, '.tesseract-work', 'fonts.json')))
        fam = fonts.get('Nunito[wght]', ['Nunito ExtraLight', 'Regular'])[0]   # the variable font registers as 'Nunito ExtraLight' with a 'Black' instance
        for i, c in enumerate(CAPTIONS):
            caption(d, 900 + i, c['text'], c['highlight'], c['t0'], c['t1'], font=(fam, 'Black'))
    return d.acts
