# PlaylistCat 🐱

*Catalog and explore your YouTube Music playlists*

A desktop application that fetches YouTube Music playlists and displays them in a sortable table format. Available in both GUI (PyQt6) and CLI versions.

## Features

- **Playlist Fetching**: Enter a YouTube Music playlist ID to fetch and display all tracks
- **Sortable Display**: Sort by Position, Artist, or Track Name
- **Direct Links**: Open any track directly in YouTube Music
- **Refresh Function**: Update the current playlist with fresh data
- **Two Interfaces**: 
  - **GUI**: Clean Qt-based interface with mouse interaction
  - **CLI**: Command-line interface for headless environments

## Installation

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
./run.sh           # Auto-detects and launches appropriate version
./run.sh --cli     # Force CLI version
```

### Manual Launch

#### GUI Version
```bash
# Make sure virtual environment is activated
source venv/bin/activate
python src/main.py
```

#### CLI Version
```bash
# Make sure virtual environment is activated
source venv/bin/activate
python src/cli.py
```

### Getting a Playlist ID
1. Go to YouTube Music
2. Open any playlist
3. Copy the playlist ID from the URL (the part after `list=`)
4. Example: `PLrAGlzNOGcAqFNKK0c4K8Z9U8QmFNKK0c`

### Using the GUI Version
- Enter the playlist ID in the input field
- Click "Fetch Playlist" or press Enter
- Wait for the tracks to load
- Click column headers to sort
- Double-click any track to open in YouTube Music
- Use "Refresh" to update the current playlist

### Using the CLI Version
```
Commands:
  fetch <playlist_id>  - Fetch a playlist
  show [sort_by]       - Show tracks (sort_by: position, artist, title)  
  open <position>      - Open track at position in browser
  refresh              - Refresh current playlist
  quit                 - Exit
```

Example CLI session:
```
> fetch PLrAGlzNOGcAqFNKK0c4K8Z9U8QmFNKK0c
> show artist
> open 5
> quit
```

## Table Columns / Display Format

### GUI Version
- **Position**: Original position in the playlist
- **Artist**: Track artist(s) 
- **Track Name**: Name of the track
- **YouTube Music Link**: Click to open in browser

### CLI Version
Displays the same information in a formatted table with columns for position, artist, track name, and URL availability.

## Project Structure

```
ytmcat/
├── src/
│   ├── __init__.py       # Package initialization
│   ├── main.py           # GUI application (PyQt6)
│   ├── cli.py            # CLI application  
│   └── utils.py          # Utility functions
├── venv/                 # Virtual environment
├── requirements.txt      # Python dependencies
├── run.sh               # Launch script (auto-detects GUI/CLI)
├── test.py              # System test script
├── examples.py          # Example playlist IDs
└── README.md            # This file
```

## Notes

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
- Or use the CLI version: `./run.sh --cli`
- The launch script automatically falls back to CLI if GUI fails

**Qt platform plugin errors**:
- Install xcb libraries: `sudo apt install libxcb-cursor0` (Ubuntu/Debian)
- Or set `export QT_QPA_PLATFORM=offscreen` for headless mode
- The application will automatically use CLI mode if no display is available

## Requirements

- Python 3.8+
- PyQt6 (for GUI version)
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
   ./run.sh          # Auto-detects best version
   ./run.sh --cli    # Force CLI version
   ```

4. **Try example playlists**:
   ```bash
   python examples.py
   ```
