from __future__ import annotations

import hashlib
import inspect
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Optional


@dataclass
class LocalProductionResult:
    film_id: str
    film_title: str
    segment_id: str
    success: bool
    output_path: Optional[str]
    metadata_path: Optional[str]
    sha256: Optional[str]
    elapsed_seconds: float
    error: Optional[str]


class AJVYRACinematicLocalProductionRunner:
    """
    Executes one real cinematic segment through the existing
    AJVYRA local video generation engine.

    This class never creates fake media.
    """

    def __init__(
        self,
        generation_engine: Any | None = None,
        output_root: str | Path = "production/cinematic_local",
    ) -> None:

        self.output_root = Path(output_root)

        if generation_engine is None:
            from ajvyra_local_video_generation_engine import (
                AJVYRALocalVideoGenerationEngine,
            )

            generation_engine = AJVYRALocalVideoGenerationEngine()

        self.engine = generation_engine

    def run(
        self,
        film_id: str,
        film_title: str,
        segment_id: str,
        prompt: str,
        *,
        negative_prompt: str = (
            "low quality, blurry, deformed anatomy, "
            "bad hands, extra fingers, duplicate characters, "
            "inconsistent face, inconsistent clothing, "
            "watermark, logo, text"
        ),
        reference_image: str | Path | None = None,
        width: int = 832,
        height: int = 480,
        fps: int = 16,
        num_frames: int = 81,
        seed: int | None = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> LocalProductionResult:

        started = time.time()

        output_path = (
            self.output_root
            / film_id
            / "segments"
            / f"{segment_id}.mp4"
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            if not film_id.strip():
                raise ValueError("film_id is empty.")

            if not film_title.strip():
                raise ValueError("film_title is empty.")

            if not segment_id.strip():
                raise ValueError("segment_id is empty.")

            if not prompt.strip():
                raise ValueError("prompt is empty.")

            if num_frames < 5:
                raise ValueError(
                    "num_frames must be at least 5."
                )

            if (num_frames - 1) % 4 != 0:
                raise ValueError(
                    "Wan2.1 requires num_frames to satisfy "
                    "(num_frames - 1) % 4 == 0."
                )

            request = self._create_generation_request(
                prompt=prompt,
                output_path=output_path,
                negative_prompt=negative_prompt,
                reference_image=reference_image,
                width=width,
                height=height,
                fps=fps,
                num_frames=num_frames,
                seed=seed,
            )

            raw_result = self._execute(request)

            actual_output = self._extract_output_path(
                raw_result
            )

            if actual_output is None:
                actual_output = output_path

            actual_output = Path(actual_output)

            if not actual_output.exists():
                raise RuntimeError(
                    "Video generation returned successfully, "
                    "but no MP4 file exists."
                )

            if actual_output.stat().st_size <= 1024:
                raise RuntimeError(
                    "Generated MP4 is too small to be valid."
                )

            checksum = self._sha256(actual_output)

            elapsed = time.time() - started

            metadata_path = (
                actual_output.with_suffix(
                    actual_output.suffix + ".json"
                )
            )

            payload = {
                "film_id": film_id,
                "film_title": film_title,
                "segment_id": segment_id,
                "success": True,
                "output_path": str(actual_output),
                "sha256": checksum,
                "elapsed_seconds": elapsed,
                "generation": {
                    "width": width,
                    "height": height,
                    "fps": fps,
                    "num_frames": num_frames,
                    "seed": seed,
                    "reference_image": (
                        str(reference_image)
                        if reference_image
                        else None
                    ),
                },
                "metadata": metadata or {},
            }

            metadata_path.write_text(
                json.dumps(
                    payload,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            return LocalProductionResult(
                film_id=film_id,
                film_title=film_title,
                segment_id=segment_id,
                success=True,
                output_path=str(actual_output),
                metadata_path=str(metadata_path),
                sha256=checksum,
                elapsed_seconds=elapsed,
                error=None,
            )

        except Exception as exc:

            return LocalProductionResult(
                film_id=film_id,
                film_title=film_title,
                segment_id=segment_id,
                success=False,
                output_path=None,
                metadata_path=None,
                sha256=None,
                elapsed_seconds=time.time() - started,
                error=str(exc),
            )

    def _create_generation_request(
        self,
        *,
        prompt: str,
        output_path: Path,
        negative_prompt: str,
        reference_image: str | Path | None,
        width: int,
        height: int,
        fps: int,
        num_frames: int,
        seed: int | None,
    ) -> Any:

        from ajvyra_local_video_generation_engine import (
            AJVYRALocalVideoGenerationRequest,
        )

        values = {
            "prompt": prompt,
            "output_path": output_path,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "fps": fps,
            "num_frames": num_frames,
            "seed": seed,
            "reference_image": (
                Path(reference_image)
                if reference_image
                else None
            ),
        }

        return self._construct_compatible_dataclass(
            AJVYRALocalVideoGenerationRequest,
            values,
        )

    @staticmethod
    def _construct_compatible_dataclass(
        cls: Any,
        values: dict[str, Any],
    ) -> Any:

        signature = inspect.signature(cls)

        accepted: dict[str, Any] = {}

        for name, parameter in signature.parameters.items():

            if name in values:
                accepted[name] = values[name]

        return cls(**accepted)

    def _execute(self, request: Any) -> Any:

        if hasattr(self.engine, "generate"):
            return self.engine.generate(request)

        if hasattr(self.engine, "run"):
            return self.engine.run(request)

        raise AttributeError(
            "Local video generation engine has neither "
            "'generate' nor 'run'."
        )

    @staticmethod
    def _extract_output_path(
        result: Any,
    ) -> str | None:

        if result is None:
            return None

        if isinstance(result, (str, Path)):
            return str(result)

        if isinstance(result, dict):

            for key in (
                "output_path",
                "video_path",
                "path",
                "file_path",
            ):
                value = result.get(key)

                if value:
                    return str(value)

        for key in (
            "output_path",
            "video_path",
            "path",
            "file_path",
        ):

            value = getattr(result, key, None)

            if value:
                return str(value)

        return None

    @staticmethod
    def _sha256(path: Path) -> str:

        digest = hashlib.sha256()

        with path.open("rb") as handle:

            while True:

                chunk = handle.read(1024 * 1024)

                if not chunk:
                    break

                digest.update(chunk)

        return digest.hexdigest()
