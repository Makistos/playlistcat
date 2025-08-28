#!/usr/bin/env python3
"""
Authentication manager for YouTube Music API access
Supports both authenticated (personal playlists) and unauthenticated (public playlists) modes
"""

import os
import json
import tempfile
import webbrowser
import shlex
from typing import Optional, Dict, List, Any
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from PyQt6.QtWidgets import QMessageBox, QInputDialog, QDialog, QVBoxLayout, QPushButton, QLabel, QTextEdit
from ytmusicapi import YTMusic


class AuthSetupDialog(QDialog):
    """Dialog for setting up YouTube Music authentication"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("YouTube Music Authentication Setup")
        self.setModal(True)
        self.resize(600, 500)
        self.auth_data = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Instructions
        instructions = QLabel("""
<h3>YouTube Music Authentication Setup</h3>
<p>To access your personal playlists, you need to provide authentication headers from your browser.</p>

<h4>Steps:</h4>
<ol>
<li>Open YouTube Music in your browser and log in</li>
<li>Open Developer Tools (F12)</li>
<li>Go to Network tab</li>
<li>Refresh the page or navigate to a playlist</li>
<li>Look for requests to <b>music.youtube.com</b></li>
<li>Find a request with <b>Cookie</b> headers (like /youtubei/v1/ or /generate_204)</li>
<li>Right-click → Copy → Copy as cURL</li>
<li>Paste the cURL command below</li>
</ol>

<p><strong>Note:</strong> The cURL command should include Cookie headers with authentication data.</p>
        """)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        # Text area for cURL input
        self.curl_input = QTextEdit()
        self.curl_input.setPlaceholderText("Paste the cURL command here...")
        layout.addWidget(self.curl_input)

        # Buttons
        button_layout = QVBoxLayout()

        self.setup_button = QPushButton("Setup Authentication")
        self.setup_button.clicked.connect(self.setup_auth)
        button_layout.addWidget(self.setup_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def setup_auth(self):
        curl_text = self.curl_input.toPlainText().strip()
        if not curl_text:
            QMessageBox.warning(self, "Warning", "Please paste a cURL command")
            return

        try:
            # Parse cURL command to extract headers
            auth_data = self.parse_curl_command(curl_text)
            if auth_data:
                # Check if we have essential authentication data
                cookie_header = auth_data.get('Cookie') or auth_data.get('cookie')
                if not cookie_header:
                    QMessageBox.critical(self, "Error",
                        "No Cookie header found in the cURL command.\n\n"
                        "Please make sure you:\n"
                        "1. Are logged into YouTube Music\n"
                        "2. Copied a request that includes authentication cookies\n"
                        "3. Used 'Copy as cURL' from the browser's Network tab")
                    return

                # Check for essential authentication cookies
                auth_cookies = ['SID=', 'HSID=', 'SSID=', 'APISID=', 'SAPISID=']
                found_cookies = [cookie for cookie in auth_cookies if cookie in cookie_header]

                if len(found_cookies) < 3:
                    QMessageBox.warning(self, "Warning",
                        f"Found only {len(found_cookies)} authentication cookies. "
                        "You may need more for full authentication.\n\n"
                        "Try copying a different request from the Network tab, "
                        "preferably one to /youtubei/v1/ endpoint.")

                self.auth_data = auth_data
                self.accept()
            else:
                QMessageBox.critical(self, "Error",
                    "Could not parse authentication data from cURL command.\n\n"
                    "Please make sure:\n"
                    "1. You copied the complete cURL command\n"
                    "2. The command includes Cookie headers\n"
                    "3. You are logged into YouTube Music\n\n"
                    "Try copying a different network request from the browser.")

        except Exception as e:
            QMessageBox.critical(self, "Error",
                f"Failed to parse cURL command: {str(e)}\n\n"
                "Please check that you pasted a complete cURL command from your browser's Network tab.")

    def parse_curl_command(self, curl_text: str) -> Optional[Dict]:
        """Parse cURL command to extract authentication headers"""
        import re

        # Clean up the curl command - remove line continuations and normalize
        # Remove backslashes at end of lines and join continuation lines
        cleaned_text = re.sub(r'\\\s*\n\s*', ' ', curl_text)

        # Split into tokens while respecting quotes
        tokens = self._tokenize_curl_command(cleaned_text)

        headers = {}
        i = 0

        while i < len(tokens):
            token = tokens[i]

            # Look for header flags
            if token in ['-H', '--header'] and i + 1 < len(tokens):
                header_value = tokens[i + 1]

                # Remove quotes if present
                if (header_value.startswith('"') and header_value.endswith('"')) or \
                   (header_value.startswith("'") and header_value.endswith("'")):
                    header_value = header_value[1:-1]

                # Parse header
                if ':' in header_value:
                    key, value = header_value.split(':', 1)
                    headers[key.strip()] = value.strip()

                i += 2  # Skip both the flag and the value
            else:
                i += 1

        # Check if we have essential authentication headers
        cookie_header = headers.get('Cookie') or headers.get('cookie')
        if cookie_header:
            # Validate that this looks like a YouTube Music cookie
            if any(cookie_part in cookie_header for cookie_part in ['SID=', 'HSID=', 'SSID=', 'APISID=', 'SAPISID=']):
                return headers

        return None

    def _tokenize_curl_command(self, text: str) -> List[str]:
        """Tokenize curl command while respecting quotes"""
        import shlex
        try:
            # Use shlex to properly handle quoted strings
            return shlex.split(text)
        except ValueError:
            # Fallback to simple splitting if shlex fails
            tokens = []
            current_token = ""
            in_quotes = False
            quote_char = None

            for char in text:
                if char in ['"', "'"] and not in_quotes:
                    in_quotes = True
                    quote_char = char
                    current_token += char
                elif char == quote_char and in_quotes:
                    in_quotes = False
                    current_token += char
                    quote_char = None
                elif char.isspace() and not in_quotes:
                    if current_token:
                        tokens.append(current_token)
                        current_token = ""
                else:
                    current_token += char

            if current_token:
                tokens.append(current_token)

            return tokens


class PlaylistFetcher(QThread):
    """Background thread for fetching playlists (both personal and public)"""

    playlists_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    progress_update = pyqtSignal(str)

    def __init__(self, ytmusic: YTMusic, fetch_personal: bool = False):
        super().__init__()
        self.ytmusic = ytmusic
        self.fetch_personal = fetch_personal

    def run(self):
        try:
            if self.fetch_personal:
                self.progress_update.emit("Fetching your personal playlists...")
                playlists = self.ytmusic.get_library_playlists(limit=100)
            else:
                # For unauthenticated mode, we can't fetch personal playlists
                # This would be used for other features like search results
                self.playlists_ready.emit([])
                return

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


class AuthenticationManager(QObject):
    """Manages YouTube Music authentication state and operations"""

    # Signals
    auth_status_changed = pyqtSignal(bool)  # True if authenticated, False if not
    user_info_updated = pyqtSignal(dict)    # User information

    def __init__(self):
        super().__init__()
        self.is_authenticated = False
        self.user_info = {}
        self.ytmusic = None
        self.auth_session = None  # Store authenticated requests session
        self.auth_file_path = os.path.join(os.path.expanduser("~"), ".playlistcat_auth.json")

        # Initialize with unauthenticated YTMusic
        self.init_unauthenticated()

    def init_unauthenticated(self):
        """Initialize YTMusic in unauthenticated mode"""
        try:
            self.ytmusic = YTMusic()
            self.is_authenticated = False
            self.user_info = {}
            self.auth_status_changed.emit(False)
        except Exception as e:
            print(f"Failed to initialize YTMusic: {e}")
            self.ytmusic = None

    def setup_authentication(self, parent_widget=None) -> bool:
        """Show authentication setup dialog and configure authentication"""
        dialog = AuthSetupDialog(parent_widget)

        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.auth_data:
            return self.authenticate_with_headers(dialog.auth_data)

        return False

    def authenticate_with_headers(self, headers: Dict[str, str]) -> bool:
        """Authenticate using browser headers with multiple fallback methods"""
        try:
            # Get cookie header
            cookie_header = headers.get('Cookie') or headers.get('cookie', '')
            if not cookie_header:
                raise Exception("No Cookie header found in the request")

            # Check for required authentication cookies
            required_cookies = ['SID=', 'HSID=', 'SSID=', 'APISID=', 'SAPISID=']
            missing_cookies = [cookie[:-1] for cookie in required_cookies if cookie not in cookie_header]

            if missing_cookies:
                raise Exception(f"Missing required authentication cookies: {missing_cookies}")

            # First verify the authentication headers work with direct API call
            print("🔧 Verifying authentication headers...")
            try:
                import requests
                test_response = requests.get(
                    'https://music.youtube.com/verify_session',
                    headers={
                        'Cookie': cookie_header,
                        'User-Agent': headers.get('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'),
                        'X-Goog-AuthUser': headers.get('X-Goog-AuthUser', '0'),
                        'Accept': '*/*',
                        'Referer': 'https://music.youtube.com/',
                    }
                )

                if test_response.status_code != 200:
                    raise Exception(f"Authentication test failed with status {test_response.status_code}")

                print("✅ Authentication headers verified")

            except Exception as api_error:
                raise Exception(f"Authentication verification failed: {api_error}")

            # Since the standard auth file approach has issues, let's try multiple methods
            # Create a custom YTMusic wrapper that handles authentication differently
            print("🔧 Setting up YTMusic with multiple authentication methods...")

            # Method 1: Try to create a working auth file using the exact format from working examples
            # IMPORTANT: We need to include Authorization header with SAPISIDHASH to avoid OAuth detection
            # See: https://github.com/sigma67/ytmusicapi/issues/781

            # Extract SAPISID from cookies to generate SAPISIDHASH
            import re
            import hashlib
            import time

            sapisid = None
            for cookie in cookie_header.split(';'):
                cookie = cookie.strip()
                if cookie.startswith('SAPISID='):
                    sapisid = cookie.split('=', 1)[1]
                    break

            authorization_header = None
            if sapisid:
                # Generate SAPISIDHASH as required by ytmusicapi for browser auth detection
                # Format: SAPISIDHASH {timestamp}_{hash}
                timestamp = str(int(time.time()))
                origin = "https://music.youtube.com"
                hash_string = f"{timestamp} {sapisid} {origin}"
                sapisidhash = hashlib.sha1(hash_string.encode()).hexdigest()
                authorization_header = f"SAPISIDHASH {timestamp}_{sapisidhash}"
                print(f"✅ Generated SAPISIDHASH authorization header")
            else:
                print("⚠️  No SAPISID found in cookies - this may cause OAuth detection issues")

            auth_data = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate",
                "content-encoding": "gzip",
                "content-type": "application/json",
                "cookie": cookie_header,
                "origin": "https://music.youtube.com",
                "user-agent": headers.get('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'),
                "x-goog-authuser": headers.get('X-Goog-AuthUser', '0'),
            }

            # Add the critical Authorization header to prevent OAuth detection
            if authorization_header:
                auth_data["authorization"] = authorization_header

            # Add YouTube-specific headers that are important
            youtube_headers_map = {
                'X-Goog-Visitor-Id': 'x-goog-visitor-id',
                'X-YouTube-Client-Name': 'x-youtube-client-name',
                'X-YouTube-Client-Version': 'x-youtube-client-version',
            }

            for header_key, auth_key in youtube_headers_map.items():
                if header_key in headers:
                    auth_data[auth_key] = headers[header_key]

            # Save authentication data to file for potential future use
            try:
                with open(self.auth_file_path, 'w') as f:
                    json.dump(auth_data, f, indent=2)
                print(f"✅ Auth file created: {self.auth_file_path}")
            except Exception as file_error:
                print(f"⚠️  Could not save auth file: {file_error}")

            # Method 2: Create a requests session with proper authentication
            session = requests.Session()
            session.headers.update({
                'Cookie': cookie_header,
                'User-Agent': headers.get('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'),
                'X-Goog-AuthUser': headers.get('X-Goog-AuthUser', '0'),
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://music.youtube.com/',
                'Origin': 'https://music.youtube.com',
            })

            # Add important YouTube headers to session
            youtube_headers = ['X-Goog-Visitor-Id', 'X-YouTube-Client-Name', 'X-YouTube-Client-Version']
            for header_key in youtube_headers:
                if header_key in headers:
                    session.headers[header_key] = headers[header_key]

            # Try multiple YTMusic initialization approaches
            test_ytmusic = None
            auth_method = None
            playlists = []  # Initialize playlists list

            # Approach 1: Try auth file + session (most likely to work for library access)
            if os.path.exists(self.auth_file_path):
                try:
                    print("🔧 Trying auth file + session...")
                    test_ytmusic = YTMusic(auth=self.auth_file_path, requests_session=session)
                    # Test library access
                    playlists = test_ytmusic.get_library_playlists(limit=1)
                    print(f"✅ Auth file + session works! Found {len(playlists)} playlists")
                    auth_method = "auth_file_session"
                except Exception as e:
                    print(f"⚠️  Auth file + session failed: {e}")
                    test_ytmusic = None

            # Approach 2: Try just auth file (if approach 1 failed)
            if test_ytmusic is None and os.path.exists(self.auth_file_path):
                try:
                    print("🔧 Trying auth file only...")
                    test_ytmusic = YTMusic(self.auth_file_path)
                    # Test library access
                    playlists = test_ytmusic.get_library_playlists(limit=1)
                    print(f"✅ Auth file works! Found {len(playlists)} playlists")
                    auth_method = "auth_file"
                except Exception as e:
                    print(f"⚠️  Auth file only failed: {e}")
                    test_ytmusic = None

            # Approach 3: Session only (fallback)
            if test_ytmusic is None:
                try:
                    print("🔧 Trying session only...")
                    test_ytmusic = YTMusic(requests_session=session)
                    print("✅ Session-only YTMusic created (library access may be limited)")
                    auth_method = "session_only"
                    playlists = []  # Can't test library access with session-only
                except Exception as e:
                    print(f"❌ Session-only failed: {e}")
                    raise Exception(f"All authentication methods failed. Last error: {e}")

            # If we get here, one of the methods worked
            self.ytmusic = test_ytmusic
            self.is_authenticated = True
            self.auth_session = session

            # Update user info based on successful method
            playlist_count = len(playlists) if playlists else 0

            self.user_info = {
                'authenticated': True,
                'playlists_count': playlist_count,
                'auth_method': auth_method,
                'note': f'Authentication successful using {auth_method}'
            }

            print(f"✅ Authentication setup complete using {auth_method}")
            if playlist_count > 0:
                print(f"✅ Library access confirmed: {playlist_count} playlists accessible")

            self.auth_status_changed.emit(True)
            self.user_info_updated.emit(self.user_info)

            return True

        except Exception as e:
            error_msg = str(e).lower()
            print(f"Authentication failed: {e}")

            # Provide more specific error messages
            if "verify_session" in error_msg or "401" in error_msg or "unauthorized" in error_msg:
                print("Authentication error: Invalid or expired credentials - please get fresh cURL command")
            elif "403" in error_msg or "forbidden" in error_msg:
                print("Authentication error: Access denied - check account permissions")
            elif "quota" in error_msg or "rate" in error_msg:
                print("Authentication error: Rate limit exceeded - try again later")
            elif "network" in error_msg or "connection" in error_msg:
                print("Authentication error: Network connection issue")
            else:
                print(f"Authentication error: {e}")

            # Fall back to unauthenticated mode
            self.init_unauthenticated()
            return False

    def load_saved_auth(self) -> bool:
        """Load previously saved authentication data"""
        if not os.path.exists(self.auth_file_path):
            return False

        try:
            # Test authentication with the saved file
            test_ytmusic = YTMusic(self.auth_file_path)
            test_ytmusic.get_library_playlists(limit=1)  # Test call

            # If we get here, authentication worked
            self.ytmusic = test_ytmusic
            self.is_authenticated = True

            self.auth_status_changed.emit(True)
            return True

        except Exception as e:
            print(f"Failed to load saved authentication: {e}")

            # Remove invalid auth file
            try:
                os.unlink(self.auth_file_path)
            except:
                pass

            self.init_unauthenticated()
            return False

    def save_auth_data(self, auth_data: Dict[str, str]):
        """Save authentication data to file"""
        try:
            # In production, you should encrypt this data
            with open(self.auth_file_path, 'w') as f:
                json.dump(auth_data, f)
        except Exception as e:
            print(f"Failed to save authentication data: {e}")

    def logout(self):
        """Logout and return to unauthenticated mode"""
        self.is_authenticated = False
        self.user_info = {}

        # Remove saved auth data
        try:
            if os.path.exists(self.auth_file_path):
                os.unlink(self.auth_file_path)
        except:
            pass

        # Reinitialize in unauthenticated mode
        self.init_unauthenticated()

    def get_user_playlists(self) -> List[Dict[str, Any]]:
        """Get user's personal playlists (only works when authenticated)"""
        if not self.is_authenticated or not self.ytmusic:
            print("Not authenticated or no YTMusic instance")
            return []

        try:
            print("🎵 Attempting to fetch user playlists...")
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

            print(f"✅ Successfully fetched {len(formatted_playlists)} playlists")
            return formatted_playlists

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Failed to get user playlists: {e}")

            # If we get the authentication error, try to re-authenticate
            if "authentication" in error_msg.lower():
                print("🔧 Authentication issue detected, trying to refresh...")

                # If we have a saved auth session, try to create a new YTMusic instance
                if hasattr(self, 'auth_session') and self.auth_session:
                    try:
                        # Try to recreate YTMusic with the auth file
                        if os.path.exists(self.auth_file_path):
                            print("🔧 Trying to reinitialize with auth file...")
                            self.ytmusic = YTMusic(self.auth_file_path)
                            # Retry the playlist fetch
                            playlists = self.ytmusic.get_library_playlists(limit=100)
                            print(f"✅ Re-authentication successful, got {len(playlists)} playlists")

                            formatted_playlists = []
                            for playlist in playlists:
                                formatted_playlists.append({
                                    'id': playlist.get('playlistId', ''),
                                    'title': playlist.get('title', 'Unknown Playlist'),
                                    'description': playlist.get('description', ''),
                                    'count': playlist.get('count', 0),
                                    'thumbnails': playlist.get('thumbnails', [])
                                })

                            return formatted_playlists

                    except Exception as retry_error:
                        print(f"⚠️  Re-authentication failed: {retry_error}")

                # If re-auth fails, provide helpful message
                print("ℹ️  Library access requires fresh authentication. Please logout and login again.")

            return []

    def get_ytmusic(self) -> Optional[YTMusic]:
        """Get the YTMusic instance (works for both authenticated and unauthenticated)"""
        return self.ytmusic

    def can_access_personal_content(self) -> bool:
        """Check if we can access personal content"""
        return self.is_authenticated and self.ytmusic is not None
