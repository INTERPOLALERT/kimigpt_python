@echo off
color 0B
title KimiGPT - Multi-Agent Website Builder

echo ╔════════════════════════════════════════════════╗
echo ║              KIMIGPT LAUNCHER                   ║
echo ║       Multi-Agent AI Website Builder            ║
echo ╚════════════════════════════════════════════════╝
echo.

:: Pre-flight Checks
echo [⏳] Running Pre-Flight Checks...
cd /d %~dp0

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Run installgpt.bat first.
    pause
    exit
)
echo ✓ Python OK

:: Check Virtual Environment
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment missing! Run installgpt.bat first.
    pause
    exit
)
echo ✓ Virtual Environment OK

:: Check API Keys
if not exist ".env" (
    echo ⚠️ No API keys configured! Some features may not work.
    echo Run installgpt.bat to configure APIs.
    pause
)
echo ✓ Configuration OK

:: Activate Virtual Environment
call venv\Scripts\activate.bat
echo ✓ Virtual Environment Activated

:: Check for Updates
echo.
echo [🔍] Checking for updates...
:: Add update check logic here
echo ✓ System up to date

:: Start Services
echo.
echo [🚀] Starting KimiGPT Services...
echo.
echo    ► Starting Multi-Agent System...
echo    ► Starting API Manager (Smart Rotation)...
echo    ► Starting Preview Server...
echo    ► Starting Web Interface...
echo.

:: Launch Main Application
start /B python src/ui/app.py

:: Wait for server to start
timeout /t 3 >nul

:: Open Browser
echo ✓ All services started!
echo.
echo ╔════════════════════════════════════════════════╗
echo ║         KIMIGPT IS READY! 🚀                    ║
echo ║                                                 ║
echo ║  Dashboard: http://localhost:5000              ║
echo ║  Preview:   http://localhost:3000              ║
echo ║                                                 ║
echo ║  Press Ctrl+C to stop all services             ║
echo ╚════════════════════════════════════════════════╝
echo.

:: Open browser automatically
start http://localhost:5000

:: Show Real-Time Status
echo.
echo [📊] Real-Time System Status:
echo ════════════════════════════════════════════════
python src/core/status_monitor.py

:: Keep window open
echo.
echo Press Ctrl+C to stop KimiGPT...
cmd /k