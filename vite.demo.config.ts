import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Demo app build: serves example/ with the library aliased to its source.
export default defineConfig({
  root: 'example',
  publicDir: 'public',
  plugins: [react()],
  resolve: {
    alias: {
      'react-molstruct/styles.css': fileURLToPath(
        new URL('./src/styles.css', import.meta.url),
      ),
      'react-molstruct': fileURLToPath(new URL('./src/index.ts', import.meta.url)),
    },
  },
  build: {
    outDir: '../dist-demo',
    emptyOutDir: true,
  },
});
