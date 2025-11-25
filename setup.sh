#!/bin/bash

# Trade Detail Setup Script
# This script sets up the development environment

set -e

echo "🚀 Setting up Trade Detail..."
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

echo "✅ Node.js $(node --version) found"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.10 or higher."
    exit 1
fi

echo "✅ Python $(python3 --version) found"

# Install pnpm if not present
if ! command -v pnpm &> /dev/null; then
    echo "📦 Installing pnpm..."
    npm install -g pnpm
fi

echo "✅ pnpm $(pnpm --version) found"

# Install frontend dependencies
echo ""
echo "📦 Installing frontend dependencies..."
pnpm install

# Create Python virtual environment
echo ""
echo "🐍 Creating Python virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

echo "✅ Virtual environment created"

# Activate virtual environment and install dependencies
echo ""
echo "📦 Installing Python dependencies..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r server/requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created. Please update it with your settings."
fi

# Install pre-commit hooks
if command -v pre-commit &> /dev/null; then
    echo ""
    echo "🔧 Installing pre-commit hooks..."
    pre-commit install
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Activate virtual environment: source .venv/bin/activate"
echo "  2. Build frontend: pnpm run build"
echo "  3. Start asset server: pnpm run serve (in one terminal)"
echo "  4. Start backend: uvicorn server.main:app --reload (in another terminal)"
echo "  5. Visit http://localhost:8000"
echo ""
echo "For deployment instructions, see DEPLOYMENT.md"
echo "🚀 Happy coding!"
