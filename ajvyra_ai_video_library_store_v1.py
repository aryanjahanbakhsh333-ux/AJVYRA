from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_LIBRARY = Path(
    "assets/ai-video-library/ajvyra-ai-video-library.json"
)


class AJVYRAAIVideoLibrary:
    """
    Local metadata catalog for AI-generated AJVYRA videos.

    Video binaries remain separate from metadata.
    """

    def __init__(self, catalog_path: Path = DEFAULT_LIBRARY):
        self.catalog_path = Path(catalog_path)
        self.catalog_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _read(self) -> dict[str, Any]:
        if not self.catalog_path.exists():
            return {
                "schema_version": 1,
                "videos": [],
            }

        with self.catalog_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def _write(self, data: dict[str, Any]) -> None:
        temp_path = self.catalog_path.with_suffix(".tmp")

        with temp_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2,
            )

        temp_path.replace(self.catalog_path)

    def add_video(
        self,
        prompt: str,
        video_url: str,
        local_path: str | None = None,
        title: str | None = None,
        style: str = "anime-animation",
    ) -> dict[str, Any]:

        if not video_url:
            raise ValueError("video_url is required.")

        data = self._read()

        video_id = f"ai-{secrets.token_hex(8)}"

        now = datetime.now(timezone.utc).isoformat()

        if not title:
            title = "AJVYRA AI Creation"

        item = {
            "id": video_id,
            "title": title,
            "type": "community-ai-video",
            "style": style,
            "prompt": prompt,
            "video_url": video_url,
            "local_path": local_path,
            "created_at": now,
            "published": True,
            "ready": True,
            "source": "AJVYRA AI Video Studio",
        }

        data["videos"].append(item)

        self._write(data)

        return item

    def list_videos(self) -> list[dict[str, Any]]:
        return self._read().get("videos", [])

    def export_site_catalog(
        self,
        output_path: Path = Path(
            "assets/ai-video-library/ajvyra-ai-site-catalog.json"
        ),
    ) -> Path:

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        videos = self.list_videos()

        catalog = {
            "schema_version": 1,
            "source": "AJVYRA AI Video Studio",
            "videos": videos,
        }

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                catalog,
                file,
                ensure_ascii=False,
                indent=2,
            )

        return output_path
