"""solve_cam.py: solve a camera (height Hc, horizontal distance D to a subject axis, pitch p, optional subject scale s) from screen
measurements of one reference frame: the subject's top-centre row (vr), base row (vb), apparent top width (w) and, optionally, the depth
of the base from a known-size neighbour (zb, e.g. a house of known width). Edit M and the model constants (Hr, Rr) for your subject.
Solve several frames of one shot, then interpolate the camera between them."""
import numpy as np
from scipy.optimize import least_squares
F = 512 / np.tan(np.radians(25))          # lens 50 (vertical fov 50 deg) -> focal in px
def proj(Hc, D, p, h, horiz):              # point at height h, 'horiz' metres in front of the camera (horizontally) -> (v, depth)
    dy, dz = h - Hc, horiz
    fz = -np.sin(p) * dy + np.cos(p) * dz  # depth along the view axis (forward = (0,-sin p, cos p) in (y, z_forward) coords)
    uy = np.cos(p) * dy + np.sin(p) * dz   # up component
    return 512 - F * uy / fz, fz
def residual(x, m, s=None):
    Hc, D, p = x[0], x[1], x[2]; sc = s if s is not None else x[3]
    Hr, Rr = 7.8 * sc, 3.3 * sc
    vr, zr = proj(Hc, D, p, Hr, D); vb, zb = proj(Hc, D, p, 0.0, D)
    w = 2 * Rr * F / zr
    res = [(vr - m['vr']) / 8, (vb - m['vb']) / 8, (w - m['w']) / 15]
    if 'zb' in m: res.append((zb - m['zb']) / 20)
    return res
M = {270: dict(vr=222, vb=438, w=248, zb=260), 312: dict(vr=173, vb=495, w=450, zb=220), 342: dict(vr=239, vb=426, w=208, zb=275), 384: dict(vr=175, vb=501, w=484, zb=198)}
for f, m in M.items():
    r = least_squares(residual, [250, 200, np.radians(50), 9], args=(m,), bounds=([20, 20, np.radians(10), 2], [2000, 2000, np.radians(85), 40]))
    Hc, D, p, s = r.x; print(f, 'free s: Hc %.0f D %.0f pitch %.1f s %.2f cost %.3f' % (Hc, D, np.degrees(p), s, r.cost))
S = 9.0
for f, m in M.items():
    r = least_squares(residual, [250, 200, np.radians(50)], args=(m, S), bounds=([20, 20, np.radians(10)], [2000, 2000, np.radians(85)]))
    Hc, D, p = r.x; vr, zr = proj(Hc, D, p, 7.8 * S, D); vb, zb = proj(Hc, D, p, 0, D)
    print(f, 's=%.1f: Hc %.0f D %.0f pitch %.1f | vr %.0f vb %.0f w %.0f zb %.0f' % (S, Hc, D, np.degrees(p), vr, vb, 2 * 3.3 * S * F / zr, zb))
