from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class AJVYRAAnimeReal30Publisher:

    def __init__(
        self,
        production_root: str = "generated/anime_production",
        website_root: str = "generated/anime_site",
        public_root: str = "public/anime",
    ):
        self.production_root = Path(production_root)
        self.website_root = Path(website_root)
        self.public_root = Path(public_root)

        self.website_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.public_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def publish_all(self) -> Dict[str, Any]:
        catalog = self._load_catalog()

        results = []

        for anime in catalog:
            results.append(
                self.publish_anime(anime)
            )

        published = sum(
            1
            for item in results
            if item["status"] == "WATCHABLE"
        )

        report = {
            "generated_at": self._now(),
            "total": len(results),
            "watchable": published,
            "not_ready": len(results) - published,
            "items": results,
        }

        self._write_json(
            self.website_root / "published_catalog.json",
            report,
        )

        return report

    def publish_anime(
        self,
        anime: Dict[str, Any],
    ) -> Dict[str, Any]:

        anime_id = anime["anime_id"]
        title = anime["title"]
        genre = anime["genre"]

        source = (
            self.production_root
            / anime_id
            / "season_01"
            / "episode_01"
            / "episode.mp4"
        )

        validation = self._validate_video(source)

        if not validation["valid"]:
            return {
                "anime_id": anime_id,
                "title": title,
                "genre": genre,
                "status": "NOT_READY",
                "reason": validation["reason"],
            }

        destination_dir = (
            self.public_root
            / anime_id
            / "season_01"
        )

        destination_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = (
            destination_dir
            / "episode_01.mp4"
        )

        shutil.copy2(
            source,
            destination,
        )

        checksum = self._sha256(
            destination
        )

        public_metadata = {
            "anime_id": anime_id,
            "title": title,
            "genre": genre,
            "season": 1,
            "episode": 1,
            "status": "WATCHABLE",
            "duration_seconds": validation[
                "duration_seconds"
            ],
            "file_size": destination.stat().st_size,
            "sha256": checksum,
            "video_url": (
                f"/anime/{anime_id}/"
                f"season_01/episode_01.mp4"
            ),
            "published_at": self._now(),
        }

        self._write_json(
            destination_dir / "episode_01.json",
            public_metadata,
        )

        self._write_json(
            self.website_root
            / anime_id
            / "anime.json",
            public_metadata,
        )

        return public_metadata

    def _load_catalog(self) -> List[Dict[str, Any]]:

        path = (
            self.production_root
            / "30_anime_master_catalog.json"
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Missing catalog: {path}"
            )

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        return data.get("entries", [])

    def _validate_video(
        self,
        path: Path,
    ) -> Dict[str, Any]:

        if not path.exists():
            return {
                "valid": False,
                "reason": "episode.mp4 does not exist.",
            }

        if path.stat().st_size < 1024:
            return {
                "valid": False,
                "reason": "Video file is suspiciously small.",
            }

        duration = self._ffprobe_duration(path)

        if duration is None:
            return {
                "valid": False,
                "reason": (
                    "FFprobe could not read the video."
                ),
            }

        if duration < 1700:
            return {
                "valid": False,
                "reason": (
                    f"Episode duration is only "
                    f"{duration:.2f}s; expected about 1800s."
                ),
            }

        return {
            "valid": True,
            "duration_seconds": duration,
        }

    @staticmethod
    def _ffprobe_duration(
        path: Path,
    ) -> Optional[float]:

        import subprocess

        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ]

        try:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            if result.returncode != 0:
                return None

            return float(
                result.stdout.strip()
            )

        except (
            FileNotFoundError,
            ValueError,
        ):
            return None

    @staticmethod
    def _sha256(path: Path) -> str:

        digest = hashlib.sha256()

        with path.open("rb") as file:
            for block in iter(
                lambda: file.read(1024 * 1024),
                b"",
            ):
                digest.update(block)

        return digest.hexdigest()

    @staticmethod
    def _now() -> str:
        return datetime.now(
            timezone.utc
        ).isoformat()

    @staticmethod
    def _write_json(
        path: Path,
        data: Dict[str, Any],
    ):

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
