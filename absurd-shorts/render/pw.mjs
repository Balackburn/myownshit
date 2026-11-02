// Resolve Playwright whether it is a local dependency or a globally installed one.
import { createRequire } from 'node:module';
let pw;
try { pw = await import('playwright'); } catch { pw = createRequire(import.meta.url)('playwright'); }
export const chromium = pw.chromium || pw.default?.chromium;
export const LAUNCH_ARGS = ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'];
