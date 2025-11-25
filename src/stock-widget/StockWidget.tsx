import React from 'react';
import { TrendingUp, TrendingDown, Activity } from 'lucide-react';
import type { StockData } from '../types';
import { formatCurrency, formatPercent, formatVolume } from '../utils/format';
import { useDisplayMode } from '../use-display-mode';

interface StockWidgetProps {
  data: StockData;
}

export function StockWidget({ data }: StockWidgetProps) {
  const displayMode = useDisplayMode();
  const isPositive = data.change >= 0;
  const isDark = displayMode === 'dark';

  return (
    <div
      className={`w-full max-w-md rounded-xl shadow-lg p-6 ${
        isDark ? 'bg-gray-800 text-white' : 'bg-white text-gray-900'
      }`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <h2 className="text-2xl font-bold">{data.symbol}</h2>
          <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            {data.name}
          </p>
        </div>
        <Activity className={isDark ? 'text-blue-400' : 'text-blue-600'} size={24} />
      </div>

      {/* Price */}
      <div className="mb-6">
        <div className="text-4xl font-bold mb-2">
          ₹{data.price.toFixed(2)}
        </div>
        <div className="flex items-center gap-2">
          {isPositive ? (
            <TrendingUp className="text-green-500" size={20} />
          ) : (
            <TrendingDown className="text-red-500" size={20} />
          )}
          <span
            className={`text-lg font-semibold ${
              isPositive ? 'text-green-500' : 'text-red-500'
            }`}
          >
            {formatPercent(data.changePercent)}
          </span>
          <span
            className={`text-sm ${
              isPositive ? 'text-green-500' : 'text-red-500'
            }`}
          >
            ({data.change >= 0 ? '+' : ''}₹{data.change.toFixed(2)})
          </span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            Open
          </p>
          <p className="text-lg font-semibold">₹{data.open.toFixed(2)}</p>
        </div>
        <div>
          <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            Volume
          </p>
          <p className="text-lg font-semibold">{formatVolume(data.volume)}</p>
        </div>
        <div>
          <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            High
          </p>
          <p className="text-lg font-semibold text-green-500">
            ₹{data.high.toFixed(2)}
          </p>
        </div>
        <div>
          <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            Low
          </p>
          <p className="text-lg font-semibold text-red-500">
            ₹{data.low.toFixed(2)}
          </p>
        </div>
      </div>

      {/* Additional Info */}
      {(data.marketCap || data.pe) && (
        <div
          className={`pt-4 border-t ${
            isDark ? 'border-gray-700' : 'border-gray-200'
          }`}
        >
          <div className="flex justify-between text-sm">
            {data.marketCap && (
              <div>
                <p className={isDark ? 'text-gray-400' : 'text-gray-600'}>
                  Market Cap
                </p>
                <p className="font-semibold">{formatCurrency(data.marketCap)}</p>
              </div>
            )}
            {data.pe && (
              <div>
                <p className={isDark ? 'text-gray-400' : 'text-gray-600'}>P/E</p>
                <p className="font-semibold">{data.pe.toFixed(2)}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Timestamp */}
      <div className="mt-4 text-xs text-center text-gray-500">
        Last updated: {new Date(data.timestamp).toLocaleString()}
      </div>
    </div>
  );
}