"""proj.py: where world points land in a 9:16 frame for a camera (pos, target, vertical FOV)."""
import numpy as np, sys, json
def proj(C, T, lens, pts, aspect=0.5625):
    C, T = np.array(C, float), np.array(T, float); f = T - C; f /= np.linalg.norm(f)
    r = np.cross(f, [0, 1, 0]); r /= np.linalg.norm(r); u = np.cross(r, f); t = np.tan(np.radians(lens / 2))
    out = {}
    for name, P in pts.items():
        v = np.array(P, float) - C; z = v @ f
        if z <= 0: out[name] = None; continue
        out[name] = (round(50 + 50 * (v @ r) / (z * t * aspect), 1), round(50 - 50 * (v @ u) / (z * t), 1), round(z, 2))
    return out
if __name__ == '__main__':
    a = json.loads(sys.argv[1])
    for k, v in proj(a['C'], a['T'], a['lens'], a['pts']).items(): print(f'{k:12s} x%,y%,depth = {v}')
