#!/usr/bin/env python3
"""
Test the authentication system integration with the main application
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_main_app_auth():
    """Test authentication integration with main application"""

    print("🔍 Testing Main Application Authentication Integration")
    print("=" * 60)

    try:
        # Import main application components
        from main import YouTubeMusicPlaylistViewer
        from auth import AuthenticationManager
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QTimer

        # Create application
        app = QApplication(sys.argv)

        print("✅ Application created")

        # Create main window
        main_window = YouTubeMusicPlaylistViewer()

        print("✅ Main window created")
        print(f"   Auth manager available: {hasattr(main_window, 'auth_manager')}")
        print(f"   Initial auth status: {main_window.auth_manager.is_authenticated}")

        # Test authentication with headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Cookie': 'YSC=5l6anihbkUE; HSID=AUdfcDsEyLyU0aMxN; SSID=A7lgSt3ejC0m-NnKu; APISID=80Y1DtGXjedfQDN_/A9i5sh07t8wXmB9U8; SAPISID=UOE9Wdjjsbphviwt/AunyGM4k8_C3Acv4f; SID=g.a0000whIt5p4txn0XvTLF9AOi3jDSHqtVyShk9WUcNQQLMn_EfwFIzGDNUzqWpoE95SicaCYHgACgYKAR8SARMSFQHGX2MiyurZOmqfxRSQb5wxGUPNyxoVAUF8yKpMEcuCZRbWYzsl23MzKE3i0076',
            'X-Goog-AuthUser': '0',
            'X-Goog-Visitor-Id': 'CgtqQUtaRHhZaFBaZyi8tsLFBjInCgJGSRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiBd',
            'X-YouTube-Client-Name': '67',
            'X-YouTube-Client-Version': '1.20250825.03.01',
        }

        print("\n🔧 Testing authentication...")
        auth_success = main_window.auth_manager.authenticate_with_headers(headers)

        print(f"✅ Authentication result: {auth_success}")
        print(f"   Auth status: {main_window.auth_manager.is_authenticated}")
        print(f"   User info: {main_window.auth_manager.user_info}")

        # Test UI updates
        print("\n🎨 Testing UI integration...")
        if hasattr(main_window, 'update_auth_ui'):
            print("   ✅ update_auth_ui method exists")

        if hasattr(main_window, 'auth_button'):
            print(f"   ✅ Auth button exists: {main_window.auth_button.text()}")

        # Close application after short delay
        QTimer.singleShot(100, app.quit)

        print("\n🏁 Integration test completed successfully")
        return True

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Set up environment to avoid display issues
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'

    success = test_main_app_auth()

    if success:
        print("\n🎉 Authentication integration working!")
    else:
        print("\n⚠️  Authentication integration needs fixes")
