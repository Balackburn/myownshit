// « L'écho » (story 60, cycle 22): a man shouted in the mountains; the echo never came back; he filed a complaint; the gendarmerie put out a missing
// notice; it was reported in three valleys; yesterday the echo came home, two years late; it shouted for three days; the gendarmerie fined the man for
// the noise. Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { mat, box, cyl, addOutline } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const list = v => [].concat(v ?? []);
// a value keyed in time: [[t, v], ...] (or [[t, a, b, ...]] with n values), linear between keys, held outside them
function lin(ks, t, dflt) {
  const k = list(ks); if (!k.length) return dflt;
  const val = e => (e.length > 2 ? e.slice(1) : e[1]);
  if (t <= k[0][0]) return val(k[0]);
  for (let i = 1; i < k.length; i++) if (t < k[i][0]) { const a = k[i - 1], b = k[i], u = (t - a[0]) / Math.max(1e-6, b[0] - a[0]);
    if (a.length > 2) return a.slice(1).map((v, j) => v + (b[j + 1] - v) * u); return a[1] + (b[1] - a[1]) * u; }
  return val(k[k.length - 1]);
}
function rng(seed) { let s = seed >>> 0 || 1; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }
// an outlined letter cut out of card (front +Z): a coloured face inside a thick ink stroke over a darker back layer (the card's thickness)
function letter(ch, fill, size) {
  const draw = (g, W, H) => { g.clearRect(0, 0, W, H); g.font = `900 ${Math.round(W * 0.84)}px Arial`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.lineJoin = 'round';
    g.lineWidth = W * 0.11; g.strokeStyle = '#1E2230'; g.strokeText(ch, W / 2, H * 0.55); g.fillStyle = fill; g.fillText(ch, W / 2, H * 0.55); };
  const f = canvasPlane(size, size, draw, { res: 256, transparent: true, emissive: 0.45 });
  const b = canvasPlane(size, size, draw, { res: 256, transparent: true }); b.material.color.set('#3E4150'); b.position.set(size * 0.035, -size * 0.035, -0.025);
  return grp(b, f);
}

export const ECHO_PROPS = {
  // A shout (pivot at the middle of the word, face +Z: give the prop face='camera'): big cut-out letters o.text ('OHÉ !') o.size (0.5) high, in
  // o.colors, carried along o.path [[t, x, y, z], ...] (in the parent's frame, held outside the keys), scaled by o.grow [[t, s]]; the letters wobble
  // (o.wobble, 0.18 rad) and bob one after the other; o.spread [[t, k]] spaces them (1: side by side); o.squash [[t, sx, sy]] flattens the word (an
  // impact); o.show [t0, t1]: only visible then.
  shoutLetters(o) {
    const text = [...(o.text ?? 'OHÉ !')].filter(c => c !== ' '), size = o.size ?? 0.5, cols = o.colors || ['#F5C33B', '#F08A3C', '#E8463A', '#F5C33B', '#3A9BDC'];
    const g = grp(), word = grp(); g.add(word);
    const ls = text.map((c, i) => { const l = letter(c, cols[i % cols.length], size); word.add(l); return l; });
    const n = ls.length;
    g.userData.update = t => {
      const show = o.show; g.visible = !show || (t >= show[0] && t < show[1]); if (!g.visible) return;
      const p = o.path ? lin(o.path, t, [0, 0, 0]) : [0, 0, 0]; word.position.set(p[0], p[1], p[2]);
      const s = lin(o.grow, t, 1), sp = lin(o.spread, t, 1), sq = o.squash ? lin(o.squash, t, [1, 1]) : [1, 1];
      word.scale.set(s * sq[0], s * sq[1], s);
      ls.forEach((l, i) => { const x = (i - (n - 1) / 2) * size * 0.78 * sp; l.position.set(x, size * 0.12 * Math.sin(t * 9 - i * 0.9), 0); l.rotation.z = (o.wobble ?? 0.18) * Math.sin(t * 7 + i * 1.3); });
    };
    g.userData.update(0); return g;
  },

  // Speed lines (cycle 22; pivot at their middle, give the prop face='camera' so that they lie in the picture plane): o.n (7) streaks, white with an
  // ink edge, o.len (1.2) long, spread over o.w (0.8) across, pointing along o.angle (rad in the picture plane, 0: toward +X of the prop), each one
  // sliding back along it and fading in a loop; visible during o.at [[t0, t1], ...] (always without it); o.path [[t, x, y, z], ...] carries them like
  // shoutLetters (the same keys behind a flying word), o.color
  speedLines(o) {
    const n = o.n ?? 7, L = o.len ?? 1.2, W = o.w ?? 0.8, r = rng(o.seed ?? 3), g = grp(), rot = grp(); g.add(rot); rot.rotation.z = o.angle ?? 0;
    const ls = [];
    for (let i = 0; i < n; i++) {
      const len = L * (0.5 + 0.5 * r()), th = 0.018 + 0.012 * r(), y = (i / Math.max(1, n - 1) - 0.5) * W + (r() - 0.5) * W * 0.12;
      const fm = new THREE.MeshBasicMaterial({ color: o.color || '#FFFFFF', transparent: true, depthWrite: false, toneMapped: false });
      const bm = new THREE.MeshBasicMaterial({ color: '#1E2230', transparent: true, depthWrite: false });
      const f = new THREE.Mesh(new THREE.PlaneGeometry(len, th), fm), b = new THREE.Mesh(new THREE.PlaneGeometry(len + 0.02, th + 0.014), bm); b.position.z = -0.002;
      const s1 = grp(b, f); rot.add(s1); ls.push({ s1, fm, bm, len, y, ph: r(), rate: 2.5 + 2 * r() });
    }
    g.userData.update = t => {
      const on = !o.at || list(o.at).some(([a, b]) => t >= a && t < b); g.visible = on; if (!on) return;
      if (o.path) { const p = lin(o.path, t, [0, 0, 0]); g.position.set(p[0], p[1], p[2]); }
      for (const l of ls) { const u = (t * l.rate + l.ph) % 1; l.s1.position.set(-u * L * 0.9 - l.len / 2, l.y, 0); const a = Math.sin(PI * u); l.fm.opacity = a; l.bm.opacity = a * 0.85; }
    };
    g.userData.update(0); return g;
  },

  // A mountain range (pivot at the middle of its foot): o.n (7) low-poly peaks over o.w (60) metres along X, up to o.h (18) high, o.d (14) deep in
  // rows, grey-green rock with snow caps (o.snow false: none), o.seed; o.colors [rock, rock2, snow]
  mountainRange(o) {
    const n = o.n ?? 7, w = o.w ?? 60, H = o.h ?? 18, d = o.d ?? 14, r = rng(o.seed ?? 11), g = grp();
    const [c1, c2, cs] = o.colors || ['#8A9488', '#77837A', '#F4F6F8'];
    for (let i = 0; i < n; i++) {
      const h = H * (0.55 + 0.45 * r()), rad = h * (0.75 + 0.35 * r()), x = -w / 2 + (i + 0.5) * w / n + (r() - 0.5) * w / n * 0.6, z = -(r() * d);
      const geo = new THREE.ConeGeometry(rad, h, 5 + Math.floor(r() * 3), 1); geo.translate(0, h / 2, 0);
      const pos = geo.attributes.position; for (let k = 0; k < pos.count; k++) if (pos.getY(k) < h * 0.9) { pos.setX(k, pos.getX(k) * (0.85 + 0.3 * r())); pos.setZ(k, pos.getZ(k) * (0.85 + 0.3 * r())); }
      geo.computeVertexNormals(); const m = new THREE.Mesh(geo, mat(i % 2 ? c1 : c2)); m.position.set(x, 0, z); m.rotation.y = r() * TAU; m.receiveShadow = true; g.add(m);
      if (o.snow !== false) { const sh = h * 0.32, sgeo = new THREE.ConeGeometry(rad * 0.34, sh, 5 + Math.floor(r() * 3), 1); sgeo.translate(0, h - sh / 2 + 0.02, 0);
        const sm = new THREE.Mesh(sgeo, mat(cs)); sm.position.copy(m.position); sm.rotation.y = m.rotation.y; g.add(sm); }
    }
    return g;
  },

  // A missing notice (pivot at its centre, face +Z): « AVIS DE RECHERCHE » in red, a drawn speech bubble with « OHÉ ! » in it, « DISPARU DANS LA
  // MONTAGNE » under it, a strip of tape at each top corner; o.w (0.5) wide, o.h (0.7) high
  missingPoster(o) {
    const w = o.w ?? 0.5, h = o.h ?? 0.7, g = grp();
    const pl = canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#F6F0DE'; c.fillRect(0, 0, W, H); c.strokeStyle = '#2A2C30'; c.lineWidth = W * 0.012; c.strokeRect(W * 0.03, H * 0.02, W * 0.94, H * 0.96);
      c.fillStyle = '#C8202A'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${Math.round(H * 0.075)}px Arial`; c.fillText('AVIS DE', W / 2, H * 0.09); c.fillText('RECHERCHE', W / 2, H * 0.17);
      c.fillStyle = '#FFFFFF'; c.strokeStyle = '#2A2C30'; c.lineWidth = W * 0.02; c.beginPath(); c.ellipse(W * 0.5, H * 0.47, W * 0.36, H * 0.17, 0, 0, TAU); c.fill(); c.stroke();
      c.beginPath(); c.moveTo(W * 0.32, H * 0.6); c.lineTo(W * 0.22, H * 0.72); c.lineTo(W * 0.44, H * 0.62); c.closePath(); c.fill(); c.stroke();
      c.fillStyle = '#2A2C30'; c.font = `900 ${Math.round(H * 0.11)}px Arial`; c.fillText('OHÉ !', W / 2, H * 0.48);
      c.font = `900 ${Math.round(H * 0.05)}px Arial`; c.fillText('DISPARU DANS', W / 2, H * 0.81); c.fillText('LA MONTAGNE', W / 2, H * 0.88); }, { res: 512 });
    g.add(pl, at(box(w * 0.22, h * 0.05, 0.003, '#E9D9A8'), -w * 0.4, h * 0.47, 0.002, 0, 0, 0.6), at(box(w * 0.22, h * 0.05, 0.003, '#E9D9A8'), w * 0.4, h * 0.47, 0.002, 0, 0, -0.6));
    return g;
  },

  // A fine (pivot at its centre, face +Z): a pale green slip « AVIS DE CONTRAVENTION », « TAPAGE », « 135 € », a signature; o.w (0.22)
  fineTicket(o) {
    const w = o.w ?? 0.22, h = w * 1.35;
    return grp(canvasPlane(w, h, (c, W, H) => { c.fillStyle = '#E4F0DA'; c.fillRect(0, 0, W, H); c.fillStyle = '#2A2C30'; c.textAlign = 'center'; c.textBaseline = 'middle';
      c.font = `900 ${Math.round(H * 0.06)}px Arial`; c.fillText('AVIS DE', W / 2, H * 0.1); c.fillText('CONTRAVENTION', W / 2, H * 0.17);
      c.fillStyle = '#C8202A'; c.font = `900 ${Math.round(H * 0.14)}px Arial`; c.fillText('TAPAGE', W / 2, H * 0.42);
      c.fillStyle = '#2A2C30'; c.font = `900 ${Math.round(H * 0.12)}px Arial`; c.fillText('135 €', W / 2, H * 0.62);
      c.strokeStyle = '#2A4B9B'; c.lineWidth = W * 0.012; c.beginPath(); c.moveTo(W * 0.25, H * 0.84); c.bezierCurveTo(W * 0.4, H * 0.74, W * 0.5, H * 0.92, W * 0.75, H * 0.8); c.stroke(); }, { res: 256 }));
  },

  // A rocky summit lookout (pivot at the floor in the middle of its flat top): a low-poly rock o.r (1.6) wide falling away under the floor, a wooden
  // railing along its front edge, a signpost « SOMMET » with o.alt (« 2 040 m »)
  summitRock(o) {
    const r0 = o.r ?? 1.6, g = grp(), rock = new THREE.Mesh(new THREE.CylinderGeometry(r0, r0 * 1.9, 3.0, 7, 2), mat('#8E8A84'));
    const pos = rock.geometry.attributes.position, rr = rng(o.seed ?? 5); for (let k = 0; k < pos.count; k++) if (pos.getY(k) < 1.4) { pos.setX(k, pos.getX(k) * (0.85 + 0.3 * rr())); pos.setZ(k, pos.getZ(k) * (0.85 + 0.3 * rr())); }
    rock.geometry.computeVertexNormals(); rock.position.y = -1.5; rock.receiveShadow = true; g.add(rock);
    for (let i = 0; i < 5; i++) g.add(at(cyl(0.035, 0.035, 0.95, '#7A5A3C', 6, { pivot: 'bottom' }), -r0 * 0.7 + i * r0 * 0.35, 0, r0 * 0.82));
    g.add(at(box(r0 * 1.5, 0.06, 0.06, '#8A6A45'), 0, 0.95, r0 * 0.82), at(box(r0 * 1.5, 0.05, 0.05, '#8A6A45'), 0, 0.55, r0 * 0.82));
    const sign = canvasPlane(0.6, 0.3, (c, W, H) => { c.fillStyle = '#F4EBD8'; c.fillRect(0, 0, W, H); c.strokeStyle = '#7A5A3C'; c.lineWidth = W * 0.03; c.strokeRect(0, 0, W, H);
      c.fillStyle = '#2A2C30'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `900 ${Math.round(H * 0.34)}px Arial`; c.fillText('SOMMET', W / 2, H * 0.36); c.font = `700 ${Math.round(H * 0.26)}px Arial`; c.fillText(o.alt ?? '2 040 m', W / 2, H * 0.72); }, { res: 256 });
    g.add(at(cyl(0.04, 0.04, 1.5, '#7A5A3C', 6, { pivot: 'bottom' }), r0 * 0.75, 0, -r0 * 0.3), at(sign, r0 * 0.75, 1.35, -r0 * 0.3 + 0.045));
    return g;
  },
};
