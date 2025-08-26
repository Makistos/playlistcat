#!/usr/bin/env python3
"""
Example usage of PlaylistCat
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
    print("Here are some example playlist IDs you can try:")
    print()

    for name, playlist_id in EXAMPLE_PLAYLISTS.items():
        print(f"{name}: {playlist_id}")

    print()
    print("To use these:")
    print("1. Run the application: ./run.sh")
    print("2. Enter one of the playlist IDs above")
    print("3. Click 'Fetch Playlist' or press Enter")
    print()
    print("Note: These are public playlists from YouTube Music.")
    print("If they don't work, try finding your own public playlist ID.")
    print()
    print("How to get your own playlist ID:")
    print("1. Go to YouTube Music (music.youtube.com)")
    print("2. Open any public playlist")
    print("3. Copy the URL")
    print("4. Extract the part after 'list=' in the URL")
    print()

if __name__ == "__main__":
    main()
