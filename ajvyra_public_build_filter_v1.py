"""
AJVYRA PUBLIC BUILD FILTER
===========================

Purpose:
    Remove legacy/unused Anime references from the PUBLIC build.

Important:
    - Does NOT delete Anime files.
    - Does NOT modify legacy Anime files.
    - Does NOT show an "Anime disabled" message.
    - Does NOT expose Anime routes.
    - Does NOT expose Anime API data.
    - Does NOT expose Anime in search.
    - Does NOT expose Anime in navigation.
    - Only public features are allowed through this filter.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


# ============================================================
# PUBLIC FEATURE DEFINITIONS
# ============================================================

PUBLIC_FEATURES = frozenset({
    "games",
    "music",
    "community",
    "profiles",
    "search",
})


# Anything containing one of these identifiers is considered
# an internal/legacy Anime reference and must never enter the
# public build.
PRIVATE_IDENTIFIERS = frozenset({
    "anime",
    "anime_wallpaper",
    "anime_video",
    "anime_audio",
    "anime_subtitles",
    "anime_player",
    "anime_catalog",
    "anime_production",
    "anime_studio",
})


# ============================================================
# RESULT MODEL
# ============================================================

@dataclass(frozen=True)
class PublicBuildResult:
    data: Dict[str, Any]
    removed_items: int


# ============================================================
# IDENTIFIER CHECKING
# ============================================================

def normalize_identifier(value: Any) -> str:
    """
    Normalize an identifier for safe comparison.
    """

    if value is None:
        return ""

    return str(value).strip().casefold()


def contains_private_identifier(value: Any) -> bool:
    """
    Detect Anime/internal identifiers without exposing them
    in the public build.
    """

    normalized = normalize_identifier(value)

    if not normalized:
        return False

    if normalized in PRIVATE_IDENTIFIERS:
        return True

    # Handle paths, routes and compound identifiers.
    tokens = (
        normalized
        .replace("\\", "/")
        .replace(":", "/")
        .replace("-", "_")
        .split("/")
    )

    for token in tokens:
        if token in PRIVATE_IDENTIFIERS:
            return True

    return False


# ============================================================
# DICTIONARY FILTER
# ============================================================

def filter_public_dict(
    data: Dict[str, Any],
) -> tuple[Dict[str, Any], int]:

    clean: Dict[str, Any] = {}
    removed = 0

    for key, value in data.items():

        if contains_private_identifier(key):
            removed += 1
            continue

        if isinstance(value, dict):

            nested, nested_removed = filter_public_dict(value)

            clean[key] = nested
            removed += nested_removed

        elif isinstance(value, list):

            filtered_list = []

            for item in value:

                if contains_private_identifier(item):
                    removed += 1
                    continue

                if isinstance(item, dict):

                    nested, nested_removed = filter_public_dict(item)

                    filtered_list.append(nested)
                    removed += nested_removed

                else:
                    filtered_list.append(item)

            clean[key] = filtered_list

        else:

            if contains_private_identifier(value):
                removed += 1
                continue

            clean[key] = value

    return clean, removed


# ============================================================
# ROUTE FILTER
# ============================================================

def filter_public_routes(
    routes: Iterable[Any],
) -> List[Any]:

    public_routes = []

    for route in routes:

        if contains_private_identifier(route):
            continue

        public_routes.append(route)

    return public_routes


# ============================================================
# NAVIGATION FILTER
# ============================================================

def filter_public_navigation(
    navigation: Iterable[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    result = []

    for item in navigation:

        if not isinstance(item, dict):
            continue

        name = item.get("name")
        href = item.get("href")
        route = item.get("route")

        if (
            contains_private_identifier(name)
            or contains_private_identifier(href)
            or contains_private_identifier(route)
        ):
            continue

        result.append(item)

    return result


# ============================================================
# SEARCH FILTER
# ============================================================

def filter_public_search_results(
    results: Iterable[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    public_results = []

    for result in results:

        if not isinstance(result, dict):
            continue

        searchable_values = [
            result.get("id"),
            result.get("name"),
            result.get("title"),
            result.get("category"),
            result.get("route"),
            result.get("url"),
        ]

        if any(
            contains_private_identifier(value)
            for value in searchable_values
        ):
            continue

        public_results.append(result)

    return public_results


# ============================================================
# API FILTER
# ============================================================

def filter_public_api_payload(
    payload: Dict[str, Any],
) -> Dict[str, Any]:

    clean, _ = filter_public_dict(payload)

    return clean


# ============================================================
# FEATURE CHECK
# ============================================================

def is_public_feature(feature_name: str) -> bool:

    normalized = normalize_identifier(feature_name)

    if contains_private_identifier(normalized):
        return False

    return normalized in PUBLIC_FEATURES


# ============================================================
# PUBLIC BUILD CREATOR
# ============================================================

class AJVYRAPublicBuild:

    def __init__(self) -> None:

        self.public_features = PUBLIC_FEATURES

    def build_manifest(self) -> Dict[str, Any]:
        """
        Creates a manifest containing only public features.

        Anime is intentionally absent rather than marked disabled.
        """

        return {
            "project": "AJVYRA",
            "build": "public",
            "features": sorted(self.public_features),
        }

    def clean_routes(
        self,
        routes: Iterable[Any],
    ) -> List[Any]:

        return filter_public_routes(routes)

    def clean_navigation(
        self,
        navigation: Iterable[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        return filter_public_navigation(navigation)

    def clean_search(
        self,
        results: Iterable[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        return filter_public_search_results(results)

    def clean_api(
        self,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:

        return filter_public_api_payload(payload)

    def clean_page_data(
        self,
        page_data: Dict[str, Any],
    ) -> PublicBuildResult:

        clean, removed = filter_public_dict(page_data)

        return PublicBuildResult(
            data=clean,
            removed_items=removed,
        )


# ============================================================
# FINAL PUBLIC BUILD VALIDATION
# ============================================================

def validate_public_build(
    build_data: Dict[str, Any],
) -> bool:
    """
    Final safety check.

    If any Anime identifier survives anywhere in the public
    build structure, validation fails.
    """

    def scan(value: Any) -> bool:

        if isinstance(value, dict):

            for key, item in value.items():

                if contains_private_identifier(key):
                    return False

                if not scan(item):
                    return False

            return True

        if isinstance(value, list):

            for item in value:

                if not scan(item):
                    return False

            return True

        return not contains_private_identifier(value)

    return scan(build_data)


# ============================================================
# PUBLIC BUILD ENTRY POINT
# ============================================================

def create_clean_public_build(
    source_data: Dict[str, Any],
) -> Dict[str, Any]:

    builder = AJVYRAPublicBuild()

    result = builder.clean_page_data(source_data)

    if not validate_public_build(result.data):
        raise RuntimeError(
            "Public build contains a forbidden internal reference."
        )

    return result.data


# ============================================================
# EXAMPLE
# ============================================================

if __name__ == "__main__":

    source = {
        "project": "AJVYRA",

        "navigation": [
            {
                "name": "Games",
                "href": "/games",
            },
            {
                "name": "Legacy",
                "href": "/internal/anime",
            },
        ],

        "routes": [
            "/",
            "/games",
            "/anime",
            "/community",
        ],

        "features": {
            "games": True,
            "music": True,
            "anime": True,
        },

        "search": [
            {
                "id": "game_001",
                "title": "Shadow Runner",
                "category": "games",
            },
            {
                "id": "anime_001",
                "title": "Legacy Content",
                "category": "anime",
            },
        ],
    }

    public_build = create_clean_public_build(source)

    print("AJVYRA PUBLIC BUILD")
    print("===================")
    print(public_build)

    if validate_public_build(public_build):
        print("\nPUBLIC BUILD VALID.")
    else:
        print("\nPUBLIC BUILD REJECTED.")
