#!/usr/bin/env python3
"""
Try to understand what ytmusicapi expects for browser authentication
"""

import os
import json
import tempfile

def test_minimal_working_auth():
    """Test the minimal auth structure that might work"""

    print("🔍 Testing Minimal Working Authentication Structures")
    print("=" * 60)

    # Test 1: Try the absolute minimal structure
    print("1️⃣ Testing absolute minimal structure...")
    minimal_auth = {
        "cookie": "YSC=5l6anihbkUE; SID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFIzGDNUzqWpoE95SicaCYHgACgYKAR8SARMSFQHGX2MiyurZOmqfxRSQb5wxGUPNyxoVAUF8yKpMEcuCZRbWYzsl23MzKE3i0076; HSID=AUdfcDsEyLyU0aMxN; SSID=A7lgSt3ejC0m-NnKu; APISID=80Y1DtGXjedfQDN_/A9i5sh07t8wXmB9U8; SAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f"
    }

    test_auth_structure(minimal_auth, "minimal")

    # Test 2: Try browser-like structure (lowercase keys)
    print("\n2️⃣ Testing browser-like structure...")
    browser_auth = {
        "cookie": "YSC=5l6anihbkUE; SID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFIzGDNUzqWpoE95SicaCYHgACgYKAR8SARMSFQHGX2MiyurZOmqfxRSQb5wxGUPNyxoVAUF8yKpMEcuCZRbWYzsl23MzKE3i0076; HSID=AUdfcDsEyLyU0aMxN; SSID=A7lgSt3ejC0m-NnKu; APISID=80Y1DtGXjedfQDN_/A9i5sh07t8wXmB9U8; SAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f",
        "x-goog-authuser": "0"
    }

    test_auth_structure(browser_auth, "browser_minimal")

    # Test 3: Try adding more browser headers
    print("\n3️⃣ Testing extended browser structure...")
    extended_auth = {
        "cookie": "YSC=5l6anihbkUE; SID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFIzGDNUzqWpoE95SicaCYHgACgYKAR8SARMSFQHGX2MiyurZOmqfxRSQb5wxGUPNyxoVAUF8yKpMEcuCZRbWYzsl23MzKE3i0076; HSID=AUdfcDsEyLyU0aMxN; SSID=A7lgSt3ejC0m-NnKu; APISID=80Y1DtGXjedfQDN_/A9i5sh07t8wXmB9U8; SAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f",
        "x-goog-authuser": "0",
        "origin": "https://music.youtube.com"
    }

    test_auth_structure(extended_auth, "extended")

    # Test 4: Try without any JSON at all - just pass the session
    print("\n4️⃣ Testing session-only approach with manual headers...")
    test_session_only()

def test_auth_structure(auth_data, name):
    """Test a specific auth structure"""
    auth_file = f'/tmp/test_auth_{name}.json'

    try:
        # Create auth file
        with open(auth_file, 'w') as f:
            json.dump(auth_data, f, indent=2)

        print(f"   Created {name} auth file")

        # Test with YTMusic
        from ytmusicapi import YTMusic
        ytmusic = YTMusic(auth_file)

        # Try library access
        playlists = ytmusic.get_library_playlists(limit=1)
        print(f"   ✅ {name} SUCCESS: {len(playlists)} playlists")
        return True

    except Exception as e:
        print(f"   ❌ {name} failed: {str(e)[:100]}...")
        return False

    finally:
        if os.path.exists(auth_file):
            os.unlink(auth_file)

def test_session_only():
    """Test using only session without any auth file"""
    try:
        import requests
        from ytmusicapi import YTMusic

        # Create session with all necessary headers
        session = requests.Session()
        session.headers.update({
            'Cookie': 'YSC=5l6anihbkUE; SID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFIzGDNUzqWpoE95SicaCYHgACgYKAR8SARMSFQHGX2MiyurZOmqfxRSQb5wxGUPNyxoVAUF8yKpMEcuCZRbWYzsl23MzKE3i0076; HSID=AUdfcDsEyLyU0aMxN; SSID=A7lgSt3ejC0m-NnKu; APISID=80Y1DtGXjedfQDN_/A9i5sh07t8wXmB9U8; SAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
            'X-Goog-AuthUser': '0',
            'Accept': '*/*',
            'Origin': 'https://music.youtube.com',
            'Referer': 'https://music.youtube.com/',
            'X-Goog-Visitor-Id': 'CgtqQUtaRHhZaFBaZyi8tsLFBjInCgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd',
            'X-YouTube-Client-Name': '67',
            'X-YouTube-Client-Version': '1.20250825.03.01',
        })

        print("   Creating YTMusic with session...")
        ytmusic = YTMusic(requests_session=session)

        print("   Testing direct API call first...")
        # Test with a direct API call to see if session works
        response = session.get('https://music.youtube.com/verify_session')
        print(f"   Direct API status: {response.status_code}")

        print("   Trying library playlists...")
        playlists = ytmusic.get_library_playlists(limit=1)
        print(f"   ✅ Session-only SUCCESS: {len(playlists)} playlists")
        return True

    except Exception as e:
        print(f"   ❌ Session-only failed: {str(e)[:100]}...")
        return False

def check_ytmusicapi_version():
    """Check what version and methods are available"""
    print("\n🔍 Checking ytmusicapi details...")

    try:
        import ytmusicapi
        print(f"Version: {ytmusicapi.__version__}")

        # Check YTMusic constructor
        from ytmusicapi import YTMusic
        import inspect
        sig = inspect.signature(YTMusic.__init__)
        print(f"Constructor params: {list(sig.parameters.keys())}")

        # Check if there are any other auth methods
        methods = [method for method in dir(YTMusic) if 'auth' in method.lower()]
        print(f"Auth-related methods: {methods}")

    except Exception as e:
        print(f"Error checking ytmusicapi: {e}")

if __name__ == "__main__":
    check_ytmusicapi_version()
    test_minimal_working_auth()
