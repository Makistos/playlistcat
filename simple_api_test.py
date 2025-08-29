#!/usr/bin/env python3

"""
Simple test to check YouTube Music API response
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_simple_api():
    """Simple test of ytmusicapi"""
    try:
        from ytmusicapi import YTMusic

        # Check if we have saved authentication
        auth_file = "headers_auth.json"
        if not os.path.exists(auth_file):
            print("❌ No authentication file found. Please authenticate first.")
            return

        print(f"🔍 Loading authentication from {auth_file}")
        ytmusic = YTMusic(auth_file)

        print("✅ YTMusic instance created successfully")

        # Test basic API call
        print("\n🎵 Testing get_library_playlists()...")
        try:
            playlists = ytmusic.get_library_playlists()
            print(f"📋 Response type: {type(playlists)}")
            print(f"📋 Response: {playlists}")
            print(f"📋 Length: {len(playlists) if playlists else 'None'}")

            if playlists:
                print(f"📋 First playlist: {playlists[0]}")
            else:
                print("📋 No playlists found")

        except Exception as e:
            print(f"❌ API call failed: {e}")

        # Test if user has any library content
        print("\n🎵 Testing get_library_songs()...")
        try:
            songs = ytmusic.get_library_songs(limit=1)
            print(f"🎵 Songs response: {len(songs) if songs else 0} songs")
        except Exception as e:
            print(f"❌ Songs API call failed: {e}")

        # Test if user has any library albums
        print("\n💿 Testing get_library_albums()...")
        try:
            albums = ytmusic.get_library_albums(limit=1)
            print(f"💿 Albums response: {len(albums) if albums else 0} albums")
        except Exception as e:
            print(f"❌ Albums API call failed: {e}")

    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_simple_api()
