#!/usr/bin/env python3
"""sand3d_models.py: find a ready-made 3D model for a shot in the sand3d datasets (Sandflow: about 100 000 objects, each written as a
short sand3d program, CC BY 4.0), build it into a GLB and use it in the absurd-shorts engine through the `glbModel` prop.

  find [--entry NAME | --like PART] [--family CATEGORY] [--sources objaverse] [--n 6] [--sheet out.jpg] [--local]
        by object name (entry 'key', like 'van', family 'vehicle'): the precise way; --sheet: a contact sheet of the renders to choose from
  search QUERY [--sources ...] [--n 6] [--sheet out.jpg]   full-text search over every column (the code too, so it is noisier)
  get SOURCE ROW [--out DIR]     the program, its metadata (licence, attribution) and its render; DIR defaults to
                                 absurd-shorts/assets/models/<entry>-<source>-<row>/
  build DIR [--glb FILE]         checks the program, builds it in the sand3d venv, exports DIR/model.glb (metres, Y up, front +Z)
  credits DIR...                 the attribution lines CC BY 4.0 asks for (put them in the video's description)
  index [--sources ...]          a local index of names, categories, scores and licences, read from the datasets' Parquet files
                                 (about 80 s for objaverse); find, search and get fall back on it when the dataset viewer API fails
  install                        creates the sand3d venv (Python 3.13 + bpy 5.2, plus pyarrow, fsspec, pillow) if it is missing

The programs are code downloaded from the internet: `build` accepts only `import sand3d as s3d` (and math), no file, system, eval or
dunder access, no private sand3d names, and runs the program in a separate isolated process with a time limit.
Venv: $SAND3D_VENV (default /root/.venvs/sand3d); local index: $SAND3D_INDEX (default ~/.cache/sand3d_index)."""
import argparse, ast, io, json, os, subprocess, sys, tempfile, time, urllib.parse, urllib.request

API = 'https://datasets-server.huggingface.co'
HUB = 'https://huggingface.co/api/datasets'
SOURCES = ['objaverse', 'cad', 'articraft', 'simready', 'automate']
VENV = os.environ.get('SAND3D_VENV', '/root/.venvs/sand3d')
VPY = os.path.join(VENV, 'bin', 'python')
INDEX = os.environ.get('SAND3D_INDEX', os.path.join(os.path.expanduser('~'), '.cache', 'sand3d_index'))
MODELS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'absurd-shorts', 'assets', 'models'))
META = ['id', 'family', 'entry', 'f_score', 'n_joints', 'license_status', 'license', 'source_license', 'attribution']


def get_json(path, fatal=True, **q):   # the Hugging Face dataset viewer API has outages (500/502/504, auth timeouts): retry with backoff
    url = f'{API}/{path}?' + urllib.parse.urlencode(q)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r: return json.loads(r.read())
        except Exception as e:
            if attempt == 3:
                if fatal: raise SystemExit(f'request failed: {url}\n{e}')
                print(f'   (dataset viewer API unavailable: {e})'); return None
            time.sleep(2 + 4 * attempt)


def fetch(url, timeout=60):
    with urllib.request.urlopen(url, timeout=timeout) as r: return r.read()


# ---- the Parquet path (needs pyarrow + fsspec: the command re-runs itself in the sand3d venv)
def have_pyarrow():
    try: import pyarrow, fsspec, aiohttp; return True
    except ImportError: return False


def need_pyarrow():
    if have_pyarrow(): return
    install(); os.execv(VPY, [VPY, os.path.abspath(__file__)] + sys.argv[1:])


def shards(src): return json.loads(fetch(f'{HUB}/Sandflow/sand3d-{src}/parquet/default/train'))


def pfile(url):
    import fsspec, pyarrow.parquet as pq
    return pq.ParquetFile(fsspec.filesystem('https', client_kwargs={'trust_env': True}).open(url, 'rb', block_size=2 ** 20))


def parquet_row(src, row, columns):   # one row's columns, located through the local index (shard, row in shard)
    d = local(src); x = d['rows'][row]; f = pfile(d['shards'][x['shard']]); r, g = x['r'], 0
    while r >= f.metadata.row_group(g).num_rows: r -= f.metadata.row_group(g).num_rows; g += 1
    return f.read_row_group(g, columns=columns).slice(r, 1).to_pylist()[0]


def local(src):
    p = os.path.join(INDEX, f'{src}.json')
    return json.load(open(p)) if os.path.exists(p) else None


def index(a):
    need_pyarrow(); os.makedirs(INDEX, exist_ok=True)
    for src in a.sources.split(','):
        urls, rows = shards(src), []
        for si, url in enumerate(urls):
            t = pfile(url).read(columns=META).to_pylist(); rows += [{**x, 'row': len(rows) + i, 'shard': si, 'r': i} for i, x in enumerate(t)]
            print(f'{src}: shard {si + 1}/{len(urls)}, {len(rows)} rows', flush=True)
        json.dump({'shards': urls, 'rows': rows}, open(os.path.join(INDEX, f'{src}.json'), 'w')); print(f'{src}: {len(rows)} rows indexed in {INDEX}')


# ---- search
def render_of(src, row, x):
    if (x.get('render') or {}).get('src'): return fetch(x['render']['src'])
    if local(src) and have_pyarrow(): return (parquet_row(src, row, ['render'])['render'] or {}).get('bytes')
    return None


def show(rows, sheet=None):
    for src, row, x in rows:
        print(f'{src:9s} {row:6d}  {x["family"] or "":14.14s} {x["entry"] or "":24.24s} f={x["f_score"] or 0:.2f} joints={x["n_joints"]} '
              f'{x["license_status"]} | {(x["attribution"] or "")[:80]}')
    if not (sheet and rows): return
    from PIL import Image, ImageDraw
    S, cols = 240, 6; n = (len(rows) + cols - 1) // cols; im = Image.new('RGB', (S * cols, S * n), 'white'); dr = ImageDraw.Draw(im)
    for i, (src, row, x) in enumerate(rows):
        try: tile = Image.open(io.BytesIO(render_of(src, row, x))).convert('RGB').resize((S, S))
        except Exception: tile = Image.new('RGB', (S, S), (200, 200, 200))
        X, Y = (i % cols) * S, (i // cols) * S; im.paste(tile, (X, Y))
        dr.rectangle([X, Y, X + S, Y + 18], fill='white'); dr.text((X + 4, Y + 3), f'{src} {row}', fill=(200, 0, 0)); dr.text((X + 4, Y + S - 14), (x['entry'] or '')[:30], fill=(20, 20, 20))
    im.save(sheet, quality=90); print('sheet', sheet)


def local_match(a, src, pred):
    d = local(src)
    if not d: return None
    out = sorted((x for x in d['rows'] if pred(x)), key=lambda x: -(x['f_score'] or 0))
    print(f'== {src}: {len(out)} matches (local index)'); return [(src, x['row'], x) for x in out[:a.n]]


def search(a):   # full text over every column (the code too: "key" also finds keyboards); `find` is more precise
    rows, q = [], a.query.lower()
    for src in a.sources.split(','):
        d = get_json('search', fatal=False, dataset=f'Sandflow/sand3d-{src}', config='default', split='train', query=a.query, offset=0, length=a.n)
        if d is not None: print(f'== {src}: {d.get("num_rows_total", 0)} matches'); rows += [(src, r['row_idx'], r['row']) for r in d.get('rows', [])]
        else: rows += local_match(a, src, lambda x: any(q in str(x.get(k) or '').lower() for k in ('entry', 'family', 'attribution'))) or []
    if a.sheet and rows and any(not x.get('render') for _, _, x in rows): need_pyarrow()
    show(rows, a.sheet)


def find(a):     # by object name: --entry exact ('key'), --like part of it ('van'), --family category ('vehicle'); one or two conditions
    q = lambda v: v.replace("'", "")
    cond = []
    if a.entry: cond.append('"entry" = ' + "'" + q(a.entry) + "'")
    if a.like: cond.append('"entry" LIKE ' + "'%" + q(a.like) + "%'")
    if a.family: cond.append('"family" = ' + "'" + q(a.family) + "'")
    if not cond: raise SystemExit('find: give --entry, --like or --family')
    pred = lambda x: (not a.entry or x['entry'] == a.entry) and (not a.like or a.like in (x['entry'] or '')) and (not a.family or x['family'] == a.family)
    rows = []
    for src in a.sources.split(','):
        d = None if a.local else get_json('filter', fatal=False, dataset=f'Sandflow/sand3d-{src}', config='default', split='train', where=' AND '.join(cond[:2]), offset=0, length=a.n)
        if d is not None: print(f'== {src}: {d.get("num_rows_total", 0)} matches'); rows += [(src, r['row_idx'], r['row']) for r in d.get('rows', [])]
        else:
            m = local_match(a, src, pred)
            if m is None: print(f'   no local index for {src}: run `index --sources {src}` once, then search again')
            rows += m or []
    if a.sheet and rows and any(not x.get('render') for _, _, x in rows): need_pyarrow()
    show(rows, a.sheet)


def get(a):
    d = get_json('rows', fatal=False, dataset=f'Sandflow/sand3d-{a.source}', config='default', split='train', offset=a.row, length=1)
    if d is not None: x = d['rows'][0]['row']; img = None
    else:
        if not local(a.source): raise SystemExit(f'the dataset viewer API is down and there is no local index: run `index --sources {a.source}` first')
        need_pyarrow(); x = parquet_row(a.source, a.row, META + ['program', 'render']); img = (x.pop('render') or {}).get('bytes')
    out = a.out or os.path.join(MODELS, f'{x["entry"]}-{a.source}-{a.row}'); os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'program.py'), 'w').write(x['program'])
    meta = {k: v for k, v in x.items() if k not in ('program', 'render')}; meta.update(dataset=f'Sandflow/sand3d-{a.source}', row=a.row)
    json.dump(meta, open(os.path.join(out, 'meta.json'), 'w'), indent=1, ensure_ascii=False)
    try: open(os.path.join(out, 'render.png'), 'wb').write(img or fetch(x['render']['src']))
    except Exception as e: print('no render:', e)
    print(out); print('licence:', x['license'], '| source licence:', x['source_license'], '|', x['license_status']); print('credit:', x['attribution'])


# ---- build
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
    if os.path.exists(VPY):
        if a is not None: print('sand3d venv ready:', VENV)
        return
    pkgs = ['sand3d', 'pyarrow', 'fsspec', 'aiohttp', 'pillow']
    uv = subprocess.run(['which', 'uv'], capture_output=True, text=True).stdout.strip()
    if uv: subprocess.run([uv, 'venv', '-q', '-p', '3.13', VENV], check=True); subprocess.run([uv, 'pip', 'install', '-q', '-p', VENV] + pkgs, check=True)
    else: subprocess.run(['python3.13', '-m', 'venv', VENV], check=True); subprocess.run([VPY, '-m', 'pip', 'install', '-q'] + pkgs, check=True)
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
    p = sp.add_parser('find'); p.add_argument('--entry'); p.add_argument('--like'); p.add_argument('--family'); p.add_argument('--sources', default='objaverse'); p.add_argument('--n', type=int, default=6); p.add_argument('--sheet'); p.add_argument('--local', action='store_true', help='use the local index only'); p.set_defaults(f=find)
    p = sp.add_parser('search'); p.add_argument('query'); p.add_argument('--sources', default=','.join(SOURCES)); p.add_argument('--n', type=int, default=6); p.add_argument('--sheet'); p.set_defaults(f=search)
    p = sp.add_parser('get'); p.add_argument('source', choices=SOURCES); p.add_argument('row', type=int); p.add_argument('--out'); p.set_defaults(f=get)
    p = sp.add_parser('build'); p.add_argument('dir'); p.add_argument('--glb'); p.add_argument('--timeout', type=int, default=300); p.set_defaults(f=build)
    p = sp.add_parser('credits'); p.add_argument('dirs', nargs='+'); p.set_defaults(f=credits)
    p = sp.add_parser('index'); p.add_argument('--sources', default='objaverse'); p.set_defaults(f=index)
    p = sp.add_parser('install'); p.set_defaults(f=install)
    a = ap.parse_args(); a.f(a)
