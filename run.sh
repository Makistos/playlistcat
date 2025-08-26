#!/bin/bash
# Launch script for PlaylistCat

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Start the GUI application
echo "Starting PlaylistCat..."
python "$SCRIPT_DIR/src/main.py"
