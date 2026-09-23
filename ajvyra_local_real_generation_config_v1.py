"""
AJVYRA — REAL LOCAL GENERATION CONFIG v1

بدون API پولی.
بدون cloud generation.
بدون Replicate.
بدون سرویس اشتراکی.

موتور:
ComfyUI محلی + Workflow محلی + مدل ویدیویی محلی + FFmpeg
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LocalGenerationConfig:
    comfyui_url: str
    workflow_path: Path
    production_root: Path
    ffmpeg_binary: str
    ffprobe_binary: str

    width: int
    height: int
    fps: int

    segment_seconds: int
    segment_count: int
    anime_count: int

    timeout_seconds: int
    poll_seconds: float
    max_retries: int

    @classmethod
    def from_environment(cls) -> "LocalGenerationConfig":
        return cls(
            comfyui_url=os.getenv(
                "AJVYRA_COMFYUI_URL",
                "http://127.0.0.1:8188",
            ).rstrip("/"),

            workflow_path=Path(
                os.getenv(
                    "AJVYRA_WAN_WORKFLOW",
                    "workflows/ajvyra_wan_api.json",
                )
            ),

            production_root=Path(
                os.getenv(
                    "AJVYRA_PRODUCTION_ROOT",
                    "anime_assets",
                )
            ),

            ffmpeg_binary=os.getenv(
                "AJVYRA_FFMPEG",
                "ffmpeg",
            ),

            ffprobe_binary=os.getenv(
                "AJVYRA_FFPROBE",
                "ffprobe",
            ),

            width=int(os.getenv("AJVYRA_VIDEO_WIDTH", "832")),
            height=int(os.getenv("AJVYRA_VIDEO_HEIGHT", "480")),
            fps=int(os.getenv("AJVYRA_VIDEO_FPS", "16")),

            segment_seconds=int(
                os.getenv("AJVYRA_SEGMENT_SECONDS", "150")
            ),

            segment_count=int(
                os.getenv("AJVYRA_SEGMENT_COUNT", "12")
            ),

            anime_count=int(
                os.getenv("AJVYRA_ANIME_COUNT", "30")
            ),

            timeout_seconds=int(
                os.getenv("AJVYRA_GENERATION_TIMEOUT", "7200")
            ),

            poll_seconds=float(
                os.getenv("AJVYRA_GENERATION_POLL", "3")
            ),

            max_retries=int(
                os.getenv("AJVYRA_GENERATION_RETRIES", "2")
            ),
        )

    def validate(self) -> None:
        if self.anime_count != 30:
            raise RuntimeError("AJVYRA requires exactly 30 anime.")

        if self.segment_count != 12:
            raise RuntimeError(
                "AJVYRA requires exactly 12 segments per anime."
            )

        if self.segment_seconds != 150:
            raise RuntimeError(
                "Each anime segment must be exactly 150 seconds."
            )

        if self.segment_count * self.segment_seconds != 1800:
            raise RuntimeError(
                "Anime runtime contract must equal exactly 1800 seconds."
            )

        if self.width < 320 or self.height < 240:
            raise RuntimeError("Video resolution is too small.")

        if self.fps < 1:
            raise RuntimeError("FPS must be positive.")

        if not self.workflow_path.exists():
            raise FileNotFoundError(
                f"Real ComfyUI workflow not found: {self.workflow_path}"
            )

        self.production_root.mkdir(
            parents=True,
            exist_ok=True,
        )
