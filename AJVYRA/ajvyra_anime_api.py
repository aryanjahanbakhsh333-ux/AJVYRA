"""
AJVYRA Anime API
================

Central API server for the AJVYRA Anime System.

Features:
- Anime catalog API
- Search
- Genre filtering
- Anime details
- Segment information
- Asset availability
- Subtitle information
- Health/status endpoint
- Safe asset path handling
- CORS support
- JSON responses
- Mobile/web client friendly

Run:
    python ajvyra_anime_api.py

Server:
    http://127.0.0.1:8787
"""

from __future__ import annotations

import json
import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from ajvyra_anime_studio import (
    ANIME,
    ROOT,
    validate_catalog,
)


# ============================================================
# CONFIGURATION
# ============================================================

HOST = "127.0.0.1"
PORT = 8787

BASE_DIR = Path(__file__).resolve().parent
ASSET_ROOT = (BASE_DIR / ROOT).resolve()


# ============================================================
# HELPERS
# ============================================================

def json_bytes(data: object) -> bytes:
    """Convert Python data to UTF-8 JSON bytes."""
    return json.dumps(
        data,
        ensure_ascii=False,
        indent=2,
    ).encode("utf-8")


def anime_to_dict(anime) -> dict:
    """Convert an Anime object into API-safe JSON data."""

    return {
        "number": anime.number,
        "title": anime.title,
        "title_fa": anime.title_fa,
        "title_ja": anime.title_ja,
        "genre": anime.genre,
        "mood": anime.mood,
        "logline": anime.logline,

        "video": anime.video,
        "poster": anime.poster,

        "voice": {
            "fa": anime.voice.get("fa"),
            "ja": anime.voice.get("ja"),
        },

        "subtitles": {
            "en": anime.subtitles.get("en"),
            "fa": anime.subtitles.get("fa"),
            "ja": anime.subtitles.get("ja"),
        },

        "segments": [
            {
                "number": segment.number,
                "start": segment.start,
                "end": segment.end,
                "title": segment.title,
            }
            for segment in anime.segments
        ],
    }


def find_anime(number: int):
    """Find anime by numeric ID."""

    for anime in ANIME:
        if anime.number == number:
            return anime

    return None


def normalize_text(value: str) -> str:
    """Normalize text for search."""

    return (
        value
        .strip()
        .lower()
        .replace("ي", "ی")
        .replace("ك", "ک")
    )


def anime_matches_search(anime, query: str) -> bool:
    """Return True when an anime matches a search query."""

    query = normalize_text(query)

    if not query:
        return True

    searchable = " ".join(
        [
            str(anime.number),
            anime.title,
            anime.title_fa,
            anime.title_ja,
            anime.genre,
            anime.mood,
            anime.logline,
        ]
    )

    return query in normalize_text(searchable)


def safe_asset_path(relative_path: str) -> Path:
    """
    Resolve an asset safely.

    Prevents requests such as:
        ../secret.txt
    """

    relative = Path(
        unquote(relative_path)
    )

    target = (
        ASSET_ROOT / relative
    ).resolve()

    if (
        target != ASSET_ROOT
        and ASSET_ROOT not in target.parents
    ):
        raise PermissionError(
            "Invalid asset path."
        )

    return target


def asset_exists(relative_path: str) -> bool:
    """Check whether an asset exists."""

    try:
        return safe_asset_path(
            relative_path
        ).is_file()

    except PermissionError:
        return False


def asset_info(relative_path: str) -> dict:
    """Return information about an asset."""

    try:
        target = safe_asset_path(
            relative_path
        )

    except PermissionError:
        return {
            "exists": False,
            "size": 0,
            "type": None,
        }

    if not target.is_file():
        return {
            "exists": False,
            "size": 0,
            "type": None,
        }

    content_type = (
        mimetypes.guess_type(
            target.name
        )[0]
        or "application/octet-stream"
    )

    return {
        "exists": True,
        "size": target.stat().st_size,
        "type": content_type,
    }


# ============================================================
# CATALOG OPERATIONS
# ============================================================

def get_catalog(
    query: str = "",
    genre: str = "",
) -> list[dict]:

    results = []

    normalized_genre = normalize_text(
        genre
    )

    for anime in ANIME:

        if normalized_genre:

            if (
                normalize_text(anime.genre)
                != normalized_genre
            ):
                continue

        if not anime_matches_search(
            anime,
            query
        ):
            continue

        results.append(
            anime_to_dict(anime)
        )

    return results


def get_genres() -> list[str]:

    return sorted(
        {
            anime.genre
            for anime in ANIME
        }
    )


def get_stats() -> dict:

    genre_counts = {}

    for anime in ANIME:

        genre_counts.setdefault(
            anime.genre,
            0
        )

        genre_counts[anime.genre] += 1

    return {
        "total_anime": len(ANIME),
        "genres": genre_counts,
        "expected_episode_minutes": 30,
        "segments_per_episode": 12,
        "audio_languages": [
            "fa",
            "ja",
        ],
        "subtitle_languages": [
            "en",
            "fa",
            "ja",
        ],
    }


# ============================================================
# ASSET REPORT
# ============================================================

def build_asset_report(anime) -> dict:

    video = asset_info(
        anime.video
    )

    poster = asset_info(
        anime.poster
    )

    fa_voice = asset_info(
        anime.voice.get("fa", "")
    )

    ja_voice = asset_info(
        anime.voice.get("ja", "")
    )

    en_subtitle = asset_info(
        anime.subtitles.get("en", "")
    )

    fa_subtitle = asset_info(
        anime.subtitles.get("fa", "")
    )

    ja_subtitle = asset_info(
        anime.subtitles.get("ja", "")
    )

    required = [
        video["exists"],
        fa_voice["exists"],
        ja_voice["exists"],
        en_subtitle["exists"],
    ]

    ready = all(required)

    return {
        "anime": anime.number,
        "title": anime.title,
        "ready": ready,

        "video": video,
        "poster": poster,

        "voice": {
            "fa": fa_voice,
            "ja": ja_voice,
        },

        "subtitles": {
            "en": en_subtitle,
            "fa": fa_subtitle,
            "ja": ja_subtitle,
        },
    }


# ============================================================
# HTTP HANDLER
# ============================================================

class AnimeAPIHandler(
    BaseHTTPRequestHandler
):

    server_version = "AJVYRA-Anime-API/1.0"


    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    def send_json(
        self,
        data,
        status=HTTPStatus.OK,
    ):

        payload = json_bytes(data)

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
        )

        self.send_header(
            "Content-Length",
            str(len(payload)),
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*",
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, OPTIONS",
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type",
        )

        self.end_headers()

        self.wfile.write(payload)


    def send_file(
        self,
        target: Path,
    ):

        if not target.is_file():

            return self.send_error(
                HTTPStatus.NOT_FOUND,
                "Asset not found.",
            )

        try:

            data = target.read_bytes()

        except OSError:

            return self.send_error(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                "Unable to read asset.",
            )

        content_type = (
            mimetypes.guess_type(
                target.name
            )[0]
            or "application/octet-stream"
        )

        self.send_response(
            HTTPStatus.OK
        )

        self.send_header(
            "Content-Type",
            content_type,
        )

        self.send_header(
            "Content-Length",
            str(len(data)),
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*",
        )

        self.end_headers()

        self.wfile.write(data)


    # --------------------------------------------------------
    # OPTIONS
    # --------------------------------------------------------

    def do_OPTIONS(self):

        self.send_response(
            HTTPStatus.NO_CONTENT
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*",
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, OPTIONS",
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type",
        )

        self.end_headers()


    # --------------------------------------------------------
    # GET ROUTER
    # --------------------------------------------------------

    def do_GET(self):

        parsed = urlparse(
            self.path
        )

        path = parsed.path

        params = parse_qs(
            parsed.query
        )


        try:

            # ------------------------------------------------
            # ROOT
            # ------------------------------------------------

            if path == "/":

                return self.send_json(
                    {
                        "name":
                            "AJVYRA Anime API",

                        "version":
                            "1.0",

                        "status":
                            "online",

                        "endpoints": [

                            "/api/anime",

                            "/api/anime/{id}",

                            "/api/search?q=",

                            "/api/genres",

                            "/api/stats",

                            "/api/status",

                            "/api/assets/{id}",

                            "/asset/{path}",
                        ],
                    }
                )


            # ------------------------------------------------
            # FULL CATALOG
            # ------------------------------------------------

            if path == "/api/anime":

                query = params.get(
                    "q",
                    [""]
                )[0]

                genre = params.get(
                    "genre",
                    [""]
                )[0]

                return self.send_json(
                    {
                        "count":
                            len(
                                get_catalog(
                                    query,
                                    genre,
                                )
                            ),

                        "anime":
                            get_catalog(
                                query,
                                genre,
                            ),
                    }
                )


            # ------------------------------------------------
            # SEARCH
            # ------------------------------------------------

            if path == "/api/search":

                query = params.get(
                    "q",
                    [""]
                )[0]

                results = get_catalog(
                    query=query
                )

                return self.send_json(
                    {
                        "query":
                            query,

                        "count":
                            len(results),

                        "results":
                            results,
                    }
                )


            # ------------------------------------------------
            # GENRES
            # ------------------------------------------------

            if path == "/api/genres":

                return self.send_json(
                    {
                        "genres":
                            get_genres()
                    }
                )


            # ------------------------------------------------
            # STATS
            # ------------------------------------------------

            if path == "/api/stats":

                return self.send_json(
                    get_stats()
                )


            # ------------------------------------------------
            # STATUS
            # ------------------------------------------------

            if path == "/api/status":

                valid, errors = (
                    validate_catalog()
                )

                return self.send_json(
                    {
                        "online":
                            True,

                        "catalog_valid":
                            valid,

                        "anime_count":
                            len(ANIME),

                        "errors":
                            errors,
                    }
                )


            # ------------------------------------------------
            # SINGLE ANIME
            # ------------------------------------------------

            if path.startswith(
                "/api/anime/"
            ):

                value = path[
                    len("/api/anime/"):
                ]

                try:

                    number = int(value)

                except ValueError:

                    return self.send_json(
                        {
                            "error":
                                "Anime ID must be a number."
                        },
                        HTTPStatus.BAD_REQUEST,
                    )


                anime = find_anime(
                    number
                )


                if anime is None:

                    return self.send_json(
                        {
                            "error":
                                "Anime not found."
                        },
                        HTTPStatus.NOT_FOUND,
                    )


                return self.send_json(
                    anime_to_dict(anime)
                )


            # ------------------------------------------------
            # ASSET REPORT
            # ------------------------------------------------

            if path.startswith(
                "/api/assets/"
            ):

                value = path[
                    len("/api/assets/"):
                ]

                try:

                    number = int(value)

                except ValueError:

                    return self.send_json(
                        {
                            "error":
                                "Anime ID must be a number."
                        },
                        HTTPStatus.BAD_REQUEST,
                    )


                anime = find_anime(
                    number
                )


                if anime is None:

                    return self.send_json(
                        {
                            "error":
                                "Anime not found."
                        },
                        HTTPStatus.NOT_FOUND,
                    )


                return self.send_json(
                    build_asset_report(
                        anime
                    )
                )


            # ------------------------------------------------
            # RAW ASSET
            # ------------------------------------------------

            if path.startswith(
                "/asset/"
            ):

                relative_path = path[
                    len("/asset/"):
                ]

                target = safe_asset_path(
                    relative_path
                )

                return self.send_file(
                    target
                )


            # ------------------------------------------------
            # NOT FOUND
            # ------------------------------------------------

            return self.send_json(
                {
                    "error":
                        "Endpoint not found.",

                    "path":
                        path,
                },
                HTTPStatus.NOT_FOUND,
            )


        except PermissionError:

            return self.send_json(
                {
                    "error":
                        "Forbidden asset path."
                },
                HTTPStatus.FORBIDDEN,
            )


        except Exception as error:

            return self.send_json(
                {
                    "error":
                        "Internal server error.",

                    "message":
                        str(error),
                },
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )


    def log_message(
        self,
        format_string,
        *args,
    ):

        print(
            "[AJVYRA API]",
            format_string % args
        )


# ============================================================
# SERVER
# ============================================================

def main():

    print()
    print("=" * 55)
    print("             AJVYRA ANIME API")
    print("=" * 55)
    print()

    valid, errors = (
        validate_catalog()
    )

    if not valid:

        print(
            "Catalog validation failed:"
        )

        for error in errors:

            print(
                " -",
                error
            )

        raise SystemExit(1)


    print(
        f"Anime catalog: {len(ANIME)} episodes"
    )

    print(
        f"Asset root: {ASSET_ROOT}"
    )

    print()

    print(
        f"API running at:"
    )

    print(
        f"http://{HOST}:{PORT}"
    )

    print()

    print(
        "Press Ctrl+C to stop."
    )

    print()


    server = ThreadingHTTPServer(
        (
            HOST,
            PORT
        ),
        AnimeAPIHandler,
    )


    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print()
        print(
            "AJVYRA Anime API stopped."
        )

    finally:

        server.server_close()


if __name__ == "__main__":

    main()
