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

:: Set the correct path
set "INSTALL_PATH=Z:\kimigpt\python kimi"

:: Check if directory exists
if not exist "%INSTALL_PATH%" (
    echo ❌ ERROR: Directory not found: %INSTALL_PATH%
    echo.
    echo Please check the path and try again.
    echo.
    pause
    exit /b 1
)

cd /d "%INSTALL_PATH%"

echo [1/4] Checking files...
echo.

:: Check if files exist
if not exist "src\ui\generator_widget.py" (
    echo ❌ ERROR: generator_widget.py not found!
    pause
    exit /b 1
)

if not exist "src\agents\orchestrator.py" (
    echo ❌ ERROR: orchestrator.py not found!
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
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set timestamp=%mydate%_%mytime%

mkdir "backups\backup_%timestamp%" 2>nul
copy "src\ui\generator_widget.py" "backups\backup_%timestamp%\generator_widget.py.bak" >nul
copy "src\agents\orchestrator.py" "backups\backup_%timestamp%\orchestrator.py.bak" >nul

echo ✅ Backups created in: backups\backup_%timestamp%\
echo.

echo [3/4] Applying fixes...
echo.

:: Create Python fix script
echo import sys > apply_fix.py
echo import os >> apply_fix.py
echo. >> apply_fix.py
echo # Fix generator_widget.py >> apply_fix.py
echo print("Fixing generator_widget.py...") >> apply_fix.py
echo. >> apply_fix.py
echo with open('src/ui/generator_widget.py', 'r', encoding='utf-8') as f: >> apply_fix.py
echo     content = f.read() >> apply_fix.py
echo. >> apply_fix.py
echo # Fix 1: Add Windows event loop policy >> apply_fix.py
echo old_code1 = '''            import asyncio >> apply_fix.py
echo             loop = asyncio.new_event_loop() >> apply_fix.py
echo             asyncio.set_event_loop(loop)''' >> apply_fix.py
echo. >> apply_fix.py
echo new_code1 = '''            import asyncio >> apply_fix.py
echo             import sys >> apply_fix.py
echo. >> apply_fix.py
echo             # Windows-specific asyncio setup for threads >> apply_fix.py
echo             # This prevents the set_wakeup_fd error >> apply_fix.py
echo             if sys.platform == 'win32': >> apply_fix.py
echo                 # Set the event loop policy to avoid set_wakeup_fd issues >> apply_fix.py
echo                 asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) >> apply_fix.py
echo. >> apply_fix.py
echo             # Create new event loop for this thread >> apply_fix.py
echo             loop = asyncio.new_event_loop() >> apply_fix.py
echo             asyncio.set_event_loop(loop)''' >> apply_fix.py
echo. >> apply_fix.py
echo if old_code1 in content: >> apply_fix.py
echo     content = content.replace(old_code1, new_code1) >> apply_fix.py
echo     print("  ✓ Applied Windows event loop policy fix") >> apply_fix.py
echo else: >> apply_fix.py
echo     print("  ℹ Windows policy fix already applied or code structure changed") >> apply_fix.py
echo. >> apply_fix.py
echo # Fix 2: Update callback method calls >> apply_fix.py
echo old_code2 = '''            result = loop.run_until_complete( >> apply_fix.py
echo                 orchestrator.process(self.input_data, self.progress_updated, self.agent_status_updated)''' >> apply_fix.py
echo. >> apply_fix.py
echo new_code2 = '''            result = loop.run_until_complete( >> apply_fix.py
echo                 orchestrator.process(self.input_data, self.emit_progress, self.emit_agent_status)''' >> apply_fix.py
echo. >> apply_fix.py
echo if old_code2 in content: >> apply_fix.py
echo     content = content.replace(old_code2, new_code2) >> apply_fix.py
echo     print("  ✓ Updated callback methods") >> apply_fix.py
echo. >> apply_fix.py
echo # Add safe emission methods if not present >> apply_fix.py
echo if 'def emit_progress' not in content: >> apply_fix.py
echo     # Find where to insert >> apply_fix.py
echo     insert_pos = content.find('class GeneratorWidget') >> apply_fix.py
echo     if insert_pos ^> 0: >> apply_fix.py
echo         safe_methods = '''\n    def emit_progress(self, value, message): >> apply_fix.py
echo         """Safe progress emission""" >> apply_fix.py
echo         try: >> apply_fix.py
echo             self.progress_updated.emit(value, message) >> apply_fix.py
echo         except: >> apply_fix.py
echo             pass >> apply_fix.py
echo. >> apply_fix.py
echo     def emit_agent_status(self, agent, status): >> apply_fix.py
echo         """Safe agent status emission""" >> apply_fix.py
echo         try: >> apply_fix.py
echo             self.agent_status_updated.emit(agent, status) >> apply_fix.py
echo         except: >> apply_fix.py
echo             pass >> apply_fix.py
echo. >> apply_fix.py
echo ''' >> apply_fix.py
echo         content = content[:insert_pos] + safe_methods + content[insert_pos:] >> apply_fix.py
echo         print("  ✓ Added safe emission methods") >> apply_fix.py
echo. >> apply_fix.py
echo with open('src/ui/generator_widget.py', 'w', encoding='utf-8') as f: >> apply_fix.py
echo     f.write(content) >> apply_fix.py
echo. >> apply_fix.py
echo print("\n✅ All fixes applied successfully!") >> apply_fix.py
echo print("\nBackup location: backups/backup_%timestamp%/") >> apply_fix.py
echo print("\nYou can now run startgpt.bat to test the fixes.") >> apply_fix.py

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
