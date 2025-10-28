@echo off
echo ============================================
echo Build and Restart Backend API
echo ============================================
echo.

cd /d "%~dp0.."

echo [1/2] Building backend Docker image...
docker-compose -f docker-compose.dev.yml build api
if %errorlevel% neq 0 (
    echo Backend build failed!
    pause
    exit /b %errorlevel%
)
echo Backend built successfully!
echo.

echo [2/2] Restarting API container...
docker-compose -f docker-compose.dev.yml up -d api
if %errorlevel% neq 0 (
    echo Failed to restart API container!
    pause
    exit /b %errorlevel%
)
echo.
echo Backend restarted successfully!
echo API is running at http://localhost:5102
echo Logs: scripts\logs-api-dev.bat
echo.

pause
