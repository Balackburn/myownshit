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
    // (review 1 of 61: the tick was a red 3D stick) flat strokes of red ink, unlit, a little wider than a pen line
    const ink = new THREE.MeshBasicMaterial({ color: '#D0202A', side: THREE.DoubleSide }), stroke = (L, t) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(L, t), ink); m.position.x = L / 2; return m; };
    // (review 2 of 61: it read as one slash, the first stroke of the exam's crosses) a bolder check: a longer short stroke down into the box, the
    // long stroke up out of it from the same point, thicker ink
    const a = grp(), b = grp(); a.add(stroke(h * 0.11, h * 0.032)); b.add(stroke(h * 0.23, h * 0.032));
    a.position.set(cx - h * 0.065, cy + h * 0.035, 0.004); a.rotation.z = -0.85; b.position.set(cx + h * 0.0, cy - h * 0.045, 0.004); b.rotation.z = 1.0; g.add(a, b);
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

  // A lamp shade (pivot at its rim, the shade up +Y like a hat; turn it over with rot [PI, 0, 0] to hang it): by default a drum (a truncated cone o.r
  // (0.26) wide at the rim, 0.45 of that at the top, o.h (0.24) high) with a brass ring and o.cord (0.35 m) of flex sticking up from the top, so it
  // reads as a lamp shade on a head (stills 1 of 61: the pointed cone read as a straw hat); o.cone: the pointed cone it was
  lampShade(o) {
    const r = o.r ?? 0.26, h = o.h ?? 0.24, g = grp(), m = new THREE.MeshLambertMaterial({ color: o.color || '#E8452C', side: THREE.DoubleSide });
    if (o.cone) { const c = new THREE.Mesh(new THREE.ConeGeometry(r, h, 14, 1, true), m); c.position.y = h / 2; g.add(c, at(cyl(0.035, 0.04, 0.05, '#B08A3E', 10), 0, h, 0)); return g; }
    const d = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.45, r, h, 16, 1, true), m); d.position.y = h / 2; g.add(d);
    g.add(at(cyl(r * 1.01, r * 1.01, 0.02, '#F2D7A0', 16), 0, 0.01, 0), at(cyl(r * 0.46, r * 0.46, 0.02, '#B08A3E', 14), 0, h, 0));
    if (o.cord !== 0) g.add(at(cyl(0.008, 0.008, o.cord ?? 0.35, '#2A2C31', 6, { pivot: 'bottom' }), 0, h, 0));
    return g;
  },

  // (review 1 of 61: the nest was a smooth orange dish floating over his hair) a twig nest (pivot at the bottom of its bowl, so it sits on what is
  // under it): a low brown bowl, a ragged rim of o.n (44) twigs sticking out every way, eggs (o.egg colour) that pop in one by one at the o.layAt
  // times, overshooting to 1.3 times their size, on the near half of the bowl so they show over the rim; o.r (0.4) the rim radius
  twigNest(o) {
    const R = o.r ?? 0.4, g = grp(), rnd = (i, k) => { const x = Math.sin(i * 12.9898 + k * 78.233) * 43758.5453; return x - Math.floor(x); };
    g.add(at(cyl(R * 0.95, R * 0.62, R * 0.32, '#7A5A34', 14, { pivot: 'bottom' }), 0, 0, 0), at(cyl(R * 0.78, R * 0.78, 0.01, '#4E3A22', 14), 0, R * 0.3, 0));
    const tw = ['#8A6A3E', '#6E5230', '#A07C4A', '#5C4428'];
    for (let i = 0; i < (o.n ?? 44); i++) { const a = i / (o.n ?? 44) * 2 * Math.PI + rnd(i, 1) * 0.3, L = R * (0.6 + 0.5 * rnd(i, 2)), y = R * (0.12 + 0.24 * rnd(i, 3));
      const t = box(L, 0.016, 0.016, tw[i % 4]); t.position.set(Math.cos(a) * R * 0.92, y, Math.sin(a) * R * 0.92); t.rotation.set(0, -a + (rnd(i, 4) - 0.5) * 1.6, (rnd(i, 5) - 0.3) * 0.9); g.add(t); }
    const lay = list(o.layAt), eggs = [];
    for (let i = 0; i < (o.max ?? 3); i++) { const e = new THREE.Mesh(new THREE.SphereGeometry(R * 0.17, 10, 8), new THREE.MeshLambertMaterial({ color: o.egg || '#EAF2F4' }));
      e.scale.y = 1.3; e.position.set((i - ((o.max ?? 3) - 1) / 2) * R * 0.36, R * 0.38, R * 0.3); g.add(e); eggs.push(e); }
    g.userData.update = t => eggs.forEach((e, i) => { const u = t - (lay[i] ?? 99); e.visible = u > 0; const k = u < 0.06 ? 1.3 * eo(u / 0.06) : 1 + 0.3 * Math.max(0, 1 - (u - 0.06) / 0.08); e.scale.set(k, 1.3 * k, k); });
    g.userData.update(0); return g;
  },

  // (review 1 of 61: a plank table did not say café) a round bistro table (pivot at the floor): a white marble top o.r (0.32) on a black cast-iron
  // pedestal and foot, o.h (0.74) high
  bistroTable(o) {
    const R = o.r ?? 0.32, H = o.h ?? 0.74;
    return grp(at(cyl(R, R, 0.03, o.top || '#F2F0EA', 20, { outline: 0.006 }), 0, H - 0.015, 0), at(cyl(0.028, 0.028, H - 0.03, '#26272B', 8, { pivot: 'bottom' }), 0, 0, 0),
      at(cyl(0.2, 0.22, 0.025, '#26272B', 12), 0, 0.012, 0));
  },
};
