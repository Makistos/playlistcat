#!/bin/bash
# Build PlaylistCat as AppImage for maximum Linux compatibility

echo "🐱 PlaylistCat - AppImage Build Script"
echo "======================================="

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ AppImage can only be built on Linux"
    exit 1
fi

# Install dependencies
echo "📦 Installing build dependencies..."
pip install pyinstaller

# Create AppDir structure
echo "📁 Creating AppDir structure..."
rm -rf AppDir
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps

# Build with PyInstaller
echo "🔨 Building with PyInstaller..."
pyinstaller --onedir --windowed --name playlistcat \
    --distpath AppDir/usr/bin \
    --add-data "README.md:." \
    --add-data "src/utils.py:." \
    --hidden-import PyQt6.QtCore \
    --hidden-import PyQt6.QtGui \
    --hidden-import PyQt6.QtWidgets \
    --hidden-import ytmusicapi \
    --hidden-import requests \
    src/main.py

# Create desktop file
cat > AppDir/usr/share/applications/playlistcat.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=PlaylistCat
Comment=YouTube Music Playlist Manager
Exec=playlistcat
Icon=playlistcat
Categories=AudioVideo;Audio;Music;
EOF

# Create a simple icon (placeholder)
cat > AppDir/usr/share/icons/hicolor/256x256/apps/playlistcat.png << 'EOF'
# This would be a PNG file - for now just a placeholder
EOF

# Create AppRun script
cat > AppDir/AppRun << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
exec "${HERE}/usr/bin/playlistcat/playlistcat" "$@"
EOF

chmod +x AppDir/AppRun

# Download appimagetool if not present
if [ ! -f appimagetool-x86_64.AppImage ]; then
    echo "⬇️  Downloading appimagetool..."
    wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x appimagetool-x86_64.AppImage
fi

# Build AppImage
echo "📦 Building AppImage..."
./appimagetool-x86_64.AppImage AppDir playlistcat-x86_64.AppImage

echo "✅ AppImage build complete!"
echo "📦 File: playlistcat-x86_64.AppImage"
echo "🚀 To run: ./playlistcat-x86_64.AppImage"
