#!/usr/bin/env python3
"""make_project.py STORY PROJECT_DIR TITLE: HyperFrames project for a story (captions, cards, root composition, -16 LUFS mix)."""
import json, os, sys, shutil, subprocess, re
S, PROJ, TITLE = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__)); SK = '/home/user/myownshit/.claude/skills/lowpoly-story-style/scripts'
TPL = '/home/user/myownshit/hyperframes/02-vos-papiers'; SC = f'/tmp/claude-0/-home-user-myownshit/55de8c21-9e41-5895-8198-7b13ed3b7877/scratchpad/s7/{S}'
os.makedirs(f'{PROJ}/compositions', exist_ok=True); os.makedirs(f'{PROJ}/assets', exist_ok=True); os.makedirs(f'{PROJ}/tools', exist_ok=True)
for f in ['CLAUDE.md', 'AGENTS.md', 'hyperframes.json']: shutil.copy(f'{TPL}/{f}', f'{PROJ}/{f}')
name = os.path.basename(PROJ.rstrip('/'))
json.dump({'name': name, 'private': True, 'type': 'module', 'scripts': {k: f'npx --yes hyperframes@0.9.13 {k}' for k in ['check', 'render', 'publish']} | {'dev': 'npx --yes hyperframes@0.9.13 preview'}}, open(f'{PROJ}/package.json', 'w'), indent=2)
json.dump({'id': name, 'name': name, 'createdAt': '2026-11-05T17:00:00.000Z'}, open(f'{PROJ}/meta.json', 'w'), indent=2)
for f in ['timeline.json', 'lines.json', 'cues.json', 'cards.txt', 'shots.json']: shutil.copy(f'{HERE}/{S}/{f}', f'{PROJ}/tools/{f}')
cards = open(f'{HERE}/{S}/cards.txt').read().strip()
subprocess.run(['python3', f'{SK}/build_hf.py', f'{PROJ}/tools/timeline.json', PROJ, '--cards', cards], check=True)
TL = json.load(open(f'{HERE}/{S}/timeline.json')); D = TL['total']; SH = json.load(open(f'{HERE}/{S}/shots.json'))
hosts = []
for i, kv in enumerate([c for c in cards.split(',') if c]):
    sid = kv.split(':')[0]; a = round(SH[sid][0] + 0.07, 3); b = round(SH[sid][1] - 0.03, 3)
    hosts.append(f'''      <div id="host-c{i + 1}" data-composition-id="card-c{i + 1}" data-composition-src="compositions/card-c{i + 1}.html"
           data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="3" data-track-kind="graphics"
           data-width="1080" data-height="1920" style="z-index: 3"></div>''')
src = open(f'{TPL}/index.html').read(); head = src[:src.index('    <!--')]
open(f'{PROJ}/index.html', 'w').write(head + f'''    <!-- {TITLE}: a story in the tornado replica's style (.claude/skills/lowpoly-story-style). 3D layer from
         absurd-shorts/scripts-fr/story_{S}.py, the series' French narrator back to back, the tornado film's music bed and effects on the actions,
         the replica's captions and THEFT-card spring for the title cards. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
      <video id="layer3d" class="clip" src="assets/layer3d.mp4" muted playsinline
             data-start="0" data-duration="{D}" data-track-index="0"
             style="position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: contain; z-index: 1"></video>
      <audio id="soundtrack" class="clip" src="assets/audio.wav" data-start="0" data-duration="{D}" data-track-index="1" data-volume="1"></audio>
{chr(10).join(hosts)}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html"
           data-start="0" data-duration="{D}" data-track-index="2" data-track-kind="captions"
           data-width="1080" data-height="1920" style="z-index: 4"></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')
# sound: narration + the tornado bed + cues, then a gain trim to -16 LUFS
subprocess.run(['python3', f'{SK}/mix.py', f'{HERE}/{S}/timeline.json', f'{HERE}/{S}/cues.json', f'{SC}/mix', '--bed',
                '/tmp/claude-0/-home-user-myownshit/55de8c21-9e41-5895-8198-7b13ed3b7877/scratchpad/mdx/instrumental.wav', '--bed-from', '17.7', '--bed-len', '6.0'], check=True, capture_output=True)
def lufs(p):
    r = subprocess.run(['ffmpeg', '-nostats', '-hide_banner', '-i', p, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])
g = -16.0 - lufs(f'{SC}/mix/mix.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{SC}/mix/mix.wav', '-af', f'volume={g:.2f}dB,alimiter=limit=0.84:level=false', f'{PROJ}/assets/audio.wav'], check=True)
open(f'{PROJ}/README.md', 'w').write(f'# {name}: {TITLE}\n\nA story in the tornado replica\'s style, made in one pass with `.claude/skills/lowpoly-story-style`.\n'
    f'Script: `tools/lines.json`; narration timeline: `tools/timeline.json`; 3D layer: `absurd-shorts/scripts-fr/story_{S}.py`;\n'
    f'cards: `tools/cards.txt`; effect cues: `tools/cues.json`. Render: `npx --yes hyperframes@0.9.13 render -o renders/{S}.mp4 --fps 30`.\n')
print('project ready', PROJ, 'mix', round(lufs(f'{PROJ}/assets/audio.wav'), 1), 'LUFS')
