import React from 'react';
import { TrendingUp, TrendingDown, BarChart3 } from 'lucide-react';
import type { IndexData } from '../types';
import { formatPercent } from '../utils/format';
import { useDisplayMode } from '../use-display-mode';

interface IndexWidgetProps {
  data: IndexData;
}

export function IndexWidget({ data }: IndexWidgetProps) {
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
          <h2 className="text-2xl font-bold">{data.name}</h2>
          <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            Market Index
          </p>
        </div>
        <BarChart3
          className={isDark ? 'text-purple-400' : 'text-purple-600'}
          size={24}
        />
      </div>

      {/* Value */}
      <div className="mb-6">
        <div className="text-4xl font-bold mb-2">{data.value.toFixed(2)}</div>
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
            ({data.change >= 0 ? '+' : ''}{data.change.toFixed(2)})
          </span>
        </div>
      </div>

      {/* Day Range */}
      <div className="mb-4">
        <p className={`text-sm mb-2 ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
          Day's Range
        </p>
        <div className="flex items-center gap-3">
          <div className="flex-1">
            <div
              className={`h-2 rounded-full ${
                isDark ? 'bg-gray-700' : 'bg-gray-200'
              } relative overflow-hidden`}
            >
              <div
                className={`h-full rounded-full ${
                  isPositive ? 'bg-green-500' : 'bg-red-500'
                }`}
                style={{
                  width: `${((data.value - data.low) / (data.high - data.low)) * 100}%`,
                }}
              />
            </div>
          </div>
        </div>
        <div className="flex justify-between text-sm mt-1">
          <span className="text-red-500 font-semibold">{data.low.toFixed(2)}</span>
          <span className="text-green-500 font-semibold">{data.high.toFixed(2)}</span>
        </div>
      </div>

      {/* Stats */}
      <div
        className={`grid grid-cols-2 gap-4 pt-4 border-t ${
          isDark ? 'border-gray-700' : 'border-gray-200'
        }`}
      >
        <div>
          <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            Day High
          </p>
          <p className="text-lg font-semibold text-green-500">
            {data.high.toFixed(2)}
          </p>
        </div>
        <div>
          <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            Day Low
          </p>
          <p className="text-lg font-semibold text-red-500">
            {data.low.toFixed(2)}
          </p>
        </div>
      </div>

      {/* Timestamp */}
      <div className="mt-4 text-xs text-center text-gray-500">
        Last updated: {new Date(data.timestamp).toLocaleString()}
      </div>
    </div>
  );
}