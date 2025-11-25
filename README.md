# Trade Detail - Stock Price Display App for ChatGPT

A ChatGPT app built with **Model Context Protocol (MCP)** that displays stock prices and index data in beautiful carousel and widget formats. Built using Python (FastAPI) backend with TypeScript/React frontend components.

## ⚡ MCP Protocol Support

✅ **SSE Transport (Server-Sent Events)** - Full MCP 1.0 compliance  
✅ **ChatGPT Compatible** - Works with Custom MCP Connectors  
✅ **JSON-RPC 2.0** - Standard protocol implementation  

**Connection URL**: `https://your-app-name.onrender.com/mcp`

> 📖 **[Complete MCP Testing & Connection Guide →](./MCP_TESTING.md)**

## Features

- 📊 **Real-time Stock Prices**: Display current stock prices with live updates
- 📈 **Index Data**: Track major market indices (Nifty 50, Nifty Midcap, Nifty Smallcap)
- 🎠 **Carousel View**: Swipe through multiple stocks in an elegant carousel
- 📱 **Widget Format**: Compact widget display for quick glances
- 🚀 **Easy Deployment**: One-click deployment to Render
- 💬 **ChatGPT Integration**: Use natural language to query stock data

## Architecture

This app follows the **Model Context Protocol (MCP)** specification:

- **Backend**: Python FastAPI server with MCP SSE transport
- **Frontend**: TypeScript/React components with Tailwind CSS
- **Widgets**: Pre-built UI components served as embedded resources
- **Transport**: SSE (Server-Sent Events) over HTTPS
- **Protocol**: MCP 1.0 + JSON-RPC 2.0
- **Deployment**: Render-ready with automatic builds

## Project Structure

```
trade_detail/
├── src/                          # Frontend React components
│   ├── stock-carousel/          # Carousel widget for stocks
│   ├── stock-widget/            # Individual stock widget
│   ├── index-widget/            # Market indices widget
│   └── utils/                   # Shared utilities
├── server/                       # Python MCP server
│   ├── main.py                  # FastAPI + MCP integration
│   ├── mcp_server.py            # MCP server with SSE transport
│   ├── stock_data.py            # Stock data fetching logic
│   └── requirements.txt         # Python dependencies
├── assets/                       # Built widget bundles (generated)
├── MCP_TESTING.md               # MCP testing & connection guide
├── build-all.mts                # Build orchestrator
└── render.yaml                  # Render deployment config
```

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+
- pnpm (recommended) or npm

### Installation

```bash
# Clone repository
git clone https://github.com/vikkysarswat/trade_detail.git
cd trade_detail

# Install dependencies
pnpm install
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r server/requirements.txt

# Build frontend
pnpm run build

# Start servers
pnpm run serve                              # Terminal 1: Assets (port 4444)
uvicorn server.main:app --reload --port 8000  # Terminal 2: MCP server
```

Visit `http://localhost:8000` to verify server is running.

## Deploy to Render

### One-Click Deployment

1. Fork this repository
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" > "Web Service"
4. Connect your GitHub repository
5. Render auto-detects `render.yaml` and deploys

### Set Environment Variables

```
BASE_URL = https://your-app-name.onrender.com
```

### Verify Deployment

```bash
curl https://your-app-name.onrender.com/health
# Should return: {"status": "healthy"}
```

## Connect to ChatGPT

### Step 1: Enable Developer Mode
- Go to ChatGPT Settings
- Enable "Developer Mode"

### Step 2: Add Custom MCP Connector

**Connector URL**:
```
https://your-app-name.onrender.com/mcp
```

### Step 3: Test

Add the connector to your chat and try:
- "Show me the current price of RELIANCE"
- "Display TCS, Infosys, and Wipro stock prices"
- "What's the Nifty 50 index doing?"

> 📖 **[Detailed connection guide with troubleshooting →](./MCP_TESTING.md)**

## MCP Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_stock_price` | Single stock widget | `symbol` (string) |
| `get_multiple_stocks` | Carousel with multiple stocks | `symbols` (array) |
| `get_index_data` | Market index display | `index_name` (string) |
| `search_stocks` | Search for stocks | `query` (string) |

## Development

### Test MCP Locally

```bash
# Install MCP inspector
npm install -g @modelcontextprotocol/inspector

# Test your server
mcp-inspector http://localhost:8000/mcp
```

### Adding New Widgets

1. Create component in `src/your-widget/`
2. Add entry point `src/your-widget/main.tsx`
3. Build automatically detects it

### Customizing Stock Data

Edit `server/stock_data.py` to integrate with:
- Yahoo Finance (default)
- Alpha Vantage
- NSE India API
- Your custom data source

## API Endpoints

- **`/mcp`** - MCP SSE endpoint for ChatGPT
- **`/health`** - Health check
- **`/`** - Server info

## Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn, MCP SDK
- **Frontend**: TypeScript, React 18, Vite
- **Styling**: Tailwind CSS
- **Protocol**: Model Context Protocol (MCP) with SSE
- **Deployment**: Render

## Troubleshooting

### "404 Not Found" in ChatGPT
- ✅ Verify URL: `https://your-app.onrender.com/mcp` (no trailing slash)
- ✅ Check health endpoint works
- ✅ Ensure HTTPS is enabled

### Widgets Not Rendering
- ✅ Set `BASE_URL` environment variable
- ✅ Build assets: `pnpm run build`
- ✅ Check assets accessible

### Connection Timeout
- ✅ Check Render logs for errors
- ✅ Verify server is running: `curl /health`
- ✅ Test with MCP inspector locally first

> 📖 **[Complete troubleshooting guide →](./MCP_TESTING.md)**

## Documentation

- **[MCP Testing & Connection Guide](./MCP_TESTING.md)** - Comprehensive testing instructions
- **[Deployment Guide](./DEPLOYMENT.md)** - Deployment options and configurations
- **[Contributing Guide](./CONTRIBUTING.md)** - How to contribute

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](./LICENSE) file for details

## Support

- **Issues**: [GitHub Issues](https://github.com/vikkysarswat/trade_detail/issues)
- **Email**: vikky.sarswat@gmail.com

## Acknowledgments

- Built with [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- Inspired by [OpenAI Apps SDK Examples](https://github.com/openai/openai-apps-sdk-examples)
- Uses official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

**Ready to deploy?** → [Render Dashboard](https://dashboard.render.com/)  
**Need help?** → [MCP Testing Guide](./MCP_TESTING.md)
