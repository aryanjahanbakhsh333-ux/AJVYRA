from __future__ import annotations

import json
import shutil
from pathlib import Path


class AJVYRAReleasePreflight:
    def __init__(self, root="generated/ajvyra_release"):
        self.root = Path(root)

    def check(self):
        checks = {
            "root_exists": self.root.exists(),
            "python": shutil.which("python") is not None,
            "ffmpeg": shutil.which("ffmpeg") is not None,
            "ffprobe": shutil.which("ffprobe") is not None,
            "anime_engine": Path(
                "ajvyra_real_anime_production_engine.py"
            ).exists(),
            "anime_manifest_source": Path(
                "ajvyra_anime_studio.py"
            ).exists(),
            "game_builder": Path(
                "ajvyra_browser_game_builder_v3.py"
            ).exists(),
        }

        report = {
            "project": "AJVYRA",
            "stage": "PREFLIGHT",
            "passed": all(checks.values()),
            "checks": checks,
        }

        self.root.mkdir(parents=True, exist_ok=True)

        (self.root / "TRUE_RELEASE_PREFLIGHT_V5.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return report


if __name__ == "__main__":
    print(json.dumps(
        AJVYRAReleasePreflight().check(),
        indent=2,
        ensure_ascii=False,
    ))
