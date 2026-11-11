// The "shaders" look (script.look = 'shaders'): Minecraft-shader-style light on top of the paper style.
//   - a stronger, warmer, lower sun with soft shadows tinted by a bluer sky fill (setupLights)
//   - ground-truth ambient occlusion in creases and contact points (GTAO at half resolution)
//   - light shafts from the sun when it is in frame (screen-space march over the depth buffer: sky = far plane)
//   - bloom on bright spots, distance haze outdoors, ACES tone mapping, a warm-highlight / teal-shadow grade
// Everything is a pure function of the frame (no temporal accumulation), so frames stay deterministic.
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const isSky = o => o.isMesh && o.renderOrder === -10 && o.material?.side === THREE.BackSide;
const vertex = 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }';

const ShaftShader = {
  uniforms: { tDiffuse: { value: null }, tDepth: { value: null }, sunPos: { value: new THREE.Vector2(0.5, 0.8) }, sunOn: { value: 0 }, sunColor: { value: new THREE.Color('#FFE2B8') }, intensity: { value: 0.55 }, aspect: { value: 9 / 16 } },
  vertexShader: vertex,
  fragmentShader: `
    uniform sampler2D tDiffuse, tDepth; uniform vec2 sunPos; uniform float sunOn, intensity, aspect; uniform vec3 sunColor; varying vec2 vUv;
    void main() {
      vec4 base = texture2D(tDiffuse, vUv);
      if (sunOn <= 0.001) { gl_FragColor = base; return; }
      const int N = 40; vec2 delta = (vUv - sunPos) * (0.92 / float(N)); vec2 uv = vUv; float illum = 1.0, acc = 0.0;
      for (int i = 0; i < N; i++) { uv -= delta; float z = texture2D(tDepth, clamp(uv, 0.001, 0.999)).x; acc += step(0.99999, z) * illum; illum *= 0.965; }
      acc /= float(N);
      vec2 dd = (vUv - sunPos) * vec2(1.0, 1.0 / aspect); float glow = exp(-length(dd) * 2.4);
      gl_FragColor = vec4(base.rgb + sunColor * (acc * (0.35 + 1.6 * glow)) * intensity * sunOn, base.a);
    }`,
};
const GradeShader = {
  uniforms: { tDiffuse: { value: null }, sat: { value: 1.12 }, contrast: { value: 1.05 }, vignette: { value: 0.18 }, warm: { value: 1.0 }, lift: { value: 0.035 }, tint: { value: new THREE.Vector3(1, 1, 1) },
    dark: { value: 0 }, darkFloor: { value: 0.05 }, darkTint: { value: new THREE.Vector3(0.55, 0.72, 1.0) },
    pool: { value: new THREE.Vector4(0.5, 0.5, 0.2, 0) }, poolTint: { value: new THREE.Vector3(1, 1, 1) }, aspect: { value: 0.5625 } },
  vertexShader: vertex,
  fragmentShader: `
    uniform sampler2D tDiffuse; uniform float sat, contrast, vignette, warm, lift, dark, darkFloor, aspect; uniform vec3 tint, darkTint, poolTint; uniform vec4 pool; varying vec2 vUv;
    void main() {
      vec3 c = texture2D(tDiffuse, vUv).rgb; float l = dot(c, vec3(0.299, 0.587, 0.114));
      c = c * (1.0 - lift * 1.43) + lift;   // lift the shade: navy suits and black robes keep their detail
      c = mix(vec3(l), c, sat); c = (c - 0.5) * contrast + 0.5;
      vec3 shadowTint = vec3(0.94, 0.99, 1.06), hiTint = vec3(1.045, 1.0, 0.94);
      c *= mix(vec3(1.0), mix(shadowTint, hiTint, smoothstep(0.12, 0.85, l)), warm);
      c *= tint;   // a per-shot colour cast (a cold September morning, a warm memory)
      float v = smoothstep(1.05, 0.38, length((vUv - 0.5) * vec2(1.0, 1.15))); c *= mix(1.0 - vignette, 1.0, v);
      c = clamp(c, 0.0, 1.0);
      if (dark > 0.001) {   // the lights are off (scene dark keys): the picture falls to a faint cold silhouette, or to black (darkFloor 0)
        float pk = 0.0;   // a pool of light in the black (scene darkPool: a match, a candle): the picture comes back round one point and falls off to the black
        if (pool.w > 0.001) { float d = length((vUv - pool.xy) * vec2(aspect, 1.0)) / max(pool.z, 0.0001); pk = pool.w * (1.0 - smoothstep(0.15, 1.0, d)); }
        c = mix(c * mix(vec3(1.0), poolTint, min(1.0, pk * 1.5)), darkTint * (darkFloor * dot(c, vec3(0.299, 0.587, 0.114))), dark * (1.0 - pk));
      }
      gl_FragColor = vec4(c, 1.0);
    }`,
};

// A light probe captured from the scene itself (sync port of three's LightProbeGenerator.fromCubeRenderTarget): the sky, the sunlit
// ground and walls around the action, as spherical harmonics. It works with the engine's Lambert materials and stands in for bounced light.
function probeFromCube(renderer, rt, cap = 6) {
  const flip = -1, w = rt.width, data = new Uint16Array(w * w * 4), sh = new THREE.SphericalHarmonics3(), co = sh.coefficients;
  const coord = new THREE.Vector3(), dir = new THREE.Vector3(), basis = [0, 0, 0, 0, 0, 0, 0, 0, 0], px = 2 / w; let total = 0, bad = 0;
  for (let f = 0; f < 6; f++) {
    renderer.readRenderTargetPixels(rt, 0, 0, w, w, data, f);
    for (let i = 0; i < data.length; i += 4) {
      let r = THREE.DataUtils.fromHalfFloat(data[i]), g = THREE.DataUtils.fromHalfFloat(data[i + 1]), b = THREE.DataUtils.fromHalfFloat(data[i + 2]);
      if (!(Number.isFinite(r) && Number.isFinite(g) && Number.isFinite(b))) { bad++; continue; }   // a NaN/Inf texel (some shader) would smear over the whole probe: the frame goes black
      r = Math.min(r, cap); g = Math.min(g, cap); b = Math.min(b, cap);   // a lamp or the sun in view must not flood the ambient
      const pi = i / 4, col = (1 - (pi % w + 0.5) * px) * flip, row = 1 - (Math.floor(pi / w) + 0.5) * px;
      switch (f) { case 0: coord.set(-1 * flip, row, col * flip); break; case 1: coord.set(1 * flip, row, -col * flip); break; case 2: coord.set(col, 1, -row); break;
        case 3: coord.set(col, -1, row); break; case 4: coord.set(col, row, 1); break; case 5: coord.set(-col, row, -1); break; }
      const l2 = coord.lengthSq(), wt = 4 / (Math.sqrt(l2) * l2); total += wt; dir.copy(coord).normalize(); THREE.SphericalHarmonics3.getBasisAt(dir, basis);
      for (let j = 0; j < 9; j++) { co[j].x += basis[j] * r * wt; co[j].y += basis[j] * g * wt; co[j].z += basis[j] * b * wt; }
    }
  }
  const norm = 4 * Math.PI / Math.max(total, 1e-6); for (let j = 0; j < 9; j++) co[j].multiplyScalar(norm);
  const avg = (0.2126 * co[0].x + 0.7152 * co[0].y + 0.0722 * co[0].z) * 0.282095;   // mean radiance around the probe (luminance)
  return { probe: new THREE.LightProbe(sh), avg, bad };
}

let _sunTex = null;
function sunTexture() {
  if (_sunTex) return _sunTex;
  const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d');
  const gr = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  gr.addColorStop(0, 'rgba(255,255,248,1)'); gr.addColorStop(0.12, 'rgba(255,250,232,1)'); gr.addColorStop(0.2, 'rgba(255,236,200,0.55)'); gr.addColorStop(0.5, 'rgba(255,214,160,0.16)'); gr.addColorStop(1, 'rgba(255,200,140,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 256, 256); _sunTex = new THREE.CanvasTexture(c); _sunTex.colorSpace = THREE.SRGBColorSpace; return _sunTex;
}

export function createLook(stage, W, H, o = {}) {
  const { renderer, scene, camera } = stage;
  const natural = !!o.natural;   // 'natural': light captured from the scene (probe), soft shadows, a filmic curve
  renderer.toneMapping = THREE.NeutralToneMapping; renderer.toneMappingExposure = o.exposure ?? 1.0;   // neutral keeps the paper hues; AgX rolls off like film
  if (natural) renderer.shadowMap.type = THREE.VSMShadowMap;   // blurred shadow maps: soft penumbras, like a sun with a size
  const cubeRT = natural ? new THREE.WebGLCubeRenderTarget(48, { type: THREE.HalfFloatType }) : null, cubeCam = natural ? new THREE.CubeCamera(0.05, 400, cubeRT) : null; let probe = null;
  const meterRT = natural ? new THREE.WebGLRenderTarget(48, 86, { type: THREE.HalfFloatType }) : null, meterBuf = natural ? new Uint16Array(48 * 86 * 4) : null;
  const meter = () => {   // the shot's brightness as the camera sees it (linear, before exposure): a centre-weighted light meter
    const prev = renderer.getRenderTarget(); renderer.setRenderTarget(meterRT); renderer.render(scene, camera); renderer.setRenderTarget(prev);
    renderer.readRenderTargetPixels(meterRT, 0, 0, 48, 86, meterBuf); let sum = 0, wsum = 0; const ls = [];
    for (let i = 0; i < meterBuf.length; i += 4) {
      const l = 0.2126 * THREE.DataUtils.fromHalfFloat(meterBuf[i]) + 0.7152 * THREE.DataUtils.fromHalfFloat(meterBuf[i + 1]) + 0.0722 * THREE.DataUtils.fromHalfFloat(meterBuf[i + 2]); if (!Number.isFinite(l)) continue;
      const p = i / 4, x = (p % 48 + 0.5) / 48 - 0.5, y = (Math.floor(p / 48) + 0.5) / 86 - 0.5, w = 1.6 - Math.min(1.2, 2.4 * Math.hypot(x, y * 1.2));   // the centre counts more
      sum += Math.min(l, 2) * w; wsum += w; ls.push(l);
    }
    ls.sort((a, b) => a - b); const q = f => ls.length ? ls[Math.min(ls.length - 1, Math.floor(f * ls.length))] : 0.3;
    return { mean: wsum ? sum / wsum : 0.3, p50: q(0.5), p75: q(0.75) };
  };
  const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
  const composer = new EffectComposer(renderer, rt); composer.setPixelRatio(1);
  composer.addPass(new RenderPass(scene, camera));
  const ao = new GTAOPass(scene, camera, W, H);
    ao.overrideVisibility = function () {   // nothing see-through in the G-buffer: sky dome (leaves depth = far for the shafts), sprites, particles, glass, cut-outs
    const cache = this._visibilityCache; scene.traverse(n => { cache.set(n, n.visible); const m = n.material;
      if (n.isPoints || n.isLine || n.isSprite || isSky(n) || (m && !Array.isArray(m) && (m.transparent || m.alphaTest > 0)) || n.userData.noAO) n.visible = false; });
  };
  ao.blendIntensity = o.ao ?? 1.0;
  // lookOpts.aoSamples (16) / lookOpts.aoDenoise ({ normalPhi, depthPhi, radius, rings, samples }): a cleaner contact shadow where two faces meet (a kerb, the foot
  // of a wall: at 16 samples the denoiser leaves a stippled fringe there), for the price of a slower AO pass
  ao.updateGtaoMaterial({ radius: 0.35, distanceExponent: 1.6, thickness: 1.0, scale: 1.0, samples: o.aoSamples ?? 16, distanceFallOff: 1.0, screenSpaceRadius: false });
  ao.updatePdMaterial({ lumaPhi: 10, depthPhi: 2, normalPhi: 3, radius: 10, rings: 3, samples: 16, ...(o.aoDenoise || {}) });
  composer.addPass(ao);
  const shafts = new ShaderPass(ShaftShader); shafts.uniforms.tDepth.value = ao.depthTexture; shafts.uniforms.aspect.value = W / H; composer.addPass(shafts);
  const bloom = new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), o.bloom ?? 0.28, 0.55, 0.92); composer.addPass(bloom);
  composer.addPass(new OutputPass());
  const grade = new ShaderPass(GradeShader); composer.addPass(grade);
  composer.setSize(W, H);
  // the sun disc + glow, far along the key light, only under an open sky
  const sun = new THREE.Sprite(new THREE.SpriteMaterial({ map: sunTexture(), transparent: true, depthWrite: false, fog: false, toneMapped: false, blending: THREE.AdditiveBlending }));
  sun.renderOrder = -9; sun.userData.noAO = true; scene.add(sun);
  const v = new THREE.Vector3(), dir = new THREE.Vector3(), ray = new THREE.Raycaster();
  // what stays visible when the lights are off (layer 1: the eyes of the face rig, a prop with `inDark`): drawn over the darkened picture, behind whatever
  // stands in front of it (a depth pass of the solid world first)
  const depthOnly = new THREE.MeshBasicMaterial({ colorWrite: false, side: THREE.DoubleSide }), hid = [];
  const inTheDark = () => {
    const mask = camera.layers.mask, au = renderer.shadowMap.autoUpdate, ac = renderer.autoClear, bg = scene.background;
    renderer.setRenderTarget(null); renderer.autoClear = false; renderer.shadowMap.autoUpdate = false; scene.background = null; renderer.clearDepth();
    // the solid world only: no ink hulls (an outline is the same shape a little bigger: drawn on both sides it would stand in front of its own mesh), nothing see-through
    scene.traverse(n => { if (n.visible === false) return; const m = n.material; if (n.name === 'outline' || n.isPoints || n.isLine || n.isSprite || isSky(n) || (m && !Array.isArray(m) && (m.transparent || m.alphaTest > 0))) { hid.push([n, n.visible]); n.visible = false; } });   // (three draws whatever is not exactly false: an `undefined` counts as visible)
    scene.overrideMaterial = depthOnly; renderer.render(scene, camera); scene.overrideMaterial = null; for (const [n, v] of hid) n.visible = v; hid.length = 0;
    camera.layers.set(1); renderer.render(scene, camera); camera.layers.mask = mask;
    scene.background = bg; renderer.autoClear = ac; renderer.shadowMap.autoUpdate = au;
  };
  const look = {
    outdoor: true, shaftsK: 1, probeDirty: false, dark: 0,
    // scene `dark` (engine/director3.js): k 0..1, floor: what is left of the picture (0.05: faint silhouettes; 0: black), tint: the colour of that rest
    setDark(k, floor = 0.05, tint = null) { look.dark = k; grade.uniforms.dark.value = k; grade.uniforms.darkFloor.value = floor; if (tint) { const c = new THREE.Color(tint); grade.uniforms.darkTint.value.set(c.r, c.g, c.b); } else grade.uniforms.darkTint.value.set(0.55, 0.72, 1.0); },
    // scene `darkPool`: a pool of light in a dark shot: k (0..1: how much of the picture comes back at its centre), at the screen point (u, v) (0..1, v up),
    // r (its radius, as a part of the frame height), tint, aspect (width / height of the frame)
    setPool(k = 0, u = 0.5, v = 0.5, r = 0.2, tint = null, aspect = 0.5625) { grade.uniforms.pool.value.set(u, v, r, k); grade.uniforms.aspect.value = aspect; if (tint) { const c = new THREE.Color(tint); grade.uniforms.poolTint.value.set(c.r, c.g, c.b); } else grade.uniforms.poolTint.value.set(1, 1, 1); },
    // per scene: retune the rig set by setLighting / atmosphere (called from setupScene)
    setupLights(L, set, sc = {}) {
      const indoor = (set.userData.lighting || 'day') === 'interior' || (set.userData.lighting === 'dark') || sc.indoor === true;
      look.outdoor = !indoor && sc.indoor !== true;
      const k = sc.look || {};
      L.hemi.intensity = (k.fill ?? 1) * L.hemi.intensity * (indoor ? 0.88 : 0.78); L.key.intensity = (k.sun ?? 1) * (indoor ? 2.4 : 3.0);
      L.hemi.color.set(indoor ? '#DCE6FF' : '#9DC0FF'); L.hemi.groundColor.set(indoor ? '#B89A78' : '#A88A62');
      L.key.color.set(k.sunColor || (indoor ? '#FFE6C4' : '#FFD8A6'));
      // a lower sun: long shadows (keep its azimuth)
      dir.copy(L.key.position).sub(L.key.target.position); const len = dir.length(); dir.normalize();
      const sd = k.sunDir || set.userData.sun; if (sd) { dir.set(...sd).normalize(); L.key.position.copy(L.key.target.position).addScaledVector(dir, len); }   // per set: the sun that lights the playing area
      const maxEl = (k.elevation ?? (indoor ? 50 : sd ? 80 : 38)) * Math.PI / 180, el = Math.asin(Math.min(1, dir.y));
      if (el > maxEl) { const hz = Math.hypot(dir.x, dir.z) || 1; dir.x *= Math.cos(maxEl) / hz; dir.z *= Math.cos(maxEl) / hz; dir.y = Math.sin(maxEl); L.key.position.copy(L.key.target.position).addScaledVector(dir, len); }
      L.key.shadow.radius = natural ? (k.softness ?? (indoor ? 9 : 6)) : 4; L.key.shadow.normalBias = 0.02; L.key.shadow.bias = Math.min(L.key.shadow.bias, -0.0004);
      if (o.draft && L.key.shadow.mapSize.x !== 1024) { L.key.shadow.mapSize.set(1024, 1024); if (L.key.shadow.map) { L.key.shadow.map.dispose(); L.key.shadow.map = null; } }   // lookOpts.draft: a quarter of the shadow texels and fewer blur samples (motion previews; never for a delivery)
      if (natural) { L.key.shadow.blurSamples = o.draft ? 6 : (o.shadowSamples ?? 16);   /* lookOpts.shadowSamples: more samples in the blur of the shadow map: the edge of a contact shadow (the foot of a wall, under a bench) is stippled at 16 */ L.hemi.intensity *= k.hemi ?? 0.45; L.key.intensity *= k.sunN ?? 0.95; look.probeK = k.probe ?? (indoor ? 1.7 : 1.2); look.probeTarget = k.probeTarget ?? o.probeTarget ?? 0.3; look.meterRef = k.meterRef ?? o.meterRef ?? (indoor ? 0.42 : 0.32); look.probeDirty = true; look.probeAt = k.probeAt || null; }
      ao.blendIntensity = k.ao ?? o.ao ?? 1.0; bloom.strength = k.bloom ?? o.bloom ?? 0.28; shafts.uniforms.intensity.value = k.shafts ?? 0.55;
      grade.uniforms.lift.value = k.lift ?? (natural ? 0.014 : 0.035); grade.uniforms.tint.value.set(...(k.tint || [1, 1, 1])); bloom.threshold = k.bloomThreshold ?? (natural ? 1.35 : 0.92);
      look.baseExposure = k.exposure ?? o.exposure ?? (natural ? (indoor ? 1.32 : 1.14) : (indoor ? 1.2 : 1.12)); look.autoExposure = natural && k.exposure == null && k.autoExposure !== false;
      grade.uniforms.sat.value = k.sat ?? (natural ? (indoor ? 1.1 : 1.16) : 1.12); grade.uniforms.contrast.value = k.contrast ?? (natural ? (indoor ? 0.98 : 1.04) : 1.05); grade.uniforms.warm.value = k.warm ?? (natural ? 0.85 : 1.0);
      renderer.toneMappingExposure = look.baseExposure;
      // distance haze outdoors, coloured like the horizon
      if (look.outdoor && !scene.fog && k.haze !== false) { const hz = new THREE.Color(k.hazeColor || '#CFE3F0'); scene.fog = new THREE.Fog(hz, k.hazeNear ?? 70, k.hazeFar ?? Math.max(260, camera.far * 1.1)); }
      set.traverse(n => { if (!isSky(n)) return; n.material.fog = false; n.material.toneMapped = false;   // the authored gradient, made a little deeper (shader skies)
        const ca = n.geometry.attributes.color; if (!ca || n.userData.deepSky || k.deepSky === false) return; n.userData.deepSky = true; const c = new THREE.Color(), hsl = {};
        for (let i = 0; i < ca.count; i++) { c.fromBufferAttribute(ca, i); c.getHSL(hsl); if (hsl.h > 0.42 && hsl.h < 0.72) { const top = Math.max(0, n.geometry.attributes.position.getY(i)) / (n.geometry.boundingSphere?.radius || 180); c.setHSL(0.575 + (hsl.h - 0.575) * 0.3, Math.min(0.82, hsl.s * 1.6 + 0.22 + 0.15 * top), Math.min(0.78, hsl.l * (0.97 - 0.12 * top))); ca.setXYZ(i, c.r, c.g, c.b); } } ca.needsUpdate = true; });
      sun.visible = look.outdoor && k.sunDisc !== false; sun.material.color.set(k.sunColor || '#FFF0D8');
      look.L = L;
    },
    render() {
      const L = look.L; let on = 0;
      if (L && look.outdoor) {
        dir.copy(L.key.position).sub(L.key.target.position).normalize();
        const d = Math.min(150, camera.far * 0.8); sun.position.copy(camera.position).addScaledVector(dir, d); sun.scale.setScalar(d * 0.22);
        v.copy(sun.position).project(camera);
        const inFront = v.z < 1, ux = v.x * 0.5 + 0.5, uy = v.y * 0.5 + 0.5;
        shafts.uniforms.sunPos.value.set(ux, uy);
        const out = Math.max(Math.max(-ux, ux - 1, 0), Math.max(-uy, uy - 1, 0));   // how far outside the frame (uv)
        on = inFront ? Math.max(0, 1 - out / 0.35) : 0;
      }
      shafts.uniforms.sunOn.value = on * look.shaftsK; shafts.enabled = on > 0.001;
      if (natural && look.probeDirty) {   // once per scene: capture the light around the action (the camera's look point, ~2.5 m ahead)
        look.probeDirty = false; if (probe) { scene.remove(probe); probe = null; }
        dir.set(0, 0, -1).applyQuaternion(camera.quaternion);
        let d = 2.5; ray.set(camera.position, dir); ray.far = 2.9; ray.camera = camera;   // in front of the first solid surface the camera looks at (not inside a wall, a fridge or a head)
        for (const h of ray.intersectObjects(scene.children, true)) { const n = h.object, m = n.material; if (!n.visible || n.isSprite || n.isPoints || n.isLine || isSky(n) || (m && !Array.isArray(m) && (m.transparent || m.alphaTest > 0))) continue; d = h.distance < 0.8 ? h.distance * 0.5 : Math.min(2.5, h.distance - 0.4); break; }
        const at = look.probeAt ? new THREE.Vector3(...look.probeAt) : camera.position.clone().addScaledVector(dir, d); at.y = Math.max(at.y, 0.6);
        const sv = sun.visible; sun.visible = false; cubeCam.position.copy(at); cubeCam.update(renderer, scene); sun.visible = sv;
        const P = probeFromCube(renderer, cubeRT); probe = P.probe;
        probe.intensity = look.probeK * Math.min(1, look.probeTarget / Math.max(1e-3, P.avg));   // a bright set (white kitchen, snow) bounces less, so it does not wash out
        probe.layers.enable(1); scene.add(probe);
        let M = null; if (look.autoExposure || o.debugProbe) M = meter();
        if (look.autoExposure) renderer.toneMappingExposure = look.baseExposure * Math.min(1.08, Math.max(0.7, Math.pow(look.meterRef / Math.max(1e-3, M.mean), 0.7)));   // a bright set is metered down, a dim one up a little
        if (o.debugProbe) console.warn(`[look] probe at ${at.toArray().map(x => x.toFixed(2))} d ${d.toFixed(2)} avg ${P.avg.toFixed(3)} bad ${P.bad} -> ${probe.intensity.toFixed(2)} | meter mean ${M.mean.toFixed(3)} p50 ${M.p50.toFixed(3)} p75 ${M.p75.toFixed(3)} exposure ${renderer.toneMappingExposure.toFixed(2)}`);
      }
      composer.render();
      if (look.dark > 0.02 || look.keepOverlay) inTheDark();   // keepOverlay: a shot with dark keys and props that stay lit draws them this way from its first frame, so that they do not change when the light goes
    },
  };
  return look;
}
