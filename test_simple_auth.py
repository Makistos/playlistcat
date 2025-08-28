#!/usr/bin/env python3
"""
Test simple manual auth file creation
"""

import os
import json
import tempfile

def test_simple_auth():
    """Test with minimal auth data"""

    # Create minimal auth data
    auth_data = {
        "cookie": "YSC=5l6anihbkUE; SID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFIzGDNUzqWpoE95SicaCYHgACgYKAR8SARMSFQHGX2MiyurZOmqfxRSQb5wxGUPNyxoVAUF8yKpMEcuCZRbWYzsl23MzKE3i0076; HSID=AUdfcDsEyLyU0aMxN; SSID=A7lgSt3ejC0m-NnKu; APISID=80Y1DtGXjedfQDN_/A9i5sh07t8wXmB9U8; SAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f",
        "X-Goog-AuthUser": "0"
    }

    debug_file = '/tmp/simple_auth.json'

    try:
        print("🔍 Creating simple auth file...")
        with open(debug_file, 'w') as f:
            json.dump(auth_data, f, indent=2)

        print(f"✅ Auth file created: {debug_file}")

        # Read and display the contents
        with open(debug_file, 'r') as f:
            content = json.load(f)

        print("\n📄 Auth file contents:")
        print(json.dumps(content, indent=2))

        # Test with YTMusic
        print("\n🧪 Testing with YTMusic...")
        from ytmusicapi import YTMusic

        ytmusic = YTMusic(debug_file)
        print("✅ YTMusic initialized successfully")

        # Try to access library
        print("🎵 Testing library access...")
        playlists = ytmusic.get_library_playlists(limit=1)
        print(f"✅ Found {len(playlists)} playlists")

    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")

        # Let's see what's in the file anyway
        if os.path.exists(debug_file):
            print(f"\n📄 Auth file contents:")
            try:
                with open(debug_file, 'r') as f:
                    content = json.load(f)
                print(json.dumps(content, indent=2))
            except:
                print("Could not read auth file")

    finally:
        # Clean up
        if os.path.exists(debug_file):
            os.unlink(debug_file)
            print(f"\n🧹 Cleaned up: {debug_file}")

def test_working_example():
    """Test with a structure that's known to work"""

    print("\n" + "="*50)
    print("🧪 Testing working example structure")

    # This is the structure that should work for browser auth
    auth_data = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate",
        "content-encoding": "gzip",
        "content-type": "application/json",
        "cookie": "YSC=5l6anihbkUE; SID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFIzGDNUzqWpoE95SicaCYHgACgYKAR8SARMSFQHGX2MiyurZOmqfxRSQb5wxGUPNyxoVAUF8yKpMEcuCZRbWYzsl23MzKE3i0076; HSID=AUdfcDsEyLyU0aMxN; SSID=A7lgSt3ejC0m-NnKu; APISID=80Y1DtGXjedfQDN_/A9i5sh07t8wXmB9U8; SAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f",
        "origin": "https://music.youtube.com",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "x-goog-authuser": "0",
        "x-goog-visitor-id": "CgtqQUtaRHhZaFBaZyi8tsLFBjInCgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd",
        "x-youtube-client-name": "67",
        "x-youtube-client-version": "1.20250825.03.01"
    }

    debug_file = '/tmp/working_auth.json'

    try:
        print("🔍 Creating working auth file...")
        with open(debug_file, 'w') as f:
            json.dump(auth_data, f, indent=2)

        print(f"✅ Auth file created: {debug_file}")

        # Test with YTMusic
        print("🧪 Testing with YTMusic...")
        from ytmusicapi import YTMusic

        ytmusic = YTMusic(debug_file)
        print("✅ YTMusic initialized successfully")

        # Try to access library
        print("🎵 Testing library access...")
        playlists = ytmusic.get_library_playlists(limit=1)
        print(f"✅ Found {len(playlists)} playlists")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

    finally:
        # Clean up
        if os.path.exists(debug_file):
            os.unlink(debug_file)
            print(f"🧹 Cleaned up: {debug_file}")

if __name__ == "__main__":
    print("🔍 Testing Simple Authentication Methods")
    print("=" * 50)

    test_simple_auth()
    success = test_working_example()

    if success:
        print("\n🎉 Found working authentication format!")
    else:
        print("\n⚠️  Authentication still not working")
