/**
 * Utility functions for formatting data
 */

export function formatCurrency(value: number): string {
  if (value >= 10000000) {
    // 1 crore
    return `₹${(value / 10000000).toFixed(2)}Cr`;
  } else if (value >= 100000) {
    // 1 lakh
    return `₹${(value / 100000).toFixed(2)}L`;
  } else {
    return `₹${value.toFixed(2)}`;
  }
}

export function formatVolume(volume: number): string {
  if (volume >= 10000000) {
    return `${(volume / 10000000).toFixed(2)}Cr`;
  } else if (volume >= 100000) {
    return `${(volume / 100000).toFixed(2)}L`;
  } else {
    return volume.toLocaleString();
  }
}

export function formatPercent(value: number): string {
  const sign = value >= 0 ? '+' : '';
  return `${sign}${value.toFixed(2)}%`;
}

export function formatNumber(value: number, decimals: number = 2): string {
  return value.toFixed(decimals);
}