#!/usr/bin/env python3
"""
Test proper browser authentication setup
"""

import os
import json
import tempfile

def test_browser_auth_proper():
    """Test browser authentication the correct way"""

    print("🔍 Testing proper browser authentication setup")
    print("=" * 50)

    # Let's try to understand what the setup function actually needs
    test_file = '/tmp/browser_auth_test.json'

    try:
        print("1️⃣ Using ytmusicapi.setup with raw headers...")
        from ytmusicapi.setup import setup

        # Raw headers string as it would come from browser
        headers_raw = """Cookie: YSC=5l6anihbkUE; SID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFIzGDNUzqWpoE95SicaCYHgACgYKAR8SARMSFQHGX2MiyurZOmqfxRSQb5wxGUPNyxoVAUF8yKpMEcuCZRbWYzsl23MzKE3i0076; HSID=AUdfcDsEyLyU0aMxN; SSID=A7lgSt3ejC0m-NnKu; APISID=80Y1DtGXjedfQDN_/A9i5sh07t8wXmB9U8; SAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f
X-Goog-AuthUser: 0"""

        setup(filepath=test_file, headers_raw=headers_raw)
        print(f"✅ Setup created file: {test_file}")

        # Look at what it created
        with open(test_file, 'r') as f:
            content = json.load(f)

        print("📄 File structure:")
        for key in content.keys():
            print(f"  - {key}")

        # Now try to use it with YTMusic
        print("\n2️⃣ Testing with YTMusic...")
        from ytmusicapi import YTMusic

        ytmusic = YTMusic(test_file)
        print("✅ YTMusic initialized successfully!")

        # Try library access
        print("🎵 Testing library access...")
        playlists = ytmusic.get_library_playlists(limit=1)
        print(f"✅ Library access worked! Found {len(playlists)} playlists")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")

        # If the file was created, let's see what's in it
        if os.path.exists(test_file):
            print("\n📄 Checking created file:")
            try:
                with open(test_file, 'r') as f:
                    content = json.load(f)
                print(json.dumps(content, indent=2)[:500] + "...")  # First 500 chars
            except Exception as read_error:
                print(f"Could not read file: {read_error}")

        return False

    finally:
        # Clean up
        if os.path.exists(test_file):
            os.unlink(test_file)
            print(f"\n🧹 Cleaned up: {test_file}")

def test_minimal_working_setup():
    """Try to create the minimal working setup"""

    print("\n" + "="*50)
    print("🧪 Testing minimal working browser auth")

    test_file = '/tmp/minimal_browser_auth.json'

    try:
        print("Creating minimal browser auth file manually...")

        # The difference might be in the structure or specific keys
        # Let's try the exact structure that should work for browser auth
        minimal_auth = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "content-encoding": "gzip",
            "content-type": "application/json",
            "cookie": "YSC=5l6anihbkUE; SID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFIzGDNUzqWpoE95SicaCYHgACgYKAR8SARMSFQHGX2MiyurZOmqfxRSQb5wxGUPNyxoVAUF8yKpMEcuCZRbWYzsl23MzKE3i0076; HSID=AUdfcDsEyLyU0aMxN; SSID=A7lgSt3ejC0m-NnKu; APISID=80Y1DtGXjedfQDN_/A9i5sh07t8wXmB9U8; SAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f",
            "origin": "https://music.youtube.com",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
            "x-goog-authuser": "0"
        }

        with open(test_file, 'w') as f:
            json.dump(minimal_auth, f, indent=2)

        print(f"✅ Created minimal auth file: {test_file}")

        # Try to use it directly without oauth_credentials
        print("Testing with YTMusic(auth_file)...")
        from ytmusicapi import YTMusic

        # Let's try different initialization methods

        # Method 1: Direct file path
        try:
            ytmusic = YTMusic(test_file)
            print("✅ Method 1 (direct file) worked!")
            return True
        except Exception as e1:
            print(f"❌ Method 1 failed: {e1}")

        # Method 2: Explicit auth parameter
        try:
            ytmusic = YTMusic(auth=test_file)
            print("✅ Method 2 (auth parameter) worked!")
            return True
        except Exception as e2:
            print(f"❌ Method 2 failed: {e2}")

        # Method 3: Pass the data directly (not file path)
        try:
            ytmusic = YTMusic(auth=minimal_auth)
            print("✅ Method 3 (direct data) worked!")
            return True
        except Exception as e3:
            print(f"❌ Method 3 failed: {e3}")

        return False

    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

    finally:
        if os.path.exists(test_file):
            os.unlink(test_file)
            print(f"🧹 Cleaned up: {test_file}")

if __name__ == "__main__":
    success1 = test_browser_auth_proper()
    success2 = test_minimal_working_setup()

    if success1 or success2:
        print("\n🎉 Found a working authentication method!")
    else:
        print("\n⚠️  Still searching for the right authentication method...")
