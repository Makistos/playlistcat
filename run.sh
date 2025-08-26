#!/bin/bash
# Launch script for PlaylistCat

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Check if GUI or CLI version should be used
if [ "$1" = "--cli" ] || [ "$1" = "-c" ]; then
    echo "Starting CLI version..."
    python "$SCRIPT_DIR/src/cli.py"
elif [ "$DISPLAY" = "" ]; then
    echo "No display detected, starting CLI version..."
    python "$SCRIPT_DIR/src/cli.py"
else
    echo "Starting GUI version..."
    python "$SCRIPT_DIR/src/main.py" 2>/dev/null || {
        echo "GUI failed to start, falling back to CLI version..."
        python "$SCRIPT_DIR/src/cli.py"
    }
fi
