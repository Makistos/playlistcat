#!/usr/bin/env python3
"""
Test the improved cURL parser with the user's example
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from auth import AuthSetupDialog

# Test curl command
test_curl = """curl 'https://music.youtube.com/generate_204' \\
  -I \\
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0' \\
  -H 'Accept: */*' \\
  -H 'Accept-Language: en-US,en;q=0.5' \\
  -H 'Accept-Encoding: gzip, deflate, br, zstd' \\
  -H 'Referer: https://music.youtube.com/' \\
  -H 'DNT: 1' \\
  -H 'Sec-Fetch-Dest: empty' \\
  -H 'Sec-Fetch-Mode: cors' \\
  -H 'Sec-Fetch-Site: same-origin' \\
  -H 'Connection: keep-alive' \\
  -H 'Cookie: YSC=5l6anihbkUE; SOCS=CAESNQgREitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjUwODI0LjA5X3AwGgJlbiACGgYIgPKzxQY; VISITOR_PRIVACY_METADATA=CgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd; PREF=f6=80^&repeat=NONE^&autoplay=true^&tz=Europe.Helsinki^&f5=30000; __Secure-1PSIDTS=sidts-CjUB5H03Pweu42MObFoC93Iar4zBUsuWbdry8j_uFUtI7Pf_TzrzSRyN5qxU4cbyMEuFPTPhFxAA; __Secure-3PSIDTS=sidts-CjUB5H03Pweu42MObFoC93Iar4zBUsuWbdry8j_uFUtI7Pf_TzrzSRyN5qxU4cbyMEuFPTPhFxAA; HSID=AUdfcDsEyLyU0aMxN; SSID=A7lgSt3ejC0m-NnKu; APISID=80Y1DtGXjedfQDN_/A9i5sh07t8wXmB9U8; SAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f; __Secure-1PAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f; __Secure-3PAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f; SID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFIzGDNUzqWpoE95SicaCYHgACgYKAR8SARMSFQHGX2MiyurZOmqfxRSQb5wxGUPNyxoVAUF8yKpMEcuCZRbWYzsl23MzKE3i0076; __Secure-1PSID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFV6Q3TQ4YA1PrVSp-E_xTjgACgYKAR0SARMSFQHGX2MicXxTwKEEDh50pHzM5glYPRoVAUF8yKo4kYCi-lWL6BcgL1gTLRJx0076; __Secure-3PSID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFs9a74j17SLZ4rCN8mmfLcwACgYKAQwSARMSFQHGX2MiggfMVUzNikW-rmLMc8IT9BoVAUF8yKrvCPBEpcLiMv2RPvP3X6NC0076; LOGIN_INFO=AFmmF2swRQIhAOTjXRnPi18LYSGLxzE0rKIsWnUMYOR9rFCzYw_A0R25AiBvXbK1P_QpDSpvBlozOLIH7FPsFHIVGrM24F2ql5JFJg:QUQ3MjNmeFprN1NxVnJaQTFDa0x4Y2ZkN2FwVWhtbElwTENPN3RXWGZnRHZSNEJTWjR0clQ1U0loRXVxOWNwZ2QwSnRscjVwc09KS3NIaU55cnAwZTkyYWZxX3lrbmtNSjZ2Y0U4VjVhMXhRYWFLclNXZDhtcXBqYWxtc21Wd3FTeXhvdTJlU1BoRGhSd2JCNlN3QVZLaExrUFpmeTFkc1lB; __Secure-ROLLOUT_TOKEN=COvHqt-25Zm9XBD_rcDuo6mPAxiSntri5auPAw%3D%3D; SIDCC=AKEyXzUp--N20fctY8KShnLRqvuHyYlwzIZeqt_8zLsRRO_tbK57hhoofDl81Y5d21oKlsGWef0; __Secure-1PSIDCC=AKEyXzXGQHVaKe-qizf0zpkJT6kPii2_78rxTqRupljjiG6iV9ETKqmHjLVjRmSfE46KAMFcdg; __Secure-3PSIDCC=AKEyXzWlFkJti21lJsJ4eXe6dc_68FWXwkLlfPJR0lIGtx-JtMIJ51edTmx0yUZpDpYiQOVrEHM; __Secure-YEC=CgtqQUtaRHhZaFBaZyi8tsLFBjInCgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd' \\
  -H 'Priority: u=4' \\
  -H 'TE: trailers'"""

def test_curl_parser():
    """Test the cURL parser with the user's example"""
    print("Testing cURL Parser")
    print("=" * 50)

    # Create a mock dialog to test the parser
    dialog = AuthSetupDialog()

    print("Testing with user's cURL command...")
    result = dialog.parse_curl_command(test_curl)

    if result:
        print("✅ Successfully parsed cURL command!")
        print(f"Found {len(result)} headers:")

        # Check for essential authentication headers
        cookie_header = result.get('Cookie')
        if cookie_header:
            print("✅ Cookie header found")
            # Count authentication cookies
            auth_cookies = ['SID=', 'HSID=', 'SSID=', 'APISID=', 'SAPISID=']
            found_cookies = [cookie for cookie in auth_cookies if cookie in cookie_header]
            print(f"✅ Found {len(found_cookies)} authentication cookies: {found_cookies}")
        else:
            print("❌ No Cookie header found")

        # Show some other important headers
        important_headers = ['User-Agent', 'Referer', 'Accept']
        for header in important_headers:
            if header in result:
                print(f"✅ {header}: {result[header][:50]}...")

        print("\n📊 Header summary:")
        for key in sorted(result.keys()):
            value = result[key]
            if key == 'Cookie':
                # Show cookie count instead of full value for privacy
                cookie_count = len([c for c in value.split(';') if c.strip()])
                print(f"  {key}: {cookie_count} cookies")
            else:
                # Truncate long values
                display_value = value[:50] + "..." if len(value) > 50 else value
                print(f"  {key}: {display_value}")

    else:
        print("❌ Failed to parse cURL command")
        print("The parser couldn't extract valid authentication headers")

if __name__ == "__main__":
    test_curl_parser()
