"""dsheet.py DIR "t,t,..." OUT.jpg [cols] [tileW]: a contact sheet of the stills s_000.. in DIR (in the order of the times), each tile labelled"""
import cv2, sys, os, numpy as np
D, T, O = sys.argv[1:4]; cols = int(sys.argv[4]) if len(sys.argv) > 4 else 5; tw = int(sys.argv[5]) if len(sys.argv) > 5 else 216
ts = T.split(','); tiles = []
for i, t in enumerate(ts):
    f = f'{D}/s_{i:03d}.jpg'; im = cv2.imread(f)
    if im is None: im = np.zeros((tw * 16 // 9, tw, 3), np.uint8)
    im = cv2.resize(im, (tw, tw * 16 // 9), interpolation=cv2.INTER_AREA)
    for k in (0.77, 0.83): cv2.line(im, (0, int(im.shape[0] * k)), (tw, int(im.shape[0] * k)), (255, 0, 255), 1)
    cv2.putText(im, f'{i}:{t}', (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 3); cv2.putText(im, f'{i}:{t}', (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
    tiles.append(im)
while len(tiles) % cols: tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[r * cols:(r + 1) * cols]) for r in range(len(tiles) // cols)]
cv2.imwrite(O, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 88]); print(O, len(ts), 'tiles')
