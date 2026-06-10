#!/usr/bin/env node
/**
 * Copies the RDKit.js MinimalLib assets (RDKit_minimal.js + RDKit_minimal.wasm)
 * from node_modules into the demo's public directory so the browser can load
 * them from /rdkit/. Library consumers do the same into their own public dir.
 */
import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const srcDir = join(here, '..', 'node_modules', '@rdkit', 'rdkit', 'dist');
const destDir = join(here, '..', 'example', 'public', 'rdkit');

const assets = ['RDKit_minimal.js', 'RDKit_minimal.wasm'];

if (!existsSync(srcDir)) {
  console.error(
    `[copy-rdkit] @rdkit/rdkit not found at ${srcDir}. Run "npm install" first.`,
  );
  process.exit(1);
}

mkdirSync(destDir, { recursive: true });
for (const asset of assets) {
  const from = join(srcDir, asset);
  if (!existsSync(from)) {
    console.error(`[copy-rdkit] Missing asset: ${from}`);
    process.exit(1);
  }
  copyFileSync(from, join(destDir, asset));
}
console.log(`[copy-rdkit] Copied ${assets.join(', ')} -> ${destDir}`);
