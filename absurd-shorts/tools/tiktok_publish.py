#!/usr/bin/env python3
"""Publish the finished stories to TikTok through the official Content Posting API (Direct Post), the step that follows each delivery.

What it does, in order:
  1. Inventory: the final render of every original story (hyperframes/NN-name/renders/*.mp4, the newest one per project; the replica and the
     remakes of other people's videos, projects 01-03, and duplicate renders are left out).
  2. Account check: the videos already on the account (Display API /v2/video/list/), matched to the stories by title, plus the local ledger
     (stories7/tiktok_published.json) of what this tool already sent.
  3. Publication of every story still missing, oldest first: creator info (privacy options, maximum length), init with FILE_UPLOAD, one PUT of
     the file to the upload URL, then the status polled until TikTok has the post. Each post carries the AI-generated label (is_aigc), the title
     and a few French hashtags. A pause between posts keeps to the API's rate limits; a daily cap error stops the run and the next run resumes.

Credentials: none in this file, in the repository or in the environment variables. The access token is a network secret of the cloud
environment for open.tiktokapis.com: the proxy puts it in the Authorization header of every request to that host, so this script sends a
placeholder. A TikTok access token lasts 24 hours.

Usage (from absurd-shorts/):
  python3 tools/tiktok_publish.py --list            inventory only, no network
  python3 tools/tiktok_publish.py --check           also ask TikTok what is on the account, publish nothing
  python3 tools/tiktok_publish.py                   publish everything missing (--max N: at most N posts this run; --only 61-ressort ...)
"""
import argparse, json, os, re, sys, time, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HF = ROOT / 'hyperframes'
LEDGER = ROOT / 'absurd-shorts' / 'stories7' / 'tiktok_published.json'
QUEUE = ROOT / 'absurd-shorts' / 'stories7' / 'queue10.sh'
API = 'https://open.tiktokapis.com'
HEADERS = {'Authorization': 'Bearer proxy-injected', 'Content-Type': 'application/json; charset=UTF-8'}   # the proxy replaces the placeholder
VERIFY = os.environ.get('REQUESTS_CA_BUNDLE') or '/root/.ccr/ca-bundle.crt'
SKIP = {'01-tornado-fr', '01-tornado-reverse', '02-vos-papiers', '03-potes-poissons', '35-ver-tesseract'}   # a replica, remakes of uploads, a duplicate
TAGS = '#humour #absurde #animation #dessinanimé #courtmétrage'


def norm(t):
    t = unicodedata.normalize('NFKD', t or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', t).strip()


def titles():
    """story key -> French title, from the TITLE table of the final render queue"""
    m = re.search(r'declare -A TITLE=\((.*?)\)\n', QUEUE.read_text(encoding='utf-8'), re.S)
    return dict(re.findall(r'\[(\w+)\]="([^"]*)"', m.group(1))) if m else {}


def inventory():
    tt, out = titles(), []
    for d in sorted(HF.iterdir()):
        if not d.is_dir() or d.name in SKIP or not re.match(r'^\d+-', d.name):
            continue
        rs = sorted((d / 'renders').glob('*.mp4'), key=lambda f: f.stat().st_mtime) if (d / 'renders').is_dir() else []
        if not rs:
            continue
        num, key = d.name.split('-', 1)
        out.append({'id': d.name, 'num': int(num), 'title': tt.get(key, key.replace('-', ' ').capitalize()), 'file': str(rs[-1]),
                    'size': rs[-1].stat().st_size})
    return sorted(out, key=lambda v: v['num'])


def ledger():
    return json.loads(LEDGER.read_text(encoding='utf-8')) if LEDGER.exists() else {}


def save_ledger(L):
    LEDGER.write_text(json.dumps(L, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


def call(path, body=None, params=None):
    import requests
    r = requests.post(API + path, headers=HEADERS, params=params, data=json.dumps(body or {}), verify=VERIFY, timeout=60)
    try:
        j = r.json()
    except ValueError:
        raise SystemExit(f'{path}: HTTP {r.status_code}, not JSON: {r.text[:200]}')
    err = (j.get('error') or {})
    if r.status_code >= 400 or err.get('code') not in (None, 'ok'):
        return None, f"HTTP {r.status_code} {err.get('code')}: {err.get('message')}"
    return j.get('data') or {}, None


def account_titles():
    """the titles and descriptions of the videos on the account (video.list scope), normalised"""
    seen, cursor = [], None
    for _ in range(50):
        body = {'max_count': 20, **({'cursor': cursor} if cursor else {})}
        data, err = call('/v2/video/list/', body, params={'fields': 'id,title,video_description,create_time'})
        if err:
            raise SystemExit(f'could not list the account videos: {err}')
        for v in data.get('videos', []):
            seen.append(norm((v.get('title') or '') + ' ' + (v.get('video_description') or '')))
        if not data.get('has_more'):
            break
        cursor = data.get('cursor')
    return seen


def on_account(v, seen):
    t = norm(v['title'])
    return any(s.startswith(t + ' ') or s == t for s in seen)


def publish(v, info):
    import requests
    opts = info.get('privacy_level_options') or ['SELF_ONLY']
    privacy = 'PUBLIC_TO_EVERYONE' if 'PUBLIC_TO_EVERYONE' in opts else opts[0]
    size = v['size']
    post = {'title': f"{v['title']} {TAGS}", 'privacy_level': privacy, 'disable_duet': bool(info.get('duet_disabled')),
            'disable_comment': bool(info.get('comment_disabled')), 'disable_stitch': bool(info.get('stitch_disabled')),
            'video_cover_timestamp_ms': 1500, 'is_aigc': True}   # the AI-generated label: synthetic voice and animation made by code
    data, err = call('/v2/post/publish/video/init/', {'post_info': post, 'source_info': {'source': 'FILE_UPLOAD', 'video_size': size,
                                                                                         'chunk_size': size, 'total_chunk_count': 1}})
    if err:
        return None, privacy, err
    with open(v['file'], 'rb') as f:
        r = requests.put(data['upload_url'], data=f.read(), headers={'Content-Type': 'video/mp4', 'Content-Range': f'bytes 0-{size - 1}/{size}'},
                         verify=VERIFY, timeout=600)
    if r.status_code not in (200, 201):
        return data.get('publish_id'), privacy, f'upload HTTP {r.status_code}: {r.text[:200]}'
    pid = data.get('publish_id')
    for _ in range(60):
        time.sleep(5)
        st, err = call('/v2/post/publish/status/fetch/', {'publish_id': pid})
        if err:
            return pid, privacy, err
        s = st.get('status')
        if s == 'PUBLISH_COMPLETE':
            return pid, privacy, None
        if s == 'FAILED':
            return pid, privacy, f"failed: {st.get('fail_reason')}"
    return pid, privacy, 'still processing after 5 min (the ledger keeps the publish id)'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', action='store_true', help='inventory only, no network')
    ap.add_argument('--check', action='store_true', help='compare with the account, publish nothing')
    ap.add_argument('--max', type=int, default=0, help='at most N posts this run (0: all)')
    ap.add_argument('--only', nargs='*', help='project ids to consider (e.g. 61-ressort)')
    ap.add_argument('--pause', type=float, default=75.0, help='seconds between posts')
    a = ap.parse_args()
    vids, L = inventory(), ledger()
    if a.only:
        vids = [v for v in vids if v['id'] in a.only]
    print(f'{len(vids)} finished stories in hyperframes/ ({len(L)} already sent by this tool)')
    if a.list:
        for v in vids:
            print(f"  {v['id']:<22} {v['title']:<28} {v['size'] / 1e6:5.1f} MB  {'sent' if v['id'] in L else ''}")
        return
    seen = account_titles()
    missing = [v for v in vids if v['id'] not in L and not on_account(v, seen)]
    print(f'{len(seen)} videos on the account; {len(missing)} stories missing from it')
    for v in missing:
        print(f"  missing: {v['id']} « {v['title']} »")
    if a.check or not missing:
        return
    info, err = call('/v2/post/publish/creator_info/query/')
    if err:
        raise SystemExit(f'creator info: {err}')
    print(f"posting as {info.get('creator_username')}, privacy options {info.get('privacy_level_options')}, max {info.get('max_video_post_duration_sec')} s")
    done = 0
    for v in missing:
        if a.max and done >= a.max:
            break
        pid, privacy, err = publish(v, info)
        if err:
            print(f"  FAILED {v['id']}: {err}")
            if 'spam_risk' in err or 'rate_limit' in err or 'too_many' in err:
                print('  daily or rate cap reached: stopping; the next run resumes here')
                break
            continue
        L[v['id']] = {'title': v['title'], 'publish_id': pid, 'privacy': privacy, 'at': time.strftime('%Y-%m-%d %H:%M')}
        save_ledger(L)
        done += 1
        print(f"  posted {v['id']} « {v['title']} » ({privacy})")
        if v is not missing[-1]:
            time.sleep(a.pause)
    print(f'{done} posted this run')


if __name__ == '__main__':
    main()
