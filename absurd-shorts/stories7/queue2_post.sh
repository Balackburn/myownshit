#!/bin/bash
# queue2_post.sh: project + HyperFrames render only (see queue2.sh)
cd /home/user/myownshit/absurd-shorts
SC=/tmp/claude-0/-home-user-myownshit/55de8c21-9e41-5895-8198-7b13ed3b7877/scratchpad/s7
declare -A NUM=([sable]=10 [lune]=11 [sapin]=12 [escargot]=13 [greve]=14 [colis]=15 [heure]=16 [police]=17 [burger]=18 [loto]=19 [independance]=20 [velo]=21 [caillou]=22 [rdv]=23 [balance]=24 [sosie]=25 [teletravail]=26 [gps]=27 [aspirateur]=28 [serrurier]=29 [armoire]=30 [parapluie]=31 [attente]=32)
declare -A TITLE=([sable]="Le sable" [lune]="La Lune" [sapin]="Le sapin" [escargot]="L'escargot" [greve]="La grève des nuages" [colis]="L'avis de passage" [heure]="Le changement d'heure" [police]="La police contre la police" [burger]="Le burger vegan" [loto]="Le loto" [independance]="L'indépendance" [velo]="Le vélo" [caillou]="Le caillou" [rdv]="Le rendez-vous" [sosie]="Le sosie" [balance]="La balance" [teletravail]="Le télétravail" [gps]="Le GPS" [aspirateur]="L'aspirateur" [serrurier]="Le serrurier" [armoire]="L'armoire" [parapluie]="Le parapluie" [attente]="La file d'attente")
# queue2_post.sh STORY...: the steps after the 3D layer (project -> HyperFrames render), when out/story_X_3d.mp4 is already good
for S in "$@"; do
  P=/home/user/myownshit/hyperframes/${NUM[$S]}-$S
  python3 stories7/make_project.py $S $P "${TITLE[$S]}" >> $SC/queue2.log 2>&1 || { echo "$S post PROJECT FAILED" >> $SC/queue.log; continue; }
  cp out/story_${S}_3d.mp4 $P/assets/layer3d.mp4
  (cd $P && export NODE_USE_ENV_PROXY=1 NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt && npx --yes hyperframes@0.9.13 check --json > $SC/$S/check.json 2>/dev/null; mkdir -p renders && npx --yes hyperframes@0.9.13 render -o renders/$S.mp4 --fps 30 > $SC/$S/hf2.log 2>&1) && echo "$S v2 DONE $P/renders/$S.mp4" >> $SC/queue.log || echo "$S v2 HF FAILED" >> $SC/queue.log
done
echo "QUEUE2 POST FINISHED" >> $SC/queue.log
