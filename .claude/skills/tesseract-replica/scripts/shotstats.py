"""shotstats.py REF.mp4 OURS.mp4 [cut frames comma-separated]: per-shot mean L*, a*, b*, chroma and contrast of the reference vs a
render (caption band excluded). Large dL / dC per shot point at lighting or grade errors; fix the biggest first."""
import subprocess, sys, numpy as np
from skimage.color import rgb2lab
REF=sys.argv[1]
OURS=sys.argv[2]
CUTS=[int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else [0,57,103,135,196,211,229,243,313,335,386,431,483,529,584,607,648,670,707,724,766,780,864]
def frames(p):
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',p,'-vf','scale=144:256','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.uint8).reshape(-1,256,144,3)
A=frames(REF); B=frames(OURS)
mask=np.ones((256,144),bool); mask[195:225,:]=False   # caption band
print('shot   ref L    a     b    C   std  | ours L    a     b    C   std  | dL    dC')
for i in range(len(CUTS) - 1):
    f0,f1=CUTS[i],CUTS[i+1]; m=(f0+f1)//2
    sl=slice(f0+2,f1-2,3)
    def st(X):
        lab=rgb2lab(X[sl].reshape(-1,144,3)/255.0).reshape(-1,256,144,3)[:, mask]
        L,a,b=lab[...,0].mean(),lab[...,1].mean(),lab[...,2].mean(); C=np.hypot(lab[...,1],lab[...,2]).mean(); sd=lab[...,0].std()
        return L,a,b,C,sd
    r=st(A); o=st(B)
    print(f'S{i+1:<3} '+' '.join(f'{v:5.1f}' for v in r)+' | '+' '.join(f'{v:5.1f}' for v in o)+f' | {o[0]-r[0]:5.1f} {o[3]-r[3]:5.1f}')
