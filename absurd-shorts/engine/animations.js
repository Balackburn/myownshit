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
    ...arms(m([0.04 * S(t * 1.6), 0, 0.2], [0.04 * S(t * 1.6 + 0.4), 0, 0.2]), m([-0.12, 0, -0.3], [-0.12, 0, -0.3])), // elbows out, forearms back to the hips (V1 18.4 s)
    root: { y: 0.004 * S(t * 3.2) },
  }),
  stand: () => ({ ...arms(m([0, 0, 0.2], [0, 0, 0.2]), m([-0.08, 0, -0.3], [-0.08, 0, -0.3])) }), // measured rest pose
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
  shrug: (t) => ({ torso: [0, 0, 0], head: [0, 0, 0.18], ...arms(m([-0.15, 0, 0.6], [-0.15, 0, 0.6]), m([-0.9, 1.1, 0], [-0.9, 1.1, 0])), handL: [0, 1.2, 0], handR: [0, -1.2, 0], root: { y: 0.015 } }),
  facepalm: () => ({ ...arms(m([0, 0, 0.06], [-1.1, 0, 0.3]), m([-0.1, 0, 0], [-2.35, 0, 0])), head: [0.35, 0, 0], torso: [0.08, 0, 0] }),
  glueForehead: (t, p = {}) => { // v1: slapping something onto the forehead
    const k = Math.min(1, t / 0.35);
    return { ...arms(m([0, 0, 0.06], [-1.6 * k, 0, 0.3 * k]), m([-0.1, 0, 0], [-1.9 * k, 0, 0])), head: [-0.2 * k, 0, 0] };
  },
  think: (t) => ({ ...arms(m([-0.5, -0.65, 0.2], [-0.6, 0, 0.2]), m([-1.75, 0, 0], [-2.4, 0, 0])), head: [-0.05, 0, 0.12 + 0.03 * S(t)] }),
  scratchHead: (t) => ({ ...arms(m([0, 0, 0.06], [-0.3, 0, 2.3]), m([-0.1, 0, 0], [-0.4, 0, 1.9 + 0.12 * S(t * 14)])), head: [0.06, 0, 0.12], torso: [0, 0, 0.03] }), // confused, hand behind the head (sheet)
  present: (t) => ({ ...arms(m([0, 0, 0.06], [-0.55, 0, 0.75]), m([-0.1, 0, 0], [-0.6, -1.2, 0])), handR: [0, -1.4, 0], head: [0, -0.18, 0.04] }), // "voilà": one arm out, palm up (sheet)
  thinkChin: (t) => ({ ...arms(m([-0.5, -0.65, 0.2], [-0.45, 0, 0.1]), m([-1.75, 0, 0], [-2.55, 0, 0])), head: [-0.08, 0.12, 0.05 + 0.02 * S(t)] }), // hand on chin, arm crossed under (sheet)
  armsUp: (t) => ({ ...arms(m([0, 0, 2.75], [0, 0, 2.75]), m([0, 0, 0.15], [0, 0, 0.15])), head: [-0.05, 0, 0] }), // both arms straight up, stiff (sheet)
  pushVacuum: (t) => { const k = Math.sin(t * 2 * PI * 1.1); return { ...arms(m([0, 0, 0.06], [-0.42 - 0.12 * k, 0, 0.12]), m([-0.12, 0, 0], [-0.3, 0, 0])), torso: [0.05, -0.08, 0], head: [0.12, -0.1, 0], hipL: [-0.12 * k, 0, 0], hipR: [0.12 * k, 0, 0], kneeL: [Math.max(0, 0.2 * k), 0, 0], kneeR: [Math.max(0, -0.2 * k), 0, 0], root: { z: 0.06 * k } }; }, // pushing a vacuum / broom back and forth
  flex: (t) => ({ ...arms(m([0, 0, 1.45 + 0.04 * S(t * 6)], [0, 0, 1.45 + 0.04 * S(t * 6 + 1)]), m([0, 0, 1.75], [0, 0, 1.75])), torso: [-0.05, 0, 0], head: [-0.08, 0, 0], root: { y: 0.005 * S(t * 12) } }), // double biceps
  punch: (t) => { const k = Math.max(0, S(t * 9)); const j = Math.max(0, -S(t * 9)); return { ...arms(m([-0.6 - 0.9 * j, 0, 0.2], [-0.6 - 0.9 * k, 0, 0.2]), m([-1.6 + 1.4 * j, 0, 0], [-1.6 + 1.4 * k, 0, 0])), torso: [0.1, 0.25 * (k - j), 0], hipL: [-0.2, 0, 0], kneeL: [0.25, 0, 0] }; },
  liftBarbell: (t) => { const k = 0.5 + 0.5 * S(t * 4); return { ...arms(m([-0.4 - 2.2 * k, 0, 0.35], [-0.4 - 2.2 * k, 0, 0.35]), m([-1.4 + 1.3 * k, 0, 0], [-1.4 + 1.3 * k, 0, 0])), head: [-0.1, 0, 0], hipL: [-0.15, 0, 0.1], hipR: [-0.15, 0, -0.1] }; },
  // ---- comedy clips ---------------------------------------------------------------------------------
  chestBeat: (t) => { const k = S(t * 22); return { ...arms(m([-1.1 - 0.25 * Math.max(0, k), -0.5, 0.25], [-1.1 - 0.25 * Math.max(0, -k), -0.5, 0.25]), m([-1.7, 0, 0], [-1.7, 0, 0])), torso: [-0.12, 0, 0.04 * k], head: [-0.3, 0, 0], root: { y: 0.01 * Math.abs(k) } }; },
  strut: (t, p = {}) => { const f = p.freq ?? 1.5; const w = CLIPS.walk(t, { freq: f, amp: 0.5 }); const ph = t * f * 2 * PI; return { ...w, torso: [-0.12, 0.18 * S(ph), 0.06 * S(ph)], head: [-0.18, -0.25 * S(ph), 0.08 * S(ph)], ...arms(m([0.9 * S(ph), 0, 0.25], [-0.9 * S(ph), 0, 0.25]), m([-0.6, 0, 0], [-0.6, 0, 0])), root: { y: 0.04 * Math.abs(S(ph)) } }; }, // proud naked strut
  tiptoe: (t, p = {}) => { const ph = t * 2 * PI * (p.freq ?? 1.1), a = Math.max(0, S(ph)), b = Math.max(0, -S(ph)); return { hipL: [-1.0 * a, 0, 0], kneeL: [1.6 * a, 0, 0], hipR: [-1.0 * b, 0, 0], kneeR: [1.6 * b, 0, 0], footL: [0.5, 0, 0], footR: [0.5, 0, 0], ...arms(m([-1.3, 0, 0.5], [-1.3, 0, 0.5]), m([-1.2, 0, 0], [-1.2, 0, 0])), handL: [1.0, 0, 0], handR: [1.0, 0, 0], torso: [0.25, 0, 0], head: [0.1, 0.4 * S(t * 1.3), 0], root: { y: 0.06 * (a + b) } }; }, // cartoon sneak
  flail: (t, p = {}) => { const r = CLIPS.run(t, { freq: p.freq ?? 3.8 }); return { ...r, ...arms(m([-PI * 2 * ((t * 3) % 1), 0, 0.3], [-PI * 2 * ((t * 3 + 0.5) % 1), 0, 0.3]), m([0, 0, 0], [0, 0, 0])), head: [-0.3, 0.3 * S(t * 15), 0] }; }, // windmill panic run
  doubleTake: (t) => { const k = t < 0.3 ? 0 : t < 0.5 ? (t - 0.3) / 0.2 : t < 0.7 ? 1 - (t - 0.5) / 0.2 : t < 0.8 ? (t - 0.7) / 0.1 : 1; const pop = t > 0.7 && t < 1.0 ? 0.12 * S((t - 0.7) / 0.3 * PI) : 0; return { ...CLIPS.stand(), head: [-0.1 * k, 0.9 * k, 0], torso: [0, 0.2 * k, 0], root: { y: pop } }; },
  selfStruggle: (t) => { const k = S(t * 11); return { ...arms(m([-0.9 + 0.35 * k, 0.3, 0.2], [-0.9 - 0.35 * k, 0.3, 0.2]), m([-1.2, 0, 0], [-1.2, 0, 0])), torso: [0.1, 0.22 * k, 0], head: [0.1, -0.2 * k, 0], root: { x: 0.03 * k } }; }, // one hand fights the other
  spinFall: (t, p = {}) => { const d = p.dur ?? 0.7, k = Math.min(1, t / d); return { root: { ry: k * PI * 4, rx: -PI / 2 * k * k, y: 0.5 * S(k * PI) + 0.12 * k, z: -1.2 * k }, ...arms(m([0, 0, 2.4], [0, 0, 2.4]), m([0, 0, 0], [0, 0, 0])), head: [-0.3, 0, 0] }; }, // knocked out spinning
  posing: (t) => { const i = Math.floor(t / 0.55) % 3; return i === 0 ? CLIPS.flex(t) : i === 1 ? { ...arms(m([0.2, 0, 0.9], [0.2, 0, 0.9]), m([0, 0.4, -1.9], [0, 0.4, -1.9])), torso: [-0.1, 0, 0], head: [-0.1, 0, 0] } : { ...arms(m([-0.4, 0.5, 0.3], [-0.2, 0, 0.6]), m([-1.6, 0, 0], [-1.3, 0, 0])), torso: [0.05, 0.6, 0], head: [0, -0.6, 0], hipL: [-0.3, 0, 0], kneeL: [0.5, 0, 0] }; }, // bodybuilder pose switch
  shovelFood: (t) => ({ ...CLIPS.sit(t), ...arms(m([-0.5, 0, 0.2], [-1.0 - 0.6 * Math.abs(S(t * 9)), 0, 0.1]), m([-1.2, 0, 0], [-1.6 - 0.6 * Math.abs(S(t * 9)), 0, 0])), head: [0.1 + 0.1 * S(t * 9), 0, 0], torso: [0.15, 0, 0] }),
  drunk: (t) => ({ ...CLIPS.sit(t), torso: [0.15 + 0.08 * S(t * 1.3), 0, 0.18 * S(t * 0.9)], head: [0.25 + 0.1 * S(t * 1.7), 0.2 * S(t * 0.7), 0.25 * S(t * 1.1)], ...arms(m([-0.9, 0, 0.1], [-0.3 + 0.2 * S(t * 2), 0, 0.3]), m([-0.9, 0, 0], [-0.5, 0, 0])) }), // swaying on a bar stool
  pushCart: (t, p = {}) => ({ ...CLIPS.walk(t, { freq: p.freq ?? 2.2, amp: 0.45 }), ...arms(m([-1.25, 0, 0.12], [-1.25, 0, 0.12]), m([-0.25, 0, 0], [-0.25, 0, 0])), torso: [0.25, 0, 0] }),
  phone: () => ({ ...arms(m([0, 0, 0.06], [-0.5, 0, 0.75]), m([-0.1, 0, 0], [-2.45, 0.2, 0])), head: [0, 0, -0.12] }),
  holdPhoneFront: () => ({ ...arms(m([0, 0, 0.06], [-1.1, 0, 0.1]), m([-0.1, 0, 0], [-1.1, 0, 0])), head: [0.35, 0, 0] }),
  binocs: (t) => ({ ...arms(m([-1.7, 0, -0.7], [-1.7, 0, -0.7]), m([-1.55, 0, 0], [-1.55, 0, 0])), head: [0.14, 0.08 * S(t * 0.7), 0], torso: [0.03, 0, 0] }), // binoculars at the eyes, slow scan
  talk: (t) => ({ head: [0.04 * S(t * 7), 0.06 * S(t * 2), 0], ...arms(m([0, 0, 0.06], [-0.6 - 0.15 * S(t * 4), 0, 0.15]), m([-0.1, 0, 0], [-1.2 + 0.2 * S(t * 4), 0.6, 0])) }),
  yell: (t) => ({ head: [-0.2 + 0.03 * S(t * 20), 0, 0], torso: [-0.08, 0, 0], ...arms(m([-0.2, 0, 0.5], [-0.2, 0, 0.5]), m([-1.3, 0, 0], [-1.3, 0, 0])), handL: [0, 0, 0], root: { y: 0.01 * S(t * 25) } }),
  nod: (t) => ({ head: [0.18 * Math.max(0, S(t * 8)), 0, 0], ...CLIPS.stand() }),
  shakeHead: (t) => ({ head: [0, 0.3 * S(t * 9), 0], ...CLIPS.stand() }),
  lookAround: (t) => ({ head: [0, 0.6 * S(t * 2.2), 0], torso: [0, 0.1 * S(t * 2.2), 0], ...CLIPS.stand() }),
  lookUp: (t) => ({ head: [-0.55, 0, 0], torso: [-0.08, 0, 0], ...CLIPS.stand() }),
  lookDown: () => ({ head: [0.5, 0, 0], ...CLIPS.stand() }),
  stareCamera: (t) => ({ ...CLIPS.stand(), head: [0.01 * S(t), 0, 0] }), // THE deadpan reaction hold
  angryFist: (t) => ({ ...arms(m([0, 0, 0.06], [-0.4, 0, 2.2]), m([-0.1, 0, 0], [0, 0, 0.6 + 0.3 * S(t * 14)])), head: [-0.1, 0, 0], torso: [-0.05, 0, 0] }),
  celebrate: (t) => ({ ...arms(m([0, 0, 2.7 + 0.15 * S(t * 10)], [0, 0, 2.7 + 0.15 * S(t * 10 + 1)]), m([0, 0, 0.3], [0, 0, 0.3])), root: { y: 0.08 * Math.abs(S(t * 5)) }, head: [-0.2, 0, 0] }),
  surrender: (t) => ({ ...arms(m([0, 0, 2.1], [0, 0, 2.1]), m([0, 0, -1.4], [0, 0, -1.4])), head: [0.05, 0, 0] }),
  handcuffed: () => ({ ...arms(m([0.45, 0, -0.15], [0.45, 0, -0.15]), m([-0.3, 0, 0.3], [-0.3, 0, 0.3])), head: [0.15, 0, 0] }),
  scared: (t) => ({ ...arms(m([-1.1, -0.4, 0.4], [-1.1, -0.4, 0.4]), m([-1.6, 0, 0], [-1.6, 0, 0])), hipL: [-0.25, 0, 0], hipR: [-0.25, 0, 0], kneeL: [0.5, 0, 0], kneeR: [0.5, 0, 0], torso: [0.15, 0, 0], root: { y: -0.04 + 0.006 * S(t * 40), x: 0.006 * S(t * 37) } }),
  pressGlass: (t) => ({ ...arms(m([-1.5, 0, 0.5], [-1.5, 0, 0.5]), m([-0.5, 0, 0], [-0.5, 0, 0])), handL: [0, 0, 0], head: [0.04 * S(t * 3), 0, 0] }), // trapped under a glass dome
  cry: (t) => ({ ...arms(m([-1.0, -0.3, 0.3], [-1.0, -0.3, 0.3]), m([-2.2, 0, 0], [-2.2, 0, 0])), head: [0.35 + 0.05 * S(t * 12), 0, 0], torso: [0.15, 0, 0], root: { y: 0.005 * S(t * 12) } }),
  dance: (t) => ({ ...arms(m([0, 0, 1.2 + 0.6 * S(t * 6)], [0, 0, 1.2 - 0.6 * S(t * 6)]), m([0, 0, 1.2], [0, 0, 1.2])), hipL: [-0.3 * Math.max(0, S(t * 6)), 0, 0], kneeL: [0.6 * Math.max(0, S(t * 6)), 0, 0], hipR: [-0.3 * Math.max(0, -S(t * 6)), 0, 0], kneeR: [0.6 * Math.max(0, -S(t * 6)), 0, 0], torso: [0, 0.3 * S(t * 3), 0.1 * S(t * 6)], root: { y: 0.03 * Math.abs(S(t * 6)) } }),
  sneak: (t, p = {}) => { return { ...CLIPS.walk(t, { freq: p.freq ?? 1.5, amp: 0.35 }), torso: [0.3, 0, 0], ...arms(m([-0.6, 0, 0.3], [-0.6, 0, 0.3]), m([-1.2, 0, 0], [-1.2, 0, 0])), root: { y: -0.05 } }; },

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
  flee: (t, p = {}) => { const r = CLIPS.run(t, { freq: p.freq ?? 3.6 }); return { ...r, ...arms(m([-0.3, 0, 2.6 + 0.2 * S(t * 20)], [-0.3, 0, 2.6 + 0.2 * S(t * 20 + 1)]), m([0, 0, 0.4], [0, 0, 0.4])) }; }, // panic, arms in the air
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

  // --- v3 action library: sharp, rigid gestures (0.35–0.8 s), whole body involved -------------------
  // root.pivot = 'hips' -> director3 rotates the body about the hips instead of the feet.
  knuckleWalk: (t, p = {}) => { const ph = t * (p.freq ?? 1.6) * 2 * PI; return {
    torso: [1.05, 0.1 * S(ph), 0], head: [-0.95, 0, 0], neck: [0, 0, 0],
    ...arms(m([-1.25 + 0.5 * S(ph), 0, 0.12], [-1.25 - 0.5 * S(ph), 0, 0.12]), m([-0.15, 0, 0], [-0.15, 0, 0])),
    hipL: [-0.75 + 0.4 * S(ph + PI), 0, 0.08], hipR: [-0.75 + 0.4 * S(ph), 0, -0.08],
    kneeL: [1.0 + 0.35 * Math.max(0, S(ph)), 0, 0], kneeR: [1.0 + 0.35 * Math.max(0, -S(ph)), 0, 0],
    root: { y: -0.3 + 0.025 * Math.abs(S(ph)) } }; },
  hangBar: (t) => ({ ...arms(m([-2.95, 0, 0.18], [-2.95, 0, 0.18]), m([-0.05, 0, 0], [-0.05, 0, 0])), hipL: [-0.15, 0, 0], hipR: [-0.1, 0, 0], kneeL: [0.5, 0, 0], kneeR: [0.6, 0, 0], head: [-0.15, 0, 0] }),
  pullUp: (t, p = {}) => { const k = 0.5 - 0.5 * C(t * (p.freq ?? 1.2) * 2 * PI); return {
    ...arms(m([-2.95 + 0.55 * k, 0, 0.18 + 0.5 * k], [-2.95 + 0.55 * k, 0, 0.18 + 0.5 * k]), m([-1.9 * k, 0, 0], [-1.9 * k, 0, 0])),
    hipL: [-0.2, 0, 0], hipR: [-0.15, 0, 0], kneeL: [0.6, 0, 0], kneeR: [0.7, 0, 0], head: [-0.25 + 0.15 * k, 0, 0], torso: [-0.05, 0, 0],
    root: { y: 0.42 * k } }; },
  swingPole: (t, p = {}) => { const sd = p.side ?? 1; return { // one hand on the pole, body flung out sideways
    shoulderR: [-2.7, 0, -0.35 * sd], elbowR: [0, 0, 0], shoulderL: [-0.3, 0, 1.6], elbowL: [0, 0, 0.2],
    hipL: [-0.5, 0, 0.25], hipR: [-0.35, 0, -0.1], kneeL: [0.7, 0, 0], kneeR: [0.4, 0, 0], torso: [0, 0, -0.15 * sd], head: [-0.1, 0, 0.2 * sd],
    root: { rz: 0.45 * sd, y: 0.25, pivot: 'hips' } }; },
  flip: (t, p = {}) => { const d = p.dur ?? 0.75, k = Math.min(1, Math.max(0, t / d)), ke = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
    const tuck = Math.sin(Math.min(1, k) * PI); return { // backflip in place
    root: { rx: -2 * PI * ke, y: 4 * (p.height ?? 0.85) * k * (1 - k), pivot: 'hips' },
    hipL: [-1.6 * tuck, 0, 0.05], hipR: [-1.6 * tuck, 0, -0.05], kneeL: [2.0 * tuck, 0, 0], kneeR: [2.0 * tuck, 0, 0],
    ...arms(m([-1.2 * tuck - 0.6 * (1 - tuck), 0, 0.3], [-1.2 * tuck - 0.6 * (1 - tuck), 0, 0.3]), m([-1.2 * tuck, 0, 0], [-1.2 * tuck, 0, 0])), head: [0.4 * tuck, 0, 0] }; },
  cartwheel: (t, p = {}) => { const d = p.dur ?? 0.8, k = Math.min(1, Math.max(0, t / d)); return {
    root: { rz: -2 * PI * k, y: 0.25 * S(k * PI), pivot: 'hips' },
    ...arms(m([0, 0, 2.8], [0, 0, 2.8]), m([0, 0, 0], [0, 0, 0])), hipL: [0, 0, 0.6], hipR: [0, 0, -0.6] }; },
  vault: () => ({ ...arms(m([-1.0, 0, 0.25], [-1.0, 0, 0.25]), m([-0.1, 0, 0], [-0.1, 0, 0])), hipL: [-1.3, 0, 0.4], hipR: [-1.1, 0, 0.3], kneeL: [1.2, 0, 0], kneeR: [1.0, 0, 0], torso: [0.25, 0, 0.15] }),
  airborne: () => ({ ...arms(m([-0.4, 0, 1.4], [-0.4, 0, 1.4]), m([0, 0, 0.3], [0, 0, 0.3])), hipL: [-0.6, 0, 0], hipR: [-0.2, 0, 0], kneeL: [1.1, 0, 0], kneeR: [0.6, 0, 0], head: [-0.15, 0, 0] }),
  land: (t) => { const k = Math.max(0, 1 - t / 0.35); return { hipL: [-0.9 * k, 0, 0.05], hipR: [-0.9 * k, 0, -0.05], kneeL: [1.6 * k, 0, 0], kneeR: [1.6 * k, 0, 0], torso: [0.35 * k, 0, 0], ...arms(m([-0.6 * k, 0, 0.5 * k + 0.2], [-0.6 * k, 0, 0.5 * k + 0.2]), m([-0.4, 0, -0.3], [-0.4, 0, -0.3])), root: { y: -0.32 * k } }; },
  tantrum: (t) => { const ph = t * 2 * PI * 2.4, a = Math.max(0, S(ph)), b = Math.max(0, -S(ph)); return {
    hipL: [-0.75 * a, 0, 0], kneeL: [1.2 * a, 0, 0], hipR: [-0.75 * b, 0, 0], kneeR: [1.2 * b, 0, 0],
    ...arms(m([-0.5, 0, 0.55 + 0.15 * S(t * 26)], [-0.5, 0, 0.55 + 0.15 * S(t * 26 + 1)]), m([-1.7, 0, 0], [-1.7, 0, 0])),
    torso: [0.18, 0, 0.08 * S(ph)], head: [-0.15, 0.35 * S(t * 15), 0], root: { y: 0.04 * (a + b) } }; },
  injectArm: (t) => { const push = t > 0.45 ? Math.min(1, (t - 0.45) / 0.12) : 0; return { // syringe (right hand) into the left forearm
    shoulderL: [-1.3, 0, 0.12], elbowL: [-0.4, 0, 0], handL: [0, 0, -0.3],
    shoulderR: [-1.15, 0.8, -0.1], elbowR: [-1.35 - 0.12 * push, 0, 0], handR: [0.3, 0, 0],
    head: [0.5, 0.3, 0], torso: [0.12, 0.15, 0], root: { y: -0.01 * push } }; },
  injectButt: (t) => { const push = t > 0.4 ? Math.min(1, (t - 0.4) / 0.12) : 0; return {
    shoulderR: [0.55, 0, -0.35], elbowR: [-1.2 - 0.15 * push, 0, 0], shoulderL: [0, 0, 0.25], elbowL: [-0.2, 0, 0],
    torso: [0.2, -0.5, 0], head: [0.1, -0.9, 0], hipR: [0.15, 0, 0] }; },
  drinkUp: (t) => { const k = Math.min(1, t / 0.3); return { // bottle / tub to the mouth, head thrown back
    shoulderR: [-2.0 * k, -0.35 * k, 0.15], elbowR: [-2.05 * k, 0, 0], shoulderL: [0, 0, 0.25], elbowL: [-0.3, 0, -0.2],
    head: [-0.55 * k, 0, 0], torso: [-0.12 * k, 0, 0] }; },
  wired: (t) => ({ // after the forbidden pre-workout: rigid, shaking, eyes wide
    ...arms(m([-0.2, 0, 0.45], [-0.2, 0, 0.45]), m([-1.2, 0, 0], [-1.2, 0, 0])), torso: [-0.05, 0, 0.03 * S(t * 47)], head: [-0.1, 0.06 * S(t * 41), 0.04 * S(t * 37)],
    root: { x: 0.012 * S(t * 53), y: 0.008 * S(t * 61) }, hipL: [-0.1, 0, 0.1], hipR: [-0.1, 0, -0.1] }),
  eatHands: (t, p = {}) => { const ph = t * 2 * PI * (p.freq ?? 1.6), a = Math.max(0, S(ph)), b = Math.max(0, -S(ph)); return {
    shoulderL: [-0.7 - 1.2 * a, -0.3 * a, 0.15], elbowL: [-0.9 - 1.1 * a, 0, 0], shoulderR: [-0.7 - 1.2 * b, 0.3 * b, -0.15], elbowR: [-0.9 - 1.1 * b, 0, 0],
    head: [0.15 - 0.1 * (a + b), 0, 0], torso: [0.1, 0, 0] }; },
  sitFloor: (t) => ({ hipL: [-1.45, 0, 0.55], hipR: [-1.45, 0, -0.55], kneeL: [2.35, 0, 0], kneeR: [2.35, 0, 0], ...arms(m([-0.5, 0, 0.35], [-0.5, 0, 0.35]), m([-0.7, 0, 0], [-0.7, 0, 0])), torso: [0.12, 0, 0], head: [0.02 * S(t), 0, 0], root: { y: -0.8 } }),
  sitFloorEat: (t, p = {}) => ({ ...CLIPS.sitFloor(t), ...(() => { const e = CLIPS.eatHands(t, p); return { shoulderL: e.shoulderL, elbowL: e.elbowL, shoulderR: e.shoulderR, elbowR: e.elbowR, head: e.head }; })() }),
  sleepSide: (t) => ({ root: { rz: -1.5, y: -0.82, pivot: 'hips' }, hipL: [-1.0, 0, 0], hipR: [-1.2, 0, 0], kneeL: [1.6, 0, 0], kneeR: [1.7, 0, 0], ...arms(m([-1.3, 0, 0], [-1.5, 0, 0]), m([-1.2, 0, 0], [-1.4, 0, 0])), head: [0.3, 0, 0], torso: [0.2 + 0.02 * S(t * 1.2), 0, 0] }),
  lieBack: (t) => ({ root: { rx: -PI / 2, y: -0.88, pivot: 'hips' }, ...arms(m([0, 0, 0.5], [0, 0, 0.5]), m([0, 0, 0], [0, 0, 0])), head: [-0.1 + 0.02 * S(t), 0, 0] }),
  koFloor: (t) => ({ root: { rx: -PI / 2, y: -0.88, pivot: 'hips' }, ...arms(m([0, 0, 1.6], [0, 0, 1.4]), m([0, 0, 0.4], [0, 0, 0.2])), hipL: [0, 0, 0.35], hipR: [0, 0, -0.35], head: [0.1, 0.35 * S(t * 3), 0] }),
  hitFly: (t) => ({ ...arms(m([-1.4, 0, 0.9], [-1.4, 0, 0.9]), m([0, 0, 0], [0, 0, 0])), hipL: [-1.1, 0, 0.2], hipR: [-0.8, 0, -0.2], kneeL: [0.4, 0, 0], kneeR: [0.6, 0, 0], torso: [-0.5, 0, 0], head: [-0.4, 0, 0], root: { rx: 0.6, pivot: 'hips' } }),
  windupPunch: (t, p = {}) => { const hit = p.hit ?? 0.35; const wind = Math.min(1, t / hit), strike = t > hit ? Math.min(1, (t - hit) / 0.08) : 0; return {
    shoulderR: [-0.3 - 1.25 * strike + 0.5 * wind * (1 - strike), 0, 0.2], elbowR: [-1.8 * (1 - strike) * wind - 0.1, 0, 0],
    shoulderL: [-1.0, 0, 0.3], elbowL: [-1.6, 0, 0], torso: [0.1, -0.45 * wind * (1 - strike) + 0.35 * strike, 0], head: [0, 0.2 * wind * (1 - strike) - 0.2 * strike, 0],
    hipL: [-0.35, 0, 0], kneeL: [0.4, 0, 0], hipR: [0.25 * strike, 0, 0] }; },
  kneelBow: (t) => ({ ...CLIPS.kneel(t), torso: [0.75, 0, 0], head: [0.3, 0, 0], ...arms(m([-1.4, 0, 0.15], [-1.4, 0, 0.15]), m([-0.2, 0, 0], [-0.2, 0, 0])) }),
  fan: (t) => ({ shoulderR: [-1.6 + 0.35 * S(t * 12), 0, 0.3], elbowR: [-0.6, 0, 0], shoulderL: [0, 0, 0.2], elbowL: [-0.2, 0, -0.3], head: [0.05, -0.2, 0] }),
  phoneCall: (t) => ({ shoulderR: [-0.55, 0, 0.75], elbowR: [-2.45, 0.2, 0], shoulderL: [-0.6 - 0.25 * Math.max(0, S(t * 3.3)), 0, 0.35], elbowL: [-1.2 + 0.3 * S(t * 3.3), 0.5, 0], head: [0.05 * S(t * 5), 0, -0.12], torso: [0, 0.08 * S(t * 1.7), 0] }),
  whistleBlow: (t) => ({ shoulderR: [-1.15, 0.6, 0], elbowR: [-2.3, 0, 0], shoulderL: [-1.45, -0.1, 0.1], elbowL: [0, 0, 0], head: [-0.1, 0, 0], torso: [-0.05, 0, 0] }),
  clipboard: (t) => ({ shoulderL: [-0.75, -0.45, 0.1], elbowL: [-1.6, 0, 0], shoulderR: [-0.85, 0.4, -0.05], elbowR: [-1.5 - 0.06 * S(t * 18), 0, 0], head: [0.35, 0, 0] }),
  cuffOther: (t) => { const k = Math.min(1, t / 0.3); return { ...arms(m([-1.0 * k, -0.25 * k, 0.1], [-1.0 * k, -0.25 * k, 0.1]), m([-0.5 * k, 0, 0], [-0.5 * k, 0, 0])), torso: [0.25 * k, 0, 0], head: [0.35 * k, 0, 0] }; },
  cuffedFront: () => ({ ...arms(m([-0.45, -0.35, 0.05], [-0.45, -0.35, 0.05]), m([-0.7, 0, 0], [-0.7, 0, 0])), head: [0.18, 0, 0], torso: [0.05, 0, 0] }),
  cuffedBack: () => ({ ...arms(m([0.55, 0, -0.1], [0.55, 0, -0.1]), m([-0.5, 0, 0.35], [-0.5, 0, 0.35])), head: [0.12, 0, 0], torso: [-0.05, 0, 0] }),
  podium: (t) => ({ shoulderR: [-1.6, 0, 0.25], elbowR: [-1.0, 0, 0.35 * S(t * 7)], handR: [0, 0, 0.4 * S(t * 7)], shoulderL: [-0.75, 0, 0.1], elbowL: [-0.6, 0, 0], head: [0, 0.15 * S(t * 3.5), 0] }),
  giveItem: (t) => { const k = Math.min(1, t / 0.35); return { shoulderR: [-1.25 * k, 0.1, 0.1], elbowR: [-0.25 - 0.5 * (1 - k), 0, 0], shoulderL: [0, 0, 0.2], elbowL: [-0.2, 0, -0.3], torso: [0.08 * k, 0, 0], head: [0.1, 0, 0] }; },
  takeItem: (t) => { const k = Math.min(1, t / 0.35); return { shoulderR: [-1.2 * (1 - k * 0.4), 0.15, 0.1], elbowR: [-0.3 - 0.9 * k, 0, 0], shoulderL: [0, 0, 0.2], elbowL: [-0.2, 0, -0.3], head: [0.25, 0, 0] }; },
  drawOn: (t) => ({ shoulderR: [-1.55, 0.2, 0.1], elbowR: [-0.5 + 0.12 * S(t * 16), 0, 0.1 * C(t * 16)], shoulderL: [-0.3, 0, 0.3], elbowL: [-1.4, 0, 0], head: [0.05, 0.1, 0], torso: [0.12, 0, 0] }),
  pour: (t) => ({ shoulderR: [-1.25, 0.3, 0.1], elbowR: [-0.6, 0, 0], handR: [0, 0, -0.9], shoulderL: [-1.05, -0.2, 0.1], elbowL: [-0.9, 0, 0], head: [0.4, 0, 0] }),
  wipeGlass: (t) => ({ shoulderR: [-0.95, 0.35, 0.05], elbowR: [-1.35 + 0.15 * S(t * 9), 0, 0.2 * S(t * 9)], shoulderL: [-0.95, -0.35, 0.05], elbowL: [-1.3, 0, 0], head: [0.3, 0, 0] }),
  drive: (t) => ({ ...CLIPS.sit(t), ...arms(m([-1.25, 0, 0.12], [-1.25, 0, 0.12]), m([-0.35 + 0.05 * S(t * 2), 0, 0], [-0.35 - 0.05 * S(t * 2), 0, 0])), head: [0, 0.08 * S(t * 0.7), 0] }),
  crouchHide: (t) => ({ hipL: [-1.2, 0, 0.1], hipR: [-1.2, 0, -0.1], kneeL: [2.0, 0, 0], kneeR: [2.0, 0, 0], torso: [0.6, 0, 0], head: [-0.4, 0.25 * S(t * 1.6), 0], ...arms(m([-1.0, 0, 0.2], [-1.0, 0, 0.2]), m([-1.3, 0, 0], [-1.3, 0, 0])), root: { y: -0.45 } }),
  boxSneak: (t, p = {}) => { const ph = t * 2 * PI * (p.freq ?? 1.8), a = Math.max(0, S(ph)), b = Math.max(0, -S(ph)); return { // crouched shuffle under a cardboard box
    hipL: [-0.9 - 0.35 * a, 0, 0.1], hipR: [-0.9 - 0.35 * b, 0, -0.1], kneeL: [1.6 + 0.3 * a, 0, 0], kneeR: [1.6 + 0.3 * b, 0, 0],
    torso: [0.7, 0, 0], head: [-0.5, 0, 0], ...arms(m([-1.5, 0, 0.3], [-1.5, 0, 0.3]), m([-0.9, 0, 0], [-0.9, 0, 0])), root: { y: -0.4 + 0.02 * (a + b) } }; },
  boxFreeze: () => ({ hipL: [-1.3, 0, 0.1], hipR: [-1.3, 0, -0.1], kneeL: [2.2, 0, 0], kneeR: [2.2, 0, 0], torso: [0.75, 0, 0], head: [-0.5, 0, 0], ...arms(m([-1.5, 0, 0.3], [-1.5, 0, 0.3]), m([-0.9, 0, 0], [-0.9, 0, 0])), root: { y: -0.52 } }),
  lookBack: (t) => ({ ...CLIPS.stand(), torso: [0, 0.55, 0], head: [0, 0.95, 0] }),
  benchPress: (t, p = {}) => { const k = 0.5 - 0.5 * C(t * (p.freq ?? 0.9) * 2 * PI); return {
    root: { rx: -PI / 2, y: -0.48, pivot: 'hips' }, ...arms(m([-1.0 - 0.57 * k, 0, 0.55 - 0.35 * k], [-1.0 - 0.57 * k, 0, 0.55 - 0.35 * k]), m([-1.5 * (1 - k), 0, 0], [-1.5 * (1 - k), 0, 0])),
    hipL: [1.25, 0, 0.15], hipR: [1.25, 0, -0.15], kneeL: [0.1, 0, 0], kneeR: [0.1, 0, 0], head: [-0.15, 0, 0] }; },
  deadlift: (t, p = {}) => { const k = 0.5 - 0.5 * C(t * (p.freq ?? 0.8) * 2 * PI); return {
    hipL: [-1.0 * (1 - k), 0, 0.12], hipR: [-1.0 * (1 - k), 0, -0.12], kneeL: [1.0 * (1 - k), 0, 0], kneeR: [1.0 * (1 - k), 0, 0], torso: [0.9 * (1 - k), 0, 0], head: [-0.6 * (1 - k), 0, 0],
    ...arms(m([-0.9 * (1 - k), 0, 0.12], [-0.9 * (1 - k), 0, 0.12]), m([0, 0, 0], [0, 0, 0])), root: { y: -0.28 * (1 - k) } }; },
  curls: (t, p = {}) => { const ph = t * 2 * PI * (p.freq ?? 1.1), a = Math.max(0, S(ph)), b = Math.max(0, -S(ph)); return { ...arms(m([-0.15, 0, 0.12], [-0.15, 0, 0.12]), m([-2.2 * a, 0, 0], [-2.2 * b, 0, 0])), torso: [-0.04, 0, 0], head: [0.1, 0, 0] }; },
  scratchButt: (t) => ({ shoulderR: [0.5, 0, -0.25], elbowR: [-1.1 + 0.2 * S(t * 15), 0, 0], shoulderL: [0, 0, 0.2], elbowL: [-0.3, 0, -0.2], torso: [0.1, -0.15, 0], head: [-0.2, 0.3, 0.1] }),
  bigShrug: (t) => ({ ...arms(m([-0.3, 0, 0.75], [-0.3, 0, 0.75]), m([-1.2, 1.2, 0], [-1.2, 1.2, 0])), handL: [0, 1.3, 0], handR: [0, -1.3, 0], head: [0, 0, 0.25], root: { y: 0.03 } }),
  growl: (t) => ({ torso: [0.35, 0, 0], head: [-0.45, 0, 0], ...arms(m([-0.8, 0, 0.7], [-0.8, 0, 0.7]), m([-1.2, 0, 0], [-1.2, 0, 0])), hipL: [-0.4, 0, 0.15], hipR: [-0.4, 0, -0.15], kneeL: [0.6, 0, 0], kneeR: [0.6, 0, 0], root: { y: -0.12 + 0.01 * S(t * 30) } }),
  pokeFinger: (t) => { const k = 0.5 + 0.5 * S(t * 8); return { shoulderR: [-1.4, 0.15, 0.05], elbowR: [-0.4 * (1 - k), 0, 0], shoulderL: [0, 0, 0.2], elbowL: [-0.3, 0, -0.2], torso: [0.1 * k, 0, 0], head: [0.1, 0, 0] }; },
  sitTalk: (t) => ({ ...CLIPS.sit(t), shoulderR: [-0.9 - 0.2 * S(t * 4), 0, 0.15], elbowR: [-1.1 + 0.25 * S(t * 4), 0.6, 0], head: [0.04 * S(t * 7), 0.08 * S(t * 2), 0] }),
  pushCartWalk: (t, p = {}) => ({ ...CLIPS.walk(t, { freq: p.freq ?? 2.0, amp: 0.4 }), ...arms(m([-1.2, 0, 0.12], [-1.2, 0, 0.12]), m([-0.3, 0, 0], [-0.3, 0, 0])), torso: [0.22, 0, 0], head: [-0.1, 0, 0] }),
  carryBox: (t, p = {}) => ({ ...CLIPS.walk(t, { freq: p.freq ?? 1.9, amp: 0.38 }), ...arms(m([-1.1, -0.15, 0.1], [-1.1, -0.15, 0.1]), m([-0.7, 0, 0], [-0.7, 0, 0])) }),

  tipOverSit: (t, p = {}) => { const k = Math.min(1, Math.max(0, t / (p.dur ?? 0.7))); const s = CLIPS.sit(t); return { ...s, ...arms(m([-0.6, 0, 0.4 + 1.6 * k], [-1.0, 0, 0.3 + 1.2 * k]), m([-0.4, 0, 0], [-0.8, 0, 0])), head: [-0.3 * k, 0, 0.3 * k], root: { y: -0.45, rz: -1.15 * k * k, pivot: 'hips' } }; },
  yawnStretch: () => ({ ...arms(m([-0.3, 0, 2.6], [-0.3, 0, 2.6]), m([0, 0, 0.6], [0, 0, 0.6])), torso: [-0.15, 0, 0], head: [-0.35, 0, 0] }),
  heroPose: () => ({ ...arms(m([0.15, 0, 0.75], [0.15, 0, 0.75]), m([0, 0.3, -2.0], [0, 0.3, -2.0])), handL: [0, 0, 0.6], handR: [0, 0, -0.6], torso: [-0.12, 0, 0], head: [-0.2, 0.25, 0], hipL: [0, 0, 0.15], hipR: [0, 0, -0.15] }),
  waveFace: (t) => ({ shoulderR: [-1.5, 0.15, 0.1], elbowR: [-0.3, 0, 0.5 * S(t * 10)], handR: [0, 0, 0.5 * S(t * 10)], shoulderL: [0, 0, 0.2], elbowL: [-0.2, 0, -0.3], head: [0.05, 0, 0.1], torso: [0.1, 0, 0] }),
  beckon: (t) => ({ ...CLIPS.sit(t), shoulderR: [-1.1, 0, 0.1], elbowR: [-1.2 - 0.5 * Math.max(0, S(t * 8)), 0, 0], handR: [0, 0, 0] }),
  sitShow: (t) => ({ ...CLIPS.sit(t), shoulderR: [-1.15, 0.1, 0.15], elbowR: [-0.75, 0, 0], shoulderL: [-0.7, 0, 0.1], elbowL: [-0.8, 0, 0], head: [0.12, -0.15, 0] }),
  sitPoint: (t) => ({ ...CLIPS.sit(t), shoulderR: [-1.45, -0.3, 0.1], elbowR: [-0.05, 0, 0], head: [-0.05, -0.3, 0] }),
  sitHoldUp: (t) => ({ ...CLIPS.sit(t), shoulderR: [-1.8, 0, 0.2], elbowR: [-0.9, 0, 0], shoulderL: [-0.7, 0, 0.1], elbowL: [-0.8, 0, 0], head: [-0.05, 0, 0] }),
  sitGive: (t) => { const k = Math.min(1, t / 0.4); return { ...CLIPS.sit(t), shoulderR: [-0.7 - 0.6 * k, 0.15, 0.1], elbowR: [-0.8 + 0.5 * k, 0, 0], torso: [0.1 * k, 0, 0] }; },
  sitTake: (t) => { const k = Math.min(1, t / 0.35); return { ...CLIPS.sit(t), shoulderR: [-1.25 + 0.4 * k, -0.1, 0.1], elbowR: [-0.3 - 1.0 * k, 0, 0], head: [0.3, 0, 0] }; },
  sitLookItem: (t) => ({ ...CLIPS.sit(t), shoulderR: [-0.85, 0.35, 0.05], elbowR: [-1.35, 0, 0], head: [0.45, 0.15, 0] }),
  // --- felt pen / yogurt gags ("son nom dessus") ------------------------------------
  writeOnHeld: (t) => ({ ...CLIPS.stand(), shoulderL: [-0.55, -0.35, 0.1], elbowL: [-1.05, 0, 0], shoulderR: [-0.6, 0.85, -0.05], elbowR: [-1.25 + 0.12 * S(t * 16), 0.1 * C(t * 16), 0], head: [0.42, 0, 0], torso: [0.08, 0, 0] }), // pot in the left hand, writing on it
  drawMid: (t) => ({ ...CLIPS.stand(), shoulderR: [-0.75, 0.3, 0.05], elbowR: [-0.35 + 0.14 * S(t * 16), 0, 0.1 * C(t * 16)], torso: [0.3, 0, 0], head: [0.15, 0.1, 0] }), // leaning, writing at waist-chest height (chair back)
  drawLow: (t) => ({ ...CLIPS.kneel(t), shoulderR: [-0.95, 0.25, 0.05], elbowR: [-0.3 + 0.14 * S(t * 16), 0, 0.1 * C(t * 16)], shoulderL: [-0.4, 0, 0.3], elbowL: [-0.9, 0, 0], torso: [0.3, 0, 0], head: [0.1, 0.1, 0] }), // crouched tagger (car door)
  drawUp: (t) => ({ ...CLIPS.stand(), shoulderR: [-2.1, 0.3, 0.05], elbowR: [-0.3 + 0.14 * S(t * 16), 0, 0.1 * C(t * 16)], shoulderL: [-0.2, 0, 0.3], elbowL: [-0.6, 0, 0], head: [-0.25, 0.05, 0], root: { y: 0.04 } }), // reaching up
  sitDraw: (t) => ({ ...CLIPS.sit(t), shoulderR: [-1.35, 0.25, 0.1], elbowR: [-0.4 + 0.12 * S(t * 16), 0, 0.1 * C(t * 16)], torso: [0.25, 0, 0], head: [0.1, 0.1, 0] }),
  eatSpoon: (t, p = {}) => { const a = Math.max(0, S(t * 2 * PI * (p.freq ?? 1.4))); return { ...CLIPS.stand(), shoulderL: [-0.55, -0.45, 0.1], elbowL: [-1.05, 0, 0], shoulderR: [-0.6 - 0.7 * a, 0.4, -0.05], elbowR: [-1.2 - 1.0 * a, 0, 0], head: [0.15 - 0.15 * a, 0, 0], torso: [0.04, 0, 0] }; },
  sitEatSpoon: (t, p = {}) => { const e = CLIPS.eatSpoon(t, p); return { ...CLIPS.sit(t), shoulderL: e.shoulderL, elbowL: e.elbowL, shoulderR: e.shoulderR, elbowR: e.elbowR, head: e.head }; },
  walkEat: (t, p = {}) => { const w = CLIPS.walk(t, { freq: p.freq ?? 1.6, amp: 0.3 }), e = CLIPS.eatSpoon(t, { freq: 1.7 }); return { ...w, shoulderL: e.shoulderL, elbowL: e.elbowL, shoulderR: e.shoulderR, elbowR: e.elbowR, head: e.head }; },
  sitSip: (t) => ({ ...CLIPS.sit(t), shoulderR: [-1.0, 0.45, -0.05], elbowR: [-1.9, 0, 0], head: [-0.18, 0, 0] }),
  kneelGive: (t) => { const k = Math.min(1, t / 0.35); return { ...CLIPS.kneel(t), shoulderR: [-1.45 * k, 0.1, 0.1], elbowR: [-0.3, 0, 0], shoulderL: [-1.2 * k, -0.1, 0.1], elbowL: [-0.4, 0, 0], torso: [0.05, 0, 0], head: [-0.15, 0, 0] }; },
  kneelMassage: (t) => { const k = 0.5 + 0.5 * S(t * 11); return { ...CLIPS.kneel(t), ...arms(m([-0.9 - 0.15 * k, -0.15, 0.1], [-0.9 - 0.15 * (1 - k), -0.15, 0.1]), m([-0.5, 0, 0], [-0.5, 0, 0])), torso: [0.45, 0, 0], head: [0.15, 0, 0] }; },
  carryBags: (t, p = {}) => { const f = p.freq ?? 1.8, ph = t * 2 * PI * f, w = CLIPS.walk(t, { freq: f, amp: 0.32 }); return { ...w, ...arms(m([0.08 * S(ph), 0, 0.3], [-0.08 * S(ph), 0, 0.3]), m([-0.12, 0, 0], [-0.12, 0, 0])), torso: [0.1, 0, 0] }; },
  holdBags: (t) => ({ ...CLIPS.stand(), ...arms(m([0, 0, 0.3], [0, 0, 0.3]), m([-0.12, 0, 0], [-0.12, 0, 0])), torso: [0.08, 0, 0], head: [0.01 * S(t), 0, 0] }),
  bow: (t) => { const k = Math.min(1, t / 0.3); return { ...CLIPS.stand(), torso: [0.85 * k, 0, 0], head: [0.2 * k, 0, 0], ...arms(m([0.15 * k, 0, 0.1], [0.15 * k, 0, 0.1]), m([-0.2, 0, 0], [-0.2, 0, 0])) }; }, // deep servile bow
  pointDown: (t) => ({ ...arms(m([0, 0, 0.08], [-0.75 + 0.05 * S(t * 3), 0.2, 0.1]), m([-0.1, 0, 0], [-0.05, 0, 0])), head: [0.3, 0, 0], torso: [0.08, 0, 0] }), // "à genoux"
  showMarker: (t) => ({ ...CLIPS.stand(), shoulderR: [-0.45, 0.15, -0.3], elbowR: [-2.15 + 0.06 * S(t * 9), 0, 0], shoulderL: [0, 0, 0.15], elbowL: [-0.3, 0, 0], head: [-0.06, -0.12, 0.05] }), // brandishes a marker beside the face
  showMarkerL: (t) => ({ ...CLIPS.stand(), shoulderL: [-0.45, -0.15, 0.3], elbowL: [-2.15 + 0.06 * S(t * 9), 0, 0], shoulderR: [0, 0, -0.15], elbowR: [-0.3, 0, 0], head: [-0.06, 0.12, -0.05] }),
  lookItem: (t) => ({ ...CLIPS.stand(), shoulderR: [-0.85, 0.35, 0.05], elbowR: [-1.35, 0, 0], head: [0.45, 0.15, 0] }),

  // --- creature/monster helper (vampire lurk, claw reach) -----------------
  lurk: (t) => ({ torso: [0.2, 0, 0], head: [0.1, 0.05 * S(t), 0], ...arms(m([-0.9, 0, 0.1], [-0.35, 0, 0.1]), m([-0.7, 0, 0], [-0.3, 0, 0])), handL: [0.6, 0, 0], root: { y: -0.02 } }),
  clawReach: (t) => { const k = Math.min(1, t / 0.6); return { ...arms(m([-1.5 * k, 0, 0.1], [0, 0, 0.06]), m([-0.1, 0, 0], [-0.1, 0, 0])), handL: [0.5, 0, 0], torso: [0.1, 0, 0] }; },
};

export const CLIP_NAMES = Object.keys(CLIPS);

const JOINTS = ['hips', 'torso', 'neck', 'head', 'shoulderL', 'elbowL', 'handL', 'shoulderR', 'elbowR', 'handR', 'hipL', 'kneeL', 'footL', 'hipR', 'kneeR', 'footR'];

export function samplePose(name, t, params) {
  const f = CLIPS[name] || CLIPS.idle; return f(Math.max(0, t), params || {});
}

// Acting transition between two poses (motion-design principles):
//   anticipation  : first ~4 frames move 15% AWAY from the target
//   overshoot     : ease-out-back (~8%) then settle
//   overlap       : head leads (+3 frames), hands/forearms trail (-2 frames), legs neutral
const LEAD = { head: 0.1, neck: 0.06, torso: 0.03, shoulderL: 0, shoulderR: 0, elbowL: -0.05, elbowR: -0.05, handL: -0.08, handR: -0.08 };
export function actingWeight(dt, { dur = 0.32, anticipation = 0.15, antDur = 0.13, overshoot = 1.2 } = {}) {
  if (dt <= 0) return 0;
  if (dt < antDur) return -anticipation * Math.sin(Math.PI * dt / antDur * 0.5) ; // ease away
  const k = Math.min(1, (dt - antDur) / dur);
  const c1 = overshoot, c3 = c1 + 1; // easeOutBack
  return -anticipation * (1 - k) + (1 + c3 * Math.pow(k - 1, 3) + c1 * Math.pow(k - 1, 2)) * (1 + anticipation * (1 - k)) - (1 - k) * 0;
}
export function actingBlend(a, b, dt, opts = {}) {
  const out = {};
  for (const j of JOINTS) {
    const w = actingWeight(dt + (LEAD[j] || 0), opts);
    const pa = a[j] || [0, 0, 0], pb = b[j] || [0, 0, 0];
    out[j] = [pa[0] + (pb[0] - pa[0]) * w, pa[1] + (pb[1] - pa[1]) * w, pa[2] + (pb[2] - pa[2]) * w];
  }
  const w = Math.max(0, Math.min(1.05, actingWeight(dt, { ...opts, anticipation: 0 })));
  const ra = a.root || {}, rb = b.root || {}; out.root = {};
  for (const k of ['x', 'y', 'z', 'rx', 'ry', 'rz']) out.root[k] = (ra[k] || 0) + ((rb[k] || 0) - (ra[k] || 0)) * w;
  out.root.sx = rb.sx; out.root.sy = rb.sy;
  return out;
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
  const sc = base.scale || 1; human.scale.set(sc, sc, sc);
}
