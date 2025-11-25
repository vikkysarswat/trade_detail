import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';
import { readdirSync, statSync } from 'fs';

const srcDir = resolve(__dirname, 'src');
const entries: Record<string, string> = {};

// Automatically discover all widget entry points
const dirs = readdirSync(srcDir).filter((file) => {
  const fullPath = resolve(srcDir, file);
  return statSync(fullPath).isDirectory();
});

for (const dir of dirs) {
  const mainFile = resolve(srcDir, dir, 'main.tsx');
  try {
    statSync(mainFile);
    entries[dir] = mainFile;
  } catch {
    // No main.tsx in this directory
  }
}

export default defineConfig({
  plugins: [react()],
  build: {
    lib: {
      entry: entries,
      formats: ['es'],
      fileName: (format, entryName) => `${entryName}.js`,
    },
    rollupOptions: {
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
        },
      },
    },
    outDir: 'assets',
    emptyOutDir: true,
    cssCodeSplit: false,
  },
});