#!/usr/bin/env python3

"""
Test different playlist methods to find the right one
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from auth import AuthenticationManager

def test_playlist_methods():
    """Test the correct playlist method"""

    auth_manager = AuthenticationManager()

    # Check if authenticated
    if not auth_manager.is_authenticated:
        print("❌ Not authenticated. Please authenticate first.")
        return

    ytmusic = auth_manager.ytmusic
    if not ytmusic:
        print("❌ No YTMusic instance available")
        return

    print("🔍 Testing playlist methods...")
    print("=" * 50)

    # Test get_user_playlists - this looks promising!
    print("\n🎯 Testing get_user_playlists():")
    try:
        # This method might need a channel ID - let's try without first
        result = ytmusic.get_user_playlists()
        print(f"   Type: {type(result)}")
        print(f"   Length: {len(result) if result else 'None'}")
        if result:
            print(f"   First item: {result[0] if len(result) > 0 else 'Empty'}")
        else:
            print("   Empty result - might need channel ID")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("   This method might require a channel ID parameter")

    # Test get_library_playlists vs get_user_playlists
    print("\n📚 Testing get_library_playlists() vs other methods:")
    try:
        library_playlists = ytmusic.get_library_playlists()
        print(f"   Library playlists: {len(library_playlists) if library_playlists else 0}")
    except Exception as e:
        print(f"   ❌ Library playlists error: {e}")

    # Check if we can get account info to find channel ID
    print("\n👤 Checking account info:")
    try:
        # Try to get account info that might contain channel ID
        account_info = ytmusic.get_account_info()
        print(f"   Account info: {account_info}")

        if account_info and 'channelId' in account_info:
            channel_id = account_info['channelId']
            print(f"   Found channel ID: {channel_id}")

            # Now try get_user_playlists with channel ID
            print(f"\n🎯 Testing get_user_playlists('{channel_id}'):")
            user_playlists = ytmusic.get_user_playlists(channel_id)
            print(f"   Type: {type(user_playlists)}")
            print(f"   Length: {len(user_playlists) if user_playlists else 'None'}")
            if user_playlists:
                print(f"   First playlist: {user_playlists[0]}")
    except Exception as e:
        print(f"   ❌ Account info error: {e}")

if __name__ == "__main__":
    test_playlist_methods()
