"""FastAPI MCP server for stock and index data."""

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from server.stock_data import (
    get_stock_data,
    get_multiple_stocks_data,
    get_index_data,
    search_stocks,
)

# Get base URL for widget assets
BASE_URL = os.getenv("BASE_URL", "http://localhost:4444")
ASSETS_PATH = Path(__file__).parent.parent / "assets"

app = FastAPI(
    title="Trade Detail MCP Server",
    description="Stock and Index Price Display for ChatGPT",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MCPRequest(BaseModel):
    """MCP request model."""
    method: str
    params: Optional[Dict[str, Any]] = None


class MCPResponse(BaseModel):
    """MCP response model."""
    result: Any
    _meta: Optional[Dict[str, Any]] = None


@lru_cache(maxsize=10)
def load_widget_html(widget_name: str) -> str:
    """Load widget HTML from assets directory."""
    html_path = ASSETS_PATH / f"{widget_name}.html"
    if html_path.exists():
        return html_path.read_text()
    
    # Fallback to generating basic HTML
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
        <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
        <script src="{BASE_URL}/{widget_name}.js" type="module"></script>
        <link rel="stylesheet" href="{BASE_URL}/{widget_name}.css">
    </head>
    <body>
        <div id="root"></div>
    </body>
    </html>
    """


def create_widget_response(
    data: Dict[str, Any],
    widget_name: str,
    description: str = "",
) -> MCPResponse:
    """Create MCP response with embedded widget."""
    html = load_widget_html(widget_name)
    
    # Inject data into HTML
    html_with_data = html.replace(
        '<div id="root"></div>',
        f'<div id="root"></div><script>window.__INITIAL_DATA__={data}</script>'
    )
    
    return MCPResponse(
        result=data,
        _meta={
            "openai/outputTemplate": {
                "type": "html",
                "html": html_with_data,
            },
            "openai/description": description,
        },
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Trade Detail MCP Server",
        "version": "1.0.0",
        "description": "Stock and Index Price Display for ChatGPT",
        "mcp_endpoint": "/mcp",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/mcp")
async def mcp_get():
    """MCP GET endpoint - list available tools."""
    return {
        "tools": [
            {
                "name": "get_stock_price",
                "description": "Get current price and details for a stock symbol. Returns a widget with stock information.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Stock symbol (e.g., RELIANCE, TCS, INFY)",
                        },
                    },
                    "required": ["symbol"],
                },
            },
            {
                "name": "get_multiple_stocks",
                "description": "Display multiple stocks in a carousel format. Great for comparing stocks.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbols": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of stock symbols",
                        },
                    },
                    "required": ["symbols"],
                },
            },
            {
                "name": "get_index_data",
                "description": "Get market index information (Nifty 50, Nifty Midcap, Nifty Smallcap).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "index_name": {
                            "type": "string",
                            "description": "Index name (NIFTY50, NIFTYMIDCAP150, NIFTYSMLCAP250)",
                        },
                    },
                    "required": ["index_name"],
                },
            },
            {
                "name": "search_stocks",
                "description": "Search for stocks by name or symbol.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query",
                        },
                    },
                    "required": ["query"],
                },
            },
        ]
    }


@app.post("/mcp")
async def mcp_post(request: MCPRequest):
    """MCP POST endpoint - execute tool calls."""
    try:
        method = request.method
        params = request.params or {}

        if method == "get_stock_price":
            symbol = params.get("symbol")
            if not symbol:
                raise HTTPException(status_code=400, detail="Symbol is required")
            
            stock_data = get_stock_data(symbol)
            return create_widget_response(
                stock_data,
                "stock-widget",
                f"Current price and details for {symbol}",
            )

        elif method == "get_multiple_stocks":
            symbols = params.get("symbols")
            if not symbols or not isinstance(symbols, list):
                raise HTTPException(status_code=400, detail="Symbols array is required")
            
            stocks_data = get_multiple_stocks_data(symbols)
            return create_widget_response(
                {"stocks": stocks_data},
                "stock-carousel",
                f"Displaying {len(symbols)} stocks in carousel",
            )

        elif method == "get_index_data":
            index_name = params.get("index_name")
            if not index_name:
                raise HTTPException(status_code=400, detail="Index name is required")
            
            index_data = get_index_data(index_name)
            return create_widget_response(
                index_data,
                "index-widget",
                f"Market index data for {index_name}",
            )

        elif method == "search_stocks":
            query = params.get("query")
            if not query:
                raise HTTPException(status_code=400, detail="Query is required")
            
            results = search_stocks(query)
            return MCPResponse(
                result={"results": results},
                _meta={
                    "openai/description": f"Found {len(results)} stocks matching '{query}'",
                },
            )

        else:
            raise HTTPException(status_code=400, detail=f"Unknown method: {method}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)