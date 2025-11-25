"""Stock data fetching and processing."""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False


# NSE India stock suffix
NSE_SUFFIX = ".NS"

# Indian market indices
INDICES_MAP = {
    "NIFTY50": "^NSEI",
    "NIFTYMIDCAP150": "^NSEMDCP50",
    "NIFTYSMLCAP250": "NIFTY_SMLCAP_250.NS",
    "BANKNIFTY": "^NSEBANK",
}


def format_currency(value: float) -> str:
    """Format value as Indian currency."""
    if value >= 10000000:  # 1 crore
        return f"₹{value/10000000:.2f}Cr"
    elif value >= 100000:  # 1 lakh
        return f"₹{value/100000:.2f}L"
    else:
        return f"₹{value:.2f}"


def get_stock_data(symbol: str) -> Dict[str, Any]:
    """Get stock data for a given symbol."""
    
    # Add NSE suffix if not present
    if not symbol.endswith(NSE_SUFFIX) and symbol not in INDICES_MAP:
        symbol_with_suffix = f"{symbol.upper()}{NSE_SUFFIX}"
    else:
        symbol_with_suffix = symbol.upper()
    
    if not YFINANCE_AVAILABLE:
        # Return mock data for development
        return _get_mock_stock_data(symbol)
    
    try:
        ticker = yf.Ticker(symbol_with_suffix)
        info = ticker.info
        hist = ticker.history(period="1d")
        
        if hist.empty:
            return _get_mock_stock_data(symbol)
        
        current_price = hist['Close'].iloc[-1]
        open_price = hist['Open'].iloc[-1]
        high = hist['High'].iloc[-1]
        low = hist['Low'].iloc[-1]
        volume = hist['Volume'].iloc[-1]
        
        # Calculate change
        change = current_price - open_price
        change_percent = (change / open_price) * 100 if open_price else 0
        
        return {
            "symbol": symbol.upper(),
            "name": info.get("longName", symbol.upper()),
            "price": round(current_price, 2),
            "change": round(change, 2),
            "changePercent": round(change_percent, 2),
            "open": round(open_price, 2),
            "high": round(high, 2),
            "low": round(low, 2),
            "volume": int(volume),
            "marketCap": info.get("marketCap"),
            "pe": info.get("trailingPE"),
            "timestamp": datetime.now().isoformat(),
        }
    
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return _get_mock_stock_data(symbol)


def get_multiple_stocks_data(symbols: List[str]) -> List[Dict[str, Any]]:
    """Get data for multiple stocks."""
    return [get_stock_data(symbol) for symbol in symbols]


def get_index_data(index_name: str) -> Dict[str, Any]:
    """Get market index data."""
    
    index_symbol = INDICES_MAP.get(index_name.upper())
    if not index_symbol:
        raise ValueError(f"Unknown index: {index_name}")
    
    if not YFINANCE_AVAILABLE:
        return _get_mock_index_data(index_name)
    
    try:
        ticker = yf.Ticker(index_symbol)
        hist = ticker.history(period="1d")
        
        if hist.empty:
            return _get_mock_index_data(index_name)
        
        current_price = hist['Close'].iloc[-1]
        open_price = hist['Open'].iloc[-1]
        high = hist['High'].iloc[-1]
        low = hist['Low'].iloc[-1]
        
        change = current_price - open_price
        change_percent = (change / open_price) * 100 if open_price else 0
        
        return {
            "name": index_name,
            "value": round(current_price, 2),
            "change": round(change, 2),
            "changePercent": round(change_percent, 2),
            "high": round(high, 2),
            "low": round(low, 2),
            "timestamp": datetime.now().isoformat(),
        }
    
    except Exception as e:
        print(f"Error fetching index data for {index_name}: {e}")
        return _get_mock_index_data(index_name)


def search_stocks(query: str) -> List[Dict[str, str]]:
    """Search for stocks by name or symbol."""
    
    # Popular Indian stocks database (simplified)
    popular_stocks = [
        {"symbol": "RELIANCE", "name": "Reliance Industries Ltd"},
        {"symbol": "TCS", "name": "Tata Consultancy Services Ltd"},
        {"symbol": "INFY", "name": "Infosys Ltd"},
        {"symbol": "HDFCBANK", "name": "HDFC Bank Ltd"},
        {"symbol": "ICICIBANK", "name": "ICICI Bank Ltd"},
        {"symbol": "HINDUNILVR", "name": "Hindustan Unilever Ltd"},
        {"symbol": "ITC", "name": "ITC Ltd"},
        {"symbol": "SBIN", "name": "State Bank of India"},
        {"symbol": "BHARTIARTL", "name": "Bharti Airtel Ltd"},
        {"symbol": "WIPRO", "name": "Wipro Ltd"},
        {"symbol": "LT", "name": "Larsen & Toubro Ltd"},
        {"symbol": "AXISBANK", "name": "Axis Bank Ltd"},
        {"symbol": "MARUTI", "name": "Maruti Suzuki India Ltd"},
        {"symbol": "SUNPHARMA", "name": "Sun Pharmaceutical Industries Ltd"},
        {"symbol": "TITAN", "name": "Titan Company Ltd"},
    ]
    
    query_lower = query.lower()
    results = [
        stock for stock in popular_stocks
        if query_lower in stock["symbol"].lower() or query_lower in stock["name"].lower()
    ]
    
    return results[:10]  # Return top 10 results


def _get_mock_stock_data(symbol: str) -> Dict[str, Any]:
    """Get mock stock data for development/testing."""
    import random
    
    base_price = random.uniform(100, 5000)
    change = random.uniform(-100, 100)
    change_percent = (change / base_price) * 100
    
    return {
        "symbol": symbol.upper(),
        "name": f"{symbol.upper()} Ltd",
        "price": round(base_price, 2),
        "change": round(change, 2),
        "changePercent": round(change_percent, 2),
        "open": round(base_price - change, 2),
        "high": round(base_price + abs(change) * 0.5, 2),
        "low": round(base_price - abs(change) * 0.5, 2),
        "volume": random.randint(1000000, 50000000),
        "marketCap": random.randint(10000000000, 1000000000000),
        "pe": round(random.uniform(10, 50), 2),
        "timestamp": datetime.now().isoformat(),
    }


def _get_mock_index_data(index_name: str) -> Dict[str, Any]:
    """Get mock index data for development/testing."""
    import random
    
    base_values = {
        "NIFTY50": 22000,
        "NIFTYMIDCAP150": 45000,
        "NIFTYSMLCAP250": 12000,
        "BANKNIFTY": 48000,
    }
    
    base_value = base_values.get(index_name.upper(), 20000)
    change = random.uniform(-500, 500)
    change_percent = (change / base_value) * 100
    
    return {
        "name": index_name,
        "value": round(base_value, 2),
        "change": round(change, 2),
        "changePercent": round(change_percent, 2),
        "high": round(base_value + abs(change) * 0.5, 2),
        "low": round(base_value - abs(change) * 0.5, 2),
        "timestamp": datetime.now().isoformat(),
    }