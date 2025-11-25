import React from 'react';
import ReactDOM from 'react-dom/client';
import { IndexWidget } from './IndexWidget';
import type { IndexData } from '../types';
import '../index.css';

// Get data from window or use sample data
const initialData: IndexData = (window as any).__INITIAL_DATA__ || {
  name: 'NIFTY 50',
  value: 22150.50,
  change: 125.30,
  changePercent: 0.57,
  high: 22180.75,
  low: 22020.40,
  timestamp: new Date().toISOString(),
};

const root = document.getElementById('root');
if (root) {
  ReactDOM.createRoot(root).render(
    <React.StrictMode>
      <IndexWidget data={initialData} />
    </React.StrictMode>
  );
}