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
  uniforms: { tDiffuse: { value: null }, sat: { value: 1.12 }, contrast: { value: 1.05 }, vignette: { value: 0.18 }, warm: { value: 1.0 } },
  vertexShader: vertex,
  fragmentShader: `
    uniform sampler2D tDiffuse; uniform float sat, contrast, vignette, warm; varying vec2 vUv;
    void main() {
      vec3 c = texture2D(tDiffuse, vUv).rgb; float l = dot(c, vec3(0.299, 0.587, 0.114));
      c = c * 0.95 + 0.035;   // lift the shade: navy suits and black robes keep their detail
      c = mix(vec3(l), c, sat); c = (c - 0.5) * contrast + 0.5;
      vec3 shadowTint = vec3(0.94, 0.99, 1.06), hiTint = vec3(1.045, 1.0, 0.94);
      c *= mix(vec3(1.0), mix(shadowTint, hiTint, smoothstep(0.12, 0.85, l)), warm);
      float v = smoothstep(1.05, 0.38, length((vUv - 0.5) * vec2(1.0, 1.15))); c *= mix(1.0 - vignette, 1.0, v);
      gl_FragColor = vec4(clamp(c, 0.0, 1.0), 1.0);
    }`,
};

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
  renderer.toneMapping = THREE.NeutralToneMapping; renderer.toneMappingExposure = o.exposure ?? 1.0;   // Khronos neutral: keeps the paper hues, rolls off the brighter sun
  const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
  const composer = new EffectComposer(renderer, rt); composer.setPixelRatio(1);
  composer.addPass(new RenderPass(scene, camera));
  const ao = new GTAOPass(scene, camera, W, H);
    ao.overrideVisibility = function () {   // nothing see-through in the G-buffer: sky dome (leaves depth = far for the shafts), sprites, particles, glass, cut-outs
    const cache = this._visibilityCache; scene.traverse(n => { cache.set(n, n.visible); const m = n.material;
      if (n.isPoints || n.isLine || n.isSprite || isSky(n) || (m && !Array.isArray(m) && (m.transparent || m.alphaTest > 0)) || n.userData.noAO) n.visible = false; });
  };
  ao.blendIntensity = o.ao ?? 1.0;
  ao.updateGtaoMaterial({ radius: 0.35, distanceExponent: 1.6, thickness: 1.0, scale: 1.0, samples: 16, distanceFallOff: 1.0, screenSpaceRadius: false });
  ao.updatePdMaterial({ lumaPhi: 10, depthPhi: 2, normalPhi: 3, radius: 10, rings: 3, samples: 16 });
  composer.addPass(ao);
  const shafts = new ShaderPass(ShaftShader); shafts.uniforms.tDepth.value = ao.depthTexture; shafts.uniforms.aspect.value = W / H; composer.addPass(shafts);
  const bloom = new UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), o.bloom ?? 0.28, 0.55, 0.92); composer.addPass(bloom);
  composer.addPass(new OutputPass());
  const grade = new ShaderPass(GradeShader); composer.addPass(grade);
  composer.setSize(W, H);
  // the sun disc + glow, far along the key light, only under an open sky
  const sun = new THREE.Sprite(new THREE.SpriteMaterial({ map: sunTexture(), transparent: true, depthWrite: false, fog: false, toneMapped: false, blending: THREE.AdditiveBlending }));
  sun.renderOrder = -9; sun.userData.noAO = true; scene.add(sun);
  const v = new THREE.Vector3(), dir = new THREE.Vector3();
  const look = {
    outdoor: true, shaftsK: 1,
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
      L.key.shadow.radius = 4; L.key.shadow.normalBias = 0.02; L.key.shadow.bias = Math.min(L.key.shadow.bias, -0.0004);
      ao.blendIntensity = k.ao ?? o.ao ?? 1.0; bloom.strength = k.bloom ?? o.bloom ?? 0.28; shafts.uniforms.intensity.value = k.shafts ?? 0.55;
      grade.uniforms.sat.value = k.sat ?? 1.12; grade.uniforms.contrast.value = k.contrast ?? 1.05; grade.uniforms.warm.value = k.warm ?? 1.0;
      renderer.toneMappingExposure = k.exposure ?? o.exposure ?? (indoor ? 1.2 : 1.12);
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
      composer.render();
    },
  };
  return look;
}
