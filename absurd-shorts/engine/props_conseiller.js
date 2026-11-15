// « Le service client » (story 73): this man called customer service and was put on hold; the hold music has been playing for ten years, became
// the national anthem, the band plays it at the parade; yesterday someone picked up: « for an adviser, press one »; he pressed one; the music came
// back. Conventions as in props.js (metres, front +Z, pivot at the floor unless said); every animated prop is a pure function of the shot time.
import * as THREE from 'three';
import { box, cyl, sphere } from './style.js';
import { grp, at, canvasPlane } from './props.js';

const PI = Math.PI, TAU = 2 * PI;
const clamp01 = x => Math.max(0, Math.min(1, x));
const hash = i => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const noteTex = (kind, col) => canvasPlane(1, 1.3, (c, W, H) => { c.clearRect(0, 0, W, H); c.fillStyle = c.strokeStyle = col; c.lineWidth = W * 0.09; c.lineCap = 'round';
  c.beginPath(); c.ellipse(W * 0.34, H * 0.78, W * 0.2, H * 0.11, -0.4, 0, TAU); c.fill(); c.beginPath(); c.moveTo(W * 0.51, H * 0.76); c.lineTo(W * 0.51, H * 0.14); c.stroke();
  if (kind) { c.beginPath(); c.moveTo(W * 0.51, H * 0.14); c.quadraticCurveTo(W * 0.92, H * 0.24, W * 0.82, H * 0.52); c.stroke(); }
  else { c.beginPath(); c.ellipse(W * 0.78, H * 0.68, W * 0.2, H * 0.11, -0.4, 0, TAU); c.fill(); c.beginPath(); c.moveTo(W * 0.95, H * 0.66); c.lineTo(W * 0.95, H * 0.06); c.lineTo(W * 0.51, H * 0.14); c.stroke(); } }, { res: 128, transparent: true });

export const CONSEILLER_PROPS = {
  // Hold music coming out of a phone, endlessly (pivot at the source; face it to the camera): o.rate notes a second (3) from o.from to o.until, each
  // drifting up and out to the side (o.dx, o.dy m/s) on a wobble, swelling in and fading out over o.life (1.2 s); o.color (navy), o.size (0.09)
  holdNotes(o) {
    const rate = o.rate ?? 3, life = o.life ?? 1.2, sz = o.size ?? 0.09, n = Math.ceil(rate * life) + 1, g = grp(), N = [];
    for (let i = 0; i < n; i++) { const pl = noteTex(i % 2, o.color || '#22305A'); pl.scale.set(sz, sz, 1); pl.material.depthWrite = false; pl.material.side = THREE.DoubleSide; pl.visible = false; g.add(pl); N.push(pl); }
    const per = n / rate;
    g.userData.update = t => { const t0 = o.from ?? 0, t1 = o.until ?? 1e9;
      N.forEach((m, i) => { let b = t0 + i / rate; if (t >= b) b += Math.floor((t - b) / per) * per; const u = t - b, on = t >= t0 && b <= t1 && u >= 0 && u < life; m.visible = on; if (!on) return;
        const side = (o.side ?? (hash(i + Math.floor(b * 3)) > 0.5 ? 1 : -1)), q = u / life;
        m.position.set(side * (o.dx ?? 0.25) * u + 0.04 * Math.sin(u * 8 + i), (o.dy ?? 0.45) * u, 0.005 * i); m.rotation.z = 0.35 * Math.sin(u * 6 + i * 2);
        const s = sz * (u < 0.1 ? u / 0.1 : 1) * (q > 0.75 ? 1 - (q - 0.75) / 0.25 : 1); m.scale.set(s, s, 1); }); };
    g.userData.update(-1); return g;
  },

  // A brass band instrument to hold (pivot at the grip): o.kind 'trumpet' (a gold tube and bell pointing +Z), 'tuba' (a big gold coil with the bell
  // up) or 'drum' (a red drum on a strap, o.beat [t...]: the skin jumps); o.s scale
  brass(o) {
    const G = o.color || '#E2B53C', g = grp(), k = o.kind || 'trumpet';
    if (k === 'trumpet') { const tube = at(cyl(0.012, 0.012, 0.32, G, 8, { outline: 0.003 }), 0, 0.02, 0.1); tube.rotation.x = PI / 2; g.add(tube);
      const bell = at(new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.12, 14, 1, true), new THREE.MeshLambertMaterial({ color: G, side: THREE.DoubleSide })), 0, 0.02, 0.3); bell.rotation.x = -PI / 2; g.add(bell);
      for (const z of [0.02, 0.06, 0.1]) g.add(at(cyl(0.008, 0.008, 0.06, '#C9A043', 6), 0, 0.06, z)); }
    else if (k === 'tuba') { const coil = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.035, 8, 18), new THREE.MeshLambertMaterial({ color: G })); coil.position.set(0, 0.1, 0); g.add(coil);
      const bell = at(new THREE.Mesh(new THREE.ConeGeometry(0.17, 0.26, 16, 1, true), new THREE.MeshLambertMaterial({ color: G, side: THREE.DoubleSide })), 0.12, 0.38, 0); bell.rotation.z = PI; g.add(bell); }
    else { const dr = grp(at(cyl(0.18, 0.18, 0.2, '#C8322A', 16, { outline: 0.004 }), 0, 0, 0), at(cyl(0.185, 0.185, 0.02, '#F4F1E8', 16), 0, 0.105, 0), at(cyl(0.185, 0.185, 0.02, '#F4F1E8', 16), 0, -0.105, 0)); dr.rotation.x = PI / 2; g.add(dr);
      const skin = dr.children[1]; g.userData.update = t => { let a = 0; for (const b of o.beat || []) { const u = t - b; if (u >= 0 && u < 0.15) a = Math.max(a, Math.exp(-u * 30)); } skin.position.y = 0.105 + 0.02 * a; }; }
    if (o.s) g.scale.setScalar(o.s); return g;
  },

  // A bridal veil (attach to the head joint; pivot at the crown): a white comb and a long sheer veil falling down the back, swaying a little
  bridalVeil(o) {
    const g = grp(), L = o.len ?? 0.9, W = o.w ?? 0.5;
    g.add(at(box(0.22, 0.03, 0.06, '#F4F1E8', { outline: 0.003 }), 0, 0.02, 0));
    const m = new THREE.MeshLambertMaterial({ color: '#FFFFFF', transparent: true, opacity: 0.72, side: THREE.DoubleSide, depthWrite: false });
    const geo = new THREE.PlaneGeometry(W, L, 4, 8); geo.translate(0, -L / 2, 0); const veil = new THREE.Mesh(geo, m); veil.position.set(0, 0.02, -0.06); veil.rotation.x = 0.18; g.add(veil);
    const p0 = geo.attributes.position.array.slice();
    g.userData.update = t => { const a = geo.attributes.position.array; for (let i = 0; i < a.length; i += 3) { const y = p0[i + 1], f = -y / L; a[i + 2] = p0[i + 2] - 0.05 * f * f * (1 + Math.sin(t * 2.2 + p0[i] * 4)); } geo.attributes.position.needsUpdate = true; };
    g.userData.update(0); return g;
  },

  // A flagpole with a flag that rises (pivot at the foot): a white pole o.h high (6), a tricolour flag climbing it between o.raise [t0, t1] and
  // flapping
  flagPole(o) {
    const H = o.h ?? 6, g = grp(), fw = o.w ?? 1.5, fh = fw * 0.66;
    g.add(at(cyl(0.05, 0.06, H, '#EDEDED', 8, { pivot: 'bottom', outline: 0.004 }), 0, 0, 0), at(sphere(0.08, '#E2B53C', 1), 0, H + 0.04, 0));
    const fl = grp(); const cols = o.colors || ['#2F62B5', '#F4F4F0', '#E0413A'];
    cols.forEach((c, i) => { const geo = new THREE.PlaneGeometry(fw / cols.length, fh, 3, 1); const s = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ color: c, side: THREE.DoubleSide })); s.position.set(0.06 + fw / cols.length * (i + 0.5), 0, 0); fl.add(s); });
    g.add(fl);
    g.userData.update = t => { const [a, b] = o.raise || [-1, -0.5], k = clamp01((t - a) / (b - a)); fl.position.y = 0.6 + (H - fh / 2 - 0.7) * k;
      fl.children.forEach((s, i) => { s.rotation.y = 0.12 * Math.sin(t * 5 + i * 0.9); s.position.z = 0.04 * Math.sin(t * 5 + i * 0.9); }); };
    g.userData.update(0); return g;
  },

  // A phone's call screen with its keypad, big for an insert (pivot at its middle, screen +Z): a black phone o.w wide (0.5), a timer line on top
  // (o.label), twelve round keys; o.pressAt: the key '1' lights up green and sinks at that time
  phoneKeypad(o) {
    const w = o.w ?? 0.5, h = w * 2.0, g = grp(at(box(w, h, 0.04, '#17181C', { outline: 0.006 }), 0, 0, 0));
    const draw = lit => (c, W, H) => { c.fillStyle = '#0E1A26'; c.fillRect(0, 0, W, H); c.fillStyle = '#CFE3F2'; c.textAlign = 'center'; c.textBaseline = 'middle'; c.font = `700 ${W * 0.07}px Arial`; c.fillText(o.label || 'EN ATTENTE', W / 2, H * 0.08);
      const keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#'];
      keys.forEach((kk, i) => { const x = W * (0.22 + 0.28 * (i % 3)), y = H * (0.3 + 0.16 * Math.floor(i / 3)); c.fillStyle = lit && kk === '1' ? '#3CCB6A' : '#2A3846'; c.beginPath(); c.arc(x, y, W * 0.11, 0, TAU); c.fill();
        c.fillStyle = '#FFFFFF'; c.font = `700 ${W * 0.1}px Arial`; c.fillText(kk, x, y + W * 0.005); }); };
    const off = canvasPlane(w * 0.9, h * 0.92, draw(false), { res: 256 }), on = canvasPlane(w * 0.9, h * 0.92, draw(true), { res: 256 }); off.position.z = on.position.z = 0.021; g.add(off, on);
    g.userData.update = t => { const p = o.pressAt != null && t >= o.pressAt; on.visible = p; off.visible = !p; };
    g.userData.update(-1); return g;
  },
};
