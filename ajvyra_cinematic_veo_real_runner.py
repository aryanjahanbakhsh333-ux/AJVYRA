from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Any


@dataclass
class VeoGenerationRequest:
    prompt: str
    output_path: str
    model: str = "veo-3.1-generate-preview"
    aspect_ratio: str = "16:9"
    resolution: str = "720p"
    reference_images: Optional[list[Any]] = None
    first_frame: Optional[Any] = None
    last_frame: Optional[Any] = None


@dataclass
class VeoGenerationResult:
    status: str
    output_path: Optional[str]
    model: str
    operation_name: Optional[str]
    error: Optional[str] = None


class AJVYRACinematicVeoRealRunner:
    """
    Real Google Veo execution layer.

    This class never creates placeholder videos.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        poll_seconds: int = 10,
    ) -> None:
        self.api_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
        )

        self.poll_seconds = max(1, int(poll_seconds))

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY or GOOGLE_API_KEY is required."
            )

        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise RuntimeError(
                "Install the Google GenAI SDK first: "
                "pip install google-genai"
            ) from exc

        self._genai = genai
        self._types = types
        self.client = genai.Client(api_key=self.api_key)

    def generate(
        self,
        request: VeoGenerationRequest,
    ) -> VeoGenerationResult:

        if not request.prompt.strip():
            raise ValueError("Veo prompt cannot be empty.")

        output = Path(request.output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        config_kwargs = {
            "aspect_ratio": request.aspect_ratio,
            "resolution": request.resolution,
        }

        if request.reference_images:
            config_kwargs["reference_images"] = request.reference_images

        if request.last_frame is not None:
            config_kwargs["last_frame"] = request.last_frame

        config = self._types.GenerateVideosConfig(
            **config_kwargs
        )

        try:
            operation = self.client.models.generate_videos(
                model=request.model,
                prompt=request.prompt,
                image=request.first_frame,
                config=config,
            )

            operation_name = getattr(
                operation,
                "name",
                None,
            )

            while not operation.done:
                time.sleep(self.poll_seconds)
                operation = self.client.operations.get(
                    operation
                )

            if getattr(operation, "error", None):
                return VeoGenerationResult(
                    status="FAILED",
                    output_path=None,
                    model=request.model,
                    operation_name=operation_name,
                    error=str(operation.error),
                )

            response = operation.response

            generated_videos = getattr(
                response,
                "generated_videos",
                None,
            )

            if not generated_videos:
                raise RuntimeError(
                    "Veo completed but returned no generated video."
                )

            generated_video = generated_videos[0]

            video_file = getattr(
                generated_video,
                "video",
                None,
            )

            if video_file is None:
                raise RuntimeError(
                    "Veo response does not contain a video file."
                )

            self.client.files.download(
                file=video_file,
                destination=str(output),
            )

            if not output.exists():
                raise RuntimeError(
                    "Veo download completed without creating the MP4."
                )

            if output.stat().st_size <= 0:
                raise RuntimeError(
                    "Veo produced an empty MP4."
                )

            return VeoGenerationResult(
                status="COMPLETED",
                output_path=str(output),
                model=request.model,
                operation_name=operation_name,
            )

        except Exception as exc:
            return VeoGenerationResult(
                status="FAILED",
                output_path=None,
                model=request.model,
                operation_name=locals().get(
                    "operation_name"
                ),
                error=str(exc),
            )
