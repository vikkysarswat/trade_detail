import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, TrendingUp, TrendingDown } from 'lucide-react';
import type { StockData } from '../types';
import { formatPercent, formatVolume } from '../utils/format';
import { useDisplayMode } from '../use-display-mode';

interface StockCarouselProps {
  data: { stocks: StockData[] };
}

export function StockCarousel({ data }: StockCarouselProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const displayMode = useDisplayMode();
  const isDark = displayMode === 'dark';
  const stocks = data.stocks || [];

  if (stocks.length === 0) {
    return (
      <div className="text-center p-8 text-gray-500">
        No stock data available
      </div>
    );
  }

  const currentStock = stocks[currentIndex];
  const isPositive = currentStock.change >= 0;

  const handlePrevious = () => {
    setCurrentIndex((prev) => (prev === 0 ? stocks.length - 1 : prev - 1));
  };

  const handleNext = () => {
    setCurrentIndex((prev) => (prev === stocks.length - 1 ? 0 : prev + 1));
  };

  return (
    <div
      className={`w-full max-w-2xl rounded-xl shadow-lg p-6 ${
        isDark ? 'bg-gray-800 text-white' : 'bg-white text-gray-900'
      }`}
    >
      {/* Carousel Navigation */}
      <div className="flex items-center justify-between mb-6">
        <button
          onClick={handlePrevious}
          className={`p-2 rounded-full transition-colors ${
            isDark
              ? 'hover:bg-gray-700 text-gray-300'
              : 'hover:bg-gray-100 text-gray-600'
          }`}
          aria-label="Previous stock"
        >
          <ChevronLeft size={24} />
        </button>

        <div className="text-center flex-1">
          <h2 className="text-3xl font-bold">{currentStock.symbol}</h2>
          <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            {currentStock.name}
          </p>
        </div>

        <button
          onClick={handleNext}
          className={`p-2 rounded-full transition-colors ${
            isDark
              ? 'hover:bg-gray-700 text-gray-300'
              : 'hover:bg-gray-100 text-gray-600'
          }`}
          aria-label="Next stock"
        >
          <ChevronRight size={24} />
        </button>
      </div>

      {/* Price Display */}
      <div className="text-center mb-6">
        <div className="text-5xl font-bold mb-3">
          ₹{currentStock.price.toFixed(2)}
        </div>
        <div className="flex items-center justify-center gap-2">
          {isPositive ? (
            <TrendingUp className="text-green-500" size={24} />
          ) : (
            <TrendingDown className="text-red-500" size={24} />
          )}
          <span
            className={`text-2xl font-semibold ${
              isPositive ? 'text-green-500' : 'text-red-500'
            }`}
          >
            {formatPercent(currentStock.changePercent)}
          </span>
          <span
            className={`text-lg ${
              isPositive ? 'text-green-500' : 'text-red-500'
            }`}
          >
            ({currentStock.change >= 0 ? '+' : ''}₹{currentStock.change.toFixed(2)})
          </span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="text-center">
          <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            Open
          </p>
          <p className="text-xl font-semibold">₹{currentStock.open.toFixed(2)}</p>
        </div>
        <div className="text-center">
          <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            High
          </p>
          <p className="text-xl font-semibold text-green-500">
            ₹{currentStock.high.toFixed(2)}
          </p>
        </div>
        <div className="text-center">
          <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            Low
          </p>
          <p className="text-xl font-semibold text-red-500">
            ₹{currentStock.low.toFixed(2)}
          </p>
        </div>
        <div className="text-center">
          <p className={`text-sm ${isDark ? 'text-gray-400' : 'text-gray-600'}`}>
            Volume
          </p>
          <p className="text-xl font-semibold">
            {formatVolume(currentStock.volume)}
          </p>
        </div>
      </div>

      {/* Pagination Dots */}
      <div className="flex justify-center gap-2 mb-4">
        {stocks.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentIndex(index)}
            className={`w-2 h-2 rounded-full transition-all ${
              index === currentIndex
                ? isDark
                  ? 'bg-blue-400 w-8'
                  : 'bg-blue-600 w-8'
                : isDark
                ? 'bg-gray-600'
                : 'bg-gray-300'
            }`}
            aria-label={`Go to stock ${index + 1}`}
          />
        ))}
      </div>

      {/* Counter */}
      <div className="text-center text-sm text-gray-500">
        {currentIndex + 1} of {stocks.length} stocks
      </div>
    </div>
  );
}