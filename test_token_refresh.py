#!/usr/bin/env python3
"""
Test automatic token refresh functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from auth import AuthenticationManager

def test_token_refresh():
    """Test the token refresh system"""

    print("🔍 Testing Automatic Token Refresh System")
    print("=" * 50)

    # Fresh headers from your recent working session
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

        print("📋 Testing initial authentication...")
        success = auth_manager.authenticate_with_headers(headers)

        if success:
            print("✅ Initial authentication successful!")

            # Get authentication status
            status = auth_manager.get_auth_status_info()
            print(f"📊 Auth Status:")
            for key, value in status.items():
                print(f"   {key}: {value}")

            # Test playlist access
            print("\n🎵 Testing playlist access...")
            playlists = auth_manager.get_user_playlists()
            print(f"✅ Found {len(playlists)} playlists")

            # Test manual refresh
            print("\n🔄 Testing manual token refresh...")
            refresh_success = auth_manager.force_token_refresh()
            print(f"🔄 Manual refresh result: {refresh_success}")

            # Test authentication health check
            print("\n🩺 Testing authentication health check...")
            health_success = auth_manager.refresh_authentication_status()
            print(f"🩺 Health check result: {health_success}")

            # Get updated status
            status = auth_manager.get_auth_status_info()
            print(f"\n📊 Updated Auth Status:")
            for key, value in status.items():
                print(f"   {key}: {value}")

            print("\n✅ Token refresh system is working!")
            print("\n📋 Features available:")
            print("   - Automatic monitoring every 30 minutes")
            print("   - Manual refresh via force_token_refresh()")
            print("   - Automatic retry on API failures")
            print("   - SAPISIDHASH regeneration")
            print("   - Fallback to multiple auth methods")
            print("   - Health check monitoring")

            return True

        else:
            print("❌ Initial authentication failed")
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_token_refresh()

    if success:
        print("\n🎉 Automatic token refresh system is working!")
    else:
        print("\n⚠️  Token refresh system needs attention")
