#!/usr/bin/env python3
"""
Test the updated authentication with the specific cURL command
"""

import sys
import os
import shlex
import json
import tempfile
from typing import Optional, Dict, List

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def parse_curl_command(curl_text: str) -> Optional[Dict]:
    """Parse cURL command to extract authentication headers"""
    import re

    # Clean up the curl command - remove line continuations and normalize
    cleaned_text = re.sub(r'\\\s*\n\s*', ' ', curl_text)

    # Split into tokens while respecting quotes
    tokens = tokenize_curl_command(cleaned_text)

    headers = {}
    i = 0

    while i < len(tokens):
        token = tokens[i]

        # Look for header flags
        if token in ['-H', '--header'] and i + 1 < len(tokens):
            header_value = tokens[i + 1]

            # Remove quotes if present
            if (header_value.startswith('"') and header_value.endswith('"')) or \
               (header_value.startswith("'") and header_value.endswith("'")):
                header_value = header_value[1:-1]

            # Parse header
            if ':' in header_value:
                key, value = header_value.split(':', 1)
                headers[key.strip()] = value.strip()

            i += 2  # Skip both the flag and the value
        else:
            i += 1

    return headers

def tokenize_curl_command(text: str) -> List[str]:
    """Tokenize curl command while respecting quotes"""
    try:
        return shlex.split(text)
    except ValueError:
        # Fallback parsing
        tokens = []
        current_token = ""
        in_quotes = False
        quote_char = None

        for char in text:
            if char in ['"', "'"] and not in_quotes:
                in_quotes = True
                quote_char = char
                current_token += char
            elif char == quote_char and in_quotes:
                in_quotes = False
                current_token += char
                quote_char = None
            elif char.isspace() and not in_quotes:
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
            else:
                current_token += char

        if current_token:
            tokens.append(current_token)

        return tokens

def test_ytmusic_auth_setup(headers: Dict[str, str]):
    """Test YTMusic authentication with setup method"""
    auth_file = None
    try:
        print("\n🔧 Testing YTMusic Authentication with setup method...")

        # Get cookie header
        cookie_header = headers.get('Cookie', '')
        if not cookie_header:
            print("❌ No Cookie header found")
            return False

        # Create auth file path
        auth_file = os.path.join(os.path.expanduser('~'), '.test_ytmcat_auth.json')

        try:
            # Method 1: Try using ytmusicapi.setup
            from ytmusicapi.setup import setup

            # Create the headers in the raw format that setup() expects
            headers_raw = f"Cookie: {cookie_header}\n"
            headers_raw += f"X-Goog-AuthUser: {headers.get('X-Goog-AuthUser', '0')}\n"

            # Add other important headers
            if 'User-Agent' in headers:
                headers_raw += f"User-Agent: {headers['User-Agent']}\n"
            if 'X-Goog-Visitor-Id' in headers:
                headers_raw += f"X-Goog-Visitor-Id: {headers['X-Goog-Visitor-Id']}\n"
            if 'X-YouTube-Client-Name' in headers:
                headers_raw += f"X-YouTube-Client-Name: {headers['X-YouTube-Client-Name']}\n"
            if 'X-YouTube-Client-Version' in headers:
                headers_raw += f"X-YouTube-Client-Version: {headers['X-YouTube-Client-Version']}\n"

            print("  Using ytmusicapi.setup() method...")
            setup(filepath=auth_file, headers_raw=headers_raw)
            print(f"  ✅ Setup created auth file: {auth_file}")

        except Exception as setup_error:
            print(f"  ⚠️  Setup method failed: {setup_error}")

            # Method 2: Fallback to manual creation
            print("  Using manual auth file creation...")
            auth_data = {
                "cookie": cookie_header,
                "X-Goog-AuthUser": headers.get('X-Goog-AuthUser', '0'),
            }

            with open(auth_file, 'w') as f:
                json.dump(auth_data, f, indent=2)
            print(f"  ✅ Manual method created auth file: {auth_file}")

        # Test with ytmusicapi
        print("  Testing authentication...")
        from ytmusicapi import YTMusic
        ytmusic = YTMusic(auth_file)

        print("  Accessing library playlists...")
        playlists = ytmusic.get_library_playlists(limit=1)

        print(f"✅ SUCCESS! Found {len(playlists)} playlists")
        if playlists:
            print(f"  Sample playlist: {playlists[0].get('title', 'Unknown')}")

        return True

    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print(f"   Error type: {type(e).__name__}")

        # Check for specific error types
        error_str = str(e).lower()
        if "oauth" in error_str:
            print("   → OAuth error: Authentication method mismatch")
        elif "401" in error_str or "unauthorized" in error_str:
            print("   → Authentication failed: Invalid or expired credentials")
        elif "403" in error_str or "forbidden" in error_str:
            print("   → Access denied: Check account permissions")

        return False

    finally:
        # Clean up test file
        if auth_file and os.path.exists(auth_file):
            try:
                os.unlink(auth_file)
                print(f"  🧹 Cleaned up test file: {auth_file}")
            except:
                pass

# Test curl command
test_curl = """curl 'https://music.youtube.com/verify_session' \\
  --compressed \\
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0' \\
  -H 'Accept: */*' \\
  -H 'Accept-Language: en-US,en;q=0.5' \\
  -H 'Accept-Encoding: gzip, deflate, br, zstd' \\
  -H 'Referer: https://music.youtube.com/' \\
  -H 'X-Goog-Visitor-Id: CgtqQUtaRHhZaFBaZyi8tsLFBjInCgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd' \\
  -H 'X-YouTube-Client-Name: 67' \\
  -H 'X-YouTube-Client-Version: 1.20250825.03.01' \\
  -H 'X-YouTube-Device: cbr=Firefox^&cbrver=128.0^&ceng=Gecko^&cengver=128.0^&cos=X11^&cplatform=DESKTOP' \\
  -H 'X-Youtube-Identity-Token: QUFFLUhqbUVuMTE0YTdCWXJSZ2xDUVJMbDBsQjhsYTFGUXw=' \\
  -H 'X-YouTube-Page-CL: 799068799' \\
  -H 'X-YouTube-Page-Label: youtube.music.web.client_20250825_03_RC01' \\
  -H 'X-Goog-AuthUser: 0' \\
  -H 'X-YouTube-Utc-Offset: 180' \\
  -H 'X-YouTube-Time-Zone: Europe/Helsinki' \\
  -H 'X-YouTube-Ad-Signals: dt=1756404540572^&flash=0^&frm^&u_tz=180^&u_his=2^&u_h=2560^&u_w=1440^&u_ah=2560^&u_aw=1440^&u_cd=24^&bc=31^&bih=782^&biw=1420^&brdim=-6%2C921%2C-6%2C921%2C1440%2C0%2C1420%2C1421%2C1420%2C782^&vis=1^&wgl=true^&ca_type=image' \\
  -H 'DNT: 1' \\
  -H 'Sec-Fetch-Dest: empty' \\
  -H 'Sec-Fetch-Mode: cors' \\
  -H 'Sec-Fetch-Site: same-origin' \\
  -H 'Connection: keep-alive' \\
  -H 'Cookie: YSC=5l6anihbkUE; SOCS=CAESNQgREitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjUwODI0LjA5X3AwGgJlbiACGgYIgPKzxQY; VISITOR_PRIVACY_METADATA=CgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd; PREF=f6=80^&repeat=NONE^&autoplay=true^&tz=Europe.Helsinki^&f5=30000; __Secure-1PSIDTS=sidts-CjUB5H03Py3fL79av8zL7nG_gmaalJOx0i5rvjMPfALb7gPb72W-aKOoDxpsZFuOfMu5DNaEOhAA; __Secure-3PSIDTS=sidts-CjUB5H03Py3fL79av8zL7nG_gmaalJOx0i5rvjMPfALb7gPb72W-aKOoDxpsZFuOfMu5DNaEOhAA; HSID=AUdfcDsEyLyU0aMxN; SSID=A7lgSt3ejC0m-NnKu; APISID=80Y1DtGXjedfQDN_/A9i5sh07t8wXmB9U8; SAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f; __Secure-1PAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f; __Secure-3PAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f; SID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFIzGDNUzqWpoE95SicaCYHgACgYKAR8SARMSFQHGX2MiyurZOmqfxRSQb5wxGUPNyxoVAUF8yKpMEcuCZRbWYzsl23MzKE3i0076; __Secure-1PSID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFV6Q3TQ4YA1PrVSp-E_xTjgACgYKAR0SARMSFQHGX2MicXxTwKEEDh50pHzM5glYPRoVAUF8yKo4kYCi-lWL6BcgL1gTLRJx0076; __Secure-3PSID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFs9a74j17SLZ4rCN8mmfLcwACgYKAQwSARMSFQHGX2MiggfMVUzNikW-rmLMc8IT9BoVAUF8yKrvCPBEpcLiMv2RPvP3X6NC0076; LOGIN_INFO=AFmmF2swRQIhAOTjXRnPi18LYSGLxzE0rKIsWnUMYOR9rFCzYw_A0R25AiBvXbK1P_QpDSpvBlozOLIH7FPsFHIVGrM24F2ql5JFJg:QUQ3MjNmeFprN1NxVnJaQTFDa0x4Y2ZkN2FwVWhtbElwTENPN3RXWGZnRHZSNEJTWjR0clQ1U0loRXVxOWNwZ2QwSnRscjVwc09KS3NIaU55cnAwZTkyYWZxX3lrbmtNSjZ2Y0U4VjVhMXhRYWFLclNXZDhtcXBqYWxtc21Wd3FTeXhvdTJlU1BoRGhSd2JCNlN3QVZLaExrUFpmeTFkc1lB; __Secure-ROLLOUT_TOKEN=COvHqt-25Zm9XBD_rcDuo6mPAxiSntri5auPAw%3D%3D; SIDCC=AKEyXzXPz-FMaDyD5R3S9quVgpcYHTGX5FargAH-AOd_OZ2pUmmSwaL-92Joe6Mvs-3zDSu3Vc4; __Secure-1PSIDCC=AKEyXzWyimGb9kk4Y0vk3P6cNYWPPCrZ-ZUX9wxLCb-T5hxfDJExvtAuVDBGVP6oTcUQCRpeJQ; __Secure-3PSIDCC=AKEyXzVZJ3NrneYvg1mDrBj3A3Qlppxos_1CH4PniZsbm6IgTBcTdhdNDxEAU119Lp9JDSATKQA; __Secure-YEC=CgtqQUtaRHhZaFBaZyi8tsLFBjInCgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd' \\
  -H 'TE: trailers'"""

def main():
    print("🔍 Testing Updated Authentication Method")
    print("=" * 50)

    print("📋 Parsing cURL command...")
    headers = parse_curl_command(test_curl)

    if not headers:
        print("❌ Failed to parse cURL command")
        return

    print(f"✅ Parsed {len(headers)} headers")

    # Check authentication elements
    cookie_header = headers.get('Cookie', '')
    auth_cookies = ['SID=', 'HSID=', 'SSID=', 'APISID=', 'SAPISID=']
    found_cookies = [cookie for cookie in auth_cookies if cookie in cookie_header]

    print(f"🍪 Authentication cookies: {len(found_cookies)}/5 found")

    # Test authentication
    success = test_ytmusic_auth_setup(headers)

    if success:
        print("\n🎉 Authentication works with updated method!")
    else:
        print("\n⚠️  Authentication still failing")

if __name__ == "__main__":
    main()
