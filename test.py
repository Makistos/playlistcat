#!/usr/bin/env python3
"""
Simple test to verify the application can import all required modules
"""

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import ytmusicapi
        print("✓ ytmusicapi imported successfully")
    except ImportError as e:
        print(f"✗ ytmusicapi import failed: {e}")
        return False
    
    try:
        from PyQt6.QtWidgets import QApplication
        print("✓ PyQt6 imported successfully")
    except ImportError as e:
        print(f"✗ PyQt6 import failed: {e}")
        print("  Note: This is expected in headless environments")
    
    try:
        import sys
        sys.path.append('src')
        from utils import extract_playlist_id, validate_playlist_id
        print("✓ Utils module imported successfully")
    except ImportError as e:
        print(f"✗ Utils import failed: {e}")
        return False
    
    return True

def test_utils():
    """Test utility functions."""
    print("\nTesting utility functions...")
    
    import sys
    sys.path.append('src')
    from utils import extract_playlist_id, validate_playlist_id
    
    # Test playlist ID extraction
    test_id = extract_playlist_id("https://music.youtube.com/playlist?list=PLtest123")
    if test_id == "PLtest123":
        print("✓ Playlist ID extraction works")
    else:
        print(f"✗ Playlist ID extraction failed: got {test_id}")
        return False
    
    # Test validation
    if validate_playlist_id("PLtest123456789"):
        print("✓ Playlist ID validation works")
    else:
        print("✗ Playlist ID validation failed")
        return False
    
    return True

def test_ytmusic_api():
    """Test YouTube Music API initialization."""
    print("\nTesting YouTube Music API...")
    
    try:
        from ytmusicapi import YTMusic
        ytmusic = YTMusic()
        print("✓ YouTube Music API initialized successfully")
        return True
    except Exception as e:
        print(f"✗ YouTube Music API initialization failed: {e}")
        return False

def main():
    """Run all tests."""
    print("PlaylistCat 🐱 - System Test")
    print("=" * 50)
    
    all_passed = True
    
    all_passed &= test_imports()
    all_passed &= test_utils()
    all_passed &= test_ytmusic_api()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All tests passed! The application should work correctly.")
    else:
        print("✗ Some tests failed. Check the errors above.")
    
    print("\nTo run the application:")
    print("  GUI: ./run.sh")
    print("  CLI: ./run.sh --cli")

if __name__ == "__main__":
    main()
