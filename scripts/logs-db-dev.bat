@echo off
echo ============================================
echo Viewing Database Logs - Development
echo ============================================
echo.

cd /d "%~dp0.."
docker-compose -f docker-compose.dev.yml logs -f whittaker-db
