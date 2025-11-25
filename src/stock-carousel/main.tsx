import React from 'react';
import ReactDOM from 'react-dom/client';
import { StockCarousel } from './StockCarousel';
import type { StockData } from '../types';
import '../index.css';

// Get data from window or use sample data
const initialData: { stocks: StockData[] } = (window as any).__INITIAL_DATA__ || {
  stocks: [
    {
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
    },
    {
      symbol: 'TCS',
      name: 'Tata Consultancy Services Ltd',
      price: 3850.50,
      change: -25.75,
      changePercent: -0.66,
      open: 3876.25,
      high: 3890.00,
      low: 3842.10,
      volume: 2450000,
      marketCap: 14000000000000,
      pe: 32.8,
      timestamp: new Date().toISOString(),
    },
    {
      symbol: 'INFY',
      name: 'Infosys Ltd',
      price: 1625.30,
      change: 18.90,
      changePercent: 1.18,
      open: 1606.40,
      high: 1632.75,
      low: 1598.50,
      volume: 5230000,
      marketCap: 6800000000000,
      pe: 28.2,
      timestamp: new Date().toISOString(),
    },
  ],
};

const root = document.getElementById('root');
if (root) {
  ReactDOM.createRoot(root).render(
    <React.StrictMode>
      <StockCarousel data={initialData} />
    </React.StrictMode>
  );
}