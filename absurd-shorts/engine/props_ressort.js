// « Le ressort » (story 61, cycle 23): a man sat on a spring. He bounced up to the roof. Since then he bounces everywhere. The town hall declared him
// a flying object. He must pass the pilot's licence. He failed it three times. Yesterday he stopped bouncing. In mid-flight. The pigeons built their
// nest on his head. Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot
// time.
import * as THREE from 'three';
import { mat, box, cyl } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const list = v => [].concat(v ?? []);
const clamp01 = x => Math.max(0, Math.min(1, x));
const eo = x => 1 - Math.pow(1 - clamp01(x), 3);

export const RESSORT_PROPS = {
  // A coiled spring bursting out of a seat (pivot at the seat's surface, it grows up +Y): at o.at it pops up to o.len (0.5) overshooting to 1.4 times
  // in 0.05 s, then boings, its length vibrating and its top swaying, dying away over o.decay (0.9 s); o.turns (6) coils of o.r (0.075) round o.wire
  // (0.014) steel; a torn flap of the seat's cloth (o.cloth) bent back round its foot (o.flap false: none). Before o.at only the flap shows.
  springCoil(o) {
    const L = o.len ?? 0.5, R = o.r ?? 0.075, n = o.turns ?? 6, wr = o.wire ?? 0.014, D = o.decay ?? 0.9, g = grp(), sp = grp(); g.add(sp);
    class Helix extends THREE.Curve { getPoint(u, tgt = new THREE.Vector3()) { return tgt.set(R * Math.cos(u * n * TAU), u, R * Math.sin(u * n * TAU)); } }
    sp.add(new THREE.Mesh(new THREE.TubeGeometry(new Helix(), n * 24, wr, 6, false), mat(o.color || '#AEB6C0')));
    if (o.flap !== false) g.add(at(box(0.22, 0.012, 0.15, o.cloth || '#8A6A45'), 0.06, 0.012, 0.03, 0.55, 0.3, 0.25));
    g.userData.update = t => {
      const u = t - (o.at ?? 0);
      if (u < 0) { sp.visible = false; return; }
      sp.visible = true;
      const k = u < 0.05 ? 1.4 * eo(u / 0.05) : 1 + 0.4 * Math.exp(-3 * (u - 0.05) / D) * Math.cos((u - 0.05) * 30);
      sp.scale.set(1, Math.max(0.04, L * k), 1);
      const sw = 0.35 * Math.exp(-2.5 * u / D) * Math.sin(u * 19);
      sp.rotation.set(0.4 * sw, 0, sw);
    };
    g.userData.update(0); return g;
  },

  // A registration sticker (pivot at its centre, face +Z): a white label with a navy frame, o.text (« F-MEC ») in navy and a red stripe; o.w (0.3) wide
  regSticker(o) {
    const w = o.w ?? 0.3, h = w * 0.42;
    return grp(canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#FFFFFF'; c.fillRect(0, 0, W, H); c.fillStyle = '#C8202A'; c.fillRect(0, H * 0.8, W, H * 0.1);
      c.strokeStyle = '#1B2A4A'; c.lineWidth = W * 0.02; c.strokeRect(W * 0.02, H * 0.04, W * 0.96, H * 0.92);
      c.fillStyle = '#1B2A4A'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${Math.round(H * 0.5)}px Arial`; c.fillText(o.text ?? 'F-MEC', W / 2, H * 0.44); }, { res: 256 }));
  },

  // A form on the counter (pivot at its centre, face +Z; lay it flat with rot [-PI / 2, 0, 0]): o.title (« DÉCLARATION ») and three boxes, o.items
  // (OISEAU / AVION / OBJET VOLANT); a red tick strikes into box o.pick (2) at o.tickAt, in two strokes over 0.12 s; o.w (0.42) wide
  formCheck(o) {
    const w = o.w ?? 0.42, h = w * 1.3, items = o.items || ['OISEAU', 'AVION', 'OBJET VOLANT'], g = grp();
    g.add(canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#F7F3E8'; c.fillRect(0, 0, W, H); c.fillStyle = '#1B2A4A'; c.textAlign = 'left'; c.textBaseline = 'middle';
      c.font = `900 ${Math.round(H * 0.075)}px Arial`; c.fillText(o.title ?? 'DÉCLARATION', W * 0.08, H * 0.1); c.fillRect(W * 0.08, H * 0.16, W * 0.84, H * 0.008);
      items.forEach((it, i) => { const y = H * (0.34 + i * 0.22); c.lineWidth = W * 0.014; c.strokeStyle = '#1B2A4A'; c.strokeRect(W * 0.08, y - H * 0.055, H * 0.11, H * 0.11);
        c.font = `900 ${Math.round(H * (it.length > 8 ? 0.062 : 0.075))}px Arial`; c.fillText(it, W * 0.08 + H * 0.16, y); }); }, { res: 512 }));
    const pick = o.pick ?? 2, cx = -w / 2 + w * 0.08 + h * 0.055, cy = h / 2 - h * (0.34 + pick * 0.22);
    const a = grp(), b = grp(); a.add(at(box(h * 0.075, 0.012, 0.004, '#D0202A'), h * 0.0375, 0, 0)); b.add(at(box(h * 0.16, 0.012, 0.004, '#D0202A'), h * 0.08, 0, 0));
    a.position.set(cx - h * 0.04, cy + h * 0.005, 0.004); a.rotation.z = -0.8; b.position.set(cx + h * 0.012, cy - h * 0.045, 0.004); b.rotation.z = 0.95; g.add(a, b);
    g.userData.update = t => { const u = t - (o.tickAt ?? 99); a.scale.x = Math.max(0.001, eo(u / 0.05)); b.scale.x = Math.max(0.001, eo((u - 0.05) / 0.07)); a.visible = u > 0; b.visible = u > 0.05; };
    g.userData.update(0); return g;
  },

  // The examiner's clipboard (pivot at its centre, face +Z): o.title (« EXAMEN DE PILOTE »), three lines ESSAI 1 / 2 / 3, and a big red cross that
  // slashes across each line at the o.marks times (two strokes over 0.1 s); o.w (0.3) wide
  clipboardX(o) {
    const w = o.w ?? 0.3, h = w * 1.35, g = grp();
    g.add(at(box(w * 1.08, h * 1.06, 0.012, '#8A6A45'), 0, 0, -0.008), at(box(w * 0.4, h * 0.07, 0.03, '#9A9CA2'), 0, h * 0.5, 0.004));
    g.add(at(canvasPlane(w, h * 0.92, (c, W, H) => { c.fillStyle = '#FBF8EF'; c.fillRect(0, 0, W, H); c.fillStyle = '#1B2A4A'; c.textAlign = 'center'; c.textBaseline = 'middle';
      c.font = `900 ${Math.round(H * 0.07)}px Arial`; c.fillText(o.title ?? 'EXAMEN DE PILOTE', W / 2, H * 0.1); c.textAlign = 'left';
      for (let i = 0; i < 3; i++) { const y = H * (0.34 + i * 0.24); c.font = `700 ${Math.round(H * 0.075)}px Arial`; c.fillText(`ESSAI ${i + 1}`, W * 0.08, y); c.fillRect(W * 0.08, y + H * 0.07, W * 0.84, H * 0.006); } }, { res: 512 }), 0, -h * 0.02, 0.002));
    const marks = list(o.marks), X = [];
    for (let i = 0; i < 3; i++) { const y = h * 0.46 - h * 0.92 * (0.34 + i * 0.24) - h * 0.02, x = w * 0.28, s = h * 0.17;
      const p = grp(), q = grp(); p.add(at(box(s, 0.016, 0.004, '#D0202A'), 0, 0, 0)); q.add(at(box(s, 0.016, 0.004, '#D0202A'), 0, 0, 0));
      p.position.set(x, y, 0.006); p.rotation.z = 0.8; q.position.set(x, y, 0.007); q.rotation.z = -0.8; g.add(p, q); X.push([p, q]); }
    g.userData.update = t => X.forEach(([p, q], i) => { const u = t - (marks[i] ?? 99); p.visible = u > 0; q.visible = u > 0.05; p.scale.x = Math.max(0.001, eo(u / 0.05)); q.scale.x = Math.max(0.001, eo((u - 0.05) / 0.05)); });
    g.userData.update(0); return g;
  },

  // A lamp shade (pivot at its rim, the cone up +Y like a hat; turn it over with rot [PI, 0, 0] to hang it): an open red cone o.r (0.24) wide at the rim,
  // o.h (0.22) high, a little brass cap on top
  lampShade(o) {
    const r = o.r ?? 0.24, h = o.h ?? 0.22, g = grp();
    const c = new THREE.Mesh(new THREE.ConeGeometry(r, h, 14, 1, true), new THREE.MeshLambertMaterial({ color: o.color || '#E8452C', side: THREE.DoubleSide })); c.position.y = h / 2; g.add(c);
    g.add(at(cyl(0.035, 0.04, 0.05, '#B08A3E', 10), 0, h, 0));
    return g;
  },
};
