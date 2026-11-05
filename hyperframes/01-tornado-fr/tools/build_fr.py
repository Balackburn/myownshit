# French captions composition + voice track from timed_fr.json (ElevenLabs word timings)
import json, html, os, subprocess, numpy as np, wave
T = json.load(open('timed_fr.json')); PROJ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SR = 44100; DUR = 28.8
# 1) line placement: at the English line's start, pushed later only if the previous line is still speaking
t_prev_end = -1; place = []
for l in T:
    st = max(l['at'], t_prev_end + 0.06); place.append(st); t_prev_end = st + l['words'][-1]['e']
    print(f"{l['id']} at {st:.3f} (slot {l['at']:.3f}) ends {t_prev_end:.3f}")
# 2) caption groups
groups = []   # (start, html)
for l, st in zip(T, place):
    wi = 0
    for gi, g in enumerate(l['groups']):
        toks = g.replace('<br/>', ' <br/> ').split(); spans = []; first = None
        for tok in toks:
            if tok == '<br/>': spans.append('<br/>'); continue
            w = l['words'][wi]; wi += 1
            if first is None: first = w['s']
            cls = 'hl' if tok in l['hl'] else ''
            spans.append(f'<span class="{cls}">{html.escape(tok)}</span>')
        t0 = (0.0 if st < 0.2 else st) if gi == 0 else st + first - 0.03
        groups.append((round(t0, 3), ' '.join(spans)))
    assert wi == len(l['words']), (l['id'], wi, len(l['words']))
divs = '\n'.join(f'      <div id="cap-{i:02d}" class="cap">{h}</div>' for i, (t, h) in enumerate(groups))
sets = []
for i, (t, h) in enumerate(groups):
    t1 = groups[i + 1][0] if i + 1 < len(groups) else DUR
    sets.append(f'    tl.set("#cap-{i:02d}", {{ opacity: 1, visibility: "visible" }}, {t:.3f});')
    sets.append(f'    tl.set("#cap-{i:02d}", {{ opacity: 0, visibility: "hidden" }}, {t1:.3f});')
src = open(f'{PROJ}/compositions/captions.html').read()
head = src[:src.index('<div id="root"')]
out = head + '<div id="root" data-composition-id="captions" data-width="576" data-height="1024">\n' + divs + '\n  </div>\n  <script>\n    const tl = gsap.timeline({ paused: true });\n' + '\n'.join(sets) + '\n    window.__timelines["captions"] = tl;\n  </script>\n</template>\n'
open(f'{PROJ}/compositions/captions.html', 'w').write(out)
# 3) voice track (mono 44.1 kHz float -> 16-bit wav)
v = np.zeros(int(SR * DUR) + SR, np.float32)
for l, st in zip(T, place):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f"{l['id']}.mp3", '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32); i0 = int(round(st * SR)); v[i0:i0 + len(x)] += x[:len(v) - i0]
v = v[:int(SR * DUR)]
with wave.open('voice_fr.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(v, -1, 1) * 32767).astype('<i2').tobytes())
json.dump({'place': place, 'groups': groups}, open('placement_fr.json', 'w'), ensure_ascii=False, indent=1)
print(len(groups), 'caption groups; voice peak', float(np.abs(v).max()))
