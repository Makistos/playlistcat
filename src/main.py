#!/usr/bin/env python3
"""
PlaylistCat - Catalog and explore your YouTube Music playlists
A Qt application to fetch and display YouTube Music playlists with sorting capabilities.
"""

import sys
import webbrowser
import os
from typing import List, Dict, Any, Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QProgressBar, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon
from ytmusicapi import YTMusic

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from utils import extract_playlist_id, validate_playlist_id
except ImportError:
    # Fallback if utils module is not found
    def extract_playlist_id(input_string):
        if not input_string:
            return None
        input_string = input_string.strip()
        if 'list=' in input_string:
            return input_string.split('list=')[1].split('&')[0]
        return input_string

    def validate_playlist_id(playlist_id):
        return playlist_id and playlist_id.startswith('PL') and len(playlist_id) > 10

import sys
import webbrowser
from typing import List, Dict, Any, Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QProgressBar, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon
from ytmusicapi import YTMusic

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from utils import extract_playlist_id, validate_playlist_id
except ImportError:
    # Fallback if utils module is not found
    def extract_playlist_id(input_string):
        if not input_string:
            return None
        input_string = input_string.strip()
        if 'list=' in input_string:
            return input_string.split('list=')[1].split('&')[0]
        return input_string

    def validate_playlist_id(playlist_id):
        return playlist_id and playlist_id.startswith('PL') and len(playlist_id) > 10


class PlaylistFetcher(QThread):
    """Background thread for fetching playlist data from YouTube Music."""

    data_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    progress_update = pyqtSignal(str)

    def __init__(self, playlist_id: str):
        super().__init__()
        self.playlist_id = playlist_id
        self.ytmusic = None

    def run(self):
        """Fetch playlist data in background thread."""
        try:
            self.progress_update.emit("Initializing YouTube Music API...")
            self.ytmusic = YTMusic()

            self.progress_update.emit("Fetching playlist data...")
            playlist_data = self.ytmusic.get_playlist(self.playlist_id)

            if not playlist_data:
                self.error_occurred.emit("Playlist not found or is private")
                return

            self.progress_update.emit("Processing tracks...")
            tracks = []

            for i, track in enumerate(playlist_data.get('tracks', []), 1):
                if track is None:
                    continue

                # Extract track information
                title = track.get('title', 'Unknown Title')
                artists = []

                # Handle artists list
                if 'artists' in track and track['artists']:
                    artists = [artist.get('name', '') for artist in track['artists'] if artist]

                artist_str = ', '.join(artists) if artists else 'Unknown Artist'

                # Create YouTube Music URL
                video_id = track.get('videoId', '')
                youtube_url = f"https://music.youtube.com/watch?v={video_id}" if video_id else ""

                tracks.append({
                    'position': i,
                    'artist': artist_str,
                    'title': title,
                    'url': youtube_url,
                    'video_id': video_id
                })

            self.progress_update.emit(f"Found {len(tracks)} tracks")
            self.data_ready.emit(tracks)

        except Exception as e:
            self.error_occurred.emit(f"Error fetching playlist: {str(e)}")


class YouTubeMusicPlaylistViewer(QMainWindow):
    """Main application window for YouTube Music Playlist Viewer."""

    def __init__(self):
        super().__init__()
        self.tracks_data = []
        self.current_sort_column = 0
        self.current_sort_order = Qt.SortOrder.AscendingOrder
        self.fetcher_thread = None

        self.init_ui()
        self.setWindowTitle("PlaylistCat - YouTube Music Playlist Viewer")
        self.resize(1000, 600)

    def init_ui(self):
        """Initialize the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title_label = QLabel("PlaylistCat 🐱")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Input section
        input_frame = QFrame()
        input_frame.setFrameStyle(QFrame.Shape.Box)
        input_layout = QHBoxLayout(input_frame)

        input_layout.addWidget(QLabel("Playlist ID:"))

        self.playlist_input = QLineEdit()
        self.playlist_input.setPlaceholderText("Enter YouTube Music playlist ID (e.g., PLrAGlzNOGcAqFNKK0c4K8Z9U8QmFNKK0c)")
        self.playlist_input.returnPressed.connect(self.fetch_playlist)
        input_layout.addWidget(self.playlist_input)

        self.fetch_button = QPushButton("Fetch Playlist")
        self.fetch_button.clicked.connect(self.fetch_playlist)
        input_layout.addWidget(self.fetch_button)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_playlist)
        self.refresh_button.setEnabled(False)
        input_layout.addWidget(self.refresh_button)

        layout.addWidget(input_frame)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Enter a playlist ID to get started")
        self.status_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.status_label)

        # Table
        self.create_table()
        layout.addWidget(self.table)

        # Instructions
        instructions = QLabel(
            "Instructions:\n"
            "• Enter a YouTube Music playlist ID and click 'Fetch Playlist'\n"
            "• Click column headers to sort by Position, Artist, or Track Name\n"
            "• Double-click any row to open the track in YouTube Music"
        )
        instructions.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(instructions)

    def create_table(self):
        """Create and configure the tracks table."""
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Position", "Artist", "Track Name", "YouTube Music Link"])

        # Configure table appearance
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Position
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)        # Artist
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)           # Track Name
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Link

        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSortingEnabled(False)  # Disable built-in sorting, use custom logic

        # Connect double-click to open URL
        self.table.itemDoubleClicked.connect(self.open_track_url)

        # Connect header clicks for custom sorting
        header.sectionClicked.connect(self.sort_table)

    def fetch_playlist(self):
        """Fetch playlist data from YouTube Music."""
        playlist_id = self.playlist_input.text().strip()

        if not playlist_id:
            QMessageBox.warning(self, "Warning", "Please enter a playlist ID")
            return

        # Clean playlist ID (remove URL parts if user pasted full URL)
        playlist_id = extract_playlist_id(playlist_id)

        if not playlist_id or not validate_playlist_id(playlist_id):
            QMessageBox.warning(self, "Warning", "Invalid playlist ID format")
            return

        self.start_fetch(playlist_id)

    def refresh_playlist(self):
        """Refresh the current playlist."""
        playlist_id = self.playlist_input.text().strip()
        if playlist_id:
            playlist_id = extract_playlist_id(playlist_id)
            if playlist_id and validate_playlist_id(playlist_id):
                self.start_fetch(playlist_id)

    def start_fetch(self, playlist_id: str):
        """Start the background fetch process."""
        if self.fetcher_thread and self.fetcher_thread.isRunning():
            self.fetcher_thread.terminate()
            self.fetcher_thread.wait()

        # Update UI for loading state
        self.fetch_button.setEnabled(False)
        self.refresh_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.status_label.setText("Fetching playlist...")

        # Start background thread
        self.fetcher_thread = PlaylistFetcher(playlist_id)
        self.fetcher_thread.data_ready.connect(self.on_data_ready)
        self.fetcher_thread.error_occurred.connect(self.on_error)
        self.fetcher_thread.progress_update.connect(self.on_progress_update)
        self.fetcher_thread.start()

    def on_data_ready(self, tracks: List[Dict[str, Any]]):
        """Handle successful data fetch."""
        self.tracks_data = tracks
        self.populate_table()

        # Update UI
        self.fetch_button.setEnabled(True)
        self.refresh_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Loaded {len(tracks)} tracks")

    def on_error(self, error_message: str):
        """Handle fetch error."""
        QMessageBox.critical(self, "Error", error_message)

        # Reset UI
        self.fetch_button.setEnabled(True)
        self.refresh_button.setEnabled(bool(self.playlist_input.text().strip()))
        self.progress_bar.setVisible(False)
        self.status_label.setText("Error occurred while fetching playlist")

    def on_progress_update(self, message: str):
        """Update progress status."""
        self.status_label.setText(message)

    def populate_table(self):
        """Populate the table with track data."""
        self.table.setRowCount(len(self.tracks_data))

        for row, track in enumerate(self.tracks_data):
            # Position
            pos_item = QTableWidgetItem(str(track['position']))
            pos_item.setData(Qt.ItemDataRole.UserRole, track['position'])
            pos_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, pos_item)

            # Artist
            artist_item = QTableWidgetItem(track['artist'])
            artist_item.setData(Qt.ItemDataRole.UserRole, track['artist'])
            self.table.setItem(row, 1, artist_item)

            # Track Name
            title_item = QTableWidgetItem(track['title'])
            title_item.setData(Qt.ItemDataRole.UserRole, track['title'])
            self.table.setItem(row, 2, title_item)

            # YouTube Music Link
            if track['url']:
                link_item = QTableWidgetItem("🎵 Open")
                link_item.setData(Qt.ItemDataRole.UserRole, track['url'])
                link_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                link_item.setToolTip(f"Double-click to open: {track['url']}")
            else:
                link_item = QTableWidgetItem("N/A")
                link_item.setData(Qt.ItemDataRole.UserRole, "")
                link_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(row, 3, link_item)

    def sort_table(self, logical_index: int):
        """Handle custom sorting for the first three columns."""
        if logical_index > 2:  # Only sort first three columns
            return

        # Toggle sort order if clicking the same column
        if logical_index == self.current_sort_column:
            self.current_sort_order = (
                Qt.SortOrder.DescendingOrder
                if self.current_sort_order == Qt.SortOrder.AscendingOrder
                else Qt.SortOrder.AscendingOrder
            )
        else:
            self.current_sort_order = Qt.SortOrder.AscendingOrder

        self.current_sort_column = logical_index

        # Sort the data
        reverse = self.current_sort_order == Qt.SortOrder.DescendingOrder

        if logical_index == 0:  # Position
            self.tracks_data.sort(key=lambda x: int(x['position']), reverse=reverse)
        elif logical_index == 1:  # Artist
            self.tracks_data.sort(key=lambda x: x['artist'].lower(), reverse=reverse)
        elif logical_index == 2:  # Track Name
            self.tracks_data.sort(key=lambda x: x['title'].lower(), reverse=reverse)

        # Repopulate table with sorted data
        self.populate_table()

        # Update status
        sort_order_text = "descending" if reverse else "ascending"
        column_names = ["Position", "Artist", "Track Name"]
        self.status_label.setText(f"Sorted by {column_names[logical_index]} ({sort_order_text})")

    def open_track_url(self, item: QTableWidgetItem):
        """Open the YouTube Music URL for the selected track."""
        row = item.row()
        url_item = self.table.item(row, 3)

        if url_item and url_item.data(Qt.ItemDataRole.UserRole):
            url = url_item.data(Qt.ItemDataRole.UserRole)
            webbrowser.open(url)
        else:
            track_name = self.table.item(row, 2).text()
            QMessageBox.information(
                self,
                "No URL Available",
                f"No YouTube Music URL available for '{track_name}'"
            )


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("PlaylistCat")

    # Set application style
    app.setStyle('Fusion')

    window = YouTubeMusicPlaylistViewer()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
