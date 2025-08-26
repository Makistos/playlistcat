#!/usr/bin/env python3
"""
PlaylistCat CLI - Catalog and explore your YouTube Music playlists
A command-line application to fetch and display YouTube Music playlists.
"""

import sys
import webbrowser
import os
from typing import List, Dict, Any
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


class YouTubeMusicCLI:
    """Command-line interface for YouTube Music Playlist Viewer."""

    def __init__(self):
        self.ytmusic = None
        self.tracks_data = []
        self.current_playlist_id = None

    def initialize_api(self):
        """Initialize the YouTube Music API."""
        try:
            self.ytmusic = YTMusic()
            return True
        except Exception as e:
            print(f"Error initializing YouTube Music API: {e}")
            return False

    def fetch_playlist(self, playlist_id: str) -> bool:
        """Fetch playlist data from YouTube Music."""
        try:
            print(f"Fetching playlist {playlist_id}...")
            playlist_data = self.ytmusic.get_playlist(playlist_id)

            if not playlist_data:
                print("Playlist not found or is private")
                return False

            print(f"Playlist: {playlist_data.get('title', 'Unknown Title')}")
            print(f"Description: {playlist_data.get('description', 'No description')}")
            print(f"Track count: {playlist_data.get('trackCount', 0)}")
            print()

            self.tracks_data = []

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

                self.tracks_data.append({
                    'position': i,
                    'artist': artist_str,
                    'title': title,
                    'url': youtube_url,
                    'video_id': video_id
                })

            self.current_playlist_id = playlist_id
            print(f"Successfully loaded {len(self.tracks_data)} tracks")
            return True

        except Exception as e:
            print(f"Error fetching playlist: {e}")
            return False

    def display_tracks(self, sort_by: str = 'position'):
        """Display tracks in a formatted table."""
        if not self.tracks_data:
            print("No tracks loaded. Please fetch a playlist first.")
            return

        # Sort tracks
        if sort_by == 'artist':
            sorted_tracks = sorted(self.tracks_data, key=lambda x: x['artist'].lower())
        elif sort_by == 'title':
            sorted_tracks = sorted(self.tracks_data, key=lambda x: x['title'].lower())
        else:  # position
            sorted_tracks = sorted(self.tracks_data, key=lambda x: x['position'])

        # Display header
        print("\n" + "=" * 100)
        print(f"{'Pos':<4} | {'Artist':<30} | {'Track Name':<40} | {'URL'}")
        print("=" * 100)

        # Display tracks
        for track in sorted_tracks:
            pos = str(track['position'])
            artist = track['artist'][:28] + ".." if len(track['artist']) > 30 else track['artist']
            title = track['title'][:38] + ".." if len(track['title']) > 40 else track['title']
            url = "Available" if track['url'] else "N/A"

            print(f"{pos:<4} | {artist:<30} | {title:<40} | {url}")

        print("=" * 100)
        print(f"Total tracks: {len(sorted_tracks)} (sorted by {sort_by})")

    def open_track(self, position: int):
        """Open a track in the browser."""
        if not self.tracks_data:
            print("No tracks loaded.")
            return

        track = next((t for t in self.tracks_data if t['position'] == position), None)
        if not track:
            print(f"Track at position {position} not found.")
            return

        if track['url']:
            print(f"Opening: {track['artist']} - {track['title']}")
            webbrowser.open(track['url'])
        else:
            print(f"No URL available for: {track['artist']} - {track['title']}")

    def run(self):
        """Main CLI loop."""
        print("PlaylistCat 🐱 (CLI)")
        print("=" * 40)

        if not self.initialize_api():
            return

        while True:
            print("\nCommands:")
            print("  fetch <playlist_id>  - Fetch a playlist")
            print("  show [sort_by]       - Show tracks (sort_by: position, artist, title)")
            print("  open <position>      - Open track at position in browser")
            print("  refresh              - Refresh current playlist")
            print("  quit                 - Exit")

            try:
                command = input("\n> ").strip().split()

                if not command:
                    continue

                cmd = command[0].lower()

                if cmd == 'quit' or cmd == 'exit':
                    break

                elif cmd == 'fetch':
                    if len(command) < 2:
                        print("Usage: fetch <playlist_id>")
                        continue

                    playlist_id = command[1]
                    # Clean playlist ID (remove URL parts if user pasted full URL)
                    playlist_id = extract_playlist_id(playlist_id)

                    if not playlist_id or not validate_playlist_id(playlist_id):
                        print("Invalid playlist ID format")
                        continue

                    self.fetch_playlist(playlist_id)

                elif cmd == 'show':
                    sort_by = command[1] if len(command) > 1 else 'position'
                    if sort_by not in ['position', 'artist', 'title']:
                        print("Invalid sort option. Use: position, artist, or title")
                        continue
                    self.display_tracks(sort_by)

                elif cmd == 'open':
                    if len(command) < 2:
                        print("Usage: open <position>")
                        continue

                    try:
                        position = int(command[1])
                        self.open_track(position)
                    except ValueError:
                        print("Position must be a number")

                elif cmd == 'refresh':
                    if self.current_playlist_id:
                        self.fetch_playlist(self.current_playlist_id)
                    else:
                        print("No playlist to refresh. Please fetch a playlist first.")

                else:
                    print("Unknown command. Try 'quit' to exit.")

            except KeyboardInterrupt:
                break
            except EOFError:
                break

        print("\nGoodbye!")


def main():
    """Main entry point."""
    cli = YouTubeMusicCLI()
    cli.run()


if __name__ == "__main__":
    main()
