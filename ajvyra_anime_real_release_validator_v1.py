from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


class AnimeRealReleaseValidator:
    """
    Hard validation layer for real AJVYRA anime releases.
    """

    REQUIRED_FIELDS = {
        "title",
        "final_movie",
        "ready",
    }

    def __init__(self, ffprobe: str = "ffprobe"):
        self.ffprobe = ffprobe

    def probe_video(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            raise FileNotFoundError(path)

        command = [
            self.ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration,size,format_name",
            "-of",
            "json",
            str(path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip() or
                "ffprobe failed"
            )

        data = json.loads(result.stdout)
        fmt = data.get("format", {})

        duration = float(
            fmt.get("duration", 0) or 0
        )

        size = int(
            fmt.get("size", 0) or 0
        )

        if duration <= 0:
            raise RuntimeError(
                f"Video has no valid duration: {path}"
            )

        if size <= 0:
            raise RuntimeError(
                f"Video has no valid size: {path}"
            )

        return {
            "duration": duration,
            "bytes": size,
            "format": fmt.get("format_name"),
        }

    def validate_release_file(
        self,
        manifest_path: str,
    ) -> dict[str, Any]:

        path = Path(manifest_path)

        if not path.exists():
            raise FileNotFoundError(path)

        data = json.loads(
            path.read_text(encoding="utf-8")
        )

        missing = self.REQUIRED_FIELDS - set(data)

        if missing:
            raise RuntimeError(
                f"Missing manifest fields: {sorted(missing)}"
            )

        if not data["ready"]:
            raise RuntimeError(
                f"Release is not marked ready: {data.get('title')}"
            )

        movie = Path(
            data["final_movie"]["path"]
        )

        media = self.probe_video(movie)

        return {
            "title": data["title"],
            "ready": True,
            "published": bool(
                data.get("published", False)
            ),
            "movie": str(movie),
            "media": media,
        }

    def validate_catalog(
        self,
        manifest_directory: str,
        expected_count: int = 30,
    ) -> list[dict[str, Any]]:

        directory = Path(manifest_directory)

        files = sorted(
            directory.glob("*.release.json")
        )

        if len(files) != expected_count:
            raise RuntimeError(
                f"Expected {expected_count} real anime releases, "
                f"found {len(files)}."
            )

        releases = []

        for file in files:
            releases.append(
                self.validate_release_file(
                    str(file)
                )
            )

        return releases


if __name__ == "__main__":
    print(
        "AJVYRA Anime Real Release Validator loaded."
    )
