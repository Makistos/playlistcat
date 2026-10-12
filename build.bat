@echo off
REM Build script for PlaylistCat standalone executables (Windows)

echo 🐱 PlaylistCat - Windows Build Script
echo =====================================

REM Check if virtual environment exists
if not exist "venv" (
    echo ⚠️ Virtual environment not found. Creating...
    python -m venv venv
)

REM Activate virtual environment
echo 📦 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

REM Create assets directory
if not exist "assets" mkdir assets
if not exist "assets\icon.ico" (
    echo 💡 No icon found. You can add an icon.ico file in assets\ directory
)

REM Clean previous builds
echo 🧹 Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Build executables
echo 🔨 Building PlaylistCat executables...

echo ⌨️ Building GUI version...
pyinstaller --onefile --windowed --name playlistcat ^
    --paths src ^
    --add-data "README.md;." ^
    --add-data "src\utils.py;." ^
    --add-data "src\auth.py;." ^
    --hidden-import PyQt6.QtCore ^
    --hidden-import PyQt6.QtGui ^
    --hidden-import PyQt6.QtWidgets ^
    --hidden-import ytmusicapi ^
    --hidden-import requests ^
    src\main.py

if %ERRORLEVEL% neq 0 (
    echo ❌ GUI build failed
    exit /b 1
)

REM Create release directory
echo 📁 Creating release package...
if not exist "release" mkdir release

echo 🔍 Checking what was built in dist directory...
dir dist

echo 📋 Copying executables...
if exist "dist\playlistcat.exe" (
    copy "dist\playlistcat.exe" "release\" >nul 2>&1
    echo ✅ Copied playlistcat.exe
) else if exist "dist\playlistcat" (
    copy "dist\playlistcat" "release\playlistcat.exe" >nul 2>&1
    echo ✅ Copied playlistcat as playlistcat.exe
) else (
    echo ❌ No GUI executable found in dist directory
    exit /b 1
)

copy README.md release\ >nul 2>&1
copy LICENSE release\ >nul 2>&1
copy examples.py release\ >nul 2>&1

REM Create Windows batch launcher
echo @echo off > release\run-gui.bat
echo REM PlaylistCat GUI Launcher >> release\run-gui.bat
echo playlistcat.exe >> release\run-gui.bat

echo ✅ Build complete!
echo.
echo 📦 Distribution files created in 'release\' directory:
dir release
echo.
echo 🚀 To distribute:
echo    - Copy the 'release\' folder to target machines
echo    - Double-click run-gui.bat to start PlaylistCat
echo.
echo 💡 No Python installation required on target machines!

REM Don't pause in CI environment
if defined CI (
    echo Build completed in CI environment
) else (
    pause
)
