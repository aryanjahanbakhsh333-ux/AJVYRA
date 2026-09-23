from __future__ import annotations

import json
import secrets
from pathlib import Path
from typing import Any

from ajvyra_ai_video_generation_core_v1 import (
    generate_anime_video,
)

from ajvyra_ai_video_persistent_publisher_v2 import (
    AJVYRAAIVideoPersistentPublisher,
)

from ajvyra_ai_video_job_queue_v2 import (
    AJVYRAAIVideoJobQueue,
)


class AJVYRAAIVideoStudioController:

    def __init__(
        self,
        catalog_path: str = (
            "assets/ai-video-library/"
            "ajvyra-ai-community-feed-v2.json"
        ),
    ):

        self.catalog_path = Path(
            catalog_path
        )

        self.catalog_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.queue = (
            AJVYRAAIVideoJobQueue()
        )

        self.publisher = (
            AJVYRAAIVideoPersistentPublisher()
        )

    def _read_catalog(self) -> dict[str, Any]:

        if not self.catalog_path.exists():
            return {
                "schema_version": 2,
                "section": "AI Community",
                "videos": [],
            }

        with self.catalog_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def _write_catalog(
        self,
        data: dict[str, Any],
    ) -> None:

        temporary = (
            self.catalog_path.with_suffix(
                ".tmp"
            )
        )

        with temporary.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2,
            )

        temporary.replace(
            self.catalog_path
        )

    def _register_ready_video(
        self,
        job: Any,
    ) -> None:

        data = self._read_catalog()

        videos = data.setdefault(
            "videos",
            [],
        )

        if any(
            item.get("id") == job.job_id
            for item in videos
        ):
            return

        videos.append(
            {
                "id": job.job_id,
                "title": (
                    "AJVYRA AI Creation"
                ),
                "type": (
                    "community-ai-video"
                ),
                "style": (
                    "anime-animation"
                ),
                "prompt": job.prompt,
                "video_url": job.video_url,
                "created_at": job.created_at,
                "published": True,
                "ready": True,
                "source": (
                    "AJVYRA AI Video Studio"
                ),
            }
        )

        data["count"] = len(videos)

        self._write_catalog(data)

    def create_video(
        self,
        prompt: str,
        session_id: str | None = None,
    ) -> dict[str, Any]:

        if session_id is None:
            session_id = (
                "session-"
                + secrets.token_hex(8)
            )

        job = self.queue.create(
            prompt=prompt,
            session_id=session_id,
        )

        final_job = self.queue.run_job(
            job.job_id,
            generator=lambda text: (
                generate_anime_video(
                    prompt=text,
                    num_frames=49,
                    fps=16,
                    inference_steps=20,
                    guidance_scale=5.0,
                )
            ),
            publisher=lambda local_path, job_id: (
                self.publisher.publish(
                    local_video_path=local_path,
                    video_id=job_id,
                )
            ),
        )

        if final_job.status == "ready":
            self._register_ready_video(
                final_job
            )

        return final_job.to_dict()

    def get_job(
        self,
        job_id: str,
    ) -> dict[str, Any]:

        job = self.queue.get(job_id)

        if job is None:
            return {
                "status": "not_found",
                "job_id": job_id,
            }

        return job.to_dict()

    def get_site_feed(self) -> dict[str, Any]:

        data = self._read_catalog()

        ready = [
            item
            for item in data.get(
                "videos",
                [],
            )
            if item.get("ready")
            and item.get("published")
            and item.get("video_url")
        ]

        return {
            "schema_version": 2,
            "section": "AI Community",
            "count": len(ready),
            "videos": ready,
        }
