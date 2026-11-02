// Renderer + lighting rig shared by film, gallery and exporter.
import * as THREE from 'three';
import { PALETTE as P } from './style.js';

export function createStage(w, h, { pixelRatio = 1 } = {}) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(pixelRatio); renderer.setSize(w, h);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  document.body.appendChild(renderer.domElement);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(40, w / h, 0.05, 400);
  const lights = setLighting(scene, 'day');
  return { renderer, scene, camera, lights };
}

// Soft, low-contrast lighting: strong hemisphere fill + one warm key with soft shadows.
export const LIGHTING = {
  day:      { sky: '#FFF8EC', ground: '#B9C8C0', hemi: 1.9, key: '#FFF1DC', keyI: 1.5, dir: [4, 9, 6], bg: P.sky, fog: null },
  interior: { sky: '#FFF6E6', ground: '#C9BFA8', hemi: 2.0, key: '#FFF0D8', keyI: 1.2, dir: [3, 8, 5], bg: P.cream, fog: null },
  night:    { sky: '#7C8FB5', ground: '#2A2F3A', hemi: 1.05, key: '#C9D6FF', keyI: 0.6, dir: [-4, 8, 3], bg: P.skyNight, fog: null },
  dusk:     { sky: '#F6C9A0', ground: '#6C6A7A', hemi: 1.4, key: '#FFC48A', keyI: 1.0, dir: [-6, 4, 4], bg: '#E7B08E', fog: null },
  savannah: { sky: '#FFF4DE', ground: '#C9A86A', hemi: 1.9, key: '#FFE8C4', keyI: 1.6, dir: [5, 9, 4], bg: P.sky, fog: null },
  dark:     { sky: '#4A5A70', ground: '#1A1D24', hemi: 0.8, key: '#E8E0C8', keyI: 0.9, dir: [1, 6, 3], bg: '#121621', fog: null },
};
export function setLighting(scene, name = 'day') {
  const L = LIGHTING[name] || LIGHTING.day;
  scene.children.filter(c => c.userData.isLight).forEach(c => scene.remove(c));
  const hemi = new THREE.HemisphereLight(L.sky, L.ground, L.hemi); hemi.userData.isLight = true; scene.add(hemi);
  const key = new THREE.DirectionalLight(L.key, L.keyI); key.position.set(...L.dir); key.userData.isLight = true;
  key.castShadow = true; key.shadow.mapSize.set(2048, 2048); key.shadow.radius = 6; key.shadow.bias = -0.0005;
  const sc = key.shadow.camera; sc.left = -14; sc.right = 14; sc.top = 14; sc.bottom = -14; sc.near = 0.5; sc.far = 60;
  scene.add(key); scene.add(key.target); key.target.userData.isLight = true;
  scene.background = new THREE.Color(L.bg);
  return { hemi, key };
}
