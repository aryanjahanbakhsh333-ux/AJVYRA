from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from ajvyra_local_video_generation_engine import (
    AJVYRALocalVideoGenerationEngine,
    AJVYRALocalVideoGenerationRequest,
)


@dataclass
class CinematicLocalModelRequest:
    film_id: str
    film_title: str
    segment_id: str

    prompt: str

    output_path: Path

    duration_seconds: float = 5.0
    width: int = 832
    height: int = 480
    fps: int = 16
    num_frames: int = 81

    seed: Optional[int] = None

    reference_image: Optional[Path] = None

    negative_prompt: str = (
        "low quality, blurry, deformed anatomy, malformed hands, "
        "extra fingers, duplicate characters, inconsistent face, "
        "inconsistent clothing, watermark, text, logo"
    )

    metadata: Dict[str, Any] = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}


@dataclass
class CinematicLocalModelResult:
    film_id: str
    film_title: str
    segment_id: str

    success: bool

    output_path: Optional[str]
    error: Optional[str]

    elapsed_seconds: float
    sha256: Optional[str]

    metadata_path: Optional[str]


class AJVYRACinematicLocalModelBridge:
    """
    Bridge between the AJVYRA cinematic production system
    and the local Wan2.1 video generation engine.

    This class does NOT fabricate media.

    If the local model cannot actually generate a video,
    the request fails explicitly.
    """

    def __init__(
        self,
        engine: Optional[AJVYRALocalVideoGenerationEngine] = None,
    ) -> None:
        self.engine = engine or AJVYRALocalVideoGenerationEngine()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def generate(
        self,
        request: CinematicLocalModelRequest,
    ) -> CinematicLocalModelResult:

        started = time.time()

        output_path = Path(request.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            self._validate_request(request)

            engine_request = self._build_engine_request(request)

            result = self.engine.generate(engine_request)

            elapsed = time.time() - started

            actual_path = self._extract_output_path(result)

            if actual_path is None:
                raise RuntimeError(
                    "Local video engine completed without returning "
                    "an output video path."
                )

            actual_path = Path(actual_path)

            if not actual_path.exists():
                raise RuntimeError(
                    f"Local video engine reported an output that does not exist: "
                    f"{actual_path}"
                )

            if actual_path.stat().st_size <= 1024:
                raise RuntimeError(
                    f"Generated video is too small to be considered valid: "
                    f"{actual_path}"
                )

            checksum = self._sha256(actual_path)

            metadata_path = self._write_metadata(
                request=request,
                actual_path=actual_path,
                elapsed_seconds=elapsed,
                checksum=checksum,
            )

            return CinematicLocalModelResult(
                film_id=request.film_id,
                film_title=request.film_title,
                segment_id=request.segment_id,
                success=True,
                output_path=str(actual_path),
                error=None,
                elapsed_seconds=elapsed,
                sha256=checksum,
                metadata_path=str(metadata_path),
            )

        except Exception as exc:
            elapsed = time.time() - started

            return CinematicLocalModelResult(
                film_id=request.film_id,
                film_title=request.film_title,
                segment_id=request.segment_id,
                success=False,
                output_path=None,
                error=str(exc),
                elapsed_seconds=elapsed,
                sha256=None,
                metadata_path=None,
            )

    # ---------------------------------------------------------
    # Batch generation
    # ---------------------------------------------------------

    def generate_many(
        self,
        requests: Iterable[CinematicLocalModelRequest],
        stop_on_error: bool = True,
    ) -> list[CinematicLocalModelResult]:

        results: list[CinematicLocalModelResult] = []

        for request in requests:
            result = self.generate(request)
            results.append(result)

            if stop_on_error and not result.success:
                break

        return results

    # ---------------------------------------------------------
    # Cinematic request conversion
    # ---------------------------------------------------------

    def from_segment(
        self,
        *,
        film_id: str,
        film_title: str,
        segment_id: str,
        segment: Any,
        output_path: Path,
        continuity_prompt: str = "",
        reference_image: Optional[Path] = None,
        seed: Optional[int] = None,
    ) -> CinematicLocalModelRequest:

        prompt_parts: list[str] = []

        prompt_parts.append(
            "Cinematic anime film shot."
        )

        prompt_parts.append(
            f"Film: {film_title}."
        )

        prompt_parts.append(
            f"Segment: {segment_id}."
        )

        segment_prompt = self._read_segment_value(
            segment,
            "prompt",
        )

        if segment_prompt:
            prompt_parts.append(segment_prompt)

        chapter = self._read_segment_value(
            segment,
            "chapter",
        )

        if chapter:
            prompt_parts.append(
                f"Chapter atmosphere: {chapter}."
            )

        scene = self._read_segment_value(
            segment,
            "scene",
        )

        if scene:
            prompt_parts.append(
                f"Scene: {scene}."
            )

        emotion = self._read_segment_value(
            segment,
            "emotion",
        )

        if emotion:
            prompt_parts.append(
                f"Emotion: {emotion}."
            )

        camera = self._read_segment_value(
            segment,
            "camera",
        )

        if camera:
            prompt_parts.append(
                f"Camera language: {camera}."
            )

        lighting = self._read_segment_value(
            segment,
            "lighting",
        )

        if lighting:
            prompt_parts.append(
                f"Lighting: {lighting}."
            )

        action = self._read_segment_value(
            segment,
            "action",
        )

        if action:
            prompt_parts.append(
                f"Character action: {action}."
            )

        if continuity_prompt:
            prompt_parts.append(
                "Character and world continuity: "
                + continuity_prompt
            )

        prompt_parts.append(
            "Maintain consistent character identity, clothing, "
            "hair, face structure, environment, lighting direction "
            "and cinematic visual language throughout the shot."
        )

        prompt_parts.append(
            "High-quality anime cinematography, controlled motion, "
            "natural camera movement, coherent anatomy, "
            "strong composition, cinematic depth."
        )

        prompt = " ".join(
            part.strip()
            for part in prompt_parts
            if part and part.strip()
        )

        return CinematicLocalModelRequest(
            film_id=film_id,
            film_title=film_title,
            segment_id=segment_id,
            prompt=prompt,
            output_path=output_path,
            reference_image=reference_image,
            seed=seed,
            metadata={
                "source": "AJVYRA cinematic segment planner",
                "continuity_enabled": bool(continuity_prompt),
                "segment_type": type(segment).__name__,
            },
        )

    # ---------------------------------------------------------
    # Engine adapter
    # ---------------------------------------------------------

    def _build_engine_request(
        self,
        request: CinematicLocalModelRequest,
    ) -> AJVYRALocalVideoGenerationRequest:

        return AJVYRALocalVideoGenerationRequest(
            prompt=request.prompt,
            output_path=request.output_path,
            negative_prompt=request.negative_prompt,
            width=request.width,
            height=request.height,
            fps=request.fps,
            num_frames=request.num_frames,
            seed=request.seed,
            reference_image=request.reference_image,
        )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def _validate_request(
        self,
        request: CinematicLocalModelRequest,
    ) -> None:

        if not request.film_id.strip():
            raise ValueError("film_id cannot be empty.")

        if not request.film_title.strip():
            raise ValueError("film_title cannot be empty.")

        if not request.segment_id.strip():
            raise ValueError("segment_id cannot be empty.")

        if not request.prompt.strip():
            raise ValueError("prompt cannot be empty.")

        if request.width <= 0:
            raise ValueError("width must be positive.")

        if request.height <= 0:
            raise ValueError("height must be positive.")

        if request.fps <= 0:
            raise ValueError("fps must be positive.")

        if request.num_frames <= 1:
            raise ValueError(
                "num_frames must be greater than one."
            )

        if request.duration_seconds <= 0:
            raise ValueError(
                "duration_seconds must be positive."
            )

        if request.reference_image is not None:
            reference = Path(request.reference_image)

            if not reference.exists():
                raise FileNotFoundError(
                    f"Reference image does not exist: {reference}"
                )

    # ---------------------------------------------------------
    # Result extraction
    # ---------------------------------------------------------

    def _extract_output_path(
        self,
        result: Any,
    ) -> Optional[str]:

        if result is None:
            return None

        if isinstance(result, (str, Path)):
            return str(result)

        for name in (
            "output_path",
            "video_path",
            "path",
            "file_path",
        ):
            value = getattr(result, name, None)

            if value:
                return str(value)

        if isinstance(result, dict):
            for name in (
                "output_path",
                "video_path",
                "path",
                "file_path",
            ):
                value = result.get(name)

                if value:
                    return str(value)

        return None

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def _write_metadata(
        self,
        *,
        request: CinematicLocalModelRequest,
        actual_path: Path,
        elapsed_seconds: float,
        checksum: str,
    ) -> Path:

        metadata_path = actual_path.with_suffix(
            actual_path.suffix + ".json"
        )

        payload = {
            "film_id": request.film_id,
            "film_title": request.film_title,
            "segment_id": request.segment_id,
            "output_path": str(actual_path),
            "prompt": request.prompt,
            "negative_prompt": request.negative_prompt,
            "width": request.width,
            "height": request.height,
            "fps": request.fps,
            "num_frames": request.num_frames,
            "duration_seconds": request.duration_seconds,
            "seed": request.seed,
            "reference_image": (
                str(request.reference_image)
                if request.reference_image
                else None
            ),
            "elapsed_seconds": elapsed_seconds,
            "sha256": checksum,
            "metadata": request.metadata,
        }

        metadata_path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return metadata_path

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _read_segment_value(
        segment: Any,
        name: str,
    ) -> str:

        if isinstance(segment, dict):
            value = segment.get(name)
        else:
            value = getattr(segment, name, None)

        if value is None:
            return ""

        return str(value)

    @staticmethod
    def _sha256(path: Path) -> str:

        digest = hashlib.sha256()

        with path.open("rb") as file:
            while True:
                chunk = file.read(1024 * 1024)

                if not chunk:
                    break

                digest.update(chunk)

        return digest.hexdigest()


__all__ = [
    "CinematicLocalModelRequest",
    "CinematicLocalModelResult",
    "AJVYRACinematicLocalModelBridge",
]
