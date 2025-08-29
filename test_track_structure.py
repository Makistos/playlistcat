#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src')

from auth import AuthenticationManager
import json

def test_track_structure():
    print("🔍 Testing track structure for remove functionality...")

    auth_manager = AuthenticationManager()

    # Load existing auth
    if not auth_manager.load_saved_auth():
        print("❌ No saved authentication found")
        return

    ytmusic = auth_manager.get_ytmusic()
    if not ytmusic:
        print("❌ Could not get YTMusic instance")
        return

    print("✅ Authentication loaded")

    try:
        # Get user playlists
        playlists = auth_manager.get_user_playlists()
        if not playlists:
            print("❌ No playlists found")
            return

        print(f"✅ Found {len(playlists)} playlists")

        # Use first playlist that has tracks
        for playlist in playlists:
            playlist_id = playlist['playlistId']
            print(f"\n🎵 Checking playlist: {playlist['title']} ({playlist_id})")

            playlist_data = ytmusic.get_playlist(playlist_id, limit=3)
            if playlist_data and 'tracks' in playlist_data and playlist_data['tracks']:
                tracks = playlist_data['tracks']
                print(f"📊 Found {len(tracks)} tracks")

                # Examine first track structure
                if tracks:
                    track = tracks[0]
                    print(f"\n🔍 Track structure for: {track.get('title', 'Unknown')}")
                    print("Available keys:")
                    for key in sorted(track.keys()):
                        value = track[key]
                        if isinstance(value, (str, int)):
                            print(f"  {key}: {value}")
                        else:
                            print(f"  {key}: {type(value).__name__}")

                    # Check for setVideoId specifically
                    if 'setVideoId' in track:
                        print(f"\n✅ setVideoId found: {track['setVideoId']}")
                        print(f"✅ videoId found: {track.get('videoId', 'N/A')}")

                        # Test remove structure
                        remove_item = {
                            'videoId': track['videoId'],
                            'setVideoId': track['setVideoId']
                        }
                        print(f"\n📋 Remove item structure: {remove_item}")
                        return True
                    else:
                        print("\n❌ setVideoId not found in track")
                        return False

                break

        print("❌ No playlists with tracks found")
        return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_track_structure()
