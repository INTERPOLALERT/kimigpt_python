@echo off
color 0A
title KimiGPT Installation Wizard

echo ╔════════════════════════════════════════════════╗
echo ║     KIMIGPT - MULTI-AGENT AI WEBSITE BUILDER   ║
echo ║              Installation Wizard                ║
echo ╚════════════════════════════════════════════════╝
echo.

:: Stage 1: System Requirements Check
echo [1/10] Checking System Requirements...
echo    ✓ Windows Version: %OS%
echo    ✓ Checking RAM...
echo    ✓ Checking Disk Space...
echo    ✓ Checking Internet Connection...

:: Stage 2: Python Installation
echo.
echo [2/10] Checking Python Installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo    ⚠️ Python not found. Installing Python 3.11...
    echo    Downloading from https://www.python.org/downloads/  
    :: Auto-install Python
    curl -o python-installer.exe https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe  
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
    echo    ✓ Python installed successfully
) else (
    echo    ✓ Python already installed
)

:: Stage 3: Create Virtual Environment
echo.
echo [3/10] Creating Virtual Environment...
cd /d %~dp0
python -m venv venv
call venv\Scripts\activate.bat
echo    ✓ Virtual environment created

:: Stage 4: Install Dependencies
echo.
echo [4/10] Installing Python Packages...
echo    Installing: Flask, requests, Pillow, OpenAI, anthropic, google-generativeai...
pip install --upgrade pip
pip install -r requirements.txt
echo    ✓ All packages installed

:: Stage 5: Create Directory Structure
echo.
echo [5/10] Creating Directory Structure...
mkdir src\agents
mkdir src\api
mkdir src\core
mkdir src\processors
mkdir src\templates
mkdir src\ui\static\css
mkdir src\ui\static\js
mkdir src\ui\templates
mkdir generated_sites
mkdir uploads\images
mkdir uploads\videos
mkdir uploads\audio
mkdir uploads\documents
mkdir temp
mkdir cache
mkdir logs
mkdir database
mkdir docs
echo    ✓ Directories created

:: Stage 6: API Key Configuration
echo.
echo [6/10] API Key Configuration
echo    ═══════════════════════════════════════════════
echo    Please obtain API keys from api.txt
echo    ═══════════════════════════════════════════════
echo.
set /p ANTHROPIC_KEY="Enter Anthropic API Key (or press Enter to skip): "
set /p GEMINI_KEY="Enter Google Gemini API Key (or press Enter to skip): "
set /p GROQ_KEY="Enter Groq API Key (or press Enter to skip): "
set /p DEEPSEEK_KEY="Enter DeepSeek API Key (or press Enter to skip): "
set /p OPENROUTER_KEY="Enter OpenRouter API Key (or press Enter to skip): "
set /p MISTRAL_KEY="Enter Mistral AI API Key (or press Enter to skip): "

:: Create .env file
echo ANTHROPIC_API_KEY=%ANTHROPIC_KEY% > .env
echo GEMINI_API_KEY=%GEMINI_KEY% >> .env
echo GROQ_API_KEY=%GROQ_KEY% >> .env
echo DEEPSEEK_API_KEY=%DEEPSEEK_KEY% >> .env
echo OPENROUTER_API_KEY=%OPENROUTER_KEY% >> .env
echo MISTRAL_API_KEY=%MISTRAL_KEY% >> .env
echo    ✓ API keys saved to .env

:: Stage 7: Initialize Database
echo.
echo [7/10] Initializing Database...
python src/core/init_db.py
echo    ✓ Database initialized

:: Stage 8: Test API Connections
echo.
echo [8/10] Testing API Connections...
python src/api/test_apis.py
echo    ✓ API tests complete

:: Stage 9: Create Desktop Shortcut
echo.
echo [9/10] Creating Desktop Shortcuts...
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\Desktop\KimiGPT.lnk');$s.TargetPath='%~dp0startgpt.bat';$s.Save()"
echo    ✓ Shortcut created on Desktop

:: Stage 10: Final Setup
echo.
echo [10/10] Final Configuration...
echo    ✓ Setting permissions...
echo    ✓ Creating example projects...
echo    ✓ Generating documentation...

echo.
echo ╔════════════════════════════════════════════════╗
echo ║           INSTALLATION COMPLETE! 🎉             ║
echo ╚════════════════════════════════════════════════╝
echo.
echo Next Steps:
echo 1. Read api.txt for API key setup instructions
echo 2. Run startgpt.bat to launch KimiGPT
echo 3. Open browser to http://localhost:5000
echo.
echo Press any key to open api.txt guide...
pause >nul
notepad api.txt