"""
AJVYRA — REAL ANIME SEGMENT GENERATOR v1

یک Segment فقط زمانی complete محسوب می‌شود که:

1. ComfyUI واقعاً Job را اجرا کرده باشد.
2. ComfyUI واقعاً Output داده باشد.
3. Output واقعاً دانلود شده باشد.
4. فایل روی دیسک وجود داشته باشد.
5. حجم فایل حداقل باشد.

هیچ fake-success وجود ندارد.
"""

from __future__ import annotations

from pathlib import Path

from ajvyra_local_real_generation_config_v1 import (
    LocalGenerationConfig,
)
from ajvyra_comfyui_real_http_v1 import (
    RealComfyUIClient,
)
from ajvyra_wan_real_workflow_v1 import (
    WanRealWorkflow,
)
from ajvyra_real_anime_job_builder_v1 import (
    RealAnimeSegmentJob,
)
from ajvyra_real_anime_job_store_v1 import (
    AnimeJobStore,
)


class RealAnimeSegmentGenerator:

    def __init__(
        self,
        config: LocalGenerationConfig,
        client: RealComfyUIClient,
        workflow: WanRealWorkflow,
        store: AnimeJobStore,
    ):
        self.config = config
        self.client = client
        self.workflow = workflow
        self.store = store

    def generate(
        self,
        job: RealAnimeSegmentJob,
    ) -> Path:

        if self.store.completed(
            job.anime_number,
            job.segment_number,
            job.output_path,
        ):
            return job.output_path

        workflow = self.workflow.build(
            prompt=job.prompt,
            negative_prompt=(
                "low quality, blurry, broken anatomy, "
                "flicker, duplicate character, "
                "deformed face, malformed hands, "
                "static image, watermark, logo, text"
            ),
            seed=job.seed,
            width=self.config.width,
            height=self.config.height,
            frames=job.duration_seconds * self.config.fps,
        )

        self.store.set(
            job.anime_number,
            job.segment_number,
            status="queued",
            title=job.segment_title,
        )

        prompt_id = self.client.submit_workflow(
            workflow
        )

        self.store.set(
            job.anime_number,
            job.segment_number,
            status="running",
            prompt_id=prompt_id,
        )

        history = self.client.wait_for_completion(
            prompt_id
        )

        outputs = self.client.list_output_files(
            history
        )

        if not outputs:
            raise RuntimeError(
                f"No real output returned for "
                f"{job.anime_title} / "
                f"segment {job.segment_number}"
            )

        video_outputs = [
            item
            for item in outputs
            if Path(
                item["filename"]
            ).suffix.lower()
            in {".mp4", ".webm", ".mov", ".mkv"}
        ]

        if not video_outputs:
            raise RuntimeError(
                "ComfyUI completed but returned no video file."
            )

        selected = video_outputs[0]

        downloaded = self.client.download_output(
            selected,
            job.output_path,
        )

        if not downloaded.exists():
            raise RuntimeError(
                "Downloaded output does not exist."
            )

        if downloaded.stat().st_size < 100_000:
            raise RuntimeError(
                "Downloaded video failed real-media validation."
            )

        self.store.set(
            job.anime_number,
            job.segment_number,
            status="complete",
            prompt_id=prompt_id,
            output=str(downloaded),
            size_bytes=downloaded.stat().st_size,
        )

        return downloaded
