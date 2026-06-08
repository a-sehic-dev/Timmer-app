@echo off
chcp 65001 >nul
echo ============================================
echo   PREMIUM TIMER APP — Windows Build
echo ============================================
echo.

:: Check Python
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Download from: https://python.org/downloads
    pause
    exit /b 1
)
echo      ✓ Python found
echo.

:: Install dependencies
echo [2/4] Installing dependencies...
pip install pyinstaller pillow -q
echo      ✓ Dependencies installed
echo.

:: Build .exe with icon
echo [3/4] Building TimerApp.exe with custom icon...
echo      This may take 1-2 minutes...
echo.

pyinstaller --onefile --noconsole --name "TimerApp" --icon "icon.ico" timer_app.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed. Check error messages above.
    pause
    exit /b 1
)

:: Move .exe to root folder
echo [4/4] Finalizing...
copy "dist\TimerApp.exe" "TimerApp.exe" >nul 2>&1
echo      ✓ TimerApp.exe created!
echo.

:: Cleanup
echo      Cleaning up build files...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del TimerApp.spec 2>nul
echo      ✓ Done!
echo.

echo ============================================
echo   BUILD COMPLETE!
echo   Double-click TimerApp.exe to run.
echo   No Python needed to run the .exe.
echo ============================================
echo.
pause
