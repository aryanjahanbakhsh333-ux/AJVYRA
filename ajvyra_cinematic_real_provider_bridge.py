from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Optional
import json
import os


@dataclass
class AJVYRABridgeRequest:
    film_id: str
    segment_id: str
    prompt: str
    output_path: str

    model: str = "veo-3.1-generate-preview"
    duration_seconds: int = 8
    resolution: str = "720p"
    aspect_ratio: str = "16:9"

    first_frame: Optional[str] = None
    last_frame: Optional[str] = None
    reference_images: Optional[list[str]] = None

    metadata: Optional[dict[str, Any]] = None


@dataclass
class AJVYRABridgeResult:
    success: bool
    film_id: str
    segment_id: str
    output_path: Optional[str]
    error: Optional[str] = None
    provider: str = "veo"
    metadata: Optional[dict[str, Any]] = None


class AJVYRACinematicRealProviderBridge:
    """
    Bridge between AJVYRA's provider-neutral production system
    and the existing real Veo runner.
    """

    def __init__(self, veo_runner: Any):
        self.veo_runner = veo_runner

    def generate(self, request: dict[str, Any]) -> str:
        bridge_request = self._normalize(request)

        output = Path(bridge_request.output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        try:
            from ajvyra_cinematic_veo_real_runner import (
                VeoGenerationRequest,
            )
        except ImportError as exc:
            raise RuntimeError(
                "ajvyra_cinematic_veo_real_runner.py is required."
            ) from exc

        veo_request = VeoGenerationRequest(
            prompt=bridge_request.prompt,
            output_path=str(output),
            model=bridge_request.model,
            duration_seconds=bridge_request.duration_seconds,
            resolution=bridge_request.resolution,
            aspect_ratio=bridge_request.aspect_ratio,
            first_frame=bridge_request.first_frame,
            last_frame=bridge_request.last_frame,
            reference_images=bridge_request.reference_images or [],
        )

        result = self.veo_runner.generate(veo_request)

        path = self._extract_path(result)

        if not path:
            raise RuntimeError(
                f"Veo generation returned no usable output for "
                f"{bridge_request.film_id}/{bridge_request.segment_id}"
            )

        path = Path(path)

        if not path.exists():
            raise RuntimeError(
                f"Provider reported success but file does not exist: {path}"
            )

        if path.stat().st_size < 10_000:
            raise RuntimeError(
                f"Generated media is suspiciously small: {path}"
            )

        self._write_metadata(bridge_request, path)

        return str(path)

    def _normalize(self, request: dict[str, Any]) -> AJVYRABridgeRequest:
        if not isinstance(request, dict):
            raise TypeError("Provider request must be a dictionary.")

        film_id = str(request.get("film_id", "unknown-film"))
        segment_id = str(request.get("segment_id", "segment-0001"))

        output_path = request.get("output_path")

        if not output_path:
            output_path = (
                Path("public")
                / "cinematic_anime"
                / film_id
                / "segments"
                / f"{segment_id}.mp4"
            )

        return AJVYRABridgeRequest(
            film_id=film_id,
            segment_id=segment_id,
            prompt=str(request.get("prompt", "")).strip(),
            output_path=str(output_path),
            model=str(
                request.get(
                    "model",
                    os.getenv(
                        "AJVYRA_VEO_MODEL",
                        "veo-3.1-generate-preview",
                    ),
                )
            ),
            duration_seconds=int(request.get("duration_seconds", 8)),
            resolution=str(request.get("resolution", "720p")),
            aspect_ratio=str(request.get("aspect_ratio", "16:9")),
            first_frame=request.get("first_frame"),
            last_frame=request.get("last_frame"),
            reference_images=request.get("reference_images") or [],
            metadata=request.get("metadata") or {},
        )

    @staticmethod
    def _extract_path(result: Any) -> Optional[str]:
        if isinstance(result, str):
            return result

        if isinstance(result, Path):
            return str(result)

        if isinstance(result, dict):
            for key in ("output_path", "video_path", "path"):
                value = result.get(key)
                if value:
                    return str(value)

        for attr in ("output_path", "video_path", "path"):
            value = getattr(result, attr, None)
            if value:
                return str(value)

        return None

    @staticmethod
    def _write_metadata(
        request: AJVYRABridgeRequest,
        output: Path,
    ) -> None:
        metadata_path = output.with_suffix(".json")

        payload = {
            "film_id": request.film_id,
            "segment_id": request.segment_id,
            "provider": "veo",
            "model": request.model,
            "output_path": str(output),
            "metadata": request.metadata or {},
        }

        metadata_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
