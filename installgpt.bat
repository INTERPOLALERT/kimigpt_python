@echo off
TITLE KimiGPT Desktop - Installation
COLOR 0A
cls

echo ═══════════════════════════════════════════════════════════════
echo    KIMIGPT DESKTOP - INSTALLATION WIZARD
echo ═══════════════════════════════════════════════════════════════
echo.
echo    Welcome to KimiGPT Desktop Installation!
echo    This will set up everything you need to start building websites with AI.
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
timeout /t 2 >nul

:: Change to script directory
cd /d "%~dp0"

:: Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.9 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python found!
echo.
timeout /t 1 >nul

:: Check Python version
echo [2/5] Verifying Python version...
python -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python 3.9 or higher is required!
    echo.
    echo Please update your Python installation.
    echo.
    pause
    exit /b 1
)
echo ✅ Python version OK!
echo.
timeout /t 1 >nul

:: Upgrade pip
echo [3/5] Upgrading pip...
python -m pip install --upgrade pip
echo ✅ pip upgraded!
echo.
timeout /t 1 >nul

:: Install requirements
echo [4/5] Installing required packages...
echo This may take a few minutes...
echo.
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Failed to install some packages!
    echo.
    echo Please check your internet connection and try again.
    echo.
    pause
    exit /b 1
)
echo.
echo ✅ All packages installed successfully!
echo.
timeout /t 1 >nul

:: Create directories
echo [5/5] Setting up directories...
if not exist "config" mkdir "config"
if not exist "output" mkdir "output"
if not exist "uploads" mkdir "uploads"
echo ✅ Directories created!
echo.

echo ═══════════════════════════════════════════════════════════════
echo    ✅ INSTALLATION COMPLETE!
echo ═══════════════════════════════════════════════════════════════
echo.
echo    Next Steps:
echo    -----------
echo.
echo    1. Get your FREE API keys:
echo       - Recommended: Groq, Gemini, Claude (all free!)
echo       - Visit provider websites for API keys
echo.
echo    2. Launch KimiGPT:
echo       - Double-click startgpt.bat
echo       - Or run: python main.py
echo.
echo    3. Configure APIs:
echo       - Click "⚙️ API Settings" tab
echo       - Paste your API keys
echo       - Click "Save API Keys"
echo.
echo    4. Start Building:
echo       - Click "🚀 Generator" tab
echo       - Describe your website
echo       - Generate!
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo    Ready to launch? Run startgpt.bat
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause
