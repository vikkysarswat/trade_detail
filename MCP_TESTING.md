# MCP Server Testing & Connection Guide

## 🔌 MCP Server Architecture

This server now uses the **official Model Context Protocol (MCP)** with SSE (Server-Sent Events) transport, making it compatible with ChatGPT's Custom MCP Connectors.

### Transport: SSE (Server-Sent Events)
- **Endpoint**: `/mcp`
- **Protocol**: SSE over HTTP
- **Format**: JSON-RPC 2.0

---

## 🧪 Local Testing

### 1. Start the Server

```bash
# Terminal 1: Asset server
pnpm run serve

# Terminal 2: MCP server
source .venv/bin/activate
uvicorn server.main:app --reload --port 8000
```

### 2. Test HTTP Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Server info
curl http://localhost:8000/

# Expected output:
# {
#   "name": "Trade Detail MCP Server",
#   "version": "1.0.0",
#   "transport": "SSE (Server-Sent Events)",
#   "status": "operational"
# }
```

### 3. Test MCP Protocol

Install MCP inspector:
```bash
npm install -g @modelcontextprotocol/inspector
```

Test the server:
```bash
mcp-inspector http://localhost:8000/mcp
```

You should see:
- ✅ List of 4 tools
- ✅ Tool schemas
- ✅ Ability to call tools

---

## 🌐 Production Deployment

### Deploy to Render

1. **Push code to GitHub** (already done)

2. **Deploy on Render**:
   - Go to https://dashboard.render.com/
   - Create new Web Service
   - Connect to `vikkysarswat/trade_detail`
   - Auto-detects config from `render.yaml`

3. **Set Environment Variables**:
   ```
   BASE_URL = https://your-app-name.onrender.com
   ```

4. **Wait for deployment** (~5 minutes)

5. **Verify deployment**:
   ```bash
   curl https://your-app-name.onrender.com/health
   ```

---

## 🤖 Connect to ChatGPT

### Step 1: Enable Developer Mode
1. Go to ChatGPT Settings
2. Enable "Developer Mode"
3. Navigate to Settings > Connectors

### Step 2: Add Custom MCP Connector

**Use this URL format**:
```
https://your-app-name.onrender.com/mcp
```

For example:
```
https://trade-detail.onrender.com/mcp
```

### Step 3: Configure Connector

- **Name**: Trade Detail Stock Prices
- **URL**: `https://your-app-name.onrender.com/mcp`
- **Transport**: SSE (automatically detected)
- **Authentication**: None (public API)

### Step 4: Test in ChatGPT

Add the connector to your conversation, then try:

1. **Single stock**:
   ```
   Show me the current price of RELIANCE
   ```

2. **Multiple stocks (carousel)**:
   ```
   Display TCS, Infosys, and Wipro stock prices
   ```

3. **Market index**:
   ```
   What's the Nifty 50 index doing?
   ```

4. **Search**:
   ```
   Search for bank stocks
   ```

---

## 🐛 Troubleshooting

### Issue: "404 Not Found"
**Cause**: Wrong endpoint URL  
**Fix**: Ensure URL is exactly `https://your-app.onrender.com/mcp` (no trailing slash)

### Issue: "Connection timeout"
**Cause**: Server not responding  
**Fix**: 
1. Check server logs on Render dashboard
2. Verify health endpoint: `curl https://your-app.onrender.com/health`
3. Check BASE_URL environment variable is set

### Issue: "Invalid transport"
**Cause**: ChatGPT expecting SSE  
**Fix**: The server now uses SSE transport - this should work automatically

### Issue: Tools not showing
**Cause**: MCP protocol negotiation failed  
**Fix**:
1. Test with MCP inspector: `mcp-inspector https://your-app.onrender.com/mcp`
2. Check server logs for errors
3. Ensure all dependencies installed: `pip install -r server/requirements.txt`

### Issue: Widgets not rendering
**Cause**: BASE_URL not set or assets not built  
**Fix**:
1. Set BASE_URL on Render: `https://your-app-name.onrender.com`
2. Rebuild assets: `pnpm run build`
3. Verify assets accessible: `curl https://your-app.onrender.com/assets/stock-widget.js`

---

## 🔍 Advanced Testing

### Test MCP Protocol Directly

Using `curl` to test SSE:

```bash
curl -N -H "Accept: text/event-stream" \
  http://localhost:8000/mcp
```

Expected: SSE stream with JSON-RPC messages

### Test Tool Execution

Using MCP inspector:
```bash
mcp-inspector http://localhost:8000/mcp

# In the inspector:
1. Select tool: get_stock_price
2. Enter params: {"symbol": "RELIANCE"}
3. Execute
4. Verify response includes HTML widget
```

---

## 📊 Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `get_stock_price` | Single stock widget | `symbol` (string) |
| `get_multiple_stocks` | Carousel widget | `symbols` (array) |
| `get_index_data` | Index widget | `index_name` (string) |
| `search_stocks` | Search stocks | `query` (string) |

---

## 🔗 URLs Reference

### Local Development
- **MCP Endpoint**: `http://localhost:8000/mcp`
- **Assets**: `http://localhost:4444`
- **Health**: `http://localhost:8000/health`

### Production (Render)
- **MCP Endpoint**: `https://your-app-name.onrender.com/mcp`
- **Assets**: `https://your-app-name.onrender.com/assets/`
- **Health**: `https://your-app-name.onrender.com/health`

### ChatGPT Connector
- **Format**: `https://your-app-name.onrender.com/mcp`
- **Transport**: SSE (Server-Sent Events)
- **Protocol**: MCP 1.0 + JSON-RPC 2.0

---

## ✅ Connection Checklist

Before connecting to ChatGPT:

- [ ] Server deployed and healthy (`/health` returns 200)
- [ ] Assets built and accessible
- [ ] BASE_URL environment variable set
- [ ] MCP endpoint responds to requests (`/mcp`)
- [ ] Tools listed correctly via MCP inspector
- [ ] No errors in server logs
- [ ] SSL/HTTPS enabled (required by ChatGPT)

---

## 📞 Support

If you encounter issues:
1. Check server logs on Render dashboard
2. Test with MCP inspector locally
3. Verify all environment variables set
4. Review this guide's troubleshooting section
5. Open GitHub issue: https://github.com/vikkysarswat/trade_detail/issues
