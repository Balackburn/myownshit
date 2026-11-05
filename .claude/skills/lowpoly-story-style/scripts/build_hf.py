# Vos papiers: captions + title cards for HyperFrames from the narration timeline (1080x1920, the tornado replica's caption style x1.875)
import json, html, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
import argparse
ap = argparse.ArgumentParser(); ap.add_argument("timeline"); ap.add_argument("project"); ap.add_argument("--cards", default="", help="SHOT:WORD,... (cards are written as compositions/card-<n>.html)")
A = ap.parse_args(); PROJ = A.project
TL = json.load(open(A.timeline)); D = TL["total"]
groups = []
FN = {'un', 'une', 'le', 'la', 'les', 'de', 'du', 'des', 'à', 'a', 'dans', 'en', 'pour', 'sa', 'ses', 'tes', 'cet', 'ce', 'il', 'ils', 'on', 'et', 'avant', 'tout', 'pas', 'qu\'il', 'est'}
for l in TL['lines']:
    words = l['words']; disp = re.sub(r'[«»]', '', l['text']).split(); assert len(disp) == len(words), l['id']
    toks = []   # (first word timing, display text): a lone "!" / "?" joins the word before it (French spacing, kept non-breaking)
    for w, d in zip(words, disp):
        if toks and d in ('!', '?', ':', ';'): toks[-1] = (toks[-1][0], toks[-1][1] + '\u00a0' + d)
        else: toks.append((w, d))
    phrases, cur = [], []
    for t in toks:
        cur.append(t)
        if t[1][-1] in '.,!?': phrases.append(cur); cur = []
    if cur: phrases.append(cur)
    for ph in phrases:
        n = len(ph); text = ' '.join(x[1] for x in ph)
        if n <= 4 and len(text) <= 22: groups.append((ph, l)); continue
        k = max(2, -(-n // 4)); b = [0]
        for j in range(1, k):   # each cut: the candidate near the even split that does not end a group on a small word or leave one word alone
            ideal = round(j * n / k); best = None
            for c in (ideal - 1, ideal, ideal + 1):
                if c <= b[-1] + 1 or c >= n - 1 and j == k - 1 and n - c < 2 or c >= n: continue
                pen = (3 if ph[c - 1][1].lower() in FN else 0) + (5 if c - b[-1] < 2 else 0) + (5 if j == k - 1 and n - c < 2 else 0) + abs(c - ideal)
                if best is None or pen < best[0]: best = (pen, c)
            b.append(best[1] if best else ideal)
        b.append(n)
        for i in range(len(b) - 1):
            g = ph[b[i]:b[i + 1]]
            if len(' '.join(x[1] for x in g)) > 22 and len(g) >= 2:   # still too wide for one caption line: halve it, not after a small word
                m = len(g) // 2
                if g[m - 1][1].lower() in FN and m + 1 < len(g): m += 1
                groups.append((g[:m], l)); groups.append((g[m:], l))
            else: groups.append((g, l))
caps = []
for i, (g, l) in enumerate(groups):
    t0 = 0.0 if i == 0 else round(g[0][0]['s'] - 0.03, 3)
    spans = ' '.join(f'<span class="{"hl" if d.split(chr(160))[0] in l["hl"] or d in l["hl"] else ""}">{html.escape(d)}</span>' for w, d in g)
    caps.append((t0, spans))
divs = '\n'.join(f'      <div id="cap-{i:02d}" class="cap">{s}</div>' for i, (t, s) in enumerate(caps))
sets = []
for i, (t, s) in enumerate(caps):
    t1 = caps[i + 1][0] if i + 1 < len(caps) else D
    sets += [f'    tl.set("#cap-{i:02d}", {{ opacity: 1, visibility: "visible" }}, {t:.3f});', f'    tl.set("#cap-{i:02d}", {{ opacity: 0, visibility: "hidden" }}, {t1:.3f});']
cap_html = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    .cap {{ position: absolute; left: 0; width: 1080px; top: 1522px; text-align: center; opacity: 0; visibility: hidden;
           font-family: "Nunito", sans-serif; font-weight: 900; font-size: 60px; line-height: 1.12; color: #FEFEFC; letter-spacing: -0.4px;
           -webkit-text-stroke: 13px #1C252A; paint-order: stroke fill; text-shadow: 0 4px 6px rgba(0, 0, 0, 0.35); }}
    .cap .hl {{ color: #D88168; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{divs}
  </div>
  <script>
    // The tornado replica's caption style (Nunito 900, white, dark stroke, keywords in #D88168), scaled x1.875 for 1080x1920.
    // Groups of up to 3 words, cut at punctuation, each shown from its first spoken word to the next group's.
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(sets)}
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
open(os.path.join(PROJ, 'compositions', 'captions.html'), 'w').write(cap_html)
# title cards: the THEFT card of the replica (navy card, white Poppins 600), its measured drop-and-spring keys, x1.875
K = [[0, -200, 1.5], [1, -153, 1.5], [2, 56.5, 3.2], [3, 29, 4.1], [4, 4.5, 3.4], [5, -20, 2.3], [6, -32, 1.3], [7, -30, 0.5], [8, -19.5, 0.4], [9, -7.5, 0.6],
     [10, 1, 1.0], [11, 4.5, 1.4], [12, 2.5, 1.65], [13, -1.5, 1.65], [14, -5, 1.5], [15, -7, 1.3], [16, -7.5, 1.15], [17, -5.5, 1.15], [18, -3.5, 1.15], [19, -1, 1.3], [20, 0, 1.27]]
K = [[f, round(y * 1.875, 1), r] for f, y, r in K]
CARDS = [(f'c{i + 1}', kv.split(':', 1)[1]) for i, kv in enumerate(A.cards.split(',')) if kv]
for cid, word in CARDS:
    open(os.path.join(PROJ, 'compositions', f'card-{cid}.html'), 'w').write(f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    #card-{cid} {{ position: absolute; left: 45px; top: 141px; width: 977px; height: 214px; background: #203447; border-radius: 2px;
                  box-shadow: 0 6px 11px rgba(0, 0, 0, 0.22); display: flex; align-items: center; justify-content: center; opacity: 0; }}
    #word-{cid} {{ font-family: "Poppins", sans-serif; font-weight: 600; font-size: {129 if len(word) <= 9 else 116}px; line-height: 1; color: #FFFFFF; letter-spacing: 1px;
                  text-shadow: 0 0 9px rgba(255, 255, 255, 0.35); white-space: nowrap; }}
  </style>
  <div id="root" data-composition-id="card-{cid}" data-width="1080" data-height="1920">
    <div id="card-{cid}"><span id="word-{cid}">{word}</span></div>
  </div>
  <script>
    // The replica's THEFT card motion (measured frame by frame): drops in from above, overshoots, springs back, settles tilted 1.27 deg.
    const tl = gsap.timeline({{ paused: true }});
    const K = {json.dumps(K)};
    tl.set("#card-{cid}", {{ opacity: 0, y: K[0][1], rotation: K[0][2] }}, 0);
    for (let i = 1; i < K.length; i++) tl.to("#card-{cid}", {{ y: K[i][1], rotation: K[i][2], duration: 1 / 30, ease: "none" }}, (K[i - 1][0]) / 30);
    tl.set("#card-{cid}", {{ opacity: 1 }}, 0.5 / 30);
    window.__timelines["card-{cid}"] = tl;
  </script>
</template>
''')
print(len(caps), 'caption groups')
