import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  root: resolve(__dirname, 'assets'),
  server: {
    cors: true,
    port: 4444,
  },
});