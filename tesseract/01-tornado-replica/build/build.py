#!/usr/bin/env python3
"""build.py — rebuild Replica.tsrct from assets + shots.py (deterministic; the .tsrct is the editable deliverable).

usage: python3 build/build.py [--only S1,S3] [--no-captions] [--out Replica.tsrct]
1. base.tsrct (cached in .tesseract-work/): empty 576x1024, 28.8 s document with every model and font imported
2. actions from shots.py -> .tesseract-work/actions.json -> tsrct project apply (atomic)
"""
import argparse, glob, json, os, subprocess, sys, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'build'))
T = os.path.expanduser('~/.local/share/Tesseract/bin/tsrct')
ENV = dict(os.environ, TESSERACT_CALLER='agent-skill', TESSERACT_SKILL='tesseract-3d', TESSERACT_HOST='claude', TESSERACT_DISTRIBUTION='standalone-skill')
W = os.path.join(ROOT, '.tesseract-work')


def tsrct(*args, capture=True):
    r = subprocess.run([T, *args], capture_output=capture, text=True, env=ENV)
    if r.returncode != 0: raise SystemExit(f"tsrct {' '.join(args[:3])} failed:\n{(r.stderr or '')[:3000]}")
    return r.stdout


def base_doc():
    """empty canvas + all assets; rebuilt when an asset file is newer than the cache"""
    base = os.path.join(W, 'base.tsrct'); assets = sorted(glob.glob(os.path.join(ROOT, 'assets/models/*.glb'))) + sorted(glob.glob(os.path.join(ROOT, 'assets/fonts/*.ttf')))
    if os.path.exists(base) and all(os.path.getmtime(a) < os.path.getmtime(base) for a in assets): return base
    if os.path.exists(base): os.remove(base)
    tsrct('project', 'create', '--project', base)
    ed = os.path.join(W, 'base_editable.json'); tsrct('project', 'checkout', '--project', base, '--output', ed)
    d = json.load(open(ed)); d['dimensions'] = {'width': 576, 'height': 1024}; d['duration'] = 28.8
    d['colorManagement'] = d.get('colorManagement', {'workingSpace': 'legacyDisplay'}); json.dump(d, open(ed, 'w')); tsrct('project', 'commit', '--project', base, '--file', ed)
    fonts = {}
    for a in assets:
        name = os.path.splitext(os.path.basename(a))[0]
        if a.endswith('.glb'):
            out = tsrct('project', 'import-asset', '--project', base, '--file', a, '--asset-id', name, '--kind', 'model3d')
            open(os.path.join(W, f'import_{name}.json'), 'w').write(out)
        else:
            out = json.loads(tsrct('project', 'import-font', '--project', base, '--file', a)); fonts[name] = [out['fontFamily'], out['fontStyle']]
    json.dump(fonts, open(os.path.join(W, 'fonts.json'), 'w'), indent=1); print('base rebuilt:', len(assets), 'assets')
    return base


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--only'); ap.add_argument('--no-captions', action='store_true'); ap.add_argument('--out', default=os.path.join(ROOT, 'Replica.tsrct'))
    a = ap.parse_args(); os.makedirs(W, exist_ok=True)
    base = base_doc()
    import shots
    acts = shots.build(only=set(a.only.split(',')) if a.only else None, captions=not a.no_captions)
    json.dump(acts, open(os.path.join(W, 'actions.json'), 'w'))
    tmp = a.out + '.tmp.tsrct'; shutil.copy(base, tmp)
    rep = json.loads(tsrct('project', 'apply', '--project', tmp, '--actions', os.path.join(W, 'actions.json')))
    if rep.get('warnings'): print('warnings:', json.dumps(rep['warnings'])[:2000])
    os.replace(tmp, a.out); print(f"built {a.out}: {rep.get('appliedActions')} actions")


if __name__ == '__main__': main()
