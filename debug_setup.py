#!/usr/bin/env python3
"""
Debug what the setup function is creating
"""

import os
import json
import tempfile

def debug_setup_output():
    """See what ytmusicapi.setup creates"""

    # Sample headers like the ones we have
    headers_raw = """Cookie: YSC=5l6anihbkUE; SID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFIzGDNUzqWpoE95SicaCYHgACgYKAR8SARMSFQHGX2MiyurZOmqfxRSQb5wxGUPNyxoVAUF8yKpMEcuCZRbWYzsl23MzKE3i0076; HSID=AUdfcDsEyLyU0aMxN; SSID=A7lgSt3ejC0m-NnKu; APISID=80Y1DtGXjedfQDN_/A9i5sh07t8wXmB9U8; SAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f
X-Goog-AuthUser: 0
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
X-Goog-Visitor-Id: CgtqQUtaRHhZaFBaZyi8tsLFBjInCgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd
X-YouTube-Client-Name: 67
X-YouTube-Client-Version: 1.20250825.03.01"""

    debug_file = '/tmp/debug_ytmusic_setup.json'

    try:
        from ytmusicapi.setup import setup

        print("🔍 Creating auth file with setup()...")
        setup(filepath=debug_file, headers_raw=headers_raw)

        print(f"✅ Auth file created: {debug_file}")

        # Read and display the contents
        with open(debug_file, 'r') as f:
            content = json.load(f)

        print("\n📄 Auth file contents:")
        print(json.dumps(content, indent=2))

        # Check what type of auth this is
        if 'oauth_credentials' in content:
            print("\n🔍 Analysis: This is OAuth authentication")
        elif 'cookie' in content:
            print("\n🔍 Analysis: This is browser/cookie authentication")
        else:
            print("\n🔍 Analysis: Unknown authentication type")

        print(f"\n📊 Keys in auth file: {list(content.keys())}")

        # Test with YTMusic
        print("\n🧪 Testing with YTMusic...")
        from ytmusicapi import YTMusic

        ytmusic = YTMusic(debug_file)
        print("✅ YTMusic initialized successfully")

    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")

        if os.path.exists(debug_file):
            print(f"\n📄 Checking auth file that was created...")
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

if __name__ == "__main__":
    debug_setup_output()
