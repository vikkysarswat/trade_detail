# Deployment Guide

This guide covers different deployment options for the Trade Detail app.

## Option 1: Deploy to Render (Recommended)

Render provides free hosting with automatic deployments from GitHub.

### Automatic Deployment

1. **Fork or Clone this repository**

2. **Create a new Web Service on Render:**
   - Go to https://dashboard.render.com/
   - Click "New +" > "Web Service"
   - Connect your GitHub account
   - Select the `trade_detail` repository

3. **Render will automatically detect `render.yaml`:**
   - Service name: `trade-detail`
   - Environment: Python
   - Build command: Automatically configured
   - Start command: Automatically configured

4. **Set Environment Variables:**
   - `BASE_URL`: Will be set to your Render URL (e.g., `https://trade-detail.onrender.com`)
   - `STOCK_API_KEY`: (Optional) Your stock data API key

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for the build to complete (~5-10 minutes)
   - Your app will be live at `https://your-service-name.onrender.com`

### Manual Configuration

If you prefer manual setup:

1. **Build Command:**
```bash
npm install -g pnpm && pnpm install && pnpm run build && pip install -r server/requirements.txt
```

2. **Start Command:**
```bash
uvicorn server.main:app --host 0.0.0.0 --port $PORT
```

3. **Environment Variables:**
   - `PYTHON_VERSION`: `3.11`
   - `BASE_URL`: Your Render app URL
   - `STOCK_API_KEY`: (Optional) Stock API key

## Option 2: Deploy to Railway

1. **Install Railway CLI:**
```bash
npm install -g @railway/cli
```

2. **Login and Initialize:**
```bash
railway login
railway init
```

3. **Deploy:**
```bash
railway up
```

4. **Set Environment Variables:**
```bash
railway variables set BASE_URL=https://your-app.railway.app
railway variables set PYTHON_VERSION=3.11
```

## Option 3: Deploy to Heroku

1. **Create `Procfile`:**
```
web: uvicorn server.main:app --host 0.0.0.0 --port $PORT
```

2. **Deploy:**
```bash
heroku create your-app-name
git push heroku main
heroku config:set BASE_URL=https://your-app-name.herokuapp.com
```

## Option 4: Deploy to Vercel

1. **Create `vercel.json`:**
```json
{
  "builds": [
    {
      "src": "server/main.py",
      "use": "@vercel/python"
    },
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "assets"
      }
    }
  ],
  "routes": [
    {
      "src": "/assets/(.*)",
      "dest": "/assets/$1"
    },
    {
      "src": "/(.*)",
      "dest": "server/main.py"
    }
  ]
}
```

2. **Deploy:**
```bash
vercel
```

## Option 5: Self-Hosted (VPS/Cloud)

### Using Docker (Recommended for Self-Hosting)

1. **Create `Dockerfile`:**
```dockerfile
FROM node:18-alpine AS frontend-builder
WORKDIR /app
COPY package*.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install
COPY . .
RUN pnpm run build

FROM python:3.11-slim
WORKDIR /app
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=frontend-builder /app/assets ./assets
COPY server ./server
EXPOSE 8000
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Build and Run:**
```bash
docker build -t trade-detail .
docker run -p 8000:8000 -e BASE_URL=https://your-domain.com trade-detail
```

### Using Nginx + Gunicorn

1. **Install Dependencies:**
```bash
sudo apt update
sudo apt install python3-pip nodejs npm nginx
```

2. **Setup Application:**
```bash
git clone https://github.com/vikkysarswat/trade_detail.git
cd trade_detail
npm install -g pnpm
pnpm install && pnpm run build
python3 -m venv venv
source venv/bin/activate
pip install -r server/requirements.txt
pip install gunicorn
```

3. **Create Systemd Service `/etc/systemd/system/trade-detail.service`:**
```ini
[Unit]
Description=Trade Detail MCP Server
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/trade_detail
Environment="PATH=/path/to/trade_detail/venv/bin"
Environment="BASE_URL=https://your-domain.com"
ExecStart=/path/to/trade_detail/venv/bin/gunicorn server.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

4. **Configure Nginx `/etc/nginx/sites-available/trade-detail`:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /assets/ {
        alias /path/to/trade_detail/assets/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. **Enable and Start:**
```bash
sudo systemctl enable trade-detail
sudo systemctl start trade-detail
sudo ln -s /etc/nginx/sites-available/trade-detail /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Post-Deployment

### 1. Test Your Deployment

Visit these endpoints:
- `https://your-app-url.com/` - Should show API info
- `https://your-app-url.com/health` - Should return `{"status": "healthy"}`
- `https://your-app-url.com/mcp` - Should list available tools

### 2. Connect to ChatGPT

1. Enable [Developer Mode](https://platform.openai.com/docs/guides/developer-mode) in ChatGPT
2. Go to Settings > Connectors
3. Add new connector: `https://your-app-url.com/mcp`
4. Test with queries like "Show me RELIANCE stock price"

### 3. Monitor Your App

- **Render**: Check logs in the Render dashboard
- **Self-hosted**: Use `journalctl -u trade-detail -f`
- **Docker**: Use `docker logs -f container-id`

## Troubleshooting

### Build Failures

1. **Frontend build fails:**
   - Ensure Node.js 18+ is installed
   - Try `pnpm install --force`

2. **Python dependencies fail:**
   - Check Python version is 3.10+
   - Try `pip install --upgrade pip`

### Runtime Issues

1. **Widgets not loading:**
   - Verify `BASE_URL` environment variable is set correctly
   - Check CORS settings in `server/main.py`

2. **Stock data not fetching:**
   - Install yfinance: `pip install yfinance`
   - Check internet connectivity from server
   - Verify NSE stock symbols are correct

3. **MCP connection fails:**
   - Ensure `/mcp` endpoint is accessible
   - Check server logs for errors
   - Verify HTTPS is enabled (required by ChatGPT)

## Updating Your Deployment

### Render (Automatic)
- Just push to GitHub - Render will auto-deploy

### Manual Updates
```bash
git pull origin main
pnpm install && pnpm run build
pip install -r server/requirements.txt
sudo systemctl restart trade-detail
```

## Security Considerations

1. **API Keys**: Store in environment variables, never commit to git
2. **HTTPS**: Always use HTTPS in production (required for ChatGPT)
3. **Rate Limiting**: Consider adding rate limiting for production use
4. **CORS**: Adjust CORS settings based on your needs

## Cost Estimates

- **Render Free Tier**: $0/month (with limitations)
- **Render Starter**: $7/month
- **Railway**: ~$5-10/month
- **Heroku**: ~$7/month
- **VPS (DigitalOcean)**: $6/month
- **Vercel**: Free for personal projects