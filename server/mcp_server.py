"""MCP Server for Trade Detail - Stock Price Display."""

import json
import os
from typing import Any, Dict, List

from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from pydantic import AnyUrl

from server.stock_data import (
    get_stock_data,
    get_multiple_stocks_data,
    get_index_data,
    search_stocks,
)

# Get base URL for widget assets
BASE_URL = os.getenv("BASE_URL", "http://localhost:4444")

# Create MCP server
mcp_server = Server("trade-detail")


def create_widget_html(widget_name: str, data: Dict[str, Any]) -> str:
    """Generate HTML for widget with embedded data."""
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <link rel="stylesheet" href="{BASE_URL}/{widget_name}.css">
</head>
<body>
    <div id="root"></div>
    <script>window.__INITIAL_DATA__ = {json.dumps(data)};</script>
    <script src="{BASE_URL}/{widget_name}.js" type="module"></script>
</body>
</html>"""


@mcp_server.list_tools()
async def list_tools() -> List[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="get_stock_price",
            description="Get current price and details for a stock symbol. Returns a widget with stock information.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., RELIANCE, TCS, INFY)",
                    }
                },
                "required": ["symbol"],
            },
        ),
        Tool(
            name="get_multiple_stocks",
            description="Display multiple stocks in a carousel format. Great for comparing stocks.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbols": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of stock symbols",
                    }
                },
                "required": ["symbols"],
            },
        ),
        Tool(
            name="get_index_data",
            description="Get market index information (Nifty 50, Nifty Midcap, Nifty Smallcap).",
            inputSchema={
                "type": "object",
                "properties": {
                    "index_name": {
                        "type": "string",
                        "description": "Index name (NIFTY50, NIFTYMIDCAP150, NIFTYSMLCAP250)",
                    }
                },
                "required": ["index_name"],
            },
        ),
        Tool(
            name="search_stocks",
            description="Search for stocks by name or symbol.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                    }
                },
                "required": ["query"],
            },
        ),
    ]


@mcp_server.call_tool()
async def call_tool(
    name: str, arguments: Dict[str, Any]
) -> List[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls."""

    if name == "get_stock_price":
        symbol = arguments.get("symbol")
        if not symbol:
            return [TextContent(type="text", text="Error: Symbol is required")]

        try:
            stock_data = get_stock_data(symbol)
            html = create_widget_html("stock-widget", stock_data)

            return [
                TextContent(
                    type="text",
                    text=f"Current price for {symbol}: ₹{stock_data['price']} ({stock_data['changePercent']:+.2f}%)",
                ),
                EmbeddedResource(
                    type="resource",
                    resource=Resource(
                        uri=AnyUrl(f"{BASE_URL}/stock-widget.html"),
                        name=f"{symbol} Stock Widget",
                        mimeType="text/html",
                        text=html,
                    ),
                ),
            ]
        except Exception as e:
            return [
                TextContent(type="text", text=f"Error fetching stock data: {str(e)}")
            ]

    elif name == "get_multiple_stocks":
        symbols = arguments.get("symbols")
        if not symbols or not isinstance(symbols, list):
            return [TextContent(type="text", text="Error: Symbols array is required")]

        try:
            stocks_data = get_multiple_stocks_data(symbols)
            data = {"stocks": stocks_data}
            html = create_widget_html("stock-carousel", data)

            summary = f"Displaying {len(symbols)} stocks: " + ", ".join(
                f"{s['symbol']}: ₹{s['price']} ({s['changePercent']:+.2f}%)"
                for s in stocks_data
            )

            return [
                TextContent(type="text", text=summary),
                EmbeddedResource(
                    type="resource",
                    resource=Resource(
                        uri=AnyUrl(f"{BASE_URL}/stock-carousel.html"),
                        name="Stock Carousel",
                        mimeType="text/html",
                        text=html,
                    ),
                ),
            ]
        except Exception as e:
            return [
                TextContent(type="text", text=f"Error fetching stocks: {str(e)}")
            ]

    elif name == "get_index_data":
        index_name = arguments.get("index_name")
        if not index_name:
            return [TextContent(type="text", text="Error: Index name is required")]

        try:
            index_data = get_index_data(index_name)
            html = create_widget_html("index-widget", index_data)

            return [
                TextContent(
                    type="text",
                    text=f"{index_name}: {index_data['value']:.2f} ({index_data['changePercent']:+.2f}%)",
                ),
                EmbeddedResource(
                    type="resource",
                    resource=Resource(
                        uri=AnyUrl(f"{BASE_URL}/index-widget.html"),
                        name=f"{index_name} Index Widget",
                        mimeType="text/html",
                        text=html,
                    ),
                ),
            ]
        except Exception as e:
            return [
                TextContent(type="text", text=f"Error fetching index data: {str(e)}")
            ]

    elif name == "search_stocks":
        query = arguments.get("query")
        if not query:
            return [TextContent(type="text", text="Error: Query is required")]

        try:
            results = search_stocks(query)
            if not results:
                return [
                    TextContent(
                        type="text", text=f"No stocks found matching '{query}'"
                    )
                ]

            result_text = f"Found {len(results)} stocks matching '{query}':\\n\\n"
            for stock in results:
                result_text += f"• {stock['symbol']} - {stock['name']}\\n"

            return [TextContent(type="text", text=result_text)]
        except Exception as e:
            return [
                TextContent(type="text", text=f"Error searching stocks: {str(e)}")
            ]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


def create_sse_transport():
    """Create SSE transport for MCP server."""
    return SseServerTransport("/mcp")


# Export server and transport
__all__ = ["mcp_server", "create_sse_transport"]
