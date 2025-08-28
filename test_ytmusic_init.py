#!/usr/bin/env python3
"""
Test YTMusic initialization methods
"""

import os
import json
import tempfile

def test_ytmusic_init():
    """Test different ways to initialize YTMusic"""

    print("🔍 Testing YTMusic initialization methods")
    print("=" * 50)

    # Test 1: No authentication (should work)
    try:
        print("1️⃣ Testing without authentication...")
        from ytmusicapi import YTMusic
        ytmusic = YTMusic()
        print("✅ Unauthenticated YTMusic works")
    except Exception as e:
        print(f"❌ Unauthenticated failed: {e}")

    # Test 2: Check what parameters YTMusic accepts
    try:
        print("\n2️⃣ Checking YTMusic constructor signature...")
        import inspect
        sig = inspect.signature(YTMusic.__init__)
        print(f"YTMusic.__init__ parameters: {list(sig.parameters.keys())}")
    except Exception as e:
        print(f"❌ Could not inspect: {e}")

    # Test 3: Try with auth parameter as None
    try:
        print("\n3️⃣ Testing with auth=None...")
        ytmusic = YTMusic(auth=None)
        print("✅ YTMusic(auth=None) works")
    except Exception as e:
        print(f"❌ auth=None failed: {e}")

    # Test 4: Try with a string path that doesn't exist
    try:
        print("\n4️⃣ Testing with non-existent file path...")
        ytmusic = YTMusic("nonexistent.json")
        print("✅ Non-existent file works (unexpected)")
    except Exception as e:
        print(f"✅ Non-existent file correctly failed: {e}")

    # Test 5: Try to understand what the error means
    print("\n5️⃣ Investigating the OAuth error...")

    # Create a minimal auth file
    auth_data = {"cookie": "test=value", "X-Goog-AuthUser": "0"}
    test_file = '/tmp/oauth_test.json'

    try:
        with open(test_file, 'w') as f:
            json.dump(auth_data, f)

        ytmusic = YTMusic(test_file)
        print("✅ Simple auth file works")

    except Exception as e:
        print(f"❌ Simple auth failed: {e}")

        # Let's see what ytmusicapi expects for OAuth vs browser auth
        error_str = str(e)
        if "oauth_credentials" in error_str:
            print("🔍 The library is expecting oauth_credentials in the auth file")
            print("🔍 This suggests it's trying to use OAuth mode instead of browser mode")

    finally:
        if os.path.exists(test_file):
            os.unlink(test_file)

    # Test 6: Try the actual auth format that might work
    print("\n6️⃣ Testing with potential correct format...")

    # Based on the error, maybe we need to use a different initialization method
    try:
        print("Trying to find setup function...")
        from ytmusicapi.setup import setup_oauth
        print("✅ Found setup_oauth function")
    except ImportError:
        print("❌ No setup_oauth function")

    try:
        from ytmusicapi.setup import setup
        print("✅ Found setup function")

        # Try to see what this setup function expects
        import inspect
        sig = inspect.signature(setup)
        print(f"setup parameters: {list(sig.parameters.keys())}")

    except Exception as e:
        print(f"❌ setup function issue: {e}")

if __name__ == "__main__":
    test_ytmusic_init()
