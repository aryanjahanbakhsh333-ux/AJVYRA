from __future__ import annotations

import os

from ajvyra_browser_game_manifest_v1 import (
    save_manifest,
)


REQUIRED_FILES = [
    "ajvyra_game_browser.html",
    "ajvyra_game_browser_v1.css",
    "ajvyra_game_browser_v1.js",
]


def prepare_release() -> dict:
    missing = [
        filename
        for filename in REQUIRED_FILES
        if not os.path.exists(filename)
    ]

    if missing:
        return {
            "ready": False,
            "missing": missing,
        }

    save_manifest()

    return {
        "ready": True,
        "manifest": "ajvyra_game_manifest.json",
        "browser": "ajvyra_game_browser.html",
    }


if __name__ == "__main__":
    result = prepare_release()

    print(result)
