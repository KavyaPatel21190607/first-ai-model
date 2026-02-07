@echo off
echo ============================================
echo   AI Spam Detection - Starting Services
echo ============================================
echo.

REM Check if required folders exist
if not exist "ml-service" (
    echo ERROR: ml-service folder not found
    pause
    exit /b 1
)

if not exist "backend" (
    echo ERROR: backend folder not found
    pause
    exit /b 1
)

if not exist "frontend" (
    echo ERROR: frontend folder not found
    pause
    exit /b 1
)

echo [1/3] Starting ML Service...
start "ML Service" cmd /k "cd ml-service && venv\Scripts\activate && python src/app.py"
timeout /t 3 >nul

echo [2/3] Starting Backend API...
start "Backend API" cmd /k "cd backend && npm run dev"
timeout /t 3 >nul

echo [3/3] Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm start"

echo.
echo ============================================
echo   All services are starting!
echo ============================================
echo.
echo ML Service:  http://localhost:5000
echo Backend API: http://localhost:3001
echo Frontend:    http://localhost:3000
echo.
echo Press any key to open the application...
pause >nul

start http://localhost:3000

echo.
echo Services are running in separate windows.
echo Close those windows to stop the services.
echo.
pause
