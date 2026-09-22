from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

from ajvyra_cinematic_30_film_story_bible import (
    AJVYRACinematic30FilmStoryBible,
)
from ajvyra_cinematic_real_film_director import (
    AJVYRACinematicRealFilmDirector,
)
from ajvyra_cinematic_real_provider_bridge import (
    AJVYRACinematicRealProviderBridge,
    AJVYRABridgeRequest,
)


@dataclass(frozen=True)
class FilmGenerationJob:
    film_id: str
    title: str
    segment: int
    prompt: str
    output_path: str


class AJVYRACinematicReal30ProductionController:
    """
    Creates real generation jobs for all 30 films.

    This controller does not create fake MP4 files.
    Every completed job must originate from a real media provider.
    """

    def __init__(
        self,
        production_root: str | Path = "production/cinematic_anime",
        segment_duration: int = 8,
    ) -> None:
        self.production_root = Path(production_root)
        self.segment_duration = segment_duration

    def create_jobs(
        self,
        film_id: str | None = None,
        segment_count: int = 225,
    ) -> list[FilmGenerationJob]:
        stories = (
            [AJVYRACinematic30FilmStoryBible.get(film_id)]
            if film_id
            else list(
                AJVYRACinematic30FilmStoryBible.all()
            )
        )

        jobs: list[FilmGenerationJob] = []

        for story in stories:
            director = (
                AJVYRACinematicRealFilmDirector(story)
            )

            moments = director.build_segment_plan(
                segment_count=segment_count
            )

            film_root = (
                self.production_root /
                story.film_id /
                "segments"
            )

            film_root.mkdir(
                parents=True,
                exist_ok=True,
            )

            for moment in moments:
                output = (
                    film_root /
                    f"{moment.sequence:04d}.mp4"
                )

                jobs.append(
                    FilmGenerationJob(
                        film_id=story.film_id,
                        title=story.title,
                        segment=moment.sequence,
                        prompt=moment.prompt,
                        output_path=str(output),
                    )
                )

        return jobs

    def save_job_manifest(
        self,
        jobs: list[FilmGenerationJob],
        output: str | Path,
    ) -> Path:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)

        payload = [
            {
                "film_id": job.film_id,
                "title": job.title,
                "segment": job.segment,
                "prompt": job.prompt,
                "output_path": job.output_path,
                "status": "PENDING",
            }
            for job in jobs
        ]

        path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path
