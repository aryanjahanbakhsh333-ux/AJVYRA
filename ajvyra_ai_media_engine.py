"""
AJVYRA AI MEDIA ENGINE
======================

FINAL HIGH-LEVEL MEDIA ENGINE.

The rest of AJVYRA talks to THIS file.

It exposes one unified interface:

    generate_image()
    generate_voice()
    generate_video()
    generate_anime_media()

The central AI therefore does not need to know how FFmpeg,
Pillow, TTS, image models or future video models work.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from ajvyra_ai_image_generation_engine import (
    AJVYRAAIImageGenerationEngine,
    ImageRequest,
)

from ajvyra_ai_voice_generation_engine import (
    AJVYRAAIVoiceGenerationEngine,
    VoiceRequest,
)

from ajvyra_ai_video_generation_engine import (
    AJVYRAAIVideoGenerationEngine,
    VideoRequest,
)

from ajvyra_ai_media_generation_orchestrator import (
    AJVYRAAIMediaGenerationOrchestrator,
)


class AJVYRAAIMediaEngine:

    ENGINE_ID = (
        "AJVYRA-AI-UNIFIED-MEDIA-ENGINE-V1"
    )

    def __init__(
        self,
        root: Path | str,
    ) -> None:

        self.root = Path(
            root
        ).resolve()

        self.image_engine = (
            AJVYRAAIImageGenerationEngine(
                self.root
            )
        )

        self.voice_engine = (
            AJVYRAAIVoiceGenerationEngine(
                self.root
            )
        )

        self.video_engine = (
            AJVYRAAIVideoGenerationEngine(
                self.root
            )
        )

        self.orchestrator = (
            AJVYRAAIMediaGenerationOrchestrator(
                self.root
            )
        )

    # =========================================================
    # IMAGE
    # =========================================================

    def generate_image(
        self,
        project_id: str,
        prompt: str,
        output_name: str = "image.png",
        width: int = 1280,
        height: int = 720,
        style: str = "anime cinematic",
    ) -> Dict[str, Any]:

        return self.image_engine.generate(
            ImageRequest(
                project_id=project_id,
                prompt=prompt,
                width=width,
                height=height,
                style=style,
                output_name=output_name,
            )
        )

    # =========================================================
    # VOICE
    # =========================================================

    def generate_voice(
        self,
        project_id: str,
        speaker_id: str,
        text: str,
        language: str = "fa",
        emotion: str = "neutral",
        output_name: str = "voice.wav",
    ) -> Dict[str, Any]:

        return self.voice_engine.generate(
            VoiceRequest(
                project_id=project_id,
                speaker_id=speaker_id,
                text=text,
                language=language,
                emotion=emotion,
                output_name=output_name,
            )
        )

    # =========================================================
    # VIDEO
    # =========================================================

    def generate_video(
        self,
        project_id: str,
        frames_dir: str,
        audio_files: List[str] | None = None,
        duration_seconds: int = 1800,
        output_name: str = "episode.mp4",
    ) -> Dict[str, Any]:

        return self.video_engine.render(
            VideoRequest(
                project_id=project_id,
                frames_dir=frames_dir,
                audio_files=audio_files or [],
                duration_seconds=duration_seconds,
                output_name=output_name,
            )
        )

    # =========================================================
    # COMPLETE ANIME
    # =========================================================

    def generate_anime(
        self,
        project: Dict[str, Any],
    ) -> Dict[str, Any]:

        return (
            self.orchestrator.generate_anime_media(
                project
            )
        )

    # =========================================================
    # ENGINE STATUS
    # =========================================================

    def status(self) -> Dict[str, Any]:

        ffmpeg = self._binary_exists(
            "ffmpeg"
        )

        return {
            "engine": self.ENGINE_ID,
            "image_engine": {
                "available": True,
            },
            "voice_engine": {
                "available": True,
            },
            "video_engine": {
                "available": ffmpeg,
                "ffmpeg": ffmpeg,
            },
            "output_root": str(
                self.root
                / "generated"
            ),
        }

    # =========================================================
    # MANIFEST
    # =========================================================

    def save_status(
        self,
    ) -> Path:

        directory = (
            self.root
            / "runtime"
            / "media_engine"
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = (
            directory
            / "engine_status.json"
        )

        path.write_text(
            json.dumps(
                self.status(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _binary_exists(
        name: str,
    ) -> bool:

        import shutil

        return (
            shutil.which(name)
            is not None
        )


__all__ = [
    "AJVYRAAIMediaEngine",
]
