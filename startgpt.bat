@echo off
TITLE WebsiteNow - AI Website Builder
COLOR 0B
cls

echo ═══════════════════════════════════════════════════════════════
echo    WEBSITENOW - AI WEBSITE BUILDER
echo ═══════════════════════════════════════════════════════════════
echo.
echo    🚀 Starting WebsiteNow...
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
timeout /t 1 >nul

:: Change to script directory (where the Python files are)
cd /d "%~dp0"

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python is not installed or not in PATH!
    echo.
    echo Please run installgpt.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

:: Check if requirements are installed
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Required packages not installed!
    echo.
    echo Please run installgpt.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

:: Launch the application
echo ✅ Launching WebsiteNow...
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo    TIP: Don't close this window while using WebsiteNow!
echo.
echo    If you see any errors, they will appear here.
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

python main.py

:: If the program exits with an error
if errorlevel 1 (
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo    ❌ WebsiteNow exited with an error
    echo ═══════════════════════════════════════════════════════════════
    echo.
    echo    Troubleshooting:
    echo    - Check that all API keys are configured in Settings
    echo    - Verify internet connection
    echo    - Run installgpt.bat again if needed
    echo    - Check the error message above for details
    echo.
    pause
) else (
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo    👋 Thanks for using WebsiteNow!
    echo ═══════════════════════════════════════════════════════════════
    echo.
)
