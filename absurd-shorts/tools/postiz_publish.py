#!/usr/bin/env python3
"""Publish the finished stories to TikTok through Postiz (the `postiz` command-line tool, npm package `postiz`, skill .claude/skills/postiz), the
step that follows each delivery.

What it does:
  1. Inventory: the final render of every original story (tools/tiktok_publish.py: hyperframes/NN-name/renders, newest render per project; the
     replica, the remakes of other people's videos and duplicate renders are left out), oldest first.
  2. Ledger: stories7/tiktok_published.json (shared with the other publishers) says what was already scheduled or published; a story is never sent
     twice.
  3. For each story to send: `postiz upload` of the mp4, then `postiz posts:create` on the TikTok channel with DIRECT_POST (it is published, not left
     as a draft in the app), without the AI-generated label (the owner's decision: the pictures are a 3D render made by code, not a generated
     video), the title, and a caption made of the title, the
     story's first line of narration and five French hashtags. Videos are 1080x1920 H.264 mp4 already, so no re-encoding.

Credentials: the Postiz API key is read from the environment variable POSTIZ_API_KEY and never written to a file, a commit or a log. Node reaches
the API through the session's proxy (NODE_USE_ENV_PROXY=1, set here).

Usage (from absurd-shorts/):
  python3 tools/postiz_publish.py --check                  list what is missing, send nothing
  python3 tools/postiz_publish.py --now 1                  publish the oldest missing story in two minutes
  python3 tools/postiz_publish.py --schedule               schedule every missing story, six a day (9:00 to 21:30 Paris time)
  python3 tools/postiz_publish.py --only 75-parcmetre --now 1    a new delivery, right away
  python3 tools/postiz_publish.py --only 75-parcmetre --now 1 --inbox    the same, to the TikTok app's inbox (published from the app)
  python3 tools/postiz_publish.py --status                 refresh the ledger from Postiz (published, error)
  python3 tools/postiz_publish.py --cancel-scheduled       delete every post still waiting in the Postiz queue and mark those stories as already on
                                                           the account (posted by hand), so they are never sent again

New deliveries go out right away (no daily slots): after each final, `--only NN-name --now 1`; `--now N` sends every finished story the ledger does not
know yet, a few minutes apart.
"""
import argparse, datetime as dt, json, os, re, subprocess, sys
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tiktok_publish import inventory, ledger, save_ledger   # noqa: E402  (the shared inventory and ledger)

ROOT = Path(__file__).resolve().parent.parent                 # absurd-shorts/
TAGS = '#humour #absurde #animation #dessinanimé #courtmétrage'
SLOTS = [(9, 0), (11, 30), (14, 0), (16, 30), (19, 0), (21, 30)]   # Paris time: six a day, under TikTok's daily cap on posts sent through its API
PARIS = ZoneInfo('Europe/Paris')


def run(args, timeout=900):
    if not os.environ.get('POSTIZ_API_KEY'):
        sys.exit('POSTIZ_API_KEY is not set in the environment')
    env = {**os.environ, 'NODE_USE_ENV_PROXY': '1', 'NODE_NO_WARNINGS': '1'}
    r = subprocess.run(['postiz', *args], capture_output=True, text=True, timeout=timeout, env=env)
    out = (r.stdout or '') + (r.stderr or '')
    if r.returncode:
        raise RuntimeError(f"postiz {args[0]} failed ({r.returncode}): {out.strip()[-600:]}")
    return out


def last_json(text):
    """The last JSON object or array printed by the CLI (it prints a banner line first)."""
    for start in [m.start() for m in re.finditer(r'[\[{]', text)]:
        try:
            return json.loads(text[start:])
        except ValueError:
            continue
    return None


def hook(story_id):
    name = story_id.split('-', 1)[1] if '-' in story_id else story_id
    f = ROOT / 'stories7' / name / 'lines.json'
    try:
        return json.load(open(f))[0]['text'].strip()
    except (OSError, ValueError, KeyError, IndexError):
        return ''


def integration():
    lst = last_json(run(['integrations:list'], 120)) or []
    tik = [i for i in lst if str(i.get('identifier', '')).startswith('tiktok') and not i.get('disabled')]
    if not tik:
        sys.exit('no TikTok channel connected in Postiz')
    return tik[0]['id']


def slots_after(start, taken, n):
    """n schedule times (UTC, ISO) from the daily Paris slots after `start`, skipping the ones already taken."""
    out, day = [], start.astimezone(PARIS).date()
    while len(out) < n:
        for h, m in SLOTS:
            t = dt.datetime(day.year, day.month, day.day, h, m, tzinfo=PARIS)
            iso = t.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            if t > start + dt.timedelta(minutes=20) and iso not in taken and len(out) < n:
                out.append(iso)
        day += dt.timedelta(days=1)
    return out


def send(v, when, chan, inbox=False):
    up = last_json(run(['upload', v['file']], 1800)) or {}
    path = up.get('path')
    if not path:
        raise RuntimeError(f"upload of {v['file']} returned no path")
    h = hook(v['id'])
    content = f"<p>{v['title']}{' — ' + h if h else ''}</p><p>{TAGS}</p>"
    settings = {'title': v['title'][:90], 'privacy_level': 'PUBLIC_TO_EVERYONE', 'duet': True, 'stitch': True, 'comment': True, 'autoAddMusic': 'no',
                'brand_content_toggle': False, 'brand_organic_toggle': False, 'video_made_with_ai': False, 'content_posting_method': 'DIRECT_POST'}
    if inbox:   # (15 Nov) --inbox: TikTok's inbox instead of the profile; the owner publishes it from the app (where the high-quality upload setting
        settings = {**settings, 'content_posting_method': 'UPLOAD'}   # applies); Postiz still validates every field, TikTok's inbox keeps the title
    res = last_json(run(['posts:create', '-c', content, '-m', path, '-i', chan, '-s', when, '--settings', json.dumps(settings, ensure_ascii=False)], 300))
    items = res if isinstance(res, list) else (res.get('posts') or res.get('data') or [res]) if isinstance(res, dict) else []
    pid = next((it.get('postId') or it.get('id') for it in items if isinstance(it, dict) and (it.get('postId') or it.get('id'))), None)
    return pid, path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--status', action='store_true')
    ap.add_argument('--now', type=int, default=0, help='publish this many missing stories two minutes from now, a few minutes apart')
    ap.add_argument('--schedule', action='store_true', help='schedule all the remaining missing stories on the daily slots')
    ap.add_argument('--max', type=int, default=0)
    ap.add_argument('--only', nargs='*')
    ap.add_argument('--cancel-scheduled', action='store_true', help='delete the posts still queued in Postiz; mark their stories as already on the account')
    ap.add_argument('--inbox', action='store_true', help="send to the TikTok app's inbox (the owner publishes from the app) instead of publishing")
    a = ap.parse_args()
    L = ledger()
    vids = [v for v in inventory() if not a.only or v['id'] in a.only]
    missing = [v for v in vids if v['id'] not in L]
    print(f"{len(vids)} finished stories, {len(missing)} not yet sent")
    if a.check:
        for v in missing:
            print(f"  missing: {v['id']} « {v['title']} »")
        return
    if a.status:
        posts = last_json(run(['posts:list'], 120)) or []
        posts = posts if isinstance(posts, list) else posts.get('posts', [])
        byid = {p.get('id'): p for p in posts if isinstance(p, dict)}
        for sid, e in L.items():
            p = byid.get(e.get('post_id'))
            if p and e.get('via') == 'postiz':
                e['status'] = str(p.get('state') or p.get('status') or e.get('status')).lower()
                if p.get('releaseURL'):
                    e['url'] = p['releaseURL']
                print(f"  {sid}: {e['status']} {e.get('url', '')}")
        save_ledger(L)
        return
    if a.cancel_scheduled:
        posts = last_json(run(['posts:list'], 120)) or []
        posts = posts if isinstance(posts, list) else posts.get('posts', [])
        state = {p.get('id'): str(p.get('state') or p.get('status') or '').upper() for p in posts if isinstance(p, dict)}
        for sid, e in L.items():
            pid = e.get('post_id')
            if e.get('via') != 'postiz' or not pid or state.get(pid) == 'PUBLISHED':
                continue
            try:
                run(['posts:delete', pid], 120)
            except (RuntimeError, subprocess.TimeoutExpired) as err:
                print(f"  FAILED to cancel {sid}: {err}")
                continue
            L[sid] = {**e, 'via': 'manual', 'status': 'already on the account (scheduled post cancelled)', 'cancelled': dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M')}
            save_ledger(L)
            print(f"  cancelled {sid} (post {pid})")
        return
    chan = integration()
    todo = missing[:a.max] if a.max else missing
    now = dt.datetime.now(dt.timezone.utc)
    taken = {e.get('date') for e in L.values() if e.get('via') == 'postiz'}
    plan = []
    if a.now:
        plan += [(v, (now + dt.timedelta(minutes=2 + 5 * i)).strftime('%Y-%m-%dT%H:%M:%SZ')) for i, v in enumerate(todo[:a.now])]
        todo = todo[a.now:]
    if a.schedule:
        last = max([dt.datetime.fromisoformat(d.replace('Z', '+00:00')) for d in taken if d] + [now])
        plan += list(zip(todo, slots_after(last, taken, len(todo))))
    for v, when in plan:
        try:
            pid, path = send(v, when, chan, inbox=a.inbox)
        except (RuntimeError, subprocess.TimeoutExpired) as e:
            print(f"  FAILED {v['id']}: {e}")
            break
        L[v['id']] = {'title': v['title'], 'via': 'postiz', 'post_id': pid, 'status': 'sent to the TikTok inbox' if a.inbox else 'scheduled', 'date': when, 'media': path,
                      'at': dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M')}
        save_ledger(L)
        print(f"  scheduled {v['id']} « {v['title']} » for {when} (post {pid})")


if __name__ == '__main__':
    main()
