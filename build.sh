#!/bin/bash
# Build script for PlaylistCat standalone executables

echo "🐱 PlaylistCat - Build Script"
echo "============================="

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not activated. Activating..."
    source venv/bin/activate
fi

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install pyinstaller

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

# Build both GUI and CLI versions
echo "🖥️  Building GUI version..."
pyinstaller --onefile --windowed --name playlistcat \
    --add-data "README.md:." \
    --add-data "src/utils.py:." \
    --hidden-import PyQt6.QtCore \
    --hidden-import PyQt6.QtGui \
    --hidden-import PyQt6.QtWidgets \
    --hidden-import ytmusicapi \
    --hidden-import requests \
    src/main.py

echo "⌨️  Building CLI version..."
pyinstaller --onefile --console --name playlistcat-cli \
    --add-data "README.md:." \
    --add-data "src/utils.py:." \
    --hidden-import ytmusicapi \
    --hidden-import requests \
    --exclude-module PyQt6 \
    src/cli.py

# Create distribution package
echo "📁 Creating distribution package..."
mkdir -p release
cp dist/* release/ 2>/dev/null || true
cp README.md release/
cp LICENSE release/
cp examples.py release/

# Create launcher scripts for the release
cat > release/run-gui.sh << 'EOF'
#!/bin/bash
# PlaylistCat GUI Launcher
./playlistcat
EOF

cat > release/run-cli.sh << 'EOF'
#!/bin/bash
# PlaylistCat CLI Launcher
./playlistcat-cli
EOF

cat > release/run-gui.bat << 'EOF'
@echo off
REM PlaylistCat GUI Launcher for Windows
playlistcat.exe
EOF

cat > release/run-cli.bat << 'EOF'
@echo off
REM PlaylistCat CLI Launcher for Windows
playlistcat-cli.exe
EOF

chmod +x release/*.sh

echo "✅ Build complete!"
echo ""
echo "📦 Distribution files created in 'release/' directory:"
ls -la release/
echo ""
echo "🚀 To distribute:"
echo "   - Copy the 'release/' folder to target machines"
echo "   - On Linux/Mac: Run ./run-gui.sh or ./run-cli.sh"
echo "   - On Windows: Run run-gui.bat or run-cli.bat"
echo ""
echo "💡 For cross-platform builds, run this script on each target OS"
