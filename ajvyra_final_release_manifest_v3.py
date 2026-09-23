"""
Creates the final immutable-ish release manifest.

This file is produced only after all 30 anime and 30 games pass.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from ajvyra_release_integrity_v3 import verify


def sha256(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)

    return h.hexdigest()


def build(root: Path) -> Path:
    verification = verify(root)

    if not verification["release_ready"]:
        raise RuntimeError(
            "AJVYRA release is blocked."
        )

    anime_manifest = root / "ajvyra_real_anime_manifest.json"
    game_manifest = root / "ajvyra_games_manifest_v3.json"

    manifest = {
        "project": "AJVYRA",
        "release": "3.0-final",
        "release_ready": True,
        "content": {
            "anime_count": 30,
            "game_count": 30,
            "anime_runtime_seconds": 1800,
            "browser_games": True,
        },
        "manifests": {
            "anime": {
                "path": str(anime_manifest),
                "sha256": sha256(anime_manifest),
            },
            "games": {
                "path": str(game_manifest),
                "sha256": sha256(game_manifest),
            },
        },
        "integrity": verification,
    }

    output = root / "AJVYRA_FINAL_RELEASE.json"

    output.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return output
