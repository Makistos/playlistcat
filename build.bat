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

echo 🖥️ Building GUI version...
pyinstaller --onefile --windowed --name playlistcat ^
    --add-data "README.md;." ^
    --add-data "src\utils.py;." ^
    --hidden-import PyQt6.QtCore ^
    --hidden-import PyQt6.QtGui ^
    --hidden-import PyQt6.QtWidgets ^
    --hidden-import ytmusicapi ^
    --hidden-import requests ^
    src\main.py

echo ⌨️ Building CLI version...
pyinstaller --onefile --console --name playlistcat-cli ^
    --add-data "README.md;." ^
    --add-data "src\utils.py;." ^
    --hidden-import ytmusicapi ^
    --hidden-import requests ^
    --exclude-module PyQt6 ^
    src\cli.py

REM Create release directory
echo 📁 Creating release package...
if not exist "release" mkdir release
copy dist\*.exe release\ >nul 2>&1
copy README.md release\ >nul 2>&1
copy LICENSE release\ >nul 2>&1
copy examples.py release\ >nul 2>&1

REM Create Windows batch launchers
echo @echo off > release\run-gui.bat
echo REM PlaylistCat GUI Launcher >> release\run-gui.bat
echo playlistcat.exe >> release\run-gui.bat

echo @echo off > release\run-cli.bat
echo REM PlaylistCat CLI Launcher >> release\run-cli.bat
echo playlistcat-cli.exe >> release\run-cli.bat

echo ✅ Build complete!
echo.
echo 📦 Distribution files created in 'release\' directory:
dir release
echo.
echo 🚀 To distribute:
echo    - Copy the 'release\' folder to target machines
echo    - Double-click run-gui.bat for GUI version
echo    - Double-click run-cli.bat for CLI version
echo.
echo 💡 No Python installation required on target machines!

pause
