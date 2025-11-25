#!/usr/bin/env tsx
import { createServer } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

async function devAll() {
  console.log('🚀 Starting development server...');

  const server = await createServer({
    plugins: [react()],
    root: resolve(process.cwd(), 'src'),
    server: {
      port: 5173,
      open: true,
    },
  });

  await server.listen();
  server.printUrls();
}

devAll().catch((error) => {
  console.error('Dev server failed:', error);
  process.exit(1);
});