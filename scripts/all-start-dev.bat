@echo off
echo ============================================
echo Starting Whittaker Agency - Development
echo ============================================
echo.

cd /d "%~dp0.."

echo [1/4] Stopping existing containers...
docker-compose -f docker-compose.dev.yml down
echo Containers stopped!
echo.

cd /d "%~dp0"

echo [2/4] Building frontend...
call frontend-build-dev.bat
if %errorlevel% neq 0 (
    echo Frontend build failed!
    pause
    exit /b %errorlevel%
)
echo.

cd /d "%~dp0.."

echo [3/4] Building backend Docker image...
docker-compose -f docker-compose.dev.yml build api
if %errorlevel% neq 0 (
    echo Backend build failed!
    pause
    exit /b %errorlevel%
)
echo Backend built successfully!
echo.

echo [4/4] Starting all Docker containers...
docker-compose -f docker-compose.dev.yml up -d
echo.
echo ============================================
echo All services started successfully!
echo ============================================
echo.
echo Frontend: http://localhost:5173
echo Backend API: http://localhost:8000
echo.
echo To view logs: docker-compose -f docker-compose.dev.yml logs -f
echo To stop: docker-compose -f docker-compose.dev.yml down
echo.
pause
