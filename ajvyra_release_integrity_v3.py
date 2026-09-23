"""
AJVYRA final integrity gate.

Checks:
- 30 anime final videos
- 30 anime posters
- anime manifest
- 30 browser games
- game manifest
- game playability report
"""

from __future__ import annotations

import json
from pathlib import Path


class ReleaseBlocked(RuntimeError):
    pass


def load_json(path: Path) -> dict:
    if not path.exists():
        raise ReleaseBlocked(f"Missing: {path}")

    try:
        return json.loads(
            path.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        raise ReleaseBlocked(
            f"Invalid JSON: {path}"
        ) from exc


def check_anime(root: Path) -> dict:
    manifest_path = root / "ajvyra_real_anime_manifest.json"

    data = load_json(manifest_path)

    anime = data.get("anime", [])

    if len(anime) != 30:
        raise ReleaseBlocked(
            f"Anime count is {len(anime)}, expected 30."
        )

    checked = 0

    for item in anime:
        video = root / item["video"]
        poster = root / item["poster"]

        if not video.exists():
            raise ReleaseBlocked(
                f"Missing anime video: {video}"
            )

        if video.stat().st_size < 100_000:
            raise ReleaseBlocked(
                f"Anime video is too small: {video}"
            )

        if not poster.exists():
            raise ReleaseBlocked(
                f"Missing anime poster: {poster}"
            )

        if poster.stat().st_size < 10_000:
            raise ReleaseBlocked(
                f"Anime poster is invalid: {poster}"
            )

        checked += 1

    return {
        "expected": 30,
        "checked": checked,
        "ready": checked == 30,
    }


def check_games(root: Path) -> dict:
    manifest = load_json(
        root / "ajvyra_games_manifest_v3.json"
    )

    probe = load_json(
        root / "game_playability_report.json"
    )

    games = manifest.get("games", [])

    if len(games) != 30:
        raise ReleaseBlocked(
            f"Game count is {len(games)}, expected 30."
        )

    if probe.get("playable") != 30:
        raise ReleaseBlocked(
            f"Only {probe.get('playable')}/30 games "
            "passed playability."
        )

    for game in games:
        path = root / "games" / f"game_{game['number']:02d}" / "index.html"

        if not path.exists():
            raise ReleaseBlocked(
                f"Missing game runtime: {path}"
            )

        if path.stat().st_size < 5000:
            raise ReleaseBlocked(
                f"Invalid game runtime: {path}"
            )

    return {
        "expected": 30,
        "checked": 30,
        "playable": 30,
        "ready": True,
    }


def verify(root: Path) -> dict:
    anime = check_anime(root)
    games = check_games(root)

    return {
        "project": "AJVYRA",
        "anime": anime,
        "games": games,
        "release_ready": True,
    }
