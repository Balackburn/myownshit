// « La gomme à mâcher » (story 51, cycle 13): a man stepped on a piece of chewing gum three weeks ago; since then it stretches behind him, a pink
// strand across Paris; the town hall listed it as a communal road; on Sundays the children skip with it; the city hung a cable car on it; yesterday
// he pulled hard to get rid of it, and the strand slung him back home in a second; since then he works from home. The strand itself is a scene
// tether (director3: sag keys, wobble, taper, thin, spin); these are the props around it. Conventions as in props.js (metres, front +Z, pivot at the
// floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { PALETTE as P, mat, box, cyl } from './style.js';
import { grp, at, label } from './props.js';

const PI = Math.PI;
const rnd = s => { let x = Math.sin(s * 127.1) * 43758.5453; return x - Math.floor(x); };
const wob = (u, f, d) => u < 0 ? 0 : Math.exp(-u * d) * Math.sin(u * f);
const keyAt = (ks, t, d) => { if (!ks || !ks.length) return d; if (t <= ks[0][0]) return ks[0][1]; for (let i = 1; i < ks.length; i++) if (t < ks[i][0]) { const [t0, v0] = ks[i - 1], [t1, v1] = ks[i], u = (t - t0) / Math.max(1e-6, t1 - t0); return v0 + (v1 - v0) * u * u * (3 - 2 * u); } return ks[ks.length - 1][1]; };
const GUM = '#F27BAA';

export const GOMME_PROPS = {
  // A blob of chewing gum on the pavement (pivot at the ground, its middle): a flattened lumpy ball. o.r (0.1 m), o.color, o.squelch: [[t, k], ...]
  // a step on it (k 1: flattened under the shoe, then it springs back with a wobble), o.pull: [[t, k], ...] a strand pulled up from it (a peak rising).
  gumBlob(o) {
    const r = o.r ?? 0.1, g = grp(), C = o.color || GUM;
    const geo = new THREE.IcosahedronGeometry(r, 1), pa = geo.attributes.position;
    for (let i = 0; i < pa.count; i++) { const x = pa.getX(i), y = pa.getY(i), z = pa.getZ(i), k = 0.85 + 0.3 * rnd(Math.round((x + 2) * 97 + (y + 2) * 31 + (z + 2) * 13)); pa.setXYZ(i, x * k, Math.max(-0.2 * r, y * k * 0.45), z * k); }
    geo.computeVertexNormals();
    const body = new THREE.Mesh(geo, mat(C, { unique: true })); body.castShadow = body.receiveShadow = true; body.position.y = 0.2 * r;
    const peak = new THREE.Mesh(new THREE.ConeGeometry(r * 0.45, r * 1.6, 7), mat(C)); peak.position.y = 0.2 * r; peak.castShadow = true;
    const shine = at(new THREE.Mesh(new THREE.SphereGeometry(r * 0.18, 6, 4), mat('#FFD2E4')), -0.3 * r, 0.42 * r, 0.25 * r);
    g.add(body, peak, shine);
    g.userData.update = t => {
      let sq = 0; for (const [t0, k] of o.squelch || []) { const u = t - t0; if (u >= 0 && u < 0.05) sq = Math.max(sq, k * u / 0.05); else if (u >= 0.05) sq = Math.max(sq, k * Math.max(0, wob(u - 0.05 + 0.06, 18, 6) * 0.7 + Math.exp(-(u - 0.05) * 14))); }
      const sy = 1 - 0.65 * Math.min(1, sq), sx = 1 + 0.5 * Math.min(1, sq); body.scale.set(sx, sy, sx); shine.position.y = 0.42 * r * sy;
      const pk = keyAt(o.pull, t, 0); peak.visible = pk > 0.02; peak.scale.set(1, Math.max(0.01, pk), 1); peak.position.y = 0.2 * r + 0.8 * r * pk;
    };
    g.userData.update(0); return g;
  },

  // A Paris street-name plate: blue enamel, a green rim, white capitals (o.lines: ['VOIRIE', 'COMMUNALE']), o.sub: a small line on top (an
  // arrondissement); o.w (0.9), o.h (0.5); o.post (m, 0): on a post that high (pivot at its foot), else the plate's middle is the pivot (for a wall).
  // o.screw: [[t, k]] the plate swinging on its last screw (k: amplitude, rad, dying out); o.drop: t, it slips down a little on the strand.
  streetPlaque(o) {
    const w = o.w ?? 0.9, h = o.h ?? 0.5, g = grp(), plate = grp(), lines = o.lines || ['VOIRIE', 'COMMUNALE'];
    const c = document.createElement('canvas'); c.width = 512; c.height = Math.round(512 * h / w); const x = c.getContext('2d');
    x.fillStyle = '#1D3F8A'; x.fillRect(0, 0, c.width, c.height);
    x.strokeStyle = '#2E8A4E'; x.lineWidth = c.width * 0.035; x.strokeRect(c.width * 0.03, c.width * 0.03, c.width * 0.94, c.height - c.width * 0.06);
    x.strokeStyle = '#F4F2EA'; x.lineWidth = c.width * 0.008; x.strokeRect(c.width * 0.065, c.width * 0.065, c.width * 0.87, c.height - c.width * 0.13);
    x.fillStyle = '#F4F2EA'; x.textAlign = 'center'; x.textBaseline = 'middle';
    const top = o.sub ? 0.24 : 0.12, n = lines.length, lh = (c.height * (0.88 - top)) / n;
    if (o.sub) { x.font = `600 ${Math.round(c.height * 0.12)}px Poppins, Arial, sans-serif`; x.fillText(o.sub, c.width / 2, c.height * 0.17); }
    for (let i = 0; i < n; i++) { let fs = Math.round(lh * 0.78); x.font = `700 ${fs}px Poppins, Arial, sans-serif`; while (x.measureText(lines[i]).width > c.width * 0.82 && fs > 10) { fs -= 2; x.font = `700 ${fs}px Poppins, Arial, sans-serif`; } x.fillText(lines[i], c.width / 2, c.height * top + lh * (i + 0.5)); }
    const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
    const face = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshLambertMaterial({ map: tex })); face.position.z = 0.012;
    plate.add(at(box(w + 0.02, h + 0.02, 0.02, '#163370', { outline: 0.006 }), 0, 0, 0), face);
    const post = o.post || 0;
    if (post) { g.add(at(cyl(0.035, 0.035, post, '#3A4A40', 8, { pivot: 'bottom' }), 0, 0, -0.04)); plate.position.set(0, post - h / 2 - 0.05, 0); }
    g.add(plate);
    g.userData.update = t => { let a = 0; for (const [t0, k] of o.screw || []) a += k * wob(t - t0, 9, 2.2); plate.rotation.z = a; };
    g.userData.update(0); return g;
  },

  // A small cable-car cabin hanging from its grip (the pivot is the grip, on the cord; the cabin hangs below): o.color ('#C8302A'), o.text (side
  // band, 'TÉLÉPHÉRIQUE'), o.riders (3: heads in the windows), o.drop (2.1 m from the grip to the cabin's roof... total height below the grip),
  // o.swing: [[t, amp (rad)], ...] the cabin swinging on its arm and dying out; o.tilt: a lasting lean (rad, the cord's slope).
  cableCar(o) {
    const C = o.color || '#C8302A', W = o.w ?? 1.5, H = o.h ?? 1.35, D = o.d ?? 1.15, arm = o.arm ?? 0.85, g = grp(), hang = grp();
    // the grip on the cord: two wheels in a housing
    g.add(at(box(0.36, 0.16, 0.2, '#3B3F46', { outline: 0.006 }), 0, 0.02, 0));
    for (const sx of [-0.1, 0.1]) g.add(at(cyl(0.06, 0.06, 0.05, '#23262B', 10), sx, 0.06, 0, PI / 2, 0, 0));
    // the arm and the cabin, hanging from the grip
    hang.add(at(cyl(0.035, 0.035, arm, '#4A4E55', 8), 0, -arm / 2, 0), at(box(0.5, 0.06, 0.06, '#4A4E55'), 0, -arm, 0));
    const cab = grp(); cab.position.y = -arm - 0.05;
    cab.add(at(box(W, 0.12, D, '#2B2E33', { outline: 0.008 }), 0, -0.06, 0));                                           // the roof
    cab.add(at(box(W, H * 0.42, D, C, { outline: 0.008 }), 0, -0.12 - H * 0.21, 0));                                     // the glazing belt (windows drawn on it)
    cab.add(at(box(W, H * 0.46, D, C, { outline: 0.008 }), 0, -0.12 - H * 0.42 - H * 0.23, 0));                           // the lower body
    const glass = '#2F4A5C', winY = -0.12 - H * 0.21;
    // (pass 2 of 51) o.glassOpacity: see-through windows (opaque, they hid the riders: the review saw an empty cabin)
    const gm = o.glassOpacity != null ? new THREE.MeshLambertMaterial({ color: '#9FC3D6', transparent: true, opacity: o.glassOpacity, depthWrite: false }) : null;
    const pane = (w, h, d) => gm ? new THREE.Mesh(new THREE.BoxGeometry(w, h, d), gm) : box(w, h, d, glass);
    for (const sz of [-1, 1]) { const n = 3; for (let i = 0; i < n; i++) cab.add(at(pane(W / n - 0.12, H * 0.34, 0.012), -W / 2 + (i + 0.5) * W / n, winY, sz * (D / 2 + 0.006))); }
    for (const sx of [-1, 1]) cab.add(at(pane(0.012, H * 0.34, D - 0.16), sx * (W / 2 + 0.006), winY, 0));
    cab.add(at(box(W + 0.01, 0.07, D + 0.01, '#F4F2EA'), 0, -0.12 - H * 0.44, 0));                                        // a white band
    if (o.text !== '') cab.add(at(label(o.text || 'TÉLÉPHÉRIQUE', W * 0.8, 0.13, { bg: null, fg: '#F4F2EA', wrap: false }), 0, -0.12 - H * 0.62, D / 2 + 0.012));
    const riders = o.riders ?? 3, skins = ['#E2B48A', '#C98B5E', '#F0C9A0', '#8D5A3B'], hairs = ['#2B2118', '#5A3A22', '#D9C27A', '#1B1B1E'];
    const hs = o.riderScale ?? 1;   // (pass 2 of 51) o.riderScale: bigger heads, with eyes, leaning out toward the camera side (o.lean, m)
    for (let i = 0; i < riders; i++) { const xx = -W / 2 + (i + 0.5) * W / riders, hh = grp(at(box(0.2, 0.24, 0.2, skins[i % 4]), 0, 0, 0), at(box(0.21, 0.07, 0.21, hairs[(i + 1) % 4]), 0, 0.13, 0));
      if (o.riderScale) for (const ex of [-0.045, 0.045]) hh.add(at(box(0.035, 0.05, 0.01, '#1B1B1E'), ex, 0.02, 0.102));
      hh.scale.setScalar(hs); hh.position.set(xx, winY - 0.02 + (hs - 1) * 0.08, D / 2 - 0.18 + (o.lean || 0)); cab.add(hh); }
    hang.add(cab); g.add(hang);
    g.userData.update = t => { let a = o.tilt || 0; for (const [t0, k] of o.swing || []) a += k * wob(t - t0, 4.2, 1.1); hang.rotation.z = a; };
    g.userData.update(0); return g;
  },
};
