from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Optional, Sequence


@dataclass
class MediaGenerationRequest:
    media_id: str
    media_type: str
    prompt: str
    output_path: str
    duration_seconds: float = 8.0
    aspect_ratio: str = "16:9"
    language: str = "en"
    reference_images: Sequence[str] = ()
    first_frame: Optional[str] = None
    last_frame: Optional[str] = None
    metadata: Dict[str, Any] | None = None


@dataclass
class MediaGenerationResult:
    media_id: str
    media_type: str
    status: str
    output_path: Optional[str]
    duration_seconds: float
    provider: str
    error: Optional[str] = None
    metadata: Dict[str, Any] | None = None


class AJVYRACinematicMediaProvider:
    """
    Provider-neutral contract.

    A provider must create real media or explicitly report failure.
    It must never silently create fake placeholder media.
    """

    provider_name = "abstract"

    def generate(
        self,
        request: MediaGenerationRequest,
    ) -> MediaGenerationResult:
        raise NotImplementedError


class AJVYRAUnavailableMediaProvider(
    AJVYRACinematicMediaProvider
):
    """
    Safe default.

    This intentionally fails instead of pretending that media
    was generated.
    """

    provider_name = "unavailable"

    def generate(
        self,
        request: MediaGenerationRequest,
    ) -> MediaGenerationResult:

        return MediaGenerationResult(
            media_id=request.media_id,
            media_type=request.media_type,
            status="failed",
            output_path=None,
            duration_seconds=0.0,
            provider=self.provider_name,
            error=(
                "No real media provider is configured. "
                "Configure a production provider before generation."
            ),
        )


class AJVYRAHTTPMediaProvider(
    AJVYRACinematicMediaProvider
):
    """
    Generic external provider adapter.

    The actual HTTP implementation is intentionally isolated here.
    AJVYRA's film engine does not need to know provider-specific APIs.
    """

    provider_name = "http"

    def __init__(
        self,
        endpoint: str,
        api_key_env: str = "AJVYRA_MEDIA_API_KEY",
        timeout_seconds: int = 1800,
    ):
        self.endpoint = endpoint
        self.api_key_env = api_key_env
        self.timeout_seconds = timeout_seconds

    def generate(
        self,
        request: MediaGenerationRequest,
    ) -> MediaGenerationResult:

        try:
            import urllib.request

            api_key = os.getenv(self.api_key_env)

            payload = {
                "media_id": request.media_id,
                "media_type": request.media_type,
                "prompt": request.prompt,
                "duration_seconds": request.duration_seconds,
                "aspect_ratio": request.aspect_ratio,
                "language": request.language,
                "reference_images": list(
                    request.reference_images
                ),
                "first_frame": request.first_frame,
                "last_frame": request.last_frame,
                "metadata": request.metadata or {},
            }

            body = json.dumps(payload).encode("utf-8")

            headers = {
                "Content-Type": "application/json",
            }

            if api_key:
                headers["Authorization"] = (
                    f"Bearer {api_key}"
                )

            http_request = urllib.request.Request(
                self.endpoint,
                data=body,
                headers=headers,
                method="POST",
            )

            with urllib.request.urlopen(
                http_request,
                timeout=self.timeout_seconds,
            ) as response:

                response_data = json.loads(
                    response.read().decode("utf-8")
                )

            output = response_data.get("output_path")

            if not output:
                raise RuntimeError(
                    "Provider returned no output_path."
                )

            return MediaGenerationResult(
                media_id=request.media_id,
                media_type=request.media_type,
                status="completed",
                output_path=output,
                duration_seconds=float(
                    response_data.get(
                        "duration_seconds",
                        request.duration_seconds,
                    )
                ),
                provider=self.provider_name,
                metadata=response_data,
            )

        except Exception as exc:
            return MediaGenerationResult(
                media_id=request.media_id,
                media_type=request.media_type,
                status="failed",
                output_path=None,
                duration_seconds=0.0,
                provider=self.provider_name,
                error=str(exc),
            )


class AJVYRAGeminiVeoMediaProvider(
    AJVYRACinematicMediaProvider
):
    """
    Real Gemini/Veo adapter.

    Requires:
        pip install google-genai

    Requires:
        GEMINI_API_KEY or GOOGLE_API_KEY

    The adapter deliberately lives outside the film engine.
    """

    provider_name = "google-veo"

    def __init__(
        self,
        model: Optional[str] = None,
    ):
        self.model = (
            model
            or os.getenv(
                "AJVYRA_VEO_MODEL",
                "veo-3.1-generate-preview",
            )
        )

    def generate(
        self,
        request: MediaGenerationRequest,
    ) -> MediaGenerationResult:

        try:
            from google import genai
            from google.genai import types

            api_key = (
                os.getenv("GEMINI_API_KEY")
                or os.getenv("GOOGLE_API_KEY")
            )

            if not api_key:
                raise RuntimeError(
                    "GEMINI_API_KEY or GOOGLE_API_KEY "
                    "is required."
                )

            client = genai.Client(
                api_key=api_key
            )

            config = types.GenerateVideosConfig(
                aspect_ratio=request.aspect_ratio,
            )

            if request.last_frame:
                last_frame = self._load_image(
                    request.last_frame
                )
                config.last_frame = last_frame

            primary_image = None

            if request.first_frame:
                primary_image = self._load_image(
                    request.first_frame
                )

            operation = client.models.generate_videos(
                model=self.model,
                prompt=request.prompt,
                image=primary_image,
                config=config,
            )

            while not operation.done:
                time.sleep(10)
                operation = client.operations.get(
                    operation
                )

            generated = (
                operation.response
                .generated_videos[0]
            )

            output = Path(request.output_path)
            output.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            client.files.download(
                file=generated.video,
                download_path=str(output),
            )

            if not output.exists():
                raise RuntimeError(
                    "Veo completed but output file "
                    "was not created."
                )

            return MediaGenerationResult(
                media_id=request.media_id,
                media_type=request.media_type,
                status="completed",
                output_path=str(output),
                duration_seconds=request.duration_seconds,
                provider=self.provider_name,
                metadata={
                    "model": self.model,
                },
            )

        except Exception as exc:
            return MediaGenerationResult(
                media_id=request.media_id,
                media_type=request.media_type,
                status="failed",
                output_path=None,
                duration_seconds=0.0,
                provider=self.provider_name,
                error=str(exc),
            )

    @staticmethod
    def _load_image(path: str):
        from google.genai import types

        data = Path(path).read_bytes()

        suffix = Path(path).suffix.lower()

        mime = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
        }.get(
            suffix,
            "image/png",
        )

        return types.Image(
            image_bytes=data,
            mime_type=mime,
        )


class AJVYRACinematicMediaBackend:

    def __init__(
        self,
        provider: Optional[
            AJVYRACinematicMediaProvider
        ] = None,
    ):
        self.provider = (
            provider
            or AJVYRAUnavailableMediaProvider()
        )

    def generate(
        self,
        request: MediaGenerationRequest,
    ) -> MediaGenerationResult:

        result = self.provider.generate(request)

        if result.status == "completed":
            if not result.output_path:
                raise RuntimeError(
                    "Provider reported completion "
                    "without an output path."
                )

            if not Path(result.output_path).exists():
                raise RuntimeError(
                    "Provider reported completion "
                    "but media file does not exist."
                )

        return result

    @staticmethod
    def fingerprint(path: str | Path) -> str:
        file_path = Path(path)

        digest = hashlib.sha256()

        with file_path.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                digest.update(chunk)

        return digest.hexdigest()
