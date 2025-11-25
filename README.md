# Trade Detail - Stock Price Display App for ChatGPT

A ChatGPT app built with the Apps SDK that displays stock prices and index data in beautiful carousel and widget formats. Built using Python (FastAPI) backend with TypeScript/React frontend components.

## Features

- 📊 **Real-time Stock Prices**: Display current stock prices with live updates
- 📈 **Index Data**: Track major market indices (Nifty 50, Nifty Midcap, Nifty Smallcap)
- 🎠 **Carousel View**: Swipe through multiple stocks in an elegant carousel
- 📱 **Widget Format**: Compact widget display for quick glances
- 🚀 **Easy Deployment**: One-click deployment to Render
- 💬 **ChatGPT Integration**: Use natural language to query stock data

## Architecture

This app follows the Model Context Protocol (MCP) specification:

- **Backend**: Python FastAPI server implementing MCP protocol
- **Frontend**: TypeScript/React components with Tailwind CSS
- **Widgets**: Pre-built UI components served as embedded resources
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
│   ├── main.py                  # FastAPI application
│   ├── stock_data.py            # Stock data fetching logic
│   └── requirements.txt         # Python dependencies
├── assets/                       # Built widget bundles (generated)
├── build-all.mts                # Build orchestrator
└── render.yaml                  # Render deployment config
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- pnpm (recommended) or npm

### Installation

1. Clone the repository:
```bash
git clone https://github.com/vikkysarswat/trade_detail.git
cd trade_detail
```

2. Install frontend dependencies:
```bash
pnpm install
```

3. Install Python dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r server/requirements.txt
```

### Build Frontend Components

```bash
pnpm run build
```

This generates the widget bundles in the `assets/` directory.

### Start Static Asset Server

```bash
pnpm run serve
```

The assets will be available at `http://localhost:4444`

### Start Python MCP Server

```bash
uvicorn server.main:app --port 8000 --reload
```

Your MCP server will be running at `http://localhost:8000`

## Usage in ChatGPT

### 1. Enable Developer Mode

- Go to [ChatGPT Developer Mode](https://platform.openai.com/docs/guides/developer-mode)
- Enable developer mode in Settings

### 2. Add Your App

#### For Local Development (using ngrok):

```bash
ngrok http 8000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok-free.app`) and add it in:
- ChatGPT Settings > Connectors
- Add connector URL: `https://abc123.ngrok-free.app/mcp`

#### For Production (Render):

Once deployed to Render, use your Render URL:
- `https://your-app-name.onrender.com/mcp`

### 3. Use in Conversations

Add the connector to your conversation via "More" options, then ask:

- "Show me the current price of RELIANCE"
- "What are the top performers in Nifty 50?"
- "Display TCS, Infosys, and Wipro stock prices"
- "How is Nifty Smallcap 250 performing?"

## Deployment to Render

### Method 1: Automatic Deployment

1. Fork this repository
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" > "Web Service"
4. Connect your GitHub repository
5. Render will automatically detect `render.yaml` and deploy

### Method 2: Manual Configuration

1. Create a new Web Service on Render
2. Configure:
   - **Build Command**: `pnpm install && pnpm run build && pip install -r server/requirements.txt`
   - **Start Command**: `uvicorn server.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     - `BASE_URL`: Your Render URL (e.g., `https://your-app.onrender.com`)
     - `PYTHON_VERSION`: `3.11`

## Environment Variables

- `BASE_URL`: Base URL for serving widget assets (required for production)
- `STOCK_API_KEY`: API key for stock data service (optional, uses mock data if not provided)
- `PORT`: Server port (default: 8000, Render sets this automatically)

## Development

### Adding New Widgets

1. Create a new component in `src/your-widget/`
2. Add the entry point in `src/your-widget/main.tsx`
3. The build script will automatically pick it up

### Customizing Stock Data

Edit `server/stock_data.py` to integrate with your preferred stock data API:

- Yahoo Finance
- Alpha Vantage
- NSE India API
- Your custom data source

### Hot Reload Development

```bash
# Terminal 1: Frontend
pnpm run dev

# Terminal 2: Backend
uvicorn server.main:app --reload --port 8000

# Terminal 3: Static server
pnpm run serve
```

## API Endpoints

- `GET /mcp` - MCP endpoint for ChatGPT
- `POST /mcp` - MCP tool calls
- `GET /health` - Health check
- `GET /` - API info

## MCP Tools

The server exposes these tools to ChatGPT:

1. **get_stock_price**: Get current price and details for a stock symbol
2. **get_multiple_stocks**: Display multiple stocks in carousel format
3. **get_index_data**: Get market index information (Nifty 50, Nifty Midcap, etc.)
4. **search_stocks**: Search for stocks by name or symbol

## Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn
- **Frontend**: TypeScript, React 18, Vite
- **Styling**: Tailwind CSS
- **Protocol**: Model Context Protocol (MCP)
- **Deployment**: Render

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/vikkysarswat/trade_detail/issues)
- Email: vikky.sarswat@gmail.com

## Acknowledgments

- Built with inspiration from [OpenAI Apps SDK Examples](https://github.com/openai/openai-apps-sdk-examples)
- Uses the Model Context Protocol (MCP) specification