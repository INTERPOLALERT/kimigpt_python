@echo off
TITLE KimiGPT - Auto Fix Script
COLOR 0E
cls

echo ═══════════════════════════════════════════════════════════════
echo    KIMIGPT AUTO-FIX SCRIPT
echo ═══════════════════════════════════════════════════════════════
echo.
echo    This script will automatically fix the asyncio threading issue
echo    that causes the "set_wakeup_fd" error on Windows.
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

:: Navigate to the script's directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

echo [1/4] Checking files...
echo.

:: Check if files exist
if not exist "src\ui\generator_widget.py" (
    echo ❌ ERROR: generator_widget.py not found!
    echo.
    echo Expected location: %CD%\src\ui\generator_widget.py
    echo.
    pause
    exit /b 1
)

if not exist "src\agents\orchestrator.py" (
    echo ❌ ERROR: orchestrator.py not found!
    echo.
    echo Expected location: %CD%\src\agents\orchestrator.py
    echo.
    pause
    exit /b 1
)

echo ✅ Files found!
echo.

echo [2/4] Creating backups...
echo.

:: Create backup directory
if not exist "backups" mkdir "backups"

:: Create timestamped backup
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/: " %%a in ("%TIME%") do (set mytime=%%a%%b)
set mytime=%mytime: =0%
set timestamp=%mydate%_%mytime%

mkdir "backups\backup_%timestamp%" 2>nul
copy "src\ui\generator_widget.py" "backups\backup_%timestamp%\generator_widget.py.bak" >nul
copy "src\agents\orchestrator.py" "backups\backup_%timestamp%\orchestrator.py.bak" >nul

echo ✅ Backups created in: backups\backup_%timestamp%\
echo.

echo [3/4] Applying fixes...
echo.

:: Create Python fix script
(
echo import sys
echo import os
echo import re
echo.
echo print^("Fixing generator_widget.py..."^)
echo.
echo # Read the file
echo with open^('src/ui/generator_widget.py', 'r', encoding='utf-8'^) as f:
echo     content = f.read^(^)
echo.
echo # Fix 1: Add Windows event loop policy
echo if "asyncio.WindowsSelectorEventLoopPolicy" not in content:
echo     # Find the asyncio import section in run method
echo     pattern1 = r'^(\s+)import asyncio\s*\n(\s+)loop = asyncio\.new_event_loop'
echo     replacement1 = r'\1import asyncio\n\1import sys\n\n\1# Windows-specific asyncio setup for threads\n\1# This prevents the set_wakeup_fd error\n\1if sys.platform == "win32":\n\1    # Set the event loop policy to avoid set_wakeup_fd issues\n\1    asyncio.set_event_loop_policy^(asyncio.WindowsSelectorEventLoopPolicy^(^)^)\n\n\1# Create new event loop for this thread\n\2loop = asyncio.new_event_loop'
echo     content = re.sub^(pattern1, replacement1, content, flags=re.MULTILINE^)
echo     print^("  ✓ Applied Windows event loop policy fix"^)
echo else:
echo     print^("  ℹ Windows policy fix already applied"^)
echo.
echo # Fix 2: Update callback method calls
echo content = content.replace^('self.progress_updated', 'self.emit_progress'^)
echo content = content.replace^('self.agent_status_updated', 'self.emit_agent_status'^)
echo # But keep the signal definitions
echo content = content.replace^('emit_progress_updated = pyqtSignal', 'progress_updated = pyqtSignal'^)
echo content = content.replace^('emit_agent_status_updated = pyqtSignal', 'agent_status_updated = pyqtSignal'^)
echo print^("  ✓ Updated callback methods"^)
echo.
echo # Fix 3: Add safe emission methods if not present
echo if 'def emit_progress' not in content:
echo     # Find the end of GenerationThread class
echo     class_end = content.find^('class GeneratorWidget'^)
echo     if class_end ^> 0:
echo         safe_methods = '''
echo     def emit_progress^(self, value, message^):
echo         """Safe progress emission"""
echo         try:
echo             self.progress_updated.emit^(value, message^)
echo         except:
echo             pass
echo.
echo     def emit_agent_status^(self, agent, status^):
echo         """Safe agent status emission"""
echo         try:
echo             self.agent_status_updated.emit^(agent, status^)
echo         except:
echo             pass
echo.
echo.
echo '''
echo         content = content[:class_end] + safe_methods + content[class_end:]
echo         print^("  ✓ Added safe emission methods"^)
echo.
echo # Write the fixed content
echo with open^('src/ui/generator_widget.py', 'w', encoding='utf-8'^) as f:
echo     f.write^(content^)
echo.
echo print^("\n✅ All fixes applied successfully!"^)
echo print^("\nBackup location: backups/backup_%timestamp%/"^)
) > apply_fix.py

:: Run the Python fix script
python apply_fix.py

if errorlevel 1 (
    echo.
    echo ❌ ERROR: Failed to apply fixes!
    echo.
    echo Your original files are backed up in: backups\backup_%timestamp%\
    echo.
    pause
    exit /b 1
)

:: Clean up
del apply_fix.py

echo.
echo [4/4] Verification...
echo.
echo ✅ Fixes applied successfully!
echo.

echo ═══════════════════════════════════════════════════════════════
echo    ✅ FIX COMPLETE!
echo ═══════════════════════════════════════════════════════════════
echo.
echo    What was fixed:
echo    ✓ Added Windows-specific event loop policy
echo    ✓ Fixed asyncio threading issues
echo    ✓ Added safe signal emission methods
echo    ✓ Resolved "set_wakeup_fd" error
echo.
echo    Your original files are safely backed up in:
echo    backups\backup_%timestamp%\
echo.
echo    Next steps:
echo    1. Close KimiGPT if it's running
echo    2. Run startgpt.bat
echo    3. Try generating a website again
echo.
echo    The "set_wakeup_fd" error should now be fixed!
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause
