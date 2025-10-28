@echo off
echo ============================================
echo Stopping Whittaker Agency - Development
echo ============================================
echo.

cd /d "%~dp0.."

echo Stopping Docker containers...
docker-compose -f docker-compose.dev.yml down

echo.
echo All services stopped.
pause
