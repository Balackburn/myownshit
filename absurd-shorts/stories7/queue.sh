#!/bin/bash
# queue.sh: render the stories in order as they are marked ready (stories7/<s>/READY): 3D layer -> project -> HyperFrames render
cd /home/user/myownshit/absurd-shorts
SC=/tmp/claude-0/-home-user-myownshit/55de8c21-9e41-5895-8198-7b13ed3b7877/scratchpad/s7
declare -A NUM=([sable]=10 [lune]=11 [sapin]=12 [escargot]=13 [greve]=14 [colis]=15 [heure]=16)
declare -A TITLE=([sable]="Le sable" [lune]="La Lune" [sapin]="Le sapin" [escargot]="L'escargot" [greve]="La grève des nuages" [colis]="L'avis de passage" [heure]="Le changement d'heure")
for S in sable lune sapin escargot greve colis heure; do
  until [ -f stories7/$S/READY ]; do sleep 15; done
  cp scripts-fr/story_$S.json scripts-fr/story_${S}_render.json
  node render/render3.mjs scripts-fr/story_${S}_render.json --timed --w 1080 --h 1920 --workers 4 --out out/story_${S}_3d.mp4 > $SC/$S/render.log 2>&1 || { echo "$S 3D FAILED" >> $SC/queue.log; continue; }
  P=/home/user/myownshit/hyperframes/${NUM[$S]}-$S
  python3 stories7/make_project.py $S $P "${TITLE[$S]}" >> $SC/queue.log 2>&1 || { echo "$S PROJECT FAILED" >> $SC/queue.log; continue; }
  cp out/story_${S}_3d.mp4 $P/assets/layer3d.mp4
  (cd $P && export NODE_USE_ENV_PROXY=1 NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt && npx --yes hyperframes@0.9.13 check --json > $SC/$S/check.json 2>/dev/null; mkdir -p renders && npx --yes hyperframes@0.9.13 render -o renders/$S.mp4 --fps 30 > $SC/$S/hf.log 2>&1) && echo "$S DONE $P/renders/$S.mp4" >> $SC/queue.log || echo "$S HF FAILED" >> $SC/queue.log
done
echo "QUEUE FINISHED" >> $SC/queue.log
