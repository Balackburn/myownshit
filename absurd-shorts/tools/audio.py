#!/usr/bin/env python3
"""Audio pipeline for absurd-shorts.

  python3 tools/audio.py tts  script.json  out/work/    -> out/work/script.timed.json + per-shot wavs
  python3 tools/audio.py mix  out/work/script.timed.json out/work/mix.wav

TTS engines (pick with script.voice.engine or $TTS_ENGINE):
  elevenlabs : best quality. Needs $ELEVENLABS_API_KEY (+ optional voice.id). Deep, deadpan male voice recommended.
  openai     : needs $OPENAI_API_KEY (model gpt-4o-mini-tts, voice "onyx").
  espeak     : offline fallback (espeak-ng + mbrola fr1/fr4). Robotic but works anywhere.
Narration style measured on the source: deep male (~110 Hz median F0), flat deadpan
delivery, fast (~3.3 words/s), almost no pauses between sentences (gaps 0.25-0.4 s),
light music bed ~30 dB under the voice.
"""
import json, os, re, subprocess, sys, wave, shutil, urllib.request
import numpy as np
from scipy.signal import lfilter, butter

SR = 44100

def read_wav(p):
    with wave.open(p) as w:
        sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        x = np.frombuffer(w.readframes(n), {2: np.int16, 4: np.int32, 1: np.uint8}[sw]).astype(np.float32)
        x /= {2: 32768, 4: 2**31, 1: 128}[sw]
        if ch > 1: x = x.reshape(-1, ch).mean(1)
    if sr != SR:  # linear resample is fine for speech
        t = np.arange(int(len(x) * SR / sr)) * sr / SR
        x = np.interp(t, np.arange(len(x)), x).astype(np.float32)
    return x

def write_wav(p, x):
    x = np.clip(x, -1, 1)
    with wave.open(p, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())

def trim_silence(x, thr=0.01):
    idx = np.where(np.abs(x) > thr)[0]
    return x[max(0, idx[0] - 200): idx[-1] + 400] if len(idx) else x

# --------------------------------------------------------------------- TTS
def tts_espeak(text, out, voice):
    v = voice.get('espeak', 'mb-fr1')
    if not os.path.exists('/usr/share/mbrola/fr1') and v.startswith('mb-'): v = 'fr'
    tmp = out + '.raw.wav'
    subprocess.run(['espeak-ng', '-v', v, '-s', str(voice.get('speed', 172)), '-p', str(voice.get('pitch', 32)), '-a', '160', '-w', tmp, text], check=True)
    x = trim_silence(read_wav(tmp)); os.remove(tmp)
    return x

def tts_elevenlabs(text, out, voice):
    key = os.environ['ELEVENLABS_API_KEY']; vid = voice.get('id', 'pNInz6obpgDQGcFmaJgB')  # "Adam" default, deep male
    body = json.dumps({'text': text, 'model_id': voice.get('model', 'eleven_multilingual_v2'),
                       'voice_settings': {'stability': voice.get('stability', 0.75), 'similarity_boost': 0.8, 'style': 0.0, 'speed': voice.get('rate', 1.1)}}).encode()
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=pcm_44100', body,
                                 {'xi-api-key': key, 'content-type': 'application/json'})
    pcm = urllib.request.urlopen(req, timeout=60).read()
    return trim_silence(np.frombuffer(pcm, np.int16).astype(np.float32) / 32768)

def tts_openai(text, out, voice):
    key = os.environ['OPENAI_API_KEY']
    body = json.dumps({'model': voice.get('model', 'gpt-4o-mini-tts'), 'voice': voice.get('id', 'onyx'), 'input': text, 'response_format': 'pcm',
                       'instructions': voice.get('instructions', "Narrateur français, voix grave, ton totalement pince-sans-rire et blasé, débit rapide, aucune emphase.")}).encode()
    req = urllib.request.Request('https://api.openai.com/v1/audio/speech', body, {'authorization': f'Bearer {key}', 'content-type': 'application/json'})
    pcm = np.frombuffer(urllib.request.urlopen(req, timeout=60).read(), np.int16).astype(np.float32) / 32768
    t = np.arange(int(len(pcm) * SR / 24000)) * 24000 / SR  # 24 kHz -> 44.1 kHz
    return trim_silence(np.interp(t, np.arange(len(pcm)), pcm).astype(np.float32))

def speakable(text):
    # captions may censor ("p*tain"); the voice says the full word; strip quotes/emoji
    t = text.replace('*', 'u').replace('"', '').replace('«', '').replace('»', '')
    return re.sub(r'[\U0001F300-\U0001FAFF]', '', t)

def syllables(w):
    return max(1, len(re.findall(r'[aeiouyàâäéèêëîïôöùûüœæ]+', w.lower())))

def cmd_tts(script_path, workdir):
    os.makedirs(workdir, exist_ok=True)
    sc = json.load(open(script_path))
    voice = sc.get('voice', {})
    engine = os.environ.get('TTS_ENGINE') or voice.get('engine') or ('elevenlabs' if os.environ.get('ELEVENLABS_API_KEY') else 'openai' if os.environ.get('OPENAI_API_KEY') else 'espeak')
    fn = {'espeak': tts_espeak, 'elevenlabs': tts_elevenlabs, 'openai': tts_openai}[engine]
    gap = voice.get('gap', 0.12)
    for i, shot in enumerate(sc['shots']):
        line = shot.get('say', shot.get('line', ''))
        if not line.strip():
            shot['duration'] = shot.get('duration', 1.2); shot['words'] = []; continue
        wav = os.path.join(workdir, f'shot{i:02d}.wav')
        v = {**voice, **shot.get('voice', {})}  # per-shot override (e.g. a cop's dialogue line)
        if line.strip().startswith(('"', '«')) and 'voice' not in shot:  # quoted dialogue -> second voice by default
            v = {**v, **sc.get('dialogueVoice', {'pitch': 48, 'speed': 185, 'id': voice.get('dialogueId', voice.get('id'))})}
        try: x = fn(speakable(line), wav, v)
        except Exception as e:
            print(f'[tts] {engine} failed on shot {i} ({e}); falling back to espeak', file=sys.stderr)
            x = tts_espeak(speakable(line), wav, v)
        write_wav(wav, x)
        speech = len(x) / SR
        # word timings: distribute by syllable weight (good enough for 2-4 word captions)
        ws = (shot.get('line') or line).split()
        weights = [syllables(w) + 0.35 for w in ws]; tot = sum(weights); acc = 0; words = []
        lead = shot.get('lead', 0.05)
        for w, k in zip(ws, weights):
            s = lead + acc / tot * speech; acc += k; words.append({'w': w, 's': round(s, 3), 'e': round(lead + acc / tot * speech, 3)})
        shot['words'] = words; shot['audio'] = os.path.basename(wav); shot['speech'] = round(speech, 3)
        shot['duration'] = round(max(shot.get('minDuration', 0.9), lead + speech + gap) + shot.get('hold', 0), 3)
    sc['_engine'] = engine
    out = os.path.join(workdir, 'script.timed.json'); json.dump(sc, open(out, 'w'), ensure_ascii=False, indent=1)
    print(out, 'total %.2fs' % sum(s['duration'] for s in sc['shots']), 'engine', engine)

# ------------------------------------------------------------------ music bed
def pluck(freq, dur, decay=0.996, bright=0.5, seed=0):
    n = int(SR * dur); p = max(2, int(SR / freq)); r = np.random.default_rng(seed)
    buf = r.uniform(-1, 1, p).astype(np.float32); out = np.zeros(n, np.float32)
    for i in range(n):  # Karplus-Strong
        out[i] = buf[i % p]; buf[i % p] = decay * (bright * buf[i % p] + (1 - bright) * buf[(i + 1) % p])
    return out * np.linspace(1, 0, n) ** 0.5

def tone(freq, dur, kind='sine', vol=1.0):
    t = np.arange(int(SR * dur)) / SR
    w = {'sine': np.sin(2 * np.pi * freq * t), 'square': np.sign(np.sin(2 * np.pi * freq * t)) * 0.5,
         'tri': 2 * np.abs(2 * (t * freq % 1) - 1) - 1}[kind]
    return (w * vol).astype(np.float32)

def env(x, a=0.005, r=0.1):
    n = len(x); e = np.ones(n, np.float32); na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr and nr < n: e[-nr:] = np.linspace(1, 0, nr)
    return x * e

NOTE = lambda m: 440 * 2 ** ((m - 69) / 12)

def music_bed(total, mood='quirky', seed=1):
    """Light procedural loop: pizzicato plucks + soft bass + brush ticks (no copyrighted music)."""
    bpm = {'quirky': 112, 'tense': 96, 'sad': 72, 'night': 88, 'epic': 120}.get(mood, 112)
    beat = 60 / bpm; n = int(SR * (total + 1)); out = np.zeros(n, np.float32)
    progs = {'quirky': [(60, 'maj'), (57, 'min'), (53, 'maj'), (55, 'maj')], 'tense': [(57, 'min'), (58, 'maj'), (57, 'min'), (56, 'dim')],
             'sad': [(57, 'min'), (53, 'maj'), (48, 'maj'), (55, 'maj')], 'night': [(50, 'min'), (46, 'maj'), (48, 'maj'), (45, 'min')], 'epic': [(50, 'min'), (46, 'maj'), (41, 'maj'), (48, 'maj')]}
    iv = {'maj': [0, 4, 7], 'min': [0, 3, 7], 'dim': [0, 3, 6]}
    prog = progs.get(mood, progs['quirky']); rng = np.random.default_rng(seed)
    pattern = [0, 2, 1, 2, 0, 2, 1, 2]  # arpeggio index per 8th
    t = 0.0; bar = 0; cache = {}
    while t < total + 1:
        root, q = prog[bar % len(prog)]
        for k in range(8):
            st = int((t + k * beat / 2) * SR)
            if st >= n: break
            m = root + iv[q][pattern[k]] + (12 if k in (3, 7) and mood == 'quirky' else 0)
            key = (m,)
            if key not in cache: cache[key] = pluck(NOTE(m), 0.45, 0.994, 0.5, seed=m)
            s = cache[key]; e = min(n, st + len(s)); out[st:e] += s[:e - st] * 0.35
            if k % 4 == 0:  # bass
                b = env(tone(NOTE(root - 24), beat * 1.6, 'tri', 0.5), 0.01, 0.3); e = min(n, st + len(b)); out[st:e] += b[:e - st]
            if mood in ('quirky', 'epic') and k % 2 == 1:  # brush tick
                nz = rng.uniform(-1, 1, int(0.04 * SR)).astype(np.float32) * np.linspace(1, 0, int(0.04 * SR)) ** 3 * 0.12
                bb, aa = butter(2, 5000 / (SR / 2), 'high'); nz = lfilter(bb, aa, nz).astype(np.float32); e = min(n, st + len(nz)); out[st:e] += nz[:e - st]
        t += beat * 4; bar += 1
    return out[:int(SR * total)]

# ----------------------------------------------------------------------- SFX
def sfx(name, seed=0):
    r = np.random.default_rng(seed); noise = lambda d: r.uniform(-1, 1, int(SR * d)).astype(np.float32)
    def bp(x, lo, hi): b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], 'band'); return lfilter(b, a, x).astype(np.float32)
    if name == 'whoosh':
        d = 0.45; x = noise(d); out = np.zeros_like(x); seg = len(x) // 12
        for i in range(12):  # sweeping band
            c = 400 + 2600 * np.sin(np.pi * i / 12); out[i * seg:(i + 1) * seg] = bp(x[i * seg:(i + 1) * seg], c * 0.6, c * 1.4)
        return out * np.sin(np.linspace(0, np.pi, len(x))) * 1.2
    if name == 'pop': return env(tone(900, 0.08) * np.exp(-np.linspace(0, 8, int(0.08 * SR))), 0.001, 0.03) * 0.8
    if name == 'thud': t = np.arange(int(0.35 * SR)) / SR; return (np.sin(2 * np.pi * (110 - 70 * t / 0.35) * t) * np.exp(-t * 12)).astype(np.float32)
    if name == 'ding': t = np.arange(int(1.2 * SR)) / SR; return ((np.sin(2 * np.pi * 1318 * t) + 0.4 * np.sin(2 * np.pi * 2637 * t)) * np.exp(-t * 3.5) * 0.5).astype(np.float32)
    if name == 'siren':  # French "pin-pon" two-tone
        parts = [env(tone(f, 0.45, 'square', 0.25), 0.01, 0.02) for f in (435, 580, 435, 580)]; return bp(np.concatenate(parts), 300, 3000)
    if name == 'shutter': return np.concatenate([bp(noise(0.03), 2000, 8000) * np.linspace(1, 0, int(0.03 * SR)), np.zeros(int(0.05 * SR), np.float32), bp(noise(0.04), 1500, 6000) * np.linspace(1, 0, int(0.04 * SR))])
    if name == 'kaching':
        bell = sfx('ding') * 0.6; clank = bp(noise(0.12), 800, 4000) * np.exp(-np.linspace(0, 6, int(0.12 * SR)))
        out = np.zeros(len(bell) + int(0.1 * SR), np.float32); out[:len(clank)] += clank; out[int(0.1 * SR):] += bell; return out
    if name == 'scratch':  # record scratch
        t = np.arange(int(0.5 * SR)) / SR; f = 300 + 900 * np.abs(np.sin(2 * np.pi * 3 * t)); ph = np.cumsum(2 * np.pi * f / SR)
        return (bp(noise(0.5), 300, 4000) * 0.6 + np.sign(np.sin(ph)) * 0.15) * np.exp(-t * 2)
    if name == 'boing': t = np.arange(int(0.6 * SR)) / SR; f = 180 + 260 * np.exp(-t * 6) * np.abs(np.cos(2 * np.pi * 9 * t)); return (np.sin(np.cumsum(2 * np.pi * f / SR)) * np.exp(-t * 4) * 0.7).astype(np.float32)
    if name == 'splat': return bp(noise(0.25), 150, 1200) * np.exp(-np.linspace(0, 10, int(0.25 * SR))) * 1.5
    if name == 'glass': t = np.arange(int(0.8 * SR)) / SR; return ((np.sin(2 * np.pi * 2900 * t) + np.sin(2 * np.pi * 4100 * t)) * np.exp(-t * 7) * 0.3 + bp(noise(0.8), 3000, 9000) * np.exp(-t * 9) * 0.6).astype(np.float32)
    if name == 'gavel': return np.concatenate([sfx('thud') * 0.9, sfx('thud') * 0.9])
    if name == 'wind': return bp(noise(2.0), 200, 900) * (0.6 + 0.4 * np.sin(np.linspace(0, 6, int(2 * SR))))
    if name == 'rotor': t = np.arange(int(2.0 * SR)) / SR; return (bp(noise(2.0), 60, 400) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 14 * t))) * 0.8).astype(np.float32)
    if name == 'click': return bp(noise(0.02), 1500, 6000) * np.linspace(1, 0, int(0.02 * SR))
    if name == 'sting':  # comedic "wah-wah" ending
        return np.concatenate([env(tone(NOTE(m), d, 'tri', 0.35), 0.01, 0.08) for m, d in ((62, 0.3), (61, 0.3), (60, 0.3), (59, 0.8))])
    if name == 'tada': return np.concatenate([env(tone(NOTE(m), d, 'square', 0.18), 0.005, 0.05) for m, d in ((72, 0.12), (76, 0.12), (79, 0.5))])
    if name == 'crickets':
        t = np.arange(int(2.0 * SR)) / SR; return (np.sin(2 * np.pi * 4500 * t) * (np.sin(2 * np.pi * 30 * t) > 0.6) * (np.sin(2 * np.pi * 0.8 * t) > 0) * 0.08).astype(np.float32)
    if name == 'step': return bp(noise(0.06), 200, 1500) * np.exp(-np.linspace(0, 9, int(0.06 * SR)))
    return np.zeros(1, np.float32)

SFX_NAMES = ['whoosh', 'pop', 'thud', 'ding', 'siren', 'shutter', 'kaching', 'scratch', 'boing', 'splat', 'glass', 'gavel', 'wind', 'rotor', 'click', 'sting', 'tada', 'crickets', 'step']

def place(track, x, at, vol=1.0):
    st = int(at * SR)
    if st >= len(track) or st < 0: return
    e = min(len(track), st + len(x)); track[st:e] += x[:e - st] * vol

def cmd_mix(timed_path, out_wav):
    sc = json.load(open(timed_path)); wd = os.path.dirname(timed_path)
    total = sum(s['duration'] for s in sc['shots']) + sc.get('tail', 0.0)
    voice = np.zeros(int(SR * (total + 1)), np.float32); fxt = np.zeros_like(voice)
    t = 0.0
    for s in sc['shots']:
        if s.get('audio'): place(voice, read_wav(os.path.join(wd, s['audio'])), t + s.get('lead', 0.05))
        for f in s.get('sfx', []):
            f = {'name': f} if isinstance(f, str) else f
            place(fxt, sfx(f['name'], f.get('seed', 0)), t + f.get('at', 0), f.get('vol', 0.5))
        t += s['duration']
    # voice: normalize + gentle "radio" presence (high-pass + light saturation)
    b, a = butter(2, 90 / (SR / 2), 'high'); voice = lfilter(b, a, voice).astype(np.float32)
    if np.abs(voice).max() > 0: voice = np.tanh(voice / np.abs(voice).max() * 1.6) * 0.7
    m = sc.get('music', {'mood': 'quirky', 'vol': 0.09})
    bed = music_bed(total + 1, m.get('mood', 'quirky'), m.get('seed', 1)) if m else np.zeros_like(voice)
    if len(bed): bed = bed / (np.abs(bed).max() + 1e-6) * m.get('vol', 0.09)
    n = len(voice); bed = np.pad(bed, (0, max(0, n - len(bed))))[:n]
    # duck the music under speech
    envv = np.convolve(np.abs(voice), np.ones(2048) / 2048, 'same'); duck = 1 - 0.45 * np.clip(envv * 8, 0, 1)
    mix = voice + bed * duck + fxt
    mix = mix[:int(SR * total)]
    mix = mix / (np.abs(mix).max() + 1e-6) * 0.89
    write_wav(out_wav, mix); print(out_wav, '%.2fs' % (len(mix) / SR))

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'tts': cmd_tts(sys.argv[2], sys.argv[3])
    elif cmd == 'mix': cmd_mix(sys.argv[2], sys.argv[3])
    elif cmd == 'sfx':  # preview: python3 tools/audio.py sfx siren out.wav
        write_wav(sys.argv[3], sfx(sys.argv[2]) * 0.8)
    else: print(__doc__)
