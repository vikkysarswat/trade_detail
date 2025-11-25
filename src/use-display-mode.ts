import { useEffect, useState } from 'react';
import type { DisplayMode } from './types';

export function useDisplayMode(): DisplayMode {
  const [mode, setMode] = useState<DisplayMode>('light');

  useEffect(() => {
    const openai = (window as any).openai;
    if (openai?.displayMode) {
      setMode(openai.displayMode);
    }
  }, []);

  return mode;
}