@echo off
echo ============================================
echo Database Migration - Development
echo ============================================
echo.

cd /d "%~dp0.."

echo Running Alembic migrations inside Docker container...
docker-compose -f docker-compose.dev.yml exec api alembic upgrade head

echo.
echo Migration complete!
pause
