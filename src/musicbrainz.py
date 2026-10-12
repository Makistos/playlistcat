#!/usr/bin/env python3
"""
MusicBrainz lookup for the original album and release year of a track.

YouTube Music often links tracks to compilations or reissues (or, for music
videos, to no album at all), so the original release is looked up from
MusicBrainz by artist and track name instead.

MusicBrainz allows one request per second and requires an identifying
User-Agent: https://musicbrainz.org/doc/MusicBrainz_API/Rate_Limiting
"""

import json
import os
import re
import threading
import time
import unicodedata
from typing import Optional, Dict

import requests

API_URL = "https://musicbrainz.org/ws/2"
USER_AGENT = "PlaylistCat/0.4.1 ( https://github.com/Makistos/playlistcat )"
MIN_REQUEST_INTERVAL = 1.1  # seconds, slightly above the 1 req/s limit
MAX_SEARCH_PAGES = 3        # popular songs have hundreds of (compilation) recordings
STUDIO_ALBUM_MAX_DELAY = 2  # years after the first release

# Parenthesized parts of YouTube titles that aren't part of the song name,
# e.g. "(Official 4K Video)", "[Remastered 2011]", "(TV Edit)", "(2011)"
TITLE_NOISE = re.compile(
    r"official|video|audio|lyric|visuali[sz]er|remaster|version|edit|\bmix\b|\bhd\b|\b4k\b|\bmv\b|"
    r"mono|stereo|explicit|clean|single|feat\.|ft\.|^\s*\d{4}\s*$", re.I)
TITLE_SUFFIX_NOISE = re.compile(
    r"\s+-\s+[^-]*(remaster|version|edit|live|mono|stereo|mix)[^-]*$", re.I)
# Recordings that are not the original studio version
UNWANTED_RECORDING = re.compile(
    r"\b(live|demo|remix|instrumental|karaoke|acoustic|re-?recorded|rehearsal|cover)\b", re.I)

# Preferred release types, best first. Songs that never appeared on a studio
# album fall back to soundtracks, EPs and singles.
RELEASE_PREFERENCE = [
    ("Album", None, ""),
    ("Album", "Soundtrack", " (Soundtrack)"),
    ("EP", None, " (EP)"),
    ("Single", None, " (Single)"),
]


class MusicBrainzError(Exception):
    """Lookup failed for a temporary reason; the result must not be cached."""


def clean_title(title: str) -> str:
    """Strip YouTube-specific decorations from a track title."""
    title = re.sub(r"\s*[\(\[]([^\)\]]*)[\)\]]",
                   lambda m: "" if TITLE_NOISE.search(m.group(1)) else m.group(0), title)
    title = TITLE_SUFFIX_NOISE.sub("", title)
    return title.strip()


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    text = text.replace("’", "'").replace("‐", "-")
    return re.sub(r"\s+", " ", text).strip()


def _comparable(text: str) -> str:
    """Normalize for title comparison, ignoring punctuation ("Girls, Girls" == "Girls Girls")."""
    return re.sub(r"[\W_]+", " ", normalize(text)).strip()


def _escape(text: str) -> str:
    """Escape Lucene query syntax characters."""
    return re.sub(r'([+\-&|!(){}\[\]^"~*?:\\/])', r'\\\1', text)


class MusicBrainzClient:
    """Rate-limited MusicBrainz client with a persistent on-disk cache."""

    def __init__(self, cache_path: Optional[str] = None):
        self.cache_path = cache_path or os.path.join(
            os.path.expanduser("~"), ".playlistcat_musicbrainz_cache.json")
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT
        self._last_request = 0.0
        self._lock = threading.Lock()
        self.cache: Dict[str, Optional[Dict[str, str]]] = {}
        try:
            with open(self.cache_path) as f:
                self.cache = json.load(f)
        except (OSError, ValueError):
            pass

    @staticmethod
    def cache_key(artist: str, title: str) -> str:
        return f"{normalize(artist)}\t{normalize(clean_title(title))}"

    def save_cache(self):
        try:
            with open(self.cache_path, "w") as f:
                json.dump(self.cache, f)
        except OSError as e:
            print(f"Failed to save MusicBrainz cache: {e}")

    def lookup(self, artist: str, title: str,
               stop_event: Optional[threading.Event] = None) -> Optional[Dict[str, str]]:
        """Return {'album': ..., 'year': ...} for the original release, or None.

        Raises MusicBrainzError if MusicBrainz could not be reached or
        stop_event was set while waiting.
        """
        key = self.cache_key(artist, title)
        if key in self.cache:
            return self.cache[key]

        self._stop_event = stop_event or threading.Event()
        result = self._find_original_release(artist, clean_title(title))
        self.cache[key] = result
        return result

    def _sleep(self, seconds: float):
        if self._stop_event.wait(seconds):
            raise MusicBrainzError("Lookup cancelled")

    def _get(self, path: str, params: Dict[str, str]) -> dict:
        params = dict(params, fmt="json")
        for attempt in range(6):
            with self._lock:
                wait = self._last_request + MIN_REQUEST_INTERVAL - time.time()
                if wait > 0:
                    self._sleep(wait)
                self._last_request = time.time()
            try:
                response = self.session.get(f"{API_URL}/{path}", params=params, timeout=20)
            except requests.RequestException as e:
                raise MusicBrainzError(str(e))
            # 503 means rate limited or server busy
            if response.status_code == 503:
                self._sleep(min(2 ** (attempt + 1), 30))
                continue
            if response.status_code != 200:
                raise MusicBrainzError(f"HTTP {response.status_code}")
            return response.json()
        raise MusicBrainzError("MusicBrainz is busy")

    def _find_original_release(self, artist: str, title: str) -> Optional[Dict[str, str]]:
        query = f'recording:"{_escape(title)}" AND artist:"{_escape(artist)}" AND status:official'
        wanted_title = _comparable(title)
        # (date, release group) for each official release of a matching recording.
        # Search results list each recording's releases, so no extra requests are needed.
        releases = []
        offset = 0
        for _ in range(MAX_SEARCH_PAGES):
            data = self._get("recording", {"query": query, "limit": "100", "offset": str(offset)})
            recordings = data.get("recordings", [])
            for recording in recordings:
                if (recording.get("score", 0) < 90
                        or _comparable(recording["title"]) != wanted_title
                        or UNWANTED_RECORDING.search(recording.get("disambiguation", ""))):
                    continue
                releases += [(rel["date"], rel["release-group"])
                             for rel in recording.get("releases", [])
                             if rel.get("status") == "Official" and rel.get("date")
                             and "release-group" in rel]
            offset += len(recordings)
            if not recordings or offset >= data.get("count", 0):
                break

        # Earliest release of each preferred type
        earliest = []  # (year, rank, album title)
        for rank, (primary, secondary, suffix) in enumerate(RELEASE_PREFERENCE):
            matching = [(date, group) for date, group in releases
                        if group.get("primary-type") == primary
                        and group.get("secondary-types", []) == ([secondary] if secondary else [])]
            if matching:
                date, group = min(matching, key=lambda m: m[0])
                album = group["title"]
                if suffix and suffix.strip(" ()").lower() not in album.lower():
                    album += suffix
                earliest.append((date[:4], rank, album))
        if not earliest:
            return None

        # Prefer the studio album when it came out around the same time as the
        # song's first release (a single usually precedes its album). If it is
        # much later, it is a reissue with bonus tracks or a mislabeled
        # compilation, and the earliest release (soundtrack, EP, single) is
        # the original.
        first = min(earliest)
        studio = next((e for e in earliest if e[1] == 0), None)
        chosen = studio if studio and int(studio[0]) - int(first[0]) <= STUDIO_ALBUM_MAX_DELAY else first
        return {"album": chosen[2], "year": chosen[0]}


class AlbumOverrides:
    """Album/year values corrected by the user, stored on disk.

    Keyed like the MusicBrainz cache, so a correction applies to the same song
    in every playlist and is never replaced by a lookup result.
    """

    FIELDS = ("album", "year")

    def __init__(self, path: Optional[str] = None):
        self.path = path or os.path.join(
            os.path.expanduser("~"), ".playlistcat_album_overrides.json")
        self.overrides: Dict[str, Dict[str, str]] = {}
        try:
            with open(self.path) as f:
                self.overrides = json.load(f)
        except (OSError, ValueError):
            pass

    def get(self, key: str) -> Dict[str, str]:
        return self.overrides.get(key, {})

    def set(self, key: str, field: str, value: str):
        self.overrides.setdefault(key, {})[field] = value
        self._save()

    def clear(self, key: str, field: str):
        fields = self.overrides.get(key, {})
        fields.pop(field, None)
        if not fields:
            self.overrides.pop(key, None)
        self._save()

    def _save(self):
        try:
            with open(self.path, "w") as f:
                json.dump(self.overrides, f, indent=1)
        except OSError as e:
            print(f"Failed to save album corrections: {e}")
