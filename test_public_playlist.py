#!/usr/bin/env python3

from ytmusicapi import YTMusic
import json

def test_public_playlist_structure():
    print("🔍 Testing public playlist structure...")

    # Use a public playlist (example ID - you might need to update this)
    # Let's use the anonymous YTMusic API first
    yt = YTMusic()

    # Test with a public playlist ID
    public_playlist_id = "RDCLAK5uy_k8nXKXKKFQGAEgBQpGwqNlDQC"  # Example public playlist

    try:
        print(f"📋 Fetching public playlist: {public_playlist_id}")
        playlist_data = yt.get_playlist(public_playlist_id, limit=2)

        if not playlist_data:
            print("❌ Could not fetch playlist")
            return

        print(f"✅ Playlist found: {playlist_data.get('title', 'Unknown')}")

        tracks = playlist_data.get('tracks', [])
        if not tracks:
            print("❌ No tracks found")
            return

        print(f"📊 Found {len(tracks)} tracks")

        # Examine first track
        track = tracks[0]
        print(f"\n🎵 Track: {track.get('title', 'Unknown')}")
        print("🔍 Available keys:")
        for key in sorted(track.keys()):
            value = track[key]
            if isinstance(value, (str, int, bool)):
                print(f"  {key}: {value}")
            elif isinstance(value, list) and value:
                print(f"  {key}: [list with {len(value)} items]")
            elif isinstance(value, dict):
                print(f"  {key}: {{dict with {len(value)} keys}}")
            else:
                print(f"  {key}: {type(value).__name__}")

        # Check for setVideoId
        if 'setVideoId' in track:
            print(f"\n✅ setVideoId found: {track['setVideoId']}")
        else:
            print(f"\n❌ setVideoId not found")

        # Check what fields we'd need for removal
        video_id = track.get('videoId', '')
        set_video_id = track.get('setVideoId', '')

        print(f"\n📋 For removal, we would need:")
        print(f"  videoId: {video_id}")
        print(f"  setVideoId: {set_video_id}")

        if video_id and set_video_id:
            print("✅ All required fields available for removal")
        else:
            print("❌ Missing required fields for removal")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_public_playlist_structure()
