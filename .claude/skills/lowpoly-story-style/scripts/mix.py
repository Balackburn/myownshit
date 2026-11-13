#!/usr/bin/env python3
"""mix.py TIMELINE.json CUES.json OUTDIR --bed STEM.wav --bed-from S --bed-len 6: narration + looped bed + synthesized effects -> OUTDIR/mix.wav"""
import json, sys, wave, subprocess, numpy as np
from scipy.signal import butter, sosfilt
sys.path.insert(0, '/home/user/myownshit/absurd-shorts/tools')
import audio3 as A3
import argparse
ap = argparse.ArgumentParser(); ap.add_argument('timeline'); ap.add_argument('cues'); ap.add_argument('out')
ap.add_argument('--bed', required=True, help='a music stem the person owns or may use'); ap.add_argument('--bed-from', type=float, default=0); ap.add_argument('--bed-len', type=float, default=6.0)
A = ap.parse_args()
SR = 44100; TL = json.load(open(A.timeline)); D = TL['total']; N = int(SR * D)
def rd(p, ch=1):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', str(ch), '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32); return x.reshape(-1, ch) if ch > 1 else x
def bp(x, lo, hi, o=4): return sosfilt(butter(o, [lo, hi], btype='band', fs=SR, output='sos'), x).astype(np.float32)
def lp(x, hi, o=4): return sosfilt(butter(o, hi, btype='low', fs=SR, output='sos'), x).astype(np.float32)
rng = np.random.default_rng(7)
def noise(d): return rng.uniform(-1, 1, int(SR * d)).astype(np.float32)
def env(n, a, r): t = np.arange(n) / SR; return (np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / max(r, 1e-4))).astype(np.float32)
# ---- voice
voice = np.zeros(N + SR, np.float32)
for l in TL['lines']:
    x = rd(l['file']); i0 = int(round(l['file_start'] * SR)); voice[i0:i0 + len(x)] += x[:len(voice) - i0]
voice = voice[:N]
# ---- music bed: a clean section of an owned/licensed stem, looped with 0.6 s equal-power crossfades
bed_src = rd(A.bed, 2)
seg = bed_src[int(A.bed_from * SR):int((A.bed_from + A.bed_len) * SR)]; X = int(0.6 * SR); L = len(seg) - X
bed = np.zeros((N + len(seg), 2), np.float32); fade = np.sqrt(np.linspace(0, 1, X))[:, None]
pos = 0
while pos < N:
    s = seg.copy(); s[:X] *= fade; s[-X:] *= fade[::-1]
    bed[pos:pos + len(s)] += s; pos += L
bed = bed[:N]; bed[:int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))[:, None]; bed[-int(0.8 * SR):] *= np.linspace(1, 0, int(0.8 * SR))[:, None]
# ---- effects (synthesized)
# (cycle 13) whoosh sorts its band: a cue written high-to-low (3000, 800: meant as a falling sweep) made scipy refuse the filter and failed the whole mix
def thunder(): x = lp(noise(2.2), 180) * env(int(2.2 * SR), 0.25, 0.7) * 3.0; return x
def rain(d): x = bp(noise(d), 1200, 9000) * 0.18 + bp(noise(d), 300, 1200) * 0.08; return x * np.minimum(1, np.arange(len(x)) / (0.25 * SR))
def whoosh(d=0.6, lo=300, hi=3000): n = int(d * SR); lo, hi = sorted((lo, hi)); x = bp(noise(d), lo, hi); e = np.sin(np.linspace(0, np.pi, n)) ** 2; return x * e * 1.4
def thud(): n = int(0.35 * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * (90 - 50 * t / 0.35) * t) * np.exp(-t * 14) * 0.9 + bp(noise(0.35), 200, 2000) * np.exp(-t * 40) * 0.5).astype(np.float32)
def clack(): n = int(0.18 * SR); t = np.arange(n) / SR; return (bp(noise(0.18), 600, 4000) * np.exp(-t * 35) + np.sin(2 * np.pi * 420 * t) * np.exp(-t * 30) * 0.4).astype(np.float32)
def clang(): n = int(1.4 * SR); t = np.arange(n) / SR; x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * d) * a for f, d, a in [(212, 3.2, 0.5), (377, 4.1, 0.35), (563, 5.0, 0.3), (911, 6.5, 0.2), (1433, 8, 0.12)]); return (x + bp(noise(1.4), 800, 6000) * np.exp(-t * 25) * 0.6).astype(np.float32)
def pop(): n = int(0.16 * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * (520 + 900 * t / 0.16) * t) * np.exp(-t * 28) * 0.6).astype(np.float32)
def gust(d=1.4): n = int(d * SR); x = bp(noise(d), 150, 1800); e = np.sin(np.linspace(0, np.pi, n)) ** 1.5; return x * e * 1.6
def engine(d): t = np.arange(int(d * SR)) / SR; x = bp(noise(d), 120, 900) * 0.5 + np.sin(2 * np.pi * 95 * t) * 0.15 + bp(noise(d), 2500, 7000) * 0.12; return x * np.minimum(1, t / 0.3)
SF = np.zeros(N + 3 * SR, np.float32)
def put(x, t, g=1.0): i = int(t * SR); SF[i:i + len(x)] += x[:len(SF) - i] * g
FX = {'thunder': thunder, 'thud': thud, 'clack': clack, 'clang': clang, 'pop': pop}
# cues: [["rain", t, gain, dur], ["whoosh", t, gain, dur, lo, hi], ["gust", t, gain, dur], ["engine", t, gain, dur], ["thud", t, gain], ["sfx:cuff", t, gain], ...]
for c in json.load(open(A.cues)):
    name, t, g = c[0], c[1], c[2]
    if name.startswith('sfx:'): x = A3.sfx(name[4:], int(t * 10))
    elif name == 'rain': x = rain(c[3])
    elif name == 'whoosh': x = whoosh(*c[3:6]) if len(c) > 3 else whoosh()
    elif name == 'gust': x = gust(c[3]) if len(c) > 3 else gust()
    elif name == 'engine': x = engine(c[3] if len(c) > 3 else 1.5)
    else: x = FX[name]()
    put(x, t, g)
SF = SF[:N]
def w16(p, x):
    x = x[:, None] if x.ndim == 1 else x
    with wave.open(p, 'wb') as w: w.setnchannels(x.shape[1]); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())
import os; os.makedirs(A.out, exist_ok=True)
w16(f'{A.out}/stem_voice.wav', voice); w16(f'{A.out}/stem_bed.wav', bed); w16(f'{A.out}/stem_sfx.wav', SF)
# mix: voice to about -16.5 LUFS alone, bed ~15 dB under, effects ~-28 LUFS; limiter at -1.5 dBFS; then check with ebur128
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{A.out}/stem_voice.wav', '-i', f'{A.out}/stem_bed.wav', '-i', f'{A.out}/stem_sfx.wav', '-filter_complex',
                '[0:a]volume=2.5dB,aformat=channel_layouts=stereo[v];[1:a]volume=3.2dB[b];[2:a]volume=-5.7dB,aformat=channel_layouts=stereo[s];'
                '[v][b][s]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.84:level=false[m]', '-map', '[m]', '-ar', str(SR), '-c:a', 'pcm_s16le', f'{A.out}/mix.wav'], check=True)
r = subprocess.run(['ffmpeg', '-nostats', '-hide_banner', '-i', f'{A.out}/mix.wav', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
print(' '.join(r[r.rfind('Integrated loudness'):].split())[:200])
print('Adjust the three volume= values until I is -16 LUFS: they were tuned for a voice stem at -18.7 LUFS, bed -33.7, effects -22.4.')
