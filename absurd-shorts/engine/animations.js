// Pose/animation library for the puppet rig.
// A clip is f(t, params) -> pose, where pose = { joint: [rx, ry, rz], root: {x,y,z,rx,ry,rz} }.
// Conventions (character faces +Z, its left is +X):
//   shoulder rx < 0  -> arm swings forward      shoulder rz > 0 (L) / < 0 (R) -> arm raised sideways
//   elbow rx < 0     -> forearm bends forward    hip rx < 0 -> leg lifts forward, knee rx > 0 -> shin bends back
// Motion style observed in the source: stiff, snappy, few in-betweens, tiny idle
// breathing, big readable silhouettes, deadpan holds. Keep amplitudes graphic.

const S = Math.sin, C = Math.cos, PI = Math.PI;
const m = (L, R) => ({ L, R }); // helper for symmetric arms
const arms = (sh, el, mirror = true) => ({
  shoulderL: sh.L, shoulderR: mirror ? [sh.R[0], -sh.R[1], -sh.R[2]] : sh.R,
  elbowL: el.L, elbowR: mirror ? [el.R[0], -el.R[1], -el.R[2]] : el.R,
});

export const CLIPS = {
  // --- standing / idle -------------------------------------------------
  idle: (t, p = {}) => ({
    torso: [0.015 * S(t * 1.6), 0, 0.01 * S(t * 0.7)],
    head: [0.02 * S(t * 0.9 + 1), 0.04 * S(t * 0.45), 0.015 * S(t * 0.6)],
    ...arms(m([0.04 * S(t * 1.6), 0, 0.07], [0.04 * S(t * 1.6 + 0.4), 0, 0.07]), m([-0.12, 0, 0], [-0.12, 0, 0])),
    root: { y: 0.004 * S(t * 3.2) },
  }),
  stand: () => ({ ...arms(m([0, 0, 0.06], [0, 0, 0.06]), m([-0.08, 0, 0], [-0.08, 0, 0])) }),
  stiff: () => ({ ...arms(m([0, 0, 0.02], [0, 0, 0.02]), m([0, 0, 0], [0, 0, 0])) }), // standing like a plank (sleeping on a wire)
  handsOnHips: (t) => ({
    torso: [0.01 * S(t * 1.5), 0, 0], head: [0, 0.03 * S(t * 0.5), 0.03],
    ...arms(m([0.15, 0, 0.75], [0.15, 0, 0.75]), m([0, 0.3, -2.0], [0, 0.3, -2.0])),
    handL: [0, 0, 0.6], handR: [0, 0, -0.6],
  }),
  oneHandHip: (t) => ({ // v1 opening: one hand on hip, other raised holding object
    ...arms(m([0.15, 0, 0.75], [-0.2, 0, 2.5]), m([0, 0.3, -2.0], [0, 0, 0.5])), handL: [0, 0, 0.6],
    head: [0, 0.05 * S(t), 0.04],
  }),
  armsCrossed: () => ({ ...arms(m([-0.5, -0.65, 0.2], [-0.55, -0.65, 0.2]), m([-1.75, 0, 0], [-1.7, 0, 0])), head: [0.05, 0, 0] }),
  point: (t, p = {}) => ({ // points forward with right arm
    ...arms(m([0, 0, 0.08], [-1.45 + 0.03 * S(t * 2), 0.2, 0.1]), m([-0.1, 0, 0], [-0.05, 0, 0])), head: [0, -0.15, 0],
  }),
  raiseOverhead: (t) => ({ ...arms(m([0, 0, 0.1], [-0.2, 0, 2.7]), m([-0.1, 0, 0], [0, 0, 0.3])), head: [-0.05, 0, 0] }),
  holdOut: () => ({ ...arms(m([-1.2, 0, 0.1], [-1.2, 0, 0.1]), m([-0.4, 0, 0], [-0.4, 0, 0])) }), // presenting / holding a magnifying glass over a table
  carry: () => ({ ...arms(m([-0.9, 0, 0.15], [-0.9, 0, 0.15]), m([-0.9, 0, 0], [-0.9, 0, 0])), torso: [-0.06, 0, 0] }),
  salute: (t) => ({ ...arms(m([0, 0, 0.06], [-0.7, 0, 1.25]), m([-0.1, 0, 0], [-2.3, 0.3, 0])), head: [-0.03, 0, 0] }),
  wave: (t) => ({ ...arms(m([0, 0, 0.06], [0, 0, 2.6]), m([-0.1, 0, 0], [0, 0, 0.5 + 0.45 * S(t * 9)])) }),
  shrug: (t) => ({ torso: [0, 0, 0], head: [0, 0, 0.18], ...arms(m([-0.1, 0, 0.35], [-0.1, 0, 0.35]), m([-1.5, 0.9, 0], [-1.5, 0.9, 0])), root: { y: 0.015 } }),
  facepalm: () => ({ ...arms(m([0, 0, 0.06], [-1.1, 0, 0.3]), m([-0.1, 0, 0], [-2.35, 0, 0])), head: [0.35, 0, 0], torso: [0.08, 0, 0] }),
  glueForehead: (t, p = {}) => { // v1: slapping something onto the forehead
    const k = Math.min(1, t / 0.35);
    return { ...arms(m([0, 0, 0.06], [-1.6 * k, 0, 0.3 * k]), m([-0.1, 0, 0], [-1.9 * k, 0, 0])), head: [-0.2 * k, 0, 0] };
  },
  think: (t) => ({ ...arms(m([-0.5, -0.65, 0.2], [-0.6, 0, 0.2]), m([-1.75, 0, 0], [-2.4, 0, 0])), head: [-0.05, 0, 0.12 + 0.03 * S(t)] }),
  phone: () => ({ ...arms(m([0, 0, 0.06], [-0.5, 0, 0.75]), m([-0.1, 0, 0], [-2.45, 0.2, 0])), head: [0, 0, -0.12] }),
  holdPhoneFront: () => ({ ...arms(m([0, 0, 0.06], [-1.1, 0, 0.1]), m([-0.1, 0, 0], [-1.1, 0, 0])), head: [0.35, 0, 0] }),
  talk: (t) => ({ head: [0.04 * S(t * 7), 0.06 * S(t * 2), 0], ...arms(m([0, 0, 0.06], [-0.6 - 0.15 * S(t * 4), 0, 0.15]), m([-0.1, 0, 0], [-1.2 + 0.2 * S(t * 4), 0.6, 0])) }),
  yell: (t) => ({ head: [-0.2 + 0.03 * S(t * 20), 0, 0], torso: [-0.08, 0, 0], ...arms(m([-0.2, 0, 0.5], [-0.2, 0, 0.5]), m([-1.3, 0, 0], [-1.3, 0, 0])), handL: [0, 0, 0], root: { y: 0.01 * S(t * 25) } }),
  nod: (t) => ({ head: [0.18 * Math.max(0, S(t * 8)), 0, 0], ...CLIPS.stand() }),
  shakeHead: (t) => ({ head: [0, 0.3 * S(t * 9), 0], ...CLIPS.stand() }),
  lookAround: (t) => ({ head: [0, 0.6 * S(t * 2.2), 0], torso: [0, 0.1 * S(t * 2.2), 0], ...CLIPS.stand() }),
  lookUp: (t) => ({ head: [-0.55, 0, 0], torso: [-0.08, 0, 0], ...CLIPS.stand() }),
  lookDown: () => ({ head: [0.5, 0, 0], ...CLIPS.stand() }),
  stareCamera: (t) => ({ head: [0.01 * S(t), 0, 0], ...CLIPS.stand() }), // THE deadpan reaction hold
  angryFist: (t) => ({ ...arms(m([0, 0, 0.06], [-0.4, 0, 2.2]), m([-0.1, 0, 0], [0, 0, 0.6 + 0.3 * S(t * 14)])), head: [-0.1, 0, 0], torso: [-0.05, 0, 0] }),
  celebrate: (t) => ({ ...arms(m([0, 0, 2.7 + 0.15 * S(t * 10)], [0, 0, 2.7 + 0.15 * S(t * 10 + 1)]), m([0, 0, 0.3], [0, 0, 0.3])), root: { y: 0.08 * Math.abs(S(t * 5)) }, head: [-0.2, 0, 0] }),
  surrender: (t) => ({ ...arms(m([0, 0, 2.1], [0, 0, 2.1]), m([0, 0, -1.4], [0, 0, -1.4])), head: [0.05, 0, 0] }),
  handcuffed: () => ({ ...arms(m([0.45, 0, -0.15], [0.45, 0, -0.15]), m([-0.3, 0, 0.3], [-0.3, 0, 0.3])), head: [0.15, 0, 0] }),
  scared: (t) => ({ ...arms(m([-1.1, -0.4, 0.4], [-1.1, -0.4, 0.4]), m([-1.6, 0, 0], [-1.6, 0, 0])), hipL: [-0.25, 0, 0], hipR: [-0.25, 0, 0], kneeL: [0.5, 0, 0], kneeR: [0.5, 0, 0], torso: [0.15, 0, 0], root: { y: -0.04 + 0.006 * S(t * 40), x: 0.006 * S(t * 37) } }),
  pressGlass: (t) => ({ ...arms(m([-1.5, 0, 0.5], [-1.5, 0, 0.5]), m([-0.5, 0, 0], [-0.5, 0, 0])), handL: [0, 0, 0], head: [0.04 * S(t * 3), 0, 0] }), // trapped under a glass dome
  cry: (t) => ({ ...arms(m([-1.0, -0.3, 0.3], [-1.0, -0.3, 0.3]), m([-2.2, 0, 0], [-2.2, 0, 0])), head: [0.35 + 0.05 * S(t * 12), 0, 0], torso: [0.15, 0, 0], root: { y: 0.005 * S(t * 12) } }),
  dance: (t) => ({ ...arms(m([0, 0, 1.2 + 0.6 * S(t * 6)], [0, 0, 1.2 - 0.6 * S(t * 6)]), m([0, 0, 1.2], [0, 0, 1.2])), hipL: [-0.3 * Math.max(0, S(t * 6)), 0, 0], kneeL: [0.6 * Math.max(0, S(t * 6)), 0, 0], hipR: [-0.3 * Math.max(0, -S(t * 6)), 0, 0], kneeR: [0.6 * Math.max(0, -S(t * 6)), 0, 0], torso: [0, 0.3 * S(t * 3), 0.1 * S(t * 6)], root: { y: 0.03 * Math.abs(S(t * 6)) } }),
  sneak: (t) => { const ph = t * 3; return { ...CLIPS.walk(t, { freq: 1.5, amp: 0.35 }), torso: [0.3, 0, 0], ...arms(m([-0.6, 0, 0.3], [-0.6, 0, 0.3]), m([-1.2, 0, 0], [-1.2, 0, 0])), root: { y: -0.05 } }; },

  // --- locomotion (root forward motion is driven by the director's path) ---
  walk: (t, p = {}) => {
    const f = p.freq ?? 1.9, a = p.amp ?? 0.42, ph = t * f * 2 * PI;
    return {
      hipL: [-a * S(ph), 0, 0], hipR: [a * S(ph), 0, 0],
      kneeL: [Math.max(0, a * 1.2 * S(ph + 1.4)), 0, 0], kneeR: [Math.max(0, a * 1.2 * S(ph + 1.4 + PI)), 0, 0],
      footL: [0.1 * S(ph), 0, 0], footR: [-0.1 * S(ph), 0, 0],
      ...arms(m([a * 0.8 * S(ph), 0, 0.06], [-a * 0.8 * S(ph), 0, 0.06]), m([-0.25, 0, 0], [-0.25, 0, 0])),
      torso: [0.03, 0.05 * S(ph), 0], head: [0, -0.04 * S(ph), 0],
      root: { y: 0.025 * Math.abs(S(ph)) },
    };
  },
  run: (t, p = {}) => { // cartoon sprint, high knees + pumping bent arms (v4)
    const f = p.freq ?? 3.1, ph = t * f * 2 * PI;
    return {
      hipL: [-0.95 * S(ph) - 0.25, 0, 0], hipR: [0.95 * S(ph) - 0.25, 0, 0],
      kneeL: [0.9 + 0.8 * S(ph + 1.2), 0, 0], kneeR: [0.9 + 0.8 * S(ph + 1.2 + PI), 0, 0],
      ...arms(m([1.0 * S(ph), 0, 0.12], [-1.0 * S(ph), 0, 0.12]), m([-1.5, 0, 0], [-1.5, 0, 0])),
      torso: [0.28, 0.12 * S(ph), 0], head: [-0.15, -0.1 * S(ph), 0],
      root: { y: 0.07 * Math.abs(S(ph)) - 0.03 },
    };
  },
  flee: (t, p = {}) => { const r = CLIPS.run(t, { freq: 3.6 }); return { ...r, ...arms(m([-0.3, 0, 2.6 + 0.2 * S(t * 20)], [-0.3, 0, 2.6 + 0.2 * S(t * 20 + 1)]), m([0, 0, 0.4], [0, 0, 0.4])) }; }, // panic, arms in the air
  climbDown: (t) => { const ph = t * 2 * PI * 1.2; return { ...arms(m([-2.6 + 0.3 * S(ph), 0, 0.2], [-2.6 - 0.3 * S(ph), 0, 0.2]), m([-0.4, 0, 0], [-0.4, 0, 0])), hipL: [-0.6 - 0.4 * S(ph), 0, 0], hipR: [-0.6 + 0.4 * S(ph), 0, 0], kneeL: [0.9, 0, 0], kneeR: [0.9, 0, 0] }; },
  jump: (t, p = {}) => { const d = p.dur ?? 0.6, k = Math.min(1, t / d); const y = 4 * k * (1 - k) * (p.height ?? 0.5); return { root: { y }, ...arms(m([0, 0, 2.4], [0, 0, 2.4]), m([0, 0, 0], [0, 0, 0])), hipL: [-0.4, 0, 0], hipR: [-0.4, 0, 0], kneeL: [0.8, 0, 0], kneeR: [0.8, 0, 0] }; },
  startle: (t) => { const k = Math.min(1, t / 0.15); const y = t < 0.3 ? 0.15 * S(t / 0.3 * PI) : 0; return { root: { y }, ...arms(m([-0.2, 0, 1.1 * k], [-0.2, 0, 1.1 * k]), m([0, 0, -0.6 * k], [0, 0, -0.6 * k])), head: [-0.15 * k, 0, 0] }; },

  // --- seated / ground --------------------------------------------------
  sit: (t) => ({ hipL: [-1.57, 0, 0.05], hipR: [-1.57, 0, -0.05], kneeL: [1.57, 0, 0], kneeR: [1.57, 0, 0], ...arms(m([-0.7, 0, 0.1], [-0.7, 0, 0.1]), m([-0.8, 0, 0], [-0.8, 0, 0])), head: [0.02 * S(t), 0, 0], root: { y: -0.45 } }),
  sitWrite: (t) => ({ ...CLIPS.sit(t), ...arms(m([-0.9, 0, 0.15], [-1.0 + 0.05 * S(t * 12), 0, 0.15]), m([-0.7, 0, 0], [-0.6, 0, 0])), head: [0.4, 0, 0], torso: [0.15, 0, 0] }),
  slumpDesk: (t) => ({ ...CLIPS.sit(t), torso: [1.15, 0, 0], head: [0.25, 0, 0.1], ...arms(m([-1.7, 0, 0.6], [-1.7, 0, 0.6]), m([0, 0, -0.4], [0, 0, -0.4])), root: { y: -0.45 + 0.004 * S(t * 2) } }), // the defeated ending
  kneel: () => ({ hipL: [-1.5, 0, 0], kneeL: [1.5, 0, 0], hipR: [0, 0, 0], kneeR: [1.55, 0, 0], footR: [0.6, 0, 0], root: { y: -0.5 }, ...arms(m([-0.2, 0, 0.1], [-0.2, 0, 0.1]), m([-0.4, 0, 0], [-0.4, 0, 0])) }),
  lieDown: (t) => ({ root: { rx: -PI / 2, y: 0.12, z: -0.9 }, ...arms(m([0, 0, 0.2], [0, 0, 0.2]), m([0, 0, 0], [0, 0, 0])), head: [0.01 * S(t), 0, 0] }),
  faint: (t, p = {}) => { const k = Math.min(1, t / (p.dur ?? 0.5)); return { root: { rx: -PI / 2 * k * k, y: 0.12 * k, z: -0.9 * k }, ...arms(m([0, 0, 0.6 * k], [0, 0, 0.6 * k]), m([0, 0, 0], [0, 0, 0])) }; },
  crawl: (t) => { const ph = t * 2 * PI * 1.4; return { root: { rx: -1.35, y: -0.55 }, ...arms(m([-1.6 + 0.4 * S(ph), 0, 0.1], [-1.6 - 0.4 * S(ph), 0, 0.1]), m([0, 0, 0], [0, 0, 0])), hipL: [-0.3 - 0.3 * S(ph), 0, 0], hipR: [-0.3 + 0.3 * S(ph), 0, 0], kneeL: [1.3, 0, 0], kneeR: [1.3, 0, 0], head: [-1.0, 0, 0] }; },
  hangWire: (t) => ({ ...CLIPS.stiff(), root: { y: 0.01 * S(t * 1.3), rz: 0.03 * S(t * 0.9) }, footL: [0.4, 0, 0], footR: [0.4, 0, 0] }), // sleeping on a power line
  float: (t) => ({ root: { y: 0.1 * S(t * 1.5) }, ...arms(m([0, 0, 0.9], [0, 0, 0.9]), m([0, 0, 0], [0, 0, 0])), hipL: [-0.2, 0, 0], kneeL: [0.4, 0, 0] }),

  // --- creature/monster helper (vampire lurk, claw reach) -----------------
  lurk: (t) => ({ torso: [0.2, 0, 0], head: [0.1, 0.05 * S(t), 0], ...arms(m([-0.9, 0, 0.1], [-0.35, 0, 0.1]), m([-0.7, 0, 0], [-0.3, 0, 0])), handL: [0.6, 0, 0], root: { y: -0.02 } }),
  clawReach: (t) => { const k = Math.min(1, t / 0.6); return { ...arms(m([-1.5 * k, 0, 0.1], [0, 0, 0.06]), m([-0.1, 0, 0], [-0.1, 0, 0])), handL: [0.5, 0, 0], torso: [0.1, 0, 0] }; },
};

export const CLIP_NAMES = Object.keys(CLIPS);

const JOINTS = ['hips', 'torso', 'neck', 'head', 'shoulderL', 'elbowL', 'handL', 'shoulderR', 'elbowR', 'handR', 'hipL', 'kneeL', 'footL', 'hipR', 'kneeR', 'footR'];

export function samplePose(name, t, params) {
  const f = CLIPS[name] || CLIPS.idle; return f(Math.max(0, t), params || {});
}

export function blendPoses(a, b, w) {
  const out = {};
  for (const j of JOINTS) {
    const pa = a[j] || [0, 0, 0], pb = b[j] || [0, 0, 0];
    out[j] = [pa[0] + (pb[0] - pa[0]) * w, pa[1] + (pb[1] - pa[1]) * w, pa[2] + (pb[2] - pa[2]) * w];
  }
  const ra = a.root || {}, rb = b.root || {}; out.root = {};
  for (const k of ['x', 'y', 'z', 'rx', 'ry', 'rz']) out.root[k] = (ra[k] || 0) + ((rb[k] || 0) - (ra[k] || 0)) * w;
  return out;
}

// Apply a pose to a human rig. `base` = {x,y,z,ry} world placement from the director.
export function applyPose(human, pose, base = {}) {
  const J = human.userData.joints;
  for (const j of JOINTS) { if (!J[j]) continue; const r = pose[j] || [0, 0, 0]; J[j].rotation.set(r[0], r[1], r[2]); }
  const rt = pose.root || {};
  human.position.set((base.x || 0) + (rt.x || 0), (base.y || 0) + (rt.y || 0), (base.z || 0) + (rt.z || 0));
  human.rotation.set(rt.rx || 0, (base.ry || 0) + (rt.ry || 0), rt.rz || 0);
  if (base.scale) human.scale.setScalar(base.scale);
}
