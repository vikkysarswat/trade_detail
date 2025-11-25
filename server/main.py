"""FastAPI + MCP server for stock and index data."""

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.applications import Starlette
from starlette.routing import Mount

from server.mcp_server import mcp_server, create_sse_transport

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


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Trade Detail MCP Server",
        "version": "1.0.0",
        "description": "Stock and Index Price Display for ChatGPT",
        "mcp_endpoint": "/mcp",
        "transport": "SSE (Server-Sent Events)",
        "status": "operational",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


# Mount MCP SSE transport
sse_transport = create_sse_transport()
sse_app = sse_transport.get_asgi_app(mcp_server)

# Mount SSE app at /mcp
app.mount("/mcp", sse_app)


if __name__ == "__main__":
    from mcp_server import mcp_server
    mcp_server.run(host="0.0.0.0", port=8000)
