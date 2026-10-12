#!/usr/bin/env python3
"""
PlaylistCat - Catalog and explore your YouTube Music playlists
A Qt application to fetch and display YouTube Music playlists with sorting capabilities.
"""

import sys
import threading
import webbrowser
import os
from typing import List, Dict, Any, Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QProgressBar, QFrame, QComboBox, QGroupBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon
from ytmusicapi import YTMusic

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from musicbrainz import MusicBrainzClient, MusicBrainzError

try:
    from utils import extract_playlist_id, validate_playlist_id
    from auth import AuthenticationManager as AuthManager
except ImportError:
    # Fallback if modules are not found
    def extract_playlist_id(input_string):
        if not input_string:
            return None
        input_string = input_string.strip()
        if 'list=' in input_string:
            return input_string.split('list=')[1].split('&')[0]
        return input_string

    def validate_playlist_id(playlist_id):
        return playlist_id and playlist_id.startswith('PL') and len(playlist_id) > 10

    # Mock AuthenticationManager for fallback
    class AuthManager:
        def __init__(self):
            self.is_authenticated = False
            try:
                self.ytmusic = YTMusic()
            except:
                self.ytmusic = None

        def get_ytmusic(self):
            return self.ytmusic

        def can_access_personal_content(self):
            return False

        def setup_authentication(self, parent=None):
            return False

        def logout(self):
            pass

        def load_saved_auth(self):
            return False


def format_total_duration(seconds: int) -> str:
    """Format a playing time as e.g. '3 h 52 min' or '45 min 10 s'."""
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    if hours:
        return f"{hours} h {minutes} min"
    return f"{minutes} min {secs} s"


class PlaylistFetcher(QThread):
    """Background thread for fetching playlist data from YouTube Music."""

    data_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    progress_update = pyqtSignal(str)

    def __init__(self, ytmusic: YTMusic, playlist_id: str):
        super().__init__()
        self.ytmusic = ytmusic
        self.playlist_id = playlist_id

    def run(self):
        """Fetch playlist data in background thread."""
        try:
            self.progress_update.emit("Fetching playlist data...")
            playlist_data = self.ytmusic.get_playlist(
                self.playlist_id, limit=None)

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
                    artists = [artist.get('name', '')
                               for artist in track['artists'] if artist]

                artist_str = ', '.join(
                    artists) if artists else 'Unknown Artist'

                # Create YouTube Music URL
                video_id = track.get('videoId', '')
                set_video_id = track.get('setVideoId', '')
                youtube_url = f"https://music.youtube.com/watch?v={video_id}" if video_id else ""

                tracks.append({
                    'position': i,
                    'artist': artist_str,
                    'title': title,
                    # First artist only, for the MusicBrainz lookup
                    'primary_artist': artists[0] if artists else '',
                    'album': '',
                    'year': '',
                    'url': youtube_url,
                    'video_id': video_id,
                    'set_video_id': set_video_id,
                    'duration': track.get('duration') or '',
                    'duration_seconds': int(track.get('duration_seconds') or 0),
                })

            self.progress_update.emit(f"Found {len(tracks)} tracks")
            self.data_ready.emit(tracks)

        except Exception as e:
            self.error_occurred.emit(f"Error fetching playlist: {str(e)}")


class AlbumInfoFetcher(QThread):
    """Background thread for looking up original albums from MusicBrainz.

    MusicBrainz allows one request per second, so results are reported one
    track at a time and the table is filled in progressively.
    """

    info_ready = pyqtSignal(str, str, str)  # cache key, album, year
    progress_update = pyqtSignal(int, int)  # done, total

    def __init__(self, client: MusicBrainzClient, lookups: List[tuple]):
        super().__init__()
        self.client = client
        self.lookups = lookups  # (cache key, artist, title)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        try:
            for done, (key, artist, title) in enumerate(self.lookups, 1):
                if self.stop_event.is_set():
                    return
                try:
                    info = self.client.lookup(artist, title, self.stop_event) or {}
                    self.info_ready.emit(key, info.get('album', ''), info.get('year', ''))
                except MusicBrainzError as e:
                    # Not cached, so it is retried the next time the playlist is loaded
                    print(f"MusicBrainz lookup failed for {artist} - {title}: {e}")
                self.progress_update.emit(done, len(self.lookups))
                if done % 10 == 0:
                    self.client.save_cache()
        finally:
            self.client.save_cache()


class PersonalPlaylistFetcher(QThread):
    """Background thread for fetching user's personal playlists."""

    playlists_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    progress_update = pyqtSignal(str)

    def __init__(self, ytmusic: YTMusic):
        super().__init__()
        self.ytmusic = ytmusic

    def run(self):
        """Fetch personal playlists in background thread."""
        try:
            self.progress_update.emit("Fetching your playlists...")
            playlists = self.ytmusic.get_library_playlists(limit=100)

            formatted_playlists = []
            for playlist in playlists:
                formatted_playlists.append({
                    'id': playlist.get('playlistId', ''),
                    'title': playlist.get('title', 'Unknown Playlist'),
                    'description': playlist.get('description', ''),
                    'count': playlist.get('count', 0),
                    'thumbnails': playlist.get('thumbnails', [])
                })

            self.progress_update.emit(f"Found {len(formatted_playlists)} playlists")
            self.playlists_ready.emit(formatted_playlists)

        except Exception as e:
            self.error_occurred.emit(f"Error fetching playlists: {str(e)}")


class YouTubeMusicPlaylistViewer(QMainWindow):
    """Main application window for YouTube Music Playlist Viewer."""

    def __init__(self):
        super().__init__()
        self.tracks_data = []
        self.personal_playlists = []
        self.current_sort_column = 0
        self.current_sort_order = Qt.SortOrder.AscendingOrder
        self.fetcher_thread = None
        self.playlist_fetcher_thread = None
        self.album_info_thread = None
        self.musicbrainz = MusicBrainzClient()
        self.current_playlist_id = None  # Track current playlist for refresh functionality

        # Initialize authentication manager
        self.auth_manager = AuthManager()

        # Initialize UI first
        self.init_ui()
        self.setWindowTitle("PlaylistCat - YouTube Music Playlist Viewer")
        self.resize(1000, 700)

        # Connect auth status changed signal if available (after UI is created)
        if hasattr(self.auth_manager, 'auth_status_changed'):
            self.auth_manager.auth_status_changed.connect(self.on_auth_status_changed)

        # Try to load saved authentication (after UI and signal connection)
        self.auth_manager.load_saved_auth()

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

        # Authentication section
        self.create_auth_section()
        layout.addWidget(self.auth_frame)

        # Input section
        self.create_input_section()
        layout.addWidget(self.input_frame)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Enter a playlist ID to get started or login to access your playlists")
        self.status_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.status_label)

        # Table
        self.create_table()
        layout.addWidget(self.table)

        # Playlist totals
        self.summary_label = QLabel("")
        self.summary_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.summary_label)

        # Instructions
        instructions = QLabel(
            "Instructions:\n"
            "• Login to access your personal playlists, or\n"
            "• Enter a YouTube Music playlist ID and click 'Fetch Playlist'\n"
            "• Click column headers to sort by Position, Artist, Track Name, Album, Year, or Length\n"
            "• Album and year show the original release, looked up from MusicBrainz in the background\n"
            "• Position numbers reflect original YouTube Music order (preserved during sorting)\n"
            "• Double-click any row to open the track in YouTube Music\n"
            "• Click the Remove button to delete a song from the playlist (removes from server if authenticated)"
        )
        instructions.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(instructions)

    def create_auth_section(self):
        """Create authentication section of the UI"""
        self.auth_frame = QGroupBox("Authentication")
        auth_layout = QHBoxLayout(self.auth_frame)

        # Authentication status
        self.auth_status_label = QLabel("Not logged in - Public playlists only")
        self.auth_status_label.setStyleSheet("color: orange; font-weight: bold;")
        auth_layout.addWidget(self.auth_status_label)

        auth_layout.addStretch()

        # Force Auth Refresh button (only visible when authenticated)
        self.refresh_auth_button = QPushButton("Refresh Auth")
        self.refresh_auth_button.clicked.connect(self.force_auth_refresh)
        self.refresh_auth_button.setVisible(False)  # Hidden by default
        self.refresh_auth_button.setToolTip("Force refresh authentication tokens")
        auth_layout.addWidget(self.refresh_auth_button)

        # Login/Logout button
        self.auth_button = QPushButton("Login")
        self.auth_button.clicked.connect(self.toggle_authentication)
        auth_layout.addWidget(self.auth_button)

    def create_input_section(self):
        """Create input section of the UI"""
        self.input_frame = QFrame()
        self.input_frame.setFrameStyle(QFrame.Shape.Box)
        input_layout = QVBoxLayout(self.input_frame)

        # Personal playlists section (only visible when authenticated)
        personal_layout = QHBoxLayout()
        personal_layout.addWidget(QLabel("Your Playlists:"))

        self.personal_playlist_combo = QComboBox()
        self.personal_playlist_combo.addItem("Select a playlist...")
        self.personal_playlist_combo.currentTextChanged.connect(self.on_personal_playlist_selected)
        personal_layout.addWidget(self.personal_playlist_combo)

        self.refresh_playlists_button = QPushButton("Refresh Playlists (Auto Token Refresh)")
        self.refresh_playlists_button.clicked.connect(self.refresh_personal_playlists)
        personal_layout.addWidget(self.refresh_playlists_button)

        self.personal_frame = QWidget()
        self.personal_frame.setLayout(personal_layout)
        self.personal_frame.setVisible(False)  # Hidden by default
        input_layout.addWidget(self.personal_frame)

        # Manual playlist ID section
        manual_layout = QHBoxLayout()
        manual_layout.addWidget(QLabel("Playlist ID:"))

        self.playlist_input = QLineEdit()
        self.playlist_input.setPlaceholderText(
            "Enter YouTube Music playlist ID (e.g., PLrAGlzNOGcAqFNKK0c4K8Z9U8QmFNKK0c)")
        self.playlist_input.returnPressed.connect(self.fetch_playlist)
        manual_layout.addWidget(self.playlist_input)

        self.fetch_button = QPushButton("Fetch Playlist")
        self.fetch_button.clicked.connect(self.fetch_playlist)
        manual_layout.addWidget(self.fetch_button)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_playlist)
        self.refresh_button.setEnabled(False)
        manual_layout.addWidget(self.refresh_button)

        input_layout.addLayout(manual_layout)

    def create_table(self):
        """Create and configure the tracks table."""
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["Position", "Artist", "Track Name", "Album", "Year", "Length", "YouTube Music Link", "Remove"])

        # Configure table appearance
        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(
                0, QHeaderView.ResizeMode.ResizeToContents)  # Position
            header.setSectionResizeMode(
                1, QHeaderView.ResizeMode.Interactive)        # Artist
            header.setSectionResizeMode(
                2, QHeaderView.ResizeMode.Stretch)           # Track Name
            header.setSectionResizeMode(
                3, QHeaderView.ResizeMode.Interactive)       # Album
            header.setSectionResizeMode(
                4, QHeaderView.ResizeMode.ResizeToContents)  # Year
            header.setSectionResizeMode(
                5, QHeaderView.ResizeMode.ResizeToContents)  # Length
            header.setSectionResizeMode(
                6, QHeaderView.ResizeMode.ResizeToContents)  # Link
            header.setSectionResizeMode(
                7, QHeaderView.ResizeMode.ResizeToContents)  # Remove
        self.table.setColumnWidth(3, 200)

        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows)
        # Disable built-in sorting, use custom logic
        self.table.setSortingEnabled(False)

        # Connect double-click to open URL
        self.table.itemDoubleClicked.connect(self.open_track_url)

        # Connect header clicks for custom sorting
        if header:
            header.sectionClicked.connect(self.sort_table)

    def toggle_authentication(self):
        """Toggle between login and logout"""
        if hasattr(self.auth_manager, 'is_authenticated') and self.auth_manager.is_authenticated:
            self.logout()
        else:
            self.login()

    def login(self):
        """Handle user login"""
        if hasattr(self.auth_manager, 'setup_authentication'):
            success = self.auth_manager.setup_authentication(self)
            if success:
                QMessageBox.information(self, "Success", "Successfully logged in!")
                self.refresh_personal_playlists()
            else:
                QMessageBox.warning(self, "Failed", "Login failed. Please try again.")

    def logout(self):
        """Handle user logout"""
        if hasattr(self.auth_manager, 'logout'):
            self.auth_manager.logout()
            QMessageBox.information(self, "Logged Out", "You have been logged out.")

    def on_auth_status_changed(self, is_authenticated: bool):
        """Handle authentication status changes"""
        if is_authenticated:
            self.auth_status_label.setText("Logged in - Access to personal playlists")
            self.auth_status_label.setStyleSheet("color: green; font-weight: bold;")
            self.auth_button.setText("Logout")
            self.refresh_auth_button.setVisible(True)  # Show refresh auth button
            self.personal_frame.setVisible(True)
            self.status_label.setText("Select one of your playlists or enter a playlist ID")
        else:
            self.auth_status_label.setText("Not logged in - Public playlists only")
            self.auth_status_label.setStyleSheet("color: orange; font-weight: bold;")
            self.auth_button.setText("Login")
            self.refresh_auth_button.setVisible(False)  # Hide refresh auth button
            self.personal_frame.setVisible(False)
            self.personal_playlist_combo.clear()
            self.personal_playlist_combo.addItem("Select a playlist...")
            self.status_label.setText("Enter a playlist ID to get started or login to access your playlists")

    def refresh_personal_playlists(self):
        """Refresh the list of personal playlists with automatic token refresh"""
        if not hasattr(self.auth_manager, 'can_access_personal_content') or not self.auth_manager.can_access_personal_content():
            QMessageBox.information(self, "Not Authenticated",
                                  "Please login first to access your personal playlists.")
            return

        # Stop any running playlist fetcher
        if self.playlist_fetcher_thread and self.playlist_fetcher_thread.isRunning():
            self.playlist_fetcher_thread.terminate()
            self.playlist_fetcher_thread.wait()

        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.status_label.setText("Fetching your playlists...")
        self.refresh_playlists_button.setEnabled(False)

        # Use the authentication manager's get_user_playlists which has token refresh
        try:
            print("🔄 Refreshing playlists using auth manager...")
            playlists = self.auth_manager.get_user_playlists()

            if playlists:
                print(f"✅ Successfully refreshed {len(playlists)} playlists")
                self.on_personal_playlists_ready(playlists)
                self.status_label.setText(f"Found {len(playlists)} personal playlists")
            else:
                print("⚠️  No playlists returned")
                # Check if we're still authenticated
                if self.auth_manager.is_authenticated:
                    # Try to refresh authentication status
                    print("🔧 Attempting authentication refresh...")
                    refresh_success = self.auth_manager.refresh_authentication_status()

                    if refresh_success:
                        # Retry after refresh
                        playlists = self.auth_manager.get_user_playlists()
                        if playlists:
                            print(f"✅ Retry successful! Got {len(playlists)} playlists after refresh")
                            self.on_personal_playlists_ready(playlists)
                            self.status_label.setText(f"Found {len(playlists)} personal playlists")
                        else:
                            self.status_label.setText("No personal playlists found")
                            QMessageBox.information(self, "No Playlists",
                                                  "No personal playlists found. This could mean:\n"
                                                  "• Your account has no created playlists\n"
                                                  "• Authentication tokens have expired\n"
                                                  "• Account permissions are restricted\n\n"
                                                  "Try logging out and logging in again with fresh authentication.")
                    else:
                        # Authentication refresh failed
                        self.status_label.setText("Authentication expired - please login again")
                        QMessageBox.warning(self, "Authentication Expired",
                                          "Your authentication has expired. Please logout and login again with a fresh cURL command from your browser.")
                        # Update UI to show not authenticated
                        self.on_auth_status_changed(False)
                else:
                    self.status_label.setText("Not authenticated - please login")
                    QMessageBox.information(self, "Not Authenticated",
                                          "You are no longer authenticated. Please login again.")

        except Exception as e:
            print(f"❌ Error refreshing playlists: {e}")
            self.status_label.setText("Error refreshing playlists")
            QMessageBox.critical(self, "Error",
                               f"Failed to refresh playlists: {str(e)}\n\n"
                               "This might be due to expired authentication. "
                               "Try logging out and logging in again.")

        finally:
            self.progress_bar.setVisible(False)
            self.refresh_playlists_button.setEnabled(True)

    def force_auth_refresh(self):
        """Force authentication token refresh"""
        if not hasattr(self.auth_manager, 'force_token_refresh'):
            QMessageBox.information(self, "Not Available",
                                  "Token refresh is not available in this authentication mode.")
            return

        # Disable button during refresh
        self.refresh_auth_button.setEnabled(False)
        self.refresh_auth_button.setText("Refreshing...")

        try:
            print("🔄 Manual authentication refresh requested...")
            refresh_success = self.auth_manager.force_token_refresh()

            if refresh_success:
                QMessageBox.information(self, "Success",
                                      "Authentication tokens refreshed successfully!")
                self.status_label.setText("Authentication refreshed - ready to fetch playlists")
                # Automatically refresh playlists after successful auth refresh
                self.refresh_personal_playlists()
            else:
                # Get authentication status info for more details
                if hasattr(self.auth_manager, 'get_auth_status_info'):
                    status = self.auth_manager.get_auth_status_info()
                    retry_count = status.get('auth_retry_count', 0)
                    max_retries = status.get('max_retries', 3)

                    QMessageBox.warning(self, "Refresh Failed",
                                      f"Authentication token refresh failed.\n\n"
                                      f"Retry attempts: {retry_count}/{max_retries}\n\n"
                                      "This usually means your browser session has expired. "
                                      "Please logout and login again with a fresh cURL command.")
                else:
                    QMessageBox.warning(self, "Refresh Failed",
                                      "Authentication token refresh failed. "
                                      "Please logout and login again.")

        except Exception as e:
            print(f"❌ Error during manual auth refresh: {e}")
            QMessageBox.critical(self, "Error",
                               f"Error during authentication refresh: {str(e)}")

        finally:
            # Re-enable button
            self.refresh_auth_button.setEnabled(True)
            self.refresh_auth_button.setText("Refresh Auth")

    def on_personal_playlists_ready(self, playlists: List[Dict[str, Any]]):
        """Handle personal playlists fetch completion"""
        self.personal_playlists = playlists
        self.personal_playlist_combo.clear()
        self.personal_playlist_combo.addItem("Select a playlist...")

        for playlist in playlists:
            title = playlist['title']
            count = playlist.get('count', 0)
            display_text = f"{title} ({count} tracks)"
            self.personal_playlist_combo.addItem(display_text, playlist['id'])

        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Found {len(playlists)} personal playlists")

    def on_personal_playlist_selected(self, text: str):
        """Handle personal playlist selection"""
        if text == "Select a playlist...":
            return

        current_index = self.personal_playlist_combo.currentIndex()
        if current_index > 0:  # Skip the first "Select a playlist..." item
            playlist_id = self.personal_playlist_combo.itemData(current_index)
            if playlist_id:
                self.playlist_input.setText(playlist_id)
                self.fetch_playlist()

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
        self.stop_album_info_fetch()

        # Store current playlist ID for refresh functionality
        self.current_playlist_id = playlist_id

        # Update UI for loading state
        self.fetch_button.setEnabled(False)
        self.refresh_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.status_label.setText("Fetching playlist...")

        # Get YTMusic instance from auth manager
        ytmusic = self.auth_manager.get_ytmusic()
        if ytmusic:
            # Start background thread
            self.fetcher_thread = PlaylistFetcher(ytmusic, playlist_id)
            self.fetcher_thread.data_ready.connect(self.on_data_ready)
            self.fetcher_thread.error_occurred.connect(self.on_error)
            self.fetcher_thread.progress_update.connect(self.on_progress_update)
            self.fetcher_thread.start()
        else:
            QMessageBox.critical(self, "Error", "YouTube Music API not available")
            self.fetch_button.setEnabled(True)
            self.refresh_button.setEnabled(True)
            self.progress_bar.setVisible(False)

    def on_data_ready(self, tracks: List[Dict[str, Any]]):
        """Handle successful data fetch."""
        self.tracks_data = tracks
        for track in self.tracks_data:
            track['mb_key'] = MusicBrainzClient.cache_key(track['primary_artist'], track['title'])
            info = self.musicbrainz.cache.get(track['mb_key']) or {}
            track['album'] = info.get('album', '')
            track['year'] = info.get('year', '')
        self.populate_table()

        # Update UI
        self.fetch_button.setEnabled(True)
        self.refresh_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Loaded {len(tracks)} tracks")
        self.start_album_info_fetch()

    def start_album_info_fetch(self):
        """Look up original albums for tracks not already in the MusicBrainz cache."""
        lookups = {}
        for t in self.tracks_data:
            if t['primary_artist'] and t['mb_key'] not in self.musicbrainz.cache:
                lookups.setdefault(t['mb_key'], (t['mb_key'], t['primary_artist'], t['title']))
        if not lookups:
            return

        self.album_info_thread = AlbumInfoFetcher(self.musicbrainz, list(lookups.values()))
        self.album_info_thread.info_ready.connect(self.on_album_info_ready)
        self.album_info_thread.progress_update.connect(self.on_album_info_progress)
        self.album_info_thread.start()

    def stop_album_info_fetch(self):
        """Stop a running album lookup, e.g. when another playlist is loaded."""
        if self.album_info_thread and self.album_info_thread.isRunning():
            self.album_info_thread.info_ready.disconnect(self.on_album_info_ready)
            self.album_info_thread.progress_update.disconnect(self.on_album_info_progress)
            self.album_info_thread.stop()
            self.album_info_thread.wait()

    def closeEvent(self, a0):
        self.stop_album_info_fetch()
        super().closeEvent(a0)

    def on_album_info_ready(self, key: str, album: str, year: str):
        """Fill in album and year for every track matching the lookup."""
        for row, track in enumerate(self.tracks_data):
            if track['mb_key'] == key:
                track['album'] = album
                track['year'] = year
                self.table.setItem(row, 3, self._album_item(album))
                self.table.setItem(row, 4, self._year_item(year))

    def on_album_info_progress(self, done: int, total: int):
        if done < total:
            self.status_label.setText(f"Looking up original albums on MusicBrainz: {done}/{total}")
        else:
            self.status_label.setText(f"Loaded {len(self.tracks_data)} tracks, album lookup complete")

    def _album_item(self, album: str) -> QTableWidgetItem:
        item = QTableWidgetItem(album)
        item.setData(Qt.ItemDataRole.UserRole, album)
        return item

    def _year_item(self, year: str) -> QTableWidgetItem:
        item = QTableWidgetItem(year)
        item.setData(Qt.ItemDataRole.UserRole, year)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item

    def on_error(self, error_message: str):
        """Handle fetch error."""
        QMessageBox.critical(self, "Error", error_message)

        # Reset UI
        self.fetch_button.setEnabled(True)
        self.refresh_button.setEnabled(
            bool(self.playlist_input.text().strip()))
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

            # Album
            self.table.setItem(row, 3, self._album_item(track['album']))

            # Year
            self.table.setItem(row, 4, self._year_item(track['year']))

            # Length
            length_item = QTableWidgetItem(track['duration'])
            length_item.setData(Qt.ItemDataRole.UserRole, track['duration_seconds'])
            length_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 5, length_item)

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

            self.table.setItem(row, 6, link_item)

            # Remove Button
            remove_button = QPushButton("🗑️ Remove")
            remove_button.setToolTip(f"Remove '{track['title']}' from the list")
            remove_button.clicked.connect(lambda checked, r=row: self.remove_track(r))
            remove_button.setStyleSheet("""
                QPushButton {
                    background-color: #ff6b6b;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 3px;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background-color: #ff5252;
                }
                QPushButton:pressed {
                    background-color: #e53935;
                }
            """)
            self.table.setCellWidget(row, 7, remove_button)

        self.update_summary()

    def update_summary(self):
        """Show the number of tracks and total playing time of the playlist."""
        if not self.tracks_data:
            self.summary_label.setText("")
            return
        total = sum(t['duration_seconds'] for t in self.tracks_data)
        unknown = sum(1 for t in self.tracks_data if not t['duration_seconds'])
        text = f"{len(self.tracks_data)} tracks · {format_total_duration(total)}"
        if unknown:
            text += f" ({unknown} without length)"
        self.summary_label.setText(text)

    def sort_table(self, logical_index: int):
        """Handle custom sorting for the data columns."""
        if logical_index > 5:  # Skip Link and Remove columns
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

        if logical_index == 0:  # Position - sort by original YouTube Music position
            self.tracks_data.sort(key=lambda x: int(
                x['position']), reverse=reverse)
        elif logical_index == 1:  # Artist - sort by artist but keep original positions
            self.tracks_data.sort(
                key=lambda x: x['artist'].lower(), reverse=reverse)
        elif logical_index == 2:  # Track Name - sort by title but keep original positions
            self.tracks_data.sort(
                key=lambda x: x['title'].lower(), reverse=reverse)
        elif logical_index in (3, 4, 5):  # Album / Year / Length - tracks without a value go last
            field = {3: 'album', 4: 'year', 5: 'duration_seconds'}[logical_index]
            with_value = [t for t in self.tracks_data if t[field]]
            without_value = [t for t in self.tracks_data if not t[field]]
            with_value.sort(key=lambda x: x[field].lower() if isinstance(x[field], str) else x[field],
                            reverse=reverse)
            self.tracks_data[:] = with_value + without_value

        # Note: We DO NOT renumber positions here - they stay as original YouTube Music order
        # Repopulate table with sorted data
        self.populate_table()

        # Update status
        sort_order_text = "descending" if reverse else "ascending"
        column_names = ["Position", "Artist", "Track Name", "Album", "Year", "Length"]
        self.status_label.setText(
            f"Sorted by {column_names[logical_index]} ({sort_order_text})")

    def open_track_url(self, item: QTableWidgetItem):
        """Open the YouTube Music URL for the selected track."""
        row = item.row()
        url_item = self.table.item(row, 6)

        if url_item and url_item.data(Qt.ItemDataRole.UserRole):
            url = url_item.data(Qt.ItemDataRole.UserRole)
            webbrowser.open(url)
        else:
            track_item = self.table.item(row, 2)
            track_name = track_item.text() if track_item else "Unknown Track"
            QMessageBox.information(
                self,
                "No URL Available",
                f"No YouTube Music URL available for '{track_name}'"
            )

    def remove_track(self, row: int):
        """Remove a track from the playlist."""
        if row < 0 or row >= len(self.tracks_data):
            return

        # Get track info for confirmation
        track = self.tracks_data[row]
        track_name = track.get('title', 'Unknown Track')
        artist_name = track.get('artist', 'Unknown Artist')

        # Confirm removal
        reply = QMessageBox.question(
            self,
            "Remove Track",
            f"Are you sure you want to remove this track from the playlist?\n\n"
            f"🎵 {track_name}\n"
            f"👤 {artist_name}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Try to remove from server first
            server_removal_success = False

            # Check if we have the required IDs for server removal
            video_id = track.get('video_id', '')
            set_video_id = track.get('set_video_id', '')
            playlist_id = getattr(self, 'current_playlist_id', '')
            ytmusic = self.auth_manager.get_ytmusic() if self.auth_manager else None

            if video_id and set_video_id and playlist_id and ytmusic:
                try:
                    self.status_label.setText("Removing track from server...")

                    # Prepare the removal data
                    videos_to_remove = [{
                        'videoId': video_id,
                        'setVideoId': set_video_id
                    }]

                    # Call the YouTube Music API to remove from server
                    result = ytmusic.remove_playlist_items(playlist_id, videos_to_remove)

                    if result:  # API returns success status
                        server_removal_success = True
                        self.status_label.setText("✅ Track removed from server successfully")
                    else:
                        self.status_label.setText("⚠️ Server removal may have failed")

                except Exception as e:
                    self.status_label.setText(f"❌ Server removal failed: {str(e)}")
                    # Ask user if they want to continue with local removal
                    reply = QMessageBox.question(
                        self,
                        "Server Removal Failed",
                        f"Failed to remove track from server:\n{str(e)}\n\n"
                        f"Do you want to remove it from the local display anyway?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                        QMessageBox.StandardButton.No
                    )
                    if reply != QMessageBox.StandardButton.Yes:
                        return

            # Remove from local data (always do this, whether server removal succeeded or not)
            self.tracks_data.pop(row)

            # Note: We preserve original YouTube Music position numbers
            # No renumbering - positions may have gaps after removal, which is correct
            # This ensures position sorting always reflects original YouTube Music order

            # Refresh the table display
            self.populate_table()

            # Update status message
            if server_removal_success:
                self.status_label.setText(
                    f"✅ Removed '{track_name}' from playlist. {len(self.tracks_data)} tracks remaining.")
            elif video_id and set_video_id and playlist_id:
                self.status_label.setText(
                    f"⚠️ '{track_name}' removed locally. Server sync may be needed. {len(self.tracks_data)} tracks remaining.")
            else:
                self.status_label.setText(
                    f"📝 '{track_name}' removed from display (read-only mode). {len(self.tracks_data)} tracks remaining.")

            # Enable refresh button if we have a current playlist
            if hasattr(self, 'current_playlist_id') and self.current_playlist_id:
                self.refresh_button.setEnabled(True)


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
