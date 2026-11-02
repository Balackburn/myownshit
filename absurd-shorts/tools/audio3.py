#!/usr/bin/env python3
"""Audio pipeline for script v3 (scene timelines).

  python3 tools/audio3.py tts  script.json workdir            -> workdir/script.timed.json (+ per-line wavs)
  python3 tools/audio3.py mix  workdir/script.timed.json workdir/events.json workdir   -> voice/sfx/music stems + mix.wav
  python3 tools/audio3.py srt  workdir/script.timed.json out.srt

Voice: ONE authorised voice for narrator and characters (ElevenLabs, voice matched by name, model from the script,
e.g. eleven_v4). Character lines use more expressive settings (lower stability, some style) - same identity, other
intonation. Real word timings come from the /with-timestamps endpoint; nothing is estimated when the API is reachable.
"""
import json, os, re, sys, base64, hashlib, subprocess, urllib.request
import numpy as np
from scipy.signal import butter, lfilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audio as A1  # read_wav, write_wav, sfx, music_bed, place, elevenlabs_voice_id, SR

SR = A1.SR
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CACHE = os.path.join(ROOT, 'out', 'tts_cache3')
FPS = 30

def say_text(t):
    return re.sub(r'[\U0001F300-\U0001FAFF]', '', t.replace('*', 'u').replace('«', '').replace('»', '').replace('"', '')).strip()

def tts_ts(text, voice, settings, prev, nxt):
    """ElevenLabs text-to-speech WITH character timestamps (mp3 output works on every plan)."""
    key = os.environ.get('ELEVENLABS_API_KEY')
    if not key: raise RuntimeError('ELEVENLABS_API_KEY not set')
    vid = A1.elevenlabs_voice_id(key, voice)
    payload = {'text': text, 'model_id': voice.get('model', 'eleven_v4'),
               'voice_settings': {'stability': settings.get('stability', 0.75), 'similarity_boost': settings.get('similarity', 0.8),
                                  'style': settings.get('style', 0.0), 'speed': settings.get('rate', 1.05)}}
    if prev: payload['previous_text'] = prev[-400:]
    if nxt: payload['next_text'] = nxt[:400]
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_128',
                                 json.dumps(payload).encode(), {'xi-api-key': key, 'content-type': 'application/json'})
    d = json.loads(urllib.request.urlopen(req, timeout=120).read())
    return base64.b64decode(d['audio_base64']), d.get('alignment') or d.get('normalized_alignment')

def decode_mp3(data, tmpdir):
    mp3 = os.path.join(tmpdir, '_tmp.mp3'); wav = os.path.join(tmpdir, '_tmp.wav')
    open(mp3, 'wb').write(data)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-ac', '1', '-ar', str(SR), wav], check=True)
    x = A1.read_wav(wav); os.remove(mp3); os.remove(wav); return x

def words_from_alignment(text, al):
    chars, st, en = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
    words, cur, s0, e0 = [], '', None, None
    for c, a, b in zip(chars, st, en):
        if c.isspace():
            if cur: words.append({'w': cur, 's': s0, 'e': e0}); cur = ''
            continue
        if not cur: s0 = a
        cur += c; e0 = b
    if cur: words.append({'w': cur, 's': s0, 'e': e0})
    # display words = the caption text's words (keeps « » / punctuation as written); map 1:1 when counts match
    disp = text.split()
    if len(disp) == len(words):
        for w, d in zip(words, disp): w['w'] = d
    return words

def envelope(x, n_frames):
    hop = SR // FPS; out = []
    for i in range(n_frames):
        seg = x[i * hop:(i + 1) * hop]
        out.append(float(np.sqrt(np.mean(seg ** 2))) if len(seg) else 0.0)
    out = np.array(out); ref = np.percentile(out, 92) if out.max() > 0 else 1
    return [round(float(v), 2) for v in np.clip(out / (ref + 1e-9), 0, 1)]

def cmd_tts(script_path, workdir):
    os.makedirs(workdir, exist_ok=True); os.makedirs(CACHE, exist_ok=True)
    sc = json.load(open(script_path))
    voice = sc.get('voice', {})
    narr = {'stability': 0.8, 'style': 0.0, 'rate': 1.06, **voice.get('narrator', {})}
    char = {'stability': 0.42, 'style': 0.35, 'rate': 1.0, **voice.get('character', {})}
    all_lines = [l for s in sc['scenes'] for l in s['lines']]
    n = 0
    for l in all_lines:
        n += 1; l.setdefault('id', f'L{n}')
    spoken = [say_text(l.get('say', l['text'])) for l in all_lines]
    engine_used = 'elevenlabs'
    for i, l in enumerate(all_lines):
        text = spoken[i]
        st = {**(char if l.get('speaker') else narr), **l.get('voice', {})}
        prev = ' '.join(spoken[max(0, i - 2):i]); nxt = ' '.join(spoken[i + 1:i + 3])
        key = hashlib.sha1(json.dumps([voice.get('name'), voice.get('id'), voice.get('model'), st, text, prev, nxt], sort_keys=True).encode()).hexdigest()[:16]
        cpath = os.path.join(CACHE, key + '.json')
        if os.path.exists(cpath):
            c = json.load(open(cpath)); x = A1.read_wav(os.path.join(CACHE, key + '.wav')); words = c['words']
        else:
            data, al = tts_ts(text, voice, st, prev, nxt)
            x = decode_mp3(data, workdir)
            words = words_from_alignment(l['text'], al) if al else []
            # trim: keep 40 ms before the first word, 120 ms after the last one
            if words:
                a = max(0.0, words[0]['s'] - 0.04); b = min(len(x) / SR, words[-1]['e'] + 0.12)
                x = x[int(a * SR):int(b * SR)]
                for w in words: w['s'] = round(w['s'] - a, 3); w['e'] = round(w['e'] - a, 3)
            A1.write_wav(os.path.join(CACHE, key + '.wav'), x); json.dump({'words': words, 'text': text}, open(cpath, 'w'), ensure_ascii=False)
        wav = os.path.join(workdir, f"{l['id']}.wav"); A1.write_wav(wav, x)
        l['audio'] = os.path.basename(wav); l['dur'] = round(len(x) / SR, 3); l['_words'] = words
        if l.get('speaker'): l['env'] = envelope(x, int(np.ceil(l['dur'] * FPS)) + 1)
        print(f"  {l['id']:>4} {l['dur']:5.2f}s {'['+l['speaker']+'] ' if l.get('speaker') else ''}{l['text'][:60]}", file=sys.stderr)
    # layout: scenes back to back, lines inside with small, deliberate gaps
    t = 0.0
    for si, s in enumerate(sc['scenes']):
        s['start'] = round(t, 3); cur = s.get('pre', 0.3 if si == 0 else 0.15); last_spk = None
        for li, l in enumerate(s['lines']):
            if li > 0: cur += l.get('pre', 0.3 if (l.get('speaker') or None) != last_spk else 0.18)
            else: cur += l.get('pre', 0.0)
            l['start'] = round(s['start'] + cur, 3); l['end'] = round(l['start'] + l['dur'], 3)
            l['words'] = [{'w': w['w'], 's': round(l['start'] + w['s'], 3), 'e': round(l['start'] + w['e'], 3)} for w in l.pop('_words')]
            cur = l['end'] - s['start'] + l.get('hold', 0); last_spk = l.get('speaker')
        s['duration'] = round(max(s.get('minDuration', 0), cur + s.get('tail', 0.35)), 3)
        t += s['duration']
    sc['total'] = round(t, 3); sc['_engine'] = engine_used
    out = os.path.join(workdir, 'script.timed.json'); json.dump(sc, open(out, 'w'), ensure_ascii=False, indent=1)
    print(f'{out}  {len(all_lines)} lines, total {t:.2f}s', file=sys.stderr)

# ------------------------------------------------------------------------------------------------ SFX
def bp(x, lo, hi):
    b, a = butter(2, [lo / (SR / 2), min(0.99, hi / (SR / 2))], 'band'); return lfilter(b, a, x).astype(np.float32)
def lp(x, hi):
    b, a = butter(2, hi / (SR / 2), 'low'); return lfilter(b, a, x).astype(np.float32)
def noise(d, seed=0): return np.random.default_rng(seed).uniform(-1, 1, int(SR * d)).astype(np.float32)
def decay(n, k): return np.exp(-np.linspace(0, k, n)).astype(np.float32)
def tone(f, d, kind='sine'):
    t = np.arange(int(SR * d)) / SR
    return (np.sin(2 * np.pi * f * t) if kind == 'sine' else np.sign(np.sin(2 * np.pi * f * t)) * 0.5).astype(np.float32)

def sfx(name, seed=0):
    r = np.random.default_rng(seed)
    if name == 'step': return bp(noise(0.07, seed), 180, 1400) * decay(int(0.07 * SR), 9) * 0.9
    if name == 'stepSoft': return bp(noise(0.05, seed), 400, 2500) * decay(int(0.05 * SR), 10) * 0.45
    if name == 'stepRun': return bp(noise(0.05, seed), 250, 2000) * decay(int(0.05 * SR), 12)
    if name == 'stepHeavy':
        t = np.arange(int(0.22 * SR)) / SR; return (np.sin(2 * np.pi * (70 - 30 * t / 0.22) * t) * np.exp(-t * 16) + bp(noise(0.22, seed), 80, 600) * np.exp(-t * 20) * 0.5).astype(np.float32)
    if name == 'punch':
        t = np.arange(int(0.25 * SR)) / SR; return (np.sin(2 * np.pi * (120 - 60 * t / 0.25) * t) * np.exp(-t * 18) * 0.9 + bp(noise(0.25, seed), 300, 4000) * np.exp(-t * 30) * 0.8).astype(np.float32)
    if name == 'whistle':
        t = np.arange(int(0.35 * SR)) / SR; f = 2600 + 120 * np.sin(2 * np.pi * 28 * t)
        one = (np.sin(np.cumsum(2 * np.pi * f / SR)) * 0.35 * np.minimum(1, t * 40) * np.minimum(1, (0.35 - t) * 30)).astype(np.float32)
        return np.concatenate([one, np.zeros(int(0.08 * SR), np.float32), one[:int(0.18 * SR)]])
    if name == 'needle': return bp(noise(0.25, seed), 3000, 9000) * decay(int(0.25 * SR), 6) * 0.35
    if name == 'gulp':
        t = np.arange(int(0.18 * SR)) / SR; return (np.sin(np.cumsum(2 * np.pi * (300 - 900 * t) / SR)) * np.exp(-t * 14) * 0.6).astype(np.float32)
    if name == 'poof': return lp(noise(0.4, seed), 900) * decay(int(0.4 * SR), 5) * 1.4
    if name == 'carDoor': return np.concatenate([sfx('punch', seed) * 0.6, np.zeros(int(0.05 * SR), np.float32), bp(noise(0.06, seed), 1500, 5000) * decay(int(0.06 * SR), 8) * 0.4])
    if name == 'engine':
        t = np.arange(int(1.6 * SR)) / SR; return (bp(noise(1.6, seed), 50, 300) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t)) * np.minimum(1, t * 3) * np.minimum(1, (1.6 - t) * 3) * 1.2).astype(np.float32)
    if name == 'brake': return bp(noise(0.5, seed), 2500, 6000) * np.linspace(1, 0, int(0.5 * SR)).astype(np.float32) * 0.5
    if name == 'clink':
        t = np.arange(int(0.4 * SR)) / SR; return ((np.sin(2 * np.pi * 3100 * t) + 0.6 * np.sin(2 * np.pi * 4700 * t)) * np.exp(-t * 14) * 0.3).astype(np.float32)
    if name == 'pour': return bp(noise(0.9, seed), 500, 3000) * (0.6 + 0.4 * np.sin(np.linspace(0, 40, int(0.9 * SR)))).astype(np.float32) * 0.35
    if name == 'tick': return bp(noise(0.012, seed), 2500, 7000) * 0.6
    if name == 'ticks':  # fast clock ticking (time passing)
        out = np.zeros(int(1.5 * SR), np.float32)
        for i in range(30): st = int(i * 0.05 * SR); seg = sfx('tick', i); out[st:st + len(seg)] += seg
        return out
    if name == 'ring':
        t = np.arange(int(0.9 * SR)) / SR; return ((np.sin(2 * np.pi * 1200 * t) + np.sin(2 * np.pi * 1500 * t)) * (np.sin(2 * np.pi * 20 * t) > 0) * 0.15).astype(np.float32)
    if name == 'beep': return tone(950, 0.12) * 0.25
    if name == 'squeak':
        t = np.arange(int(0.25 * SR)) / SR; return (np.sin(np.cumsum(2 * np.pi * (1800 + 600 * np.sin(2 * np.pi * 9 * t)) / SR)) * 0.12 * np.exp(-t * 3)).astype(np.float32)
    if name == 'cuff': return np.concatenate([bp(noise(0.03, seed), 2000, 8000) * 0.8, np.zeros(int(0.04 * SR), np.float32), bp(noise(0.05, seed + 1), 1500, 7000) * decay(int(0.05 * SR), 6)])
    if name == 'grunt':
        t = np.arange(int(0.45 * SR)) / SR; saw = ((t * (95 + 15 * np.sin(2 * np.pi * 7 * t))) % 1) * 2 - 1
        return (lp(saw.astype(np.float32), 700) * np.minimum(1, t * 25) * np.exp(-t * 3) * 0.8 + bp(noise(0.45, seed), 150, 900) * np.exp(-t * 4) * 0.3).astype(np.float32)
    if name == 'roar':
        t = np.arange(int(1.1 * SR)) / SR; saw = ((t * (80 + 25 * np.sin(2 * np.pi * 5 * t))) % 1) * 2 - 1
        return (lp(saw.astype(np.float32), 900) * np.minimum(1, t * 8) * np.minimum(1, (1.1 - t) * 4) * 0.9 + bp(noise(1.1, seed), 120, 1500) * 0.4 * np.minimum(1, t * 8)).astype(np.float32)
    if name == 'cluck':
        out = np.zeros(int(0.6 * SR), np.float32)
        for i, f in enumerate((780, 820, 900)): seg = (tone(f, 0.06, 'square') * decay(int(0.06 * SR), 6) * 0.25); st = int(i * 0.14 * SR); out[st:st + len(seg)] += seg
        return bp(out, 400, 3000)
    if name == 'gasp': return bp(noise(0.4, seed), 800, 5000) * np.sin(np.linspace(0, np.pi, int(0.4 * SR))).astype(np.float32) * 0.4
    if name == 'cash':
        return np.concatenate([bp(noise(0.08, seed), 1000, 6000) * decay(int(0.08 * SR), 6) * 0.5, A1.sfx('ding') * 0.5])
    if name == 'paper': return bp(noise(0.3, seed), 1500, 8000) * (0.5 + 0.5 * np.abs(np.sin(np.linspace(0, 30, int(0.3 * SR))))).astype(np.float32) * 0.3
    if name == 'splash': return bp(noise(0.6, seed), 300, 3500) * decay(int(0.6 * SR), 5) * 0.8
    if name == 'spring': return A1.sfx('boing') * 0.7
    if name == 'bell': return A1.sfx('ding') * 0.6
    return A1.sfx(name, seed)

def ambience(kind, dur, seed=0):
    n = int(SR * dur); r = np.random.default_rng(seed); x = np.zeros(n, np.float32)
    if kind in ('office', 'bank', 'station', 'gym', 'lab'):
        x = lp(noise(dur, seed), 300) * 0.12 + tone(60 if kind != 'gym' else 50, dur) * 0.015
    elif kind == 'bar':
        x = bp(noise(dur, seed), 300, 1800) * (0.6 + 0.4 * np.sin(np.linspace(0, dur * 3, n))).astype(np.float32) * 0.2
    elif kind == 'street':
        x = lp(noise(dur, seed), 400) * 0.25
        for i in range(int(dur / 3)): st = int(r.uniform(0, max(0.1, dur - 2)) * SR); car = sfx('engine', i) * 0.25; x[st:st + len(car)] += car[:n - st]
    elif kind in ('zoo', 'park', 'farm'):
        x = lp(noise(dur, seed), 500) * 0.08
        for i in range(int(dur * 1.2)):
            st = int(r.uniform(0, dur) * SR); f = r.uniform(2500, 4200); d = r.uniform(0.05, 0.12)
            t = np.arange(int(d * SR)) / SR; ch = (np.sin(np.cumsum(2 * np.pi * (f + 900 * np.sin(2 * np.pi * 25 * t)) / SR)) * np.exp(-t * 20) * 0.06).astype(np.float32)
            x[st:st + len(ch)] += ch[:n - st]
        if kind == 'farm':
            for i in range(int(dur / 2.5)): st = int(r.uniform(0, max(0.1, dur - 1)) * SR); c = sfx('cluck', i) * 0.6; x[st:st + len(c)] += c[:n - st]
    elif kind == 'night':
        t = np.arange(n) / SR; x = (np.sin(2 * np.pi * 4300 * t) * (np.sin(2 * np.pi * 28 * t) > 0.6) * (np.sin(2 * np.pi * 0.7 * t) > 0) * 0.025 + lp(noise(dur, seed), 300) * 0.05).astype(np.float32)
    elif kind == 'cave':
        x = lp(noise(dur, seed), 200) * 0.12
    return x.astype(np.float32)

def cmd_mix(timed_path, events_path, outdir):
    sc = json.load(open(timed_path)); wd = os.path.dirname(timed_path)
    ev = json.load(open(events_path)) if events_path and os.path.exists(events_path) else []
    total = sc['total']; n = int(SR * (total + 0.5))
    voice = np.zeros(n, np.float32); fx = np.zeros(n, np.float32); amb = np.zeros(n, np.float32)
    for s in sc['scenes']:
        for l in s['lines']: A1.place(voice, A1.read_wav(os.path.join(wd, l['audio'])), l['start'])
        if s.get('ambience'):
            a = ambience(s['ambience'], s['duration'], hash(s['id']) % 1000) * s.get('ambienceVol', 1.0)
            fade = np.minimum(1, np.minimum(np.arange(len(a)), np.arange(len(a))[::-1]) / (0.08 * SR)).astype(np.float32)
            A1.place(amb, a * fade, s['start'])
    for i, e in enumerate(ev):
        A1.place(fx, sfx(e['name'], i), e['t'], e.get('vol', 0.5))
    b, a = butter(2, 90 / (SR / 2), 'high'); voice = lfilter(b, a, voice).astype(np.float32)
    if np.abs(voice).max() > 0: voice = np.tanh(voice / np.abs(voice).max() * 1.5) * 0.72
    m = sc.get('music', {'mood': 'quirky', 'vol': 0.07})
    bed = A1.music_bed(total + 0.5, m.get('mood', 'quirky'), m.get('seed', 1)) if m else np.zeros(n, np.float32)
    bed = np.pad(bed, (0, max(0, n - len(bed))))[:n]
    if np.abs(bed).max() > 0: bed = bed / np.abs(bed).max() * m.get('vol', 0.07)
    env = np.convolve(np.abs(voice), np.ones(2048) / 2048, 'same'); duck = 1 - 0.5 * np.clip(env * 8, 0, 1)
    fx_peak = np.abs(fx).max()
    if fx_peak > 0.9: fx = fx / fx_peak * 0.9
    sfx_stem = fx * (1 - 0.25 * np.clip(env * 8, 0, 1)) + amb * duck
    music = bed * duck
    mix = voice + sfx_stem + music
    mix = mix[:int(SR * total)]; mix = mix / (np.abs(mix).max() + 1e-6) * 0.89
    os.makedirs(outdir, exist_ok=True)
    A1.write_wav(os.path.join(outdir, 'voice.wav'), voice[:int(SR * total)])
    A1.write_wav(os.path.join(outdir, 'sfx.wav'), np.clip(sfx_stem[:int(SR * total)], -1, 1))
    A1.write_wav(os.path.join(outdir, 'music.wav'), music[:int(SR * total)])
    A1.write_wav(os.path.join(outdir, 'mix.wav'), mix)
    print(os.path.join(outdir, 'mix.wav'), f'{total:.2f}s, {len(ev)} sfx events', file=sys.stderr)

# ------------------------------------------------------------------------------------------------ SRT
FUNC = set('le la les l un une des du de d sa son ses mon ma mes ton ta tes leur leurs ce cet cette ces au aux a et ou en pour par sur dans avec sans qui que qu il elle on ils se s ne n plus tres trop je j vous nous tu me m t c y'.split())
def norm(w): import unicodedata; return re.sub(r"[^a-z0-9']", '', unicodedata.normalize('NFD', w.lower()).encode('ascii', 'ignore').decode())
def chunks(l, max_w=3):
    ws = [dict(w) for w in l['words']]
    if not ws: return []
    if l.get('speaker'): ws[0]['w'] = '« ' + ws[0]['w']; ws[-1]['w'] += ' »'
    out, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        dangling = norm(w['w']) in FUNC and i < len(ws) - 1 and len(cur) < max_w + 2
        end = re.search(r'[.,!?;:…»]$', w['w']) or (len(cur) >= max_w and not dangling) or i == len(ws) - 1
        if end: out.append({'text': ' '.join(x['w'] for x in cur), 's': cur[0]['s'], 'e': ws[i + 1]['s'] if i + 1 < len(ws) else l['end'] + 0.15}); cur = []
    return out
def ts(t): h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60; return f'{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}'
def cmd_srt(timed_path, out):
    sc = json.load(open(timed_path)); items = []
    for s in sc['scenes']:
        for l in s['lines']: items += chunks(l, sc.get('captionWords', 3))
    items.sort(key=lambda c: c['s'])
    for i in range(len(items) - 1): items[i]['e'] = min(items[i]['e'], items[i + 1]['s'] - 0.01)
    with open(out, 'w', encoding='utf-8') as f:
        for i, c in enumerate(items, 1): f.write(f"{i}\n{ts(c['s'])} --> {ts(c['e'])}\n{c['text']}\n\n")
    print(out, len(items), 'cues', file=sys.stderr)

if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'tts': cmd_tts(sys.argv[2], sys.argv[3])
    elif c == 'mix': cmd_mix(sys.argv[2], sys.argv[3], sys.argv[4])
    elif c == 'srt': cmd_srt(sys.argv[2], sys.argv[3])
    else: print(__doc__)
