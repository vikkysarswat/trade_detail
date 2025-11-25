#!/usr/bin/env tsx
import { build } from 'vite';
import { resolve } from 'path';
import { readdirSync, statSync, writeFileSync } from 'fs';
import { createHash } from 'crypto';

const srcDir = resolve(process.cwd(), 'src');
const assetsDir = resolve(process.cwd(), 'assets');

interface BuildResult {
  name: string;
  jsFile: string;
  cssFile?: string;
  htmlFile: string;
}

async function buildAll() {
  console.log('🏗️  Building all widgets...');

  // Get all widget directories
  const dirs = readdirSync(srcDir).filter((file) => {
    const fullPath = resolve(srcDir, file);
    if (!statSync(fullPath).isDirectory()) return false;

    // Check if main.tsx exists
    try {
      statSync(resolve(fullPath, 'main.tsx'));
      return true;
    } catch {
      return false;
    }
  });

  console.log(`Found ${dirs.length} widgets: ${dirs.join(', ')}`);

  // Build all widgets
  await build();

  console.log('✅ Build complete!');
  console.log('📦 Widget bundles are in the assets/ directory');
}

buildAll().catch((error) => {
  console.error('Build failed:', error);
  process.exit(1);
});