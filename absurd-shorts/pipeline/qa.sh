#!/bin/bash
# qa.sh STORY NUM: checks of the final render: streams and size, loudness (target -16 LUFS), HyperFrames check summary, contact sheet
# ($PIPE/s7/STORY/final.jpg, one frame per shot at 62 %).
source "$(dirname "${BASH_SOURCE[0]}")/env.sh"
S=$1; N=$2; P=$REPO/hyperframes/$N-$S; O=$PIPE/s7/$S; mkdir -p $O
ffprobe -v error -show_entries stream=codec_type,width,height -show_entries format=duration -of compact $P/renders/$S.mp4 | tr '\n' ' '; echo
ffmpeg -nostats -hide_banner -i $P/renders/$S.mp4 -vn -af ebur128=peak=true -f null - 2>&1 | grep -A14 Summary | grep -E " I:| Peak:" | tr -s ' ' | tr '\n' ' '; echo
python3 -c "
import json; d=json.load(open('$O/check.json'))
print({k: (d.get(k,{}).get('errorCount'), d.get(k,{}).get('warningCount')) for k in ['lint','runtime','layout','motion','contrast','craft','audio']})
" 2>/dev/null
python3 - <<PY
import cv2, json, numpy as np
d=json.load(open('$ROOT/scripts-fr/story_$S.json')); c=cv2.VideoCapture('$P/renders/$S.mp4'); ims=[]
for s in d['scenes']:
    c.set(cv2.CAP_PROP_POS_FRAMES, int((s['start']+s['duration']*0.62)*30)); ok,im=c.read()
    im=cv2.resize(im,(180,320)); cv2.putText(im,s['id'],(4,16),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2); ims.append(im)
while len(ims)%8: ims.append(np.zeros_like(ims[0]))
cv2.imwrite('$O/final.jpg', np.vstack([np.hstack(ims[j:j+8]) for j in range(0,len(ims),8)]))
PY
