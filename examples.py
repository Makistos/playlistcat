#!/usr/bin/env python3
"""
Example usage of PlaylistCat with authentication features
"""

# Example public playlist IDs for testing (these may or may not work depending on availability)
EXAMPLE_PLAYLISTS = {
    "Pop Hits": "RDCLAK5uy_l8gNZK16IbBfJhwO9Anh5sV8dA1N2Kv_o",  # YouTube's Pop Hits
    "Top Charts": "RDCLAK5uy_lf8okgl2ygD075nMiY-lOGjoPquE8E8Y8",  # YouTube's Top Charts
    "Your Mix": "RDCLAK5uy_lKhOSSxZdG7tF2L_TQBFb5X1KQ2Q3",  # Sample mix
}

def main():
    print("PlaylistCat 🐱 - Example Usage")
    print("=" * 50)
    print()

    print("🔓 UNAUTHENTICATED MODE (No Login Required)")
    print("-" * 50)
    print("Here are some example PUBLIC playlist IDs you can try:")
    print()

    for name, playlist_id in EXAMPLE_PLAYLISTS.items():
        print(f"  {name}: {playlist_id}")

    print()
    print("To use these:")
    print("1. Run the application: ./run.sh")
    print("2. Enter one of the playlist IDs above")
    print("3. Click 'Fetch Playlist' or press Enter")
    print()

    print("🔐 AUTHENTICATED MODE (Login Required)")
    print("-" * 50)
    print("To access YOUR personal playlists:")
    print()
    print("1. Run the application: ./run.sh")
    print("2. Click 'Login' in the Authentication section")
    print("3. Follow the setup wizard:")
    print("   - Open YouTube Music in browser")
    print("   - Open Developer Tools (F12)")
    print("   - Go to Network tab")
    print("   - Refresh the page")
    print("   - Copy a request as cURL")
    print("   - Paste into PlaylistCat")
    print("4. Select from your personal playlists dropdown")
    print()

    print("🎯 FEATURES COMPARISON")
    print("-" * 50)
    print("Unauthenticated Mode:")
    print("  ✓ Access to public playlists")
    print("  ✓ Manual playlist ID entry")
    print("  ✓ All viewing and sorting features")
    print("  ✗ No personal playlist access")
    print()
    print("Authenticated Mode:")
    print("  ✓ All unauthenticated features")
    print("  ✓ Personal playlist browsing")
    print("  ✓ Playlist dropdown selection")
    print("  ✓ Access to private playlists")
    print("  ✓ Real-time playlist updates")
    print()

    print("💡 TIPS")
    print("-" * 50)
    print("- Start with unauthenticated mode to try the app")
    print("- Use authentication only if you need personal playlists")
    print("- Both modes work simultaneously - no restrictions")
    print("- Authentication is optional and can be set up later")
    print("- Logout anytime to return to unauthenticated mode")
    print()

    print("🔍 HOW TO GET PLAYLIST IDs")
    print("-" * 50)
    print("For public playlists:")
    print("1. Go to YouTube Music (music.youtube.com)")
    print("2. Open any public playlist")
    print("3. Copy the URL")
    print("4. Extract the part after 'list=' in the URL")
    print()
    print("For your playlists:")
    print("1. Login to PlaylistCat (see Authentication Mode above)")
    print("2. Select from dropdown - no manual ID needed!")
    print()

if __name__ == "__main__":
    main()
