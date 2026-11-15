#!/bin/bash
# critic_final_stills.sh STORY OUTDIR "name:t,name:t,..." [cardNames]: 576x1024 stills in the final look, magenta lines at the caption band (77 and 83 %), cyan lines at the
# title card band (7 and 18 %) on the names listed in cardNames (comma separated)
S=$1; C=$2; L=$3; CARD=${4:-}
cd /home/user/myownshit/absurd-shorts
T=$(echo "$L" | tr ',' '\n' | cut -d: -f2 | paste -sd,)
node render/render3.mjs scripts-fr/story_$S.json --timed --w 576 --h 1024 --stills "$T" > $C/final_stills.log 2>&1 || { echo render failed; tail -3 $C/final_stills.log; exit 1; }
python3 - "$S" "$C" "$L" "$CARD" <<'PY'
import cv2, sys
S, C, L, CARD = sys.argv[1:5]; card = set(CARD.split(',')) if CARD else set()
for i, x in enumerate(L.split(',')):
    nm, t = x.split(':'); im = cv2.imread(f'out/work/story_{S}/stills/s_{i:03d}.jpg'); h, w = im.shape[:2]
    for f in (0.77, 0.83): cv2.line(im, (0, int(h * f)), (w, int(h * f)), (255, 0, 255), 1)
    if nm in card:
        for f in (0.07, 0.18): cv2.line(im, (0, int(h * f)), (w, int(h * f)), (255, 255, 0), 1)
    cv2.imwrite(f'{C}/frame_{nm}.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, 92])
print(len(L.split(',')), 'stills')
PY
