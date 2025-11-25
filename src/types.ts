/**
 * Common types for stock widgets
 */

export interface StockData {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  open: number;
  high: number;
  low: number;
  volume: number;
  marketCap?: number;
  pe?: number;
  timestamp: string;
}

export interface IndexData {
  name: string;
  value: number;
  change: number;
  changePercent: number;
  high: number;
  low: number;
  timestamp: string;
}

export interface WidgetProps<T = any> {
  data: T;
  displayMode?: 'light' | 'dark';
}

export type DisplayMode = 'light' | 'dark';

export interface OpenAIGlobal {
  displayMode: DisplayMode;
}