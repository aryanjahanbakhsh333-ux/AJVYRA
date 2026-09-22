from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ajvyra_cinematic_film_assembly_pipeline import (
    FilmSegment,
    AJVYRACinematicFilmAssemblyPipeline,
)


@dataclass
class RealFilmPipelineResult:
    film_id: str
    status: str
    movie_path: str | None
    segment_count: int
    duration_seconds: float
    error: str | None = None


class AJVYRACinematicRealFilmPipeline:

    def __init__(
        self,
        workspace: str | Path,
        runtime: Any,
        assembler: AJVYRACinematicFilmAssemblyPipeline,
    ) -> None:

        self.workspace = Path(workspace)
        self.runtime = runtime
        self.assembler = assembler

    def produce(
        self,
        film_id: str,
        scenes: list[Any],
    ) -> RealFilmPipelineResult:

        try:
            scene_results = self.runtime.generate_film(
                scenes
            )

            if not scene_results:
                raise RuntimeError(
                    "Film produced zero scenes."
                )

            if any(
                result.status != "COMPLETED"
                for result in scene_results
            ):
                failed = next(
                    result
                    for result in scene_results
                    if result.status != "COMPLETED"
                )

                raise RuntimeError(
                    f"Scene '{failed.scene_id}' failed: "
                    f"{failed.error}"
                )

            segments = []

            for index, result in enumerate(
                scene_results
            ):
                if not result.output_path:
                    raise RuntimeError(
                        f"Scene '{result.scene_id}' "
                        "has no output file."
                    )

                segments.append(
                    FilmSegment(
                        segment_id=result.scene_id,
                        file_path=result.output_path,
                        order=index,
                    )
                )

            output = (
                self.workspace
                / "films"
                / film_id
                / "master"
                / "movie.mp4"
            )

            assembly = self.assembler.assemble(
                film_id=film_id,
                segments=segments,
                output_path=output,
            )

            return RealFilmPipelineResult(
                film_id=film_id,
                status="COMPLETE",
                movie_path=assembly.output_path,
                segment_count=assembly.segment_count,
                duration_seconds=assembly.duration_seconds,
            )

        except Exception as exc:
            return RealFilmPipelineResult(
                film_id=film_id,
                status="FAILED",
                movie_path=None,
                segment_count=0,
                duration_seconds=0.0,
                error=str(exc),
            )
