#!/bin/bash

echo "============================================"
echo "  AI Spam Detection - Starting Services"
echo "============================================"
echo ""

# Check if required folders exist
if [ ! -d "ml-service" ]; then
    echo "ERROR: ml-service folder not found"
    exit 1
fi

if [ ! -d "backend" ]; then
    echo "ERROR: backend folder not found"
    exit 1
fi

if [ ! -d "frontend" ]; then
    echo "ERROR: frontend folder not found"
    exit 1
fi

echo "[1/3] Starting ML Service..."
osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/ml-service && source venv/bin/activate && python src/app.py"'
sleep 3

echo "[2/3] Starting Backend API..."
osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/backend && npm run dev"'
sleep 3

echo "[3/3] Starting Frontend..."
osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/frontend && npm start"'

echo ""
echo "============================================"
echo "  All services are starting!"
echo "============================================"
echo ""
echo "ML Service:  http://localhost:5000"
echo "Backend API: http://localhost:3001"
echo "Frontend:    http://localhost:3000"
echo ""
echo "Opening application in 5 seconds..."
sleep 5

open http://localhost:3000

echo ""
echo "Services are running in separate Terminal windows."
echo "Close those windows to stop the services."
echo ""
