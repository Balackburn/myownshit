import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

// Demo app build: serves example/ with the library aliased to its source.
// DEMO_BASE lets CI build for a sub-path host (e.g. GitHub Pages /repo-name/).
export default defineConfig({
  root: 'example',
  publicDir: 'public',
  base: process.env.DEMO_BASE ?? '/',
  plugins: [react(), tailwindcss()],
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
    rollupOptions: {
      input: {
        main: fileURLToPath(new URL('./example/index.html', import.meta.url)),
        embed: fileURLToPath(new URL('./example/embed.html', import.meta.url)),
      },
    },
  },
});
