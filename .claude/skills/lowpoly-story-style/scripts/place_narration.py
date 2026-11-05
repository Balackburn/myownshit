#!/usr/bin/env python3
"""place_narration.py LINES.json TTS_DIR OUT.json [--atempo K] [--tail 0.84]
Back-to-back placement of per-line TTS files (TTS_DIR/<id>.mp3|.wav + <id>.json ElevenLabs alignment). With --atempo, the lines are
first time-stretched (ffmpeg atempo, written as <id>.k.wav) and the timings divided by K. Gaps: GAP per line id (default 0.10 s)."""
import json, sys, os, re, subprocess, argparse, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'absurd-shorts', 'tools'))
import audio3 as A3
ap = argparse.ArgumentParser(); ap.add_argument('lines'); ap.add_argument('tts'); ap.add_argument('out')
ap.add_argument('--atempo', type=float, default=1.0); ap.add_argument('--tail', type=float, default=0.84); ap.add_argument('--gap', type=float, default=0.10)
ap.add_argument('--gaps', default='', help='per-line gaps, e.g. "L03:0.06,L27:0.16"')
a = ap.parse_args(); SR = 44100
GAP = {kv.split(':')[0]: float(kv.split(':')[1]) for kv in a.gaps.split(',') if kv}
L = json.load(open(a.lines)); t = 0.10; out = []
for l in L:
    src = next(p for p in (f"{a.tts}/{l['id']}.wav", f"{a.tts}/{l['id']}.mp3") if os.path.exists(p))
    al = json.load(open(f"{a.tts}/{l['id']}.json"))
    if a.atempo != 1.0:
        dst = f"{a.tts}/{l['id']}.k.wav"; subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af', f'atempo={a.atempo}', '-ar', str(SR), '-ac', '1', dst], check=True); src = dst
        al = {**al, 'character_start_times_seconds': [x / a.atempo for x in al['character_start_times_seconds']], 'character_end_times_seconds': [x / a.atempo for x in al['character_end_times_seconds']]}
    txt = re.sub(r'[«»]', '', l['text']).strip(); words = A3.words_from_alignment(txt, al)
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout, np.float32)
    nz = np.nonzero(np.abs(x) > 0.01)[0]; a0, a1 = nz[0] / SR, nz[-1] / SR
    s0 = max(0.0, min(words[0]['s'], a0) - 0.02)
    start = (t + GAP.get(l['id'], a.gap) - s0) if out else (t - s0); end = start + max(words[-1]['e'], a1)
    out.append({**l, 'file': src, 'file_start': round(start, 3), 'speech_start': round(start + s0, 3), 'speech_end': round(end, 3),
                'words': [{**w, 's': round(start + w['s'], 3), 'e': round(start + w['e'], 3)} for w in words]})
    t = end; print(f"{l['id']} {start + s0:6.2f}-{end:6.2f}  {txt}")
json.dump({'lines': out, 'total': round(t + a.tail, 2)}, open(a.out, 'w'), ensure_ascii=False, indent=1)
print('total', round(t + a.tail, 2))
