#!/usr/bin/env python3
"""sand3d_models.py: find a ready-made 3D model for a shot in the sand3d datasets (Sandflow: about 100 000 objects, each written as a
short sand3d program, CC BY 4.0), build it into a GLB and use it in the absurd-shorts engine through the `glbModel` prop.

  find [--entry NAME | --like PART] [--family CATEGORY] [--sources objaverse] [--n 6] [--sheet out.jpg]
        by object name (entry 'key', like 'van', family 'vehicle'): the precise way; --sheet: a contact sheet of the renders to choose from
  search QUERY [--sources ...] [--n 6] [--sheet out.jpg]   full-text search over every column (the code too, so it is noisier)
  get SOURCE ROW [--out DIR]     the program, its metadata (licence, attribution) and its render; DIR defaults to
                                 absurd-shorts/assets/models/<entry>-<source>-<row>/
  build DIR [--glb FILE]         checks the program, builds it in the sand3d venv, exports DIR/model.glb (metres, Y up, front +Z)
  credits DIR...                 the attribution lines CC BY 4.0 asks for (put them in the video's description)
  install                        creates the sand3d venv (Python 3.13 + bpy 5.2) if it is missing

The programs are code downloaded from the internet: `build` accepts only `import sand3d as s3d` (and math), no file, system, eval or
dunder access, no private sand3d names, and runs the program in a separate isolated process with a time limit.
Venv: $SAND3D_VENV (default /root/.venvs/sand3d)."""
import argparse, ast, json, os, subprocess, sys, tempfile, time, urllib.parse, urllib.request

API = 'https://datasets-server.huggingface.co'
SOURCES = ['objaverse', 'cad', 'articraft', 'simready', 'automate']
VENV = os.environ.get('SAND3D_VENV', '/root/.venvs/sand3d')
VPY = os.path.join(VENV, 'bin', 'python')
MODELS = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'absurd-shorts', 'assets', 'models'))


def get_json(path, fatal=True, **q):   # the Hugging Face dataset viewer API has short outages (500, auth timeouts): retry with backoff
    url = f'{API}/{path}?' + urllib.parse.urlencode(q)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=60) as r: return json.loads(r.read())
        except Exception as e:
            if attempt == 4:
                if fatal: raise SystemExit(f'request failed: {url}\n{e}')
                print(f'   (skipped: {e})'); return {}
            time.sleep(2 + 4 * attempt)


def fetch(url, timeout=60):
    with urllib.request.urlopen(url, timeout=timeout) as r: return r.read()


def show(rows, sheet=None):
    for src, row, x in rows:
        print(f'{src:9s} {row:6d}  {x["family"] or "":14.14s} {x["entry"] or "":24.24s} f={x["f_score"] or 0:.2f} joints={x["n_joints"]} '
              f'{x["license_status"]} | {(x["attribution"] or "")[:80]}')
    if sheet and rows:
        import cv2, numpy as np
        tiles = []
        for src, row, x in rows:
            try: im = cv2.imdecode(np.frombuffer(fetch(x['render']['src']), np.uint8), cv2.IMREAD_COLOR); im = cv2.resize(im, (240, 240))
            except Exception: im = np.full((240, 240, 3), 200, np.uint8)
            cv2.rectangle(im, (0, 0), (240, 22), (255, 255, 255), -1); cv2.putText(im, f'{src} {row}', (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 200), 1)
            cv2.putText(im, (x['entry'] or '')[:26], (4, 234), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (20, 20, 20), 1); tiles.append(im)
        while len(tiles) % 6: tiles.append(np.full((240, 240, 3), 255, np.uint8))
        cv2.imwrite(sheet, np.vstack([np.hstack(tiles[i:i + 6]) for i in range(0, len(tiles), 6)])); print('sheet', sheet)


def search(a):   # full text over every column (the code too: "key" also finds keyboards); `find` is more precise
    rows = []
    for src in a.sources.split(','):
        d = get_json('search', fatal=False, dataset=f'Sandflow/sand3d-{src}', config='default', split='train', query=a.query, offset=0, length=a.n)
        print(f'== {src}: {d.get("num_rows_total", 0)} matches'); rows += [(src, r['row_idx'], r['row']) for r in d.get('rows', [])]
    show(rows, a.sheet)


def find(a):     # by object name: --entry exact ('key'), --like part of it ('van'), --family category ('vehicle'); one or two conditions
    q = lambda v: v.replace("'", "")
    cond = []
    if a.entry: cond.append('"entry" = ' + "'" + q(a.entry) + "'")
    if a.like: cond.append('"entry" LIKE ' + "'%" + q(a.like) + "%'")
    if a.family: cond.append('"family" = ' + "'" + q(a.family) + "'")
    if not cond: raise SystemExit('find: give --entry, --like or --family')
    rows = []
    for src in a.sources.split(','):
        d = get_json('filter', fatal=False, dataset=f'Sandflow/sand3d-{src}', config='default', split='train', where=' AND '.join(cond[:2]), offset=0, length=a.n)
        print(f'== {src}: {d.get("num_rows_total", 0)} matches'); rows += [(src, r['row_idx'], r['row']) for r in d.get('rows', [])]
    show(rows, a.sheet)


def get(a):
    d = get_json('rows', dataset=f'Sandflow/sand3d-{a.source}', config='default', split='train', offset=a.row, length=1)
    x = d['rows'][0]['row']
    out = a.out or os.path.join(MODELS, f'{x["entry"]}-{a.source}-{a.row}'); os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'program.py'), 'w').write(x['program'])
    meta = {k: v for k, v in x.items() if k not in ('program', 'render')}; meta.update(dataset=f'Sandflow/sand3d-{a.source}', row=a.row)
    json.dump(meta, open(os.path.join(out, 'meta.json'), 'w'), indent=1, ensure_ascii=False)
    try: open(os.path.join(out, 'render.png'), 'wb').write(fetch(x['render']['src']))
    except Exception as e: print('no render:', e)
    print(out); print('licence:', x['license'], '| source licence:', x['source_license'], '|', x['license_status']); print('credit:', x['attribution'])


BANNED_NAMES = {'eval', 'exec', 'compile', 'open', '__import__', 'globals', 'locals', 'vars', 'getattr', 'setattr', 'delattr', 'input',
                'breakpoint', 'exit', 'quit', 'help', 'memoryview', 'bpy', 'bmesh', 'os', 'sys', 'subprocess', 'importlib', 'builtins'}


def check(src):
    """reasons the program is refused (empty list: only sand3d and math calls)"""
    bad = []
    try: tree = ast.parse(src)
    except SyntaxError as e: return [f'syntax error: {e}']
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for al in n.names:
                if not ((al.name == 'sand3d' and al.asname == 's3d') or (al.name == 'math' and al.asname in (None, 'math'))): bad.append(f'import {al.name}')
        elif isinstance(n, ast.ImportFrom):
            if n.module != 'math': bad.append(f'from {n.module} import ...')
        elif isinstance(n, ast.Name) and n.id in BANNED_NAMES: bad.append(f'name {n.id}')
        elif isinstance(n, ast.Attribute) and (n.attr.startswith('__') or (isinstance(n.value, ast.Name) and n.value.id == 's3d' and n.attr.startswith('_'))): bad.append(f'attribute .{n.attr}')
        elif isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value.startswith('__') and n.value.endswith('__'): bad.append(f'string {n.value}')
    return sorted(set(bad))


RUNNER = '''import json, runpy, sys
import sand3d as s3d
prog, entry, out = sys.argv[1], sys.argv[2], sys.argv[3]
ns = runpy.run_path(prog, run_name="sand3d_program")
obj = ns[entry]()
s3d.export(obj, out)
print("built", out)
'''


def install(a=None):
    if os.path.exists(VPY): print('sand3d venv ready:', VENV); return
    uv = subprocess.run(['which', 'uv'], capture_output=True, text=True).stdout.strip()
    if uv: subprocess.run([uv, 'venv', '-q', '-p', '3.13', VENV], check=True); subprocess.run([uv, 'pip', 'install', '-q', '-p', VENV, 'sand3d'], check=True)
    else: subprocess.run(['python3.13', '-m', 'venv', VENV], check=True); subprocess.run([VPY, '-m', 'pip', 'install', '-q', 'sand3d'], check=True)
    print('installed sand3d in', VENV)


def build(a):
    meta = json.load(open(os.path.join(a.dir, 'meta.json'))); prog = os.path.abspath(os.path.join(a.dir, 'program.py'))
    bad = check(open(prog).read())
    if bad: raise SystemExit('refused (not a plain sand3d program): ' + ', '.join(bad))
    install()
    glb = os.path.abspath(a.glb or os.path.join(a.dir, 'model.glb'))
    with tempfile.TemporaryDirectory() as tmp:
        runner = os.path.join(tmp, 'run_sand3d.py'); open(runner, 'w').write(RUNNER)
        r = subprocess.run([VPY, '-I', runner, prog, meta['entry'], glb], cwd=tmp, capture_output=True, text=True, timeout=a.timeout)
    if r.returncode or not os.path.exists(glb): raise SystemExit('build failed:\n' + (r.stderr or r.stdout)[-2000:])
    print(f'{glb} ({os.path.getsize(glb) // 1024} KB)  ->  glbModel src: /assets/models/{os.path.relpath(glb, MODELS)}')


def credits(a):
    for d in a.dirs:
        m = json.load(open(os.path.join(d, 'meta.json')))
        print(f'{m["attribution"]} — sand3d program from {m.get("dataset", "Sandflow sand3d")} ({m["license"]})')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('search'); p.add_argument('query'); p.add_argument('--sources', default=','.join(SOURCES)); p.add_argument('--n', type=int, default=6); p.add_argument('--sheet'); p.set_defaults(f=search)
    p = sp.add_parser('find'); p.add_argument('--entry'); p.add_argument('--like'); p.add_argument('--family'); p.add_argument('--sources', default='objaverse'); p.add_argument('--n', type=int, default=6); p.add_argument('--sheet'); p.set_defaults(f=find)
    p = sp.add_parser('get'); p.add_argument('source', choices=SOURCES); p.add_argument('row', type=int); p.add_argument('--out'); p.set_defaults(f=get)
    p = sp.add_parser('build'); p.add_argument('dir'); p.add_argument('--glb'); p.add_argument('--timeout', type=int, default=300); p.set_defaults(f=build)
    p = sp.add_parser('credits'); p.add_argument('dirs', nargs='+'); p.set_defaults(f=credits)
    p = sp.add_parser('install'); p.set_defaults(f=install)
    a = ap.parse_args(); a.f(a)
