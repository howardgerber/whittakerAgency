@echo off
echo ============================================
echo Starting Whittaker Agency - Development
echo ============================================
echo.

cd /d "%~dp0"

echo [1/3] Building frontend...
call frontend-build-dev.bat
if %errorlevel% neq 0 (
    echo Frontend build failed!
    pause
    exit /b %errorlevel%
)
echo.

cd /d "%~dp0.."

echo [2/3] Building backend Docker image...
docker-compose -f docker-compose.dev.yml build api
if %errorlevel% neq 0 (
    echo Backend build failed!
    pause
    exit /b %errorlevel%
)
echo Backend built successfully!
echo.

echo [3/3] Starting all Docker containers...
docker-compose -f docker-compose.dev.yml up

pause
