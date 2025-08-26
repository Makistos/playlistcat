#!/usr/bin/env python3
"""
Utility functions for YouTube Music Playlist Viewer
"""

import re
from typing import Optional


def extract_playlist_id(input_string: str) -> Optional[str]:
    """
    Extract playlist ID from various YouTube Music URL formats or return the ID if already clean.

    Supported formats:
    - https://music.youtube.com/playlist?list=PLrAGlzNOGcAqFNKK0c4K8Z9U8QmFNKK0c
    - https://music.youtube.com/playlist?list=PLrAGlzNOGcAqFNKK0c4K8Z9U8QmFNKK0c&si=...
    - PLrAGlzNOGcAqFNKK0c4K8Z9U8QmFNKK0c

    Args:
        input_string: URL or playlist ID

    Returns:
        Cleaned playlist ID or None if invalid
    """
    if not input_string:
        return None

    input_string = input_string.strip()

    # If it looks like a playlist ID already (starts with PL and is alphanumeric)
    if re.match(r'^PL[a-zA-Z0-9_-]+$', input_string):
        return input_string

    # Extract from URL
    patterns = [
        r'[?&]list=([a-zA-Z0-9_-]+)',  # Standard list parameter
        r'/playlist\?list=([a-zA-Z0-9_-]+)',  # Playlist URL
    ]

    for pattern in patterns:
        match = re.search(pattern, input_string)
        if match:
            playlist_id = match.group(1)
            # Validate that it looks like a playlist ID
            if playlist_id.startswith('PL'):
                return playlist_id

    return None


def format_duration(duration_seconds: int) -> str:
    """
    Format duration from seconds to MM:SS or HH:MM:SS format.

    Args:
        duration_seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    if duration_seconds < 0:
        return "0:00"

    hours = duration_seconds // 3600
    minutes = (duration_seconds % 3600) // 60
    seconds = duration_seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"


def validate_playlist_id(playlist_id: str) -> bool:
    """
    Validate if a string looks like a valid YouTube playlist ID.

    Args:
        playlist_id: The playlist ID to validate

    Returns:
        True if valid, False otherwise
    """
    if not playlist_id:
        return False

    # YouTube playlist IDs typically start with "PL" and are 34 characters long
    # But let's be more flexible and just check for basic format
    return bool(re.match(r'^PL[a-zA-Z0-9_-]{10,}$', playlist_id))


if __name__ == "__main__":
    # Test the utility functions
    test_urls = [
        "https://music.youtube.com/playlist?list=PLrAGlzNOGcAqFNKK0c4K8Z9U8QmFNKK0c",
        "https://music.youtube.com/playlist?list=PLrAGlzNOGcAqFNKK0c4K8Z9U8QmFNKK0c&si=abcd1234",
        "PLrAGlzNOGcAqFNKK0c4K8Z9U8QmFNKK0c",
        "invalid_id",
        "",
    ]

    print("Testing playlist ID extraction:")
    for url in test_urls:
        result = extract_playlist_id(url)
        valid = validate_playlist_id(result) if result else False
        print(f"Input: {url}")
        print(f"Result: {result}")
        print(f"Valid: {valid}")
        print("-" * 40)

    print("\nTesting duration formatting:")
    test_durations = [30, 90, 3661, 7200, 0, -1]
    for duration in test_durations:
        formatted = format_duration(duration)
        print(f"{duration}s -> {formatted}")
