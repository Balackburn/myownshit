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
  explain: (t) => ({ ...arms(m([-0.38, 0.0, 0.28], [-0.38, 0.0, 0.28]), m([-1.2 + 0.06 * S(t * 3.1), 0.35, 0], [-1.2 + 0.06 * S(t * 3.1 + 1), 0.35, 0])), handL: [0, 1.1, 0], handR: [0, -1.1, 0], head: [0.02 * S(t * 2.3), 0, 0] }), // both forearms forward at chest height, palms up ('that was theft')
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
  sitPunch: (t) => { const { hipL, kneeL, ...up } = CLIPS.punch(t); return { ...CLIPS.sit(t), ...up }; }, // seated, hitting the monitor (upper body of punch)
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
  tumble: (t, p = {}) => ({ // tumbling round and round (in a washing-machine drum), limbs out
    root: { rz: -(p.speed ?? 11) * t, pivot: 'hips' }, ...arms(m([0, 0, 2.3 + 0.3 * S(t * 9)], [0, 0, 2.3 + 0.3 * S(t * 9 + 1)]), m([0, 0, 0.3], [0, 0, 0.3])),
    hipL: [-0.3 * S(t * 7), 0, 0.55], hipR: [0.3 * S(t * 7), 0, -0.55], kneeL: [0.4, 0, 0], kneeR: [0.4, 0, 0], head: [-0.2, 0, 0] }),
  cartwheel: (t, p = {}) => { const d = p.dur ?? 0.8, k = Math.min(1, Math.max(0, t / d)); return {
    root: { rz: -2 * PI * k, y: 0.25 * S(k * PI), pivot: 'hips' },
    ...arms(m([0, 0, 2.8], [0, 0, 2.8]), m([0, 0, 0], [0, 0, 0])), hipL: [0, 0, 0.6], hipR: [0, 0, -0.6] }; },
  vault: () => ({ ...arms(m([-1.0, 0, 0.25], [-1.0, 0, 0.25]), m([-0.1, 0, 0], [-0.1, 0, 0])), hipL: [-1.3, 0, 0.4], hipR: [-1.1, 0, 0.3], kneeL: [1.2, 0, 0], kneeR: [1.0, 0, 0], torso: [0.25, 0, 0.15] }),
  pointSelf: (t) => ({ ...arms(m([0, 0, 0.2], [-0.75, 0.6, 0.25]), m([-0.08, 0, -0.3], [-2.0, 0.4, 0])), handR: [0, 0, -0.3], head: [0.12, 0, 0], torso: [0.02 * S(t * 2), 0, 0] }), // index on the chest: 'moi ?'
  pokeUp: (t, p = {}) => { const f = p.freq ?? 2.4, k = Math.max(0, Math.sin(t * f * 2 * PI)); return { // jabbing the ceiling with a broom held overhead
    ...arms(m([-2.75 + 0.08 * k, 0, 0.3], [-2.75 + 0.08 * k, 0, 0.18]), m([-0.75 + 0.6 * k, 0, 0], [-0.75 + 0.6 * k, 0, 0])), head: [-0.4, 0, 0], torso: [-0.06, 0, 0], root: { y: 0.03 * k } }; },
  scarecrowPose: (t) => ({ ...arms(m([0, 0, 1.52], [0, 0, 1.52]), m([0, 0, 0.12 + 0.03 * S(t * 1.3)], [0, 0, 0.1])), head: [0.2, 0, 0.18], torso: [0, 0, 0.03] }), // arms straight out, head on one side
  superman: (t) => ({ // flying horizontally, right fist forward, left arm back along the body (holds the jet can); face the travel direction
    root: { rx: 1.35, y: -0.88 + 0.03 * S(t * 7), rz: 0.04 * S(t * 5), pivot: 'hips' }, ...arms(m([0.35, 0, 0.12], [-2.95, 0, 0.1]), m([0, 0, 0], [-0.05, 0, 0])),
    hipL: [0.12, 0, 0.06], hipR: [0.2, 0, -0.06], kneeL: [0.3, 0, 0], kneeR: [0.15, 0, 0], head: [-0.95, 0, 0], torso: [-0.1, 0, 0] }),
  shakeCan: (t) => ({ // shaking a can hard in the right hand, in front of the chest
    ...arms(m([0, 0, 0.2], [-0.9 + 0.3 * S(t * 30), 0, 0.15]), m([-0.08, 0, -0.3], [-1.1 + 0.45 * S(t * 30), 0, 0])), torso: [0.02 * S(t * 30), 0, 0], head: [0.15, 0, 0], root: { y: 0.01 * Math.abs(S(t * 30)) } }),
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
  diveIn: (t) => { const k = Math.sin(t * 14); return { root: { rx: 1.5, pivot: 'hips' }, ...arms(m([-2.95, 0, 0.12], [-2.95, 0, 0.12]), m([0, 0, 0], [0, 0, 0])), hipL: [0.18 * k, 0, 0], hipR: [-0.18 * k, 0, 0], kneeL: [0.35 + 0.35 * k, 0, 0], kneeR: [0.35 - 0.35 * k, 0, 0], head: [-0.35, 0, 0] }; },   // diving head first, body horizontal at hip height, arms ahead, legs kicking
  peerIn: (t) => ({ ...CLIPS.kneel(t), torso: [0.62, 0, 0], head: [-0.48 + 0.03 * S(t * 2.2), 0.14 * S(t * 1.3), 0], ...arms(m([-1.2, 0, 0.28], [-1.2, 0, 0.28]), m([-0.4, 0, 0], [-0.4, 0, 0])) }),   // kneeling, bent forward, peering into something low (a washing machine), hands on its edge
  fanSide: (t) => ({ shoulderR: [-0.35, 0, 1.75], elbowR: [-1.35 + 0.35 * S(t * 13), 0, 0], handR: [0, 0, 0.5 * S(t * 13)], shoulderL: [-0.45, 0, 0.12], elbowL: [-2.0, 0, 0], torso: [0.08, 0, 0], head: [-0.12 + 0.03 * S(t * 2), 0.12, 0.05], root: { y: -0.01 } }),   // fanning his face from the side (the face stays clear), the other hand pulling his collar
  frozenTopple: (t, p = {}) => { const k = Math.min(1, Math.max(0, t / (p.dur ?? 0.5))), b = k >= 1 ? 0.06 * Math.max(0, 1 - (t - (p.dur ?? 0.5)) / 0.25) * Math.sin((t - (p.dur ?? 0.5)) * 40) : 0;
    return { ...CLIPS.sitFloor(0), head: [0, 0, 0], root: { y: -0.8, rx: 1.45 * k * k - b, pivot: 'hips' } }; },   // frozen solid in the cross-legged pose, he tips forward like a block (p.dur) and bounces once
  fan: (t) => ({ shoulderR: [-1.6 + 0.35 * S(t * 12), 0, 0.3], elbowR: [-0.6, 0, 0], shoulderL: [0, 0, 0.2], elbowL: [-0.2, 0, -0.3], head: [0.05, -0.2, 0] }),
  explainLook: (t, p = {}) => ({ ...CLIPS.explain(t), head: [0.02 * S(t * 2.3), p.yaw ?? 0.7, 0.04], torso: [0, (p.yaw ?? 0.7) * 0.25, 0] }), // explaining toward someone off to the side, face turned to the camera
  gavelStrike: (t, p = {}) => { // judge: right arm raises the gavel over the head and brings it down on the block at p.hit, then holds it there
    const hit = p.hit ?? 0.37, r0 = hit - 0.2, e = x => x * x;
    let sh, el;
    if (t < r0) { const k = Math.max(0, t / r0); sh = -1.7 - 0.9 * k; el = -1.0 - 0.6 * k; }
    else if (t < hit) { const k = e((t - r0) / 0.2); sh = -2.6 + 1.45 * k; el = -1.6 + 1.2 * k; }
    else { const k = Math.min(1, (t - hit) / 0.12); sh = -1.15 + 0.06 * Math.sin(k * PI); el = -0.4; }
    const jolt = t > hit && t < hit + 0.15 ? Math.sin((t - hit) / 0.15 * PI) : 0;
    return { shoulderR: [sh, -0.25, -0.15], elbowR: [el, 0, 0], shoulderL: [-0.85, 0, 0.12], elbowL: [-1.0, 0, 0],
      torso: [0.06 + 0.08 * jolt, 0, 0], head: [0.04 + 0.12 * jolt + 0.02 * S(t * 2), 0.05 * S(t * 0.8), 0] };
  },
  gavelStrikeL: (t, p) => { const q = CLIPS.gavelStrike(t, p), f = v => v && [v[0], -v[1], -v[2]]; return { ...q, shoulderL: f(q.shoulderR), elbowL: f(q.elbowR), shoulderR: f(q.shoulderL), elbowR: f(q.elbowL), head: f(q.head) }; },
  whipWalk: (t, p = {}) => { // officer striding forward cracking a whip: walk legs, the right arm winds up overhead and lashes forward every p.period s
    const w = CLIPS.walk(t, { freq: p.freq ?? 1.5, amp: p.amp ?? 0.48 }), per = p.period ?? 0.6, ph = ((t + (p.phase || 0)) % per) / per;
    const up = ph < 0.55 ? Math.sin(ph / 0.55 * PI / 2) : Math.cos((ph - 0.55) / 0.45 * PI / 2);
    return { ...w, shoulderR: [-0.6 - 2.3 * up, 0, -0.25 - 0.2 * up], elbowR: [-0.3 - 0.9 * up, 0, 0], torso: [0.12 - 0.1 * up, 0.15 * Math.sin(ph * 2 * PI), 0], head: [0.05, 0.25, 0] };
  },
  phoneCallL: (t) => { const q = CLIPS.phoneCall(t), f = v => v && [v[0], -v[1], -v[2]]; return { ...q, shoulderL: f(q.shoulderR), elbowL: f(q.elbowR), shoulderR: f(q.shoulderL), elbowR: f(q.elbowL), head: f(q.head) }; }, // phone in the LEFT hand (mirror of phoneCall)
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
  ride: (t, p = {}) => { const ph = t * 2 * PI * (p.cadence ?? 1.5), a = S(ph); // racing cyclist on a bicycle: leaning forward, hands on the bars, pedalling
    return { hipL: [-1.3 + 0.42 * a, 0, 0.06], hipR: [-1.3 - 0.42 * a, 0, -0.06], kneeL: [1.35 - 0.5 * C(ph), 0, 0], kneeR: [1.35 + 0.5 * C(ph), 0, 0], torso: [p.lean ?? 0.6, 0, 0.025 * a], head: [-(p.lean ?? 0.6) * 0.85, 0, 0],
      ...arms(m([-1.05, 0, 0.16], [-1.05, 0, 0.16]), m([-0.3, 0, 0], [-0.3, 0, 0])), root: { y: -0.4 + 0.012 * Math.abs(a) } }; },
  sitSlump: (t) => ({ ...CLIPS.sit(t), torso: [0.35, 0, 0], head: [0.5 + 0.03 * S(t * 1.1), 0, 0], ...arms(m([-0.35, 0, 0.02], [-0.35, 0, 0.02]), m([-0.5, 0, 0], [-0.5, 0, 0])) }), // sitting, defeated: elbows on the knees, head down
  presentL: (t) => { const q = CLIPS.present(t), f = v => v && [v[0], -v[1], -v[2]]; return { ...q, shoulderL: f(q.shoulderR), elbowL: f(q.elbowR), shoulderR: f(q.shoulderL), elbowR: f(q.elbowL), handL: f(q.handR), handR: f(q.handL), head: f(q.head) }; }, // "after you" with the left arm
  facepalmFlat: (t) => ({ ...CLIPS.stand(), shoulderR: [-1.5, 0.35, 0.28], elbowR: [-2.25, 0, 0], handR: [0.3, 0, 0], head: [0.32, -0.1, 0], torso: [0.12, 0, 0] }), // palm flat on the forehead, head down
  kneelLook: (t) => { const q = CLIPS.lookItem(t); return { ...CLIPS.kneel(t), shoulderR: q.shoulderR, elbowR: q.elbowR, handR: q.handR, shoulderL: [-0.5, 0, 0.25], elbowL: [-1.2, 0, 0], head: [0.12, 0, 0], torso: [0.18, 0, 0] }; }, // kneeling, an item held up to the eye (a magnifier)
  statueRun: () => ({ hipL: [-0.75, 0, 0.05], kneeL: [0.9, 0, 0], hipR: [0.3, 0, -0.03], kneeR: [0.25, 0, 0], ...arms(m([0.6, 0, 0.35], [-0.9, 0, 0.35]), m([-0.4, 0, 0], [-0.6, 0, 0])), torso: [0.12, 0.1, 0], head: [-0.05, 0, 0] }), // frozen mid-stride (« 1, 2, 3, soleil »)
  pointCheek: (t) => ({ ...CLIPS.stand(), shoulderR: [-0.9, 0, 0.5], elbowR: [-2.35, 0.25, 0], handR: [0, 0, 0.3], head: [0.02, -0.12, 0.05] }), // index on his own cheek (« un grain de beauté »)
  phoneEar: (t) => ({ ...CLIPS.stand(), shoulderR: [-0.3, 0, -0.42], elbowR: [-2.55, 0, 0], handR: [0, 0.4, 0], head: [0.03 * Math.sin(t * 4), -0.1, -0.08] }), // a phone held to the right ear
  slump: (t) => ({ ...CLIPS.stand(), torso: [0.2, 0, 0], head: [0.45 + 0.03 * S(t * 1.3), 0, 0], ...arms(m([-0.12, 0, 0.04], [-0.12, 0, 0.04]), m([-0.12, 0, 0], [-0.12, 0, 0])), root: { y: -0.015 } }), // defeated: head down, arms hanging
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
  // --- autumn-2026 news memes ------------------------------------------------------
  sixSeven: (t, p = {}) => { const k = S(t * 2 * PI * (p.freq ?? 2.6)); return { ...CLIPS.stand(), shoulderL: [-0.75 - 0.3 * k, -0.2, 0.25], elbowL: [-1.1, 0, 0], shoulderR: [-0.75 + 0.3 * k, 0.2, -0.25], elbowR: [-1.1, 0, 0], handL: [0, 1.4, 0], handR: [0, -1.4, 0], head: [0.05 * k, 0.12 * k, 0], torso: [0, 0.06 * k, 0] }; }, // "6-7": palms up, alternating like scales
  scuba: (t) => { const k = S(t * 2 * PI * 1.6); return { ...CLIPS.stand(), shoulderR: [-1.2, 0.6, 0], elbowR: [-2.0, 0, 0], shoulderL: [-1.3 + 0.35 * k, 0, 0.1], elbowL: [-0.2, 0, 0], handL: [0.4 * k, 0, 0], hipL: [-0.3, 0, 0], hipR: [-0.3, 0, 0], kneeL: [0.6, 0, 0], kneeR: [0.6, 0, 0], torso: [0.25, 0, 0], head: [0.1, 0, 0], root: { y: -0.08 + 0.03 * k } }; }, // pinches the nose and "swims" down
  auraPose: (t) => ({ ...CLIPS.stand(), ...arms(m([-0.5, -0.65, 0.2], [-0.55, -0.65, 0.2]), m([-1.75, 0, 0], [-1.7, 0, 0])), head: [-0.28, 0.15, 0.05], torso: [-0.12, 0, 0], root: { y: 0.02 } }), // chin up, arms crossed, chest out
  auraPose2: (t) => ({ ...CLIPS.stand(), shoulderL: [0, 0, 0.25], elbowL: [-0.2, 0, 0], shoulderR: [-2.6, 0, -0.3], elbowR: [-0.6, 0, 0], head: [-0.3, -0.2, 0], torso: [-0.15, 0.1, 0], hipL: [-0.1, 0, 0.12], hipR: [0.05, 0, -0.08] }), // one fist to the sky
  leanTable: (t) => ({ ...CLIPS.stand(), ...arms(m([-0.85, 0, 0.18], [-0.85, 0, 0.18]), m([-0.25, 0, 0], [-0.25, 0, 0])), torso: [0.5, 0, 0], head: [-0.25, 0, 0] }), // interrogator leaning on the table
  slamTable: (t) => { const k = t < 0.12 ? t / 0.12 : 1; return { ...CLIPS.stand(), ...arms(m([-1.6 + 0.75 * k, 0, 0.18], [-1.6 + 0.75 * k, 0, 0.18]), m([-0.6 + 0.35 * k, 0, 0], [-0.6 + 0.35 * k, 0, 0])), torso: [0.15 + 0.4 * k, 0, 0], head: [-0.3, 0, 0] }; },
  bowRepeat: (t, p = {}) => { const k = Math.max(0, S(t * 2 * PI * (p.freq ?? 1.4))); return { ...CLIPS.stand(), torso: [0.8 * k, 0, 0], head: [0.15 * k, 0, 0], ...arms(m([0.12 * k, 0, 0.08], [0.12 * k, 0, 0.08]), m([-0.15, 0, 0], [-0.15, 0, 0])) }; }, // apologising again and again
  sitCuffed: (t) => { const c = CLIPS.cuffedFront(t); return { ...CLIPS.sit(t), shoulderL: c.shoulderL, shoulderR: c.shoulderR, elbowL: c.elbowL, elbowR: c.elbowR, head: [0.08, 0.04 * S(t), 0] }; },
  podiumTalk: (t) => ({ ...CLIPS.stand(), ...arms(m([-0.75, 0, 0.15], [-0.75 + 0.1 * S(t * 4), 0, 0.15]), m([-0.55, 0, 0], [-0.55, 0, 0])), head: [0.04 * S(t * 3), 0.05 * S(t * 1.3), 0], torso: [0.08, 0, 0] }),
  patPockets: (t) => { const k = 0.5 + 0.5 * S(t * 8), j = 0.5 + 0.5 * S(t * 8 + 2.4); return { ...CLIPS.stand(), ...arms(m([-0.15 - 0.45 * j, 0, 0.18], [-0.15 - 0.45 * k, 0, 0.18]), m([-0.3 - 1.4 * j, 0, 0], [-0.3 - 1.4 * k, 0, 0])), torso: [0.1, 0.06 * S(t * 4), 0], head: [0.32, 0.2 * S(t * 4), 0] }; }, // pats his trouser and jacket pockets, looking down (lost keys)
  handInPocket: (t) => { const k = Math.min(1, t / 0.4); return { ...CLIPS.stand(), ...arms(m([0, 0, 0.06], [-0.3 * k, 0, -0.2 * k]), m([-0.1, 0, 0], [-1.0 * k, 0, 0])), torso: [0.06 * k, 0, 0], head: [0.32 * k, -0.18 * k, 0] }; }, // slides the right hand into the front pocket (in front of the hip), looking down at it
  holdUp: (t) => ({ ...arms(m([-0.08, 0, 2.92], [-0.08, 0, 2.92]), m([0, 0, 0.12], [0, 0, 0.12])), handL: [0, 0, 1.4], handR: [0, 0, 1.4], head: [-0.22 + 0.02 * S(t * 2), 0, 0], root: { y: 0.01 * S(t * 3) } }), // arms stretched straight up, palms flat under the thing held over the head (a modem, a trophy)
  placeHigh: (t) => ({ ...arms(m([-2.55, 0, 0.32], [-2.55, 0, 0.32]), m([-0.25, 0, 0], [-0.25, 0, 0])), head: [-0.28, 0, 0], torso: [-0.05, 0, 0] }), // both arms up and forward, sliding something onto a high shelf
  floatTilt: (t) => ({ ...CLIPS.float(t), root: { y: 0.1 * S(t * 1.5), rz: 0.2 + 0.05 * S(t * 0.9), rx: -0.12 } }), // weightless, tilted to one side
  floatTiltB: (t) => ({ ...CLIPS.float(t + 1.3), root: { y: 0.1 * S(t * 1.3 + 1), rz: -0.18 + 0.05 * S(t * 0.8), rx: 0.1 } }),
  checkWatch: (t) => ({ ...CLIPS.stand(), shoulderL: [-0.42, 0, 0.12], elbowL: [-1.55, 0.75, 0], handL: [0, 0, 0.45], head: [0.42 + 0.02 * S(t * 2), 0.22, 0], torso: [0.05, 0, 0] }), // left forearm across the chest, wrist up, head down at the watch
  // « Le ver de terre »: pushing a lawnmower, both hands on the handle bar
  pushMower: (t, p = {}) => ({ ...CLIPS.walk(t, { freq: p.freq ?? 1.7, amp: 0.38 }), ...arms(m([-0.78, 0, 0.14], [-0.78, 0, 0.14]), m([-0.32, 0, 0], [-0.32, 0, 0])), torso: [0.12, 0, 0], head: [-0.08 + 0.02 * S(t * 7), 0, 0] }),
  pushMowerStand: (t) => ({ ...arms(m([-0.78, 0, 0.14], [-0.78, 0, 0.14]), m([-0.32, 0, 0], [-0.32, 0, 0])), torso: [0.1, 0, 0], head: [-0.05, 0, 0] }),
  // « La canicule »: life cross-legged in a fridge
  sitFloorSpoon: (t, p = {}) => { const e = CLIPS.eatSpoon(t, p); return { ...CLIPS.sitFloor(t), shoulderL: e.shoulderL, elbowL: e.elbowL, shoulderR: e.shoulderR, elbowR: e.elbowR, head: e.head }; },
  sitFloorWave: (t) => ({ ...CLIPS.sitFloor(t), shoulderR: [0, 0, -2.6], elbowR: [0, 0, -(0.5 + 0.45 * S(t * 9))], head: [0.02 * S(t), -0.15, 0] }),
  sitFloorSip: (t) => { const k = Math.max(0, Math.sin(t * 2.2 - 0.6)) ** 2; return { ...CLIPS.sitFloor(t), shoulderR: [-1.0 - 0.42 * k, 0.45, -0.05], elbowR: [-1.9 - 0.25 * k, 0, 0], head: [-0.18 - 0.16 * k, 0, 0] }; },   // seated, sipping from the mug (a sip every ~2.9 s)
  sitFloorClap: (t) => { const k = Math.abs(S(t * PI * 4)); return { ...CLIPS.sitFloor(t), ...arms(m([-1.25, 0, 0.1 + 0.3 * k], [-1.25, 0, 0.1 + 0.3 * k]), m([-0.95, 0, 0], [-0.95, 0, 0])), head: [-0.12, 0.12 * S(t * 3), 0] }; },
  sitFloorBlow: (t) => ({ ...CLIPS.sitFloor(t), torso: [0.32, 0, 0], head: [0.25, 0, 0], ...arms(m([-0.3, 0, 0.35], [-0.3, 0, 0.35]), m([-0.5, 0, 0], [-0.5, 0, 0])) }),
  stiffStand: (t) => ({ ...arms(m([0, 0, 0.05], [0, 0, 0.05]), m([0, 0, 0], [0, 0, 0])), head: [0.01 * S(t * 40), 0, 0] }),   // frozen stiff, arms glued to the body
  hugCold: (t) => { const r = 0.06 * S(t * 9); return { ...arms(m([-0.62, -0.78 + r, 0.28], [-0.66, -0.78 - r, 0.28]), m([-1.85, 0, 0], [-1.8, 0, 0])), torso: [0.14, 0, 0], head: [0.15 + 0.02 * S(t * 37), 0, 0], root: { y: -0.015 } }; },   // arms wrapped tight round himself, rubbing his arms, hunched and shivering
  sitWave: (t) => ({ ...CLIPS.sit(t), ...arms(m([0, 0, 0.06], [0, 0, 2.6]), m([-0.1, 0, 0], [0, 0, 0.5 + 0.45 * S(t * 9)])), head: [0.02 * S(t), 0.15, 0] }), // seated, waving bye-bye with the right arm (the postman leaving by boat)
  dangleItem: (t) => ({ ...CLIPS.stand(), shoulderR: [-1.55, 0.3, 0.15], elbowR: [-1.2, 0, 0], shoulderL: [0, 0, 0.06], elbowL: [-0.25, 0, 0], head: [0.2 + 0.02 * S(t * 3), 0.3, 0] }), // holds something up beside the face at eye height (keys dangling), head turned to look at it
  holdSign: (t) => ({ ...CLIPS.stand(), ...arms(m([-2.7, -0.2, 0.15], [-2.7, -0.2, 0.15]), m([-0.3, 0, 0], [-0.3, 0, 0])), head: [-0.1, 0, 0], root: { y: 0.02 * Math.abs(S(t * 6)) } }), // protest sign overhead, bouncing
  chant: (t) => { const k = Math.max(0, S(t * 2 * PI * 2)); return { ...CLIPS.stand(), shoulderR: [-2.4 - 0.4 * k, 0, -0.2], elbowR: [-0.4, 0, 0], shoulderL: [0, 0, 0.12], head: [-0.2, 0, 0], root: { y: 0.04 * k } }; }, // fist pumping
  clickCount: (t) => ({ ...CLIPS.stand(), shoulderR: [-0.9, 0.3, 0.05], elbowR: [-0.9, 0, 0], handR: [0.25 * Math.max(0, S(t * 2 * PI * 4)), 0, 0], head: [-0.05, 0.25 * S(t * 1.5), 0] }), // tally counter, scanning the crowd
  readPhone: (t) => ({ ...CLIPS.stand(), shoulderR: [-0.75, 0.35, 0.05], elbowR: [-1.45, 0, 0], handR: [0.3, 0, 0], head: [0.35, 0, 0] }), // phone at chest height, screen toward the face
  showPhone: (t) => ({ ...CLIPS.stand(), shoulderR: [-1.45, 0.15, 0.05], elbowR: [-0.15, 0, 0], handR: [0, 0, 0], head: [0.05, -0.1, 0] }), // arm out, screen toward the others
  showPhoneFaceL: (t) => ({ ...CLIPS.stand(), shoulderL: [-1.15, 0.45, 0.62], elbowL: [-2.45, -0.5, 0], handL: [0, -0.2, 0], head: [0.03 * S(t * 2.2), -0.06, 0.04], torso: [0, -0.06, 0] }), // phone held up beside the face, screen to the camera (selfie)
  reachUpL: (t) => ({ ...CLIPS.stand(), shoulderL: [-2.0 + 0.08 * S(t * 6), 0.3, 0.35], elbowL: [-0.25, 0, 0], head: [-0.12, 0.35, 0], torso: [-0.04, 0.2, 0] }), // left arm flung up toward something flying away behind him
  laugh: (t) => { const k = Math.abs(S(t * 2 * PI * 3)); return { ...CLIPS.stand(), torso: [0.15 + 0.12 * k, 0, 0], head: [-0.25 + 0.2 * k, 0, 0], ...arms(m([-0.45, -0.35, 0.1], [-0.45, -0.35, 0.1]), m([-1.4, 0, 0], [-1.4, 0, 0])), root: { y: 0.02 * k } }; }, // belly laugh, hands on the stomach
  lookItem: (t) => ({ ...CLIPS.stand(), shoulderR: [-0.85, 0.35, 0.05], elbowR: [-1.35, 0, 0], head: [0.45, 0.15, 0] }),

  // --- creature/monster helper (vampire lurk, claw reach) -----------------
  lurk: (t) => ({ torso: [0.2, 0, 0], head: [0.1, 0.05 * S(t), 0], ...arms(m([-0.9, 0, 0.1], [-0.35, 0, 0.1]), m([-0.7, 0, 0], [-0.3, 0, 0])), handL: [0.6, 0, 0], root: { y: -0.02 } }),
  clawReach: (t) => { const k = Math.min(1, t / 0.6); return { ...arms(m([-1.5 * k, 0, 0.1], [0, 0, 0.06]), m([-0.1, 0, 0], [-0.1, 0, 0])), handL: [0.5, 0, 0], torso: [0.1, 0, 0] }; },
  // la balance: standing on tiptoe (heels up, arms out for balance, wobbling), holding the breath (chest out, shoulders up, trembling),
  // kneeling to press a button on the floor, riding a flying board (knees bent, arms out), the same waving / cheering, lying back relaxed
  onTiptoes: (t) => { const k = Math.min(1, t / 0.2); return { root: { y: 0.1 * k + 0.01 * S(t * 9), rz: 0.035 * S(t * 4.5) }, footL: [0.62 * k, 0, 0], footR: [0.62 * k, 0, 0], ...arms(m([-0.15, 0, 0.55 * k + 0.05 * S(t * 7)], [-0.15, 0, 0.55 * k - 0.05 * S(t * 7)]), m([0, 0, -0.2], [0, 0, -0.2])), torso: [-0.04, 0, 0.03 * S(t * 4.5)], head: [-0.08, 0, 0] }; },
  holdBreath: (t) => { const k = Math.min(1, t / 0.25), tr = 0.012 * S(t * 47); return { torso: [-0.12 * k, 0, tr], head: [-0.06 * k, tr, 0], ...arms(m([0.08, 0, 0.28 * k], [0.08, 0, 0.28 * k]), m([0, 0, -0.1], [0, 0, -0.1])), shoulderL: [0.08, 0, 0.28 * k + tr], shoulderR: [0.08, 0, 0.28 * k - tr], headScale: 1 + 0.2 * Math.min(1, t / 1.1) + 0.015 * S(t * 13), flush: Math.min(1, t / 0.9) }; },
  kneelPress: (t) => { const k = Math.min(1, t / 0.3), poke = t > 0.35 ? 0.12 * Math.max(0, S((t - 0.35) * 9)) : 0; return { ...CLIPS.kneel(t), torso: [0.55 * k, 0, 0], head: [0.2 * k, 0, 0], shoulderR: [-0.95 * k - poke, 0.05, 0.12], elbowR: [-0.15, 0, 0], shoulderL: [-0.3, 0, 0.25], elbowL: [-0.9, 0, 0] }; },
  surfRide: (t) => ({ hipL: [-0.75, 0, 0.2], hipR: [-0.75, 0, -0.2], kneeL: [1.3, 0, 0], kneeR: [1.3, 0, 0], footL: [-0.55, 0, 0], footR: [-0.55, 0, 0], torso: [0.3, 0.06 * S(t * 1.7), 0.06 * S(t * 1.3)], head: [-0.3, 0, 0],
    ...arms(m([-0.35, 0, 0.85 + 0.1 * S(t * 2.1)], [-0.35, 0, 0.85 - 0.1 * S(t * 2.1)]), m([-0.5, 0, 0.35], [-0.5, 0, 0.35])), root: { y: -0.24 + 0.02 * S(t * 3) } }),
  rideWave: (t) => ({ ...CLIPS.surfRide(t), ...arms(m([-0.1, 0, 1.15], [0, 0, 2.6]), m([0, 0, 0.25], [0, 0, 0.5 + 0.45 * S(t * 9)])), head: [-0.05, 0, 0] }),
  rideCheer: (t) => ({ ...CLIPS.surfRide(t), ...arms(m([0, 0, 2.7 + 0.15 * S(t * 10)], [0, 0, 2.7 + 0.15 * S(t * 10 + 1)]), m([0, 0, 0.3], [0, 0, 0.3])), head: [-0.2, 0, 0], root: { y: -0.1 + 0.05 * Math.abs(S(t * 5)) } }),
  commandSit: (t) => ({ ...CLIPS.stand(), shoulderR: [-0.55, 0.05, 0.12], elbowR: [-0.05, 0, 0], handR: [0.25, 0, 0], shoulderL: [0.1, 0, 0.18], torso: [0.18, 0, 0], head: [0.32 + 0.02 * S(t * 3), 0, 0] }),   // standing over someone, arm straight down-forward: « assis ! »
  feedTreat: (t) => { const k = Math.min(1, t / 0.35); return { ...CLIPS.stand(), shoulderR: [-0.85 * k, 0.05, 0.1], elbowR: [-0.25, 0, 0], torso: [0.32 * k, 0, 0], head: [0.3 * k, 0, 0] }; },   // leaning down to hand a treat
  sitEdge: (t) => ({ hipL: [-1.5, 0, 0.1], hipR: [-1.5, 0, -0.1], kneeL: [1.25 + 0.12 * S(t * 2.2), 0, 0], kneeR: [1.5 - 0.12 * S(t * 2.2), 0, 0], torso: [-0.42, 0, 0.03 * S(t * 1.1)], head: [0.32 + 0.03 * S(t * 1.4), 0.05 * S(t * 0.8), 0], ...arms(m([0.85, 0, 0.35], [0.85, 0, 0.35]), m([0, 0, 0], [0, 0, 0])), root: { y: -0.45 } }),   // sitting on an edge, legs dangling and swinging, leaning back on the hands
  reclineBack: (t) => ({ hipL: [-1.3, 0, 0.14], hipR: [-1.3, 0, -0.14], kneeL: [0.3, 0, 0], kneeR: [0.75, 0, 0], torso: [-0.62, 0, 0], head: [0.42 + 0.03 * S(t * 1.4), 0.06 * S(t * 0.9), 0], ...arms(m([0.95, 0, 0.32], [0.95, 0, 0.32]), m([0, 0, 0], [0, 0, 0])), root: { y: -0.8 } }),
  lieRelax: (t) => ({ root: { rx: -PI / 2, y: -0.88, pivot: 'hips' }, ...arms(m([0, 0, 2.75], [0, 0, 2.75]), m([0, 0, 2.0], [0, 0, 2.0])), hipL: [-0.75, 0, 0.05], kneeL: [1.4, 0, 0], hipR: [0, 0, -0.05], head: [0.35 + 0.03 * S(t * 1.5), 0, 0] }),
};

// ---- cartoon clips (toon rig: engine/toon.js). They return extra channels under `toon` (sq, scl, bend, face); on an actor without the
// cartoon rig those channels are ignored and the joints still play. Times are seconds from the key.
const sqv = s => { const k = 1 / Math.sqrt(Math.max(0.05, s)); return [k, s, k]; };   // volume-preserving squash (< 1) / stretch (> 1) along Y
const c01 = x => Math.max(0, Math.min(1, x));
const eo = x => 1 - Math.pow(1 - c01(x), 3), ei = x => c01(x) ** 3, eio = x => { x = c01(x); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const back = (x, c1 = 2.4) => { x = c01(x); const c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };   // overshoot, then settle
const wob = (t, f = 30, decay = 6) => (t <= 0 ? 0 : Math.sin(t * f) * Math.exp(-t * decay));   // decaying wobble (a jelly settling)
const mix = (a, b, k) => a + (b - a) * k;
Object.assign(CLIPS, {
  // the Tex Avery take: sink (anticipation), shoot up with the eyes out and the jaw down, vibrate, settle. p.hold (0.7 s), p.pop / p.jaw (0..1)
  take: (t, p = {}) => {
    const hold = p.hold ?? 0.7, a = c01(t / 0.14), b = t < 0.14 ? 0 : back((t - 0.14) / 0.13), end = 0.27 + hold, out = t < end ? 0 : eio((t - end) / 0.25), live = b * (1 - out);
    const sy = mix(mix(1, 0.7, eo(a)), 1.16, b) * (1 - out) + out + 0.05 * wob(t - end, 34, 7), sh = t > 0.27 && t < end ? 1 : 0, arm = mix(0.15, 2.05, b) * (1 - out) + 0.2 * out;
    return { ...arms(m([mix(-0.5 * a, -0.3, b), 0, arm], [mix(-0.5 * a, -0.3, b), 0, arm]), m([mix(-1.3 * a, -0.25, b) * (1 - out), 0, 0], [mix(-1.3 * a, -0.25, b) * (1 - out), 0, 0])),
      hipL: [-0.25 * a * (1 - b), 0, 0.08 * live], hipR: [-0.25 * a * (1 - b), 0, -0.08 * live], kneeL: [0.5 * a * (1 - b), 0, 0], kneeR: [0.5 * a * (1 - b), 0, 0],
      head: [mix(0.3 * a, -0.05, b) * (1 - out), 0.012 * sh * S(t * 53), 0], root: { x: 0.004 * sh * S(t * 61), y: mix(-0.1 * a, 0.03, b) * (1 - out) },
      toon: { sq: sqv(sy), bend: { spine: [mix(0.35 * a, -0.14, b) * (1 - out), 0, 0, 1, null], neck: [0, 0, 0, 1 + 1.1 * live, null] }, scl: { head: [1 + 0.14 * live, 1 + 0.26 * live, 1 + 0.14 * live] },
        ears: 0.7 * live + 0.15 * sh * S(t * 47), hat: [0.32 * live + 0.02 * sh * S(t * 31), 0.25 * live, 6.3 * eo((t - 0.14) / 0.5)],
        face: { pop: (p.pop ?? 1) * live, popLen: 0.13, jaw: (p.jaw ?? 1) * live, tongue: (p.tongue ?? 0) * live, expr: p.expr ?? 'take', exprW: Math.max(live, 0.6 * eo(a) * (1 - out)) } } };
  },
  // double take: a casual look away (p.side ±1), a beat, a dip, then the head whips back smeared wide, eyes out. p.beat (0.3 s)
  doubleTakeToon: (t, p = {}) => {
    const sd = p.side ?? 1, beat = p.beat ?? 0.3, t1 = 0.22, t2 = t1 + beat, t3 = t2 + 0.08, t4 = t3 + 0.1;
    const away = t < t2 ? eo(t / t1) : 1 - back((t - t3) / (t4 - t3), 3.2), dip = t < t2 ? 0 : t < t3 ? eo((t - t2) / 0.08) : 1 - eo((t - t3) / 0.1), whip = t > t3 && t < t4 ? S((t - t3) / (t4 - t3) * PI) : 0, pop = t > t3 ? eo((t - t3) / 0.1) : 0;
    return { ...CLIPS.stand(), head: [0.1 * away + 0.3 * dip - 0.12 * pop, 0.95 * sd * Math.max(-0.2, away), 0], neck: [0, 0.25 * sd * Math.max(0, away), 0], torso: [0.1 * dip, 0.18 * sd * Math.max(0, away), 0], root: { y: -0.05 * dip + 0.05 * pop * Math.max(0, 1 - (t - t4) * 3) },
      toon: { sq: sqv(1 - 0.12 * dip + 0.1 * pop * Math.max(0, 1 - (t - t4) * 4)), scl: { head: [1 + 0.55 * whip, 1 - 0.18 * whip, 1] }, bend: { spine: [0.2 * dip - 0.15 * pop, 0, 0, 1, null], neck: [0, 0, 0, 1 + 0.5 * pop * Math.max(0, 1 - (t - t4) * 2.5), null] },
        face: { pop: (p.pop ?? 0.75) * pop, jaw: (p.jaw ?? 0.3) * pop, expr: t < t2 ? (p.calm ?? 'unimpressed') : (p.expr ?? 'takeSmall'), exprW: t < t2 ? 0.8 * eo(t / t1) : Math.max(dip, pop) } } };
  },
  // running on the spot before a dash: legs a blur (stretched, 9 cycles/s), the body leans back then tips forward. p.dur (0.6 s)
  scramble: (t, p = {}) => {
    const d = p.dur ?? 0.6, k = c01(t / d), ph = t * 2 * PI * (p.freq ?? 9), lean = mix(-0.45, 0.5, eio(k));
    return { hipL: [-0.4 + 1.3 * S(ph), 0, 0.05], hipR: [-0.4 + 1.3 * S(ph + PI), 0, -0.05], kneeL: [1.2 + 0.9 * S(ph + 1.2), 0, 0], kneeR: [1.2 + 0.9 * S(ph + PI + 1.2), 0, 0],
      ...arms(m([-0.6 + 1.1 * S(ph + PI), 0, 0.25], [-0.6 + 1.1 * S(ph), 0, 0.25]), m([-1.5, 0, 0], [-1.5, 0, 0])), torso: [0, 0.1 * S(ph), 0], head: [-lean * 0.5, 0, 0], root: { y: 0.03 + 0.02 * Math.abs(S(ph)), z: -0.12 * (1 - k) },
      toon: { bend: { spine: [lean, 0, 0, 1, null], legL: [0, 0, 0, 1.18, null], legR: [0, 0, 0, 1.18, null] }, face: { steam: p.steam ?? 0, expr: p.expr ?? 'determined', exprW: 1 } } };
  },
  // the dash itself (use it on a fast move): the body a long horizontal smear, arms and one leg trailing
  dashOff: (t, p = {}) => { const k = p.k ?? 1, ph = t * 2 * PI * 7; return { ...arms(m([0.9, 0, 0.5], [0.9, 0, 0.5]), m([0, 0, 0], [0, 0, 0])), hipL: [-1.3 + 0.3 * S(ph), 0, 0], hipR: [1.0 + 0.3 * S(ph + PI), 0, 0], kneeL: [0.3, 0, 0], kneeR: [0.9, 0, 0], head: [-0.75, 0, 0],
      toon: { sq: [1 - 0.22 * k, 1 - 0.18 * k, 1 + 0.75 * k], bend: { spine: [0.85, 0, 0, 1.15, null], armL: [0, 0, 0, 1.3, null], armR: [0, 0, 0, 1.3, null], legR: [0, 0, 0, 1.35, null] } } }; },
  // hanging in mid-air past the edge: legs still walking, he stops, looks down (p.downAt), looks at us (p.usAt), gulps. Then let him fall with a move
  hangAir: (t, p = {}) => {
    const dn = eo((t - (p.downAt ?? 0.25)) / 0.12), us = eo((t - (p.usAt ?? 0.75)) / 0.1), walk = Math.max(0, 1 - t / 0.2), ph = t * 2 * PI * 2.2;
    return { ...arms(m([0, 0, 0.35 + 0.5 * dn], [0, 0, 0.35 + 0.5 * dn]), m([-0.2, 0, -0.2], [-0.2, 0, -0.2])), hipL: [-0.5 * walk * S(ph), 0, 0.06], hipR: [0.5 * walk * S(ph), 0, -0.06], kneeL: [0.3 * walk, 0, 0], kneeR: [0.3 * walk, 0, 0], footL: [0.5 * dn, 0, 0], footR: [0.5 * dn, 0, 0],
      head: [0.75 * dn * (1 - us), 0, 0], root: { y: 0.012 * S(t * 3) },
      toon: { bend: { spine: [0.3 * dn * (1 - us), 0, 0, 1, null], neck: [0, 0, 0, 1 + 0.35 * dn * (1 - us), null], legL: [0, 0, 0, 1 + 0.12 * us, null], legR: [0, 0, 0, 1 + 0.12 * us, null] }, face: { expr: us > 0.5 ? (p.expr ?? 'gulp') : 'lookDown', exprW: Math.max(dn * (1 - us), us) } } };
  },
  // flattened like a pancake (a disc at ankle height), then at p.popAt he springs back, overshoots tall and jiggles. p.flat (0.08)
  pancake: (t, p = {}) => {
    const flat = p.flat ?? 0.08, at = p.popAt ?? 1e9, u = t - at, sy = u < 0 ? flat * (1 + 0.08 * S(t * 3)) : mix(flat, 1, back(u / 0.3, 3.4)) + 0.07 * wob(u - 0.3, 30, 6), sx = u < 0 ? 1.7 : mix(1.7, 1, eo(u / 0.25)) / Math.sqrt(Math.max(0.3, Math.min(1.4, sy)));
    const k = u < 0 ? 1 : 1 - eo(u / 0.3);
    return { ...arms(m([0, 0, 1.45 * k + 0.2 * (1 - k)], [0, 0, 1.45 * k + 0.2 * (1 - k)]), m([0, 0, 0.1 * k - 0.3 * (1 - k)], [0, 0, 0.1 * k - 0.3 * (1 - k)])), hipL: [0, 0, 0.5 * k], hipR: [0, 0, -0.5 * k], head: [0, 0, 0],
      toon: { sq: [sx, sy, sx], face: { expr: p.expr ?? 'dizzy', exprW: u < 0 ? 1 : 1 - eo(u / 0.5), stars: (p.stars ?? 0) * (u < 0 ? 1 : 1 - eo(u / 0.8)) } } };
  },
  // rolled thin as a sheet of paper (front to back), swaying like a falling leaf; p.popAt puffs him back
  paperThin: (t, p = {}) => { const at = p.popAt ?? 1e9, u = t - at, k = u < 0 ? 1 : 1 - eo(u / 0.25), sz = mix(1, p.thin ?? 0.05, k) + (u > 0 ? 0.12 * wob(u - 0.2, 26, 6) : 0);
    return { ...CLIPS.stand(), head: [0, 0, 0.05 * k * S(t * 2.2)], root: { rz: 0.12 * k * S(t * 2.2), x: 0.05 * k * S(t * 2.2 + 1) }, toon: { sq: [1 + 0.25 * k, 1 + 0.2 * k, sz], bend: { spine: [0, 0.22 * k * S(t * 2.2 + 0.6), 0, 1, null] } } }; },
  // blown up like a balloon (p.k 0..1 or grows over p.dur), limbs pushed out, then p.popAt lets the air out
  inflate: (t, p = {}) => { const at = p.popAt ?? 1e9, u = t - at, k = (p.k ?? eo(t / (p.dur ?? 0.8))) * (u < 0 ? 1 : 1 - eo(u / 0.18)), w = 1 + 0.95 * k + 0.03 * k * S(t * 9);
    return { ...arms(m([0, 0, 0.2 + 1.2 * k], [0, 0, 0.2 + 1.2 * k]), m([0, 0, -0.3 * (1 - k)], [0, 0, -0.3 * (1 - k)])), hipL: [0, 0, 0.35 * k], hipR: [0, 0, -0.35 * k], head: [-0.2 * k, 0, 0], root: { y: 0.25 * k * (p.float ?? 0) + (u > 0 ? 0 : 0.01 * k * S(t * 5)) },
      toon: { bend: { spine: [0, 0, 0, 1 + 0.12 * k, w] }, scl: { head: [1 + 0.25 * k, 1 + 0.12 * k, 1 + 0.25 * k] }, face: { expr: p.expr ?? 'puffed', exprW: Math.min(1, k * 1.6) } } }; },
  // an arm that stretches out to grab something far away (p.reach x length, p.side 'R'/'L'), the body leaning back; p.backAt snaps it home with a recoil
  stretchGrab: (t, p = {}) => {
    const R = (p.side ?? 'R') === 'R', reach = p.reach ?? 3, go = eo(t / (p.dur ?? 0.35)), at = p.backAt ?? 1e9, u = t - at, st = u < 0 ? mix(1, reach, go) : mix(reach, 1, back(u / 0.16, 2.2)), rec = u > 0 ? wob(u - 0.1, 30, 7) : 0;
    const arm = [-1.5 + 0.05 * S(t * 12) * (u < 0 ? 1 : 0), 0, 0.08], other = [0.25 * go, 0, 0.3];
    return { ...CLIPS.stand(), shoulderR: R ? [arm[0], 0, -arm[2]] : [other[0], 0, -other[2]], shoulderL: R ? other : arm, elbowR: [0, 0, 0], elbowL: [0, 0, 0], head: [0, 0, 0], torso: [0, (R ? 0.25 : -0.25) * go * (u < 0 ? 1 : 0), 0],
      toon: { sq: sqv(1 - 0.12 * rec), bend: { spine: [-0.3 * go * (u < 0 ? 1 : 0) + 0.25 * rec, 0, 0, 1, null], [R ? 'armR' : 'armL']: [0, 0, 0, st, null], [R ? 'foreR' : 'foreL']: [0, 0, 0, st, null] } } };
  },
  // the neck goes up like a periscope (p.len x), the head looks round; p.backAt drops it with a boing
  periscope: (t, p = {}) => { const at = p.backAt ?? 1e9, u = t - at, k = u < 0 ? back(t / 0.3, 2) : 1 - back(u / 0.18, 2.5), len = 1 + ((p.len ?? 4) - 1) * k;
    return { ...CLIPS.stand(), head: [0, 0.7 * S(t * 2.6) * Math.max(0, k), 0], toon: { bend: { neck: [0.05 * S(t * 2.6), 0.1 * S(t * 3.1) * k, 0, len, 0.75 + 0.25 / Math.sqrt(Math.max(1, len))] }, sq: sqv(1 + (u > 0 ? 0.08 * wob(u - 0.12, 30, 7) : 0)) } }; },
  // squeezed like an accordion after a crash: the torso pumps short and tall, short legs. p.amp (0.45)
  accordion: (t, p = {}) => { const a = p.amp ?? 0.45, s = p.hit ? (p.rest ?? 0.78) - (p.amp ?? 0.55) * Math.exp(-t * (p.decay ?? 7)) * Math.cos(t * (p.freq ?? 55)) : 1 - a * (0.55 + 0.45 * S(t * (p.freq ?? 7))) * Math.exp(-t * (p.decay ?? 0)), w = 1 / Math.sqrt(s) * 1.1;   // p.hit: a hard landing (flat on the first frame, then bellows bounces that die out; key it with blend=0.02)
    return { ...arms(m([0, 0, 0.5], [0, 0, 0.5]), m([0, 0, -0.5], [0, 0, -0.5])), head: [0.12 * S(t * 7 + 1), 0, 0.08 * S(t * 3.5)], toon: { bend: { spine: [0, 0, 0, s, w], legL: [0, 0, 0, 0.6, 1.25], legR: [0, 0, 0, 0.6, 1.25], shinL: [0, 0, 0, 0.6, 1.25], shinR: [0, 0, 0, 0.6, 1.25] }, face: { expr: p.expr ?? 'dizzy', exprW: 1, stars: p.stars ?? 0 } }, root: { y: -0.39 } }; },
  // jelly settle after any impact: the whole body wobbles tall/short and sways, dying out. p.amp (0.3)
  jelly: (t, p = {}) => { const a = p.amp ?? 0.3, w = wob(t + 0.05, p.freq ?? 26, p.decay ?? 5); return { ...CLIPS.stand(), head: [0.1 * a * w, 0, 0.1 * a * wob(t, 19, 5)], toon: { sq: sqv(1 + a * w), bend: { spine: [0, 0.5 * a * wob(t, 19, 5), 0, 1, null] } } }; },
  // rubber-hose arms: both arms ripple like noodles (terror, or showing off). p.amp (1)
  noodle: (t, p = {}) => { const a = p.amp ?? 1, w = (ph) => 0.9 * a * S(t * 9 + ph);
    return { ...arms(m([0, 0, 1.6], [0, 0, 1.6]), m([0, 0, 0], [0, 0, 0])), head: [-0.1, 0.15 * S(t * 4.5), 0], hipL: [0, 0, 0.05], hipR: [0, 0, -0.05], root: { y: 0.02 * Math.abs(S(t * 9)) },
      toon: { bend: { armL: [0, w(0), 0, 1.25, null], foreL: [0, w(1.6), 0, 1.25, null], armR: [0, -w(0.8), 0, 1.25, null], foreR: [0, -w(2.4), 0, 1.25, null], spine: [0, 0.12 * S(t * 4.5), 0, 1, null] } } }; },
  // melting with despair: he sinks into a puddle, shoulders and arms drooping. p.dur (0.9 s), p.k
  melt: (t, p = {}) => { const k = p.k ?? eio(t / (p.dur ?? 0.9)); return { ...arms(m([0, 0, 0.1], [0, 0, 0.1]), m([0, 0, 0], [0, 0, 0])), head: [0.5 * k, 0, 0.1 * k], hipL: [0, 0, 0.3 * k], hipR: [0, 0, -0.3 * k],
      toon: { sq: [1 + 0.9 * k, 1 - 0.78 * k, 1 + 0.9 * k], bend: { spine: [0.5 * k, 0, 0, 1, null], armL: [0, 0, 0, 1 + 0.5 * k, null], armR: [0, 0, 0, 1 + 0.5 * k, null] }, scl: { head: [1 + 0.2 * k, 1 - 0.3 * k, 1] }, face: { expr: p.expr ?? 'cry', exprW: Math.min(1, k * 1.5) } } }; },
  // wind-up before a dash or a punch: coil back on one leg, the spine a C, arms cocked; p.dur (0.3 s)
  windUp: (t, p = {}) => { const k = back(t / (p.dur ?? 0.3), 1.6); return { ...arms(m([0.9 * k, 0, 0.4], [-1.4 * k, 0, 0.3]), m([-1.2 * k, 0, 0], [-1.6 * k, 0, 0])), hipL: [-1.1 * k, 0, 0], kneeL: [1.5 * k, 0, 0], hipR: [0.25 * k, 0, 0], kneeR: [0.2 * k, 0, 0], head: [0.2 * k, 0, 0], root: { y: -0.03 * k, z: -0.15 * k },
      toon: { sq: sqv(1 - 0.1 * k), bend: { spine: [-0.55 * k, 0, 0.3 * k, 1, null] }, face: { expr: p.expr ?? 'determined', exprW: Math.min(1, k) } } }; },
  // ---- cycle 1 additions (story 37): gaits with busy hands, a braking skid, the edge of the void, dives
  // walking with the eyes on a phone held at chest height (right hand): the free arm swings, the head stays down
  walkRead: (t, p = {}) => { const w = CLIPS.walk(t, p); return { ...w, shoulderR: [-1.0, 0.3, 0.05], elbowR: [-1.8 + 0.04 * S(t * (p.freq ?? 1.9) * 4 * PI), 0, 0], handR: [0.3, 0, 0], head: [0.36, 0, 0], torso: [0.06, w.torso[1], 0] }; },   // the phone at chin height, clear of the chest
  // walking while ticking boxes on a clipboard (left hand holds it, the right hand writes)
  walkWrite: (t, p = {}) => { const w = CLIPS.walk(t, p); return { ...w, shoulderL: [-0.75, -0.45, 0.1], elbowL: [-1.6, 0, 0], shoulderR: [-0.85, 0.4, -0.05], elbowR: [-1.5 - 0.07 * S(t * 18), 0, 0], head: [0.38, 0, 0], torso: [0.05, w.torso[1], 0] }; },
  // a pompous march: chest out, chin up, arms swinging wide and stiff (an official arriving)
  marchPomp: (t, p = {}) => { const f = p.freq ?? 1.7, ph = t * f * 2 * PI; return { hipL: [-0.6 * S(ph), 0, 0], hipR: [0.6 * S(ph), 0, 0], kneeL: [Math.max(0, 0.35 * S(ph + 1.4)), 0, 0], kneeR: [Math.max(0, 0.35 * S(ph + 1.4 + PI)), 0, 0], footL: [-0.35 * Math.max(0, S(ph)), 0, 0], footR: [-0.35 * Math.max(0, -S(ph)), 0, 0],
      ...arms(m([0.7 * S(ph), 0, 0.12], [-0.7 * S(ph), 0, 0.12]), m([-0.1, 0, 0], [-0.1, 0, 0])), torso: [-0.14, 0.06 * S(ph), 0], head: [-0.16, 0, 0], root: { y: 0.03 * Math.abs(S(ph)) }, toon: { bend: { spine: [-0.22, 0, 0, 1.04, null] }, face: { expr: p.expr ?? 'proud', exprW: 1 } } }; },
  // braking from a sprint: heels dug in, the body thrown back then whipped forward as it stops (p.dur 0.4 s), then standing on the edge
  skidStop: (t, p = {}) => { const d = p.dur ?? 0.4, k = c01(t / d), lean = mix(-0.75, 0, eo(k)) + 0.5 * wob(t - d, 22, 6), sq = 1 - 0.2 * S(c01(t / (d * 0.6)) * PI) + 0.1 * wob(t - d, 22, 6);
    return { hipL: [-0.9 * (1 - eo(k)), 0, 0.05], hipR: [-0.7 * (1 - eo(k)), 0, -0.05], kneeL: [0.25 * (1 - k), 0, 0], kneeR: [0.2 * (1 - k), 0, 0], footL: [-0.7 * (1 - k), 0, 0], footR: [-0.7 * (1 - k), 0, 0],
      ...arms(m([-0.9 * (1 - k) - 0.2, 0, 0.9 * (1 - k) + 0.2], [-0.9 * (1 - k) - 0.2, 0, 0.9 * (1 - k) + 0.2]), m([-0.5, 0, 0], [-0.5, 0, 0])), head: [0.35 * (1 - k) + 0.3 * wob(t - d, 22, 6), 0, 0], root: { rx: lean * 0.45 },
      toon: { sq: sqv(sq), bend: { spine: [lean * 0.7, 0, 0, 1, null] }, face: { expr: p.expr ?? 'scared', exprW: 1 } } }; },
  // teetering on the edge of the void: the body rocks forward and back, more each time, the arms windmill like rubber hoses (p.grow)
  teeter: (t, p = {}) => { const g = 1 + (p.grow ?? 1.2) * t, fa = p.fallAt ?? 1e9, f = ei((t - fa) / 0.2), a = (0.26 * g * S(t * (p.freq ?? 7))) * (1 - f) + 1.25 * f, wm = t * (p.spin ?? 13);   // p.fallAt: he finally tips over, forward and down
    return { ...arms(m([-PI * 2 * ((wm / (2 * PI)) % 1), 0, 0.5], [-PI * 2 * (((wm + PI) / (2 * PI)) % 1), 0, 0.5]), m([-0.2, 0, 0], [-0.2, 0, 0])), hipL: [-0.5 * a * (1 - f), 0, 0.06], hipR: [-0.5 * a * (1 - f), 0, -0.06], footL: [-0.4 * a * (1 - f), 0, 0], footR: [-0.4 * a * (1 - f), 0, 0], head: [-0.5 * a * (1 - f), 0, 0],
      root: { rx: a * 0.9, y: 0.03 * Math.max(0, S(t * 14)) * (1 - f) - 2.2 * f * f, z: 0.75 * f }, toon: { bend: { spine: [a * 1.2 * (1 - f), 0, 0, 1, null], armL: [0, 0, 0, 1.25, null], foreL: [0.4 * S(wm), 0, 0, 1.25, null], armR: [0, 0, 0, 1.25, null], foreR: [0.4 * S(wm + PI), 0, 0, 1.25, null] }, face: { expr: p.expr ?? 'scared', exprW: 1, jaw: (p.jaw ?? 0.25) + 0.6 * f, pop: p.pop ?? 0, popLen: 0.1 } } }; },
  // a swan dive: arms spread, the back arched, legs together and stretched (use it on a move with an arc; the body pitches with p.k 0..1)
  swanDive: (t, p = {}) => { const k = p.k ?? c01(t / (p.dur ?? 0.6)); return { root: { rx: mix(0.2, 2.9, eio(k)), pivot: 'hips' }, ...arms(m([-0.3, 0, 1.75 - 1.6 * ei(k)], [-0.3, 0, 1.75 - 1.6 * ei(k)]), m([0, 0, 0], [0, 0, 0])), hipL: [0.25, 0, 0.02], hipR: [0.25, 0, -0.02], head: [-0.5 + 0.4 * k, 0, 0],
      toon: { bend: { spine: [-0.45 * (1 - k), 0, 0, 1.08, null], legL: [0, 0, 0, 1.2, null], legR: [0, 0, 0, 1.2, null], shinL: [0, 0, 0, 1.15, null], shinR: [0, 0, 0, 1.15, null] }, face: { expr: p.expr ?? 'bigGrin', exprW: 1 } } }; },
  // a cannonball: knees to the chest, arms round them, the body a tight ball that spins forward (p.spin turns/s)
  cannonball: (t, p = {}) => { const k = eo(t / 0.15); return { root: { rx: (p.spin ?? 1.5) * 2 * PI * t, pivot: 'hips' }, hipL: [-2.1 * k, 0, 0.1], hipR: [-2.1 * k, 0, -0.1], kneeL: [2.3 * k, 0, 0], kneeR: [2.3 * k, 0, 0], ...arms(m([-1.3 * k, 0, 0.1], [-1.3 * k, 0, 0.1]), m([-1.4 * k, 0, 0], [-1.4 * k, 0, 0])), head: [0.5 * k, 0, 0], torso: [0.5 * k, 0, 0],
      toon: { sq: sqv(1 - 0.12 * k), bend: { spine: [0.6 * k, 0, 0, 0.9, null] }, face: { expr: p.expr ?? 'laugh', exprW: 1 } } }; },
  // holding the nose and jumping feet first (a child's jump into the water), the other arm straight up
  noseJump: (t, p = {}) => ({ ...arms(m([0, 0, 2.9], [-0.9, 0.5, 0.2]), m([0, 0, 0.1], [-2.35, 0, 0])), hipL: [-0.5, 0, 0.1], hipR: [-0.2, 0, -0.05], kneeL: [0.9, 0, 0], kneeR: [0.4, 0, 0], head: [-0.1, 0, 0], toon: { face: { expr: p.expr ?? 'puffed', exprW: 1 } } }),
  // seated, a phone at the right ear, the left hand brings a rubber stamp down on the desk at p.hit (wind-up, slam, rebound)
  stampPhone: (t, p = {}) => { const hit = p.hit ?? 0.8, up = eo((t - (hit - 0.32)) / 0.2), dn = ei((t - (hit - 0.09)) / 0.09), a = up * (1 - dn), reb = wob(t - hit, 30, 9), after = t > hit ? 1 : 0;
    return { ...CLIPS.sit(t), shoulderR: [-0.3, 0, -0.42], elbowR: [-2.55, 0, 0], handR: [0, 0.4, 0], shoulderL: [-0.85 - 1.25 * a + 0.12 * reb, 0, 0.12], elbowL: [-0.95 - 0.6 * a, 0, 0],
      head: [0.08 + 0.3 * after * Math.max(0, 1 - (t - hit) * 2.5) - 0.22 * a, -0.1, -0.08], torso: [0.04 + 0.22 * after * Math.max(0, 1 - (t - hit) * 2.5) - 0.12 * a, 0, 0],
      toon: { sq: sqv(1 - 0.07 * reb + 0.05 * a), bend: { spine: [0.2 * after * Math.max(0, 1 - (t - hit) * 2.5) - 0.15 * a, 0, 0, 1, null] } } }; },
  // squeezed in a crowd: shoulders in, arms pinned to the body, the head free to look round (p.look yaw). Scale the actor's toon.sq for the squeeze
  squeezed: (t, p = {}) => ({ ...arms(m([0.1, 0, -0.05], [0.1, 0, -0.05]), m([-0.5, 0.6, 0], [-0.5, 0.6, 0])), head: [-0.25 + 0.03 * S(t * 2 + (p.ph ?? 0)), (p.look ?? 0) + 0.12 * S(t * 1.3 + (p.ph ?? 0)), 0], hipL: [0, 0, -0.03], hipR: [0, 0, 0.03], root: { y: 0.008 * S(t * 2.2 + (p.ph ?? 0)) } }),
  // ---- cycle 1, second pass (after the animation review): falls that trail, a real rug, a wave from the wrist, a stamp with a wind-up
  // falling feet first: everything that can trail does (arms up and rippling like ribbons, legs dangling, the body long, hat and ears lifted). Use it on a fast drop
  fallDrag: (t, p = {}) => { const f = t * 33; return { ...arms(m([0.12 * S(f), 0, 2.9 + 0.1 * S(f * 0.7)], [0.12 * S(f + 2), 0, 2.9 + 0.1 * S(f * 0.7 + 1.3)]), m([0, 0, 0.2 * S(f + 1)], [0, 0, 0.2 * S(f + 2.5)])),
      hipL: [-0.35 + 0.15 * S(f * 0.8), 0, 0.14], hipR: [-0.12 + 0.15 * S(f * 0.8 + 2), 0, -0.14], kneeL: [0.75, 0, 0], kneeR: [0.45, 0, 0], footL: [0.5, 0, 0], footR: [0.5, 0, 0], head: [0.12, 0, 0],
      toon: { sq: sqv(p.stretch ?? 1.14), bend: { armL: [0, 0.3 * S(f), 0, 1.35, null], foreL: [0, -0.45 * S(f + 1), 0, 1.35, null], armR: [0, -0.3 * S(f + 2), 0, 1.35, null], foreR: [0, 0.45 * S(f + 3), 0, 1.35, null], spine: [-0.1, 0, 0, 1.06, null] },
        hat: [0.3, 0.2 * S(f), 0], ears: 0.6, face: { expr: p.expr ?? 'scared', exprW: 1, jaw: p.jaw ?? 0.7 } } }; },
  // flat on the ground like a rug (for a camera that looks down on the floor at 25-35 deg): lying on his back, as thin as paper, the suit and the face turned to the sky,
  // hands up and legs apart, wall to wall; spiral eyes, then a blink or two; at p.popAt he springs back upright (overshoot, jiggle). Key it with blend=0.02:
  // a hard hit has no ease in. The head points away from the camera (−Z for an actor facing +Z)
  splat: (t, p = {}) => {
    const flat = p.flat ?? 0.09, W = p.wide ?? 1.1, at = p.popAt ?? 1e9, u = t - at, bA = p.blinkAt ?? 0.14;
    if (u < 0) { const hit = Math.exp(-t * 24) * Math.cos(t * 44), bl = (t > bA && t < bA + 0.08) || (t > bA + 0.17 && t < bA + 0.24);
      return { root: { rx: -PI / 2, y: -0.92, pivot: 'hips' }, ...arms(m([0, 0, 1.1], [0, 0, 1.1]), m([0, 0, 1.3 + 0.25 * hit], [0, 0, 1.3 - 0.25 * hit])), hipL: [0, 0, 0.5], hipR: [0, 0, -0.5], footL: [0, 0, 0.5], footR: [0, 0, -0.5], head: [0, 0, 0.1 * hit],
        toon: { sq: [W * (1 + 0.12 * hit), (p.long ?? 0.82) * (1 + 0.08 * hit), flat * (1 + 0.8 * hit)], scl: { head: [1.8, 1.6, 2.6] }, face: { expr: t < bA - 0.04 ? 'dizzy' : bl ? 'blink' : (p.expr ?? 'deadpan'), exprW: 1, stars: p.stars ?? 0 } } }; }
    const sy = mix(0.12, 1, back(u / 0.3, 3.4)) + 0.07 * wob(u - 0.3, 30, 6), sx = mix(1.6, 1, eo(u / 0.25)) / Math.sqrt(Math.max(0.3, Math.min(1.4, sy))), k = 1 - eo(u / 0.3);
    return { ...arms(m([0, 0, 1.45 * k + 0.2 * (1 - k)], [0, 0, 1.45 * k + 0.2 * (1 - k)]), m([-0.08 * (1 - k), 0, 0.1 * k - 0.3 * (1 - k)], [-0.08 * (1 - k), 0, 0.1 * k - 0.3 * (1 - k)])), hipL: [0, 0, 0.5 * k], hipR: [0, 0, -0.5 * k], head: [0, 0, 0],
      toon: { sq: [sx, sy, sx], face: { expr: 'dizzy', exprW: 1 - eo(u / 0.5), stars: (p.stars ?? 0) * (1 - eo(u / 0.8)) } } };
  },
  // the wave of an official: the upper arm level, the forearm upright, the hand turning at the wrist (never a straight raised arm: a freeze frame of it
  // reads as a salute). p.side 'R' / 'L'; p.flickAt: one last quick flick of the hand; p.fore (1.5): the elbow (1.78 puts the forearm upright: a forearm
  // stretched from the story then grows straight up); p.foreAmp (1): how much the forearm sways with the wave (0.3 when it is stretched: its end swings far)
  royalWave: (t, p = {}) => { const w = S(t * (p.freq ?? 7.5)), fl = p.flickAt != null ? wob(t - p.flickAt, 36, 9) : 0, L = (p.side ?? 'R') === 'L', up = [0, 0, 1.36 + 0.03 * w], fore = [0, 0, (p.fore ?? 1.5) + (p.foreAmp ?? 1) * (0.1 * w + 0.45 * fl)], rest = [0, 0, 0.08], restE = [-0.1, 0, 0], hand = [0, 0.6 * w, 0.3 * w + 0.9 * fl];
    return { ...arms(m(L ? up : rest, L ? rest : up), m(L ? fore : restE, L ? restE : fore)), [L ? 'handL' : 'handR']: L ? hand : [hand[0], -hand[1], -hand[2]], head: [-0.06, 0, 0.04 * w], torso: [-0.05, 0, 0] }; },
  // seated, a phone at the right ear; the left hand holds a rubber stamp: wind-up with the arm stretched above the head (held, trembling), a two-frame slam on
  // the desk at p.hit, the whole body squashing on the hit, then a satisfied look at the result and back to the call (she keeps moving)
  stampDesk: (t, p = {}) => { const hit = p.hit ?? 0.8, u = t - hit, up = back((t - (hit - 0.42)) / 0.2, 1.8), dn = ei((t - (hit - 0.07)) / 0.07), a = up * (1 - dn), sh = u < -0.07 && u > -0.24 ? 1 : 0, reb = wob(u, 30, 8), nod = u > 0 ? Math.max(0, 1 - u * 2.4) : 0, life = eo((u - 0.3) / 0.3);
    return { ...CLIPS.sit(t), shoulderR: [-0.3, 0, -0.42 - 0.06 * a], elbowR: [-2.55, 0, 0], handR: [0, 0.4, 0],
      shoulderL: [-0.6 - 2.3 * a + 0.14 * reb - 0.3 * life, 0, 0.12 + 0.15 * a], elbowL: [-0.7 + 0.6 * a - 0.35 * life, 0, 0],
      head: [0.08 - 0.3 * a + 0.4 * nod + 0.04 * life * S(t * 4.4), -0.1 + 0.3 * life * (0.6 + 0.4 * S(t * 2.2)), -0.08 + 0.12 * life], torso: [0.04 - 0.22 * a + 0.3 * nod, 0.12 * a - 0.08 * life, 0],
      toon: { sq: sqv(1 + 0.08 * a - (u > 0 && u < 0.35 ? 0.16 * reb : 0)), bend: { spine: [-0.3 * a + 0.3 * nod, 0, 0.15 * a, 1 + 0.06 * a, null], armL: [0, 0, 0, 1 + 0.75 * a, null], foreL: [0.3 * sh * S(t * 60), 0, 0, 1 + 0.75 * a, null] }, ears: 0.5 * reb,
        face: { expr: u < 0 ? (p.wind ?? 'determined') : (p.expr ?? 'smug'), exprW: Math.max(Math.min(1, a * 2), u > 0 ? 1 : 0) } } }; },
  // hang time with a phone in the right hand (it follows walkRead: the same arm): the feet stop, the phone moves aside, the head goes down past it (p.downAt),
  // then up to us (p.usAt), a gulp that runs down the neck. Then let him fall with a move
  hangPhone: (t, p = {}) => { const dA = p.downAt ?? 0.15, uA = p.usAt ?? 0.5, dn = eo((t - dA) / 0.14), us = eo((t - uA) / 0.09), look = dn * (1 - us), walk = Math.max(0, 1 - t / 0.16), ph = t * 2 * PI * 2.2, g = t - uA - 0.16, gulp = g > 0 && g < 0.2 ? S(g / 0.2 * PI) : 0, tr = us * 0.012 * S(t * 55);
    return { shoulderR: [-1.0 + 0.2 * look + 0.3 * us, 0.3 - 0.5 * look, 0.05 - 0.25 * look], elbowR: [-1.8 + 0.25 * look + 0.45 * us, 0, 0], handR: [0.3, 0, 0], shoulderL: [0, 0, 0.2 + 0.45 * us], elbowL: [-0.08 - 0.3 * us, 0, -0.3],
      hipL: [-0.4 * walk * S(ph), 0, 0.05 + 0.05 * us], hipR: [0.4 * walk * S(ph), 0, -0.05 - 0.05 * us], kneeL: [0.3 * walk, 0, 0], kneeR: [0.3 * walk, 0, 0], footL: [0.45 * us, 0, 0], footR: [0.45 * us, 0, 0],
      head: [0.36 + 0.3 * look - 0.36 * us, tr, 0], torso: [0.06 + 0.06 * look - 0.06 * us, 0, 0], root: { y: 0.01 * S(t * 3), x: tr * 0.3 },
      toon: { sq: sqv(1 - 0.06 * gulp + 0.05 * us), bend: { spine: [0.18 * look, 0, 0, 1, null], neck: [0.25 * look, 0, 0, 1 + 2.2 * look + 0.25 * gulp, 1 + 0.5 * gulp] }, ears: 0.4 * us, face: { expr: us > 0.5 ? (p.expr ?? 'gulp') : 'lookDown', exprW: Math.max(look, us) } } }; },
  // one arm straight up as far as it goes (the other pinned as in `squeezed`), the hand fumbling at the top, the head thrown back to watch it. p.side 'L' / 'R'.
  // Stretch the arm from the story: toon bend armL / foreL [0, 0, 0, 3.6, 0.6]
  reachHigh: (t, p = {}) => { const L = (p.side ?? 'L') === 'L', w = S(t * 34), up = [0, 0, 3.02 + 0.03 * S(t * 23)], hand = [0.5 * w, 0, 0.5 * S(t * 34 + 1.2)], sq = CLIPS.squeezed(t, p);
    return { ...sq, ...(L ? { shoulderL: up, elbowL: [0, 0, 0.06], handL: hand } : { shoulderR: [0, 0, -up[2]], elbowR: [0, 0, -0.06], handR: hand }), head: [-0.5, (L ? 1 : -1) * 0.12, 0],
      toon: { bend: { [L ? 'armL' : 'armR']: [0, 0.1 * S(t * 23), 0, 1, null], [L ? 'foreL' : 'foreR']: [0, -0.16 * S(t * 23 + 1), 0, 1, null] } } }; },
  // head first into something soft and stuck there (a diver's arrival): upside down, the legs up in the air and wobbling (dying out), the arms pushing in vain.
  // The actor's position is where the head goes in; p.sink (0.2 m)
  headStuck: (t, p = {}) => { const w = wob(t + 0.02, p.freq ?? 21, p.decay ?? 3.2), w2 = wob(t + 0.05, 17, 3); return { root: { rx: PI + 0.1 * w, rz: 0.12 * w2, y: 0.42 - (p.sink ?? 0.2), pivot: 'hips' },
      ...arms(m([0.4 * S(t * 16), 0, 0.5], [0.4 * S(t * 16 + 2), 0, 0.5]), m([-0.9, 0, 0], [-0.9, 0, 0])), hipL: [0.5 * w + 0.25 * S(t * 11), 0, 0.3], hipR: [-0.5 * w + 0.25 * S(t * 11 + PI), 0, -0.3], kneeL: [0.5 + 0.4 * S(t * 11), 0, 0], kneeR: [0.5 + 0.4 * S(t * 11 + PI), 0, 0], head: [0, 0, 0],
      toon: { sq: sqv(1 - 0.18 * Math.exp(-t * 9) * Math.cos(t * 30)), bend: { spine: [0.25 * w, 0.2 * w2, 0, 1, null], legL: [0, 0.3 * w2, 0, 1.1, null], legR: [0, 0.3 * w2, 0, 1.1, null] } } }; },
  // melting from the top down (p.dur 0.45 s): the head sinks into the shoulders and droops, the arms run down to the ground, then the whole body spreads into a
  // puddle; p.landAt: something lands on the puddle (the hat he left in the air: a prop), it jiggles
  meltDown: (t, p = {}) => { const d = p.dur ?? 0.45, land = p.landAt != null ? wob(t - p.landAt, 30, 8) : 0;
    if (p.sink) {   // p.sink: upright, like a candle: the head sags into the shoulders, the shoulders droop and the arms run down, the trunk shortens and widens,
      // then the legs (he goes down into his shoes), and only at the end the film. Nothing tips forward: a fold at the waist reads as a bow, not as a melt
      const k1 = eio(t / (d * 0.4)), k2 = eio((t - d * 0.18) / (d * 0.5)), k3 = eio((t - d * 0.4) / (d * 0.5)), k4 = eio((t - d * 0.72) / (d * 0.28)), sL = 1 - 0.78 * k3, wv = 0.05 * S(t * 21) * k2 * (1 - k4);
      return { ...arms(m([0, 0, 0.06 + 0.06 * k2], [0, 0, 0.06 + 0.06 * k2]), m([0, 0, 0], [0, 0, 0])), head: [0.14 * k1, 0, wv], torso: [0.05 * k2, 0, wv * 0.6], hipL: [0, 0, 0.1 * k3], hipR: [0, 0, -0.1 * k3], root: { y: -0.94 * (1 - sL) },
        toon: { sq: [(1 + (p.spread ?? 0.6) * (0.1 * k2 + 0.3 * k3 + 0.6 * k4)) * (1 + 0.08 * land), (1 - (p.flat ?? 0.8) * k4) * (1 - 0.3 * land), (1 + (p.spread ?? 0.6) * (0.1 * k2 + 0.3 * k3 + 0.6 * k4)) * (1 + 0.08 * land)],
          bend: { neck: [0.2 * k1, 0, 0, 1 - 0.75 * k1, 1 + 0.6 * k1], spine: [0.1 * k2, 0, wv, 1 - 0.68 * k2, 1 + 0.75 * k2], armL: [0, 0, 0, 1 + 0.35 * k1 - 0.6 * k3, 1 + 0.5 * k3], armR: [0, 0, 0, 1 + 0.35 * k1 - 0.6 * k3, 1 + 0.5 * k3], foreL: [0, 0, 0, 1 + 0.45 * k2 - 0.7 * k3, 1 + 0.5 * k3], foreR: [0, 0, 0, 1 + 0.45 * k2 - 0.7 * k3, 1 + 0.5 * k3],
            legL: [0, 0, 0, sL, 1 + 0.7 * k3], legR: [0, 0, 0, sL, 1 + 0.7 * k3], shinL: [0, 0, 0, sL, 1 + 0.7 * k3], shinR: [0, 0, 0, sL, 1 + 0.7 * k3] },
          scl: { head: [1 + 0.3 * k1 + 0.2 * k2, 1 - 0.5 * k1 - 0.2 * k2, 1 + 0.2 * k1] }, face: { expr: p.expr ?? 'cry', exprW: Math.min(1, k1 * 1.5) } } };
    }
    const k1 = eio(t / (d * 0.55)), k2 = eio((t - d * 0.3) / (d * 0.7)), sy = 1 - (p.flat ?? 0.8) * k2;   // p.flat 0.97: down to a film (then hide him and show a puddle prop: props_trou.js meltPuddle)
    return { ...arms(m([0, 0, 0.1 + 0.25 * k2], [0, 0, 0.1 + 0.25 * k2]), m([0, 0, 0], [0, 0, 0])), head: [0.55 * k1, 0, 0.12 * k1], neck: [0.3 * k1, 0, 0], torso: [0.25 * k1, 0, 0], hipL: [0, 0, 0.35 * k2], hipR: [0, 0, -0.35 * k2], kneeL: [0.4 * k1 * (1 - k2), 0, 0], kneeR: [0.4 * k1 * (1 - k2), 0, 0],
      toon: { sq: [(1 + (p.spread ?? 0.95) * k2) * (1 + 0.08 * land), sy * (1 - 0.3 * land), (1 + (p.spread ?? 0.95) * k2) * (1 + 0.08 * land)], bend: { spine: [0.45 * k1, 0, 0, 1 - 0.25 * k1 * (1 - k2), 1 + 0.25 * k1], neck: [0.3 * k1, 0, 0, 1 - 0.5 * k1, null], armL: [0, 0, 0, 1 + 0.75 * k1, null], armR: [0, 0, 0, 1 + 0.75 * k1, null], foreL: [0, 0, 0, 1 + 0.5 * k1, null], foreR: [0, 0, 0, 1 + 0.5 * k1, null] },
        scl: { head: [1 + 0.25 * k2, 1 - 0.3 * k2, 1] }, face: { expr: p.expr ?? 'cry', exprW: Math.min(1, k1 * 1.5) } } }; },
  // the neck as a rubber hose (the periscope again, but alive): it shoots up with an overshoot (p.len x), sways in an arc, the head staying level on top like
  // the elbow of a periscope; the head yaw is left to the look keys. p.backAt drops it
  hoseNeck: (t, p = {}) => { const at = p.backAt ?? 1e9, u = t - at, k = u < 0 ? back(t / 0.26, 2.6) : 1 - back(u / 0.18, 2.5), len = 1 + ((p.len ?? 10) - 1) * Math.max(0, k), sw = (p.curve ?? 0) * Math.max(0, k) + (p.sway ?? 0.5) * (S(t * 4.2) * 0.6 + 0.9 * wob(t - 0.2, 15, 3.5)), fw = (p.lean ?? 0) * Math.max(0, k) + 0.22 * S(t * 3.1 + 1) + 0.5 * wob(t - 0.18, 19, 4);   // p.curve / p.lean (rad): a standing arc to the side / forward (a swan's neck, not a stick)
    return { ...CLIPS.squeezed(t, p), head: [-fw * 0.9, 0, -sw * 0.95], toon: { bend: { neck: [fw, sw, 0, len, p.fat ?? 0.5] }, sq: sqv(1 + (u > 0 ? 0.08 * wob(u - 0.12, 30, 7) : 0) - 0.07 * Math.exp(-t * 14)) } }; },
});

// ---- cycle 2 (story 38): a sneeze and what it does to people. Hand poses under toon.hands need the finger hands (script `fingers: true`)
Object.assign(CLIPS, {
  // the build-up of a sneeze: breaths in, each one bigger (the chest fills, the head goes back, he rises on his toes and off the ground), the index finger
  // comes up under the nose. p.dur (0.9 s) for p.breaths (3), p.float (0.25 m)
  sneezeUp: (t, p = {}) => {
    // p.times [t0, t1, ...]: when each breath starts, instead of p.breaths even ones over p.dur (shorter and shorter gaps make it a ratchet); p.last: the span of the
    // last breath; p.tremble: how much more he shakes once the last breath is in (the apex, held)
    const d = p.dur ?? 0.9, n0 = p.breaths ?? 3, st = d / n0, T = p.times || Array.from({ length: n0 }, (_, i) => i * st), n = T.length, span = i => (i < n - 1 ? T[i + 1] - T[i] : (p.last ?? (n > 1 ? T[n - 1] - T[n - 2] : st))); let L = 0;
    for (let i = 0; i < n; i++) { const u = t - T[i], sp = span(i); if (u > 0) L += (eo(u / (sp * 0.42)) - (i < n - 1 ? 0.22 * S(c01((u - sp * 0.5) / (sp * 0.5)) * PI) : 0)) / n; }
    L = Math.max(0, L); const apex = c01((t - T[n - 1] - span(n - 1) * 0.42) / 0.12), tr = 0.012 * S(t * 49) * L * (1 + (p.tremble ?? 0) * apex), up = eo(t / 0.22), bk = p.back ?? 1;   // p.back (1): how far the head and the chest go back (0.6 when the camera must keep the face)
    let inh = 0; for (let i = 0; i < n; i++) { const u = (t - T[i]) / (span(i) * 0.42); if (u > 0 && u < 1) inh = Math.max(inh, S(u * PI)); }   // each inhale pulls the tie and the hair toward his nose
    return { ...arms(m([0.25 * L, 0, 0.3 + 0.45 * L], [-(p.shx ?? 1.0) * up - (p.shxL ?? 0.85) * L, ((p.armIn ?? -0.75) + (p.armInL ?? -0.6) * L) * up, (0.05 - 0.25 * L) * up + 0.2 * (1 - up)]), m([-0.2 * L, 0, 0.1], [-(p.elb ?? 2.3) * up + (p.elbL ?? 0.6) * L, 0, 0])), handR: [0, (p.wrist ?? (p.ik ? 0 : 1.3)) * up, 0], head: [-0.28 * bk * L + tr, 0, tr], torso: [-0.2 * bk * L, 0, 0], neck: [-0.1 * bk * L, 0, 0],   // the arm reaches round the swollen chest: its numbers grow with L
      footL: [0.55 * L, 0, 0], footR: [0.55 * L, 0, 0], root: { y: (p.float ?? 0.25) * L * L + 0.03 * L },
      toon: { sq: sqv(1 + 0.07 * L), wind: [0, 5 * L + 7 * inh, 2 * L + 2 * inh], hairUp: 0.55 * L, bend: { spine: [-0.18 * bk * L, 0, 0, 1 + 0.08 * L, 1 + 0.75 * L], armR: [0, 0, 0, 1 + (p.armS ?? 0.15) * L, null], foreR: [0, 0, 0, 1 + (p.foreS ?? 0.45) * L, null] }, scl: { head: [1 + 0.1 * L, 1, 1 + 0.1 * L] }, hands: { R: 'point', L: 'spread' },
        ...(p.ik ? { touch: { R: ['face', p.nx ?? 0.06, p.ny ?? 0.3, p.nz ?? 0.025, up * p.ik, p.tip ?? 0.16, [-1, p.elbUp ?? 0.2, p.elbFwd ?? 0.3]] } } : null),   // p.ik 1: the index is held under the nose by the guided hand (toon channel `touch`), whatever the head and the chest do; the elbow out to the side
        face: { expr: p.expr ?? 'strain', exprW: Math.min(1, 0.4 + L), jaw: 0.42 * L } } };   // jaw under 0.45: a round « aah », not a laugh
  },
  // the sneeze itself: the body whips forward in two frames, holds bent and shaking (p.hold 0.3 s), then comes back up dazed. The recoil is a move of the story
  // p.fold (1): how far the body folds; p.chin (0): the head held up by that much (rad) while the body folds: seen from the front the face stays on us, mouth wide
  sneeze: (t, p = {}) => { const w = eo(t / 0.06), hold = p.hold ?? 0.3, out = eio((t - 0.06 - hold) / 0.3), k = w * (1 - out), sh = k * S(t * 57) * 0.02, fo = p.fold ?? 1, ch = p.chin ?? 0;
    return { ...arms(m([0.9 * k, 0, 0.55 * k + 0.2], [0.9 * k, 0, 0.55 * k + 0.2]), m([-0.3 * k - 0.08, 0, -0.3 * (1 - k)], [-0.3 * k - 0.08, 0, -0.3 * (1 - k)])), torso: [0.75 * fo * k, 0, sh], head: [(0.55 - ch) * k + sh, 0, 0], neck: [(0.2 - 0.3 * ch) * k, 0, 0],
      hipL: [-0.5 * k, 0, 0.08], hipR: [-0.5 * k, 0, -0.08], kneeL: [0.6 * k, 0, 0], kneeR: [0.6 * k, 0, 0], root: { y: 0.1 * k * (1 - c01(t / 0.25)), x: sh },
      toon: { sq: [1 + 0.1 * k, 1 - 0.14 * k, 1 + 0.3 * k], bend: { spine: [0.75 * fo * k, 0, 0, 1, null] }, hands: { L: 'spread', R: 'spread' }, ears: 0.8 * k, face: { expr: out > 0.5 ? (p.after ?? 'dizzy') : 'strain', exprW: 1, jaw: k, tongue: 0.5 * k } } }; },
  // a small sniff (or two: p.n): the nose goes up, the chest takes a little air, the finger comes to the nose. Everybody around should react
  sniff: (t, p = {}) => { const n = p.n ?? 2, st = 0.2, i = Math.min(n - 1, Math.floor(t / st)), u = c01((t - i * st) / st), k = t < n * st ? S(u * PI) : 0, up = p.held ? 1 : eo(t / 0.15);   // p.held: the finger is already at the nose (a second sniff keyed after a first)
    return { ...CLIPS.stand(), shoulderR: [-1.0 * up, 0, -0.26 * up - 0.2 * (1 - up)], elbowR: [-2.2 * up - 0.08 * (1 - up), 0, 0.3 * (1 - up)], handR: p.ik ? [0, 0, 0] : [0, 0, -1.2 * up], head: [-0.22 * k - 0.05 * up, 0, 0.04 * k], torso: [-0.08 * k, 0, 0],
      toon: { sq: sqv(1 + 0.03 * k), wind: [0, 8 * k, 2 * k], bend: { spine: [-0.08 * k, 0, 0, 1, 1 + 0.22 * k] }, hands: { R: 'point' }, face: { expr: p.expr ?? 'strain', exprW: 0.5 + 0.5 * k, jaw: 0.15 * k },
        ...(p.ik ? { touch: { R: ['face', 0.06, 0.3, 0.025, up * p.ik, 0.16, [-1, 0.2, 0.3]] } } : null) } }; },   // p.ik 1: the index held under the nose by the guided hand (as in sneezeUp); each sniff lifts the tie
  // blown flat against a wall behind him like a poster (key it with blend=0.02 at the end of a fast glide to the wall): arms and legs spread, as thin as paper;
  // from p.slideAt he peels off from the top and slides down, swaying. The actor's back is to the wall; p.high: how far off the ground he is stuck
  poster: (t, p = {}) => { const hit = Math.exp(-t * 22) * Math.cos(t * 40), sl = Math.max(0, t - (p.slideAt ?? 0.5)), peel = eo(sl / 0.5) * (p.peelK ?? 1);   // p.peelK (1): 3 = he comes off head first, folded over, like wallpaper
    return { ...arms(m([0, 0, 1.3 + 0.15 * hit], [0, 0, 1.3 - 0.15 * hit]), m([0, 0, 0.35], [0, 0, 0.35])), hipL: [0, 0, 0.42], hipR: [0, 0, -0.42], head: [0.35 * peel, 0, 0.12 * S(t * 2.3)], torso: [0.25 * peel, 0, 0],
      root: { y: (p.high ?? 0.35) - (p.slide ?? 0.5) * sl, rz: 0.06 * S(t * 2.1) * (0.3 + peel) },
      toon: { sq: [1.22 * (1 + 0.1 * hit), 1.06, (p.flat ?? 0.07) * (1 + 0.6 * hit)], bend: { spine: [0.3 * peel, 0, 0, 1, null] }, hands: { L: 'spread', R: 'spread' }, face: { expr: p.expr ?? 'dizzy', exprW: 1, stars: p.stars ?? 0 } } }; },
  // spun like a top by something held up at arm's length (an anemometer): the right arm up, the body turning faster and faster (p.turns [[t, turns/s], ...]),
  // the spine and a leg twisted behind the turn; when the speed has fallen he staggers
  spinTop: (t, p = {}) => { const keys = p.turns || [[0, 0], [0.3, 4], [0.9, 4], [1.2, 0]]; let a = 0, v = keys[0][1];
    for (let i = 0; i < keys.length; i++) { const [t0, v0] = keys[i], nx = keys[i + 1]; if (t <= t0) break; const t1 = nx ? Math.min(t, nx[0]) : t, v1 = nx ? v0 + (nx[1] - v0) * (t1 - t0) / Math.max(1e-6, nx[0] - t0) : v0; a += (v0 + v1) / 2 * (t1 - t0); v = v1; }
    const k = Math.min(1, Math.abs(v) / 3), end = keys[keys.length - 1][0], dz = t > end ? wob(t - end, 9, 1.6) : 0;
    return { ...arms(m([0.2, 0, 0.9 * k + 0.2], [-0.1, 0, 2.5]), m([0, 0, 0.2 * k], [0, 0, 0.15])), head: [0.1 * dz, 0.5 * dz, 0.25 * dz - 0.15 * k], torso: [0, 0, 0.2 * dz], hipL: [0, 0, 0.1 + 0.25 * k], hipR: [0.3 * k, 0, -0.1], kneeR: [0.5 * k, 0, 0],
      root: { ry: a * 2 * PI, x: 0.12 * dz, y: 0.06 * k },
      toon: { sq: sqv(1 + 0.1 * k), bend: { spine: [0, 0.2 * dz, -0.9 * k, 1 + 0.06 * k, null], legL: [0, 0, -0.6 * k, 1, null], armL: [0, 0.4 * k, 0, 1 + 0.3 * k, null] }, hands: { R: 'grip', L: 'spread' },
        face: { expr: k > 0.3 || t > end ? 'dizzy' : (p.expr ?? 'determined'), exprW: 1, jaw: 0.4 * k } } }; },
  // hit on the top of the head by something heavy at p.at (a big stamp): the head is driven into the shoulders (no neck left, the head squashed, shoulders up),
  // held four frames, then it springs out too far and wobbles; the eyes cross while it is in
  headHammer: (t, p = {}) => { const u = t - (p.at ?? 0.3), inn = u < 0 ? 0 : u < 0.03 ? u / 0.03 : u < 0.17 ? 1 : 1 - back((u - 0.17) / 0.16, 3.2), w = u > 0.33 ? wob(u - 0.33, 28, 6) : 0, pos = Math.max(0, inn);
    return { ...arms(m([0, 0, 0.2 + 0.35 * pos], [0, 0, 0.2 + 0.35 * pos]), m([-0.08, 0, -0.3], [-0.08, 0, -0.3])), head: [0.05 * w, 0, 0.1 * w],
      toon: { sq: sqv(1 - 0.1 * pos + 0.05 * w), bend: { neck: [0, 0, 0, Math.max(0.12, 1 - 0.85 * inn + 0.4 * w), 1 + 0.6 * pos], spine: [0, 0, 0, 1 - 0.12 * pos, null] }, scl: { head: [1 + 0.3 * pos, 1 - 0.3 * pos, 1 + 0.2 * pos] },
        hands: { L: 'spread', R: 'spread' }, face: { expr: inn > 0.3 ? 'dizzy' : (p.expr ?? 'unimpressed'), exprW: 1, cross: pos } } }; },
  // swept off his feet by a blast from in front (use it on a fast glide backward): folded like a hairpin, arms and legs trailing toward where the wind comes
  // from, the head forward, the whole body tipped back
  blownBack: (t, p = {}) => { const f = t * 31, k = eo(t / 0.07);
    return { root: { rx: -0.55 * k, y: 0.25 * k, pivot: 'hips' }, ...arms(m([-1.5 * k + 0.1 * S(f), 0, 0.25], [-1.5 * k + 0.1 * S(f + 2), 0, 0.25]), m([-0.2, 0, 0], [-0.2, 0, 0])), hipL: [-1.15 * k + 0.1 * S(f * 0.8), 0, 0.12], hipR: [-0.95 * k + 0.1 * S(f * 0.8 + 2), 0, -0.12], kneeL: [0.25, 0, 0], kneeR: [0.4, 0, 0],
      head: [0.5 * k, 0, 0], torso: [0.35 * k, 0, 0],
      toon: { sq: [1, 1, 1 + 0.25 * k], bend: { spine: [0.5 * k, 0, 0, 1, null], armL: [0, 0, 0, 1.25, null], armR: [0, 0, 0, 1.25, null], legL: [0, 0, 0, 1.15, null], legR: [0, 0, 0, 1.15, null] }, hands: { L: 'spread', R: 'spread' }, ears: 0.7 * k, face: { expr: p.expr ?? 'take', exprW: k, jaw: 0.8 * k } } }; },
  // a big stamp brought down on something as high as a head, an arm's length in front (p.hit): the right arm goes up and back, he rises on his toes and leans
  // back (held, trembling), then the arm comes over in two frames to point up and forward, the body lunging after it; a small rebound. The story stretches
  // the arm (toon armR / foreR x1.7 at the hit) so that the hand ends 0.8 m above his shoulder, 0.85 m in front
  stampDown: (t, p = {}) => { const hit = p.hit ?? 0.5, u = t - hit, a = back(t / Math.max(0.12, hit - 0.16), 1.5), d = c01((t - (hit - 0.066)) / 0.066), reb = wob(u, 26, 7), sh = a > 0.95 && d === 0 ? 0.02 * S(t * 55) : 0,
      r = eio((u - (p.rest ?? 0.3)) / 0.28);   // p.rest (0.3 s after the hit): he takes the stamp back and holds it in front of him, pleased
    return { shoulderR: [mix(-0.3 - 2.95 * a + 0.4 * d + 0.08 * reb + sh, -1.25, r), 0, 0.05], elbowR: [mix(-0.1 - 0.9 * a * (1 - d), -1.1, r), 0, 0], shoulderL: [mix(0.5 * a - 0.9 * d, 0, r), 0, 0.2], elbowL: [-0.4, 0, -0.2],
      torso: [mix(-0.22 * a + 0.52 * d + 0.05 * reb, -0.04, r), 0, 0], head: [mix(-0.2 * a + 0.32 * d, -0.08, r), 0, 0], footL: [0.5 * a * (1 - d), 0, 0], footR: [0.5 * a * (1 - d), 0, 0], root: { y: 0.07 * a * (1 - d) },
      toon: { hands: { R: 'grip' }, sq: sqv(1 + 0.08 * a * (1 - d) - 0.1 * d * Math.max(0, 1 - u * 6)) } }; },
  // stiff as a plank, he tips over backward (p.dir -1) or forward (+1) about his heels in p.dur (0.4 s) and lands flat with one small bounce: the delayed
  // fall of somebody who has just been hit on the head. p.hang (0 s): first he hangs that long, leaning p.lean (0.17 rad) and trembling: the time suspended
  // before the fall. p.feet (0 rad): once flat his legs flip up by that much, stay up a third of a second, then drop
  plankFall: (t, p = {}) => { const d = p.dur ?? 0.4, dir = p.dir ?? -1, hang = p.hang ?? 0, ln = hang ? (p.lean ?? 0.17) : 0, u = t - hang, k = c01(u / d), land = u - d,
      b = land > 0 ? 0.07 * Math.exp(-land * 9) * Math.abs(S(land * 24)) : 0, ang = u < 0 ? ln * eo(t / (hang * 0.7)) * (1 + 0.1 * S(t * 26)) : ln + (1.5 - ln) * k * k - b,
      fu = land > 0 && p.feet ? p.feet * Math.min(1, land / 0.07) * (land < 0.34 ? 1 : Math.exp(-(land - 0.34) * 9)) : 0, tw = fu ? 0.12 * S(land * 38) * fu : 0;
    return { ...CLIPS.stiff(), head: [0, 0, 0], hipL: [dir * (fu + tw), 0, 0.05], hipR: [dir * (0.8 * fu - tw), 0, -0.05], root: { rx: dir * ang }, toon: { face: { expr: p.expr ?? 'dizzy', exprW: 1 } } }; },
  // a handshake that is too hearty. p.role 'pump': the one who shakes (right arm out, the forearm pumping, the body firm, a grin); 'wave': the one who is
  // shaken: the pumping travels up his arm as a wave (arm, forearm), into the spine and the head, his feet leave the ground on each stroke.
  // p.freq (6 strokes/s), p.stopAt: the shaking stops (the wave dies out); p.thumbAt (pump): the left thumb comes up
  shakeHands: (t, p = {}) => { const f = (p.freq ?? 6) * 2 * PI, st = p.stopAt ?? 1e9, live = t < st ? Math.min(1, t / 0.12) : Math.exp(-(t - st) * 7), a = S(t * f) * live;
    if ((p.role ?? 'pump') === 'pump') { const th = p.thumbAt != null ? eo((t - p.thumbAt) / 0.14) : 0;
      return { shoulderR: [-1.15 + 0.12 * a, 0, 0.1], elbowR: [-0.5 - 0.45 * a, 0, 0], shoulderL: [-1.5 * th, 0, 0.15 + 0.35 * th], elbowL: [-0.25 - 1.3 * th, 0, 0], torso: [0.1 + 0.04 * a, 0, 0], head: [-0.05, 0, 0.04 * a], root: { y: 0.012 * Math.abs(a) },
        toon: { hands: { R: 'grip', L: th > 0.3 ? 'thumbUp' : 'rest' }, bend: { spine: [0.05 * a, 0, 0, 1, null] } } }; }
    const w1 = S(t * f - 0.9) * live, w2 = S(t * f - 1.8) * live, w3 = S(t * f - 2.7) * live;   // the wave arrives later the further from the hand
    return { shoulderR: [-1.2, 0, 0.1], elbowR: [-0.35, 0, 0], shoulderL: [0.3 * w2, 0, 0.25 + 0.2 * Math.abs(w2)], elbowL: [-0.3, 0, -0.3], head: [0.25 * w3, 0, 0.12 * w3], torso: [0.06 * w2, 0, 0], hipL: [0, 0, 0.06 * Math.abs(w2)], hipR: [0, 0, -0.06 * Math.abs(w2)],
      footL: [0.3 * Math.abs(w2), 0, 0], footR: [0.3 * Math.abs(w2), 0, 0], root: { y: 0.07 * Math.abs(w2) },
      toon: { hands: { R: 'grip' }, bend: { foreR: [0.55 * a, 0, 0, 1.08, null], armR: [-0.5 * w1, 0, 0, 1.05, null], spine: [0.22 * w2, 0, 0.06 * w2, 1 + 0.05 * w2, null], neck: [0.3 * w3, 0, 0, 1 + 0.5 * Math.abs(w3), null] }, sq: sqv(1 + 0.05 * w2),
        face: { expr: p.expr ?? 'dizzy', exprW: Math.min(1, live) } } }; },
  // the same handshake with guided hands (toon channel `reach`): both hold one point, p.grip [x, y, z] (in the world), which pumps up and down, a little more
  // at every stroke (p.amp [first, last] m, p.freq strokes/s) until p.stopAt. role 'pump': he shakes with both hands (p.two 1: the left hand on top), leaning
  // in, bobbing with it; after the release his left thumb goes up high (p.thumbAt). role 'wave': the one who is shaken: his hand is held, and the stroke
  // travels through him two frames later at every joint: shoulder, chest, neck, head; he leaves the ground on the last strokes; after the release he rings
  // down (three wobbles that die out)
  shakeHands2: (t, p = {}) => { const f = (p.freq ?? 3.6) * 2 * PI, st = p.stopAt ?? 1e9, [a0, a1] = p.amp || [0.08, 0.3], g = p.grip || [0, 1.4, 0.4],
      pump = tt => { const u = c01(tt / st); return tt < 0 ? 0 : tt < st ? (a0 + (a1 - a0) * u) * S(tt * f) : 0; },   // metres, at time tt
      rel = c01((t - st) / 0.1), w = (1 - rel) * c01(t / 0.1), ring = t > st ? Math.exp(-(t - st) * 5.5) * S((t - st) * 44) : 0, ring2 = t > st + 0.066 ? Math.exp(-(t - st - 0.066) * 5.5) * S((t - st - 0.066) * 44) : 0;   // after the release he rings like a ruler twanged on a desk: three wobbles in twelve frames, the head two frames behind the chest
    if ((p.role ?? 'pump') === 'pump') { const th = p.thumbAt != null && t > p.thumbAt ? back((t - p.thumbAt) / 0.22, 2.2) : 0, y = pump(t), k = y / a1, tp = p.thumb,   // p.thumb [x, y, z]: where the thumb goes (a point of the world, in clear sky between the two men): the arm is guided there
        pu = p.thumbAt != null ? 0.14 * (S(PI * c01((t - p.thumbAt - 0.34) / 0.14)) + S(PI * c01((t - p.thumbAt - 0.54) / 0.14))) : 0, kt = Math.min(1, th) + pu;   // then it is pumped twice along its way
      return { ...CLIPS.stand(), shoulderL: [tp ? 0 : -2.75 * th, 0, (tp ? 0 : 0.3 * th) + 0.1], elbowL: [(tp ? 0 : -0.35 * th) - 0.2, 0, 0], handL: [0, (p.thumbTwist ?? -1.2) * th, 0], torso: [0.14 * (1 - rel) + 0.1 * k, 0, 0], head: [-0.1 * (1 - rel) - 0.12 * k, 0, 0.05 * k], root: { y: 0.03 * Math.max(0, k) + 0.05 * th * Math.abs(S((t - (p.thumbAt ?? 0)) * 9)) * Math.exp(-Math.max(0, t - (p.thumbAt ?? 0)) * 2.5) },
        toon: { hands: { R: 'grip', L: th > 0.25 ? 'thumbUp' : 'grip' }, reach: { R: [g[0], g[1] + y, g[2], w, 0.05], ...(p.two || tp ? { L: tp && th > 0 ? [g[0] + (tp[0] - g[0]) * kt, g[1] + (tp[1] - g[1]) * (Math.min(1.12, th) + pu), g[2] + (tp[2] - g[2]) * kt, 1, 0.05, [1, -0.5, 0.3]] : [g[0], g[1] + y + 0.07, g[2] + 0.02, p.two ? w : 0, 0.05] } : null) },
          bend: { spine: [0.12 * k, 0, 0, 1, null] }, sq: sqv(1 + 0.04 * k) } }; }
    const D = 0.066, y0 = pump(t), k1 = pump(t - D) / a1, k2 = pump(t - 2 * D) / a1, k3 = pump(t - 3 * D) / a1, up = Math.max(0, k2), lift = Math.max(0, k2 - 0.45) * 0.45;   // the stroke, later at each joint
    return { ...CLIPS.stand(), shoulderL: [0.5 * k2 + 0.5 * ring, 0, 0.25 + 0.3 * Math.abs(k2)], shoulderR: [0.4 * ring2 * rel, 0, -0.1], elbowL: [-0.3 - 0.5 * up, 0, 0], head: [-0.4 * k3 - 0.45 * ring2, 0, 0.14 * k3 + 0.3 * ring2], torso: [-0.1 * k2 + 0.12 * ring, 0, 0.12 * ring],
      hipL: [0.25 * up, 0, 0.08 * up], hipR: [0.25 * up, 0, -0.08 * up], kneeL: [0.5 * up, 0, 0], kneeR: [0.5 * up, 0, 0], footL: [0.5 * up, 0, 0], footR: [0.5 * up, 0, 0], root: { y: 0.1 * up + lift },   // the feet stay planted while he rings
      toon: { hands: { R: 'grip', L: 'spread' }, reach: { R: [g[0], g[1] + y0, g[2], w, 0.05] }, sq: sqv(1 + 0.16 * k1 + 0.14 * ring),
        bend: { spine: [-0.3 * k2 + 0.4 * ring, 0, 0.3 * ring, 1 + 0.1 * k2, null], neck: [-0.35 * k3 + 0.3 * ring2, 0, 0.45 * ring2, 1 + 0.55 * Math.max(0, k3) + 0.5 * Math.abs(ring2), null] },
        face: { expr: p.expr ?? 'dizzy', exprW: Math.min(1, t / 0.3), jaw: 0.3 * Math.max(0, k3), stars: rel, cross: 0.7 * rel } } }; },
  // leaning away from somebody who passes (p.side +1: away toward his own left, -1: toward his right): the body a C, one foot off the ground, hands up
  leanAway: (t, p = {}) => { const sd = p.side ?? 1, k = p.k ?? back(t / 0.22, 2), br = 0.03 * S(t * 3 + (p.ph ?? 0)), L = sd > 0;
    return { ...arms(m([-0.5 * k, 0, 0.5 + 0.3 * k * (L ? 1 : 0.3)], [-0.5 * k, 0, 0.5 + 0.3 * k * (L ? 0.3 : 1)]), m([-1.5 * k, 0, 0], [-1.5 * k, 0, 0])), head: [0, -0.55 * sd * k, 0.2 * sd * k], torso: [0, -0.2 * sd * k, 0],
      hipL: [0, 0, L ? 0.5 * k : 0.05], hipR: [0, 0, L ? -0.05 : -0.5 * k], [L ? 'kneeL' : 'kneeR']: [0.7 * k, 0, 0], root: { x: 0.12 * sd * k, y: br * 0.2 },
      toon: { bend: { spine: [0, -0.55 * sd * k + br, 0, 1.05, null], neck: [0, -0.2 * sd * k, 0, 1 + 0.5 * k, null] }, hands: { L: 'spread', R: 'spread' }, face: { expr: p.expr ?? 'scared', exprW: Math.min(1, k) } } }; },
});

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
