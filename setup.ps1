# Trade Detail Setup Script for Windows
# Run this in PowerShell

Write-Host "🚀 Setting up Trade Detail..." -ForegroundColor Green
Write-Host ""

# Check Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js is not installed. Please install Node.js 18 or higher." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Node.js $(node --version) found" -ForegroundColor Green

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python is not installed. Please install Python 3.10 or higher." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Python $(python --version) found" -ForegroundColor Green

# Install pnpm if not present
if (-not (Get-Command pnpm -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Installing pnpm..." -ForegroundColor Yellow
    npm install -g pnpm
}

Write-Host "✅ pnpm found" -ForegroundColor Green

# Install frontend dependencies
Write-Host ""
Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
pnpm install

# Create Python virtual environment
Write-Host ""
Write-Host "🐍 Creating Python virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

Write-Host "✅ Virtual environment created" -ForegroundColor Green

# Activate virtual environment and install dependencies
Write-Host ""
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r server/requirements.txt

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "📝 Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✅ .env file created. Please update it with your settings." -ForegroundColor Green
}

Write-Host ""
Write-Host "✨ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Activate virtual environment: .venv\Scripts\Activate.ps1"
Write-Host "  2. Build frontend: pnpm run build"
Write-Host "  3. Start asset server: pnpm run serve (in one terminal)"
Write-Host "  4. Start backend: uvicorn server.main:app --reload (in another terminal)"
Write-Host "  5. Visit http://localhost:8000"
Write-Host ""
Write-Host "For deployment instructions, see DEPLOYMENT.md"
Write-Host "🚀 Happy coding!" -ForegroundColor Green
