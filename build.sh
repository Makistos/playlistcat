#!/bin/bash
# Build script for PlaylistCat standalone executables

echo "🐱 PlaylistCat - Build Script"
echo "============================="

# Set environment variables for headless builds
export QT_QPA_PLATFORM=offscreen
export QT_LOGGING_RULES="*.debug=false;qt.qpa.*=false"

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not activated. Activating..."
    source venv/bin/activate
fi

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install pyinstaller || {
    echo "❌ Failed to install pyinstaller"
    exit 1
}

# Create assets directory and placeholder icon
mkdir -p assets
if [ ! -f "assets/icon.ico" ]; then
    echo "💡 No icon found. Creating placeholder..."
    # You can replace this with a real icon file
    touch assets/icon.ico
fi

# Build for current platform
echo "🔨 Building PlaylistCat executables..."

# Clean previous builds
rm -rf build dist

# Build GUI version
echo "🖥️  Building GUI version..."
pyinstaller --onefile --windowed --name playlistcat \
    --paths src \
    --add-data "README.md:." \
    --add-data "src/utils.py:." \
    --add-data "src/auth.py:." \
    --hidden-import PyQt6.QtCore \
    --hidden-import PyQt6.QtGui \
    --hidden-import PyQt6.QtWidgets \
    --hidden-import ytmusicapi \
    --hidden-import requests \
    --strip \
    --noupx \
    src/main.py || {
    echo "❌ GUI build failed"
    exit 1
}

# Create distribution package
echo "📁 Creating distribution package..."
mkdir -p release
cp dist/* release/ 2>/dev/null || true
cp README.md release/
cp LICENSE release/
cp examples.py release/

# Create launcher script for the release
cat > release/run-gui.sh << 'EOF'
#!/bin/bash
# PlaylistCat GUI Launcher
./playlistcat
EOF

cat > release/run-gui.bat << 'EOF'
@echo off
REM PlaylistCat GUI Launcher for Windows
playlistcat.exe
EOF

chmod +x release/*.sh

echo "✅ Build complete!"
echo ""
echo "📦 Distribution files created in 'release/' directory:"
ls -la release/
echo ""
echo "🚀 To distribute:"
echo "   - Copy the 'release/' folder to target machines"
echo "   - On Linux/Mac: Run ./run-gui.sh"
echo "   - On Windows: Run run-gui.bat"
echo ""
echo "💡 For cross-platform builds, run this script on each target OS"
