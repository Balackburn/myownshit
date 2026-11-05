# French narration: one ElevenLabs request per line (with neighbour context), real word timings from /with-timestamps
import json, os, sys
sys.path.insert(0, '/home/user/myownshit/absurd-shorts/tools'); sys.path.insert(0, '/home/user/myownshit/absurd-shorts/scripts-fr')
import audio3 as A3
from actu_common import VOICE
L = json.load(open('lines_fr.json')); out = []
for i, l in enumerate(L):
    prev = ' '.join(x['text'] for x in L[max(0, i - 2):i]); nxt = L[i + 1]['text'] if i + 1 < len(L) else ''
    mp3p = f"{l['id']}.mp3"
    if not os.path.exists(mp3p) or not os.path.exists(l['id'] + '.json'):
        data, al = A3.tts_ts(l['text'], VOICE, VOICE['narrator'], prev, nxt)
        open(mp3p, 'wb').write(data); json.dump(al, open(l['id'] + '.json', 'w'))
    al = json.load(open(l['id'] + '.json'))
    words = A3.words_from_alignment(l['text'], al)
    dur = float(os.popen(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {mp3p}").read())
    out.append({**l, 'words': words, 'dur': dur})
    print(f"{l['id']} {dur:.2f}s  slot {l['slot'] - l['at']:.2f}s  last word end {words[-1]['e']:.2f}  {'OVER' if l['at'] + words[-1]['e'] > l['slot'] else ''}")
json.dump(out, open('timed_fr.json', 'w'), ensure_ascii=False, indent=1)
