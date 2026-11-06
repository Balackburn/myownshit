# narration for the 7 stories: one ElevenLabs request per line (neighbour context), narrator vs quote settings; skips lines already made
import json, os, sys, re
sys.path.insert(0, '/home/user/myownshit/absurd-shorts/tools'); sys.path.insert(0, '/home/user/myownshit/absurd-shorts/scripts-fr')
import audio3 as A3
from actu_common import VOICE
say = lambda t: re.sub(r'[«»]', '', t).strip()
spoken = lambda l: say(l.get('say', l['text']))   # optional 'say': what the voice reads (e.g. « cent kilos. » for the caption « 100 kilos. »), same word count
for story in sys.argv[1:]:
    L = json.load(open(f'{story}/lines.json')); os.makedirs(f'/tmp/claude-0/-home-user-myownshit/55de8c21-9e41-5895-8198-7b13ed3b7877/scratchpad/s7/{story}/tts', exist_ok=True)
    for i, l in enumerate(L):
        p = f"/tmp/claude-0/-home-user-myownshit/55de8c21-9e41-5895-8198-7b13ed3b7877/scratchpad/s7/{story}/tts/{l['id']}"
        if os.path.exists(p + '.json'): continue
        prev = ' '.join(spoken(x) for x in L[max(0, i - 2):i]); nxt = spoken(L[i + 1]) if i + 1 < len(L) else ''
        data, al = A3.tts_ts(spoken(l), VOICE, VOICE['character'] if l['who'] == 'C' else VOICE['narrator'], prev, nxt)
        open(p + '.mp3', 'wb').write(data); json.dump(al, open(p + '.json', 'w'))
    print(story, 'done', flush=True)
