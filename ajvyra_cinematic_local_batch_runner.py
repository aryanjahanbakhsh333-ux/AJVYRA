from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable

from ajvyra_cinematic_local_production_runner import (
    AJVYRACinematicLocalProductionRunner,
    LocalProductionResult,
)


class AJVYRACinematicLocalBatchRunner:
    """
    Batch executor for cinematic segments.

    A batch contains already-planned cinematic segments.
    It does not invent story content.
    """

    def __init__(
        self,
        runner: AJVYRACinematicLocalProductionRunner | None = None,
        output_root: str | Path = "production/cinematic_local",
    ) -> None:

        self.output_root = Path(output_root)

        self.runner = runner or (
            AJVYRACinematicLocalProductionRunner(
                output_root=self.output_root
            )
        )

    def run(
        self,
        film_id: str,
        film_title: str,
        segments: Iterable[Any],
        *,
        stop_on_error: bool = True,
        resume: bool = True,
        generation_options: dict[str, Any] | None = None,
    ) -> list[LocalProductionResult]:

        results: list[LocalProductionResult] = []

        options = generation_options or {}

        for index, segment in enumerate(segments, start=1):

            segment_id = self._segment_value(
                segment,
                "segment_id",
                f"segment_{index:04d}",
            )

            prompt = self._segment_value(
                segment,
                "prompt",
                "",
            )

            output_path = (
                self.output_root
                / film_id
                / "segments"
                / f"{segment_id}.mp4"
            )

            if resume and self._valid_file(output_path):

                result = LocalProductionResult(
                    film_id=film_id,
                    film_title=film_title,
                    segment_id=segment_id,
                    success=True,
                    output_path=str(output_path),
                    metadata_path=str(
                        output_path.with_suffix(
                            ".mp4.json"
                        )
                    ),
                    sha256=self._sha256(output_path),
                    elapsed_seconds=0.0,
                    error=None,
                )

                results.append(result)
                continue

            if not prompt:
                result = LocalProductionResult(
                    film_id=film_id,
                    film_title=film_title,
                    segment_id=segment_id,
                    success=False,
                    output_path=None,
                    metadata_path=None,
                    sha256=None,
                    elapsed_seconds=0.0,
                    error="Segment has no prompt.",
                )

                results.append(result)

                if stop_on_error:
                    break

                continue

            reference_image = self._segment_value(
                segment,
                "reference_image",
                None,
            )

            metadata = self._segment_metadata(
                segment
            )

            result = self.runner.run(
                film_id=film_id,
                film_title=film_title,
                segment_id=segment_id,
                prompt=prompt,
                reference_image=reference_image,
                metadata=metadata,
                **options,
            )

            results.append(result)

            if not result.success and stop_on_error:
                break

        self._save_batch_report(
            film_id,
            film_title,
            results,
        )

        return results

    def _save_batch_report(
        self,
        film_id: str,
        film_title: str,
        results: list[LocalProductionResult],
    ) -> Path:

        report_dir = (
            self.output_root
            / film_id
        )

        report_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        report_path = (
            report_dir
            / "batch_report.json"
        )

        successful = sum(
            1
            for result in results
            if result.success
        )

        payload = {
            "film_id": film_id,
            "film_title": film_title,
            "total_segments": len(results),
            "successful_segments": successful,
            "failed_segments": (
                len(results) - successful
            ),
            "complete": (
                len(results) > 0
                and successful == len(results)
            ),
            "segments": [
                asdict(result)
                for result in results
            ],
        }

        report_path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return report_path

    @staticmethod
    def _segment_value(
        segment: Any,
        name: str,
        default: Any,
    ) -> Any:

        if isinstance(segment, dict):
            value = segment.get(name)
        else:
            value = getattr(
                segment,
                name,
                None,
            )

        return (
            default
            if value is None
            else value
        )

    @staticmethod
    def _segment_metadata(
        segment: Any,
    ) -> dict[str, Any]:

        if isinstance(segment, dict):
            return {
                key: value
                for key, value in segment.items()
                if key not in {
                    "prompt",
                    "reference_image",
                }
            }

        if hasattr(segment, "__dict__"):
            return dict(segment.__dict__)

        return {}

    @staticmethod
    def _valid_file(
        path: Path,
    ) -> bool:

        return (
            path.exists()
            and path.is_file()
            and path.stat().st_size > 1024
        )

    @staticmethod
    def _sha256(
        path: Path,
    ) -> str:

        import hashlib

        digest = hashlib.sha256()

        with path.open("rb") as handle:

            while True:

                chunk = handle.read(1024 * 1024)

                if not chunk:
                    break

                digest.update(chunk)

        return digest.hexdigest()
