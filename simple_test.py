#!/usr/bin/env python3
"""
Simple auth test
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_simple():
    print("Starting simple test...")

    from auth import AuthenticationManager
    print("✅ Import successful")

    # Test basic creation
    auth_manager = AuthenticationManager()
    print("✅ AuthenticationManager created")

    # Check if auth file exists
    auth_file_path = os.path.expanduser('~/.playlistcat_auth.json')
    print(f"Auth file exists: {os.path.exists(auth_file_path)}")

    if os.path.exists(auth_file_path):
        import json
        with open(auth_file_path, 'r') as f:
            auth_data = json.load(f)
            print(f"Auth file keys: {list(auth_data.keys())}")
            print(f"Has authorization: {'authorization' in auth_data}")

    print("Simple test complete")

if __name__ == "__main__":
    test_simple()
