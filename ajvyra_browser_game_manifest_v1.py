from __future__ import annotations

import json
from ajvyra_game_catalog_v1 import AJVYRAGameCatalog


def build_manifest() -> dict:
    catalog = AJVYRAGameCatalog()

    games = catalog.all_games()

    return {
        "name": "AJVYRA",
        "version": "1.0",
        "target_games": 300,
        "games": games,
    }


def save_manifest(path: str = "ajvyra_game_manifest.json") -> None:
    manifest = build_manifest()

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            manifest,
            file,
            ensure_ascii=False,
            indent=2,
        )


if __name__ == "__main__":
    save_manifest()
    print("AJVYRA manifest generated.")
