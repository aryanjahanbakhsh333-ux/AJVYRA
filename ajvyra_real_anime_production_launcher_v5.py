from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


class RealAnimeProductionLauncher:
    """
    Launches the real local anime production engine.

    This class never creates fake MP4 files.
    A successful result requires actual generated media.
    """

    def __init__(self, root="generated/ajvyra_release"):
        self.root = Path(root)

    def command(self):
        engine = Path(
            os.getenv(
                "AJVYRA_ANIME_ENGINE",
                "ajvyra_real_anime_production_engine.py",
            )
        )

        if not engine.exists():
            raise FileNotFoundError(
                f"Anime production engine not found: {engine}"
            )

        return [
            sys.executable,
            str(engine),
        ]

    def run(self):
        self.root.mkdir(parents=True, exist_ok=True)

        result = subprocess.run(
            self.command(),
            text=True,
        )

        report = {
            "project": "AJVYRA",
            "stage": "REAL_ANIME_PRODUCTION",
            "return_code": result.returncode,
            "passed": result.returncode == 0,
            "fake_media_allowed": False,
        }

        (self.root / "REAL_ANIME_PRODUCTION_RESULT_V5.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Real anime production did not complete successfully."
            )

        return report


if __name__ == "__main__":
    print(json.dumps(
        RealAnimeProductionLauncher().run(),
        indent=2,
        ensure_ascii=False,
    ))
