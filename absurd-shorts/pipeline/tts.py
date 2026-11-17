# tts.py STORY...: narration of a story (pipeline copy of stories7/tts_all.py): one ElevenLabs request per line (neighbour context), narrator vs
# quote settings; skips lines already made. Reads stories7/STORY/lines.json, writes $PIPE/s7/STORY/tts/Lnn.mp3 + .json (word timings).
# Run with ELEVENLABS_API_KEY=proxy-injected (the network proxy injects the real key); filter the log with  | grep -v -i voice
import json, os, sys, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PIPE = os.environ.get('PIPE', '/tmp/pipe')
sys.path.insert(0, f'{ROOT}/tools'); sys.path.insert(0, f'{ROOT}/scripts-fr')
import audio3 as A3
from actu_common import VOICE
say = lambda t: re.sub(r'[«»]', '', t).strip()
spoken = lambda l: say(l.get('say', l['text']))   # optional 'say': what the voice reads (e.g. « cent kilos. » for the caption « 100 kilos. »), same word count
for story in sys.argv[1:]:
    L = json.load(open(f'{ROOT}/stories7/{story}/lines.json')); os.makedirs(f'{PIPE}/s7/{story}/tts', exist_ok=True)
    for i, l in enumerate(L):
        p = f"{PIPE}/s7/{story}/tts/{l['id']}"
        if os.path.exists(p + '.json'): continue
        prev = ' '.join(spoken(x) for x in L[max(0, i - 2):i]); nxt = spoken(L[i + 1]) if i + 1 < len(L) else ''
        data, al = A3.tts_ts(spoken(l), VOICE, VOICE['character'] if l['who'] == 'C' else VOICE['narrator'], prev, nxt)
        open(p + '.mp3', 'wb').write(data); json.dump(al, open(p + '.json', 'w'))
    print(story, 'done', flush=True)
