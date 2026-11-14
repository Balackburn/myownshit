#!/usr/bin/env python3
"""Publish the finished stories to TikTok through PostOnce's hosted MCP server (https://postonce.to/mcp, github.com/postoncehq/tiktok-mcp),
the step that follows each delivery. It speaks MCP (Streamable HTTP, JSON-RPC) directly, so it runs from any session without a restart.

What it does, in order:
  1. Inventory: the final render of every original story (the same list as tools/tiktok_publish.py: hyperframes/NN-name/renders, newest
     render per project; the replica, the remakes of other people's videos and duplicate renders are left out).
  2. Account check: the TikTok account connected to PostOnce (list_accounts), the posts PostOnce already holds (list_posts) and the local
     ledger stories7/tiktok_published.json; a story counts as present when one of them carries its title.
  3. For each missing story, oldest first: create_upload_url, one PUT of the file to the signed URL (a short-lived credential: never printed),
     get_media for the public URL, create_post to the TikTok account with the title and up to five French hashtags, the AI-generated label
     and public privacy, then get_post until it is published or failed. An idempotency key per story keeps a retried request from posting twice.

Credentials: none in this file, in the repository or in the environment variables. The PostOnce API key is a network secret of the cloud
environment for postonce.to: the proxy puts it in the Authorization header, so this script sends a placeholder (the repository's .mcp.json does
the same for the MCP connection of new sessions). Without an API key, connect https://postonce.to/mcp as a claude.ai connector instead and let
the agent call the same tools.

Usage (from absurd-shorts/):
  python3 tools/postonce_publish.py --tools        list the server's tools and their input schemas
  python3 tools/postonce_publish.py --check        what is missing on the account, publish nothing
  python3 tools/postonce_publish.py                publish everything missing (--max N, --only 61-ressort ..., --pause S)
"""
import argparse, json, os, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tiktok_publish import inventory, ledger, save_ledger, norm   # noqa: E402  (the shared inventory and ledger)

MCP = 'https://postonce.to/mcp'
VERIFY = os.environ.get('REQUESTS_CA_BUNDLE') or '/root/.ccr/ca-bundle.crt'
TAGS = '#humour #absurde #animation #dessinanimé #courtmétrage'   # five: TikTok drops any past five


class Client:
    def __init__(self):
        import requests
        self.s, self.sid, self.n = requests.Session(), None, 0

    def _post(self, msg):
        h = {'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream', 'Authorization': 'Bearer proxy-injected'}   # the proxy replaces it
        if self.sid:
            h['Mcp-Session-Id'] = self.sid
        r = self.s.post(MCP, headers=h, data=json.dumps(msg), verify=VERIFY, timeout=120)
        if r.headers.get('Mcp-Session-Id'):
            self.sid = r.headers['Mcp-Session-Id']
        if r.status_code == 202 or not r.content:
            return None
        if r.status_code >= 400:
            raise SystemExit(f'PostOnce MCP: HTTP {r.status_code}: {r.text[:300]} (no API key saved for postonce.to, or the plan has no API access?)')
        if 'text/event-stream' in r.headers.get('Content-Type', ''):
            out = None
            for line in r.text.splitlines():
                if line.startswith('data:'):
                    try:
                        j = json.loads(line[5:].strip())
                    except ValueError:
                        continue
                    if j.get('id') == msg.get('id'):
                        out = j
            return out
        return r.json()

    def request(self, method, params=None):
        self.n += 1
        j = self._post({'jsonrpc': '2.0', 'id': self.n, 'method': method, **({'params': params} if params is not None else {})})
        if j is None:
            raise SystemExit(f'{method}: no answer')
        if 'error' in j:
            raise RuntimeError(f"{method}: {j['error'].get('message')} {j['error'].get('data', '')}")
        return j.get('result')

    def start(self):
        res = self.request('initialize', {'protocolVersion': '2025-03-26', 'capabilities': {}, 'clientInfo': {'name': 'absurd-shorts-publisher', 'version': '1.0'}})
        self._post({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
        return res

    def tools(self):
        return {t['name']: t for t in (self.request('tools/list') or {}).get('tools', [])}

    def call(self, name, args):
        res = self.request('tools/call', {'name': name, 'arguments': args})
        if res.get('isError'):
            raise RuntimeError(f"{name}: {' '.join(c.get('text', '') for c in res.get('content', []))[:400]}")
        if res.get('structuredContent') is not None:
            return res['structuredContent']
        txt = ' '.join(c.get('text', '') for c in res.get('content', []) if c.get('type') == 'text')
        try:
            return json.loads(txt)
        except ValueError:
            return {'text': txt}


def pick(d, *keys):
    """the first of several possible keys, looking inside a 'data' wrapper too"""
    for src in (d, d.get('data') if isinstance(d, dict) else None):
        if isinstance(src, dict):
            for k in keys:
                if src.get(k) is not None:
                    return src[k]
    return None


def items(d, *keys):
    v = pick(d, *keys)
    return v if isinstance(v, list) else (d if isinstance(d, list) else [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tools', action='store_true', help="list the server's tools and their schemas")
    ap.add_argument('--check', action='store_true', help='what is missing on the account; publish nothing')
    ap.add_argument('--max', type=int, default=0)
    ap.add_argument('--only', nargs='*')
    ap.add_argument('--pause', type=float, default=60.0)
    a = ap.parse_args()
    c = Client(); c.start(); T = c.tools()
    if a.tools:
        for n, t in sorted(T.items()):
            print(f"== {n}: {t.get('description', '')[:160]}\n   {json.dumps(t.get('inputSchema', {}), ensure_ascii=False)[:600]}")
        return
    accs = items(c.call('list_active_accounts' if 'list_active_accounts' in T else 'list_accounts', {}), 'accounts', 'items')
    tik = [x for x in accs if 'tiktok' in json.dumps(x).lower()]
    if not tik:
        raise SystemExit(f'no TikTok account connected to PostOnce ({len(accs)} accounts): connect it at https://postonce.to/dashboard/accounts')
    acc = tik[0]; acc_id = pick(acc, 'id', 'account_id')
    print(f"TikTok account: {pick(acc, 'username', 'name', 'display_name')} ({acc_id})")
    seen = []
    if 'list_posts' in T:
        for p in items(c.call('list_posts', {}), 'posts', 'items'):
            seen.append(norm(json.dumps(p, ensure_ascii=False)))
    vids, L = inventory(), ledger()
    if a.only:
        vids = [v for v in vids if v['id'] in a.only]
    missing = [v for v in vids if v['id'] not in L and not any(norm(v['title']) in s for s in seen)]
    print(f'{len(vids)} finished stories, {len(seen)} posts on PostOnce, {len(missing)} missing')
    for v in missing:
        print(f"  missing: {v['id']} « {v['title']} »")
    if a.check or not missing:
        return
    schema = (T.get('create_post') or {}).get('inputSchema', {})
    props = schema.get('properties', {})
    tgt_props = ((props.get('targets') or {}).get('items') or {}).get('properties', {})
    opts = {'privacy': 'public', 'publish_mode': 'direct', 'ai_generated': True}   # the AI label: synthetic voice, animation made by code
    done = 0
    for v in missing:
        if a.max and done >= a.max:
            break
        try:
            up = c.call('create_upload_url', {'filename': Path(v['file']).name, 'content_type': 'video/mp4'})
            signed = pick(pick(up, 'upload') or {}, 'signedUrl', 'signed_url') or pick(up, 'signedUrl', 'signed_url', 'upload_url')
            mid = pick(up, 'media_id', 'mediaId')
            with open(v['file'], 'rb') as f:
                r = c.s.put(signed, data=f.read(), headers={'Content-Type': 'video/mp4'}, verify=VERIFY, timeout=900)
            if r.status_code not in (200, 201, 204):
                raise RuntimeError(f'upload HTTP {r.status_code}')
            url = pick(c.call('get_media', {'media_id': mid}), 'url', 'public_url', 'publicUrl')
            target = {'account_id': acc_id, **({'platform_options': opts} if 'platform_options' in tgt_props else {})}
            args = {'content': f"{v['title']} {TAGS}", 'targets': [target], 'media': [{'type': 'video', 'url': url}]}
            if 'platform_options' in props and 'platform_options' not in tgt_props:
                args['platform_options'] = opts
            if 'idempotency_key' in props:
                args['idempotency_key'] = f"absurd-shorts-{v['id']}"
            post = c.call('create_post', args)
            pid = pick(post, 'id', 'post_id', 'postId')
            status, link = 'created', None
            for _ in range(36):
                time.sleep(10)
                g = c.call('get_post', {'post_id': pid} if 'post_id' in json.dumps((T.get('get_post') or {}).get('inputSchema', {})) else {'id': pid})
                status = str(pick(g, 'status', 'state') or status).lower()
                link = pick(g, 'url', 'published_url', 'permalink')
                if status in ('published', 'failed', 'error'):
                    break
            if status in ('failed', 'error'):
                raise RuntimeError(f'post {pid} failed: {json.dumps(g, ensure_ascii=False)[:300]}')
            L[v['id']] = {'title': v['title'], 'via': 'postonce', 'post_id': pid, 'status': status, 'url': link, 'at': time.strftime('%Y-%m-%d %H:%M')}
            save_ledger(L); done += 1
            print(f"  {status}: {v['id']} « {v['title']} » {link or ''}")
        except (RuntimeError, OSError) as e:
            msg = str(e)
            print(f"  FAILED {v['id']}: {msg[:300]}")
            if any(w in msg.lower() for w in ('limit', 'quota', 'too many', 'plan')):
                print('  a cap or plan limit: stopping here; the next run resumes')
                break
        if v is not missing[-1]:
            time.sleep(a.pause)
    print(f'{done} sent this run')


if __name__ == '__main__':
    main()
