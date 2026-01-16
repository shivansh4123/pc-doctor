@echo off
REM PC Doctor Build Script
REM Builds executable and installer

echo ========================================
echo   PC Doctor - Automated Build Script
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

REM Install/Update PyInstaller
echo [1/5] Installing PyInstaller...
pip install pyinstaller packaging --quiet

REM Clean previous builds
echo [2/5] Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

REM Build executable
echo [3/5] Building executable...
pyinstaller --onefile ^
    --windowed ^
    --name PCDoctor ^
    --icon=icon.ico ^
    --add-data "templates;templates" ^
    app.py

if errorlevel 1 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo [4/5] Testing executable...
cd dist
start PCDoctor.exe
timeout /t 5 >nul
taskkill /f /im PCDoctor.exe >nul 2>&1
cd ..

echo [5/5] Build complete!
echo.
echo ========================================
echo  Executable: dist\PCDoctor.exe
echo  Size: 
dir dist\PCDoctor.exe | find "PCDoctor.exe"
echo ========================================
echo.

REM Inno Setup check
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo.
    choice /m "Build installer with Inno Setup?"
    if errorlevel 2 goto skip_installer
    if errorlevel 1 goto build_installer
) else (
    echo.
    echo NOTE: Inno Setup not found
    echo Install from: https://jrsoftware.org/isdl.php
    goto skip_installer
)

:build_installer
echo.
echo Building installer...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
echo.
echo Installer: output\PCDoctor_Setup.exe
goto end

:skip_installer
echo.
echo Skipping installer build.

:end
echo.
echo ========================================
echo  Build complete! Ready to distribute.
echo ========================================
pause
