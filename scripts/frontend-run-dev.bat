@echo off
echo ============================================
echo Build and Run Frontend Dev Server
echo ============================================
echo.

cd /d "%~dp0.."
cd frontend

echo [1/2] Building frontend...
call npm run build:dev
if %errorlevel% neq 0 (
    echo Frontend build failed!
    pause
    exit /b %errorlevel%
)
echo Build successful!
echo.

echo [2/2] Starting Vite dev server on http://localhost:3003
echo Hot-reload enabled - changes will update automatically
echo.
npm run dev

pause
