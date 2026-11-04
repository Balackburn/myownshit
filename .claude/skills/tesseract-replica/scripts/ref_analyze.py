#!/usr/bin/env python3
"""ref_analyze.py — first pass on a reference video: probe, cuts, per-shot colour/motion, contact sheets, word timings.

usage: ref_analyze.py REF.mp4 OUTDIR [--no-words] [--cut-threshold 0.18]
writes OUTDIR/: probe.json, cuts.json, shot_metrics.json, shots_skeleton.json, sheet_*.jpg, cuts_check.jpg, words.json
Check every cut on cuts_check.jpg: whips, flashes and cloud wipes are not cuts; gradual wipes are missed.
"""
import argparse, json, os, subprocess, wave
import numpy as np, cv2
from skimage.color import rgb2lab

def run(cmd): return subprocess.run(cmd, capture_output=True)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('ref'); ap.add_argument('out'); ap.add_argument('--no-words', action='store_true')
    ap.add_argument('--cut-threshold', type=float, default=0.18); a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    pj = json.loads(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,pix_fmt,color_space,color_transfer,sample_rate,channels', '-of', 'json', a.ref]).stdout)
    json.dump(pj, open(f'{a.out}/probe.json', 'w'), indent=1)
    v = [s for s in pj['streams'] if s['codec_type'] == 'video'][0]; W, H = int(v['width']), int(v['height']); n, d = v['r_frame_rate'].split('/'); fps = float(n) / float(d)
    w, h = 144, int(round(144 * H / W / 2) * 2)
    raw = run(['ffmpeg', '-v', 'error', '-i', a.ref, '-vf', f'scale={w}:{h}:flags=area', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']).stdout
    F = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3); N = len(F)
    g = F.mean(-1); diff = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))
    def hist(f): hh, _ = np.histogramdd(f.reshape(-1, 3), bins=(8, 8, 8), range=((0, 256),) * 3); return hh.ravel() / hh.sum()
    hs = np.array([hist(f) for f in F]); hd = 0.5 * np.abs(np.diff(hs, axis=0)).sum(1); med = np.median(diff)
    cand = [i + 1 for i in range(len(diff)) if (diff[i] > max(12, 4 * med) and hd[i] > a.cut_threshold) or hd[i] > 0.35]
    cuts = [0]
    for c in cand:
        if c - cuts[-1] > 3: cuts.append(c)
    cuts.append(N); json.dump(dict(fps=fps, frames=N, cuts=cuts, diff=diff.round(2).tolist(), hist=hd.round(3).tolist()), open(f'{a.out}/cuts.json', 'w'))
    # cut check sheet
    tiles = [np.concatenate([F[c - 1], F[c]], 1) for c in cuts[1:-1]]
    if tiles:
        cols = 7; rows = [np.concatenate(tiles[i:i + cols] + [np.zeros_like(tiles[0])] * (cols - len(tiles[i:i + cols])), 1) for i in range(0, len(tiles), cols)]
        cv2.imwrite(f'{a.out}/cuts_check.jpg', cv2.cvtColor(np.concatenate(rows, 0), cv2.COLOR_RGB2BGR))
    shots = []; mets = []
    for i, (s, e) in enumerate(zip(cuts[:-1], cuts[1:])):
        seg = F[s:e].astype(np.float32) / 255; lab = rgb2lab(seg[::3].reshape(-1, 1, 3)).reshape(-1, 3)
        sat = ((seg.max(-1) - seg.min(-1)) / np.maximum(seg.max(-1), 1e-6)).mean()
        mot = float(np.abs(np.diff(seg.mean(-1), axis=0)).mean() * 255) if e - s > 1 else 0
        mets.append(dict(id=f'S{i + 1}', frames=[s, e - 1], t0=round(s / fps, 3), t1=round(e / fps, 3), L=round(float(lab[:, 0].mean()), 1), a=round(float(lab[:, 1].mean()), 1), b=round(float(lab[:, 2].mean()), 1), sat=round(float(sat), 3), motion=round(mot, 1)))
        shots.append(dict(id=f'S{i + 1}', frames=[s, e - 1], t0=round(s / fps, 3), t1=round(e / fps, 3), title='', camera='', subjects='', set='', fx=''))
    json.dump(mets, open(f'{a.out}/shot_metrics.json', 'w'), indent=1)
    json.dump(dict(reference=dict(file=os.path.basename(a.ref), width=W, height=H, fps=fps, frames=N), shots=shots, captions=[]), open(f'{a.out}/shots_skeleton.json', 'w'), indent=1)
    # start / middle / end sheets, 8 shots per sheet
    raw = run(['ffmpeg', '-v', 'error', '-i', a.ref, '-vf', 'scale=216:384:flags=area', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']).stdout
    B = np.frombuffer(raw, np.uint8).reshape(-1, 384, 216, 3)
    for k in range(0, len(shots), 8):
        rows = []
        for s in shots[k:k + 8]:
            f0, f1 = s['frames']; rows.append(np.concatenate([B[min(f0 + 1, f1)], B[(f0 + f1) // 2], B[max(f1 - 1, f0)]], 1))
        pad = [np.zeros_like(rows[0])] * (len(rows) % 2)
        rows += pad; grid = np.concatenate([np.concatenate(rows[i:i + 2], 1) for i in range(0, len(rows), 2)], 0)
        cv2.imwrite(f'{a.out}/sheet_{k // 8 + 1}.jpg', cv2.cvtColor(grid, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 82])
    if not a.no_words:
        try:
            from faster_whisper import WhisperModel
            run(['ffmpeg', '-v', 'error', '-y', '-i', a.ref, '-vn', '-ac', '1', '-ar', '16000', f'{a.out}/audio16k.wav'])
            wv = wave.open(f'{a.out}/audio16k.wav'); x = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32) / 32768
            segs, _ = WhisperModel('base.en', device='cpu', compute_type='int8').transcribe(x, word_timestamps=True, beam_size=5)
            json.dump([dict(start=s.start, end=s.end, text=s.text, words=[dict(w=t.word, s=t.start, e=t.end) for t in s.words]) for s in segs], open(f'{a.out}/words.json', 'w'), indent=1)
        except Exception as ex: print('word timings skipped:', ex)
    print(f'{N} frames @ {fps} fps, {len(shots)} shots; cuts at frames {cuts[1:-1]}')

if __name__ == '__main__': main()
