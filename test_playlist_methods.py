#!/usr/bin/env python3

"""
Test script to explore different YouTube Music API methods for getting playlists
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from auth import AuthenticationManager

def test_playlist_methods():
    """Test different playlist retrieval methods"""

    # Initialize auth manager
    auth_manager = AuthenticationManager()

    # Check if authenticated
    if not auth_manager.is_authenticated:
        print("❌ Not authenticated. Please authenticate first.")
        return

    ytmusic = auth_manager.ytmusic
    if not ytmusic:
        print("❌ No YTMusic instance available")
        return

    print("🔍 Testing different playlist retrieval methods...")
    print("=" * 60)

    # Method 1: get_library_playlists
    print("\n1️⃣ Testing get_library_playlists():")
    try:
        result1 = ytmusic.get_library_playlists(limit=10)
        print(f"   Type: {type(result1)}")
        print(f"   Length: {len(result1) if result1 else 'None'}")
        if result1:
            print(f"   First item: {result1[0] if len(result1) > 0 else 'Empty'}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Method 2: get_library_playlists with no limit
    print("\n2️⃣ Testing get_library_playlists() with no limit:")
    try:
        result2 = ytmusic.get_library_playlists()
        print(f"   Type: {type(result2)}")
        print(f"   Length: {len(result2) if result2 else 'None'}")
        if result2:
            print(f"   First item: {result2[0] if len(result2) > 0 else 'Empty'}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Method 3: Check if there are other methods
    print("\n3️⃣ Available methods containing 'playlist':")
    playlist_methods = [method for method in dir(ytmusic) if 'playlist' in method.lower()]
    for method in playlist_methods:
        print(f"   - {method}")

    # Method 4: Try get_playlists if it exists
    if hasattr(ytmusic, 'get_playlists'):
        print("\n4️⃣ Testing get_playlists():")
        try:
            result4 = ytmusic.get_playlists()
            print(f"   Type: {type(result4)}")
            print(f"   Length: {len(result4) if result4 else 'None'}")
            if result4:
                print(f"   First item: {result4[0] if len(result4) > 0 else 'Empty'}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    # Method 5: Try searching for playlists
    print("\n5️⃣ Testing search for user's playlists:")
    try:
        # Search for playlists to see if any exist
        search_result = ytmusic.search("", filter="playlists", limit=10)
        print(f"   Type: {type(search_result)}")
        print(f"   Length: {len(search_result) if search_result else 'None'}")
        if search_result:
            print(f"   First item: {search_result[0] if len(search_result) > 0 else 'Empty'}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_playlist_methods()
