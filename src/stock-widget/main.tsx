import React from 'react';
import ReactDOM from 'react-dom/client';
import { StockWidget } from './StockWidget';
import type { StockData } from '../types';
import '../index.css';

// Get data from window or use sample data
const initialData: StockData = (window as any).__INITIAL_DATA__ || {
  symbol: 'RELIANCE',
  name: 'Reliance Industries Ltd',
  price: 2450.75,
  change: 45.30,
  changePercent: 1.88,
  open: 2405.45,
  high: 2465.80,
  low: 2398.20,
  volume: 8750000,
  marketCap: 16500000000000,
  pe: 28.5,
  timestamp: new Date().toISOString(),
};

const root = document.getElementById('root');
if (root) {
  ReactDOM.createRoot(root).render(
    <React.StrictMode>
      <StockWidget data={initialData} />
    </React.StrictMode>
  );
}