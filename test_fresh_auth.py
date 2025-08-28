#!/usr/bin/env python3
"""
Test authentication with the fresh cURL command from the user
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from auth import AuthenticationManager

def test_fresh_auth():
    """Test authentication with the user's fresh cURL command"""

    print("🔍 Testing Fresh Authentication Headers")
    print("=" * 50)

    # Headers extracted from the fresh cURL command
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://music.youtube.com/',
        'DNT': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Cookie': 'YSC=5l6anihbkUE; SOCS=CAESNQgREitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjUwODI0LjA5X3AwGgJlbiACGgYIgPKzxQY; VISITOR_PRIVACY_METADATA=CgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd; PREF=f6=80^&repeat=NONE^&autoplay=true^&tz=Europe.Helsinki^&f5=30000; __Secure-1PSIDTS=sidts-CjUB5H03P263q8VzRdG9tQrHGLfaEinyW0yVPlmuJGF3iCoT4r3bANdKeNFaRHJexPkcCto6CBAA; __Secure-3PSIDTS=sidts-CjUB5H03P263q8VzRdG9tQrHGLfaEinyW0yVPlmuJGF3iCoT4r3bANdKeNFaRHJexPkcCto6CBAA; HSID=AUdfcDsEyLyU0aMxN; SSID=A7lgSt3ejC0m-NnKu; APISID=80Y1DtGXjedfQDN_/A9i5sh07t8wXmB9U8; SAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f; __Secure-1PAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f; __Secure-3PAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f; SID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFIzGDNUzqWpoE95SicaCYHgACgYKAR8SARMSFQHGX2MiyurZOmqfxRSQb5wxGUPNyxoVAUF8yKpMEcuCZRbWYzsl23MzKE3i0076; __Secure-1PSID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFV6Q3TQ4YA1PrVSp-E_xTjgACgYKAR0SARMSFQHGX2MicXxTwKEEDh50pHzM5glYPRoVAUF8yKo4kYCi-lWL6BcgL1gTLRJx0076; __Secure-3PSID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFs9a74j17SLZ4rCN8mmfLcwACgYKAQwSARMSFQHGX2MiggfMVUzNikW-rmLMc8IT9BoVAUF8yKrvCPBEpcLiMv2RPvP3X6NC0076; LOGIN_INFO=AFmmF2swRQIhAOTjXRnPi18LYSGLxzE0rKIsWnUMYOR9rFCzYw_A0R25AiBvXbK1P_QpDSpvBlozOLIH7FPsFHIVGrM24F2ql5JFJg:QUQ3MjNmeFprN1NxVnJaQTFDa0x4Y2ZkN2FwVWhtbElwTENPN3RXWGZnRHZSNEJTWjR0clQ1U0loRXVxOWNwZ2QwSnRscjVwc09KS3NIaU55cnAwZTkyYWZxX3lrbmtNSjZ2Y0U4VjVhMXhRYWFLclNXZDhtcXBqYWxtc21Wd3FTeXhvdTJlU1BoRGhSd2JCNlN3QVZLaExrUFpmeTFkc1lB; __Secure-ROLLOUT_TOKEN=COvHqt-25Zm9XBD_rcDuo6mPAxiSntri5auPAw%3D%3D; SIDCC=AKEyXzXRqT3nTQ-2lKkqgPhEDQOaO0OyWcwWKZu_YBU5_dKOeOZ0oaznlnCd977h2GAcwqtFdYo; __Secure-1PSIDCC=AKEyXzVBvi_3WdS2CDhqHHXv2R-xb06SISdBj9ytrG87uxtT1RtIHJsWAg1YH7lCWf259rP_mw; __Secure-3PSIDCC=AKEyXzV0F3_YzgebQSjcU0Joe81NC17L8Xo0Bqbg5GlkHn6I3R3DsBkrmOiqURFcnoOLBiy-XZ0; __Secure-YEC=CgtqQUtaRHhZaFBaZyjv6cLFBjInCgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd',
        'Priority': 'u=4',
        'TE': 'trailers'
    }

    try:
        print("🔧 Creating AuthenticationManager...")
        auth_manager = AuthenticationManager()

        print("📋 Testing fresh authentication...")
        success = auth_manager.authenticate_with_headers(headers)

        if success:
            print("✅ Authentication successful!")
            print(f"   Auth method: {auth_manager.user_info.get('auth_method', 'unknown')}")
            print(f"   Playlist count during auth: {auth_manager.user_info.get('playlists_count', 0)}")

            # Test playlist fetching
            print("\n🎵 Testing playlist fetching...")
            playlists = auth_manager.get_user_playlists()

            if playlists:
                print(f"✅ Successfully fetched {len(playlists)} playlists!")
                for i, playlist in enumerate(playlists[:5]):  # Show first 5
                    print(f"   {i+1}. {playlist['title']} ({playlist['count']} songs)")
            else:
                print("⚠️  No playlists returned")

            # Test other authenticated functions
            print("\n🎶 Testing other authenticated features...")

            try:
                # Test liked songs
                print("   Testing liked songs...")
                liked = auth_manager.ytmusic.get_liked_songs(limit=1)
                if liked and liked.get('tracks'):
                    print(f"   ✅ Liked songs: {len(liked['tracks'])} found")
                else:
                    print("   ℹ️  No liked songs or limited access")
            except Exception as e:
                print(f"   ⚠️  Liked songs error: {e}")

            try:
                # Test history
                print("   Testing history...")
                history = auth_manager.ytmusic.get_history()
                if history:
                    print(f"   ✅ History: {len(history)} items found")
                else:
                    print("   ℹ️  No history or limited access")
            except Exception as e:
                print(f"   ⚠️  History error: {e}")

            try:
                # Test library albums
                print("   Testing library albums...")
                albums = auth_manager.ytmusic.get_library_albums(limit=1)
                if albums:
                    print(f"   ✅ Library albums: {len(albums)} found")
                else:
                    print("   ℹ️  No library albums")
            except Exception as e:
                print(f"   ⚠️  Library albums error: {e}")

            return len(playlists) > 0

        else:
            print("❌ Authentication failed")
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_fresh_auth()

    if success:
        print("\n🎉 Fresh authentication working with playlists!")
    else:
        print("\n⚠️  Authentication working but no playlists found")
        print("   This could mean:")
        print("   1. The account has no personal playlists")
        print("   2. The account needs YouTube Music setup")
        print("   3. The account permissions are restricted")
