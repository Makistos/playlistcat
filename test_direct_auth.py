#!/usr/bin/env python3
"""
Test direct header authentication without files
"""

def test_direct_auth():
    """Test authentication by passing headers directly to requests"""

    print("🔍 Testing direct header authentication")
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
        'X-Youtube-Identity-Token': 'QUFFLUhqbUVuMTE0YTdCWXJSZ2xDUVJMbDBsQjhsYTFGUXw=',
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
        print("1️⃣ Testing direct API call...")
        import requests

        # Test the exact URL from the cURL command
        url = 'https://music.youtube.com/verify_session'

        response = requests.get(url, headers=headers)
        print(f"✅ Direct API call status: {response.status_code}")

        if response.status_code == 200:
            print("✅ Authentication headers are valid!")
            return True
        else:
            print(f"❌ API call failed: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False

    except Exception as e:
        print(f"❌ Direct API call failed: {e}")
        return False

def test_session_approach():
    """Test using requests session with YTMusic"""

    print("\n" + "="*50)
    print("🧪 Testing session-based approach")

    try:
        print("Creating requests session with authentication...")
        import requests

        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://music.youtube.com/',
            'X-Goog-Visitor-Id': 'CgtqQUtaRHhZaFBaZyi8tsLFBjInCgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd',
            'X-YouTube-Client-Name': '67',
            'X-YouTube-Client-Version': '1.20250825.03.01',
            'X-Goog-AuthUser': '0',
            'Cookie': 'YSC=5l6anihbkUE; SOCS=CAESNQgREitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjUwODI0LjA5X3AwGgJlbiACGgYIgPKzxQY; VISITOR_PRIVACY_METADATA=CgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd; PREF=f6=80^&repeat=NONE^&autoplay=true^&tz=Europe.Helsinki^&f5=30000; __Secure-1PSIDTS=sidts-CjUB5H03Py3fL79av8zL7nG_gmaalJOx0i5rvjMPfALb7gPb72W-aKOoDxpsZFuOfMu5DNaEOhAA; __Secure-3PSIDTS=sidts-CjUB5H03Py3fL79av8zL7nG_gmaalJOx0i5rvjMPfALb7gPb72W-aKOoDxpsZFuOfMu5DNaEOhAA; HSID=AUdfcDsEyLyU0aMxN; SSID=A7lgSt3ejC0m-NnKu; APISID=80Y1DtGXjedfQDN_/A9i5sh07t8wXmB9U8; SAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f; __Secure-1PAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f; __Secure-3PAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f; SID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFIzGDNUzqWpoE95SicaCYHgACgYKAR8SARMSFQHGX2MiyurZOmqfxRSQb5wxGUPNyxoVAUF8yKpMEcuCZRbWYzsl23MzKE3i0076; __Secure-1PSID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFV6Q3TQ4YA1PrVSp-E_xTjgACgYKAR0SARMSFQHGX2MicXxTwKEEDh50pHzM5glYPRoVAUF8yKo4kYCi-lWL6BcgL1gTLRJx0076; __Secure-3PSID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFs9a74j17SLZ4rCN8mmfLcwACgYKAQwSARMSFQHGX2MiggfMVUzNikW-rmLMc8IT9BoVAUF8yKrvCPBEpcLiMv2RPvP3X6NC0076; LOGIN_INFO=AFmmF2swRQIhAOTjXRnPi18LYSGLxzE0rKIsWnUMYOR9rFCzYw_A0R25AiBvXbK1P_QpDSpvBlozOLIH7FPsFHIVGrM24F2ql5JFJg:QUQ3MjNmeFprN1NxVnJaQTFDa0x4Y2ZkN2FwVWhtbElwTENPN3RXWGZnRHZSNEJTWjR0clQ1U0loRXVxOWNwZ2QwSnRscjVwc09KS3NIaU55cnAwZTkyYWZxX3lrbmtNSjZ2Y0U4VjVhMXhRYWFLclNXZDhtcXBqYWxtc21Wd3FTeXhvdTJlU1BoRGhSd2JCNlN3QVZLaExrUFpmeTFkc1lB; __Secure-ROLLOUT_TOKEN=COvHqt-25Zm9XBD_rcDuo6mPAxiSntri5auPAw%3D%3D; SIDCC=AKEyXzXPz-FMaDyD5R3S9quVgpcYHTGX5FargAH-AOd_OZ2pUmmSwaL-92Joe6Mvs-3zDSu3Vc4; __Secure-1PSIDCC=AKEyXzWyimGb9kk4Y0vk3P6cNYWPPCrZ-ZUX9wxLCb-T5hxfDJExvtAuVDBGVP6oTcUQCRpeJQ; __Secure-3PSIDCC=AKEyXzVZJ3NrneYvg1mDrBj3A3Qlppxos_1CH4PniZsbm6IgTBcTdhdNDxEAU119Lp9JDSATKQA; __Secure-YEC=CgtqQUtaRHhZaFBaZyi8tsLFBjInCgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd'
        })

        print("✅ Session configured")

        # Try to use session with YTMusic
        print("Testing YTMusic with session...")
        from ytmusicapi import YTMusic

        ytmusic = YTMusic(requests_session=session)
        print("✅ YTMusic with session initialized")

        # Try library access
        print("🎵 Testing library access...")
        playlists = ytmusic.get_library_playlists(limit=1)
        print(f"✅ Library access worked! Found {len(playlists)} playlists")

        return True

    except Exception as e:
        print(f"❌ Session approach failed: {e}")
        return False

if __name__ == "__main__":
    api_works = test_direct_auth()
    session_works = test_session_approach()

    if api_works:
        print("\n🎉 Direct API authentication works!")
    if session_works:
        print("\n🎉 Session-based authentication works!")

    if not (api_works or session_works):
        print("\n⚠️  Both methods failed - the credentials may be expired")
