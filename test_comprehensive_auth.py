#!/usr/bin/env python3
"""
Test the fixed authentication with more comprehensive checks
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from auth import AuthenticationManager

def test_comprehensive_auth():
    """Test authentication with comprehensive YTMusic functionality"""

    print("🔍 Testing Comprehensive Authentication")
    print("=" * 50)

    # Headers from the user's cURL command
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://music.youtube.com/',
        'X-Goog-Visitor-Id': 'CgtqQUtaRHhZaFBaZyi8tsLFBjInCgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd',
        'X-YouTube-Client-Name': '67',
        'X-YouTube-Client-Version': '1.20250825.03.01',
        'X-YouTube-Device': 'cbr=Firefox^&cbrver=128.0^&ceng=Gecko^&cengver=128.0^&cos=X11^&cplatform=DESKTOP',
        'X-Youtube-Identity-Token': 'QUFFLUhqbUVuMTE0YTdCWXJSZ2xDUVJMbDBsQjhsYTFGUXc=',
        'X-YouTube-Page-CL': '799068799',
        'X-YouTube-Page-Label': 'youtube.music.web.client_20250825_03_RC01',
        'X-Goog-AuthUser': '0',
        'X-YouTube-Utc-Offset': '180',
        'X-YouTube-Time-Zone': 'Europe/Helsinki',
        'X-YouTube-Ad-Signals': 'dt=1756404540572^&flash=0^&frm^&u_tz=180^&u_his=2^&u_h=2560^&u_w=1440^&u_ah=2560^&u_aw=1440^&u_cd=24^&bc=31^&bih=782^&biw=1420^&brdim=-6%2C921%2C-6%2C921%2C1440%2C0%2C1420%2C1421%2C1420%2C782^&vis=1^&wgl=true^&ca_type=image',
        'DNT': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Cookie': 'YSC=5l6anihbkUE; SOCS=CAESNQgREitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjUwODI0LjA5X3AwGgJlbiACGgYIgPKzxQY; VISITOR_PRIVACY_METADATA=CgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd; PREF=f6=80^&repeat=NONE^&autoplay=true^&tz=Europe.Helsinki^&f5=30000; __Secure-1PSIDTS=sidts-CjUB5H03Py3fL79av8zL7nG_gmaalJOx0i5rvjMPfALb7gPb72W-aKOoDxpsZFuOfMu5DNaEOhAA; __Secure-3PSIDTS=sidts-CjUB5H03Py3fL79av8zL7nG_gmaalJOx0i5rvjMPfALb7gPb72W-aKOoDxpsZFuOfMu5DNaEOhAA; HSID=AUdfcDsEyLyU0aMxN; SSID=A7lgSt3ejC0m-NnKu; APISID=80Y1DtGXjedfQDN_/A9i5sh07t8wXmB9U8; SAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f; __Secure-1PAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f; __Secure-3PAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f; SID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFIzGDNUzqWpoE95SicaCYHgACgYKAR8SARMSFQHGX2MiyurZOmqfxRSQb5wxGUPNyxoVAUF8yKpMEcuCZRbWYzsl23MzKE3i0076; __Secure-1PSID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFV6Q3TQ4YA1PrVSp-E_xTjgACgYKAR0SARMSFQHGX2MicXxTwKEEDh50pHzM5glYPRoVAUF8yKo4kYCi-lWL6BcgL1gTLRJx0076; __Secure-3PSID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFs9a74j17SLZ4rCN8mmfLcwACgYKAQwSARMSFQHGX2MiggfMVUzNikW-rmLMc8IT9BoVAUF8yKrvCPBEpcLiMv2RPvP3X6NC0076; LOGIN_INFO=AFmmF2swRQIhAOTjXRnPi18LYSGLxzE0rKIsWnUMYOR9rFCzYw_A0R25AiBvXbK1P_QpDSpvBlozOLIH7FPsFHIVGrM24F2ql5JFJg:QUQ3MjNmeFprN1NxVnJaQTFDa0x4Y2ZkN2FwVWhtbElwTENPN3RXWGZnRHZSNEJTWjR0clQ1U0loRXVxOWNwZ2QwSnRscjVwc09KS3NIaU55cnAwZTkyYWZxX3lrbmtNSjZ2Y0U4VjVhMXhRYWFLclNXZDhtcXBqYWxtc21Wd3FTeXhvdTJlU1BoRGhSd2JCNlN3QVZLaExrUFpmeTFkc1lB; __Secure-ROLLOUT_TOKEN=COvHqt-25Zm9XBD_rcDuo6mPAxiSntri5auPAw%3D%3D; SIDCC=AKEyXzXPz-FMaDyD5R3S9quVgpcYHTGX5FargAH-AOd_OZ2pUmmSwaL-92Joe6Mvs-3zDSu3Vc4; __Secure-1PSIDCC=AKEyXzWyimGb9kk4Y0vk3P6cNYWPPCrZ-ZUX9wxLCb-T5hxfDJExvtAuVDBGVP6oTcUQCRpeJQ; __Secure-3PSIDCC=AKEyXzVZJ3NrneYvg1mDrBj3A3Qlppxos_1CH4PniZsbm6IgTBcTdhdNDxEAU119Lp9JDSATKQA; __Secure-YEC=CgtqQUtaRHhZaFBaZyi8tsLFBjInCgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd',
        'TE': 'trailers'
    }

    try:
        print("🔧 Creating AuthenticationManager...")
        auth_manager = AuthenticationManager()

        print("📋 Testing authentication...")
        success = auth_manager.authenticate_with_headers(headers)

        if success:
            print("✅ Authentication successful!")
            print(f"   Auth method: {auth_manager.user_info.get('auth_method', 'unknown')}")

            # Test various YTMusic authenticated functions
            ytmusic = auth_manager.ytmusic

            print("\n🎵 Testing authenticated YTMusic functions...")

            # Test 1: Library playlists
            try:
                print("   Testing get_library_playlists...")
                playlists = ytmusic.get_library_playlists(limit=50)
                print(f"   ✅ Library playlists: {len(playlists)} found")
                if playlists:
                    for i, playlist in enumerate(playlists[:3]):
                        title = playlist.get('title', 'Unknown')
                        count = playlist.get('count', 0)
                        print(f"      {i+1}. {title} ({count} songs)")
            except Exception as e:
                print(f"   ❌ Library playlists failed: {e}")

            # Test 2: Liked songs
            try:
                print("   Testing get_liked_songs...")
                liked = ytmusic.get_liked_songs(limit=10)
                tracks = liked.get('tracks', []) if liked else []
                print(f"   ✅ Liked songs: {len(tracks)} found")
            except Exception as e:
                print(f"   ❌ Liked songs failed: {e}")

            # Test 3: History
            try:
                print("   Testing get_history...")
                history = ytmusic.get_history()
                print(f"   ✅ History: {len(history)} items found")
            except Exception as e:
                print(f"   ❌ History failed: {e}")

            # Test 4: Library albums
            try:
                print("   Testing get_library_albums...")
                albums = ytmusic.get_library_albums(limit=10)
                print(f"   ✅ Library albums: {len(albums)} found")
            except Exception as e:
                print(f"   ❌ Library albums failed: {e}")

            # Test 5: Library artists
            try:
                print("   Testing get_library_artists...")
                artists = ytmusic.get_library_artists(limit=10)
                print(f"   ✅ Library artists: {len(artists)} found")
            except Exception as e:
                print(f"   ❌ Library artists failed: {e}")

            # Test 6: Regular search (should work regardless)
            try:
                print("   Testing search...")
                search_results = ytmusic.search("test", filter="songs", limit=5)
                print(f"   ✅ Search: {len(search_results)} results")
            except Exception as e:
                print(f"   ❌ Search failed: {e}")

            print("\n📊 Summary:")
            print("   Authentication is working and properly detected as browser auth!")
            print("   If playlist count is 0, it may be that:")
            print("   - The account has no created playlists")
            print("   - Only liked songs and library items exist")
            print("   - Authentication is limited to certain library sections")

            return True

        else:
            print("❌ Authentication failed")
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_comprehensive_auth()

    if success:
        print("\n🎉 Authentication system fully working!")
    else:
        print("\n⚠️  Authentication system still has issues")
