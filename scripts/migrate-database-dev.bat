@echo off
echo ============================================
echo Database Migration - Development
echo ============================================
echo.

cd /d "%~dp0.."
cd backend

echo Running Alembic migrations...
alembic upgrade head

echo.
echo Migration complete!
cd ..
pause
