#!/bin/bash

# Script to launch IBM Bob 2.0 Backend & Frontend concurrently
set -e

echo "🚀 Starting IBM Bob 2.0 - Kanban Evidence Tracker..."

# 1. Start Backend in background
echo "📦 Starting FastAPI backend on http://localhost:8000..."
cd "$(dirname "$0")/backend"
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Trap signals to shut down backend when frontend terminates
trap "echo '🛑 Shutting down backend...'; kill $BACKEND_PID" EXIT INT TERM

# 2. Start Frontend
echo "💻 Starting React (Vite) frontend on http://localhost:5173..."
cd "../frontend"
npm run dev
