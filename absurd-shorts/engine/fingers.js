// Hands with fingers for the cartoon rig (cycle 2). Opt-in: script `fingers: true` or cast `{fingers: true}`; without it a character keeps the
// measured mitten (a flat paddle and a thumb), so older stories render exactly as before.
//
// A hand pose is six numbers [index, middle, ring, little, thumb, splay]:
//   curls 0 (straight) .. 1 (closed on the palm); thumb -1 (stuck out, a thumbs-up) .. 0 (relaxed) .. 1 (folded across the palm);
//   splay -1 (fingers tight) .. 1 (fanned).
// Clips and story keys give a pose by name or as numbers under the toon channel `hands`: {L: 'point', R: [0, 1, 1, 1, 0.9, 0]}.
// The palm faces +Z of the hand joint (forward when the arm hangs); turn the wrist with the hand joint (handL / handR: ry twists the forearm).
import * as THREE from 'three';
import { box } from './style.js';

export const HAND_POSES = {
  rest: [0.18, 0.2, 0.24, 0.28, 0.2, 0],        // relaxed, slightly curled
  open: [0, 0, 0, 0, 0, 0.3],                   // flat hand
  spread: [0, 0, 0, 0, -0.35, 1],               // fingers fanned (a take, « stop »)
  fist: [1, 1, 1, 1, 1, 0],
  point: [0, 1, 1, 1, 0.9, 0],                  // the index alone
  two: [0, 0, 1, 1, 0.9, 0.55],                 // index and middle (two, or a V)
  pinch: [0.6, 0.15, 0.1, 0.1, 0.8, 0.2],       // thumb against the index (holding a sheet, a nose)
  thumbUp: [1, 1, 1, 1, -1, 0],
  grip: [0.7, 0.7, 0.7, 0.7, 0.6, 0],           // round an object
  claw: [0.45, 0.45, 0.45, 0.45, 0.2, 0.8],     // fingers hooked and fanned (fear, strain)
};
export const handPose = p => Array.isArray(p) ? p : (HAND_POSES[p] || HAND_POSES.rest);
export const blendHand = (a, b, w) => { const x = handPose(a), y = handPose(b); return x.map((v, i) => v + (y[i] - v) * w); };
export function blendHands(a, b, w) {   // {L, R} x {L, R}; a missing side is the rest pose
  if (!a && !b) return null; const out = {};
  for (const s of ['L', 'R']) if (a?.[s] != null || b?.[s] != null) out[s] = blendHand(a?.[s] ?? 'rest', b?.[s] ?? 'rest', w);
  return out;
}

// swap the mittens of a built human for a palm, four two-part fingers and a two-part thumb
export function fingersUpgrade(obj) {
  const ud = obj.userData, J = ud.joints; if (!J || ud.fingers) return ud.fingers;
  const hands = {};
  for (const s of ['L', 'R']) {
    const h = J['hand' + s]; if (!h) continue; const sx = s === 'L' ? 1 : -1;
    const old = h.children.filter(c => c.isMesh && !c.userData.isAttachment); if (!old.length) continue;
    const skin = ud.spec?.gloves || ud.dims?.skinColor || ud.spec?.skin || '#E2B48A';   // the painted hero: the tone of his atlas skin
    for (const m of old) m.visible = false;
    const g = new THREE.Group(); g.name = 'fingers'; h.add(g);
    g.add(box(0.085, 0.072, 0.04, skin, { pivot: 'top' }));   // the palm
    const fs = [];
    for (let i = 0; i < 4; i++) {   // index (thumb side) .. little finger
      const k = new THREE.Group(); k.position.set(sx * (0.031 - i * 0.0207), -0.07, 0); g.add(k);
      const L1 = [0.036, 0.04, 0.038, 0.03][i], L2 = [0.03, 0.033, 0.03, 0.024][i];
      k.add(box(0.0185, L1, 0.03, skin, { pivot: 'top' }));
      const k2 = new THREE.Group(); k2.position.y = -L1; k.add(k2); k2.add(box(0.0175, L2, 0.027, skin, { pivot: 'top' }));
      fs.push({ k, k2 });
    }
    const tk = new THREE.Group(); tk.position.set(sx * 0.044, -0.014, 0.006); g.add(tk); tk.add(box(0.024, 0.04, 0.03, skin, { pivot: 'top' }));
    const tk2 = new THREE.Group(); tk2.position.y = -0.04; tk.add(tk2); tk2.add(box(0.022, 0.03, 0.027, skin, { pivot: 'top' }));
    hands[s] = p => {
      const [a, b, c, d, th, sp] = handPose(p);
      [a, b, c, d].forEach((cv, i) => { const f = fs[i]; f.k.rotation.set(-1.45 * cv, 0, sx * sp * (0.26 - i * 0.175) * (1 - 0.8 * Math.min(1, cv))); f.k2.rotation.x = -1.5 * cv; });
      // thumb: out to the side at rest, straight up/out for a thumbs-up (th < 0), folded over the fingers for a fist (th > 0)
      const t = Math.max(0, th), up = Math.max(0, -th);
      tk.rotation.set(-0.9 * t, sx * 0.9 * t, sx * (0.55 + 0.95 * up - 0.35 * t)); tk2.rotation.set(-0.7 * t, 0, sx * 0.1 * up);
    };
    hands[s]('rest');
  }
  ud.fingers = { set(hs) { for (const s of ['L', 'R']) hands[s]?.(hs?.[s] ?? 'rest'); } };
  return ud.fingers;
}
