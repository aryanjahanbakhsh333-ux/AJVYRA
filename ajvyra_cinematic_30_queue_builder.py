from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from ajvyra_cinematic_30_production_manifest import (
    AJVYRACinematic30ProductionManifest,
    CinematicFilmManifest,
)
from ajvyra_cinematic_production_scheduler import (
    AJVYRACinematicProductionScheduler,
)


@dataclass
class QueueBuildReport:
    films_added: int
    tasks_created: int
    manifest_path: str


class AJVYRACinematic30QueueBuilder:

    def __init__(
        self,
        root: str | Path = "cinematic_production",
    ):
        self.root = Path(root)

        self.manifest = (
            AJVYRACinematic30ProductionManifest(
                self.root
            )
        )

        self.scheduler = (
            AJVYRACinematicProductionScheduler(
                self.root / "queue"
            )
        )

    def add_film(
        self,
        film: CinematicFilmManifest,
    ) -> None:

        self.manifest.add(film)

        film_root = (
            Path(
                film.output_directory
            )
        )

        previous_task = None

        # Internal media tasks can later be mapped to
        # real provider outputs. The film remains the
        # top-level production unit.

        for index in range(1, 31):

            task_id = (
                f"{film.film_id}_chapter_{index:02d}"
            )

            output = (
                film_root
                / "media"
                / f"chapter_{index:02d}.mp4"
            )

            task = (
                self.scheduler.add_media_task(
                    task_id=task_id,
                    film_id=film.film_id,
                    prompt=(
                        f"Cinematic anime chapter "
                        f"{index} of {film.title}. "
                        f"Genre: {film.genre}. "
                        "Maintain character identity, "
                        "world continuity and emotional "
                        "progression."
                    ),
                    output_path=str(output),
                    duration_seconds=60,
                    dependencies=(
                        [previous_task]
                        if previous_task
                        else []
                    ),
                    priority=100 - index,
                    metadata={
                        "film_id": film.film_id,
                        "timeline_order": index,
                        "chapter": index,
                    },
                )
            )

            previous_task = task.task_id

    def build(
        self,
        films: Iterable[
            CinematicFilmManifest
        ],
    ) -> QueueBuildReport:

        for film in films:
            self.add_film(film)

        manifest_path = (
            self.manifest.save()
        )

        self.scheduler.save()

        return QueueBuildReport(
            films_added=self.manifest.count,
            tasks_created=len(
                self.scheduler.tasks
            ),
            manifest_path=str(
                manifest_path
            ),
        )
