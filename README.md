# PlaylistCat 🐱

*Catalog and explore your YouTube Music playlists*

A desktop application that fetches YouTube Music playlists and displays them in a sortable table format using a modern PyQt6 GUI interface.

## Features

- **Playlist Fetching**: Enter a YouTube Music playlist ID to fetch and display all tracks
- **Sortable Display**: Sort by Position, Artist, or Track Name
- **Direct Links**: Open any track directly in YouTube Music
- **Refresh Function**: Update the current playlist with fresh data
- **Modern GUI**: Clean Qt-based interface with mouse interaction
- **Standalone Packaging**: Create executables that run without Python installation

## Quick Start (Standalone)

**Download the latest release for your platform:**

[![Latest Release](https://img.shields.io/github/v/release/Makistos/playlistcat?style=for-the-badge)](https://github.com/Makistos/playlistcat/releases/latest)

### Windows
1. Download `playlistcat-windows-x64.zip`
2. Extract and run `run-gui.bat`

### macOS
1. Download `playlistcat-macos-x64.tar.gz`
2. Extract and run `./run-gui.sh`

### Linux
1. Download `playlistcat-linux-x64.tar.gz`
2. Extract and run `./run-gui.sh`

**No Python installation required!**

## Developer Installation

1. **Install Python 3.8+** if not already installed

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install ytmusicapi PyQt6 requests
   ```

## Usage

### Easy Launch (Recommended)
```bash
./run.sh           # Launch the application
```

### Manual Launch

#### GUI Application
```bash
# Make sure virtual environment is activated
source venv/bin/activate
python src/main.py
```

### Getting a Playlist ID
1. Go to YouTube Music
2. Open any playlist
3. Copy the playlist ID from the URL (the part after `list=`)
4. Example: `PLrAGlzNOGcAqFNKK0c4K8Z9U8QmFNKK0c`

### Using the Application
- Enter the playlist ID in the input field
- Click "Fetch Playlist" or press Enter
- Wait for the tracks to load
- Click column headers to sort
- Double-click any track to open in YouTube Music
- Use "Refresh" to update the current playlist

## Table Columns / Display Format

- **Position**: Original position in the playlist
- **Artist**: Track artist(s)
- **Track Name**: Name of the track
- **YouTube Music Link**: Click to open in browser

## Project Structure

```
playlistcat/
├── src/
│   ├── __init__.py       # Package initialization
│   ├── main.py           # GUI application (PyQt6)
│   └── utils.py          # Utility functions
├── venv/                 # Virtual environment
├── dist/                 # Built executables (after packaging)
├── requirements.txt      # Python dependencies
├── run.sh               # Launch script
├── build.sh/.bat        # Build standalone executables
├── test.py              # System test script
├── examples.py          # Example playlist IDs
├── PACKAGING.md         # Packaging guide
└── README.md            # This file
```## Notes

- The application fetches public playlists only
- Private playlists will show an error
- Large playlists may take a few moments to load
- Sorting is done locally for better performance

## Troubleshooting

**"Playlist not found or is private"**:
- Verify the playlist ID is correct
- Make sure the playlist is public
- Try copying the ID again from the YouTube Music URL

**Import errors**:
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're using Python 3.8 or higher

**GUI won't start**:
- Install missing system packages: `sudo apt install python3-pyqt6` (Ubuntu/Debian)
- Check that your system supports GUI applications

**Qt platform plugin errors**:
- Install xcb libraries: `sudo apt install libxcb-cursor0` (Ubuntu/Debian)
- For headless environments, consider using the application in a virtual display

## Requirements

- Python 3.8+
- PyQt6 (for GUI)
- ytmusicapi
- requests
- Internet connection

## Quick Start

1. **Clone and setup**:
   ```bash
   cd ytmcat
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Test the installation**:
   ```bash
   python test.py
   ```

3. **Run the application**:
   ```bash
   ./run.sh          # Launch PlaylistCat
   ```

4. **Try example playlists**:
   ```bash
   python examples.py
   ```

## ✅ Status: **Production Ready!** 🚀

- ✅ **Modern GUI**: PyQt6 interface fully functional
- ✅ **Standalone Packaging**: No Python required for end users
- ✅ **Cross-Platform**: Works on Linux, macOS, and Windows
- ✅ **Smart Launcher**: Easy to use
- ✅ **Comprehensive Testing**: All systems verified
- ✅ **Complete Documentation**: Setup, usage, and packaging guides
   ```bash
   python examples.py
   ```

## 📦 Standalone Packaging

Create executables that run on any machine without Python:

```bash
# Build standalone executables
./build.sh          # Linux/macOS
build.bat           # Windows

# Result: playlistcat(.exe)
# No Python installation required on target machines!
```

See [PACKAGING.md](PACKAGING.md) for detailed instructions.
