@echo off
echo ============================================
echo Build Frontend Only
echo ============================================
echo.
echo This builds the frontend and updates dist/
echo nginx will automatically serve the new files
echo.

cd /d "%~dp0.."
cd frontend

echo Building frontend...
call npm run build
if %errorlevel% neq 0 (
    echo Frontend build failed!
    pause
    exit /b %errorlevel%
)

echo.
echo ============================================
echo Build Complete!
echo ============================================
echo Frontend updated at http://localhost:8082
echo No container restart needed - changes are live!
echo.

pause
