from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import time

from ajvyra_cinematic_real_provider_bridge import (
    AJVYRACinematicRealProviderBridge,
    AJVYRABridgeRequest,
)


@dataclass(frozen=True)
class RealGenerationResult:
    success: bool
    film_id: str
    segment: int
    output_path: str
    error: str | None = None


class AJVYRACinematicReal30GenerationRunner:
    """
    Executes actual video-generation jobs.

    Existing valid files are reused.
    Missing files are sent to the real provider.
    """

    def __init__(
        self,
        bridge: AJVYRACinematicRealProviderBridge,
        retries: int = 3,
        retry_delay: float = 5.0,
    ) -> None:
        self.bridge = bridge
        self.retries = max(1, retries)
        self.retry_delay = max(0.0, retry_delay)

    def run_job(
        self,
        film_id: str,
        segment: int,
        prompt: str,
        output_path: str | Path,
    ) -> RealGenerationResult:
        output = Path(output_path)
        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if self._valid_existing_file(output):
            return RealGenerationResult(
                success=True,
                film_id=film_id,
                segment=segment,
                output_path=str(output),
            )

        last_error: str | None = None

        for attempt in range(1, self.retries + 1):
            try:
                request = AJVYRABridgeRequest(
                    prompt=prompt,
                    output_path=str(output),
                    duration_seconds=8,
                    aspect_ratio="16:9",
                    resolution="720p",
                )

                result = self.bridge.generate(
                    request
                )

                generated = Path(
                    result.output_path
                )

                if not self._valid_existing_file(
                    generated
                ):
                    raise RuntimeError(
                        "Provider returned without a valid MP4."
                    )

                return RealGenerationResult(
                    success=True,
                    film_id=film_id,
                    segment=segment,
                    output_path=str(generated),
                )

            except Exception as exc:
                last_error = str(exc)

                if attempt < self.retries:
                    time.sleep(
                        self.retry_delay
                    )

        return RealGenerationResult(
            success=False,
            film_id=film_id,
            segment=segment,
            output_path=str(output),
            error=last_error,
        )

    @staticmethod
    def _valid_existing_file(
        path: Path,
    ) -> bool:
        return (
            path.is_file()
            and path.stat().st_size > 1024
            and path.suffix.lower() == ".mp4"
        )

    def run_manifest(
        self,
        manifest_path: str | Path,
    ) -> list[RealGenerationResult]:
        path = Path(manifest_path)

        payload = json.loads(
            path.read_text(encoding="utf-8")
        )

        if not isinstance(payload, list):
            raise ValueError(
                "Generation manifest must contain a list."
            )

        results: list[RealGenerationResult] = []

        for job in payload:
            result = self.run_job(
                film_id=str(job["film_id"]),
                segment=int(job["segment"]),
                prompt=str(job["prompt"]),
                output_path=str(
                    job["output_path"]
                ),
            )

            results.append(result)

            if not result.success:
                break

        return results
