from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class AJVYRAAIVideoSiteBridge:
    """
    Converts AI-generated video records into the same type of
    catalog item that the AJVYRA website can consume.
    """

    def __init__(
        self,
        catalog_path: str = (
            "assets/ai-video-library/"
            "ajvyra-ai-site-catalog.json"
        ),
    ):
        self.catalog_path = Path(catalog_path)

    def load(self) -> dict[str, Any]:
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

    def ready_videos(self) -> list[dict[str, Any]]:
        catalog = self.load()

        result = []

        for video in catalog.get("videos", []):
            if not isinstance(video, dict):
                continue

            if not video.get("ready"):
                continue

            if not video.get("published"):
                continue

            if not video.get("video_url"):
                continue

            result.append(
                {
                    "id": video.get("id"),
                    "title": video.get("title"),
                    "type": "community-ai-video",
                    "style": video.get("style"),
                    "prompt": video.get("prompt"),
                    "video_url": video.get("video_url"),
                    "poster_url": video.get("poster_url"),
                    "subtitle_url": video.get("subtitle_url"),
                    "created_at": video.get("created_at"),
                    "source": "AJVYRA AI Video Studio",
                }
            )

        return result

    def build_site_payload(self) -> dict[str, Any]:
        videos = self.ready_videos()

        return {
            "section": "AI Community",
            "items": videos,
            "count": len(videos),
        }

    def write_site_payload(
        self,
        output_path: str = (
            "assets/ai-video-library/"
            "ajvyra-ai-community-feed.json"
        ),
    ) -> str:

        target = Path(output_path)

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = self.build_site_payload()

        with target.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                payload,
                file,
                ensure_ascii=False,
                indent=2,
            )

        return str(target)
